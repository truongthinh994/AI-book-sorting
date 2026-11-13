# Smoke GPU r07 trên Colab

Ngày2026-11-13, A11/H08 đạt kiểm chạy GPU thật. Đây là bằng chứng khả năng chạy/lưu artifacts, không phải kết luận chất lượng model hoặc A02 full training.

## Dữ liệu và môi trường

ZIP đã khóa giữ nguyên SHA0803bd193c8af403aa95645de0facf731fc974236298fd958854bcc602e8baab và split manifest SHA90f4d6ed4e82cd5e584646ebcc60a345abd980e0b271695bddbf2d77af1b6ad4. Colab kiểm inventory/profile/mapping/hash/nhóm/ID/counts PASS:398train/86val/87test.49 ảnh cách ly không tham gia; test không được dùng để đánh giá model.

Tesla T4 14913MiB;Python3.13.16,Torch2.14.1+cu130,Ultralytics8.4.208. Cả hai smoke dùng imgsz640,batch16,seed42,AdamW,lr0=.001,AMP,2epochs/patience2. Batch16 được chọn chung. Smoke2epoch có close_mosaic mặc định đóng mosaic từ đầu nên không đại diện augmentation của lượt100epoch.

| Run | Kết quả | GPU_mem lớn nhất trong log | CSV epoch | Checkpoints |
|---|---|---|---|---|
| smoke-n16-01 | PASS | 2.86G | 2 | best.pt/last.pt,5,500,506 bytes mỗi file |
| smoke-s16-01 | PASS | 5.12G | 2 | best.pt/last.pt,19,173,530 bytes mỗi file |

## Artifacts và giới hạn bằng chứng

- [Notebook hiện tại](https://colab.research.google.com/drive/1Z9_1-5Y0WMHzDvIOPn1d_1MGYcG7QWT6?authuser=1), [Drive tài khoản Pro](https://drive.google.com/drive/folders/1b0L0gXSYFAWRnblHw3oa_Ar6g8Igqx0D), [summary có SHA checkpoints](https://drive.google.com/file/d/1ki-XlQsorFHJhaOlwEdcw-f038mQmP9U/view).
- Drive readback xác nhận artifacts thật. Mỗi run có run_identity.json,initial-weights-sha256.txt,pip-freeze.txt,runtime.yaml,train/args.yaml,results.csv,curves và weights. Summary thực kiểm cấu hình/version/SHA/environment,cả best/last và đúng2dòng CSV.
- Cổng check_resume được kiểm với identity đúng và SHA dataset sai trên checkpoint thật. Tests CPU kiểm từ chối resume khác identity/thiếu checkpoint PASS. **Chưa thực hiện gián đoạn rồi resume GPU**; không coi kiểm fingerprint là chạy lại GPU. Smoke kết thúc nên optimizer bị strip theo log; dùng run mới cho baseline.
- Notebook copy trong folderPro, nguồn gốc/ZIP/bản cũ vẫn giữ. FolderPro general access restricted, tài khoản Drive connector hiện có editor trên đúng folder, tắt thông báo email. Không chia sẻ công khai, không bật file URL permission của extension.
- User đã xác nhận quyền đọc/sửa Drive cho notebook tại bước mount; không ghi credential hoặc OAuth URL/token vào Git. Chưa xác minh số compute units hoặc quyền lợi subscription cụ thể từ membership badge.

## Tiếp tục A02

Chạy run mới n640-default-seed42-01 với MODEL='n',GENTLE=False,SEED=42,BATCH=16,SMOKE=False,RESUME=False; mặc định100epochs/patience20. Kiểm tên chưa có trước chạy. Đây là task tiếp theo, chưa tự bắt đầu trong phiên A11. Không chọn model bằng AP smoke. Chưa threshold validation hoặc test cuối, chưa có model bàn giao.
