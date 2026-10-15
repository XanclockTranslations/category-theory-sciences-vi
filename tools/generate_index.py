"""Generate the translated index only when every entry-specific anchor is present."""
from pathlib import Path
import argparse
import json
import re
from index_anchor_io import ROOT, chapter_source, apply_anchors, expected_targets, anchor_path

parser = argparse.ArgumentParser()
parser.add_argument('--aux', type=Path, help='Final build aux file; coalesce referrals resolving to the same Vietnamese page')
args = parser.parse_args()
inventory = json.loads((ROOT / 'translation/index-inventory.json').read_text(encoding='utf-8'))
for chapter in range(1,8):
    apply_anchors(chapter_source(chapter),chapter,require_complete=True)

def escape(value):
    return ''.join({'&':r'\&','%':r'\%','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in value)

resolved = {}
if args.aux:
    aux = args.aux.read_text(encoding='utf-8')
    resolved = {label:page for label,page in re.findall(r'\\newlabel\{(idx\d+:\d+)\}\{\{\}\{([^}]+)\}',aux)}
    expected = {t['label'] for e in inventory['entries'] for t in e['targets']}
    if set(resolved) != expected:
        raise ValueError(f'Index aux coverage mismatch; missing={sorted(expected-set(resolved))}, unexpected={sorted(set(resolved)-expected)}')

parts = [r'''\chapter*{Chỉ mục}
\addcontentsline{toc}{chapter}{Chỉ mục}
\markboth{Chỉ mục}{Chỉ mục}
\setcounter{translatornote}{0}
Chỉ mục giữ thứ tự các mục từ của bản gốc tiếng Anh. Các mục từ được chuyển ngữ, kèm nguyên ngữ khi hữu ích để tra cứu song song. Số trang dẫn đến các đoạn tương ứng trong bản dịch. Những dẫn chiếu cũ không khớp với nội dung của ấn bản được cung cấp đã được điều chỉnh theo vị trí thực tế của khái niệm.
\medskip
\begingroup\small
\raggedright
\setlength{\parskip}{1.5pt}
\newcommand{\indexline}[2]{\par\begingroup\leftskip=#1em\parindent=0pt\hangindent=1em\hangafter=1 #2\par\endgroup}
''']
groups = {'a category','a functor','a group','a monad','a schema','a set','a symbol','a warning','an operad'}
special_parents = set()
for entry in inventory['entries']:
    if entry['english'] in groups and entry['depth'] == 0:
        special_parents.add(entry['id'])
    label = entry['vietnamese_tex']
    # Mathematical names and the deliberately named collection groups already
    # preserve the source identifier. Other entries retain the English lookup key.
    math_only = label.startswith('$') and label.endswith('$')
    needs_original = (not math_only and label.casefold() != entry['english'].casefold()
                      and entry['english'] not in groups)
    if needs_original:
        label += r' (\emph{' + escape(entry['english']) + '})'
    if entry['id'] == 'idx0040':
        label += r'\translatornote{Chỉ mục gốc ghi $\operatorname{Kls}(\top)\to\mathbf{Set}$ và dẫn trang 442 của nguyên bản. Đoạn được dẫn, Nhận xét 7.3.3.3, lại xây dựng hàm tử $i:\mathbf{Set}\to\operatorname{Kls}(\top)$. Bản dịch giữ mục từ gốc và ghi rõ chiều ngược lại trong đoạn ấy.}'
    if entry['id'] == 'idx0317':
        label += r'\translatornote{Mục con ``as functor'' của ``graph homomorphism'' được giữ theo chỉ mục gốc. Đoạn được dẫn thực tế đồng nhất các đồng cấu đồ thị với các biến đổi tự nhiên giữa những hàm tử đồ thị.}'
    seen_pages = set()
    refs=[]
    for target in entry['targets']:
        target_label=target['label']
        page=resolved.get(target_label)
        if page is not None and page in seen_pages:
            continue
        if page is not None:
            seen_pages.add(page)
        refs.append(r'\hyperlink{' + target_label + r'}{\pageref*{' + target_label + '}}')
    if refs:
        label += ', ' + ', '.join(refs)
    elif entry['depth'] == 0:
        label = r'\textbf{' + label + '}'
    parts.append(r'\indexline{' + str(entry['depth']) + '}{' + label + '}')
parts.append(r'\endgroup')
(ROOT / 'translation/index.tex').write_text('\n'.join(parts)+'\n',encoding='utf-8',newline='\n')
report=dict(entry_count=inventory['entry_count'],original_reference_count=inventory['reference_count'],
            anchor_count=sum(len(expected_targets(c)) for c in range(1,8)),
            pagination_status='all_refs_resolved_and_duplicate_pages_coalesced' if args.aux else 'anchors_complete_awaiting_aux',
            aux=str(args.aux) if args.aux else None)
(ROOT / 'review/index-build.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
