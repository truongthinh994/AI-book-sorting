Active task: A09
Last updated: 2026-11-12
Branch: feat/three-kept-rebuild
Last green commit: e369f0dade213445bd929c4e61b2fb96fcf3367e

## Điểm tiếp tục — D29

Người dùng yêu cầu triển khai kế hoạch mới từ ZIP: chỉ Barcode0/Ripped1/Wornout2, bỏ Notch/Spot/Tag; không gộp Notch vào Ripped, không replay sửa cũ. Train Colab sau khi người dùng duyệt split một lần. D29 thay D28 trong chiến dịch mới; xem ../THREE_KEPT_CAMPAIGN.md. Các thay đổi có sẵn lúc đầu phiên vẫn giữ nguyên, không commit gộp.

- Folder nguồn mới: data/local/campaign-v4-three-kept-2026-11-12; audit620 ảnh/1944 hộp,63 rỗng/100 ứng viên âm.
- Bản hoạt động: data/local/campaign-v4-three-kept-2026-11-12-r02; sửa Barcode rõ ràng ở #3/#15/#22 sau xem riêng640. Audit620 ảnh/1945 hộp: Barcode195,Ripped411,Wornout1339;62 rỗng/100 ứng viên âm. Không có approved; chưa split/train.
- Đã xem24 ảnh trên3 sheet ở640 mỗi ảnh;596 còn lại. Không biến việc mở ảnh thành duyệt toàn nhãn/nhóm. #1 Ripped lớn và #24 Barcode nhỏ cần rà tiếp. Nhóm #13/#14 là gợi ý cùng thiết kế; chưa khóa nhóm.
- Bản đầu reports/native-review có78 sheet640, index.json,20 pHash hints, review-progress.json. reports/findings-01.json và patches-01.json lưu lý do/hash. Nguồn/version cũ bất biến. Không lấy group_id/approval cũ sang bản mới.
- CLI độc lập python -m vision.yolo.kept: convert-three --profile book-three-kept-v1, audit, revise, review, split-three, lock. Chỉ nguồn ZIP6 lớp; không nhận parent5. Không thay profile lịch sử.
- Notebook notebooks/three_kept_colab.ipynb nhận EXPECTED=None cho tới khóa split; giữ Drive/resume identity,8 lượt,validation thresholds. GPU/Colab/model metrics NOT_RUN.

## Kiểm tra và xuất bản

Baseline HEAD0025fb7 + thay đổi có sẵn: repository checker PASS;137 tests PASS29.389s. Công cụ mới14 tests; kiểm cuối toàn bộ151 tests PASS49.868s; xem SESSION_LOG cho kiểm cuối và commit/push. Không gán kết quả working tree cho SHA nguyên trạng. Browser UI NOT_RUN: công cụ chặn protocol file://, không thử lách bằng trình duyệt khác.

## Việc tiếp tục

A09: mở và ghi kết luận596 ảnh còn lại; sửa nhãn bằng version mới, liên kết đủ các mặt/cuốn/thiết kế; duyệt âm riêng. Chưa yêu cầu người dùng duyệt bản split khi bản đó chưa tồn tại. Chỉ sau A09 mới đề xuất split A10, người dùng duyệt đúng bản một lần rồi khóa; không train trước. Không tự nghiệm thu phần cứng.

Publication checkpoint: code commit36b989c local. Push retry reached GitHub but403: truongthinh994 lacks origin write permission. No remote branch/PR or hosted ZIP claimed; no remote change/fork/merge. Local source ZIP fallback under ../tmp.
