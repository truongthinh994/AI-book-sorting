# Thí nghiệm YOLO r07 — giai đoạn 3–4

Ngày 2026-11-13, theo yêu cầu tiếp tục của người dùng, đã hoàn tất A/B/C trên Colab T4 và tổng hợp báo cáo train/validation. **A640 là ứng viên tốt nhất trong các checkpoint cùng bài toán ba lớp đã đo**, nhưng Wornout vẫn yếu và chưa có model triển khai được khóa. D không chạy vì không đáp ứng điều kiện của thí nghiệm. Test và chọn threshold: **NOT_RUN**.

## Dữ liệu, cấu hình và phạm vi

Dataset gốc `three-kept-4c4d10dc50f0f52e8c31`, train398/validation86, giữ nguyên split và nhãn đã khóa trong [lock r07](../configs/three-kept-r07.lock.json). A/B dùng Barcode/Ripped/Wornout. C dùng bản sao train/val mới với mapping Barcode→Barcode, Ripped/Wornout→Damaged; ảnh và tọa độ box được giữ nguyên. Bản sao không chứa test.

Các lượt mới khởi tạo độc lập từ cùng `yolo11n.pt`, seed42, batch16, AdamW, lr0=.001, AMP và deterministic, giới hạn150epoch/patience50. Augmentation và tham số tối ưu giữ theo baseline; B đổi imgsz640→960, C đổi taxonomy trên bản sao. Save_period10 chỉ giảm số checkpoint định kỳ, không thay bước tối ưu. Môi trường thực tế: Ultralytics8.4.208, Python3.13.16, Torch2.14.1+cu130, CUDA13.0, Tesla T4.

Sau train, mỗi lượt nạp riêng `best.pt` để đo trên toàn bộ train và validation: conf=.001, NMS IoU=.7, max_det300, batch16, augmentation tắt; imgsz tương ứng640/960. P/R và bbox AP không phải accuracy phân loại toàn sách. Các chỉ số validation do trainer in lúc kết thúc không được trộn với kết quả explicit validation này.

| Lượt | Run | Taxonomy | Imgsz | Giới hạn / patience | Epoch thực tế / best |
|---|---|---|---:|---:|---:|
| Original | `n640-default-seed42-01` | 3 lớp | 640 | 100 / 20 | 38 / 18 |
| A | `A-n640-long-seed42-01` | 3 lớp | 640 | 150 / 50 | 106 / 56 |
| B | `B-n960-long-seed42-01` | 3 lớp | 960 | 150 / 50 | 89 / 39 |
| C | `C-n640-damaged-seed42-01` | Barcode/Damaged | 640 | 150 / 50 | 150 / 129 |
| D | SKIPPED | Detector + classifier | N/A | N/A | NOT_RUN |

A/B dừng sớm sau50epoch không cải thiện; C đạt giới hạn150. D chỉ phù hợp nếu hai lỗi là tình trạng riêng của barcode. Ảnh kiểm toán cho thấy nhiều hư hại ở bìa/gáy/viền sách, nên chưa có căn cứ để tạo nhãn Intact hoặc chạy bộ phân loại quanh barcode.

## Validation cùng bài toán ba lớp

| Lượt | Lớp | AP50 | AP50–95 |
|---|---|---:|---:|
| Original | Barcode | 79.16% | 54.45% |
| Original | Ripped | 12.59% | 5.11% |
| Original | Wornout | 7.37% | 2.24% |
| A | Barcode | 81.08% | 57.53% |
| A | Ripped | 27.53% | 9.14% |
| A | Wornout | 6.85% | 1.75% |
| B | Barcode | 83.57% | 60.41% |
| B | Ripped | 17.58% | 6.04% |
| B | Wornout | 6.36% | 1.97% |

Tiêu chí so ứng viên cùng taxonomy là mean AP50–95 của Ripped và Wornout trên validation; Barcode báo riêng. Train dùng chẩn đoán khả năng học/tổng quát hóa, không dùng chọn thắng.

| Lượt | Train damage macro AP50–95 | Val damage macro AP50–95 | Δ val so Original |
|---|---:|---:|---:|
| Original | 7.98% | 3.68% | 0.00 điểm phần trăm |
| A | 20.95% | **5.44%** | +1.77 điểm phần trăm |
| B | 16.84% | 4.00% | +0.33 điểm phần trăm |

A cải thiện Ripped, nhưng **không cải thiện Wornout**: AP50 Wornout giảm7.37%→6.85%, AP50–95 giảm2.24%→1.75%. B960 cũng không cải thiện Wornout và kém A640 về damage macro validation ở seed42. Không suy từ kết quả này rằng nâng độ phân giải luôn có ích.

A có gap train–val AP50–95 là19.18điểm cho Ripped và11.83điểm cho Wornout. Loss train tiếp tục giảm sau best epoch56 trong khi validation suy giảm ở cuối lượt; kết quả phù hợp với vấn đề tổng quát hóa sau điểm tốt nhất, chưa chứng minh một nguyên nhân duy nhất.

## C: bài toán gộp Damaged riêng

Bản sao C có train Barcode199/Damaged1142 box và validation Barcode41/Damaged211 box. Không sửa hay gộp nhãn gốc tại chỗ.

| Split | Lớp | AP50 | AP50–95 |
|---|---|---:|---:|
| train | Barcode | 99.31% | 90.03% |
| train | Damaged | **85.46%** | 50.83% |
| val | Barcode | 80.64% | 60.79% |
| val | Damaged | **16.89%** | 4.84% |

Damaged có gap train–val AP50 **68.57điểm phần trăm**, AP50–95 **45.99điểm**. Model C khớp train tốt nhưng chưa giải quyết được tổng quát hóa trên validation trong lượt này.

AP Damaged và AP riêng Ripped/Wornout là hai bài toán khác nhau. Không lấy AP gộp hoặc trung bình hai AP riêng để tuyên bố C thắng bài toán ba lớp. Campaign chưa có đánh giá A/B sau remap sang cùng taxonomy gộp để tách riêng lợi ích của việc train gộp.

## Toàn vẹn và kiểm chứng

- Đã kiểm969 file nguồn train/val và969 file nguồn bản sao C theo inventory trước/sau; ảnh/nhãn không đổi. Split manifest SHA256: `90f4d6ed4e82cd5e584646ebcc60a345abd980e0b271695bddbf2d77af1b6ad4`.
- `best.pt` gốc và `best_epoch18_backup.pt` giữ SHA256 `bcda8823ce5ee126a7d9a264d881ea7d9be73016c05b9b3f16b90dbef431564a`. Không ghi đè checkpoint này.
- Pretrained SHA256 chung: `0ebbc80d4a7680d14987a577cd21342b65ecfd94632bd9a8da63ae6417644ee1`.
- CSV A/B/C có106/89/150 dòng epoch; hash khớp experiment result. Best56/39/129 khớp cực đại all-class AP50–95 trong CSV. Actual args khớp cấu hình đã yêu cầu; toàn bộ22 hàng AP/P/R của bảng báo cáo khớp JSON đo được.
- GPU training và train/validation metrics: PASS. Test, threshold sweep, multi-seed và camera thực: NOT_RUN. Không dùng kiểm tra cấu trúc tài liệu hoặc CPU để thay bằng chứng GPU.

`best.pt` mỗi lượt được trainer chọn theo standard fitness toàn bộ lớp của lượt đó. Sau đó mới xếp hạng các checkpoint này bằng validation mean AP50–95 hai lỗi. Chưa quét mọi epoch để chọn riêng checkpoint tối ưu cho damage.

## Artifact và giới hạn

- [Báo cáo cuối đầy đủ trên Drive](https://drive.google.com/file/d/1rFMaVe0m5TWu0vhdsaYgdfT6puYYnpz5/view): AP50/AP50–95 theo lớp trên cả train/val, cấu hình, môi trường và diễn giải.
- [Bộ artifact báo cáo ZIP](https://drive.google.com/file/d/1MS9tWLvCN0p3gQ1hKjR3g4qUA2agOF4T/view): CSV, JSON, biểu đồ và kiểm chứng ngoài Git.
- [Thư mục báo cáo giai đoạn3–4](https://drive.google.com/drive/folders/15JTdzWk4pUIhQLoGumgaWB1XN9L2FLpH).
- Ứng viên A: [best.pt](https://drive.google.com/file/d/1Pbg3xc0JM48Bct5EpPSd5UyZO-zUQYip/view), [toàn bộ run](https://drive.google.com/drive/folders/1l_NxisOUUxq7Tha-R5lDK7KnxZ_fGe59). Đây là model để kiểm chứng tiếp, chưa khóa triển khai.
- [Drive dự án](https://drive.google.com/drive/folders/1b0L0gXSYFAWRnblHw3oa_Ar6g8Igqx0D); đối chứng cũ xem [BASELINE_R07.md](BASELINE_R07.md).

Chỉ seed42 được chạy; chưa có độ lệch chuẩn hay bằng chứng ổn định nhiều seed. Ảnh nguồn640×640 nên B960 không phục hồi chi tiết ảnh gốc đã mất. Nhãn hợp lệ cấu trúc không chứng minh đúng ngữ nghĩa;26 nhóm bảo thủ/64 singleton vẫn giới hạn độc lập theo cuốn. A150 cũng thay lịch learning-rate và thời điểm tắt mosaic so Original100, nên không diễn giải thí nghiệm là chỉ tiếp tục checkpoint18 thêm epoch.

Campaign giai đoạn3–4 đã hoàn tất; A là ứng viên để kiểm chứng tiếp, **chưa khóa triển khai**. Bước tiếp theo là rà lỗi Wornout/validation và kiểm chứng độ ổn định trước chọn threshold; không tự mở thêm lượt train. Chỉ chạy test khi người dùng cho phép sau khi chốt model/ngưỡng. Dữ liệu, ảnh, weights và log riêng không nằm trong Git.
