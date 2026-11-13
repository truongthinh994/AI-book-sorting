# Khóa dataset r07 và bàn giao Colab

> Cập nhật A02 2026-11-13: baseline YOLO11n trên T4 đã hoàn tất; validation và artifact thật xem [báo cáo baseline](BASELINE_R07.md). Chưa chọn model/ngưỡng hoặc đánh giá test cuối.

> Cập nhật 2026-11-13 sau mount: smoke n/s trên T4 đều PASS2epoch,batch16; A11/H08 hoàn thành. A02 full baseline là bước tiếp theo, chưa chạy. Xem [báo cáo smoke GPU](COLAB_SMOKE_R07.md).

Ngày 2026-11-13 (Asia/Saigon), người dùng chấp nhận bản r07 proposed-02 và yêu cầu làm tiếp. Approval ghi nguyên văn trong reports/user-approval-proposed-02.json ngoài Git, gắn proposal SHA `13ae187e222c1b8b33bbdb53093606cc07cb86b1f68bc465779e8f581c3cede9`. A09/A10 hoàn thành; A11 còn cần smoke GPU.

Không đổi nhãn/nhóm/split:571 ảnh,49 cách ly; train/val/test398/86/87, âm65/14/14. Tổng1920 hộp Barcode284/Ripped356/Wornout1280. Giới hạn26 nhóm bảo thủ/64 singleton vẫn giữ; không khẳng định đã giải mã đủ barcode hoặc độc lập mọi cuốn.

## Artifacts và kiểm chứng

- Local ZIP: data/local/campaign-v4-three-kept-2026-11-12-r07/split-locked.zip (20,203,802 bytes).
- ZIP SHA256: `0803bd193c8af403aa95645de0facf731fc974236298fd958854bcc602e8baab`.
- Split manifest SHA256: `90f4d6ed4e82cd5e584646ebcc60a345abd980e0b271695bddbf2d77af1b6ad4`.
- Version: `three-kept-4c4d10dc50f0f52e8c31`; profile book-three-kept-v1, bỏ Notch/Spot/Tag, không gộp Notch.
- Checksum độc lập: [configs/three-kept-r07.lock.json](../configs/three-kept-r07.lock.json).
- Tái tính đề xuất trước khóa PASS; giải nén ZIP mới, kiểm inventory/hash/mapping/nhóm/ID/counts/cách ly bằng local validator và helper thực nhúng notebook PASS. YAML train chỉ train/val; test vẫn giữ kín.
- [Drive folder](https://drive.google.com/drive/folders/1nRoTh0dG7AZYbTSeEinWYDwSSkXoaGe9), [dataset ZIP](https://drive.google.com/file/d/1YHF3vqfc9xnBwCl9O8WZUJNEd7jqMPPj/view), [lock](https://drive.google.com/file/d/1mIn-0y-acs8v6ZpDbhk0HkUD9eGzqjKP/view), [Colab](https://colab.research.google.com/drive/1kuX3sQIOzSh2HGX70_SAZ8wdiG4m2_9E). Không đổi sharing.

## Chạy tiếp

Colab hiện yêu cầu Google Sign in trong Edge; chưa kết nối GPU hoặc mount Drive. Người dùng đăng nhập đúng tài khoản chứa folder trên. Chọn GPU runtime rồi chạy ô cài đặt/mount, helper, dataset. Notebook đã điền EXPECTED và đường dẫn MyDrive/PBL5-three-kept-r07/split-locked.zip; chạy dữ liệu phải in PASS và398/86/87.

Smoke mặc định n/batch16/2epochs, run smoke-n16-01. Sau đó đổi MODEL='s', RUN_TAG='smoke-s16-01', giữ SMOKE=True; chạy ô train. OOM thì smoke mới batch8 cho cả n/s, tên mới; không ghi đè. Smoke không báo chất lượng. Khi cả hai đạt, chọn batch chung, SMOKE=False, MODEL='n', GENTLE=False, SEED=42 và tên run mới để chạy baseline100epochs/patience20. Giữ checkpoint ở Drive. Không chạy ô validation của smoke hoặc ô test cuối lúc này.

Kế hoạch các lượt sau xem [chiến dịch](THREE_KEPT_CAMPAIGN.md); tối đa8 lượt chính, threshold chỉ validation. GPU/Colab train NOT_RUN; chưa có best.pt/last.pt hoặc metrics thật. Không coi kiểm CPU là nghiệm thu A11.

Tài khoản Drive được connector get_profile xác minh: nguyentruongthinh9904@gmail.com (Thịnh Nguyễn Trường). Đây là tài khoản lưu artifacts; không suy từ tài khoản đăng nhập ChatGPT.
