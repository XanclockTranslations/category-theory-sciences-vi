"""Check source coverage, index destinations, artwork, and final PDF diagnostics."""
from pathlib import Path
import argparse
import hashlib
import json
import re
from pypdf import PdfReader
from index_anchor_io import ROOT, apply_anchors, chapter_source, expected_targets, source_segments
from source_fingerprint import source_fingerprint

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pdf',type=Path)
parser.add_argument('--log',type=Path,help='Optional local TeX log; unavailable diagnostics are reported explicitly')
args = parser.parse_args()
assembly_path = ROOT / 'output/assembly.json'
assembly = json.loads(assembly_path.read_text(encoding='utf-8')) if assembly_path.exists() else {}
pdf = args.pdf.resolve() if args.pdf else ROOT / assembly.get('reading_copy_pdf', 'output/pdf/category-theory-sciences-vi-machine.pdf')
reader = PdfReader(pdf)
chapter_ranges = ((1,8),(9,40),(41,114),(115,202),(203,314),(315,374),(375,474))
chapters = []
expected_labels = set()
for chapter, (start,end) in enumerate(chapter_ranges,1):
    source = chapter_source(chapter)
    markers = set(source_segments(source))
    assert markers == set(range(start,end+1)), (chapter,sorted(set(range(start,end+1))-markers))
    apply_anchors(source,chapter,require_complete=True)
    labels = set(expected_targets(chapter))
    expected_labels.update(labels)
    chapters.append(dict(chapter=chapter,source_pages=end-start+1,index_targets=len(labels)))
destinations = reader.named_destinations
index_labels = {name for name in destinations if re.fullmatch(r'idx\d+:\d+',name)}
assert index_labels == expected_labels, sorted(expected_labels-index_labels)
unresolved_links = []
internal_links = 0
fonts = {}
for page_number,page in enumerate(reader.pages,1):
    resources = page.get('/Resources')
    if resources:
        resources = resources.get_object()
        for reference in resources.get('/Font',{}).get_object().values() if resources.get('/Font') else []:
            font = reference.get_object()
            name = str(font.get('/BaseFont',reference))
            descendants = font.get('/DescendantFonts')
            font_info = descendants[0].get_object() if descendants else font
            descriptor = font_info.get('/FontDescriptor')
            descriptor = descriptor.get_object() if descriptor else {}
            fonts[name] = any(key in descriptor for key in ('/FontFile','/FontFile2','/FontFile3')) or font.get('/Subtype') == '/Type3'
    for reference in page.get('/Annots',[]):
        annotation = reference.get_object()
        action = annotation.get('/A')
        if action:
            action = action.get_object()
        destination = annotation.get('/Dest')
        if action and action.get('/S') == '/GoTo':
            destination = action.get('/D')
        if destination is None:
            continue
        internal_links += 1
        if isinstance(destination,str) and destination not in destinations:
            unresolved_links.append(dict(page=page_number,destination=destination))
assert not unresolved_links, unresolved_links
assert all(fonts.values()), [name for name,embedded in fonts.items() if not embedded]
source_hash = hashlib.sha256((ROOT / 'source/original.pdf').read_bytes()).hexdigest()
assert source_hash == '1e07e429bc482473967c64b868e459b6495ca3f4d590c0fef0a967a4bc86de7e'
assets = json.loads((ROOT / 'translation/assets/ch07-assets.json').read_text(encoding='utf-8'))['assets']
for asset in assets:
    assert hashlib.sha256((ROOT / 'translation/assets' / asset['file']).read_bytes()).hexdigest() == asset['sha256']
log_path = args.log if args.log else ROOT / 'output/pdf/book-draft.log'
if args.log and not log_path.is_file():
    raise FileNotFoundError(log_path)
log = log_path.read_text(encoding='utf-8',errors='replace') if log_path.is_file() else ''
bad_lines = [line for line in log.splitlines() if any(token in line for token in (
    'Missing character:','Overfull','Underfull','undefined references','Reference `','destination with the same identifier'))]
assert not bad_lines, bad_lines
report = dict(pdf=pdf.relative_to(ROOT).as_posix() if pdf.is_relative_to(ROOT) else str(pdf),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),pdf_pages=len(reader.pages),
              source_sha256=source_hash,chapter_source_pages=sum(c['source_pages'] for c in chapters),
              chapters=chapters,index_destinations=len(index_labels),internal_pdf_links=internal_links,
              unresolved_internal_links=unresolved_links,original_image_assets_verified=len(assets),
              embedded_font_count=len(fonts),all_fonts_embedded=True,
              source_input_sha256=source_fingerprint(),
              tex_diagnostic_status='passed' if log_path.is_file() else 'unavailable_no_local_build_log',visual_review_status='separately_recorded_in_final-qa')
(ROOT / 'review').mkdir(parents=True,exist_ok=True)
(ROOT / 'review/final-technical-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('chapters','source_input_sha256')},ensure_ascii=False))
