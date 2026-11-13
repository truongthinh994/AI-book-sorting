Active task: NONE
Last updated: 2026-11-13
Branch: feat/three-kept-rebuild
Last green commit: e369f0dade213445bd929c4e61b2fb96fcf3367e

## Điểm tiếp tục — A02 baseline thật đã xong

Người dùng yêu cầu train; đã hoàn tất run n640-default-seed42-01 trên ColabT4,640/batch16/seed42,AdamW/lr0=.001/AMP,giới hạn100epochs/patience20. Epoch thực tế38,stopped_before_limit=True. A02 DONE,không có CODEX IN_PROGRESS. A11/H08/A09/A10 giữ DONE.

Đã kiểm ZIP/splitmanifest/inventory gốc trước train; dataset r07 giữ398/86/87 và49 cách ly,không đổi dữ liệu. Run identity/config/environment/CSV/weights SHA lưu Drive; explicit validation best.pt đủ3lớp. Macro damage AP50–95=0.036777; chi tiết docs/BASELINE_R07.md. Một baseline chưa chứng minh model tốt nhất hoặc sẵn sàng camera.

Notebook https://colab.research.google.com/drive/1Z9_1-5Y0WMHzDvIOPn1d_1MGYcG7QWT6?authuser=1
Drive https://drive.google.com/drive/folders/1b0L0gXSYFAWRnblHw3oa_Ar6g8Igqx0D
Local report data/local/campaign-v4-three-kept-2026-11-12-r07/reports/baseline-validation.json. Không commit dataset,weights hoặc log riêng.

## Một việc tiếp theo

A12: các cấu hình so sánh/seed tiếp theo theo chiến dịch trước khi chọn model/ngưỡng. Chưa tự chạy thêm model khác,threshold hoặc held-out test. Người dùng có thể yêu cầu lượt tiếp; không cần duyệt dataset lại. Nếu tiếp tục Colab, giữ môi trường/batch/hash; tên run mới riêng. Notebook có cell audit smoke sau train, không Run all.

## Giới hạn và kiểm tra

Threshold/test cuối NOT_RUN; không kết luận accuracy phân loại toàn sách từ bbox AP. GPU interruption/resume NOT_RUN,identity gate/CPU fixtures đã kiểm ởA11. Baseline checker49sources và15 tests PASS11.357s trên88bb351 + working-tree changes; mọi legacy modifications giữ nguyên và ngoài commit. CI tracked-tree của bản xuất bản ghi riêng trong report sau khi có kết quả thật.

## Xuất bản mã

Người dùng chỉ định repo truongthinh994/AI-book-sorting; origin cũ giữ nguyên. DraftPR https://github.com/truongthinh994/AI-book-sorting/pull/1, không merge. GitHubZIP chỉ có mã/tài liệu, không chứa ảnh/weights/reviewHTML. Source branch giữ lịch sử gốc, local ref publish/ai-book-three-kept giữ lịch sử repo đích.

Trước push: xác minh delivery:feat/three-kept-rebuild khớp ref publish. Commit source đúng allowlist; commit-tree từ sourceHEAD tree,parent publish, update-ref có kiểm parent rồi normalpush publish sang delivery:feat/three-kept-rebuild. Không push trực tiếp sourceHEAD khác lịch sử, không force. Giữ mọi modified/untracked legacy có sẵn; không stage chúng. CI/deliverySHA cuối ghi localpublicationreport và bàn giao.
