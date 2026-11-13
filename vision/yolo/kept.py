"""Immutable, source-only three-kept campaign. No legacy Notch merge or approval inheritance.

python -m vision.yolo.kept --help
This module is deliberately independent of the historical conversion implementation.
"""
import argparse
import csv
import hashlib
import html
import json
import math
from pathlib import Path
import random
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone

PROFILE = "book-three-kept-v1"
CLASSES = ["Barcode", "Ripped", "Wornout"]
SOURCE_CLASSES = ["Barcode", "Notch", "Ripped", "Spot", "Tag", "Wornout"]
MAPPING = {"0": 0, "1": None, "2": 1, "3": None, "4": None, "5": 2}
FIELDS = ["image_id", "group_id", "label_review", "negative_review", "reason"]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def labels(text, count):
    result = []
    for line in text.splitlines():
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 5 or fields[0] not in [str(i) for i in range(count)]:
            raise ValueError("Invalid class/YOLO label")
        x, y, w, h = map(float, fields[1:])
        if not all(math.isfinite(v) and 0 <= v <= 1 for v in (x, y, w, h)) or min(w, h) <= 0:
            raise ValueError("Invalid bbox")
        result.append(" ".join(fields))
    return result


def label_text(lines):
    return "\n".join(lines) + ("\n" if lines else "")


def version(m):
    return "three-kept-" + digest({k: v for k, v in m.items() if k != "dataset_version"})[:20]


def inventory(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(Path(root).rglob("*")) if p.is_file()}


def convert(archive, output, profile=PROFILE):
    archive, output = Path(archive).resolve(), Path(output).resolve()
    if profile != PROFILE or output.exists() or output in archive.parents:
        raise ValueError("Expected kept profile and a new, separate output")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix=".kept-") as temp:
        stage = Path(temp) / "campaign"
        source, review = stage / "source", stage / "review"
        source.mkdir(parents=True)
        for directory in (review / "images", review / "labels", stage / "reports", stage / "training"):
            directory.mkdir(parents=True)
        shutil.copyfile(archive, stage / "source.zip")
        with zipfile.ZipFile(archive) as package:
            seen = {}
            for entry in package.infolist():
                name = entry.filename.replace("\\", "/")
                path = (source / name).resolve()
                if path == source or source not in path.parents or ":" in name:
                    raise ValueError("Unsafe archive path")
                if entry.is_dir():
                    path.mkdir(parents=True, exist_ok=True)
                    continue
                content = package.read(entry)
                if name in seen and seen[name] != hashlib.sha256(content).hexdigest():
                    raise ValueError("Conflicting duplicate archive member")
                seen[name] = hashlib.sha256(content).hexdigest()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        import ast
        config = (source / "data.yaml").read_text(encoding="utf-8-sig")
        names = ast.literal_eval(next(line.split(":", 1)[1].strip() for line in config.splitlines() if line.startswith("names:")))
        if names != SOURCE_CLASSES:
            raise ValueError("Unexpected source class order")
        records, reviews = [], []
        for split in ("train", "valid", "test"):
            images = sorted((source / split / "images").iterdir())
            if {p.stem for p in images} != {p.stem for p in (source / split / "labels").glob("*.txt")}:
                raise ValueError("Source image/label mismatch")
            for image in images:
                original = source / split / "labels" / (image.stem + ".txt")
                before = labels(original.read_text(encoding="utf-8-sig"), 6)
                after = [str(MAPPING[line.split()[0]]) + " " + line.split(" ", 1)[1]
                         for line in before if MAPPING[line.split()[0]] is not None]
                identity = split + "__" + image.stem
                filename = identity + image.suffix.lower()
                shutil.copyfile(image, review / "images" / filename)
                (review / "labels" / (identity + ".txt")).write_text(label_text(after), encoding="utf-8")
                negative = not any(line.split()[0] != "0" for line in after)
                records.append(dict(image_id=identity, image_file=filename,
                                    source_image=image.relative_to(source).as_posix(), source_label=original.relative_to(source).as_posix(),
                                    image_sha256=sha(image), source_label_sha256=sha(original),
                                    before_labels=before, converted_labels=after, labels=after, negative_candidate=negative))
                reviews.append(dict(image_id=identity, group_id="", label_review="pending",
                                    negative_review="pending" if negative else "not_needed", reason=""))
        m = dict(schema_version=1, taxonomy_profile=PROFILE, classes=CLASSES, source_classes=SOURCE_CLASSES,
                 source_id_mapping=MAPPING, archive_sha256=sha(archive), source_files=inventory(source),
                 license="CC BY 4.0", source="https://universe.roboflow.com/atcom21-gmail-com/damaged-books/dataset/1",
                 created_utc=datetime.now(timezone.utc).isoformat(), conversion_actor="Codex",
                 conversion_reason="User approved restart from ZIP; drop Notch, Spot, Tag; no inherited edits",
                 records=records, revisions=[], split_ready=False)
        m["dataset_version"] = version(m)
        write(review / "manifest.json", m)
        with (review / "review.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(reviews)
        write(stage / "reports" / "conversion.json", statistics(m))
        (review / "data.yaml").write_text("# Review only; no training splits\nnc: 3\nnames: " + json.dumps(CLASSES) + "\n", encoding="utf-8")
        audit(stage)
        stage.rename(output)
    return statistics(read(output / "review/manifest.json"))


def statistics(m):
    counts = Counter(CLASSES[int(line.split()[0])] for r in m["records"] for line in r["labels"])
    return dict(dataset_version=m["dataset_version"], taxonomy_profile=m["taxonomy_profile"],
                images=len(m["records"]), boxes=sum(counts.values()), class_counts=dict(counts),
                empty_labels=sum(not r["labels"] for r in m["records"]),
                negative_candidates=sum(r["negative_candidate"] for r in m["records"]))


def audit(root):
    root = Path(root)
    m = read(root / "review/manifest.json")
    if (m["taxonomy_profile"], m["classes"], m["source_classes"], m["source_id_mapping"]) != (PROFILE, CLASSES, SOURCE_CLASSES, MAPPING):
        raise ValueError("Wrong taxonomy/profile/mapping")
    if m["dataset_version"] != version(m) or sha(root / "source.zip") != m["archive_sha256"] or inventory(root / "source") != m["source_files"]:
        raise ValueError("Version or immutable source changed")
    ids = [r["image_id"] for r in m["records"]]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate image IDs")
    with zipfile.ZipFile(root / "source.zip") as package:
        for name, hashed in m["source_files"].items():
            if hashlib.sha256(package.read(name)).hexdigest() != hashed:
                raise ValueError("Source differs from ZIP")
    for r in m["records"]:
        original = labels((root / "source" / r["source_label"]).read_text(encoding="utf-8-sig"), 6)
        expected = [str(MAPPING[s.split()[0]]) + " " + s.split(" ", 1)[1] for s in original if MAPPING[s.split()[0]] is not None]
        if original != r["before_labels"] or expected != r["converted_labels"]:
            raise ValueError("Incorrect conversion log")
        for patch in m["revisions"]:
            if patch["image_id"] == r["image_id"]:
                if patch["before_labels"] != expected or not patch["actor"].strip() or not patch["reason"].strip():
                    raise ValueError("Invalid revision lineage")
                expected = labels(label_text(patch["after_labels"]), 3)
        if expected != r["labels"] or (root / "review/labels" / (r["image_id"] + ".txt")).read_text() != label_text(expected):
            raise ValueError("Labels changed without a versioned revision")
        if sha(root / "review/images" / r["image_file"]) != r["image_sha256"] or sha(root / "source" / r["source_image"]) != r["image_sha256"] or sha(root / "source" / r["source_label"]) != r["source_label_sha256"]:
            raise ValueError("Image or source label changed")
        if r["negative_candidate"] != (not any(s.split()[0] != "0" for s in expected)):
            raise ValueError("Negative candidate mismatch")
    for kind, expected in (("images", {r["image_file"] for r in m["records"]}), ("labels", {i + ".txt" for i in ids})):
        if {p.name for p in (root / "review" / kind).iterdir()} != expected:
            raise ValueError("Review inventory mismatch")
    with (root / "review/review.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != len(ids) or {r["image_id"] for r in rows} != set(ids):
        raise ValueError("Review inventory mismatch")
    negatives = {r["image_id"] for r in m["records"] if r["negative_candidate"]}
    for row in rows:
        if row["label_review"] not in ("approved", "pending", "rejected") or row["negative_review"] not in ("approved", "pending", "rejected", "not_needed"):
            raise ValueError("Invalid review status")
        if (row["image_id"] in negatives) == (row["negative_review"] == "not_needed"):
            raise ValueError("Negative review mismatch")
        if row["label_review"] == "approved" and (not row["reason"].strip() or not row["group_id"].strip()):
            raise ValueError("Approved review requires group and evidence/reason")
    return m, rows


def propose(root, output):
    root, output = Path(root), Path(output)
    m, rows = audit(root)
    if output.exists():
        raise ValueError("Output exists")
    byid = {r["image_id"]: r for r in m["records"]}
    groups, quarantine = defaultdict(list), []
    hashes = {}
    for row in rows:
        record = byid[row["image_id"]]
        if row["label_review"] != "approved" or (record["negative_candidate"] and row["negative_review"] != "approved"):
            quarantine.append(row["image_id"])
            continue
        group = row["group_id"].strip()
        previous = hashes.setdefault(record["image_sha256"], group)
        if previous != group:
            raise ValueError("Identical images in different groups")
        groups[group].append(record)
    class_groups = [{g for g, rs in groups.items() if any(int(s.split()[0]) == c for r in rs for s in r["labels"])} for c in range(3)]
    if any(len(gs) < 3 for gs in class_groups):
        raise ValueError("Need at least three independent reviewed groups per class; no split created")
    ratios = dict(train=.7, val=.15, test=.15)
    totals = Counter(int(s.split()[0]) for rs in groups.values() for r in rs for s in r["labels"])
    total_images = sum(map(len, groups.values()))
    group_negatives = {g: sum(r['negative_candidate'] for r in rs) for g, rs in groups.items()}
    total_negatives = sum(group_negatives.values())
    best = None
    for seed in range(42, 74):
        rng = random.Random(seed)
        for attempt in range(100):
            keys = sorted(groups)
            rng.shuffle(keys)
            assigned = {p: [] for p in ratios}
            sizes = Counter()
            for group in keys:
                part = min(ratios, key=lambda p: sizes[p] / ratios[p])
                assigned[part].append(group)
                sizes[part] += len(groups[group])
            counts = {p: Counter(int(s.split()[0]) for g in gs for r in groups[g] for s in r["labels"]) for p, gs in assigned.items()}
            if any(set(cs) != {0, 1, 2} for cs in counts.values()):
                continue
            negative_error = (sum(abs(sum(group_negatives[g] for g in assigned[p]) / total_negatives - ratios[p])
                                  for p in ratios) if total_negatives else 0)
            score = (sum(abs(counts[p][c] / totals[c] - ratios[p]) for p in ratios for c in range(3)) + negative_error,
                     sum(abs(sizes[p] / total_images - ratios[p]) for p in ratios), seed, attempt)
            if best is None or score < best[0]:
                best = score, assigned, counts
    if best is None:
        raise ValueError("No class-complete split found without breaking groups")
    assignment = {p: [dict(image_id=r["image_id"], image_file=r["image_file"], group_id=g) for g in gs for r in groups[g]] for p, gs in best[1].items()}
    plan = dict(split_algorithm='kept-group-v2-class-negative',
                taxonomy_profile=PROFILE, classes=CLASSES, source_id_mapping=MAPPING,
                dataset_version=m["dataset_version"], manifest_sha256=sha(root / "review/manifest.json"),
                review_csv_sha256=sha(root / "review/review.csv"), seed=best[0][2], attempt=best[0][3],
                assignment=assignment, quarantined=quarantine, split_ready=False,
                counts={p: len(rs) for p, rs in assignment.items()},
                class_counts={p: {CLASSES[c]: cs[c] for c in range(3)} for p, cs in best[2].items()},
                class_group_counts={p: {CLASSES[c]: len(set(gs) & class_groups[c]) for c in range(3)} for p, gs in best[1].items()},
                negative_counts={p: sum(byid[r["image_id"]]["negative_candidate"] for r in rs) for p, rs in assignment.items()})
    plan["warnings"] = [f"{p}: {name} below target 20 boxes" for p in ("val", "test") for name, n in plan["class_counts"][p].items() if n < 20]
    plan["warnings"] += [f"{p}: no approved negative images" for p in ("val", "test") if not plan["negative_counts"][p]]
    plan["plan_sha256"] = digest(plan)
    output.mkdir(parents=True)
    write(output / "split_plan.json", plan)
    gallery(root, output / "index.html", plan)
    return plan


def lock(root, proposed, output, approval):
    root, proposed, output = Path(root), Path(proposed), Path(output)
    m, _ = audit(root)
    plan = read(proposed / "split_plan.json")
    confirmed = read(approval)
    if output.exists() or plan["manifest_sha256"] != sha(root / "review/manifest.json") or plan["review_csv_sha256"] != sha(root / "review/review.csv"):
        raise ValueError("Output exists or review changed; propose again")
    if digest({k: v for k, v in plan.items() if k != "plan_sha256"}) != plan["plan_sha256"]:
        raise ValueError("Split plan changed")
    if confirmed.get("plan_sha256") != plan["plan_sha256"] or confirmed.get("approved") is not True or not confirmed.get("reviewer", "").strip():
        raise ValueError("Explicit user approval of this exact split is required")
    # Re-run deterministic selection; approval cannot bypass eligibility or leakage checks.
    with tempfile.TemporaryDirectory() as temp:
        if propose(root, Path(temp) / "check") != plan:
            raise ValueError("Split does not match reviewed deterministic proposal")
    with tempfile.TemporaryDirectory(dir=output.parent) as temp:
        stage = Path(temp) / "split"
        for part, rows in plan["assignment"].items():
            for kind in ("images", "labels"):
                (stage / part / kind).mkdir(parents=True)
            for r in rows:
                shutil.copyfile(root / "review/images" / r["image_file"], stage / part / "images" / r["image_file"])
                shutil.copyfile(root / "review/labels" / (r["image_id"] + ".txt"), stage / part / "labels" / (r["image_id"] + ".txt"))
        (stage / "data.yaml").write_text("path: .\ntrain: train/images\nval: val/images\nnc: 3\nnames: " + json.dumps(CLASSES) + "\n", encoding="utf-8")
        report = dict(plan, split_ready=True, approval=confirmed, file_sha256=inventory(stage), archive_sha256=m["archive_sha256"])
        write(stage / "split_manifest.json", report)
        stage.rename(output)
    archive = shutil.make_archive(str(output), "zip", output)
    write(str(output) + ".lock.json", dict(zip_sha256=sha(archive), split_manifest_sha256=sha(output / "split_manifest.json"), dataset_version=m["dataset_version"], taxonomy_profile=PROFILE))
    return report


def gallery(root, output, plan=None):
    """Offline reviewer; CSV export is explicit, never writes approvals automatically."""
    from PIL import Image, ImageDraw
    import base64
    import io
    import os
    root, output = Path(root), Path(output)
    m, reviews = audit(root)
    statuses = {r["image_id"]: r for r in reviews}
    parts = {r["image_id"]: p for p, rs in (plan or {}).get("assignment", {}).items() for r in rs}
    data = []
    for r in m["records"]:
        image = Image.open(root / "review/images" / r["image_file"]).convert("RGB")
        draw = ImageDraw.Draw(image)
        w, h = image.size
        for line in r["labels"]:
            c, x, y, bw, bh = map(float, line.split())
            color = ["#20bfff", "#ff3535", "#e4a500"][int(c)]
            box = [(x-bw/2)*w, (y-bh/2)*h, (x+bw/2)*w, (y+bh/2)*h]
            draw.rectangle(box, outline=color, width=2)
            draw.text((box[0], max(0, box[1]-12)), CLASSES[int(c)], fill=color)
        image.thumbnail((640, 640))
        stream = io.BytesIO()
        image.save(stream, format="JPEG", quality=90)
        data.append(dict(**statuses[r["image_id"]], image=base64.b64encode(stream.getvalue()).decode(),
                         raw=os.path.relpath(root / "review/images" / r["image_file"], output.parent).replace("\\", "/"),
                         part=parts.get(r["image_id"], "quarantine" if plan else "unsplit"), negative=r["negative_candidate"],
                         classes=sorted({CLASSES[int(s.split()[0])] for s in r["labels"]})))
    template = Path(__file__).with_name("kept_review.html").read_text(encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template.replace("__DATA__", json.dumps(data).replace("<", "\\u003c")).replace("__SUMMARY__", html.escape(json.dumps((plan or {}).get("class_counts", statistics(m)), ensure_ascii=False))), encoding="utf-8")
    return str(output)


def revise(root, output, patch_file):
    """Apply explicit bbox edits to a new campaign, preserving source and old versions."""
    root, output = Path(root).resolve(), Path(output).resolve()
    m, rows = audit(root)
    patches = read(patch_file)
    if output.exists() or root in output.parents or output in root.parents:
        raise ValueError('Use a separate new version')
    byid = {r['image_id']:r for r in m['records']}
    touched=set()
    for p in patches:
        if p['image_id'] in touched or p['image_id'] not in byid or not p['actor'].strip() or not p['reason'].strip():
            raise ValueError('Invalid duplicate/unknown patch or missing actor/reason')
        touched.add(p['image_id'])
        row=byid[p['image_id']]
        if digest(row['labels']) != p['before_sha256']:
            raise ValueError('Stale patch')
        after=labels(label_text(p['labels']),3)
        m['revisions'].append(dict(image_id=p['image_id'],before_labels=row['labels'],after_labels=after,
                                   actor=p['actor'],reason=p['reason'],timestamp_utc=datetime.now(timezone.utc).isoformat()))
        row['labels']=after
        row['negative_candidate']=not any(s.split()[0]!='0' for s in after)
    m['dataset_version']=version(m)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as temp:
        stage=Path(temp)/'version'
        shutil.copytree(root,stage,ignore=shutil.ignore_patterns('reports','training','split','proposed'))
        for r in m['records']:
            (stage/'review/labels'/(r['image_id']+'.txt')).write_text(label_text(r['labels']),encoding='utf-8')
        for r in rows:
            if r['image_id'] in touched:
                r.update(label_review='pending',negative_review='pending' if byid[r['image_id']]['negative_candidate'] else 'not_needed',reason='')
        with (stage/'review/review.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
        write(stage/'review/manifest.json',m)
        audit(stage)
        stage.rename(output)
    return statistics(m)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("convert-three")
    c.add_argument("--archive", required=True)
    c.add_argument("--output", required=True)
    c.add_argument("--profile", required=True, choices=[PROFILE])
    for name in ("audit", "review", "split-three", "lock", "revise"):
        p = sub.add_parser(name)
        p.add_argument("--campaign", required=True)
        if name != "audit":
            p.add_argument("--output", required=True)
        if name == "lock":
            p.add_argument("--proposed", required=True)
            p.add_argument("--approval", required=True)
        if name == 'revise':
            p.add_argument('--patches', required=True)
    args = parser.parse_args(argv)
    if args.command == "convert-three":
        result = convert(args.archive, args.output, args.profile)
    elif args.command == "audit":
        result = statistics(audit(args.campaign)[0])
    elif args.command == "review":
        result = gallery(args.campaign, args.output)
    elif args.command == "split-three":
        result = propose(args.campaign, args.output)
    elif args.command == 'revise':
        result = revise(args.campaign,args.output,args.patches)
    else:
        result = lock(args.campaign, args.proposed, args.output, args.approval)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
