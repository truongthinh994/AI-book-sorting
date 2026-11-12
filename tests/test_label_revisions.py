"""Provenance, negative-review invalidation and immutable label versions."""
import csv
import json
from pathlib import Path
import tempfile
import unittest

from vision.yolo.prepare import audit, prepare, sha256, write_json
from vision.yolo.revisions import label_hash, revise, revision_version


class RevisionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.base, self.output = [self.root / name for name in ("source", "base", "revised")]
        self.source.mkdir()
        (self.source / "data.yaml").write_text("names: ['Barcode', 'Notch', 'Ripped', 'Spot', 'Tag', 'Wornout']")
        for part in ("train", "valid", "test"):
            for kind in ("images", "labels"):
                (self.source / part / kind).mkdir(parents=True)
        for n in range(2):
            (self.source / f"train/images/book{n}.jpg").write_bytes(bytes([n]))
            (self.source / f"train/labels/book{n}.txt").write_text("2 .5 .5 .2 .2\n")
        self.manifest = prepare(self.source, self.base)
        self.id = self.manifest["records"][0]["image_id"]
        with (self.base / "review.csv").open(encoding="utf-8", newline="") as stream:
            self.reviews = list(csv.DictReader(stream))
        for r in self.reviews:
            r.update(group_id="same_book", label_review="approved")
        with (self.base / "review.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=self.reviews[0].keys())
            writer.writeheader()
            writer.writerows(self.reviews)

    def change(self, **values):
        result = dict(image_id=self.id, before_sha256=label_hash(self.manifest["records"][0]["labels"]),
                      labels=[], reason="Synthetic wrong box removed", reviewer="fixture-reviewer")
        result.update(values)
        return result

    def create(self, changes=None, **kwargs):
        return revise(self.source, self.base, self.output,
                      [self.change()] if changes is None else changes, **kwargs)

    def test_source_unchanged_and_audit_replays_history(self):
        before = {p: sha256(p) for directory in (self.source, self.base)
                  for p in directory.rglob("*") if p.is_file()}
        result = self.create()
        self.assertEqual({p: sha256(p) for p in before}, before)
        self.assertEqual(result["statistics"]["empty_labels"], 1)
        self.assertEqual(result["statistics"]["Ripped"], 1)
        self.assertTrue(result["records"][0]["negative_candidate"])
        self.assertEqual(audit(self.source, self.output)["status"], "PASS")
        with (self.output / "review.csv").open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(rows[0]["label_review"], "pending")
        self.assertEqual(rows[0]["negative_review"], "pending")
        self.assertEqual(rows[0]["group_id"], "same_book")
        self.assertEqual(rows[1]["label_review"], "approved")

    def test_restart_review_does_not_inherit_approvals(self):
        self.create([], restart_review=True)
        with (self.output / "review.csv").open(newline="") as stream:
            self.assertTrue(all(r["label_review"] == "pending" for r in csv.DictReader(stream)))

    def test_multiple_revisions_replay_from_original(self):
        first = self.create()
        patch = self.change(labels=["0 .5 .5 .3 .3"], before_sha256=label_hash([]))
        second_root = self.root / "second"
        second = revise(self.source, self.output, second_root, [patch])
        self.assertEqual(len(second["label_revisions"]), 2)
        self.assertNotEqual(first["dataset_version"], second["dataset_version"])
        self.assertEqual(audit(self.source, second_root)["status"], "PASS")

    def test_bad_change_never_creates_output(self):
        for update in [dict(before_sha256="0"*64), dict(image_id="../escape"),
                       dict(reviewer=""), dict(reason=" "), dict(labels=["5 .5 .5 .2 .2"]),
                       dict(labels=["1 nan .5 .2 .2"]), dict(labels=["1 .1 .5 .8 .2"]),
                       dict(labels=["1 .5 .5 0 .2"]), dict(labels=["2 .5 .5 .2 .2"]),
                       dict(labels=["0 .5 .5 .2 .2", "0 .5 .5 .2 .2"])]:
            with self.subTest(update=update), self.assertRaises(ValueError):
                self.create([self.change(**update)])
            self.assertFalse(self.output.exists())

    def test_duplicate_changes_rejected(self):
        with self.assertRaises(ValueError):
            self.create([self.change(), self.change()])
        self.assertFalse(self.output.exists())

    def test_existing_version_never_overwritten(self):
        self.create()
        with self.assertRaises(ValueError):
            self.create()

    def test_changed_prepared_label_rejected(self):
        (self.base / "labels" / (self.id+".txt")).write_text("")
        with self.assertRaises(ValueError):
            self.create()
        self.assertFalse(self.output.exists())

    def test_replay_rejects_wrong_before_even_if_version_recomputed(self):
        result = self.create()
        result["label_revisions"][0]["before_sha256"] = "0"*64
        result["dataset_version"] = revision_version(result)
        write_json(self.output / "manifest.json", result)
        with self.assertRaisesRegex(ValueError, "before checksum"):
            audit(self.source, self.output)

    def test_history_or_image_tampering_rejected(self):
        result = self.create()
        result["label_revisions"][0]["reason"] += "tampered"
        write_json(self.output / "manifest.json", result)
        with self.assertRaisesRegex(ValueError, "version mismatch"):
            audit(self.source, self.output)

    def test_destination_inside_parent_rejected(self):
        with self.assertRaises(ValueError):
            revise(self.source, self.base, self.base / "nested", [self.change()])
        self.assertFalse((self.base / "nested").exists())


if __name__ == "__main__":
    unittest.main()
