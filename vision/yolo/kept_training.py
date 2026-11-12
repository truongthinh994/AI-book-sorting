"""Colab artifact validation and bounded experiment settings (stdlib only)."""
import json
from pathlib import Path
from .kept import CLASSES, MAPPING, PROFILE, read, sha, labels

ULTRALYTICS_VERSION = '8.4.208'


def validate_split(root, expected):
    root = Path(root)
    if not expected or expected.get('taxonomy_profile') != PROFILE or not expected.get('dataset_version'):
        raise ValueError('Split not approved/locked yet')
    if sha(root/'split_manifest.json') != expected.get('split_manifest_sha256'):
        raise ValueError('Split manifest checksum mismatch')
    m = read(root/'split_manifest.json')
    if m.get('taxonomy_profile') != PROFILE or m.get('source_id_mapping') != MAPPING or m.get('classes') != CLASSES or not m.get('split_ready') or m.get('dataset_version') != expected['dataset_version']:
        raise ValueError('Wrong profile/mapping/classes/version or unlocked split')
    if not m.get('approval', {}).get('approved') or m['approval'].get('plan_sha256') != m.get('plan_sha256'):
        raise ValueError('Missing split approval')
    actual_files = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual_files != set(m['file_sha256']) | {'split_manifest.json'}:
        raise ValueError('Split file inventory mismatch')
    for name, checksum in m['file_sha256'].items():
        p = (root/name).resolve()
        if root.resolve() not in p.parents or sha(p) != checksum:
            raise ValueError('Split file checksum/path mismatch')
    groups, ids, hashes = set(), set(), set()
    for part, rows in m['assignment'].items():
        if part not in ('train','val','test'):
            raise ValueError('Unknown split')
        local_groups = {r['group_id'] for r in rows}
        local_ids = {r['image_id'] for r in rows}
        local_hashes = {sha(root/part/'images'/r['image_file']) for r in rows}
        if groups & local_groups or ids & local_ids or hashes & local_hashes or len(local_ids) != len(rows):
            raise ValueError('Group/ID/image leakage')
        groups |= local_groups
        ids |= local_ids
        hashes |= local_hashes
        counts = {name:0 for name in CLASSES}
        for row in rows:
            for line in labels((root/part/'labels'/(row['image_id']+'.txt')).read_text(), 3):
                counts[CLASSES[int(line.split()[0])]] += 1
        if counts != m['class_counts'][part] or any(n == 0 for n in counts.values()) or len(rows) != m['counts'][part]:
            raise ValueError('Class/record counts mismatch')
    if set(m['assignment']) != {'train','val','test'} or ids & set(m['quarantined']):
        raise ValueError('Missing split or quarantine leakage')
    return m


def settings(model='n', gentle=False, seed=42, batch=16):
    if model not in ('n','s') or type(seed) is not int or seed not in (42,43,44) or batch not in (8,16):
        raise ValueError('Unknown experiment')
    config = dict(weights=f'yolo11{model}.pt', imgsz=640, epochs=100, patience=20,
                  optimizer='AdamW', lr0=.001, seed=seed, batch=batch, amp=True,
                  deterministic=True, workers=2, save=True, save_period=1,
                  name=f'{model}640_{"gentle" if gentle else "default"}_seed{seed}')
    if gentle:
        config.update(mosaic=.25, scale=.2, hsv_s=.3, hsv_v=.2)
    return config


def check_resume(run, fingerprint):
    run = Path(run)
    if read(run/'run_identity.json') != fingerprint or not (run/'train/weights/last.pt').is_file():
        raise ValueError('Resume requires same run/dataset/config and last.pt')
    return run/'train/weights/last.pt'


def compare_runs(root):
    """Three-seed comparison; model seed42 is always the deliverable."""
    import statistics
    rows = [read(p) for p in Path(root).glob('*/validation.json')]
    groups = {}
    for r in rows:
        groups.setdefault((r['dataset_version'],r['model'],r['gentle']), []).append(r)
    result = []
    for key, rs in groups.items():
        seeds = [r['seed'] for r in rs]
        if len(set(seeds)) != len(seeds):
            raise ValueError('Duplicate seed results for a configuration')
        scores = [r['macro_damage_ap5095'] for r in rs]
        result.append(dict(dataset_version=key[0], model=key[1], gentle=key[2], seeds=seeds,
                           mean=statistics.mean(scores), stdev=statistics.stdev(scores) if len(scores)>1 else None,
                           complete=set(seeds)=={42,43,44}))
    return sorted(result,key=lambda r:-r['mean'])


def operating_metrics(label_root, prediction_root, thresholds):
    """Greedy class-aware bbox matching at IoU .50, after saved NMS predictions."""
    def iou(a,b):
        def xy(r):
            x,y,w,h=r
            return x-w/2,y-h/2,x+w/2,y+h/2
        a,b=xy(a),xy(b)
        intersection=max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
        union=(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-intersection
        return intersection/union if union else 0
    totals={n:dict(tp=0,fp=0,fn=0) for n in CLASSES}
    for target in Path(label_root).glob('*.txt'):
        gt=labels(target.read_text(),3)
        pred=Path(prediction_root)/target.name
        detections=[]
        if pred.exists():
            for line in pred.read_text().splitlines():
                f=line.split()
                if len(f)!=6:
                    raise ValueError('Predictions need class xywh confidence')
                labels(' '.join(f[:5]),3)
                detections.append((int(f[0]),list(map(float,f[1:5])),float(f[5])))
        for c,name in enumerate(CLASSES):
            boxes=[list(map(float,s.split()[1:])) for s in gt if int(s.split()[0])==c]
            used=set()
            selected=sorted((d for d in detections if d[0]==c and d[2]>=thresholds[name]),key=lambda d:-d[2])
            for _,box,confidence in selected:
                candidates=[(iou(box,other),j) for j,other in enumerate(boxes) if j not in used]
                match=max(candidates,default=(0,-1))
                if match[0]>=.5:
                    used.add(match[1]); totals[name]['tp']+=1
                else:
                    totals[name]['fp']+=1
            totals[name]['fn']+=len(boxes)-len(used)
    for name,t in totals.items():
        beta=2 if name=='Ripped' else 1
        t['precision']=t['tp']/max(1,t['tp']+t['fp'])
        t['recall']=t['tp']/max(1,t['tp']+t['fn'])
        t['fbeta']=(1+beta**2)*t['tp']/max(1,(1+beta**2)*t['tp']+beta**2*t['fn']+t['fp'])
        t['threshold']=thresholds[name]
    return totals


def select_final(rows):
    """Compare finalists with complete seeds; stable tie-break favors fewer parameters."""
    import math
    complete=sorted((r for r in rows if r['complete']),key=lambda r:-r['mean'])
    if len(complete)<2 or len({r['dataset_version'] for r in complete})!=1:
        raise ValueError('Need two three-seed finalists on the same dataset')
    a,b=complete[:2]
    pooled=math.sqrt((a['stdev']**2+b['stdev']**2)/2)
    if a['mean']-b['mean']<=pooled:
        return min((a,b),key=lambda r:({'n':0,'s':1}[r['model']],r['gentle'],-r['mean']))
    return a


def choose_thresholds(label_root,prediction_root):
    grid=[.001]+[i/100 for i in range(1,100)]
    evaluated=[operating_metrics(label_root,prediction_root,{n:t for n in CLASSES}) for t in grid]
    return {n:max((row[n] for row in evaluated),key=lambda r:(r['fbeta'],-r['threshold'])) for n in CLASSES}
