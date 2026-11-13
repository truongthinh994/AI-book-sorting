# Baseline YOLO11n r07

Ngày2026-11-13, theo yêu cầu người dùng, đã chạy thực tế run `n640-default-seed42-01` trên Colab T4 và kiểm validation của best.pt. A02 DONE: pipeline train thật có config/seed/split/model/artifacts. Đây là một baseline, chưa phải model bàn giao đã được chọn qua A12/A13.

## Cấu hình và dữ liệu

YOLO11n pretrained,640px,batch16,seed42,AdamW,lr0=.001,AMP,deterministic,giới hạn100epochs,patience20. Dừng sớm tại **epoch38** vì20epoch liên tiếp không cải thiện; log trainer chọn **best.pt ở epoch18**. Môi trường: {'python': '3.13.16', 'torch': '2.14.1+cu130', 'cuda': '13.0', 'gpu': 'Tesla T4', 'ultralytics': '8.4.208'}. Augmentation mặc định Ultralytics của cấu hình đối chứng, không chuyển gentle giữa lượt.

Dataset `three-kept-4c4d10dc50f0f52e8c31`;398train/86validation/87test,49 ảnh cách ly. ZIP và manifest checksum giữ [bản khóa](../configs/three-kept-r07.lock.json). Trước train đã kiểm lại ZIP,split_manifest và từng file gốc theo inventory; cache Ultralytics là file dẫn xuất không thay ảnh/nhãn. Test không có trong YAML train/validation.

## Validation best.pt

Chỉ số dưới đây đo trên86 ảnh validation, không phải accuracy phân loại sách hay đánh giá camera. P/R là điểm vận hành mặc định của Ultralytics, chưa phải threshold được chọn cho hệ thống.

| Lớp | Precision | Recall | AP50 | AP50–95 |
|---|---:|---:|---:|---:|
| Barcode | 57.49% | 80.49% | 79.16% | 54.45% |
| Ripped | 14.79% | 14.55% | 12.59% | 5.11% |
| Wornout | 12.14% | 16.03% | 7.37% | 2.24% |

Macro AP50–95 riêng Ripped/Wornout: **3.68%**. Hai lớp lỗi còn thấp; baseline này chưa đủ căn cứ để đưa vào phân loại thực tế. Barcode báo riêng. Chưa kết luận cấu hình này tốt nhất, chưa so đủ model/augmentation/seed43/44; không điều chỉnh theo test.

## Artifact và bằng chứng

- Run `n640-default-seed42-01` trong [Drive dự án](https://drive.google.com/drive/folders/1b0L0gXSYFAWRnblHw3oa_Ar6g8Igqx0D); [notebook đang dùng](https://colab.research.google.com/drive/1Z9_1-5Y0WMHzDvIOPn1d_1MGYcG7QWT6?authuser=1).
- best.pt SHA256: `bcda8823ce5ee126a7d9a264d881ea7d9be73016c05b9b3f16b90dbef431564a`.
- last.pt SHA256: `3844063269e0a4a537859b606ef14bd383cd7b1ce70f1cdee05b029b99872710`.
- Config yêu cầu,train/args.yaml thực tế,run_identity.json,pip-freeze.txt,initial weights SHA,results.csv,weights và curves được lưu ngoài Git. Báo cáo baseline-validation.json có per-class validation,checksums,environment và tổng số epoch; đã đọc lại qua Drive.
- Training và explicit validation trên GPU thật PASS. Baseline CPU checker PASS49sources và15 kept/training tests PASS11.357s trên source88bb351 + legacy working-tree changes; không gán các kết quả này cho pristine HEAD. Không thay source Python runtime trong phiên A02.
- Threshold selection NOT_RUN; held-out test NOT_RUN; interrupted GPU continuation NOT_RUN. Các checkpoint sau run hoàn tất được trainer strip optimizer theo log; không lấy smoke hoặc checkpoint hoàn tất để giả là resume run đang dở.

## Điểm tiếp tục

A12 còn TODO. Kế hoạch hiện có thử các cấu hình n/s × default/gentle seed42 rồi hai ứng viên qua seed43/44, tối đa8 lượt chính, macro AP hai lỗi để so sánh và threshold trên validation. Chưa tự bắt đầu task/lượt tiếp theo trong phiên này. Dataset Damaged Books chưa đại diện camera thật;26 nhóm bảo thủ/64 singleton và sự lệch lớp vẫn là giới hạn của dữ liệu.

Model tải dùng thử: [best.pt](https://drive.google.com/file/d/1k1WyzJu7yvO3XDO8itUX2VnyKq7MW-iI/view); [last.pt](https://drive.google.com/file/d/19eNVkX1lgo7OKJ_med3_GpMaKa-73yQB/view); [toàn bộ run](https://drive.google.com/drive/folders/1_k_Wv8mm6aDW3fgXhKcXyKdl-ymo3MKV).

[Báo cáo JSON thực trên Drive](https://drive.google.com/file/d/1OTk6ysBT2Z0LQr3ncWBQIIs2hlnnq0h9/view) đã đọc lại và đối chiếu bằng với kết quả quan sát trong Colab.
