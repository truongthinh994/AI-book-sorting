Active task: A09
Last updated: 2026-11-12
Branch: feat/three-kept-rebuild
Last green commit: e369f0dade213445bd929c4e61b2fb96fcf3367e

## Điểm tiếp tục — D29, repo đích mới

Người dùng yêu cầu đẩy sang truongthinh994/AI-book-sorting rồi tiếp tục. Remote delivery trỏ repo đích, origin cũ giữ nguyên. Đã xuất bản nhánh feat/three-kept-rebuild và draft PR https://github.com/truongthinh994/AI-book-sorting/pull/1, không merge. Repo đích ban đầu chỉ có README; nhập snapshot tracked có parent main đích để PR có lịch sử chung, không đưa thay đổi cũ chưa commit lên.

## Dữ liệu và tiến độ A09

- D29: nguồn ZIP mới, Barcode0/Ripped1/Wornout2; bỏ Notch/Spot/Tag, không gộp Notch vào Ripped. Chỉ kế thừa sửa có audit trong chính chiến dịch kept, không replay chiến dịch5 lớp. Train sau một lần người dùng duyệt đúng split đã rà.
- Bản hoạt động: data/local/campaign-v4-three-kept-2026-11-12-r06, version three-kept-4c4d10dc50f0f52e8c31.620 ảnh/2050 hộp: Barcode301,Ripped411,Wornout1338;42 nhãn rỗng/101 ứng viên âm. Nhãn571pending/49rejected,0approved; âm93pending/8rejected,0approved.
- Đã mở đủ620 ảnh640:sheet001–078. Lượt4 xem160 mới#241–400,51 gốc riêng,4 crop4x;35 patch tạo r05 (+35/-1 Barcode). Lượt5 xem220 mới#401–620,59 gốc riêng,5 crop4x;42 patch tạo r06 (+36/-6 Barcode,1 Wornout→Barcode#608). Xem lại đủ35+42 ảnh sửa qua11 sheet bbox. Nguồn/version trước bất biến. Đây là lượt xem đầy đủ, chưa hoàn thành duyệt bbox/nhóm.
- Tổng102 đề xuất nhóm/333 ảnh có group_id;287 ảnh chưa có đề xuất, không mặc định coi độc lập. Chưa chứng minh liên kết toàn dataset. Sửa đề xuất sai#5 SF Philosophy từng ghép vào ThirdHumanity4; tiêu đề/ID xác nhận#494/#605/#619 thuộc ThirdHumanity4, #620 đi cùng#587/TheArtOfContraryThinking. Không kế thừa split cũ. Chi tiết ../DATASET_KEPT_PASS4.md, ../DATASET_KEPT_PASS5.md và r06 reports/group-proposals-pass5.json/errata-pass5.json.
- 49 ảnh nhãn rejected,8 âm rejected:#42/#110/#125/#160/#167/#323/#447/#483. Đầy đủ ID/lý do trong r06 reports/pass5-summary.json và review.csv. Không vẽ đoán mã mờ, không auto gộp Notch vào rách hay đổi lỗi thành âm sạch. #608 tăng ứng viên âm từ100 lên101 sau sửa nhãn sai lớp, chưa duyệt âm.
- r06 reports: review.html,observations-pass5.json,group-proposals-pass5.json,errata-pass5.json,unresolved-group-queue.json,review-progress.json,patches-05.json,box-spec-pass5.json,validation-pass5.json,source-immutability-pass5.json. Sheet ở bản đầu reports/native-review còn là nhãn trước sửa; patch-review-01–06 của r06 là nhãn hiện hành. Giữ r04/r05/source bất biến, chỉ thêm report dẫn xuất phục vụ patch. Launcher ReviewThreeKept.cmd mở r06.
- Notebook giữ EXPECTED=None; chưa có split/proposal/approval người dùng, chưa smoke/train hoặc best.pt/last.pt. Chưa hỏi duyệt cuối khi chưa có bản cụ thể.

## Kiểm tra và xuất bản

14 tests công cụ PASS8.862s trên working tree d7cde64+thay đổi cũ có sẵn; không gán kết quả cho SHA nguyên trạng. Audit r04/r05/r06 và ZIP Downloads PASS; nguồn/620 pixel ảnh không đổi, Ripped giữ nguyên, Wornout chỉ sửa lớp#608. Manifest r06 SHA8e316ef234b0cf9b9e83f14d58af6f51331473e95365776b2daf2a19b61e4f77; reviewCSV9822e9c97ab686e06b54aa3a34c6e9ffd7c2959620f4d4b310eb68dc46dad849. Checker/xuất bản cuối xem SESSION_LOG. UI browser/GPU/camera NOT_RUN; file:// bị chặn trước đó, không lách policy.

CI repo đích lần đầu thất bại vì thiếu Pillow ở requirements CI. Đã đọc log: ModuleNotFoundError PIL, không lỗi dữ liệu. Thêm dependency review nhẹ riêng vision/yolo/requirements-review.txt và CI install, giữ collector requirements. Remote88c72bd: CI success, run43235243033. Xem SESSION_LOG cho kiểm cuối và remote SHA mới nhất.

Local branch feat/three-kept-rebuild giữ lịch sử source. Local ref publish/ai-book-three-kept giữ lịch sử nhánh ở repo đích, hiện đã có main đích làm ancestor. Khi xuất bản thay đổi tracked đã kiểm: commit source đúng allowlist; tạo commit-tree từ source HEAD tree, parent là publish/ai-book-three-kept; update-ref có kiểm parent, push ref publish sang delivery:feat/three-kept-rebuild, không force. Không push trực tiếp source HEAD khác lịch sử vào delivery. Nếu remote có thay đổi mới, fetch/đối chiếu trước; không ghi đè. Không commit thay đổi cũ chưa được stage từ đầu phiên.

## Việc tiếp tục

A09: đã xem đủ620; tiếp tục đối chiếu102 nhóm đề xuất/287 ảnh chưa có liên kết,49 ca cách ly và độ chính xác từng bbox, duyệt101 ứng viên âm riêng. Bắt đầu từ r06 reports/unresolved-group-queue.json và pass5-summary.json, không mở lại toàn bộ từ đầu hoặc coi pending đã duyệt. Chỉ khi đủ nhãn/nhóm mới A10 đề xuất split70/15/15 theo nhóm, người dùng duyệt đúng bản một lần, khóa SHA rồi train Colab. Không tự nghiệm thu phần cứng.
