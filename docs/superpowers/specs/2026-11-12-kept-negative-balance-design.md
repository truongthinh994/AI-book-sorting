# Cân bằng mẫu âm khi chọn split kept

Phạm vi đã được người dùng duyệt trong kế hoạch: chia theo nhóm, seed42–73, chọn bằng phân bố lớp/mẫu âm và tỷ lệ ảnh; không dùng model để chọn. Không thêm bước duyệt thiết kế. Gate duyệt cuối vẫn dành cho proposal dữ liệu cụ thể.

## Vấn đề và lựa chọn

`kept.propose` loại nhóm chưa duyệt, giữ nguyên nhóm, yêu cầu đủ3 lớp, rồi chọn theo sai lệch tỷ lệ hộp và ảnh. Mẫu âm chỉ xuất hiện trong báo cáo/cảnh báo nên không tác động tới lựa chọn. r07 lần đầu có93 mẫu âm nhưng chia71/8/14.

Giữ cách chọn cũ sẽ tiếp tục bỏ qua mẫu âm. Ép một quota cứng có thể không khả thi khi cả cuốn phải cùng tập. Chọn bổ sung sai lệch tỷ lệ mẫu âm vào tổng sai lệch lớp; đây là cùng kiểu chuẩn hóa đang dùng, không phá nhóm và không đặt quota mới.

## Thiết kế đã nằm trong kế hoạch được duyệt

Giữ nguyên3200 ứng viên (32seed ×100attempt), thứ tự ưu tiên: nguyên nhóm và đủ3 lớp là điều kiện; sau đó tối thiểu tổng sai lệch của ba lớp cộng mẫu âm, rồi sai lệch tỷ lệ ảnh, cuối cùng seed/attempt. Nếu không có mẫu âm, thành phần âm bằng0. Không thay mapping/nhãn/pixel hay train config. Ghi tên thuật toán trong proposal để truy nguồn thay đổi; proposal cũ giữ nguyên, tạo proposal mới. Dữ liệu đã khóa vẫn đọc qua validator hiện hành; proposal cũ phải được tạo lại trước khi khóa bằng thuật toán mới.

## Kiểm chứng

Fixture48 nhóm: mục tiêu12 ảnh âm là8/2/2 sau làm tròn. Bộ chọn cũ cho8/3/1 dù có phương án cân bằng. Regression kiểm ảnh âm cùng với lớp, nhóm và tính tái lập. Chạy lại14 tests công cụ, kiểm toàn repo và audit r07; chạy cùng dữ liệu hai lần phải cùng proposalSHA. Trình bày số nhóm, lớp, ảnh âm và mức chắc chắn của nhóm; chưa duyệt thì không khóa hay train.
