Active task: A09
Last updated: 2026-11-12
Branch: feat/three-kept-rebuild
Last green commit: e369f0dade213445bd929c4e61b2fb96fcf3367e

## Điểm tiếp tục — D29, repo đích mới

Người dùng yêu cầu đẩy sang truongthinh994/AI-book-sorting rồi tiếp tục. Remote delivery trỏ repo đích, origin cũ giữ nguyên. Đã xuất bản nhánh feat/three-kept-rebuild và draft PR https://github.com/truongthinh994/AI-book-sorting/pull/1, không merge. Repo đích ban đầu chỉ có README; nhập snapshot tracked có parent main đích để PR có lịch sử chung, không đưa thay đổi cũ chưa commit lên.

## Dữ liệu và tiến độ A09

- D29: nguồn ZIP mới, Barcode0/Ripped1/Wornout2; bỏ Notch/Spot/Tag, không gộp Notch vào Ripped. Chỉ kế thừa sửa có audit trong chính chiến dịch kept, không replay chiến dịch5 lớp. Train sau một lần người dùng duyệt đúng split đã rà.
- Bản hoạt động: data/local/campaign-v4-three-kept-2026-11-12-r04, version three-kept-e64b4b01e90b4ebf5e8a.620 ảnh/1986 hộp: Barcode236,Ripped411,Wornout1339;56 nhãn rỗng/100 ứng viên âm. Nhãn604pending/16rejected,0approved; âm95pending/5rejected,0approved.
- Đã mở240 ảnh640:sheet001–030. Lượt3 mở120 ảnh mới #121–240 và27 ảnh riêng (có #59/#63 từ lượt trước), crop4x #125. Còn380, bắt đầu #241/sheet031. Lượt3 thêm24 Barcode, bỏ3 sai ở#125/#152/#176,27 ảnh sửa thành r04; nguồn/version trước bất biến.
- Tổng35 đề xuất nhóm/97 ảnh có group_id; chưa chứng minh độc lập toàn dataset. KIPF vàng gom theo họ ảnh thiết kế dù tiêu đề/năm khác, không gọi cùng cuốn vật lý. Các nhóm/ảnh xem trong ../DATASET_KEPT_PASS3.md và r04 reports/group-proposals-pass3.json.
- Rejected hiện tại: #1,#42,#52,#61,#62,#103,#106,#110,#125,#145,#160,#167,#179,#199,#226,#234. Âm rejected #42/#110/#125/#160/#167. Không vẽ đoán mã mờ, không auto gộp Notch vào rách hay đổi lỗi thành âm sạch.
- r04 reports: review.html,observations-pass3.json,group-proposals-pass3.json,review-progress.json,patches-03.json,validation-pass3.json,source-immutability-pass3.json. Sheet ở bản đầu reports/native-review còn là nhãn trước sửa. Source/manifest/review r03 không đổi, chỉ thêm report dẫn xuất để chuẩn bị patch.
- Notebook giữ EXPECTED=None; chưa có split/proposal/approval người dùng, chưa smoke/train hoặc best.pt/last.pt. Chưa hỏi duyệt cuối khi chưa có bản cụ thể.

## Kiểm tra và xuất bản

Baseline checker và14 tests PASS9.827s trên726fc11+thay đổi cũ có sẵn; không gán kết quả cho SHA nguyên trạng. Lượt3 audit r03/r04/ZIP Downloads PASS; checker cuối xem SESSION_LOG. UI browser/GPU/camera NOT_RUN; file:// bị chặn trước đó, không lách policy.

CI repo đích lần đầu thất bại vì thiếu Pillow ở requirements CI. Đã đọc log: ModuleNotFoundError PIL, không lỗi dữ liệu. Thêm dependency review nhẹ riêng vision/yolo/requirements-review.txt và CI install, giữ collector requirements. Remote88c72bd: CI success, run43235243033. Xem SESSION_LOG cho kiểm cuối và remote SHA mới nhất.

Local branch feat/three-kept-rebuild giữ lịch sử source. Local ref publish/ai-book-three-kept giữ lịch sử nhánh ở repo đích, hiện đã có main đích làm ancestor. Khi xuất bản thay đổi tracked đã kiểm: commit source đúng allowlist; tạo commit-tree từ source HEAD tree, parent là publish/ai-book-three-kept; update-ref có kiểm parent, push ref publish sang delivery:feat/three-kept-rebuild, không force. Không push trực tiếp source HEAD khác lịch sử vào delivery. Nếu remote có thay đổi mới, fetch/đối chiếu trước; không ghi đè. Không commit thay đổi cũ chưa được stage từ đầu phiên.

## Việc tiếp tục

A09: rà380 ảnh còn lại và các ca nghi vấn; liên kết đủ mọi mặt/cuốn/họ thiết kế. Chỉ sau đó A10 đề xuất split70/15/15 theo nhóm, người dùng duyệt đúng bản một lần, khóa SHA rồi mới train Colab. Không tự nghiệm thu phần cứng.
