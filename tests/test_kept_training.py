import ast
import json
from pathlib import Path
import tempfile
import unittest
from vision.yolo.kept_training import settings, validate_split, check_resume, choose_thresholds, operating_metrics, select_final


class KeptTrainingTests(unittest.TestCase):
    def test_unlocked_data_rejected(self):
        with self.assertRaisesRegex(ValueError,'not approved'):
            validate_split('.',None)

    def test_experiments_and_gentle(self):
        self.assertEqual(settings()['weights'],'yolo11n.pt')
        self.assertEqual(settings('s',True,43,8)['mosaic'],.25)
        with self.assertRaises(ValueError): settings(seed=45)

    def test_resume_requires_same_identity_and_checkpoint(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            (p/'run_identity.json').write_text(json.dumps({'dataset':'one'}))
            with self.assertRaises(ValueError):check_resume(p,{'dataset':'two'})
            with self.assertRaises(ValueError):check_resume(p,{'dataset':'one'})

    def test_threshold_bbox_matching_includes_empty_prediction_images(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);gt=root/'gt';pr=root/'pred';gt.mkdir();pr.mkdir()
            (gt/'a.txt').write_text('1 .5 .5 .2 .2\n')
            (gt/'b.txt').write_text('1 .5 .5 .2 .2\n')
            (pr/'a.txt').write_text('1 .5 .5 .2 .2 .8\n1 .1 .1 .1 .1 .1\n')
            selected=choose_thresholds(gt,pr)
            self.assertEqual(selected['Ripped']['tp'],1)
            self.assertEqual(selected['Ripped']['fn'],1)
            self.assertEqual(selected['Ripped']['fp'],0)
            self.assertGreater(selected['Ripped']['threshold'],.1)

    def test_notebook_code_compiles_and_unlocked_gate_is_present(self):
        root=Path(__file__).resolve().parents[1]
        nb=json.loads((root/'notebooks/three_kept_colab.ipynb').read_text(encoding='utf-8'))
        code='\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code')
        # The released notebook must bind the independently shipped real split lock.
        expected = json.loads((root/'configs/three-kept-r07.lock.json').read_text())
        binding = next(n for n in ast.parse(code.replace('%pip install -q ultralytics==8.4.208','')).body
                       if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXPECTED' for t in n.targets))
        self.assertEqual(ast.literal_eval(binding.value),expected)
        self.assertIn("assert EXPECTED and EXPECTED.get('zip_sha256')",code)
        self.assertIn('check_resume',code)
        for cell in nb['cells']:
            if cell['cell_type']=='code':
                ast.parse('\n'.join(l for l in ''.join(cell['source']).splitlines() if not l.startswith('%')))

    def test_finalist_requires_three_seeds_and_prefers_small_within_variation(self):
        rows=[dict(complete=True,dataset_version='v1',mean=.61,stdev=.03,model='s',gentle=False),
              dict(complete=True,dataset_version='v1',mean=.60,stdev=.03,model='n',gentle=False)]
        self.assertEqual(select_final(rows)['model'],'n')
        rows[0]['mean']=.8
        self.assertEqual(select_final(rows)['model'],'s')
        rows[1]['complete']=False
        with self.assertRaises(ValueError):select_final(rows)
