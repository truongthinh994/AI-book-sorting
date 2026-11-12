# Chiến dịch mới: giữ Barcode / Ripped / Wornout

Ngày 2026-11-12, quyết định D29 theo kế hoạch người dùng yêu cầu triển khai. D29 thay D28 cho chiến dịch này: bắt đầu từ ZIP, **bỏ Notch**, không gộp vào rách; bỏ Spot/Tag. Dữ liệu và thay đổi có sẵn giữ nguyên. Không kế thừa sửa nhãn hay approval. Collector và firmware ngoài phạm vi.

## Trạng thái thực tế

- Folder đầu: `data/local/campaign-v4-three-kept-2026-11-12` (ngoài Git). Đã giải nén nguyên trạng, copy ZIP và audit từng ảnh/nhãn so với ZIP. 620 ảnh, 1.944 hộp: Barcode194, Ripped411, Wornout1339;63 nhãn rỗng,100 ứng viên âm. Nguồn SHA256 `dc2a81293b0f841b0fd187a410b869a1fc9021077ffc6221f9f33621ff978197`.
- Checkpoint trước lượt2: đã mở 24 ảnh với bbox ở kích thước640 trên3 sheet; mở riêng #3/#15/#22 để đối chiếu. Phát hiện hai Barcode thiếu (#3, ISBN thứ hai #15) và một Barcode sai là tem chữ/số (#22). Patch có actor/lý do/hash, không replay sửa cũ.
- Lịch sử r02 (tại checkpoint đầu, không phải bản hoạt động): `data/local/campaign-v4-three-kept-2026-11-12-r02`, 620 ảnh/1.945 hộp, Barcode195/Ripped411/Wornout1339,62 nhãn rỗng/100 ứng viên âm. Chưa ảnh/nhóm nào approved; **còn596 ảnh chưa mở**. #1 bbox Ripped lớn, #24 Barcode nhỏ cần đối chiếu tiếp.
- 78 sheet hỗ trợ rà gốc và20 cặp pHash gợi ý nằm trong `reports/native-review` của bản đầu; không phải bằng chứng đã rà toàn bộ hoặc nhóm đã xác nhận. Hai cặp nguồn vượt train/test cũ phải kiểm liên kết sách, không dùng split618/1/1.
- Chưa có split đề xuất/được duyệt/khóa. Notebook giữ `EXPECTED=None`, không được train. GPU/Colab và chất lượng model NOT_RUN; không có best.pt/last.pt của chiến dịch này.

Checkpoint hiện tại: **r06**, version `three-kept-4c4d10dc50f0f52e8c31`,620 ảnh/2050 hộp (Barcode301/Ripped411/Wornout1338),42 nhãn rỗng/101 ứng viên âm. Đã mở đủ620/620 ảnh ở640px, còn duyệt bbox và liên kết toàn cục. Có102 đề xuất nhóm/333 ảnh,287 ảnh chưa có đề xuất nhóm;49 ảnh nhãn rejected, chưa có approved. #608 sửa Wornout gán nhầm tem thành Barcode, tăng một ứng viên âm. Đã tách #5 SF Philosophy khỏi nhóm ThirdHumanity4 bị đề xuất sai trước đó. Chi tiết [lượt5](DATASET_KEPT_PASS5.md); lịch sử [lượt4](DATASET_KEPT_PASS4.md), [lượt3](DATASET_KEPT_PASS3.md), [lượt2](DATASET_KEPT_PASS2.md). Mã/notebook được xuất bản ở repo mới do người dùng chỉ định: [AI-book-sorting](https://github.com/truongthinh994/AI-book-sorting/tree/feat/three-kept-rebuild), [draft PR1](https://github.com/truongthinh994/AI-book-sorting/pull/1). Chưa merge.

## Lệnh chạy

Chạy tại root repo bằng Python3.11 trong venv YOLO hiện có. Trang rà/sheet cần `pip install -r vision/yolo/requirements-review.txt`; dependency này cũng được cài riêng trong CI, không thêm Torch/YOLO vào collector. Module mới độc lập giữ nguyên công cụ/profile lịch sử, tránh thay đổi đang dở trong các file cũ.

```powershell
$py = '..\.venv-yolo\Scripts\python.exe'
$campaign = 'data/local/campaign-v4-three-kept-2026-11-12-r06'
& $py -m vision.yolo.kept audit --campaign $campaign
& $py -m vision.yolo.kept review --campaign $campaign --output "$campaign/reports/review.html"
```

Để dựng mới ở folder chưa tồn tại:

```powershell
& $py -m vision.yolo.kept convert-three --profile book-three-kept-v1 --archive 'C:\Users\LENOVO\Downloads\Damaged Books.v1i.yolov11.zip' --output data/local/three-kept-next
```

`convert-three` của module mới chỉ nhận ZIP sáu lớp, không nhận parent đã sửa. Profile cũ `book-three-v1` vẫn ở module lịch sử; không tráo dữ liệu vì cùng ba tên lớp.

Rà `review/review.csv`: group_id, label_review, negative_review, reason. Dùng trang HTML lọc lớp/âm, xem ảnh640/gốc, nhập nhóm/lý do rồi xuất CSV; thay đổi UI không tự ghi đĩa. Chỉ approved khi đã rà đủ nhãn và nhóm, kèm bằng chứng/lý do. Mẫu âm cần duyệt riêng. Notch/rách khó phân biệt thì cách ly. Không suy barcode không tồn tại từ việc giải mã thất bại.

Sửa nhãn bằng `revise --campaign ... --output <folder-mới> --patches <json>`. Patch là danh sách gồm image_id, before_sha256 (digest JSON labels), labels mới, actor, reason. Revision tạo bản mới, giữ nguồn/nhãn cũ, hạ trạng thái ảnh bị sửa về pending. Không sửa TXT ngoài manifest.

## Chia, duyệt một lần và khóa

```powershell
& $py -m vision.yolo.kept split-three --campaign $campaign --output "$campaign/proposed-01"
# Sau khi người dùng duyệt đúng bản đề xuất:
& $py -m vision.yolo.kept lock --campaign $campaign --proposed "$campaign/proposed-01" --approval approval.json --output "$campaign/split-locked"
```

`split-three` audit dữ liệu trước, loại pending/rejected và âm chưa duyệt. Cần ít nhất3 nhóm độc lập mỗi lớp; không đủ thì dừng. Search seed42–73,100 phương án/seed, khóa cả seed và attempt; chỉ giữ phương án đủ3 lớp từng tập. Xếp hạng sai lệch tỷ lệ hộp rồi ảnh, hòa chọn seed/attempt nhỏ. Không chia cùng nhóm sang nhiều tập. Báo số nhóm mỗi lớp, số âm và cảnh báo val/test dưới20 hộp/lớp hoặc không có âm. Thiếu mẫu không thành bằng chứng chất lượng.

Trang `proposed-01/index.html` có các góc cùng nhóm, tập/lớp/âm/cách ly. Khi người dùng duyệt một lần, tạo `approval.json` với `approved:true`, `reviewer` và `plan_sha256` chính xác từ proposal. Không tự tạo approval thay người dùng. Thay đổi CSV/nhãn sau proposal bắt buộc đề xuất và duyệt lại.

`lock` chạy lại chọn split tái lập, kiểm approval, tạo dataset ZIP và `.lock.json` bên cạnh. SHA ngoài ZIP là giá trị notebook phải nhận độc lập; không tin manifest tự khai. YAML train chỉ có train/val, không chứa test. Không nạp split cũ năm lớp hoặc ba lớp gộp Notch.

## Colab và bàn giao

[Notebook độc lập](../notebooks/three_kept_colab.ipynb) được build bằng `python scripts/build_kept_notebook.py` từ helper đã kiểm thử. Không clone repo hoặc cài thư viện AI vào collector. Sau duyệt, copy ZIP đã khóa lên Drive và dán `.lock.json` vào EXPECTED. Notebook kiểm inventory/SHA/profile/mapping/version, giao nhóm/ID/hash và counts trước train.

Ultralytics8.4.208; smoke n/s trước để chọn batch16 hoặc8 chung. Bốn lượt seed42: n/s × default/gentle. Cấu hình100epochs,patience20,AdamW,lr0=.001,AMP,640. Gentle mosaic=.25,scale=.2,hsv_s=.3,hsv_v=.2. Chọn hai cấu hình tốt trên validation rồi chạy seed43/44; tối đa8 lượt đầy đủ. Lưu Drive: môi trường, pip freeze, data/config identity, checksum weights, checkpoints và metrics. Resume xác minh đúng identity và last.pt.

So macro AP50–95 Ripped/Wornout; Barcode riêng. Hai ứng viên cuối so mean3seed và độ lệch chuẩn gộp; ưu tiên ít tham số khi chênh lệch không vượt độ dao động. Bàn giao seed42. Threshold trên validation: F2 Ripped, F1 hai lớp khác, matching IoU.50, NMS.70; quét .001 và .01–.99, hòa chọn ngưỡng thấp hơn. Báo P/R tại ngưỡng vận hành riêng với AP. Chốt model/ngưỡng rồi mới mở ô test, ghi marker để tránh đánh giá lại nhằm tune. Đổi nhãn sau train phải tạo version và chạy lại đối chứng.

Giới hạn: trang HTML chưa được chạy trong browser vì chính sách công cụ chặn file://. Unit/static checks không thay thế nghiệm thu UI. Chưa chạy Colab GPU, chưa đánh giá camera thực.
