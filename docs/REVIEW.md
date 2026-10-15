# Hồ sơ kiểm tra / Review record

## Bản PDF được ghi nhận / Recorded reading copy

- Bản dịch máy không chính thức, hoàn chỉnh về phạm vi: 463 trang.
- AI: GPT-6.1 Sol (Ultra); prompting: Bế Trọng Nghĩa (@ichxorya).
- SHA-256: `f6d1280e9c18c2067a336d9d3109b55086ced8978f7bfa5aa51883e7c8d3d4c8`.
- Nguồn: ấn bản MIT Press 2014, 495 trang; mã băm trong `source/manifest.json`.
- Hồ sơ máy đọc được: [review/final-qa.json](../review/final-qa.json).

Nội dung đã được đối chiếu với bản PDF nguồn; bảy chương đã qua các lượt kiểm tra
nội dung và trình bày bằng các tác nhân độc lập. Sơ đồ, bảng và hình ảnh có kiểm
tra chi tiết. Đây là quy trình có sử dụng AI, không phải chứng nhận hiệu đính
toán học của con người. Trạng thái `publication_ready` vẫn là `false`.

The supplied PDF was the authority for source comparisons. Each of the seven
chapters received independent agent reviews of content and presentation, with
detailed checks of diagrams, tables and images. These AI-assisted checks do
not constitute human mathematical proofreading. This remains an unofficial
machine-translation draft; `publication_ready` is `false`.

## Kết quả kỹ thuật / Technical results

| Kiểm tra / Check | Kết quả / Result |
| --- | --- |
| Mốc trang nguồn trong bảy chương / Chapter source-page markers | 474 |
| Mục từ chỉ mục / Index entries | 566 |
| Đích dẫn trang chỉ mục / Index destinations | 605 |
| Liên kết nội bộ giải quyết được / Resolved internal links | 946 |
| Font nhúng / Embedded fonts | 33, tất cả / all embedded |
| Ảnh thiên văn giữ nguyên / Unchanged original astronomy images | 4 |
| Thiếu ký tự, tràn dòng, tham chiếu chưa giải quyết / Missing glyphs, overflow, unresolved refs | 0 |

Nhật ký lần dựng đã kiểm tra có bốn cảnh báo diễn giải màu CMYK của ảnh gốc;
ảnh đã được đối chiếu trực quan. Lịch sử đầy đủ gồm ảnh trang, nhật ký, các lượt
sửa và biên bản được giữ trong kho lưu trữ cục bộ, ngoài kho Git công khai.
The reviewed build had four accepted CMYK interpretation warnings for original
images, whose colors were visually checked. Full local evidence, render images,
logs and historical reports are preserved outside the public repository.

## Bìa và chuẩn bị kho / Cover and repository preparation

Bìa giữ nguyên khối pixel của ảnh gốc, thêm chữ vector tìm kiếm được. Bản cập
nhật bìa đã được xem lại ở cả năm trang thay đổi: 1, 2, 5, 17 và 249. Các trang
17 và 249 chỉ dịch nội dung lên 1.82519 pt, không đổi văn bản, kiểu chữ, xuống
dòng hay số trang. 458 trang còn lại giống hoàn toàn về pixel với bản đã kiểm
tra trước đó. Văn bản các chương, tài liệu tham khảo, chỉ mục và toàn bộ đích
chỉ mục được giữ nguyên.

The original cover pixels are preserved with editable searchable vector text.
All five changed pages were inspected. Pages 17 and 249 had only a 1.82519 pt
upward shift, preserving text, typography, wrapping and folios; the other 458
pages were exact full-RGB matches to the previously reviewed copy. Chapter,
reference and index text and all index targets were unchanged.

Khi chuẩn bị GitHub, chỉ chuẩn hóa xuống dòng thành LF, làm sạch siêu dữ liệu
đường dẫn, bổ sung tài liệu và cải thiện tính di động của công cụ. Nội dung TeX
sau chuẩn hóa xuống dòng được đối chiếu với bản trước; tệp PDF và tài sản nhị
phân được giữ nguyên. Mã băm đầu vào hiện tại và bằng chứng chuyển tiếp được ghi
trong hồ sơ QA, không gán lại các lượt kiểm tra cũ thành một lượt mới.

GitHub preparation normalized line endings, removed machine-specific metadata,
added documentation, and made tool discovery portable. Logical book-source
content was compared with the preserved snapshot; the PDF and binary book
assets were unchanged. Current input hashes and this preparation's provenance
are recorded in the QA snapshot without claiming a new full visual review.
