# Kept — rà nhãn và nhóm lượt3

Ngày2026-11-12; tiếp tục A09/D29. [Lượt2](DATASET_KEPT_PASS2.md) · [Quy trình](THREE_KEPT_CAMPAIGN.md).

## Phạm vi đã xem

- Mở sheet016–030:120 ảnh mới #121–240, mỗi ảnh giữ640px. Cộng240/620 ảnh đã mở, còn380. Đây là bằng chứng đã xem, không đồng nghĩa duyệt xong toàn bộ bbox/nhóm.
- Mở riêng27 ảnh640: #59,#63,#122,#125,#127,#142,#152,#153,#159,#162,#165,#168,#176,#177,#181,#201,#202,#203,#205,#206,#209,#219,#221,#231,#235,#236,#239. #59/#63 là ca mã bị cắt đã xếp hàng từ lượt trước. Xem thêm crop4x của vùng Barcode#125 để kiểm phần tối mờ.
- Các sheet là nhãn bản chuyển ban đầu; sửa nhãn thực tế được lưu trong version mới r04, không ghi đè nguồn/r03.

## Sửa nhãn có bằng chứng

Thêm24 hộp Barcode trên24 ảnh: #59,#63,#122,#127,#142,#153,#159,#162,#165,#168,#177,#181,#201,#202,#203,#205,#206,#209,#219,#221,#231,#235,#236,#239. Phần lớn là mã nhà xuất bản bị bỏ sót khi ảnh có mã thư viện.

- #59/#63: chỉ gán phần vạch nhìn thấy ở cạnh ảnh, không suy ra kích thước ngoài khung. Không khẳng định giải mã thành công.
- #221: thêm mã1D, giữ QR cạnh đó ngoài lớp Barcode.
- Bỏ ba Barcode sai: #125 bao vùng gáy/gập bìa/tay và chữ, không nhận ra vạch1D; #152/#176 chỉ còn tem trắng/chữ do vạch đã nằm ngoài ảnh. Không coi bỏ nhãn là xác nhận ảnh âm sạch.
- Không tự đổi Ripped thành Wornout/Notch khi chưa rõ. Giữ các hộp lỗi nghi vấn để cách ly/rà tiếp, không đưa Notch trở lại lớp rách.

## Nhóm và cách ly

- Tổng35 đề xuất nhóm cho97 ảnh có group_id, từ đối chiếu tiêu đề, ID thư viện và thiết kế. Chưa chứng minh liên kết độc lập trên toàn620 ảnh; nhóm cũ chỉ được kế thừa từ lượt rà của chính chiến dịch kept này, không lấy từ chiến dịch5 lớp.
- Nối các góc mới vào Education Theory, Spain Digest11, họ bìa Hanja và History10. Gom conservative họ bìa KIPF vàng dùng chung ảnh thiết kế, dù tiêu đề/năm báo cáo khác nhau; không gọi chúng là cùng một cuốn vật lý.
- Thêm các nhóm như Werber Sin1/2, Made in China, Dokgong, Automatic Control, Laughing Man, Mars/Venus, OECD, Evolutionary Psychology, Camus Stranger, Myth of Individualism và sách quản trị tri thức có hình sách/vạch đánh dấu đỏ. Lý do/ảnh thành viên đầy đủ nằm trong report cục bộ.
- Thêm8 ảnh nhãn rejected: #125,#145,#160,#167,#179,#199,#226,#234. Lý do gồm barcode xiên/mờ, tem sai và khó phân biệt rách với nếp gấp/sờn/khuyết. #125/#160/#167 cũng negative_review=rejected. Không vẽ đoán vùng mờ hoặc coi mẫu âm chưa duyệt là dùng được.

## Bản r04 và kiểm tra

`data/local/campaign-v4-three-kept-2026-11-12-r04`, version `three-kept-e64b4b01e90b4ebf5e8a`.

| Chỉ số | Giá trị |
|---|---:|
| Ảnh | 620 |
| Barcode / Ripped / Wornout | 236 / 411 / 1339 |
| Tổng hộp | 1986 |
| Nhãn rỗng / ứng viên âm | 56 / 100 |
| Nhãn pending / rejected / approved | 604 / 16 / 0 |
| Âm pending / rejected / approved | 95 / 5 / 0 |
| Đề xuất nhóm / ảnh có group_id | 35 / 97 |

Audit phát lại nguồn6→mapping kept→r02→r03→27 patch r04 PASS. Audit r03 và r04 khớp nguồn ZIP/ảnh/nhãn gốc; hash ZIP Downloads vẫn `dc2a81293b0f841b0fd187a410b869a1fc9021077ffc6221f9f33621ff978197`. Manifest r04 SHA `43cc9f516c42719c3c7c5b4fb6f4b67618d59bff53f0446c066edb16bdb51727`; review.csv SHA `5c3463dc1e29839d9e009b82114ba7e5eddaafc1494756ca465265c6c5e30234`. CSV metadata có khóa riêng khi split sau này.

Các file ngoài Git trong r04/reports: `patches-03.json`, `observations-pass3.json` (120 kết luận), `group-proposals-pass3.json`, `review-progress.json`, `validation-pass3.json`, `source-immutability-pass3.json`, `review.html`. Launcher ReviewThreeKept.cmd mở r04. Nguồn/version cũ bất biến; pixel ảnh không sửa.

Baseline checker PASS;14 tests công cụ PASS9.827s. Thay đổi lần này là nhãn/nhóm/báo cáo, không sửa thuật toán model. Chưa có split đề xuất/được duyệt/khóa, chưa train hoặc nghiệm thu camera/browser UI.

Tiếp tục #241/sheet031 và16 ảnh rejected; còn380 ảnh cần xem, đồng thời rà đủ bbox và liên kết các nhóm trước khi A10 được mở. Chỉ xin duyệt cuối khi đã có split cụ thể; notebook vẫn EXPECTED=None.
