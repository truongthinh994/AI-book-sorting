# Rà ảnh gốc và nhóm sách — lượt2

Ngày2026-11-12. Tiếp tục A09 theo yêu cầu người dùng, dựa trên [lượt1](DATASET_REVIEW_PASS1.md), [quy tắc nhãn](LABEL_REVIEW_GUIDE.md) và [kế hoạch](MODEL_TRAINING_PLAN.md). Tiến độ chính thức ở [TASKS](codex/TASKS.md). A09 chưa hoàn tất; chưa chia tập hoặc train.

## Kết quả trực quan

Đã mở39 ảnh gốc640×640 cạnh bản có hộp, thuộc11 đề xuất nhóm của lượt1. Cộng9 ảnh gốc đã xem lượt trước là48 ảnh khác nhau;572 ảnh còn lại mới được sàng lọc ở320px. Không coi48 lượt xem là48 ảnh đã duyệt đầy đủ nhãn.

Index dưới đây nối tới image_id trong `visual-pass1/index.json`; nhật ký lượt2 cũng lưu image_id, không dùng index của các đợt lịch sử khác.

| Đề xuất | Index đã xem gốc | Kết luận nhóm của Codex |
|---|---|---|
| P01 | 14,92,452 | Cùng sách bìa xanh đậm; mã, chữ và vết mép khớp; review2_book_001 |
| P02 | 19,35,36,481,599 | Tiêu đề hồng trên trước/gáy và chữ mặt sau khớp; visual_group_033 |
| P03 | 37,38,63 | Sách vàng Paris, mã thư viện và bố cục khớp; visual_group_065 |
| P04 | 45,57,70 | DIGEST100 tập11, mã và vết xước khớp; visual_group_011 |
| P05 | 121,151,158,295 | Bìa sau đỏ có chân dung, mã và nếp băng keo khớp; review2_book_005 |
| P06 | 9,18,246,411,524,527 | Họ bìa L'Ultime Secret, có tập/màu khác nhau; review2_family_006 |
| P07 | 12,13,16,31 | Họ thiết kế báo cáo KIPF, có tiêu đề khác nhau; visual_group_037 |
| P08 | 116,142,167 | Họ bìa Người đàn ông cười; không khẳng định cùng tập/cuốn; visual_group_087 |
| P09 | 130,377 | Gáy xám, tiêu đề vàng khớp qua hai góc; review2_book_009 |
| P10 | 93,219,421 | Tiêu đề đỏ trước/gáy và mép trên khớp; visual_group_024 |
| P11 | 113,168,310 | Bìa vàng/trắng có chân dung, mã và chữ khớp; visual_group_085 |

Nhóm là đơn vị chống rò rỉ theo cuốn/thiết kế bìa của D11, không xác thực số bản vật lý. P06/P07/P08 được ghi rõ là họ thiết kế. Chưa kết luận11 nhóm độc lập với toàn bộ620 ảnh; đặc biệt cần đối chiếu tiếp quan hệ P05–P06 giữa các sách đỏ bọc băng keo trước khi split.

Đã cập nhật23 group_id trong CSV mới;384 ảnh có group_id, nhưng chỉ39 ảnh trong lượt này có bằng chứng kiểm gốc mới. Các group_id còn lại giữ vai trò gợi ý cũ; không tuyên bố384 ảnh đã xác nhận nhóm.

## Nhãn sửa và phiên bản

Tạo riêng `data/local/campaign-v2/review-assistant-v2`, version `damaged-books-v1-five-revised-31e9c40f9399d568`. Bản nguồn, review-start và review-assistant-v1 được giữ nguyên.

- Sửa30 ảnh:9,13,14,18,19,31,35,38,45,57,70,92,93,113,116,121,151,158,167,168,246,295,310,377,411,421,452,524,527,599.
- Bỏ190 hộp:182 Notch trên nếp bìa/băng keo, phản sáng hoặc vùng in nguyên vẹn;7 Spot trên chi tiết in/tem;1 Barcode trên tem chữ không có vạch.
- Bổ sung12 Barcode nhà xuất bản còn thiếu, gồm mã bị cắt nhưng còn thấy vạch. Áp dụng D27: mọi mã1D nhìn thấy, không chỉ mã thư viện.
- Mỗi patch lưu toàn bộ nhãn trước/sau, hash, lý do, reviewer Codex và thời gian. Đã xem lại3 bảng trước/sau của30 ảnh và bảng crop của cả12 mã thêm.
- Những hộp Spot/Wornout/Ripped còn mơ hồ vẫn chờ kiểm. Không biến việc xóa hộp Notch sai thành xác nhận ảnh không lỗi.

| Chỉ số | Trước lượt2 | Sau lượt2 |
|---|---:|---:|
| Ảnh | 620 | 620 |
| Hộp | 3592 | 3414 |
| Barcode | 192 | 203 |
| Notch | 714 | 532 |
| Ripped | 411 | 411 |
| Spot | 937 | 930 |
| Wornout | 1338 | 1338 |
| Nhãn rỗng | 34 | 35 |
| Ứng viên mẫu âm | 52 | 53 |

Ảnh31 trở thành nhãn rỗng sau bỏ hộp sai; vẫn pending, chưa được xác nhận không lỗi. Cả620 label_review và53 negative_review vẫn pending. Đây là kết quả sửa một phần và xác nhận nhóm của trợ lý, chưa phải dataset dùng để train.

## Bằng chứng và cách xem

Trong `data/local/campaign-v2/visual-pass2` có `REVIEW_REPORT.md` chứa ảnh đối chiếu; `actions.json`, `image-observations.csv`, `label-changes-02.json`, `group-review-audit.json`, `pass-summary.json`, `validation.json`. Patch và CSV nhóm lưu riêng: version nhãn nằm trong manifest; quyết định nhóm được kiểm bằng checksum CSV và nhật ký trước/sau. Split sau này phải khóa cả hai.

SHA256 manifest: `ac3c834d141af27a21480a98b94c7e0bb2b01c99100393127e25cde387fd694d`.

SHA256 review.csv: `ed3a206af0bcd7fa97b4da7428f9d46bf259f438517df31c8e1dd6c4a4088a0d`.

Audit nguồn cộng lịch sử sửa PASS;620 ảnh đầu ra khớp hash nguồn, bản cha không đổi, CSV đủ620 ID duy nhất và trạng thái mẫu âm khớp manifest. Chưa có train/val/test trong đầu ra. Đã tạo HTML bằng generator hiện có; QA trình duyệt NOT_RUN.

Chạy `scripts/windows/ReviewDataset.cmd` để mở v2 nếu tồn tại, fallback v1 rồi review-start. Dữ liệu/ảnh/CSV/HTML thật nằm ngoài Git nên máy khác phải có bản dữ liệu tương ứng. Trang hiện hỗ trợ xem ảnh, nhóm và trạng thái; web xem split theo nhóm/lớp/mẫu âm vẫn thuộc A10.

Điểm tiếp tục A09: kiểm quan hệ nhóm chéo, rà tiếp572 ảnh gốc còn lại, sửa các nhãn mơ hồ và xác nhận mẫu âm. Người dùng xác nhận trường hợp khó phân biệt; không tự nâng trạng thái người dùng hoặc kế thừa duyệt của release361 cũ.
