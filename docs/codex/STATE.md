Active task: A09
Last updated: 2026-11-12
Branch: feat/three-kept-rebuild
Last green commit: e369f0dade213445bd929c4e61b2fb96fcf3367e

## Điểm tiếp tục — D29, repo đích mới

Người dùng yêu cầu đẩy sang truongthinh994/AI-book-sorting rồi tiếp tục. Remote delivery trỏ repo đích, origin cũ giữ nguyên. Đã xuất bản nhánh feat/three-kept-rebuild và draft PR https://github.com/truongthinh994/AI-book-sorting/pull/1, không merge. Repo đích ban đầu chỉ có README; nhập snapshot tracked có parent main đích để PR có lịch sử chung, không đưa thay đổi cũ chưa commit lên.

## Dữ liệu và tiến độ A09

- D29: nguồn ZIP mới, Barcode0/Ripped1/Wornout2; bỏ Notch/Spot/Tag, không gộp Notch vào Ripped, không replay sửa cũ. Train Colab chỉ sau một lần người dùng duyệt đúng split đã rà.
- Bản hoạt động: data/local/campaign-v4-three-kept-2026-11-12-r03, version three-kept-718b59c52ce639f24518.620 ảnh/1965 hộp: Barcode215,Ripped411,Wornout1339;59 nhãn rỗng/100 ứng viên âm. Nhãn612pending/8rejected,0approved; âm98pending/2rejected,0approved.
- Đã mở120 ảnh640:sheet001–015;96 ảnh mới ở lượt2. Còn500, bắt đầu #121/sheet016.20 ảnh mở riêng lượt2; #24 kiểm rõ hai QR không thuộc Barcode. Thêm20 Barcode trên19 ảnh vào r03; r02 giữ ba sửa trước đó, source/version trước bất biến.
- 14 nhóm đề xuất/33 ảnh có group_id từ đối chiếu tiêu đề/ID/thiết kế, chưa chứng minh liên kết độc lập toàn dataset. Không lấy nhóm/approval cũ sang. Xem ../DATASET_KEPT_PASS2.md và ../THREE_KEPT_CAMPAIGN.md.
- Rejected: #1,#42,#52,#61,#62,#103,#106,#110. #42/#110 cũng âm rejected. #59/#63 mã cắt cần mở riêng; không đoán #42/#62 mờ. Trang trong#110 không phải mặt bìa.
- r03 reports: review.html, observations-pass2.json,group-proposals-pass2.json,review-progress.json,patches-02.json,validation-pass2.json,immutable-audit-pass2.json. Sheet640 ở bản đầu campaign-v4-three-kept-2026-11-12/reports/native-review vẫn là nhãn trước sửa, không nhầm với r03.
- Notebook notebooks/three_kept_colab.ipynb giữ EXPECTED=None; không có split/proposal/approval người dùng, chưa smoke/train/best.pt/last.pt. Không hỏi duyệt split khi chưa có bản đề xuất cụ thể.

## Kiểm tra và xuất bản

Code mới14 tests PASS26.634s tại0401b9c+working tree; full suite trước151PASS49.868s, không gán cho commit mới. Audit bản đầu/r02/r03/ZIP Downloads PASS. UI browser/GPU/camera NOT_RUN; file:// bị chặn trước đó, không lách policy.

CI repo đích lần đầu thất bại vì thiếu Pillow ở requirements CI. Đã đọc log: ModuleNotFoundError PIL, không lỗi dữ liệu. Thêm dependency review nhẹ riêng vision/yolo/requirements-review.txt và CI install, giữ collector requirements. Remote88c72bd: CI success, run43235243033. Xem SESSION_LOG cho kiểm cuối và remote SHA mới nhất.

Local branch feat/three-kept-rebuild giữ lịch sử source. Local ref publish/ai-book-three-kept giữ lịch sử nhánh ở repo đích, hiện đã có main đích làm ancestor. Khi xuất bản thay đổi tracked đã kiểm: commit source đúng allowlist; tạo commit-tree từ source HEAD tree, parent là publish/ai-book-three-kept; update-ref có kiểm parent, push ref publish sang delivery:feat/three-kept-rebuild, không force. Không push trực tiếp source HEAD khác lịch sử vào delivery. Nếu remote có thay đổi mới, fetch/đối chiếu trước; không ghi đè. Không commit thay đổi cũ chưa được stage từ đầu phiên.

## Việc tiếp tục

A09: rà500 ảnh còn lại và các ca nghi vấn; liên kết đủ mọi mặt/cuốn/họ thiết kế. Chỉ sau đó A10 đề xuất split70/15/15 theo nhóm, người dùng duyệt đúng bản một lần, khóa SHA rồi mới train Colab. Không tự nghiệm thu phần cứng.
