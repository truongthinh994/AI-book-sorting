"""Create full-resolution bbox sheets and similarity hints; never approve images/groups."""
import argparse
import csv
import json
import math
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vision.yolo.kept import audit, write


def build(root, output):
    from PIL import Image, ImageDraw
    import cv2
    import numpy as np
    root, output=Path(root),Path(output)
    if output.exists():
        raise ValueError('Queue output exists')
    m, reviews=audit(root)
    output.mkdir(parents=True)
    hashes=[]
    index=[]
    for i,r in enumerate(m['records']):
        image=Image.open(root/'review/images'/r['image_file']).convert('RGB')
        image.load()
        gray=np.asarray(image.convert('L').resize((32,32)),dtype=np.float32)
        dct=cv2.dct(gray)[:8,:8]
        bits=dct>np.median(dct.flatten()[1:])
        hashes.append(sum(int(b)<<j for j,b in enumerate(bits.flatten())))
        if i%8==0:
            sheet=Image.new('RGB',(1280,4*680),'#f2f1e9')
        draw=ImageDraw.Draw(image)
        w,h=image.size
        for s in r['labels']:
            c,x,y,bw,bh=map(float,s.split())
            box=((x-bw/2)*w,(y-bh/2)*h,(x+bw/2)*w,(y+bh/2)*h)
            color=['#00bfff','#ff3030','#f1b400'][int(c)]
            draw.rectangle(box,outline=color,width=2)
            draw.text((box[0],max(0,box[1]-12)),m['classes'][int(c)],fill=color)
        x=(i%2)*640;y=((i%8)//2)*680
        sheet.paste(image,(x,y+40))
        ImageDraw.Draw(sheet).text((x+8,y+4),f'#{i+1} {r["image_id"][:72]}\nnegative_candidate={r["negative_candidate"]}',fill='#151d18')
        name=f'sheet-{i//8+1:03}.jpg'
        index.append(dict(number=i+1,image_id=r['image_id'],sheet=name,negative_candidate=r['negative_candidate']))
        if i%8==7 or i==len(m['records'])-1:
            sheet.save(output/name,quality=95)
    pairs=[]
    for i,a in enumerate(hashes):
        for j in range(i+1,len(hashes)):
            distance=(a^hashes[j]).bit_count()
            if distance<=8:
                pairs.append(dict(a=m['records'][i]['image_id'],b=m['records'][j]['image_id'],distance=distance,status='hint_only'))
    write(output/'index.json',index)
    write(output/'similarity-hints.json',pairs)
    write(output/'review-progress.json',dict(dataset_version=m['dataset_version'],native_resolution_reviewed=[],
          screened=[],group_verified=[],note='Sheets and similarity are only review aids. No approvals inferred.'))
    print(json.dumps(dict(images=len(index),sheets=math.ceil(len(index)/8),similarity_hints=len(pairs))))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--campaign',required=True)
    p.add_argument('--output',required=True)
    a=p.parse_args();build(a.campaign,a.output)
