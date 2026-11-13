# Kept — hoàn tất lượt xem620 ảnh, tiếp tục duyệt nhóm/bbox

Ngày2026-11-12, tiếp tục A09/D29 từ [lượt4](DATASET_KEPT_PASS4.md). [Quy trình](THREE_KEPT_CAMPAIGN.md).

## Phạm vi đã xem

- Mở sheet051–078:220 ảnh mới #401–620, mỗi ảnh640px. Đã mở đủ620/620 ảnh trong chiến dịch kept, gồm100 ứng viên âm ban đầu. Việc mở đủ ảnh chưa chứng minh toàn bộ bbox/nhóm đã đạt yêu cầu.
- Mở riêng46 ảnh nghi vấn và13 ảnh tham chiếu nhóm; phóng to4x #401/#422/#503/#516/#611. Xem lại42 ảnh sửa trên6 sheet bbox r06.
- Các sheet gốc dùng nhãn chuyển ban đầu; sửa thực tế nằm trong version mới, không ghi đè nguồn hoặc bản trước. Phiên này hoàn thành cả lượt4 và5, thêm380 ảnh mới so với checkpoint240 ảnh.

## Sửa nhãn có bằng chứng

42 patch tạo r06 từ r05:

- Thêm36 vùng Barcode nhà xuất bản bị bỏ sót: #414,#416,#425,#435,#445,#448,#449,#453,#463,#470,#471,#487,#492,#496,#497,#499,#505,#509,#512,#513,#517,#519,#520,#521,#524,#542,#555,#560,#561,#564,#567,#568,#580,#584,#602,#613.
- Bỏ6 Barcode sai ở#422/#497/#500/#503/#516/#611: tem chữ, phần tem không còn vạch, gáy/gập bìa hoặc hình in. #497 đồng thời thêm đúng mã nhà xuất bản ở cạnh trái;#516 chỉ bỏ hộp nhỏ dưới cùng, giữ mã thư viện thật. #401 vẫn có vạch ở mép dưới, giữ hộp cũ.
- #608: hộp Wornout duy nhất thực tế bao tem mã thư viện EM0518824. Đổi lớp2→Barcode0, giữ tọa độ. Ảnh trở thành ứng viên âm thứ101 và vẫn chờ duyệt âm riêng. Không tự gọi đây là ảnh âm sạch.
- Phần mã bị cắt chỉ gán phạm vi nhìn thấy; không suy phần ngoài ảnh hoặc khẳng định giải mã. Các vùng1D cạnh QR được gán riêng, không gán QR. Không sửa Ripped, không gộp Notch vào rách.

## Nhóm, sai sót đã sửa và cách ly

102 đề xuất nhóm cho333 ảnh có group_id. **287 ảnh chưa có đề xuất liên kết**, không mặc định xem chúng là287 nhóm độc lập. Tất cả đề xuất còn chờ đối chiếu toàn cục, đặc biệt các cầu nối giữa bìa trước/sau và các họ bìa.

- Phát hiện đề xuất cũ sai: #5 có tiêu đề SF Philosophy, đã bị ghép vào ThirdHumanity4 ở lượt trước. Chuyển#5 sang nhóm SF Philosophy cùng#458/#479/#489/#550/#598 sau khi xem lại tiêu đề/ID; ghi erratum, không sửa lịch sử.
- #494/#605 có ID EM0486158, nối với ThirdHumanity4 #1/#111/#619. Bỏ mô tả đoán LaFontaine ở ghi chú ban đầu. Ảnh valid cũ#619 phải đi cùng nhóm sách trong train cũ.
- #587/#620 có cùng ID EM3214377, cùng The Art of Contrary Thinking với#471/#512. Ảnh test cũ#620 không độc lập với train cũ; không kế thừa split618/1/1.
- Đối chiếu mới nối thêm các mặt/gáy AutomaticControl, OECD, WerberSin, Nothomb, PianoDuo, KIPF, HumanDignity, ConcreteDeterioration và nhiều sách khác. Không ghép sách chỉ bởi cùng màu hoặc chủ đề. Ví dụ Dali trước/sau và KIPF gray vẫn có cầu nối chưa đủ bằng chứng.
- Thêm21 nhãn rejected, tổng49. #447/#483 cũng negative_review=rejected, tổng8. Nhãn mơ hồ gồm barcode rất xiên/mờ, rách so với khuyết/gập/bong film, và hộp cần sửa biên. Chi tiết số ảnh/lý do ở report cục bộ; không tự đổi thành mẫu âm.

## Bản r06 và kiểm tra

`data/local/campaign-v4-three-kept-2026-11-12-r06`, version `three-kept-4c4d10dc50f0f52e8c31`.

| Chỉ số | Giá trị |
|---|---:|
| Ảnh / hộp | 620 / 2050 |
| Barcode / Ripped / Wornout | 301 / 411 / 1338 |
| Nhãn rỗng / ứng viên âm | 42 / 101 |
| Nhãn pending / rejected / approved | 571 / 49 / 0 |
| Âm pending / rejected / approved | 93 / 8 / 0 |
| Đề xuất nhóm / ảnh có group_id | 102 / 333 |

Audit r05/r06 phát lại toàn bộ nguồn và revision PASS; ZIP gốc, manifest/CSV r05 và620 pixel ảnh giữ nguyên. Tất cả Ripped không đổi; Wornout chỉ đổi lớp ở#608 như patch ghi rõ. SHA ZIP `dc2a81293b0f841b0fd187a410b869a1fc9021077ffc6221f9f33621ff978197`; manifest r06 `8e316ef234b0cf9b9e83f14d58af6f51331473e95365776b2daf2a19b61e4f77`; CSV `9822e9c97ab686e06b54aa3a34c6e9ffd7c2959620f4d4b310eb68dc46dad849`.

Report ngoài Git trong r06/reports: `patches-05.json`, `box-spec-pass5.json`, `observations-pass5.json`, `group-proposals-pass5.json`, `errata-pass5.json`, `unresolved-group-queue.json`, `review-progress.json`, `validation-pass5.json`, `source-immutability-pass5.json`, `review.html`. Launcher ReviewThreeKept.cmd mở r06. Ảnh/weights không đưa lên GitHub.

Cần tiếp tục duyệt biên/lớp bbox,49 ca cách ly và liên kết đủ các nhóm trước khi A09 hoàn thành. Chưa tạo split đề xuất, xin duyệt cuối hoặc khóa dataset; notebook giữ EXPECTED=None. GPU/smoke/train/test model và browser/camera acceptance NOT_RUN. Không có best.pt/last.pt của chiến dịch mới.
