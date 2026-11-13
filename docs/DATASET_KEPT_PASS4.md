# Kept — rà nhãn và nhóm lượt4

Ngày2026-11-12, tiếp tục A09/D29 từ [lượt3](DATASET_KEPT_PASS3.md). Bản kế tiếp: [lượt5](DATASET_KEPT_PASS5.md).

Mở sheet031–050:160 ảnh mới #241–400, mỗi ảnh640px. Cộng400/620 ảnh đã mở. Mở riêng39 ảnh nghi vấn barcode và12 ảnh tham chiếu nhóm; phóng to4x #248/#256/#323/#387. Xem lại cả35 ảnh đã sửa trên5 sheet bbox r05. Đây là bằng chứng đã xem, chưa phải duyệt toàn bộ nhãn/nhóm.

35 patch tạo bản mới r05 từ r04: thêm35 Barcode trên34 ảnh (riêng#314 thêm hai vùng1D), bỏ một Barcode sai#351 chỉ bao chữ call-number/EM trên gáy. #248/#256 vẫn còn vạch thật ở cạnh ảnh nên giữ hộp cũ. #323 quá xiên/mờ để xác nhận, cách ly; #387 không thấy vạch trong phần tem trắng nên không vẽ đoán. Mã bị cắt#246/#275 chỉ gán phần nhìn thấy; #272 không gán QR thành Barcode. Không thay đổi pixel, Ripped hoặc Wornout trong lượt4.

r05: `data/local/campaign-v4-three-kept-2026-11-12-r05`, version `three-kept-919e5578ec8f82702ed5`.

| Chỉ số | Giá trị |
|---|---:|
| Ảnh / hộp | 620 / 2020 |
| Barcode / Ripped / Wornout | 270 / 411 / 1339 |
| Nhãn rỗng / ứng viên âm | 50 / 100 |
| Nhãn pending / rejected / approved | 592 / 28 / 0 |
| Âm pending / rejected / approved | 94 / 6 / 0 |
| Đề xuất nhóm / ảnh có group_id | 61 / 168 |

Thêm12 nhãn rejected:#269,#292,#300,#313,#323,#334,#340,#351,#365,#367,#374,#379;#323 cũng âm rejected. Lý do gồm barcode mờ, phản chiếu/bong film và khó phân biệt rách với gập/khuyết/sờn. Không biến ca mơ hồ thành âm sạch.

Nhóm được đề xuất từ tiêu đề, ID và thiết kế, gồm PianoDuo, Nietzsche, Hwarang, PostMisogyny, EscapeFromFreedom và các góc mới. #183 được sửa mô tả từ Einstein sang Nietzsche bằng tiêu đề/chân dung rõ; giữ nguyên báo cáo cũ và thêm erratum. Mọi nhóm vẫn phải đối chiếu toàn dataset; lượt5 đã phát hiện và sửa một đề xuất nhóm cũ sai, nên không dùng các đề xuất này như nhóm đã khóa.

Audit r04/r05 phát lại nguồn6 lớp→mapping kept→tất cả revision PASS; ZIP gốc và620 ảnh không đổi. SHA ZIP `dc2a81293b0f841b0fd187a410b869a1fc9021077ffc6221f9f33621ff978197`; manifest r05 `03759ddd032f711f446d09c96f3bf7b8e454cb13b0d4e063de960c9c011a03af`; CSV `d657d003f528a443f9d2c2ab937da7c5b202232c368864fb4d5933043b7bbe99`. CSV có khóa riêng khi tạo split.

Báo cáo cục bộ ngoài Git: `reports/patches-04.json`, `box-spec-pass4.json`, `observations-pass4.json`, `group-proposals-pass4.json`, `errata-pass4.json`, `validation-pass4.json`, `source-immutability-pass4.json`, `review-progress.json`, `review.html`.14 tests công cụ PASS8.862s. Chưa split, khóa hoặc train.
