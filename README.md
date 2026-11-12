# AI Book Sorting

Chiến dịch hiện tại dựng lại dữ liệu từ ZIP, chỉ giữ **Barcode, Ripped (rách), Wornout (sờn)**. Bỏ Notch/Spot/Tag; không gộp Notch vào rách. Ảnh và weights ở ngoài Git.

- [Notebook Colab độc lập](notebooks/three_kept_colab.ipynb) · [Mở trong Colab](https://colab.research.google.com/github/truongthinh994/AI-book-sorting/blob/feat/three-kept-rebuild/notebooks/three_kept_colab.ipynb)
- [Cách chuẩn bị, rà, chia nhóm và khóa dữ liệu](docs/THREE_KEPT_CAMPAIGN.md) · [Kết quả rà lượt3](docs/DATASET_KEPT_PASS3.md)
- Bản r04 cục bộ:620 ảnh/1986 hộp; đã mở240 ảnh ở640px, còn380 ảnh.35 đề xuất nhóm/97 ảnh;16 ảnh nhãn nghi vấn cách ly. Chưa duyệt xong nhãn/nhóm, chưa split/train.
- Notebook giữ `EXPECTED=None` tới khi người dùng duyệt đúng split một lần và khóa SHA; không dùng dataset5 lớp hoặc bản3 lớp gộp Notch cũ.

Công cụ rà ảnh dùng dependency nhẹ riêng:

```powershell
python -m pip install -r requirements.txt -r vision/yolo/requirements-review.txt
python -m vision.yolo.kept --help
```

## Collector hiện có

Phần dưới mô tả ứng dụng thu ảnh và phần cứng legacy. Trạng thái chiến dịch dataset/train hiện tại nằm ở các liên kết phía trên.

**Ưu tiên mới2026-11-12:** [kế hoạch rà620 ảnh và train Colab](docs/MODEL_TRAINING_PLAN.md) · [quy tắc rà nhãn](docs/LABEL_REVIEW_GUIDE.md). Khóa dataset mới trước chiến dịch train; bộ361 ảnh/notebook bên dưới là phiên bản trước.

Bước hiện tại: [chuẩn hóa Damaged Books v1 năm nhãn và rà lại split](docs/DAMAGED_BOOKS_DATASET.md). Đã bỏ nhãn Tag trong bản dữ liệu riêng; chưa huấn luyện hay tích hợp AI vào collector. Hướng dẫn collector phía dưới vẫn là luồng QR hiện có.

Hệ thống thử nghiệm kiểm tra tình trạng và phân loại sách thư viện bằng Machine Vision và AI. Hiện có ứng dụng thu ảnh OpenCV/QR và bộ công cụ chuẩn bị dữ liệu, huấn luyện YOLO trên Colab. AI phân tuyến và cơ cấu ESP32 chưa được nghiệm thu.

[![Checks](https://github.com/truongthinh994/AI-book-sorting/actions/workflows/checks.yml/badge.svg?branch=feat%2Fthree-kept-rebuild)](https://github.com/truongthinh994/AI-book-sorting/actions/workflows/checks.yml)
![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)
![PlatformIO](https://img.shields.io/badge/Firmware-PlatformIO-F5822A?logo=platformio&logoColor=white)

## Phạm vi collector legacy

- Nhận dạng bìa sách A6 và mã QR của từng bản sách.
- Căn chỉnh phối cảnh, kiểm tra độ nét và ánh sáng, thu ảnh có metadata.
- Luồng AI đang phát triển dùng `Barcode`, `Notch`, `Ripped`, `Spot`, `Wornout`; Barcode là vùng mã vạch, không phải lỗi.
- Tích hợp phần mềm với ESP32 để phân loại sách vào khay.

Collector A6/QR hiện tại được giữ để thu ảnh. Mô hình AI, cơ cấu phân loại và luồng tích hợp đang phát triển. [Tiến độ](PROGRESS.md) · [Kiến trúc](docs/ARCHITECTURE.md) · [Kế hoạch](docs/PLAN.md).

**A08 đã có công cụ [sửa nhãn có lịch sử](docs/LABEL_REVISIONS.md).** Trên máy đã chuẩn bị dữ liệu, chạy `scripts/windows/ReviewDataset.cmd` để rà620 ảnh; trang hiện để rà nhãn/nhóm, web xem split được thực hiện ở A10 sau khi rà xong.

[Lượt sàng lọc620 ảnh và sửa7 ảnh rõ ràng](docs/DATASET_REVIEW_PASS1.md): launcher ưu tiên bản review-assistant-v1; các nhãn/nhóm vẫn pending, chưa chia dataset mới.

## Team huấn luyện song song

[Mở notebook trên Colab](https://colab.research.google.com/github/nguyenhuunghia10t1-creator/pbl5-library-book-inspection/blob/feat/damaged-books-colab/notebooks/damaged_books_colab.ipynb), chọn GPU, rồi sửa `TEAM_MEMBER` và `EXPERIMENT` tại bước 2. Dataset được tải từ [GitHub Releases](https://github.com/nguyenhuunghia10t1-creator/pbl5-library-book-inspection/releases/tag/damaged-books-reviewed-v1) và kiểm checksum tự động. [Cách chia việc, thu kết quả và so sánh](docs/TEAM_TRAINING.md) · [Hướng dẫn từng ô](docs/COLAB_TRAINING.md).

Ba lượt thử ban đầu: `n640`, `s640`, `n960`. Tất cả giữ cùng split253/54/54 và seed42; mỗi lượt xuất `experiment-summary.csv` và model riêng. Chỉ dùng validation để so sánh; test dành cho đánh giá cuối. Chưa có số đo chất lượng AI hoặc kiểm chứng trên camera thực tế.

## Cấu trúc repository

```text
firmware/esp32/           Firmware ESP32, cấu hình PlatformIO
vision/opencv/           Camera, xử lý bìa, QR, chất lượng ảnh và cấu hình
vision/yolo/             Phạm vi phát triển mô hình nhận diện lỗi
software/desktop/        Giao diện và điều phối ứng dụng thu ảnh
examples/opencv_basics/   Các bài thực hành OpenCV
scripts/                 Công cụ chạy và kiểm tra
tests/                  Kiểm thử tự động
docs/                   Tài liệu kỹ thuật và quyết định thiết kế
data/                   Hướng dẫn quản lý dữ liệu cục bộ
```

## Cài đặt

Yêu cầu: Git, Python và Windows để sử dụng camera DirectShow/MSMF. Firmware sử dụng PlatformIO; không cài chung công cụ firmware vào môi trường Python của ứng dụng.

```powershell
git clone --branch feat/three-kept-rebuild https://github.com/truongthinh994/AI-book-sorting.git
cd AI-book-sorting
py -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
```

## Chạy ứng dụng

```powershell
& '.\.venv\Scripts\python.exe' -m vision.opencv --camera 0
```

Có thể chạy `scripts/windows/CaptureCovers.cmd`. Cấu hình camera và ngưỡng xử lý nằm trong [cover_capture.json](vision/opencv/configs/cover_capture.json).

| Phím | Chức năng |
|---|---|
| `B` | Hiệu chuẩn khi nền trống |
| `S` | Xử lý và lưu khung mới đạt điều kiện |
| `D` | Lưu mẫu cần kiểm tra lại |
| `M` | Chọn bốn góc trên ảnh tĩnh |
| `R` | Lật ảnh đầu ra 180° |
| `Q` | Thoát |

Dữ liệu được lưu tại `data/opencv/collection/`: ảnh gốc, ảnh đã căn, ảnh chẩn đoán và metadata. [Hướng dẫn sử dụng](docs/COVER_CAPTURE.md) · [Quy định dữ liệu](data/README.md).

## Kiểm thử

```powershell
& '.\.venv\Scripts\python.exe' scripts/check_repository.py
& '.\.venv\Scripts\python.exe' -m unittest discover -s tests -v
```

Các test dùng ảnh tổng hợp và thiết bị mô phỏng, không yêu cầu camera hoặc ESP32. Kiểm thử thiết bị thật được ghi riêng trong [báo cáo kiểm chứng](docs/COVER_CAPTURE_VALIDATION.md).

## Firmware

Mở `smart-vision-inspection.code-workspace` bằng VS Code hoặc mở trực tiếp `firmware/esp32` trong PlatformIO.

```powershell
pio run --project-dir firmware/esp32
```

Cấu hình hiện tại: `esp32dev`, Arduino. [Hướng dẫn firmware](firmware/README.md).

## Phát triển cùng nhóm

Mỗi thay đổi thực hiện trên nhánh riêng, gửi pull request vào `main` và cần ít nhất một reviewer. Thành viên chưa có quyền ghi có thể fork repository rồi gửi pull request.

[Quy trình đóng góp](CONTRIBUTING.md) · [Issues](https://github.com/nguyenhuunghia10t1-creator/pbl5-library-book-inspection/issues) · [Quyết định thiết kế](docs/DECISIONS.md).

## Hạn chế hiện tại

Preview đọc frame mới độc lập với worker geometry/QR. Crop/QR hiển thị kèm số frame đã phân tích; bấm S/D sẽ đợi xử lý một frame mới sau yêu cầu. V07 kết hợp cạnh nhiều kênh/màu Lab, kiểm bốn cạnh và hiệu chuẩn B theo từng vùng để giảm nhầm bìa sáng/tối, đường ron và viền in. Kết quả hiện mới kiểm bằng ảnh tổng hợp; chưa đảm bảo mọi màu/nền ngoài thực tế. Nếu ranh giới giấy–nền không nhìn thấy, dùng B, đổi nền hoặc chọn góc M. Bìa ít chi tiết giữ QUALITY_WARNING khi chưa xác minh được nét. Xem [bài thử webcam V07](docs/COVER_CAPTURE.md#thử-bìa-sángtối-v07-trên-webcam) và [báo cáo](docs/COLOR_BACKGROUND_VALIDATION.md) trước khi thu hàng loạt. Nhãn ảnh đạt điều kiện thu không đồng nghĩa với kết luận sách không có lỗi.
