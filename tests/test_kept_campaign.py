"""Source ZIP conversion, approval gates, deterministic group split and tamper rejection."""
import csv
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
import io
from PIL import Image
from vision.yolo import kept


class KeptCampaignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.archive = self.base / 'source.zip'
        with zipfile.ZipFile(self.archive, 'w') as z:
            z.writestr('data.yaml', 'names: ' + repr(kept.SOURCE_CLASSES))
            for part in ('train', 'valid', 'test'):
                for i in range(6):
                    stream = io.BytesIO()
                    Image.new('RGB', (40,40), (i*30, ['train','valid','test'].index(part)*70, 20)).save(stream, format='JPEG')
                    z.writestr(f'{part}/images/{i}.jpg', stream.getvalue())
                    z.writestr(f'{part}/labels/{i}.txt', '\n'.join(f'{c} .5 .5 .2 .2' for c in range(6)))
        self.root = self.base / 'campaign'
        kept.convert(self.archive, self.root)

    def approve(self):
        path = self.root / 'review/review.csv'
        with path.open(encoding='utf-8') as stream:
            rows = list(csv.DictReader(stream))
        for i, r in enumerate(rows):
            r.update(group_id=f'g{i//2}', label_review='approved', reason='fixture visual evidence')
        with path.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=kept.FIELDS)
            w.writeheader()
            w.writerows(rows)

    def test_drop_notch_mapping_and_source_immutable(self):
        m, _ = kept.audit(self.root)
        self.assertEqual([s.split()[0] for s in m['records'][0]['labels']], ['0','1','2'])
        self.assertEqual(kept.statistics(m)['boxes'], 54)
        self.assertEqual(kept.sha(self.archive), kept.sha(self.root/'source.zip'))
        with self.assertRaises(ValueError):
            kept.convert(self.archive, self.root)

    def test_unreviewed_cannot_split(self):
        with self.assertRaisesRegex(ValueError, 'three independent'):
            kept.propose(self.root, self.base/'plan')

    def test_split_deterministic_and_no_group_leakage(self):
        self.approve()
        a = kept.propose(self.root, self.base/'a')
        b = kept.propose(self.root, self.base/'b')
        self.assertEqual(a, b)
        groups = [{r['group_id'] for r in rs} for rs in a['assignment'].values()]
        self.assertFalse(any(x & y for i,x in enumerate(groups) for y in groups[i+1:]))
        self.assertEqual(sum(a['counts'].values()), 18)

    def test_label_tamper_rejected(self):
        next((self.root/'review/labels').iterdir()).write_text('')
        with self.assertRaisesRegex(ValueError, 'Labels changed'):
            kept.audit(self.root)

    def test_negative_balance_is_part_of_split_selection(self):
        """Class-balanced candidates can still concentrate healthy images in one split."""
        import random
        from unittest.mock import patch
        rng = random.Random(0)
        records, rows = [], []
        for i in range(48):
            negative = i % 4 == 0
            lines = ['0 .5 .5 .2 .2'] * rng.randint(1, 3)
            if not negative:
                lines += ['1 .5 .5 .2 .2'] * rng.randint(1, 5)
                lines += ['2 .5 .5 .2 .2'] * rng.randint(1, 9)
            records.append(dict(image_id=f'i{i}', image_file=f'i{i}.jpg',
                                image_sha256=f'{i:064x}', labels=lines,
                                negative_candidate=negative))
            rows.append(dict(image_id=f'i{i}', group_id=f'g{i}', label_review='approved',
                             negative_review='approved' if negative else 'not_needed',
                             reason='synthetic split-selection fixture'))
        manifest = dict(dataset_version='synthetic', records=records)
        with patch.object(kept, 'audit', return_value=(manifest, rows)), patch.object(kept, 'gallery'):
            plan = kept.propose(self.root, self.base / 'negative-balanced')
        self.assertEqual(plan['negative_counts'], dict(train=8, val=2, test=2))
        self.assertTrue(all(set(counts) == set(kept.CLASSES)
                            for counts in plan['class_counts'].values()))

    def test_same_names_wrong_profile_rejected(self):
        path = self.root/'review/manifest.json'
        m = kept.read(path)
        m['taxonomy_profile'] = 'book-three-v1'
        kept.write(path, m)
        with self.assertRaisesRegex(ValueError, 'Wrong taxonomy'):
            kept.audit(self.root)

    def test_archive_traversal_rejected(self):
        with zipfile.ZipFile(self.archive, 'w') as z:
            z.writestr('../escape.txt', 'bad')
        with self.assertRaisesRegex(ValueError, 'Unsafe archive'):
            kept.convert(self.archive, self.base/'unsafe')

    def test_lock_requires_exact_approval(self):
        self.approve()
        # Fixtures have placeholder image bytes; gallery needs actual images.
        from unittest.mock import patch
        with patch.object(kept, 'gallery'):
            plan = kept.propose(self.root, self.base/'plan')
            approval = self.base/'approval.json'
            kept.write(approval, dict(approved=True, reviewer='User', plan_sha256='wrong'))
            with self.assertRaisesRegex(ValueError, 'Explicit user approval'):
                kept.lock(self.root,self.base/'plan',self.base/'locked',approval)
            kept.write(approval, dict(approved=True, reviewer='User', plan_sha256=plan['plan_sha256']))
            report = kept.lock(self.root,self.base/'plan',self.base/'locked',approval)
        self.assertTrue(report['split_ready'])
        self.assertNotIn('test:', (self.base/'locked/data.yaml').read_text())
        from vision.yolo.kept_training import validate_split
        validate_split(self.base/'locked',kept.read(str(self.base/'locked')+'.lock.json'))

    def test_revision_resets_review_and_replays_from_zip(self):
        m,_=kept.audit(self.root)
        r=m['records'][0]
        patch=self.base/'patches.json'
        kept.write(patch,[dict(image_id=r['image_id'],before_sha256=kept.digest(r['labels']),
                               labels=[],actor='Fixture',reason='Known wrong bbox')])
        output=self.base/'revised'
        kept.revise(self.root,output,patch)
        revised,reviews=kept.audit(output)
        self.assertEqual(revised['records'][0]['labels'],[])
        self.assertEqual(reviews[0]['negative_review'],'pending')
        self.assertEqual(kept.audit(self.root)[0]['records'][0]['labels'],r['labels'])


if __name__ == '__main__':
    unittest.main()
