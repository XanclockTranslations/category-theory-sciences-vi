# Lý thuyết phạm trù cho các ngành khoa học

[English](README_EN.md)

**[Machine Translated, Not Reviewed]**

Bản dịch máy này chưa được con người hiệu đính. Các lượt kiểm tra bằng AI và
kiểm tra kỹ thuật được ghi nhận riêng trong [hồ sơ kiểm tra](docs/REVIEW.md).

Dự án thuộc [XanclockTranslations](https://github.com/XanclockTranslations):
[kho mã nguồn](https://github.com/XanclockTranslations/category-theory-sciences-vi) ·
[báo lỗi hoặc góp ý](https://github.com/XanclockTranslations/category-theory-sciences-vi/issues).

<img src="docs/images/cover.png" width="300" alt="Bìa bản dịch máy tiếng Việt của Category Theory for the Sciences">

Bản dịch máy tiếng Việt không chính thức của *Category Theory for the Sciences*,
David I. Spivak, The MIT Press, 2014.
[Thông tin sách gốc](https://mitpress.mit.edu/9780262028134/category-theory-for-the-sciences/).

AI được sử dụng: **GPT-6.1 Sol (Ultra)**.
Người thực hiện prompting: **Bế Trọng Nghĩa (@ichxorya)**.

**[Đọc bản PDF tiếng Việt, 463 trang](output/pdf/category-theory-sciences-vi-machine.pdf).**

Bản thảo bao gồm phần mở đầu, bảy chương, bài tập và lời giải có trong nguồn,
sơ đồ, bảng, tài liệu tham khảo và chỉ mục. Chỉ mục có 566 mục từ và 605 đích
dẫn trang. Các lượt đối chiếu được ghi nhận trong [hồ sơ kiểm tra](docs/REVIEW.md).
Bản dịch vẫn cần người có chuyên môn hiệu đính; hoàn thành phạm vi dịch không
đồng nghĩa với một ấn bản đã được thẩm định.

## Nguồn chỉnh sửa

| Đường dẫn | Nội dung |
| --- | --- |
| [translation/](translation/) | Văn bản LaTeX, dữ liệu chỉ mục và tài sản hình ảnh |
| [source/original.pdf](source/original.pdf) | Bản PDF gốc được giữ nguyên |
| [source/manifest.json](source/manifest.json) | Xuất xứ, mã băm và ánh xạ trang |
| [tools/](tools/) | Công cụ dựng, kiểm tra, xử lý bìa và đóng gói |
| [docs/](docs/) | Hướng dẫn dựng, hồ sơ kiểm tra và quyền sử dụng |
| [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) | Quy ước dịch và thuật ngữ chung |

Sơ đồ TikZ và lớp chữ vector trên bìa có thể chỉnh sửa. Bìa giữ hình gốc,
thêm nhãn “Bản dịch máy tiếng Việt” và nhan đề tiếng Việt. Các ảnh thiên văn
giữ ghi công từ nguồn; thông tin tài sản nằm trong `translation/assets/`.

## Dựng sách

Cần Python 3.12 trở lên, các thư viện trong [requirements.txt](requirements.txt),
Tectonic và bộ font Times New Roman, Arial, Consolas từ máy của bạn.
Poppler là công cụ tùy chọn để xuất ảnh trang phục vụ kiểm tra.

Xem [hướng dẫn dựng trên Windows, macOS và Linux](docs/BUILD.md) để cài thư viện,
cấu hình font và cập nhật chỉ mục. Văn bản dùng UTF-8 và LF; `.gitattributes`
giữ cách xuống dòng thống nhất giữa các hệ điều hành. Font, bộ biên dịch, cache,
nhật ký, ảnh kiểm tra và ZIP được Git bỏ qua.

Báo lỗi hoặc đề xuất sửa theo [hướng dẫn đóng góp](CONTRIBUTING.md).

## Ghi công và giấy phép

Sách gốc: David I. Spivak, *Category Theory for the Sciences*, The MIT Press,
2014. Bản quyền bản gốc: © 2014 Massachusetts Institute of Technology.

Bản dịch chia sẻ theo **CC BY-NC-SA 4.0**, theo giấy phép truy cập mở mà
[MIT Press công bố cho sách gốc](https://mitpress.mit.edu/9780262028134/category-theory-for-the-sciences/).
Cần ghi công, nêu các thay đổi, sử dụng phi thương mại và chia sẻ bản chuyển thể
theo điều kiện tương ứng của [giấy phép](https://creativecommons.org/licenses/by-nc-sa/4.0/).

Xem [license.md](license.md), [toàn văn giấy phép](LICENSE) và
[hồ sơ nguồn, quyền sử dụng](docs/SOURCE_AND_RIGHTS.md).
Thông báo quyền và ghi công của bên thứ ba được giữ lại. Tác giả và nhà xuất bản
không bảo trợ hay phê duyệt bản dịch. Giấy phép hiện hành không cấp quyền phát
hành thương mại.
