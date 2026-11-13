Active task: NONE
Last updated: 2026-11-13
Branch: feat/three-kept-rebuild
Last green commit: e369f0dade213445bd929c4e61b2fb96fcf3367e

## Điểm tiếp tục — A11/H08 smoke GPU đạt, A02 baseline sẵn sàng

Người dùng đã chọn tài khoản Pro trong Colab và yêu cầu làm tiếp; đã xác nhận cấp quyền mount Drive ngay tại bước OAuth. Đã tạo folder PBL5-three-kept-r07 trong MyDrive của tài khoản Pro; tài khoản connector hiện có được editor trên đúng folder, general access restricted, tắt email thông báo. Copy ZIP/lock/notebook qua Drive API, không bật quyền file URL của extension. Không đăng email tài khoản Pro hoặc log riêng lên Git.

Notebook đang mở: https://colab.research.google.com/drive/1Z9_1-5Y0WMHzDvIOPn1d_1MGYcG7QWT6?authuser=1
Drive: https://drive.google.com/drive/folders/1b0L0gXSYFAWRnblHw3oa_Ar6g8Igqx0D
Summary: https://drive.google.com/file/d/1ki-XlQsorFHJhaOlwEdcw-f038mQmP9U/view

GPU Tesla T4 14913MiB,Python3.13.16,Torch2.14.1+cu130,Ultralytics8.4.208. Drive mount và split SHA thực PASS:398/86/87,version three-kept-4c4d10dc50f0f52e8c31. Dataset/nhãn/nhóm/49 cách ly không đổi; checksum độc lập configs/three-kept-r07.lock.json. A09/A10 vẫn DONE.

smoke-n16-01 và smoke-s16-01 mỗi2epoch,batch16,640,seed42,AdamW,lr0=.001,AMP hoàn tất; GPU_mem trong log n2.86G/s5.12G,không OOM. Đã kiểm CSV2dòng/run,checkpoint best/last tồn tại và SHA; config/seed/hash/environment khớp,check_resume nhận identity đúng và từ chối SHA sai. Các tests CPU resume giữ riêng; chạy tiếp GPU sau gián đoạn NOT_RUN. Hai smoke đã kết thúc và optimizer được Ultralytics strip; không resume chúng để biến thành baseline.

A11/H08 DONE theo evidence smoke; A02 TODO, không tự bắt đầu task kế tiếp. Chưa có lượt100epoch,model bàn giao,threshold hoặc đánh giá test. Không dùng AP smoke để chọn model. Chi tiết docs/COLAB_SMOKE_R07.md.

## Một việc tiếp theo

A02: giữ runtime và dataset hiện có; ở ô train chọn MODEL='n',GENTLE=False,SEED=42,BATCH=16,SMOKE=False,RESUME=False,RUN_TAG='n640-default-seed42-01' (kiểm tên chưa tồn tại),chạy baseline100epochs/patience20. Cloud notebook có ô audit smoke mới sau ô train; ô validation/full và test phía sau chưa chạy. Không Run all vì khối validation smoke cố ý chặn. Không yêu cầu duyệt dataset/train lần nữa.

## Human actions pending

Không còn chờ đăng nhập hoặc mount cho phiên hiện tại. Không có yêu cầu người dùng mới để hoàn tất A11. Nếu runtime bị thu hồi thì xác minh mount/identity/checkpoint trước tiếp tục; quyền không tự đồng nghĩa compute units trả phí đã được xác minh.

## Kiểm tra

Windows/PowerShell/Python3.11.9 ../.venv-yolo/Scripts/python.exe: repository checker PASS49sources;15 kept/training tests PASS12.586s tại source5e5e29d + legacy working-tree changes. Colab GPU runtime là môi trường riêng nêu trên. Real summary đọc lại từ Drive PASS. Không gán các kết quả working tree cho pristine HEAD; giữ mọi legacy modifications ngoài commit.

## Xuất bản mã

Người dùng chỉ định repo truongthinh994/AI-book-sorting; origin cũ giữ nguyên. DraftPR https://github.com/truongthinh994/AI-book-sorting/pull/1, không merge. GitHubZIP chỉ có mã/tài liệu, không chứa ảnh/weights/reviewHTML. Source branch giữ lịch sử gốc, local ref publish/ai-book-three-kept giữ lịch sử repo đích.

Trước push: xác minh delivery:feat/three-kept-rebuild khớp ref publish. Commit source đúng allowlist; commit-tree từ sourceHEAD tree,parent publish, update-ref có kiểm parent rồi normalpush publish sang delivery:feat/three-kept-rebuild. Không push trực tiếp sourceHEAD khác lịch sử, không force. Giữ mọi modified/untracked legacy có sẵn; không stage chúng. CI/deliverySHA cuối ghi localpublicationreport và bàn giao.
