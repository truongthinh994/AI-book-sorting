# Rà mẫu âm và sửa quan hệ nhóm — lượt3

Ngày2026-11-12, tiếp tục A09 theo [kế hoạch](MODEL_TRAINING_PLAN.md) và [quy tắc nhãn](LABEL_REVIEW_GUIDE.md). Tiến độ chính thức ở [TASKS](codex/TASKS.md). Bản này vẫn chưa đủ điều kiện split/train.

## Phạm vi đã xem

Mở73 ảnh gốc640×640 không thu nhỏ trong các bảng đối chiếu:53 ứng viên âm của v2,10 ảnh P05/P06 và13 ảnh thuộc hai nhóm cần kiểm; có3 ảnh giao giữa các tập kiểm này. Trong73 ảnh có56 ảnh chưa được mở gốc ở các lượt trước. Cộng dồn104/620 ảnh đã mở gốc, còn516 ảnh trong queue mới. Xem gốc không đồng nghĩa hoàn tất kiểm mọi nhãn hoặc đã được người dùng duyệt.

Mỗi ảnh có image_id, phạm vi kiểm, nhận xét và actor Codex trong `visual-pass3/image-observations.json`/CSV. Các ảnh chỉ đối chiếu nhóm được đánh dấu rõ; không tự nhận đã kiểm đủ nhãn trên chúng.

## Quan hệ nhóm được sửa

| Ảnh theo index lượt1 | Kết luận có ảnh đối chiếu | Nhóm sau lượt3 |
|---|---|---|
| 9,18,121,151,158,246,295,411,524,527 | Ảnh158 chụp liền bìa trước L’Ultime Secret và mặt sau có chân dung, nối P05 với P06; họ gồm các tập đỏ/cam | review2_family_006 |
| 148,166,167,215 | Les Misérables tập2: tiêu đề gáy, hình khắc mặt người và nội dung Jean Valjean ở mặt sau khớp | visual_group_007 |
| 116,142,508,510 | Người đàn ông cười tập2: tiêu đề gáy510, mắt/dải đỏ ở trước và sau khớp | visual_group_087 |
| 191,328,442,591 | Notre-Dame de Paris: bìa sọc vàng/trắng, tranh và các góc khớp qua ảnh xoay đúng chiều | review3_book_notredame |
| 288,404 | François le Champi / George Sand: tên, bố cục chữ tối giản, mã EM0443528 và góc rách khớp | review3_book_champi |
| 396,607 | Human Relations Theory: tiêu đề, chân dung, bố cục và mã EM0510824 khớp | review3_book_relations |

Nhóm007 cũ trộn nhiều đầu sách; P08 của lượt2 gộp nhầm ảnh167 vào Người đàn ông cười. Lượt này sửa các liên kết đó, giữ lịch sử cũ. Không dùng việc cùng tác giả để kết luận cùng sách. Tên đọc sơ bộ của nhóm sọc đã được đối chiếu lại bằng ảnh xoay180°; nhật ký giữ bản sửa tên, không xóa dấu vết.

Đổi group_id của15 ảnh riêng biệt; nhật ký có19 lần đổi vì4 ảnh được chỉnh tên nhóm trong cùng lượt. Tổng387 ảnh có group_id, phần còn lại của các gợi ý cũ chưa được xác nhận trên toàn dataset. Các nhóm trong bảng chưa được chứng minh độc lập với516 ảnh gốc còn lại.

## Nhãn và mẫu âm

Tạo `data/local/campaign-v2/review-assistant-v3`, version `damaged-books-v1-five-revised-e25851381d844786`. V2 và nguồn bất biến.

- Sửa12 ảnh:49,200,205,234,260,274,297,336,415,424,559,508.
- Thêm12 hộp Barcode nhìn thấy; #205 là mã thư viện, các ảnh còn lại có mã nhà xuất bản. QR ở #49 không được gán Barcode. #274 chỉ lấy phần vạch còn trong ảnh. Giữ cách bao vùng ISBN kèm phần bổ sung liền cạnh như lượt2.
- Bỏ một hộp Notch ở mép dưới-phải nguyên vẹn của #508. Không suy ảnh không lỗi từ việc bỏ hộp đó; #508 là ứng viên âm mới, vẫn pending.
- Đã mở lại cả12 ảnh có hộp sau sửa và12 vùng mã được thêm. Mọi patch có hash trước/sau, toàn bộ nhãn, lý do, actor và thời điểm; không ghi người dùng đã duyệt.

| Chỉ số | V2 | V3 |
|---|---:|---:|
| Ảnh | 620 | 620 |
| Hộp | 3414 | 3425 |
| Barcode | 203 | 215 |
| Notch | 532 | 531 |
| Ripped | 411 | 411 |
| Spot | 930 | 930 |
| Wornout | 1338 | 1338 |
| Nhãn rỗng | 35 | 25 |
| Ứng viên âm | 53 | 54 |

Bảy ứng viên #8,#27,#89,#130,#354,#500,#530 có vết nhỏ, phản sáng, mờ hoặc ranh giới trang/bìa chưa rõ: `label_review=rejected`, `negative_review=rejected` để cách ly. #41,#215,#482 có vùng Barcode quá xiên/mờ: giữ nhãn hiện có, không vẽ đoán, đặt `label_review=rejected`; trạng thái âm vẫn pending vì lỗi Barcode không tự chứng minh có hư hỏng.

Tổng trạng thái nhãn:610 pending/10 rejected/0 approved. Mẫu âm:47 pending/7 rejected/0 approved;566 ảnh không cần duyệt âm. Chưa xác nhận ảnh âm nào thay người dùng. Nếp gấp/băng keo và thiết kế in chưa rõ không được tự đổi thành Ripped/Spot/Wornout.

## Bằng chứng và mở kết quả

`data/local/campaign-v2/visual-pass3/REVIEW_REPORT.md` có ảnh gốc, nhãn sau sửa, bảy ảnh cần xác nhận và nhận xét từng ảnh. Nhật ký gồm `label-changes-03.json`, `review-metadata-audit.json`, `image-observations.csv`, `pass-summary.json`, `validation.json`; queue còn lại là `remaining-original640.csv`. Dữ liệu thật được Git ignore.

Chạy `scripts/windows/ReviewDataset.cmd`: ưu tiên v3 rồi v2/v1/review-start. HTML dùng generator hiện có; kiểm đường dẫn launcher PASS, render trình duyệt NOT_RUN. Mở trực tiếp `review-assistant-v3/review.html` cũng được. Trang không tự lưu CSV xuống đĩa.

- SHA256 manifest: `bb1483f1caeeab575dfb558a1b9c38aff8be153fd935fd1ef0aef6c8b7c5023b`.
- SHA256 review.csv: `fd39cb513207761884c5d7b726065da78f535b77d078c7a8eaf8945f84fc6c6e`.
- Audit nguồn cộng lịch sử nhãn PASS; snapshot toàn bộ nguồn/v2 không đổi;620 hash ảnh duy nhất và khớp nguồn PASS.
- Kiểm độc lập SHA ZIP `dc2a81293b0f841b0fd187a410b869a1fc9021077ffc6221f9f33621ff978197` và1240 tệp nguồn với ZIP PASS. Trường `source_matches_zip=null` của audit được giữ đúng vì ZIP nằm cạnh thư mục nguồn.
- Phát lại trạng thái từ CSV v2 qua reset của revision engine rồi qua36 chỉnh metadata PASS. Lần kiểm đầu thiếu bước reset tự động của #508 nên FAIL; đã bổ sung đúng bước này vào phép kiểm độc lập, không đổi dữ liệu để ép PASS.

Version nhãn không khóa group_id hoặc trạng thái CSV; A10 phải khóa cả manifest và checksum CSV cuối. Chưa tạo split hoặc train/GPU/model/camera. Kiểm repo và unittest được ghi trong SESSION_LOG; không gán kết quả working tree cho SHA lịch sử.

Điểm tiếp tục: A09, mở516 ảnh trong queue, kiểm liên kết chéo với các nhóm đã sửa và hoàn tất nhận xét/nhãn; người dùng xác nhận các trường hợp mơ hồ và mẫu âm. Không bắt A10/A11 khi A09 chưa đủ acceptance.
