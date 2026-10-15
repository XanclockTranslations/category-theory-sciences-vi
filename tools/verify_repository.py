"""Read-only checks for publishable files, LF text, links and the recorded PDF."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote
from pypdf import PdfReader
from index_anchor_io import chapter_source, apply_anchors, source_segments
from source_fingerprint import ROOT, BUILD_TOOLS, PUBLIC_ROOT_FILES, source_fingerprint


def git(*args, check=True):
    return subprocess.run(['git',*args],cwd=ROOT,check=check,capture_output=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    paths = [ROOT/p.decode('utf-8') for p in
             git('ls-files','--cached','--others','--exclude-standard','-z').stdout.split(b'\0') if p]
    assert paths, 'Initialize Git before checking publication files.'
    binary_suffixes = {'.pdf','.png','.jpg','.jpeg','.bmp','.gif','.zip','.ttf','.otf','.woff','.woff2','.exe'}
    texts = 0
    for path in paths:
        assert path.is_file(), f'Missing publication file: {path.relative_to(ROOT)}'
        assert path.stat().st_size < 50*1024*1024, f'Large file: {path.relative_to(ROOT)}'
        if path.suffix.casefold() in binary_suffixes:
            continue
        data = path.read_bytes()
        data.decode('utf-8')
        assert not data.startswith(b'\xef\xbb\xbf'), f'UTF-8 BOM: {path.relative_to(ROOT)}'
        assert b'\r' not in data, f'Non-LF text: {path.relative_to(ROOT)}'
        assert not data or data.endswith(b'\n'), f'Missing final newline: {path.relative_to(ROOT)}'
        texts += 1
        if path.suffix == '.py':
            ast.parse(data.decode('utf-8'),filename=str(path))
        if path.suffix == '.md':
            value = data.decode('utf-8')
            targets = re.findall(r'\]\(([^\s)]+)(?:\s+[^)]*)?\)',value)
            targets += re.findall(r'<img\b[^>]*\bsrc="([^"]+)"',value)
            for target in targets:
                if re.match(r'^[a-z]+:|^#',target,re.I):
                    continue
                target = unquote(target.split('#')[0])
                assert (path.parent/target).exists(), f'Broken link in {path.relative_to(ROOT)}: {target}'
    for name in PUBLIC_ROOT_FILES:
        assert ROOT/name in paths, f'Root metadata omitted by Git: {name}'
    for name in BUILD_TOOLS:
        assert ROOT/'tools'/name in paths, f'Build tool omitted by Git: {name}'
    attrs = git('check-attr','text','eol','--','README.md','translation/chapters/chapter-01.tex',
                'output/pdf/category-theory-sciences-vi-machine.pdf','translation/assets/original-cover.png').stdout.decode('utf-8')
    assert 'README.md: eol: lf' in attrs and 'chapter-01.tex: eol: lf' in attrs
    assert 'category-theory-sciences-vi-machine.pdf: text: unset' in attrs
    assert 'original-cover.png: text: unset' in attrs
    for name in ['tmp/test.png','tools/vendor/tectonic.exe','output/fonts/times.ttf',
                 'output/private.zip','review/render-current.json','.env']:
        assert git('check-ignore','--no-index','--',name,check=False).returncode == 0, name
    for name in ['source/original.pdf','output/pdf/category-theory-sciences-vi-machine.pdf',
                 'translation/assets/original-cover.png']:
        assert git('check-ignore','--no-index','--',name,check=False).returncode == 1, name
    qa = json.loads((ROOT/'review/final-qa.json').read_text(encoding='utf-8'))
    assert qa['status'] == 'passed' and not qa['publication_ready']
    assert source_fingerprint() == qa['source_input_sha256'], 'Sources/build inputs differ from recorded QA.'
    pdf = ROOT/qa['pdf']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == qa['pdf_sha256']
    assert hashlib.sha256((ROOT/'source/original.pdf').read_bytes()).hexdigest() == qa['source_sha256']
    reader = PdfReader(pdf)
    assert len(reader.pages) == qa['pdf_pages'] == 463
    labels = {n for n in reader.named_destinations if re.fullmatch(r'idx\d+:\d+',n)}
    assert len(labels) == qa['index_destinations_verified'] == 605
    markers = 0
    for chapter in range(1,8):
        value = chapter_source(chapter)
        apply_anchors(value,chapter,require_complete=True)
        markers += len(source_segments(value))
    assert markers == qa['chapter_source_markers_verified'] == 474
    print(json.dumps(dict(status='passed',publication_files=len(paths),utf8_lf_text_files=texts,
                          pdf_pages=463,index_destinations=605,source_page_markers=474,
                          markdown_links='passed',git_attributes_and_ignores='passed')))


if __name__ == '__main__':
    main()
