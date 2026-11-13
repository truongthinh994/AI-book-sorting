# Nhãn đã chốt và đề xuất nhóm/split r07

> Cập nhật 2026-11-13: người dùng đã duyệt r07 proposed-02; dataset đã khóa, notebook đã điền SHA và tải Drive. Colab đang chờ đăng nhập để smoke GPU. Xem [bàn giao hiện tại](THREE_KEPT_LOCK_R07.md); các trạng thái chưa duyệt bên dưới là lịch sử trước xác nhận.

Ngày2026-11-12, người dùng xác nhận: “ok chốt nhãn, cách ly 49 ảnh, làm bước tiếp theo”. Quyết định này chốt nhãn r06 và danh sách cách ly; chưa phải duyệt nhóm/split hay cho phép bỏ gate trước train.

## Bản dữ liệu và nguồn

Folder cục bộ ngoài Git: `data/local/campaign-v4-three-kept-2026-11-12-r07/`. Tạo bản riêng bằng `revise` với danh sách patch rỗng; không sửa thêm bbox, lớp hay pixel. Nguồn ZIP, manifest,620 ảnh và620 TXT khớp r06; r06/source ZIP Downloads giữ nguyên.

Version nội dung nhãn giữ `three-kept-4c4d10dc50f0f52e8c31` vì nội dung không đổi. Metadata rà có version `group-review-r07-v1`, CSV/nhóm và proposal có SHA riêng.620 ảnh/2050 hộp vẫn được bảo toàn trong bản rà;571 ảnh được chốt nhãn,49 rejected. Dữ liệu dự kiến dùng còn1920 hộp: Barcode284/Ripped356/Wornout1280.101 ứng viên âm gồm93 nhận theo nhãn đã chốt và8 cách ly; nhận âm chỉ áp dụng nội dung thấy trên ảnh, không kết luận toàn cuốn là sách tốt.

## Nhóm đề xuất và giới hạn

Đã đối chiếu lại102 đề xuất r06 và287 ảnh chưa nối nhóm. CSV lịch sử chỉ gợi ý; không kế thừa approval.17 sheet gợi ý cũ,10 sheet ảnh còn lại và28 sheet các nhóm dùng để đối chiếu toàn cục, mở gốc640 khi cần đọc tiêu đề/ID. SIFT chỉ dùng gợi ý; khớp nền gỗ hoặc tem thư viện chung không phải bằng chứng cùng sách.

207 nhóm có ảnh đủ điều kiện:117 nhóm khớp tiêu đề/ID/thiết kế,26 nhóm ghép bảo thủ và64 đề xuất nhóm đơn sau đối chiếu trực quan.26 thành phần bảo thủ có thể chứa nhiều cuốn khác nhau, nhằm giữ những cận cảnh có khả năng liên quan cùng tập; không tuyên bố cùng barcode hay cuốn vật lý. Nhóm đơn nghĩa là chưa tìm thấy ảnh cùng sách, không phải chứng minh độc lập. Nhóm và split vẫn cần lần duyệt cuối của người dùng.

Sửa các gợi ý sai:116 không thuộc Camus174;36 khác WantToMeetAgain;95/460 là Reading Bukhak, tách Dokgong90/157;577 là Seismic Diagnosis and Reinforcement, tách Seismic Design212/222. Nối lại Musso Seras-tu-là180/469/530/591/594/612 và Leader Conditions98/300/326/370/383/420. Các tập DIGEST100 giữ chung thiết kế dù khác tập sách. Chi tiết từng nhóm, singleton, ghép bảo thủ và lý do nằm trong `reports/group-review.json` và `group-decisions.json`.

OpenCV barcode detector trên các hộp1D ở1x/3x chỉ giải mã được1 ảnh. Không có bằng chứng giải mã đủ toàn dataset; không suy không trùng sách từ việc giải mã thất bại. Check tự động bên dưới chỉ xác nhận ID ảnh/hash chính xác và group_id được khai báo, không thay thế duyệt danh tính sách.

## Đề xuất hiện tại

`proposed-02/index.html` hiển thị các góc và bbox theo nhóm, tập, lớp, âm/cách ly, thống kê và mức chắc chắn. Launcher `scripts/windows/ReviewThreeKept.cmd` mở trang này trên máy có dữ liệu cục bộ. GitHub ZIP chỉ chứa mã/tài liệu, không chứa trang có ảnh hay dataset.

| Tập | Ảnh | Nhóm | Barcode | Ripped | Wornout | Ảnh âm |
|---|---:|---:|---:|---:|---:|---:|
| Train |398|139|199|247|895|65|
| Validation |86|35|41|55|156|14|
| Test |87|33|44|54|229|14|

Số nhóm đóng góp Barcode/Ripped/Wornout: train97/52/120, validation21/15/28, test22/12/28. Tỷ lệ ảnh69,70%/15,06%/15,24%; val/test đều vượt20 hộp/lớp. Sờn vẫn lệch156/229 giữa val/test; giữ nguyên nhóm, không tách sách để ép số.

Thuật toán `kept-group-v2-class-negative` chọn seed45,attempt25 trong3200 phương án seed42–73. Nguyên nhóm và đủ3 lớp là điều kiện; sau đó giảm tổng sai lệch tỷ lệ hộp ba lớp cộng tỷ lệ ảnh âm, rồi tỷ lệ ảnh, seed/attempt. Không dùng kết quả model. Bộ chọn trước chỉ tính lớp nên chọn71/8/14 ảnh âm; giữ proposal cũ trong `proposed/` để đối chiếu, không khóa nó. Regression48 nhóm chứng minh lỗi8/3/1 trước sửa và8/2/2 sau sửa.

## Kiểm tra và checksum

`reports/split-validation.json` PASS: audit nguồn/revision đầy đủ; r06 manifest/CSV và pixel/nhãn không đổi; cách ly đúng49; không giao image_id, group_id, SHA tệp hoặc SHA pixel RGB chính xác giữa ba tập; tái đề xuất cùng đầu vào cho cùng JSON/SHA. Các kiểm này không chứng minh không còn cùng sách dưới ID chưa đọc được.

- Source ZIP: `dc2a81293b0f841b0fd187a410b869a1fc9021077ffc6221f9f33621ff978197`.
- Manifest: `8e316ef234b0cf9b9e83f14d58af6f51331473e95365776b2daf2a19b61e4f77`.
- Review CSV: `aee6a076e830248d3c52f5742c7d0e0cbb937ebbf8ff3edfb5361af49ac2f8fc`.
- Nhóm: `62186c1b70a977ba8c04c29330605576a2e7c566d2f564f30395e0d1322d89b6`.
- Proposal SHA: `13ae187e222c1b8b33bbdb53093606cc07cb86b1f68bc465779e8f581c3cede9`.

15 tests kept/training PASS7.494s; toàn working tree152 tests PASS46.790s, gồm thay đổi lịch sử có sẵn chưa đưa vào commit. Kiểm CI bản tracked được ghi riêng ở SESSION_LOG/report xuất bản. Browser UI và Colab GPU NOT_RUN; không coi static/unit test là nghiệm thu giao diện hoặc chất lượng model.

## Gate tiếp theo

Duyệt đúng nhóm/split r07 `proposed-02` với SHA trên, chú ý26 nhóm bảo thủ/64 singleton. Chỉ khi người dùng chấp nhận bản cụ thể này mới tạo approval gắn SHA, khóa dataset ZIP/manifest, điền EXPECTED và đưa lên Drive để smoke/train. Nếu cần đổi nhóm, tạo review/proposal version mới trước khi duyệt; không ghi đè bản này. Hiện `split_ready=false`, không có approval/lock/weights; notebook giữ `EXPECTED=None`. Không train hoặc báo hoàn thành đánh giá test.
