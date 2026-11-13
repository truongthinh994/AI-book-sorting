# Quy tắc rà nhãn Damaged Books năm lớp

Áp dụng cho đợt rà lại620 ảnh theo [kế hoạch đã duyệt](MODEL_TRAINING_PLAN.md). Đây là quy tắc thao tác và ví dụ bằng lời, không phải bằng chứng đã xem/duyệt các ảnh thật. Tiến độ và evidence chỉ ghi tại [TASKS](codex/TASKS.md).

## Năm lớp và ví dụ đối chiếu

| ID | Lớp | Ví dụ đúng | Ví dụ sai cần bỏ/sửa |
|---|---|---|---|
| 0 | Barcode | Hộp ôm vùng mã vạch nhìn thấy | Cả tem chữ/giá chỉ có chữ, logo hoặc đường trang trí không phải mã |
| 1 | Notch | Mép bìa mất một mảnh tạo khuyết cục bộ nhìn rõ | Góc khuất ngoài ảnh, bo góc nguyên bản, khe giữa hai cuốn |
| 2 | Ripped | Giấy/bìa nứt rách hoặc có vạt bị xé nhìn rõ | Nếp gấp không thấy rách, đường viền in, đường ráp gáy còn nguyên |
| 3 | Spot | Vết bẩn/ố khác bề mặt in có căn cứ nhìn thấy | Chữ, hình minh họa, hoa văn, bóng đổ hoặc lóe sáng |
| 4 | Wornout | Vùng sờn/tróc/mài mòn bề mặt hoặc mép | Mép sáng sạch, chữ trắng, chi tiết in giả cổ hoặc một nếp gấp đơn thuần |

Barcode không phải lỗi và hộp Barcode không chứng minh giải mã được nội dung. Tag không phải lớp đích. Không đổi một tem Tag thành Spot/Barcode chỉ để giữ hộp nguồn. Không dùng ví dụ bằng lời để đoán khi ảnh thật không đủ chi tiết.

Người dùng chốt2026-11-12: gán Barcode cho tất cả mã vạch1D nhìn thấy, gồm mã thư viện và ISBN của nhà xuất bản. Mỗi mã một hộp; mã bị cắt chỉ gán phần còn thấy nếu xác định được các vạch. Không gán QR hoặc tem số phân loại/chữ không có vạch. Không bỏ ISBN chỉ vì ảnh đã có mã thư viện.

Nếu không phân biệt được Notch/Ripped/Wornout, ghi rõ cặp lớp nghi vấn và vùng ảnh, giữ pending hoặc rejected. Không tự gộp các lớp. Một ảnh có thể có nhiều lớp thật ở các vùng khác nhau.

## Cách kiểm và vẽ hộp

1. Xem ảnh gốc trước, sau đó bật hộp nhãn; phóng to vùng nghi vấn. Xem ảnh khác cùng sách để phân biệt thiết kế in với lỗi thật. Phóng to không tạo thêm chi tiết.
2. Kiểm đủ mọi vùng nhìn thấy, không chỉ xem các hộp đang có. Thêm hộp cho lỗi bị bỏ sót; bỏ hộp sai đối tượng/lớp. Không gán nhãn phần bị che hoặc nằm ngoài ảnh.
3. Hộp ôm sát phần lỗi nhìn thấy, đủ toàn bộ vùng lỗi, không ôm cả cuốn khi lỗi chỉ ở góc. Một vùng lỗi liên tục dùng một hộp; các vùng tách biệt dùng hộp riêng. Không chia cùng vùng thành nhiều hộp li ti theo từng chữ/hạt nhiễu.
4. Bỏ hộp trùng cùng lớp/cùng vùng. Hộp chồng nhau chỉ giữ nếu có căn cứ là các vùng/lỗi riêng, không chép một vùng mơ hồ thành nhiều lớp.
5. Kiểm YOLO `class x_center y_center width height`: ID0–4, số hữu hạn, tọa độ chuẩn hóa, chiều rộng/cao dương, hộp nằm trong ảnh. Mọi thay đổi lưu ở version mới; nguồn không đổi.

## Kết luận cho mỗi ảnh

- **Dùng được:** nhãn đầy đủ/đúng, nhóm sách đủ căn cứ, các kiểm tra đạt.
- **Sửa được:** ghi danh sách thêm/bỏ/đổi lớp/đổi hộp và lý do; chỉ chuyển dùng được sau khi kiểm lại bản sửa.
- **Cách ly:** ảnh mờ/lóa/che, chưa rõ lớp hoặc nhóm, hoặc còn nhãn chưa sửa; ghi lý do cụ thể. Không phải tất cả ảnh cách ly đều là mẫu xấu vĩnh viễn.

Giữ `label_review=pending` khi chưa kiểm; `rejected` khi còn nghi vấn đã xác định; `approved` chỉ sau khi kiểm đủ. Ghi người duyệt và thời điểm trong nhật ký version mới. Trạng thái cũ của361 ảnh là lịch sử, không tự đại diện đợt rà mới.

## Mẫu âm

Kiểm riêng51 ứng viên sau bỏ Tag, bao gồm34 nhãn rỗng. Chỉ `negative_review=approved` khi đã kiểm không thấy Notch/Ripped/Spot/Wornout trên phần nhìn thấy. Ảnh Barcode-only vẫn là mẫu âm đối với lỗi; không phải ảnh nhãn rỗng đối với detection. Không gọi cả cuốn là sách lành chỉ vì một mặt không thấy lỗi.

Nếu bỏ hộp lỗi sai làm ảnh trở thành ứng viên mẫu âm, phải duyệt mẫu âm lại. Nếu thêm lỗi thật, ảnh không còn là mẫu âm. Ảnh khó nhìn không được thay thành nhãn rỗng để train background.

## Nhóm sách và nhật ký sửa

Cùng cuốn hoặc thiết kế bìa qua ảnh trước/sau/gáy và các góc chụp thuộc cùng group_id. Tên file không chứng minh nhóm; không đặt mỗi ảnh một nhóm để đủ split. Ảnh gần trùng chỉ là gợi ý; đối chiếu hình ảnh trước khi gộp. Chưa rõ quan hệ giữ cách ly.

Mỗi chỉnh sửa cần image_id, checksum nhãn trước/sau, nội dung thay đổi, lý do và người duyệt. Nhật ký sửa, CSV và ảnh thật nằm ngoài Git. Tạo bản nhãn mới có nội dung/version/hash riêng; không sửa tay vào prepared hiện tại rồi bỏ qua lỗi audit. Trang review hiện chỉ hỗ trợ nhóm/trạng thái, chưa sửa bbox; công cụ [sửa có audit trail](LABEL_REVISIONS.md) tạo version mới bằng CLI; trang hiện chưa sửa bbox trực tiếp.

## Điều kiện kết thúc đợt rà

Đủ620 kết luận có lý do; mọi ảnh dùng có nhãn đã duyệt và group_id; mọi mẫu âm dùng đã duyệt riêng; ảnh chưa rõ vẫn được liệt kê cách ly; báo cáo đếm ảnh/nhóm/lớp/hộp/mẫu âm và checksum. Chỉ sau đó mới tạo split và chuyển sang Colab.
