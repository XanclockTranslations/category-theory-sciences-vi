"""Entry-specific, source-traceable labels for the Vietnamese index."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE_MARKER = re.compile(r'^% Source: printed p\. (\d+); PDF p\. (\d+)\s*$', re.M)

def chapter_for_page(page):
    for n, (start, end) in enumerate(((1,8),(9,40),(41,114),(115,202),(203,314),(315,374),(375,474)),1):
        if start <= page <= end:
            return n
    raise ValueError(f'Not a chapter page: {page}')

def expand_source(path, stack=()):
    path = path.resolve()
    if path in stack or not path.is_relative_to(ROOT):
        raise ValueError(f'Invalid or recursive include: {path}')
    value = path.read_text(encoding='utf-8')
    def include(match):
        name = match[1]
        if not Path(name).suffix:
            name += '.tex'
        for candidate in (path.parent / name, ROOT / name, ROOT / 'output' / name):
            if candidate.exists():
                return expand_source(candidate, stack+(path,))
        raise FileNotFoundError(f'Include {name} from {path}')
    return re.sub(r'\\(?:input|include)\{([^}]+)\}', include, value)

def source_segments(text):
    matches = list(PAGE_MARKER.finditer(text))
    segments = {}
    for i, match in enumerate(matches):
        page = int(match[1])
        if int(match[2]) != page + 9 or page in segments:
            raise ValueError(f'Invalid or duplicate source marker: {match[0]}')
        start, end = match.end(), matches[i+1].start() if i+1 < len(matches) else len(text)
        segments[page] = (start, end)
    return segments

def chapter_source(chapter):
    return expand_source(ROOT / f'translation/chapters/chapter-{chapter:02d}.tex')

def expected_targets(chapter):
    inventory = json.loads((ROOT / 'translation/index-inventory.json').read_text(encoding='utf-8'))
    return {t['label']: dict(t, entry_id=e['id'], english=e['english'],
                             vietnamese_tex=e['vietnamese_tex'], parent_id=e['parent_id'])
            for e in inventory['entries'] for t in e['targets']
            if chapter_for_page(t['source_page']) == chapter}

def anchor_path(chapter):
    return ROOT / f'translation/index-anchors-ch{chapter:02d}.json'

def apply_anchors(text, chapter, require_complete=False):
    path = anchor_path(chapter)
    if not path.exists():
        if require_complete:
            raise ValueError(f'Missing index anchors: {path}')
        return text
    records = json.loads(path.read_text(encoding='utf-8'))['anchors']
    expected = expected_targets(chapter)
    found = set()
    segments = source_segments(text)
    edits = []
    for record in records:
        label = record['label']
        if label in found or label not in expected:
            raise ValueError(f'Duplicate or unrecognized index target: {label}')
        found.add(label)
        if record['source_page'] != expected[label]['source_page']:
            raise ValueError(f'Wrong source index reference: {label}')
        page = record.get('search_page', record['source_page'])
        if page != record['source_page'] and not record.get('reason'):
            raise ValueError(f'Index search-page relocation lacks explanation: {label}')
        start,end = segments[page]
        needle = record['needle']
        if not needle or '\\label' in needle:
            raise ValueError(f'Invalid index anchor needle: {label}')
        hits = list(re.finditer(re.escape(needle),text[start:end]))
        occurrence = record.get('occurrence',1)
        if occurrence < 1 or occurrence > len(hits):
            raise ValueError(f'Index anchor needle missing: {label}, source p.{page}, {needle!r}')
        hit = hits[occurrence-1]
        placement = record.get('placement','after')
        if placement not in ('before','after'):
            raise ValueError(f'Invalid anchor placement: {label}')
        offset = start + (hit.end() if placement == 'after' else hit.start())
        edits.append((offset, f'\\indexanchor{{{label}}}'))
    if require_complete and found != set(expected):
        raise ValueError(f'Unresolved chapter{chapter} index targets: {sorted(set(expected)-found)}')
    for offset,addition in sorted(edits,reverse=True):
        text = text[:offset] + addition + text[offset:]
    return text

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--chapter',type=int,required=True)
    parser.add_argument('--require-complete',action='store_true')
    args=parser.parse_args()
    text=chapter_source(args.chapter)
    apply_anchors(text,args.chapter,args.require_complete)
    print(json.dumps(dict(chapter=args.chapter,expected_index_targets=len(expected_targets(args.chapter)),
                          anchor_manifest_exists=anchor_path(args.chapter).exists(),
                          source_pages=len(source_segments(text)))))
