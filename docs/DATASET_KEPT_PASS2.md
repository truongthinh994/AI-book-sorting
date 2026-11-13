# Kept — rà nhãn và nhóm lượt2

Ngày2026-11-12. Tiếp tục A09/D29, không dùng nhóm/approval/sửa nhãn từ chiến dịch cũ. Nguồn ZIP và các bản trước giữ nguyên. [Quy trình](THREE_KEPT_CAMPAIGN.md).

## Đã thực hiện

- Mở sheet004–015 ở kích thước gốc,8 ảnh640/sheet:96 ảnh mới #25–120. Cộng lượt trước120/620 ảnh, còn500. Mở riêng20 ảnh #24,#31,#36,#39,#47,#50,#51,#66,#69,#70,#72,#89,#91,#93,#98,#105,#107,#114,#117,#119 để kiểm các mã nhỏ/cắt/xiên. Việc đã mở ảnh không đồng nghĩa mọi bbox đã được duyệt.
- #24: hai mã vuông trên bìa gập là QR/2D. Nghi vấn Barcode thiếu ở checkpoint trước đã được kiểm lại; không thêm QR vào Barcode.
- Sửa19 ảnh, thêm20 hộp Barcode:18 ảnh thêm1 hộp, #105 thêm2 hộp (thư viện và nhà xuất bản). #36 chỉ gán phần vạch nhìn thấy bị cắt ở cạnh phải, không vẽ đoán ngoài ảnh. Ảnh khác vẫn giữ hộp nguồn trong hàng chờ, không tự sửa lớp lỗi theo suy đoán.
- 14 đề xuất nhóm cho33 ảnh đã đối chiếu cùng tiêu đề/thiết kế hoặc ID thư viện. Đó là nhóm liên kết cục bộ, chưa chứng minh độc lập với toàn bộ500 ảnh chưa mở. CSV có group_id và lý do, label_review vẫn pending/rejected; không kế thừa group_id cũ.
- Cách ly8 ảnh có nhãn nghi vấn: #1 bbox Ripped quá lớn; #42 Barcode xiên/mờ; #52 Notch/Ripped khó phân biệt; #61 Ripped chồng hình in; #62 mã trên mặt sau quá mờ; #103 vết bẩn hay rách; #106 sờn/in hay rách; #110 trang trong thay vì mặt bìa. Với #42/#110, mẫu âm cũng rejected.

## Bản mới và kiểm chứng

`data/local/campaign-v4-three-kept-2026-11-12-r03`, version `three-kept-718b59c52ce639f24518`.

| Chỉ số | Giá trị |
|---|---:|
| Ảnh | 620 |
| Barcode | 215 |
| Ripped | 411 |
| Wornout | 1339 |
| Tổng hộp | 1965 |
| Nhãn rỗng | 59 |
| Ứng viên âm | 100 |
| Nhãn pending / rejected / approved | 612 / 8 / 0 |
| Âm pending / rejected / approved | 98 / 2 / 0 |
| Đề xuất nhóm / ảnh có group_id | 14 / 33 |

Audit r03 phát lại nguồn sáu lớp→mapping bỏ Notch/Spot/Tag→ba sửa ở r02→19 sửa lượt2 PASS. Audit bản đầu/r02/r03 và hash ZIP gốc Downloads vẫn khớp. Pixel không thay đổi; không có split/training/approval người dùng. Patch, lý do, pixel bbox và nhật ký từng ảnh giữ ngoài Git trong reports.

Các nhóm đã đối chiếu: Metaverse(#9/41/60), Paris wealth(#38/39/64), Spain Digest11(#46/58/71), tropical fish(#6/82), Education Theory(#8/49/81), bìa xanh EM0934902(#15/93), History10(#16/108), pink Meet Again(#20/37), Baduk/AI(#45/84), họ bìa nghi lễ Hanja(#48/77), circuit back(#72/107), KIPF xám2007.12(#74/92), KIPF vàng07-09(#13/14), Third Humanity4(#1/5/111). Nhóm họ thiết kế giữ cùng tập kể cả biến thể tập sách; cần liên kết các mặt còn lại trước chia tập.

## File cục bộ để tiếp tục

- r03 `reports/review.html`:620 ảnh/bbox, nhóm được xếp cạnh nhau; launcher `scripts/windows/ReviewThreeKept.cmd` mở r03.
- r03 `reports/observations-pass2.json`:96 nhận xét mới; `group-proposals-pass2.json`:14 nhóm và bằng chứng; `review-progress.json`:danh sách120 ảnh đã mở,500 còn lại.
- r03 `reports/patches-02.json`, `validation-pass2.json`, `immutable-audit-pass2.json`:19 patch và bằng chứng replay/inventory/hash. Sheet ở bản đầu `reports/native-review`; chúng mô tả nhãn bản đầu, không phải nhãn sau sửa.
- r03 `training/three_kept_colab.ipynb`:bản sao notebook giữ EXPECTED=None. Bbox Barcode không chứng minh đã giải mã được mã.

Tiếp tục từ #121/sheet016; ưu tiên #59/#63 có mã bị cắt cần mở riêng, #42/#62 mờ không được vẽ đoán, và tám ảnh nhãn rejected. Chưa đủ điều kiện tạo proposal split; chưa hỏi duyệt cuối hoặc chạy GPU.
