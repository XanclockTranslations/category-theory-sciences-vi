"""Build the translation with Tectonic and locally supplied fonts on any OS."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FONT_FILES = ('times.ttf','timesbd.ttf','timesi.ttf','timesbi.ttf',
              'arial.ttf','arialbd.ttf','ariali.ttf','arialbi.ttf',
              'consola.ttf','consolab.ttf','consolai.ttf','consolaz.ttf')


def resolve_fonts(font_directory=None):
    directories = []
    if font_directory:
        directories.append(Path(font_directory).expanduser().resolve())
    directories.append(ROOT/'output/fonts')
    if os.name == 'nt':
        directories.append(Path(os.environ.get('SystemRoot', 'C:/Windows'))/'Fonts')
    available = {}
    for directory in directories:
        if directory.is_dir():
            for path in directory.iterdir():
                if path.is_file():
                    available.setdefault(path.name.casefold(), path)
    missing = [name for name in FONT_FILES if name not in available]
    if missing:
        raise SystemExit('Missing fonts: '+', '.join(missing)+
                         '. Supply --font-dir, CT_SCIENCES_FONT_DIR, or output/fonts/.')
    return {name:available[name] for name in FONT_FILES}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font-dir', type=Path, default=os.environ.get('CT_SCIENCES_FONT_DIR'))
    parser.add_argument('--tectonic', default=os.environ.get('CT_SCIENCES_TECTONIC'))
    parser.add_argument('--check', action='store_true', help='Check tools/fonts without writing or compiling a PDF')
    args = parser.parse_args()
    if args.tectonic:
        compiler = Path(shutil.which(str(args.tectonic)) or args.tectonic).expanduser().resolve()
    else:
        compiler = ROOT/'tools/vendor/tectonic'/('tectonic.exe' if os.name == 'nt' else 'tectonic')
        if not compiler.is_file():
            installed = shutil.which('tectonic')
            if not installed:
                raise SystemExit('Install Tectonic on PATH, or supply --tectonic / CT_SCIENCES_TECTONIC.')
            compiler = Path(installed)
    if not compiler.is_file():
        raise SystemExit(f'Tectonic executable not found: {compiler}')
    font_sources = resolve_fonts(args.font_dir)
    if args.check:
        version = subprocess.run([str(compiler),'--version'],check=True,capture_output=True,text=True)
        print(json.dumps(dict(status='passed', compiler=version.stdout.strip(), local_fonts=len(font_sources))))
        return
    if not (ROOT/'output/book-draft.tex').is_file():
        raise SystemExit('Run tools/assemble_book.py before building.')
    fonts = ROOT/'output/fonts'
    fonts.mkdir(parents=True, exist_ok=True)
    for name, source in font_sources.items():
        target = fonts/name
        if source.resolve() != target.resolve():
            shutil.copy2(source,target)
    env = os.environ.copy()
    cache = ROOT/'tools/vendor/tectonic/cache'
    if cache.is_dir():
        env.setdefault('TECTONIC_CACHE_DIR',str(cache))
    (ROOT/'output/pdf').mkdir(parents=True,exist_ok=True)
    (ROOT/'review').mkdir(parents=True,exist_ok=True)
    log_path = ROOT/'review/build.stdout.log'
    with log_path.open('w',encoding='utf-8',newline='\n') as log:
        result = subprocess.run([str(compiler),'-X','compile','--keep-logs',
                                 '--keep-intermediates','--outdir','pdf','book-draft.tex'],
                                cwd=ROOT/'output',env=env,stdout=log,stderr=subprocess.STDOUT)
    log_text = log_path.read_text(encoding='utf-8',errors='replace')
    if result.returncode:
        print('\n'.join(log_text.splitlines()[-30:]))
        raise SystemExit(result.returncode)
    if 'Missing character:' in log_text:
        raise SystemExit(f'Missing-glyph warnings; inspect {log_path}. Output not accepted.')
    assembly = json.loads((ROOT/'output/assembly.json').read_text(encoding='utf-8'))
    filename = 'category-theory-sciences-vi-machine.pdf' if assembly.get('complete_draft') else 'category-theory-sciences-vi-draft.pdf'
    target = ROOT/'output/pdf'/filename
    shutil.copy2(ROOT/'output/pdf/book-draft.pdf',target)
    assembly['reading_copy_pdf'] = target.relative_to(ROOT).as_posix()
    (ROOT/'output/assembly.json').write_text(json.dumps(assembly,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(str(target))
    print(f"Warnings: {sum('warning:' in line for line in log_text.splitlines())}; log: {log_path}")


if __name__ == '__main__':
    main()
