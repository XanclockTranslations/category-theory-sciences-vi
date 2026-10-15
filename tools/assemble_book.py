"""Assemble translated chapters with accurate coverage and review notices."""
from pathlib import Path
import argparse
import json
import re
from index_anchor_io import apply_anchors

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--chapters", type=int, nargs="*")
parser.add_argument("--index-labels", action="store_true", help="Include reviewed entry-specific index anchors")
parser.add_argument("--include-index", action="store_true", help="Include complete translated index; requires all seven chapters and all anchors")
parser.add_argument("--complete-draft", action="store_true", help="Use the complete-translation notice after independent content reviews pass")
args = parser.parse_args()
progress = json.loads((ROOT / "translation/progress.json").read_text(encoding="utf-8"))
chapters = args.chapters if args.chapters is not None else [c["chapter"] for c in progress["chapters"] if c["status"].startswith("draft_complete")]
if args.include_index and chapters != list(range(1,8)):
    raise ValueError("Complete index requires all seven chapters in order")
if args.complete_draft:
    if not args.include_index or chapters != list(range(1,8)):
        raise ValueError("Complete draft requires all seven chapters and the complete index")
    if any(c['status'] != 'draft_complete_independently_reviewed' for c in progress['chapters']):
        raise ValueError("Complete draft requires independent fidelity review of every chapter")
    if any(progress[k] != 'draft_complete_independently_reviewed' for k in ('frontmatter','references')):
        raise ValueError("Complete draft requires reviewed opening material and references")

def expand_parts(path, stack=()):
    path = path.resolve()
    if path in stack or not path.is_relative_to(ROOT):
        raise ValueError(f"Invalid or recursive source include: {path}")
    text = path.read_text(encoding="utf-8")
    def replace(match):
        name = match.group(1)
        if not Path(name).suffix:
            name += ".tex"
        candidates = [path.parent / name, ROOT / name, ROOT / "output" / name]
        for candidate in candidates:
            if candidate.exists():
                return expand_parts(candidate, stack + (path,))
        raise FileNotFoundError(f"Include {name} from {path}")
    return re.sub(r"\\(?:input|include)\{([^}]+)\}", replace, text)

def normalize_translator_notes(text):
    """Use distinct D marks while keeping the original numeric footnote counter."""
    names = ('ctIIInote', 'ctfournote', 'ctfivenote', 'ctVInote', 'ctsevennote')
    for name in names:
        pattern = rf'^\\(?:providecommand|newcommand)\{{\\{name}\}}\[1\].*$'
        replacement = rf'\providecommand{{\{name}}}[1]{{\translatornote{{#1}}}}'
        text = re.sub(pattern, lambda match: replacement, text, flags=re.M)
    old_start = r'\begingroup\renewcommand{\thefootnote}{*}\footnote[0]{Chú thích của người dịch: '
    old_end = r'}\endgroup'
    if old_start in text:
        start = text.index(old_start)
        end = text.index(old_end, start + len(old_start))
        body = text[start + len(old_start):end]
        text = text[:start] + r'\translatornote{' + body + '}' + text[end + len(old_end):]
    return text
preamble = r"""\documentclass[11pt,oneside]{book}
\usepackage{fontspec}
\setmainfont{times.ttf}[Path=./fonts/,BoldFont=timesbd.ttf,ItalicFont=timesi.ttf,BoldItalicFont=timesbi.ttf]
\setsansfont{arial.ttf}[Path=./fonts/,BoldFont=arialbd.ttf,ItalicFont=ariali.ttf,BoldItalicFont=arialbi.ttf]
\setmonofont{consola.ttf}[Path=./fonts/,BoldFont=consolab.ttf,ItalicFont=consolai.ttf,BoldItalicFont=consolaz.ttf]
\usepackage[b5paper,margin=22mm]{geometry}
\usepackage{amsmath,amssymb,amsthm,array,longtable,booktabs,graphicx}
\usepackage{tikz,tikz-cd}
\usetikzlibrary{arrows.meta,positioning,calc,matrix,fit,decorations.pathreplacing}
\usepackage{enumitem}
\usepackage[unicode,hidelinks,hypertexnames=false]{hyperref}
\usepackage{xurl}
\setlength{\parskip}{3pt}
\setlength{\parindent}{1.2em}
\renewcommand{\chaptername}{Chương}
\renewcommand{\contentsname}{Mục lục}
\renewcommand{\figurename}{Hình}
\renewcommand{\tablename}{Bảng}
\renewcommand{\proofname}{Chứng minh}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}
\newcommand{\Set}{\mathbf{Set}}
\newcommand{\Cat}{\mathbf{Cat}}
\newcommand{\Sch}{\mathbf{Sch}}
\newcommand{\id}{\mathrm{id}}
\newcommand{\Hom}{\operatorname{Hom}}
\newcommand{\Ob}{\operatorname{Ob}}
\newcommand{\Mor}{\operatorname{Mor}}
\newcommand{\sourcepage}[1]{\label{srcp:#1}}
\newcounter{translatornote}[chapter]
\newcommand{\translatornote}[1]{\begingroup\stepcounter{translatornote}\renewcommand{\thefootnote}{D\arabic{translatornote}}\footnote[0]{Chú thích của người dịch: #1}\endgroup}
% Index marks use page labels directly, avoiding AMS's one-label-per-equation rule.
\makeatletter
% Use the standard heading hook so a following list keeps its first item.
\newcommand{\keepwithnext}{\par\nobreak\@afterheading}
\newcommand{\indexanchor}[1]{\ifmeasuring@\else
  \hypertarget{#1}{}\protected@write\@auxout{}{\string\newlabel{#1}{{}{\thepage}{}{#1}{}}}%
\fi}
\makeatother
\begin{document}
\frontmatter
\hypersetup{pageanchor=false}
% EDITABLE_COVER
\hypersetup{pageanchor=true}
"""
preamble = preamble.replace('% EDITABLE_COVER', expand_parts(ROOT / 'translation/frontmatter/cover.tex'))
parts = [preamble]
opening = ROOT / "translation/frontmatter/opening.tex"
if opening.exists():
    parts.append(opening.read_text(encoding="utf-8"))
parts.append("\n\\chapter*{Về bản chuyển ngữ này}\n" if args.complete_draft else "\n\\chapter*{Tình trạng bản thảo}\n")
if args.complete_draft:
    parts.append("Bản thảo này chuyển ngữ toàn bộ ấn bản MIT Press năm 2014 được cung cấp: phần mở đầu, bảy chương, các bài tập và lời giải có trong nguồn, sơ đồ, bảng, tài liệu tham khảo và chỉ mục. Nội dung đã được đối chiếu với ấn bản ấy. Đây là bản dịch máy tiếng Việt không chính thức.\n")
    parts.append("Những lỗi đánh máy hoặc ký hiệu có thể xác định rõ trong nguồn được giải thích tại chỗ khi sửa. Những phát biểu cần làm rõ được giữ lại cùng chú thích của người dịch. Chỉ mục giữ thứ tự mục từ tiếng Anh, chuyển ngữ các mục từ và dẫn đến số trang của bản tiếng Việt.\n")
else:
    parts.append("Phạm vi của dự án là toàn bộ sách gốc gồm bảy chương, phần mở đầu, các bài tập và lời giải, sơ đồ, bảng, tài liệu tham khảo và chỉ mục. ")
    parts.append("Bản thảo hiện tại chỉ chứa các phần đã được biên soạn; chưa phải bản dịch hoàn chỉnh.\n")
    parts.append("Các chương có trong bản đọc này: " + (", ".join(str(n) for n in chapters) if chapters else "chưa có") + ".\n")
parts.append("Các chú thích mang dấu D1, D2, v.v. do bản dịch bổ sung; các chú thích mang số thông thường tương ứng với chú thích của bản gốc. Chú thích D được đánh số lại từ D1 ở mỗi chương và ở chỉ mục.\n")
parts.append("\n\\tableofcontents\n\\mainmatter\n")
for n in chapters:
    path = ROOT / f"translation/chapters/chapter-{n:02d}.tex"
    if not path.exists():
        raise FileNotFoundError(path)
    parts.append(f"\n\\setcounter{{chapter}}{{{n-1}}}\n")
    content = normalize_translator_notes(expand_parts(path))
    if args.index_labels or args.include_index:
        content = apply_anchors(content, n, require_complete=args.include_index)
    parts.append(content)
if (ROOT / "translation/references.tex").exists():
    parts.append("\n\\backmatter\n")
    parts.append((ROOT / "translation/references.tex").read_text(encoding="utf-8"))
if args.include_index:
    index_path = ROOT / "translation/index.tex"
    if not index_path.exists():
        raise FileNotFoundError(index_path)
    parts.append(index_path.read_text(encoding="utf-8"))
parts.append("\n\\end{document}\n")
output = ROOT / "output/book-draft.tex"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(parts), encoding="utf-8", newline="\n")
(ROOT / "output/assembly.json").write_text(json.dumps({"included_chapters": chapters, "complete_draft": args.complete_draft, "full_book_complete": progress['full_book_complete'] if args.complete_draft else False, "source_sha256": progress["source_sha256"]}, indent=2)+'\n', encoding="utf-8", newline="\n")
print(str(output))
