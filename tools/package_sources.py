"""Package portable editable sources and publication metadata for the checked PDF."""
from pathlib import Path
import hashlib
import json
import zipfile
from source_fingerprint import ROOT, BUILD_TOOLS, PUBLIC_ROOT_FILES, source_fingerprint

progress = json.loads((ROOT/'translation/progress.json').read_text(encoding='utf-8'))
qa = json.loads((ROOT/'review/final-qa.json').read_text(encoding='utf-8'))
pdf = ROOT/qa['pdf']
pdf_hash = hashlib.sha256(pdf.read_bytes()).hexdigest()
if not progress['full_book_complete'] or qa['status'] != 'passed' or qa['pdf_sha256'] != pdf_hash:
    raise SystemExit('Packaging requires complete progress and passed QA for the current PDF.')
if source_fingerprint() != qa['source_input_sha256']:
    raise SystemExit('Source/build inputs changed after QA; review the changed inputs before packaging.')
files = [ROOT/name for name in PUBLIC_ROOT_FILES]
files += [ROOT/name for name in ('source/original.pdf','source/manifest.json','review/final-qa.json')]
files += [p for p in (ROOT/'translation').rglob('*') if p.is_file() and p.suffix in ('.tex','.txt','.json','.jpg','.png')]
files += [ROOT/'tools'/name for name in BUILD_TOOLS]
files += [p for p in (ROOT/'docs').rglob('*') if p.is_file() and p.suffix in ('.md','.png')]
files = sorted(set(files))
records = [dict(path=p.relative_to(ROOT).as_posix(),size=p.stat().st_size,
                sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
manifest = dict(title='Lý thuyết phạm trù cho các ngành khoa học',
                source_title='Category Theory for the Sciences',author='David I. Spivak',
                publisher='The MIT Press',year=2014,adaptation='Unofficial Vietnamese machine translation',
                ai_model='GPT-6.1 Sol (Ultra)',prompting_by='Bế Trọng Nghĩa',prompting_handle='@ichxorya',
                license='CC BY-NC-SA 4.0',license_url='https://creativecommons.org/licenses/by-nc-sa/4.0/',
                reading_copy_pdf=pdf.relative_to(ROOT).as_posix(),reading_copy_pdf_sha256=pdf_hash,
                reading_copy_pdf_pages=qa['pdf_pages'],files=records,
                exclusions=['Local fonts','Compiler runtimes and caches','Private inspection history',
                            'Recovery mirror','Generated TeX/auxiliary files','Reading-copy PDF supplied separately'])
archive = ROOT/'output/category-theory-sciences-vi-editable.zip'
archive.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as package:
    for path in files:
        package.write(path,arcname='category-theory-sciences-vi/'+path.relative_to(ROOT).as_posix())
    package.writestr('category-theory-sciences-vi/PACKAGE-MANIFEST.json',
                     json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(archive) as package:
    assert package.testzip() is None
    for record in records:
        assert hashlib.sha256(package.read('category-theory-sciences-vi/'+record['path'])).hexdigest() == record['sha256']
result = dict(archive=archive.relative_to(ROOT).as_posix(),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
              archive_bytes=archive.stat().st_size,verified_files=len(records),reading_copy_pdf_sha256=pdf_hash)
(ROOT/'output/source-package.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result))
