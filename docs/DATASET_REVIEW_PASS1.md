# Rà620 ảnh — lượt hỗ trợ A09 đầu tiên

Ngày2026-11-12. Công việc hỗ trợ A14; kết quả này không hoàn thành A09 hoặc cho phép khóa split. Tiến độ ở [TASKS](codex/TASKS.md); xem [quy tắc nhãn](LABEL_REVIEW_GUIDE.md) và [công cụ sửa nhãn](LABEL_REVISIONS.md). Đã có [lượt2 kiểm ảnh gốc và cập nhật nhóm](DATASET_REVIEW_PASS2.md); số liệu dưới đây giữ làm lịch sử lượt1.

## Phạm vi đã xem

- Đã xem620 ảnh qua62 bảng ảnh gốc cạnh ảnh có nhãn, mỗi ô320px; ghi620 quan sát theo ID ảnh, trong đó418 có ghi chú cụ thể,202 chưa kết luận từ ảnh nhỏ.
- Mở9 ảnh gốc640px để kiểm kỹ: index28,242,275,306,350,400,499,515,607. Index chỉ có nghĩa trong `visual-pass1/index.json`, không dùng index lịch sử để nối nhầm ảnh.
- Người dùng chốt: Barcode gồm mọi mã1D nhìn thấy, cả mã thư viện và ISBN; không gồm QR hoặc tem chỉ có chữ/số. Ghi chú thiếu Barcode trước khi chốt được đọc theo quy tắc này.
- Nhiều hộp Notch/Spot nằm trên chữ, hình in hoặc phản sáng. Một số mã1D chưa có hộp; có hộp Barcode trên tem số phân loại. Đây là trường hợp cần rà/sửa; không suy mọi ảnh cũ đều sai hoặc mọi cảnh báo đều đã xác nhận.

## Sửa đổi đã lưu

Version mới `damaged-books-v1-five-revised-d5a199deb6ae1c96`, local `data/local/campaign-v2/review-assistant-v1`. Giữ nguyên nguồn và `review-start`.

| Index | Sửa có dấu vết sau khi xem ảnh gốc |
|---|---|
| 28 | Bỏ11 hộp Notch trong bề mặt/chi tiết in; giữ hộp mép để rà tiếp |
| 242 | Bỏ3 hộp Notch trên tem/vùng bìa nguyên vẹn và phản sáng |
| 275 | Bỏ1 hộp Notch trên chữ in FCC; Spot/Wornout còn chờ kiểm |
| 350,499 | Bỏ mỗi ảnh1 hộp Barcode trên tem chữ/số không có vạch |
| 515 | Bỏ Barcode thứ hai trên chữ in sát đáy; giữ hộp mã thật |
| 607 | Đổi Wornout phủ mã vạch thật thành Barcode, giữ tọa độ |

Tổng7 ảnh sửa,18 hộp bị bỏ,1 hộp đổi lớp. 306/400 đã xem gốc nhưng vùng mã/tem bị cắt nên chưa xóa khi thiếu căn cứ. Ảnh sửa vẫn pending, không tự nâng thành dùng được.

Thống kê mới:620 ảnh,3592 hộp (Barcode192, Notch714, Ripped411, Spot937, Wornout1338),34 nhãn rỗng,52 ứng viên mẫu âm. Ứng viên mẫu âm chưa phải ảnh đã duyệt không lỗi.

## Nhóm sách và bằng chứng cục bộ

Giữ361 group_id từ release cũ làm gợi ý, không kế thừa duyệt hoặc khẳng định đã kiểm độc lập121 nhóm. Có11 bảng đề xuất nhóm, gồm cặp cùng cuốn và họ thiết kế; tất cả unconfirmed. Không tự gộp vì màu hoặc tên file giống nhau.

Trong `data/local/campaign-v2/visual-pass1`:

- `REVIEW_REPORT.md`: ảnh trước/sau và11 bảng đối chiếu nhóm.
- `screening-notes.csv`, `observations.json`:620 ghi chú, phân biệt xem bảng và mở gốc.
- `group-proposals.csv`, `group-proposals.json`: ID ảnh, căn cứ, loại đề xuất; chưa áp dụng gộp.
- `label-changes-01.json`: nội dung/hash nhãn trước-sau, lý do, người kiểm là Codex, không giả là người dùng duyệt.
- `pass-summary.json`, `validation.json`: thống kê và kiểm nguồn/lịch sử/version; không thay nhận định bằng mắt.

Ảnh, CSV, patch và HTML thật bị Git ignore. Gói tham chiếu cũ được kiểm SHA256 trước khi dùng; nguồn ZIP vẫn bất biến.

## Điểm tiếp tục

Chạy `scripts/windows/ReviewDataset.cmd`: máy có bản mới mở `review-assistant-v1/review.html`, nếu chưa có dùng `review-start`. Đọc báo cáo/ghi chú, kiểm ảnh gốc và nhóm, xuất review.csv trước khi đóng. Không chép CSV nhãn cũ đè bản mới mà bỏ qua ảnh sửa/mẫu âm mới.

Cần tiếp tục sửa nhãn nghi vấn, xác nhận nhóm và duyệt mẫu âm. Chưa có ảnh nào được tự đánh approved trong lượt này; chưa chia tập hoặc chạy GPU. Web xem train/validation/test theo nhóm vẫn thuộc A10, sau khi A09 có dữ liệu đủ tin cậy.
