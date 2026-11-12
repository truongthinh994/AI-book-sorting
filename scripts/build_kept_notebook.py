"""Build the self-contained Colab notebook from tested local helper functions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build():
    cells = []
    def cell(kind, source):
        item = dict(cell_type=kind, metadata={}, source=source.splitlines(keepends=True))
        if kind == 'code':
            item.update(execution_count=None, outputs=[])
        cells.append(item)
    cell('markdown', '''# Dataset mới: Barcode · Ripped · Wornout
Profile **book-three-kept-v1** bỏ Notch/Spot/Tag. Chỉ chạy sau khi duyệt và khóa split.
Notebook độc lập, không cần clone repo. Dataset từ Drive → /content; checkpoint ở Drive.
Smoke test không phải kết quả chất lượng. Test giữ kín đến khi chốt model/ngưỡng.
''')
    cell('code', '''# Chỉ cài trong runtime Colab, không đổi môi trường collector
%pip install -q ultralytics==8.4.208
from google.colab import drive
drive.mount('/content/drive')
''')
    # Embed the exact tested helpers, with relative imports replaced by the needed primitives.
    source = (ROOT/'vision/yolo/kept.py').read_text(encoding='utf-8')
    import ast
    tree = ast.parse(source)
    primitive = '\n'.join(ast.get_source_segment(source, node) for node in tree.body
                          if isinstance(node, ast.FunctionDef) and node.name in ('sha','read','labels'))
    helper = (ROOT/'vision/yolo/kept_training.py').read_text(encoding='utf-8')
    helper = helper.replace('from .kept import CLASSES, MAPPING, PROFILE, read, sha, labels',
        "import hashlib, math\nCLASSES=['Barcode','Ripped','Wornout']\nPROFILE='book-three-kept-v1'\nMAPPING={'0':0,'1':None,'2':1,'3':None,'4':None,'5':2}\n" + primitive)
    cell('code', helper)
    cell('code', '''# Dán nội dung .lock.json đã nhận SAU khi duyệt, độc lập với ZIP.
EXPECTED = None
ZIP_ON_DRIVE = '/content/drive/MyDrive/PBL5/three-kept/split.zip'
RUNS = Path('/content/drive/MyDrive/PBL5/three-kept/runs')
assert EXPECTED and EXPECTED.get('zip_sha256'), 'Chưa có split đã được duyệt/khóa; dừng trước train'
import shutil, zipfile
archive=Path('/content/three-kept.zip')
shutil.copyfile(ZIP_ON_DRIVE,archive)
assert sha(archive)==EXPECTED['zip_sha256'], 'ZIP SHA mismatch'
DATA=Path('/content/three-kept-data')
assert not DATA.exists(), 'Runtime còn dataset cũ; dùng runtime sạch hoặc kiểm tra dữ liệu'
DATA.mkdir()
with zipfile.ZipFile(archive) as z:
    for name in z.namelist():
        dest=(DATA/name).resolve()
        assert DATA.resolve() in dest.parents and ':' not in name and '\\\\' not in name, 'Unsafe ZIP'
    z.extractall(DATA)
manifest=validate_split(DATA,EXPECTED)
runtime_yaml=Path('/content/train-three-kept.yaml')
runtime_yaml.write_text('path: '+str(DATA)+'\\ntrain: train/images\\nval: val/images\\nnc: 3\\nnames: '+json.dumps(CLASSES)+'\\n')
print('PASS',manifest['dataset_version'],manifest['counts'])
''')
    cell('markdown', '''## Smoke rồi chạy tối đa tám lượt
Smoke cả n/s với batch16; nếu OOM tạo run smoke mới batch8. Chọn batch chung trước các lượt đầy đủ.
Lượt1–4: n/default, s/default, n/gentle, s/gentle, seed42. Dùng validation chọn hai cấu hình;
lượt5–8 chạy hai cấu hình đó với seed43/44. Không chọn ứng viên bằng test.
''')
    cell('code', '''MODEL='n'      # n hoặc s
GENTLE=False
SEED=42
BATCH=16       # cùng batch cho toàn chiến dịch
SMOKE=True
RESUME=False
RUN_TAG='smoke-n16-01'  # tên riêng; không ghi đè run
config=settings(MODEL,GENTLE,SEED,BATCH)
if SMOKE: config.update(epochs=2,patience=2)
import platform, subprocess, torch, ultralytics
assert ultralytics.__version__==ULTRALYTICS_VERSION
assert torch.cuda.is_available(), 'Chọn GPU runtime Colab trước khi train'
env=dict(python=platform.python_version(),torch=torch.__version__,cuda=torch.version.cuda,
         gpu=torch.cuda.get_device_name(0),ultralytics=ultralytics.__version__)
identity=dict(dataset_version=manifest['dataset_version'],split_manifest_sha256=EXPECTED['split_manifest_sha256'],
              config=config,environment=env,smoke=SMOKE)
run=RUNS/RUN_TAG
from ultralytics import YOLO
if RESUME:
    checkpoint=check_resume(run,identity)
    model=YOLO(str(checkpoint))
    model.train(resume=True)
else:
    assert not run.exists(), 'Tên run đã có; resume đúng run hoặc chọn tên mới'
    previous=[read(p) for p in RUNS.glob('*/run_identity.json')] if RUNS.exists() else []
    full=[p for p in previous if not p.get('smoke')]
    if not SMOKE:
        assert len(full)<8, 'Đã đủ tám lượt chính'
        assert all(p['split_manifest_sha256']==identity['split_manifest_sha256'] and p['environment']==env and p['config']['batch']==BATCH for p in full), 'Không so trực tiếp khác dữ liệu/môi trường/batch'
    run.mkdir(parents=True)
    (run/'run_identity.json').write_text(json.dumps(identity,indent=2))
    (run/'pip-freeze.txt').write_text(subprocess.check_output(['pip','freeze'],text=True))
    shutil.copyfile(runtime_yaml,run/'runtime.yaml')
    kwargs=dict(config)
    weights=kwargs.pop('weights'); kwargs.pop('name')
    model=YOLO(weights)
    if Path(weights).is_file():
        (run/'initial-weights-sha256.txt').write_text(sha(weights))
    model.train(data=str(runtime_yaml),project=str(run),name='train',exist_ok=False,**kwargs)
''')
    cell('code', '''assert not SMOKE, 'Smoke chỉ kiểm chạy và bộ nhớ, không so chất lượng'
best=run/'train/weights/best.pt'
trained=YOLO(str(best))
metrics=trained.val(data=str(runtime_yaml),split='val',imgsz=640,batch=BATCH,project=str(run),name='validation')
rows=[]
for i,name in enumerate(CLASSES):
    p,r,ap50,ap=metrics.box.class_result(list(metrics.box.ap_class_index).index(i))
    rows.append(dict(class_name=name,precision=float(p),recall=float(r),ap50=float(ap50),ap5095=float(ap)))
result=dict(dataset_version=manifest['dataset_version'],model=MODEL,gentle=GENTLE,seed=SEED,
            macro_damage_ap5095=sum(r['ap5095'] for r in rows if r['class_name']!='Barcode')/2,
            per_class=rows,best_sha256=sha(best),environment=env)
(run/'validation.json').write_text(json.dumps(result,indent=2))
trained.predict(source=str(DATA/'val/images'),imgsz=640,conf=.001,save=True,save_txt=True,save_conf=True,
                iou=.7,project=str(run),name='val-predictions',exist_ok=True)
threshold_report=choose_thresholds(DATA/'val/labels',run/'val-predictions/labels')
(run/'thresholds-validation.json').write_text(json.dumps(threshold_report,indent=2))
print(json.dumps(compare_runs(RUNS),indent=2))
''')
    cell('markdown', '''## Chốt model và test cuối
Chọn bằng macro AP50–95 hai lỗi; báo Barcode riêng. So hai cấu hình cuối qua seed42/43/44;
nếu chênh lệch không vượt độ lệch chuẩn gộp, ưu tiên model ít tham số hơn.
Bản bàn giao dùng seed42. Chọn threshold F2 Ripped, F1 Barcode/Wornout trên validation.
Không chạy test trước khi chốt model và threshold. Nếu sửa nhãn: version mới, chạy lại đối chứng.
Ô dưới chỉ mở khi đã lưu quyết định chọn model/ngưỡng; tự chạy lại test để tune là sai quy trình.
''')
    cell('code', '''# Điền sau khi hoàn tất so sánh + threshold validation
FINAL_SELECTION=None  # {'best_path':..., 'best_sha256':..., 'thresholds': {'Barcode':..., 'Ripped':..., 'Wornout':...}}
RUN_FINAL_TEST=False
if RUN_FINAL_TEST:
    assert FINAL_SELECTION and set(FINAL_SELECTION['thresholds'])==set(CLASSES)
    chosen=Path(FINAL_SELECTION['best_path'])
    assert sha(chosen)==FINAL_SELECTION['best_sha256']
    chosen_identity=read(chosen.parents[2]/'run_identity.json')
    assert chosen_identity['config']['seed']==42 and not chosen_identity['smoke']
    assert chosen_identity['split_manifest_sha256']==EXPECTED['split_manifest_sha256']
    assert all(0<=float(t)<=1 for t in FINAL_SELECTION['thresholds'].values())
    testdir=RUNS/'FINAL_TEST'
    assert not testdir.exists(), 'Test đã bắt đầu/chạy; không tune bằng test'
    testdir.mkdir()
    (testdir/'selection.json').write_text(json.dumps(FINAL_SELECTION,indent=2))
    test_yaml=Path('/content/test-three-kept.yaml')
    test_yaml.write_text(runtime_yaml.read_text()+'test: test/images\\n')
    final=YOLO(str(chosen))
    final.val(data=str(test_yaml),split='test',imgsz=640,project=str(testdir),name='metrics')
    final.predict(source=str(DATA/'test/images'),imgsz=640,conf=.001,iou=.7,save_txt=True,save_conf=True,
                  project=str(testdir),name='predictions')
    report=operating_metrics(DATA/'test/labels',testdir/'predictions/labels',FINAL_SELECTION['thresholds'])
    (testdir/'operating-metrics.json').write_text(json.dumps(report,indent=2))
''')
    notebook=dict(cells=cells,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),
                    language_info=dict(name='python'),accelerator='GPU'),nbformat=4,nbformat_minor=5)
    target=ROOT/'notebooks/three_kept_colab.ipynb'
    target.write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    return target


if __name__=='__main__':
    print(build())
