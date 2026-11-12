# Sửa nhãn có lịch sử — A08

Công cụ `python -m vision.yolo.revisions` tạo thư mục version mới, không sửa nguồn hoặc bản prepared đầu vào. Chỉ dùng thư viện chuẩn. Đợt rà620 ảnh theo [kế hoạch](MODEL_TRAINING_PLAN.md) và [quy tắc năm lớp](LABEL_REVIEW_GUIDE.md).

## Bản sẵn sàng rà trên máy hiện tại

Lượt hỗ trợ đầu đã tạo `review-assistant-v1` với7 ảnh sửa có lịch sử, toàn bộ trạng thái vẫn pending. Launcher ưu tiên bản này, fallback sang review-start khi chưa có dữ liệu mới. Xem [báo cáo lượt rà](DATASET_REVIEW_PASS1.md); không dùng bản pending để khóa split/train.

Trong repository, mở `data/local/campaign-v2/review-start/review.html` bằng trình duyệt hoặc chạy `scripts/windows/ReviewDataset.cmd`. Trang được tạo bằng công cụ review đã có: xem ảnh gốc, phóng to hộp, gán group_id, đánh dấu nhãn và mẫu âm, xuất/nạp review.csv. Trang không tự lưu xuống đĩa và chưa có công cụ kéo/sửa bbox trực tiếp.

620 ảnh ban đầu đều pending trong đợt mới, chưa được chia train/val/test. `source-converted` giữ nhãn sau chuyển đổi; `review-start` là bản bắt đầu rà độc lập, giữ nguồn bất biến. `changes-empty.json` chỉ chứa danh sách rỗng: không ngụ ý đã sửa/duyệt ảnh nào.

## Sửa một hoặc nhiều ảnh

Lưu một JSON list trong thư mục dữ liệu local. Ví dụ dưới là dữ liệu minh họa, thay ID/hash bằng bản đang rà; không chép tên người duyệt nếu chưa có xác nhận thật:

```json
[
  {
    "image_id": "train__example",
    "before_sha256": "SHA256_cua_file_nhan_hien_tai",
    "labels": ["0 0.5 0.5 0.2 0.2", "2 0.7 0.5 0.1 0.2"],
    "reviewer": "nguoi_da_doi_chieu_anh",
    "reason": "Bo hop Spot tren chu in; them vet rach bi bo sot"
  }
]
```

`labels` là toàn bộ nội dung nhãn mới của ảnh; danh sách rỗng xóa mọi hộp. Hộp có ID0–4, tọa độ chuẩn hóa và nằm trong ảnh; hộp trùng, NaN hoặc sai lớp bị từ chối. before_sha256 là hash nội dung nhãn chuẩn hóa UTF-8/LF (không phải hash byte CRLF của file legacy). Tính bằng lệnh sau tại repository, thay đường dẫn ví dụ bằng file thật:

```powershell
& '..\.venv-yolo\Scripts\python.exe' -c "from pathlib import Path; from vision.yolo.revisions import label_hash; print(label_hash(Path('data/local/campaign-v2/review-start/labels/train__example.txt').read_text().splitlines()))"
```

Hash sai nghĩa là bản nhãn đã thay đổi, phải xem lại trước khi sửa. Hash before/after trong lịch sử là hash nhãn chuẩn hóa; source_label_sha256 vẫn kiểm byte nguồn bất biến.

```powershell
# Chạy tại repository; đặt các đường dẫn tới phiên bản thật của bạn.
$pythonExe = '..\.venv-yolo\Scripts\python.exe'
$sourceRoot = Read-Host 'Thu muc goc Damaged Books da giai nen'
$baseRoot = 'data/local/campaign-v2/review-start'
$nextRoot = 'data/local/campaign-v2/review-revision-01'
$changesFile = 'data/local/campaign-v2/changes-01.json'
& $pythonExe -m vision.yolo.revisions --source $sourceRoot --prepared $baseRoot --output $nextRoot --changes $changesFile
& $pythonExe -m vision.yolo.prepare audit --source $sourceRoot --prepared $nextRoot
& $pythonExe -m vision.yolo.review --prepared $nextRoot
```

Output phải chưa tồn tại và không nằm trong thư mục nguồn/prepared. Công cụ kiểm toàn bộ đầu vào rồi tạo ở staging, audit lại trước khi công bố thư mục. Thiếu đĩa/quyền ghi sẽ báo lỗi; không báo thành công khi chưa audit được.

## Version, duyệt lại và audit

- Manifest schema2 giữ lịch sử trước/sau, reviewer, lý do, timestamp có múi giờ, checksum và tham chiếu version/manifest cha. Có thể sửa nối tiếp nhiều version; audit phát lại từ nhãn nguồn qua toàn bộ lịch sử.
- Mọi nhãn sửa đổi làm `label_review=pending`. Nếu ảnh mới không còn bốn lỗi thì `negative_review=pending`; nếu có lỗi thì `not_needed`. Không tự duyệt vì thao tác sửa đã chạy thành công.
- Mặc định giữ group_id và trạng thái ảnh không thay đổi. `--restart-review` chủ động đưa toàn bộ ảnh về pending; group_id cũ chỉ là gợi ý. Muốn rà lại nhóm vẫn phải kiểm bằng ảnh.
- `negative_candidate`, số ảnh/hộp/lớp và version được tính lại. Version phản ánh nội dung ảnh/nhãn, lịch sử sửa và manifest cha; split sau này tiếp tục có ID/hash riêng theo cách chia.
- Audit kiểm khớp nguồn, ảnh, nhãn, lịch sử, thống kê và version. Lịch sử là dấu vết có thể kiểm tra, không phải chữ ký xác thực danh tính reviewer hoặc bằng chứng họ đã xem ảnh.
- Audit bản nguồn cũ vẫn dùng schema1. Chưa có thuật toán tự sửa hoặc tự đoán nhãn/nhóm; ảnh mơ hồ giữ cách ly.

Nếu source không chứa ZIP thì trường source_matches_zip là null; không báo đã so ZIP từ lệnh audit đó. Báo cáo local của đợt khởi tạo kiểm ZIP nguồn riêng và đối chiếu các tệp giải nén. Dữ liệu, CSV, JSON chỉnh sửa và ảnh HTML nằm ngoài Git; code và hướng dẫn mới được commit.

## Web xem split — yêu cầu cho A10

Người dùng yêu cầu web cục bộ để xem trực quan dữ liệu đã chia, theo nhóm sách thay vì chỉ từng ảnh:

- Ba tập train/validation/test có tổng số ảnh, nhóm, lớp và mẫu âm; xem mọi góc chụp của một nhóm cạnh nhau.
- Lọc theo tập, group_id, lớp và mẫu âm; mở ảnh gốc/phóng to bbox; xem ảnh đang cách ly cùng lý do.
- Đánh dấu rõ nhóm/ID/ảnh trùng giữa các tập. Không có cảnh báo không chứng minh đã phát hiện hết cùng sách: vẫn cần rà trực quan.
- Chỉ tạo báo cáo từ split manifest thật. Không tạo một split tạm rồi báo đã khóa train/test trước khi A09 hoàn tất. Duyệt lại và sửa nhóm phải tạo version/split mới có dấu vết.

Train dùng để học; validation để chọn model/tham số/ngưỡng; test để đánh giá cuối trên sách chưa dùng khi phát triển. Nhiều ảnh của cùng cuốn ở góc khác nhau phải cùng tập; chia ngẫu nhiên từng ảnh có thể khiến model nhận ra cuốn sách đã gặp và cho điểm đánh giá quá lạc quan.
