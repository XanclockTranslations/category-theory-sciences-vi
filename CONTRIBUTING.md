# Đóng góp / Contributing

## Tiếng Việt

Đây là bản dịch máy không chính thức. Đóng góp hữu ích nhất là sửa sai về nội dung
toán học, thuật ngữ, tiếng Việt và trình bày.

Gửi báo lỗi và góp ý tại [Issues của dự án XanclockTranslations](https://github.com/XanclockTranslations/category-theory-sciences-vi/issues).

- Khi báo lỗi, ghi chương, mục, số định nghĩa/bài tập/công thức nếu có, trang in
  trong bản gốc và bản dịch, cùng trích đoạn hoặc mô tả đủ để xác định vị trí.
  Nêu cách sửa đề xuất và lý do.
- Giữ các mốc `% Source: ...`, số hiệu, nhãn LaTeX và ý nghĩa toán học. Khi sửa
  sơ đồ, giữ các đối tượng, cấu xạ, hướng mũi tên và quan hệ giao hoán của bản gốc.
- Theo [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) và bảng thuật ngữ chung;
  giữ các thuật ngữ mượn đã thống nhất. Đề xuất đổi thuật ngữ cần nêu các vị trí
  liên quan để có thể sửa nhất quán.
- Phân biệt chú thích của tác giả với chú thích người dịch mang ký hiệu D1, D2,
  v.v. Nếu sửa lỗi trong bản gốc, ghi rõ biểu thức gốc và lý do sửa trong chú thích.
- Lưu tệp văn bản bằng UTF-8, dùng kết thúc dòng LF theo `.gitattributes`.
  Để Git dùng cấu hình của kho; nếu cấu hình toàn cục gây chuyển đổi ngoài ý muốn,
  dùng `git config --local core.autocrlf false`. Không đưa font, bộ biên dịch,
  cache, tệp tạm hoặc nhật ký dựng vào commit.
- Sau khi đổi TeX, dựng lại theo [docs/BUILD.md](docs/BUILD.md), kiểm tra các trang
  bị ảnh hưởng, tham chiếu, liên kết và chỉ mục. Nếu số trang thay đổi, kiểm tra
  lại các trang kế tiếp và các đích chỉ mục liên quan. Ghi rõ phần đã kiểm tra;
  chỉ gọi bản PDF mới là đã kiểm chứng sau khi hoàn tất các kiểm tra đó.

Giữ ghi công và thông báo quyền của sách gốc và các tài nguyên bên thứ ba.
Xem [license.md](license.md) về giấy phép hiện hành của dự án.

## English

This is an unofficial machine translation. Corrections to mathematical content,
terminology, Vietnamese wording, and layout are especially useful.

Report problems and suggest corrections in [the XanclockTranslations project issues](https://github.com/XanclockTranslations/category-theory-sciences-vi/issues).

- Report the chapter, section, definition/exercise/equation number where
  available, and the printed pages in both the original and the translation.
  Include enough text or description to locate the issue, a proposed correction,
  and its reason.
- Preserve `% Source: ...` markers, numbering, LaTeX labels, and mathematical
  meaning. Diagram changes must preserve the original objects, morphisms,
  arrow directions, and commutativity relations.
- Follow [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) and its shared glossary,
  including established borrowed terms. A terminology change should identify
  related occurrences so that it can be applied consistently.
- Keep author footnotes distinct from translator notes marked D1, D2, etc.
  A correction to the source book should record the original expression and
  explain the correction in a translator note.
- Save text as UTF-8 with LF line endings, as specified by `.gitattributes`.
  Let Git follow repository settings; if global settings cause unwanted
  conversion, use `git config --local core.autocrlf false`. Keep font files,
  compiler binaries, caches, temporary files, and build logs out of commits.
- After TeX changes, rebuild using [docs/BUILD.md](docs/BUILD.md) and inspect the
  affected pages, references, links, and index. Pagination changes also require
  checking later pages and related index destinations. State what was checked;
  describe a new PDF as verified only after completing those checks.

Preserve the original book's attribution and rights notices, including
third-party credits. See [license.md](license.md) for the project's existing
license.
