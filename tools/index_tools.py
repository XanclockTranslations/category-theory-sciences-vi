"""Build the translated index inventory. Entry-specific anchors are reviewed separately."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def read_entries():
    entries = []
    parent = None
    source_page = None
    for lineno, line in enumerate((ROOT / 'translation/index-entries.txt').read_text(encoding='utf-8').splitlines(), 1):
        match = re.fullmatch(r'# Source: printed p\. (\d+); PDF p\. (\d+)', line)
        if match:
            source_page = int(match[1])
            assert int(match[2]) == source_page + 9
        if not line or line.startswith('#'):
            continue
        fields = line.split('|')
        if len(fields) != 4:
            raise ValueError(f'Index line {lineno}: expected four fields')
        depth, english, vietnamese, pages = fields
        depth = int(depth)
        assert depth in (0, 1)
        if depth == 1 and parent is None:
            raise ValueError(f'Index line {lineno}: missing parent')
        source_pages = [int(p) for p in pages.split(',')] if pages else []
        assert all(1 <= p <= 474 for p in source_pages)
        entry_id = f'idx{len(entries)+1:04d}'
        entry = dict(id=entry_id, depth=depth, english=english, vietnamese_tex=vietnamese,
                     source_pages=source_pages, index_source_page=source_page,
                     parent_id=parent if depth else None,
                     targets=[dict(source_page=p, label=f'{entry_id}:{p}', status='pending') for p in source_pages])
        entries.append(entry)
        if depth == 0:
            parent = entry_id
    return entries

if __name__ == '__main__':
    entries = read_entries()
    output = ROOT / 'translation/index-inventory.json'
    # Inventory regeneration preserves previously reviewed entry-specific anchors.
    previous = json.loads(output.read_text(encoding='utf-8')) if output.exists() else {}
    old = {e['id']: e for e in previous.get('entries', [])}
    for e in entries:
        prior = old.get(e['id'])
        if prior and prior['english'] == e['english'] and prior['source_pages'] == e['source_pages']:
            e['targets'] = prior['targets']
    report = dict(source_index_printed_pages=list(range(479,487)), entry_count=len(entries),
                  reference_count=sum(len(e['targets']) for e in entries),
                  index_translation_status='draft_complete_pending_independent_review',
                  pagination_status='pending_entry_specific_anchors', entries=entries)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'entries'},ensure_ascii=False))
