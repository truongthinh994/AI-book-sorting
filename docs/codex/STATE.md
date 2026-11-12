Active task: NONE
Last updated: 2026-11-12
Branch: feat/three-kept-rebuild
Last green commit: e369f0dade213445bd929c4e61b2fb96fcf3367e

## Điểm tiếp tục — chốt nhãn, duyệt nhóm/split r07

Người dùng chốt nhãn và cách ly đúng49 ảnh, yêu cầu làm bước tiếp theo. Nhãn571 ảnh được nhận; quyết định không tự trở thành approval nhóm/split. A09/A10 BLOCKED chờ một lần duyệt bản cụ thể dưới đây, không có CODEX IN_PROGRESS. Không chuyển sang train hoặc task ngoài phạm vi.

## Dữ liệu thực tế

- Folder `data/local/campaign-v4-three-kept-2026-11-12-r07/`, ảnh/nhãn/source giữ nguyên r06. Version nội dung `three-kept-4c4d10dc50f0f52e8c31`, metadata `group-review-r07-v1`;620 ảnh/2050 hộp vẫn bảo toàn,571 nhận nhãn/49 rejected. Sau loại49:1920 hộp Barcode284/Ripped356/Wornout1280;93 âm nhận/8 cách ly. Không sửa thêm bbox/pixel, không replay nhãn cũ hoặc gộp Notch.
- Đối chiếu lại102 nhóm/287 ảnh chưa nối của r06 bằng atlas toàn cục và gốc640 khi cần.207 nhóm đề xuất:117 khớp tiêu đề/ID/thiết kế,26 ghép bảo thủ có thể chứa nhiều cuốn,64 singleton chưa tìm thấy đối ảnh. Chưa chứng minh độc lập vật lý của mọi sách. CSV lịch sử và SIFT chỉ gợi ý; nền gỗ/tem chung không là bằng chứng. Decoder hiện có chỉ đọc thành công1 ảnh, không đủ chứng minh không trùng barcode. Chi tiết DATASET_KEPT_SPLIT_R07.md và reports/group-review.json/group-decisions.json.
- Đã tách gợi ý ghép sai Bukhak95/460 khỏi Dokgong90/157,577 khỏi SeismicDesign212/222;116 khỏi Camus,36 khỏi WantToMeetAgain. Nối Musso Seras-tu-là và LeaderConditions; grouping bảo thủ ghi rõ từng ca.49 cách ly giữ nguyên r06,8 âm cách ly giữ nguyên.
- Bản cần duyệt: `r07/proposed-02/index.html`; launcher ReviewThreeKept.cmd mở trang này.398 train/86val/87test,139/35/33 nhóm,65/14/14 âm. Hộp Barcode/Ripped/Wornout: train199/247/895,val41/55/156,test44/54/229. Seed45/attempt25, thuật toán kept-group-v2-class-negative. Mỗi lớp val/test hơn20 hộp; không tách nhóm để ép cân bằng sờn.
- SourceZIP SHA `dc2a81293b0f841b0fd187a410b869a1fc9021077ffc6221f9f33621ff978197`; manifest `8e316ef234b0cf9b9e83f14d58af6f51331473e95365776b2daf2a19b61e4f77`; CSV `aee6a076e830248d3c52f5742c7d0e0cbb937ebbf8ff3edfb5361af49ac2f8fc`; group-review `62186c1b70a977ba8c04c29330605576a2e7c566d2f564f30395e0d1322d89b6`.
- ProposalSHA `13ae187e222c1b8b33bbdb53093606cc07cb86b1f68bc465779e8f581c3cede9`. `split_ready=false`, không có approval/lock, notebook EXPECTED=None, GPU/Colab/camera NOT_RUN, chưa best.pt/last.pt. Bản đầu `proposed/` dùng v1/âm71/8/14 chỉ lưu đối chiếu, không chọn để khóa.

## Kiểm tra

reports/split-validation.json PASS audit nguồn/revisions, r06/source Downloads bất biến,620pixel/TXT không đổi, đúng49 cách ly, không giao image_id/group_id/fileSHA/pixelRGBSHA và tái đề xuất bằng nhau. Đây là kiểm nhóm được khai báo và trùng nội dung chính xác, không chứng nhận toàn bộ danh tính vật lý.

Regression trước sửa FAIL8/3/1 âm ở fixture48 nhóm; sau sửa PASS8/2/2.15 tests kept/training PASS7.494s. Toàn working tree152 tests PASS46.790s, có thay đổi cũ chưa commit; không gán kết quả này cho sourceHEAD nguyên trạng. Kiểm/publish cuối xem SESSION_LOG và r07 reports/publication-r07.json. UI browser NOT_RUN do file:// bị policy chặn từ phiên trước, không lách qua HTTP/khác surface. Không cài decoder mới.

## Human actions pending

Duyệt nhóm/split r07 proposed-02 đúng SHA trên, chú ý26 nhóm bảo thủ và64 singleton. Đây là gate một lần đã có trong kế hoạch, chưa yêu cầu duyệt train riêng. Nếu người dùng chấp nhận đúng bản: ghi approval gắn SHA, đóng A09, hoàn tất A10 bằng lock, tạo datasetZIP/checksum, điền EXPECTED rồi xử lý Colab/Drive theo quyền truy cập thực tế. Nếu thay nhóm, tạo review/proposal version mới rồi duyệt; không ghi đè r07. Không tự tạo approval thay người dùng.

## Xuất bản mã

Người dùng chỉ định repo truongthinh994/AI-book-sorting; origin cũ giữ nguyên. DraftPR https://github.com/truongthinh994/AI-book-sorting/pull/1, không merge. GitHubZIP chỉ có mã/tài liệu, không chứa ảnh/weights/reviewHTML. Source branch giữ lịch sử gốc, local ref publish/ai-book-three-kept giữ lịch sử repo đích.

Trước push: xác minh delivery:feat/three-kept-rebuild khớp ref publish. Commit source đúng allowlist; commit-tree từ sourceHEAD tree,parent publish, update-ref có kiểm parent rồi normalpush publish sang delivery:feat/three-kept-rebuild. Không push trực tiếp sourceHEAD khác lịch sử, không force. Giữ mọi modified/untracked legacy có sẵn; không stage chúng. CI/deliverySHA cuối ghi localpublicationreport và bàn giao.
