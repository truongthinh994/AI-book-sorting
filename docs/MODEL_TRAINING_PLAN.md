# Kế hoạch làm sạch dataset và huấn luyện model sách trên Colab

Ngày chốt: 2026-11-12. Nguồn: kế hoạch người dùng đã duyệt trong chat.
Tiến độ chỉ ghi tại [TASKS](codex/TASKS.md); điểm tiếp tục tại [STATE](codex/STATE.md).

## Mục tiêu và hiện trạng

Giữ năm lớp theo ID: 0 Barcode, 1 Notch, 2 Ripped, 3 Spot, 4 Wornout. Barcode không phải lỗi. Quyết định bổ sung2026-11-12: gồm mọi mã1D nhìn thấy, thư viện và ISBN; không gồm QR/tem chữ-số. Bỏ Tag nguồn ID4, đổi Wornout nguồn ID5 thành ID4; không xóa vùng tem trên ảnh.

Rà toàn bộ 620 ảnh gốc rồi tạo dataset mới; chỉ dùng ảnh đủ tin cậy, không cố đưa đủ 620 ảnh vào train. Tối đa tám lượt train có kiểm soát; chưa thêm ảnh camera riêng, chưa tích hợp app/ESP32. Không cam kết accuracy trước khi đo.

Đã kiểm trong phiên rà soát: 620 ảnh 640×640 đọc được; ảnh/nhãn khớp ZIP nguồn SHA256 `dc2a81293b0f841b0fd187a410b869a1fc9021077ffc6221f9f33621ff978197`; không có ảnh trùng byte. Sau bỏ Tag có 34 nhãn rỗng, 51 ứng viên không có lỗi. Bản phát hành cũ dùng 361 ảnh/121 nhóm (253/54/54), cách ly 259 ảnh; test chỉ có hai ảnh không có nhãn lỗi. Khoảng 71% hộp Spot trong bản đã duyệt có diện tích dưới 32×32 pixel ở ảnh 640. Đây là kiểm dữ liệu/cấu trúc, không phải rà trực quan lại 620 ảnh hay kết quả AI.

## Trình tự thực hiện

| Bước | Đầu ra cần có | Điều kiện chuyển bước |
|---|---|---|
| 1. Quy tắc nhãn | [Hướng dẫn rà nhãn](LABEL_REVIEW_GUIDE.md), ví dụ đúng/sai của năm lớp | Có cách xử lý nhãn thiếu, sai, trùng, mơ hồ và mẫu âm |
| 2. Rà 620 ảnh | Quyết định cho từng ảnh; ưu tiên 259 ảnh cách ly rồi rà lại 361 ảnh cũ | Mỗi ảnh dùng được, sửa được hoặc cách ly, có lý do; chưa rõ thì chưa duyệt |
| 3. Sửa nhãn ở bản mới | Ảnh nguồn bất biến, nhật ký sửa, checksum trước/sau, version mới | Nhãn sửa có đối chiếu; ảnh không có lỗi được duyệt riêng; không sửa đè nguồn |
| 4. Rà nhóm sách | Cùng cuốn/thiết kế bìa thuộc cùng nhóm qua các mặt/góc chụp | Kiểm cả ảnh gần trùng; nhóm cũ là gợi ý, chưa rõ tiếp tục cách ly |
| 5. Khóa split mới | Khoảng 70/15/15 theo nhóm, seed42; phân bố lớp và mẫu âm | Không giao nhau nhóm/ID/nội dung ảnh; cả ba tập đủ năm lớp; báo cáo số ảnh và nhóm, SHA256 |
| 6. Chuẩn bị Colab | Notebook nhận đúng dataset version/SHA; lưu Drive, checkpoint và môi trường | Smoke 1–2 epoch, kiểm resume và bộ nhớ; smoke không là bằng chứng model tốt |
| 7. Thử nghiệm | Ma trận tối đa tám lượt, cùng split, artifact riêng | Chỉ dùng validation để so sánh; ghi mọi khác biệt cấu hình |
| 8. Đánh giá cuối | Model/ngưỡng đã khóa, báo cáo test và giới hạn | Test một lần sau chốt; không chỉnh model theo test rồi báo đánh giá độc lập |

Sau khi train bắt đầu, không đổi split theo kết quả. Nếu phát hiện nhãn sai cần sửa, dừng chiến dịch, tạo version mới và ghi rõ các lượt không còn so sánh trực tiếp được. Augmentation chỉ áp dụng cho train. Không sao chép ảnh/biến thể của cùng sách qua các tập để cân bằng số lượng.

## Yêu cầu công cụ

Bổ sung2026-11-12: A10 phải có web cục bộ xem ba tập theo nhóm sách, mọi góc chụp cạnh nhau, lọc lớp/mẫu âm, ảnh cách ly và cảnh báo giao tập. Không chia ngẫu nhiên từng ảnh của cùng cuốn. [Chi tiết công cụ và web split](LABEL_REVISIONS.md).

- Giữ bản nguồn và release361 cũ; tạo thư mục version mới trong `data/local` được ignore. Mọi nhãn sửa cần image ID, lý do, người duyệt, nội dung trước/sau và checksum. Bản corrected phải được audit theo nguồn cộng các chỉnh sửa đã ghi, không giả là chuyển đổi nguyên trạng.
- Manifest/version phải phản ánh nội dung nhãn và cách chia; notebook chỉ nhận ZIP có SHA256/version đã khóa độc lập, không tự tin mọi manifest người dùng tải lên.
- Notebook lưu config yêu cầu và config thực tế, seed, phiên bản Python/Torch/CUDA/Ultralytics, GPU, model/dataset hash, dự đoán validation, metrics và checkpoint. YAML train không chứa test.
- Resume dùng `last.pt`, cùng dataset/version/config và run cũ; tạo run mới không phải resume. Không ghi đè lượt đã chạy. Không cài AI vào môi trường collector.

## Ma trận train

Cấu hình chung: pretrained YOLO11, epochs100, patience20, AdamW, lr0=0.001, seed42, AMP. Kiểm bộ nhớ trước để chọn batch16 hoặc batch8 thống nhất cho ba lượt đầu. Giữ thư viện ghim theo notebook; lưu cấu hình augmentation thực tế thay vì phụ thuộc mặc định không ghi nhận.

| Lượt | Cấu hình | Giả thuyết |
|---|---|---|
| 1 | YOLO11n/640 | Baseline |
| 2 | YOLO11s/640 | Model lớn hơn có cải thiện không |
| 3 | YOLO11n/960 | Đầu vào lớn hơn có giúp lỗi nhỏ không |
| 4 | Kiến trúc/kích thước tốt nhất của 1–3, lr0=0.0003 | Learning rate thấp hơn |
| 5 | Cùng kiến trúc/kích thước đó, lr0=0.003 | Learning rate cao hơn |
| 6 | Cấu hình tốt nhất 1–5; mosaic0.25, scale0.2, hsv_s0.3, hsv_v0.2 | Augmentation nhẹ hơn, các tham số khác giữ nguyên đối chứng |
| 7–8 | Cấu hình tốt nhất 1–6, seed43 và seed44 | Độ ổn định qua ba seed |

Không dùng điểm của seed43/44 để chọn lại bản có test tốt nhất. Bản bàn giao giữ seed42. Ảnh nguồn chỉ640×640; thử960 không khôi phục chi tiết đã mất. Lượt lỗi/OOM ghi FAIL và cấu hình thực; không tính như một kết quả train hoàn chỉnh.

## Chọn model, ngưỡng và kiểm tra cuối

1. Báo precision/recall/AP50/AP50–95 từng lớp. Xếp hạng bằng macro AP50–95 của bốn lỗi; nếu bằng, dùng F2 Ripped rồi kích thước model nhỏ hơn. Barcode báo riêng, không làm tăng điểm lỗi tổng hợp.
2. Chọn threshold trên validation: F2 cho Ripped, F1 cho bốn lớp khác. Ghi confidence, IoU matching/NMS và cách ghép bbox dùng khi đo. Chỉ số P/R mặc định Ultralytics chưa phải P/R tại ngưỡng vận hành.
3. Xem false positive/negative: Spot nhỏ, Wornout trên chữ/hình in, mép bìa, bóng/lóa và ảnh không lỗi. Nếu kết quả kém, xác định lỗi dữ liệu hay model trước khi tăng epochs.
4. Báo kết quả cả ba seed, so baseline trên cùng version/split. Chốt model seed42, config và threshold trước khi mở test.
5. Test một lần, lưu báo cáo số mẫu/nhóm, từng lớp, false positive trên mẫu âm, hash model/data và giới hạn. Không suy khả năng đọc nội dung barcode từ bbox Barcode. Không suy khả năng chạy camera thực từ dataset này.

## Phân công và bàn giao

Codex chuẩn bị quy tắc, công cụ dữ liệu, split, notebook và báo cáo; thực hiện từng task có kiểm tra. Người dùng xác nhận ảnh mơ hồ, chạy Colab GPU/kết nối Drive và gửi ZIP artifacts sau mỗi lượt. Trường hợp thiếu xác nhận giữ cách ly, không tự coi đã duyệt.

Gói cuối cần có dataset ZIP/manifest/checksum, nhật ký duyệt/sửa và phân bố; notebook/config; best.pt và checkpoint; results.csv, experiment-summary.csv, metrics, confusion/PR curves và ảnh dự đoán; model metadata, threshold và báo cáo test. Ảnh/weights nằm ngoài Git, chỉ code và tài liệu được commit. Ledger giữ task mới riêng với bằng chứng version cũ, không xóa lịch sử H14/A01.

## Tài liệu tham khảo

- [Ultralytics: chuẩn bị dữ liệu](https://docs.ultralytics.com/guides/preprocessing_annotated_data/)
- [Ultralytics: train và resume](https://docs.ultralytics.com/modes/train/)
- [Ultralytics: đọc metrics](https://docs.ultralytics.com/guides/yolo-performance-metrics/)
- [Nguồn Damaged Books v1, CC BY4.0](https://universe.roboflow.com/atcom21-gmail-com/damaged-books/dataset/1)
