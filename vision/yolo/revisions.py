"""Create new label versions; replay their history against immutable source labels."""
import argparse
from collections import Counter
import copy
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import shutil
import tempfile

from . import CLASSES


def label_text(lines):
    return "\n".join(lines) + ("\n" if lines else "")


def label_hash(lines):
    return hashlib.sha256(label_text(lines).encode("utf-8")).hexdigest()


def validate_labels(lines):
    if not isinstance(lines, list) or any(not isinstance(line, str) for line in lines):
        raise ValueError("labels must be a list of YOLO lines")
    seen = set()
    for line in lines:
        fields = line.split()
        if len(fields) != 5 or "\n" in line or "\r" in line:
            raise ValueError("Each label must be one class x y w h line")
        try:
            c = int(fields[0])
            x, y, w, h = map(float, fields[1:])
        except ValueError as error:
            raise ValueError("Invalid numeric label") from error
        if c not in range(len(CLASSES)) or not all(math.isfinite(v) for v in (x, y, w, h)):
            raise ValueError("Invalid class or nonfinite coordinate")
        if not (0 <= x <= 1 and 0 <= y <= 1 and 0 < w <= 1 and 0 < h <= 1):
            raise ValueError("Invalid normalized coordinates")
        if min(x-w/2, y-h/2) < -1e-6 or max(x+w/2, y+h/2) > 1+1e-6:
            raise ValueError("Box extends outside image")
        key = (c, x, y, w, h)
        if key in seen:
            raise ValueError("Duplicate label box")
        seen.add(key)


def revision_version(manifest):
    value = {key: manifest[key] for key in
             ("classes", "records", "label_revisions", "parent_manifest_sha256", "restart_review")}
    digest = hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return "damaged-books-v1-five-revised-" + digest[:16]


def validate_history(manifest):
    """Checks integrity/consistency, not authenticity of a reviewer's identity."""
    ids = {r["image_id"] for r in manifest["records"]}
    if not isinstance(manifest.get("label_revisions"), list):
        raise ValueError("Missing label revision history")
    for change in manifest["label_revisions"]:
        if change.get("image_id") not in ids:
            raise ValueError("Unknown image in revision history")
        for key in ("reviewer", "reason", "timestamp_utc"):
            if not isinstance(change.get(key), str) or not change[key].strip():
                raise ValueError(f"Revision requires {key}")
        try:
            stamp = datetime.fromisoformat(change["timestamp_utc"])
        except ValueError as error:
            raise ValueError("Invalid revision timestamp") from error
        if stamp.utcoffset() is None:
            raise ValueError("Revision timestamp requires timezone")
        validate_labels(change["after_labels"])
        if change["after_sha256"] != label_hash(change["after_labels"]):
            raise ValueError("Revision after checksum mismatch")
    if manifest["dataset_version"] != revision_version(manifest):
        raise ValueError("Revision dataset version mismatch")


def replay_labels(image_id, original_lines, history):
    lines = original_lines
    for change in history:
        if change["image_id"] == image_id:
            if change["before_sha256"] != label_hash(lines) or change["before_labels"] != lines:
                raise ValueError("Revision before checksum/content mismatch")
            lines = change["after_labels"]
    return lines


def revise(source, prepared, destination, changes, restart_review=False):
    """changes is an explicit list; no labels or approvals are inferred."""
    from .prepare import REVIEW_FIELDS, audit, sha256, write_json
    source, prepared, destination = map(lambda p: Path(p).resolve(), (source, prepared, destination))
    if destination.exists():
        raise ValueError("Output already exists; never overwrite a dataset version")
    for protected in (source, prepared):
        if destination == protected or protected in destination.parents or destination in protected.parents:
            raise ValueError("Output must be separate from source and prepared directories")
    audit(source, prepared)
    if not isinstance(changes, list) or (not changes and not restart_review):
        raise ValueError("Provide changes, or explicitly restart review")
    manifest = json.loads((prepared / "manifest.json").read_text(encoding="utf-8"))
    revised = copy.deepcopy(manifest)
    revised.update(schema_version=2, split_ready=False, restart_review=bool(restart_review),
                   parent_dataset_version=manifest["dataset_version"],
                   parent_manifest_sha256=sha256(prepared / "manifest.json"))
    history = revised.setdefault("label_revisions", [])
    by_id = {r["image_id"]: r for r in revised["records"]}
    with (prepared / "review.csv").open(encoding="utf-8-sig", newline="") as stream:
        reviews = list(csv.DictReader(stream))
    if len(reviews) != len(by_id) or {r["image_id"] for r in reviews} != set(by_id):
        raise ValueError("Review must contain each image exactly once")
    review_by_id = {r["image_id"]: r for r in reviews}
    touched = set()
    for change in changes:
        if not isinstance(change, dict):
            raise ValueError("Each change must be an object")
        image_id = change.get("image_id")
        if image_id not in by_id or image_id in touched:
            raise ValueError("Unknown or duplicate image in changes")
        touched.add(image_id)
        row = by_id[image_id]
        if change.get("before_sha256") != label_hash(row["labels"]):
            raise ValueError("Stale before checksum; re-open the latest label")
        for key in ("reviewer", "reason"):
            if not isinstance(change.get(key), str) or not change[key].strip():
                raise ValueError(f"Change requires {key}")
        validate_labels(change.get("labels"))
        if row["labels"] == change["labels"]:
            raise ValueError("No label change")
        history.append(dict(image_id=image_id, before_labels=row["labels"],
                            after_labels=change["labels"], before_sha256=change["before_sha256"],
                            after_sha256=label_hash(change["labels"]), reviewer=change["reviewer"],
                            reason=change["reason"], timestamp_utc=datetime.now(timezone.utc).isoformat()))
        row["labels"] = list(change["labels"])
    for row in revised["records"]:
        negative = not any(int(line.split()[0]) != 0 for line in row["labels"])
        row["negative_candidate"] = negative
        review = review_by_id[row["image_id"]]
        if review["label_review"] not in ("approved", "pending", "rejected") or review["negative_review"] not in ("approved", "pending", "rejected", "not_needed"):
            raise ValueError("Invalid review status")
        if restart_review or row["image_id"] in touched:
            review["label_review"] = "pending"
            review["negative_review"] = "pending" if negative else "not_needed"
    counts = Counter(CLASSES[int(line.split()[0])] for r in revised["records"] for line in r["labels"])
    revised["statistics"].update({name: counts[name] for name in CLASSES})
    revised["statistics"].update(images=len(by_id), boxes=sum(counts.values()),
        empty_labels=sum(not r["labels"] for r in revised["records"]),
        negative_candidates=sum(r["negative_candidate"] for r in revised["records"]))
    revised["dataset_version"] = revision_version(revised)
    validate_history(revised)
    # All semantic validation precedes output. Publish only a fully audited tree.
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".label-revision-", dir=destination.parent) as temporary:
        stage = Path(temporary) / "dataset"
        (stage / "images").mkdir(parents=True)
        (stage / "labels").mkdir()
        for row in revised["records"]:
            shutil.copyfile(prepared / "images" / row["image_file"], stage / "images" / row["image_file"])
            (stage / "labels" / (row["image_id"] + ".txt")).write_text(label_text(row["labels"]), encoding="utf-8", newline="\n")
        with (stage / "review.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=REVIEW_FIELDS)
            writer.writeheader()
            writer.writerows(reviews)
        for name in ("README.dataset.txt", "README.roboflow.txt"):
            if (prepared / name).exists():
                shutil.copyfile(prepared / name, stage / name)
        write_json(stage / "manifest.json", revised)
        audit(source, stage)
        stage.rename(destination)
    return revised


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--prepared", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--changes", required=True, help="JSON list, with image_id/labels/before_sha256/reviewer/reason")
    parser.add_argument("--restart-review", action="store_true", help="Reset approvals for all images; retain group IDs as hints")
    args = parser.parse_args()
    manifest = revise(args.source, args.prepared, args.output,
                      json.loads(Path(args.changes).read_text(encoding="utf-8-sig")), args.restart_review)
    print(json.dumps({"dataset_version": manifest["dataset_version"], "statistics": manifest["statistics"]}))


if __name__ == "__main__":
    main()
