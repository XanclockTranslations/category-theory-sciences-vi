# Dựng sách / Build

## Công cụ và font / Tools and fonts

Cần Python 3.12 trở lên và Tectonic. Từ thư mục gốc, cài thư viện Python:
Use Python 3.12 or newer and Tectonic; install dependencies from the project root:

```sh
python -m pip install -r requirements.txt
```

Đặt `tectonic` trong `PATH`, truyền `--tectonic`, hoặc đặt biến
`CT_SCIENCES_TECTONIC`. Bản cục bộ trong `tools/vendor/tectonic/` cũng dùng được.
Tectonic có thể tải gói TeX tiêu chuẩn ở lần dựng đầu.
Put Tectonic on `PATH`, pass `--tectonic`, set `CT_SCIENCES_TECTONIC`, or use the
ignored local `tools/vendor/tectonic/` installation. The first build may fetch
the standard TeX bundle.

Để giữ kiểu chữ đã kiểm tra, cung cấp cùng 12 tệp font cục bộ:
Supply the same twelve local font files to preserve the recorded typography:

```text
times.ttf     timesbd.ttf   timesi.ttf    timesbi.ttf
arial.ttf     arialbd.ttf   ariali.ttf    arialbi.ttf
consola.ttf   consolab.ttf  consolai.ttf  consolaz.ttf
```

Windows: công cụ tìm font trong `output/fonts/` và thư mục font Windows.
macOS/Linux: cung cấp font trong `output/fonts/`, dùng `--font-dir`, hoặc đặt
`CT_SCIENCES_FONT_DIR`. Đặt đường dẫn có dấu cách trong dấu nháy. Font không
được phân phối trong kho; sử dụng theo quyền của bản cài cục bộ của bạn.
Thay bộ font sẽ cần kiểm tra lại phân trang.
On Windows, fonts can come from `output/fonts/` or the system font directory.
On macOS/Linux, supply the same files in `output/fonts/`, use `--font-dir`, or
set `CT_SCIENCES_FONT_DIR`. Quote paths containing spaces. Fonts are not
distributed; use them under your local installation's terms. Changing fonts
requires a fresh pagination review.

PowerShell: `$env:CT_SCIENCES_FONT_DIR = 'D:\My Fonts'`

macOS/Linux: `export CT_SCIENCES_FONT_DIR='/path/to/local/fonts'`

Kiểm tra mà chưa dựng PDF / Check dependencies without building a PDF:

```sh
python tools/build_pdf.py --check
```

## PDF và chỉ mục / PDF and index

Chạy từ thư mục gốc theo thứ tự / Run in order from the project root:

```sh
python tools/generate_index.py
python tools/assemble_book.py --chapters 1 2 3 4 5 6 7 --include-index --complete-draft
python tools/build_pdf.py
python tools/generate_index.py --aux output/pdf/book-draft.aux
python tools/assemble_book.py --chapters 1 2 3 4 5 6 7 --include-index --complete-draft
python tools/build_pdf.py
```

PDF: `output/pdf/category-theory-sciences-vi-machine.pdf`. Lượt dựng sau gộp
các dẫn chiếu chỉ mục trùng trang. Khi phân trang thay đổi, lặp ba lệnh cuối
đến khi đích chỉ mục ổn định. Đóng trình xem PDF nếu Windows khóa tệp.
The second build coalesces index referrals resolving to the same page. After
pagination changes, repeat the last three commands until targets are stable.
Close the PDF viewer before rebuilding if Windows has locked the file.

## Bìa, kiểm tra và gói nguồn / Cover, checks and source package

Chữ vector nằm trong `translation/frontmatter/cover.tex`. Tạo lại nền B5 từ
PNG gốc đã lưu / The vector lettering is in the cover TeX; regenerate the
background from the stored original PNG:

```sh
python tools/prepare_cover.py
```

Để xuất ảnh trang, cài Poppler và đặt `pdftoppm` trong `PATH`, hoặc truyền
`--poppler` / Install Poppler on `PATH`, or pass its executable with `--poppler`:

```sh
python tools/render_review.py --pdf output/pdf/category-theory-sciences-vi-machine.pdf --output tmp/pdfs/review --report review/render-current.json
python tools/audit_book.py
python tools/verify_repository.py
```

Kiểm tra kỹ thuật không thay thế đọc đối chiếu và xem từng trang thay đổi.
Nếu chưa dựng trên máy hiện tại, `audit_book.py` ghi rõ không có nhật ký TeX;
có thể dùng `--log` để chọn nhật ký. `review/final-qa.json` ghi nhận bản PDF
đã kiểm tra trong kho. Khi đổi nội dung hoặc PDF, cập nhật hồ sơ sau kiểm tra.
Technical checks do not replace source comparison and visual inspection.
Without a local build log, the audit explicitly reports unavailable TeX
diagnostics; use `--log` to select a log. Update the QA snapshot after reviewing
changed content or a new PDF.

Đóng gói nguồn khớp với hồ sơ QA / Package sources matching the QA snapshot:

```sh
python tools/package_sources.py
```

ZIP nằm trong `output/`, được Git bỏ qua và có thể dùng làm tài sản GitHub
Release. Font, runtime và lịch sử kiểm tra cục bộ không nằm trong gói.
The ignored ZIP under `output/` can be attached to a GitHub Release. Fonts,
runtimes and private inspection history are excluded.

## Git và xuống dòng / Git and line endings

Văn bản dùng UTF-8/LF trên Windows, macOS và Linux. `.gitattributes` quy định
cách xuống dòng; `.editorconfig` hướng dẫn trình soạn thảo. Cấu hình sau chỉ
áp dụng cho kho hiện tại / These settings affect only this repository:

```sh
git config --local core.autocrlf false
git config --local core.safecrlf true
python tools/verify_repository.py
git add .
git diff --cached --check
git diff --cached --stat
```

Kho GitHub của dự án / Project repository:
[XanclockTranslations/category-theory-sciences-vi](https://github.com/XanclockTranslations/category-theory-sciences-vi).
Dùng URL `https://github.com/XanclockTranslations/category-theory-sciences-vi.git`
khi thêm remote / Use this URL when adding the Git remote.

Mô tả kho GitHub / GitHub repository description:

> [Machine Translated, Not Reviewed] Vietnamese translation of David I. Spivak's Category Theory for the Sciences.

Không đưa font, token hoặc cấu hình riêng vào commit / Keep local fonts and
credentials outside commits.
