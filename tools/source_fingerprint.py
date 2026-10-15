"""Bind editable book content and its build scripts to the reviewed reading copy."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
BUILD_TOOLS = ('assemble_book.py','build_pdf.py','generate_index.py','index_anchor_io.py',
               'index_tools.py','audit_book.py','source_fingerprint.py','render_review.py','package_sources.py',
               'prepare_cover.py','verify_repository.py')

PUBLIC_ROOT_FILES = ('.gitignore','.gitattributes','.editorconfig','README.md','README_EN.md',
                     'CONTRIBUTING.md','TRANSLATION_GUIDE.md','license.md','LICENSE','requirements.txt')

def source_fingerprint():
    paths = [p for p in (ROOT / 'translation').rglob('*') if p.is_file()
             and p.suffix in ('.tex','.txt','.json','.jpg','.png') and p.name != 'progress.json']
    paths += [ROOT / 'tools' / name for name in BUILD_TOOLS]
    # Generated assembly must not make clean-clone hashes differ.
    paths += [ROOT / name for name in ('source/original.pdf','source/manifest.json')]
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}
