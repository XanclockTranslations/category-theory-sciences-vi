"""Render every supplied reading-copy page and record layout-review inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--pdf', type=Path, default=ROOT / 'output/pdf/category-theory-sciences-vi-machine.pdf')
parser.add_argument('--output', type=Path, default=ROOT / 'tmp/pdfs/layout-current')
parser.add_argument('--report', type=Path, default=ROOT / 'review/render-current.json')
parser.add_argument('--poppler', type=Path)
parser.add_argument('--scale', type=int, default=1600, help='Maximum rendered page dimension in pixels')
args = parser.parse_args()
pdf = args.pdf.resolve()
output = args.output.resolve()
report = args.report.resolve()
if not output.is_relative_to(ROOT / 'tmp') or not report.is_relative_to(ROOT):
    raise ValueError('Render output and report must remain in this project')
output.mkdir(parents=True, exist_ok=True)
for pattern in ("page-*.png", "sheet-*.png"):
    for old in output.glob(pattern):
        if not old.resolve().is_relative_to(output.resolve()):
            raise ValueError(f"Unexpected render target: {old}")
        old.unlink()
poppler = args.poppler
if poppler is None:
    installed = shutil.which('pdftoppm')
    poppler = Path(installed) if installed else None
if poppler is None or not poppler.is_file():
    raise SystemExit('Install Poppler and add pdftoppm to PATH, or pass --poppler PATH.')
if args.scale < 1000:
    raise ValueError('Use at least 1000 pixels per page for visual review')
subprocess.run([str(poppler), "-scale-to", str(args.scale), "-png", str(pdf), str(output / "page")], check=True)
pages = sorted(output.glob("page-*.png"))
count = len(PdfReader(pdf).pages)
assert len(pages) == count, (len(pages), count)
sheets = []
for start in range(0, count, 3):
    canvas = Image.new("RGB", (1680, 840), "#d9dde2")
    draw = ImageDraw.Draw(canvas)
    for slot, path in enumerate(pages[start:start + 3]):
        img = Image.open(path).convert("RGB")
        img.thumbnail((550, 790))
        x = slot * 560 + (550 - img.width) // 2
        canvas.paste(img, (x, 35))
        draw.text((slot * 560 + 12, 12), f"PDF page {start + slot + 1}", fill="black")
    path = output / f"sheet-{start // 3 + 1:02d}.png"
    canvas.save(path)
    sheets.append(str(path))
report.parent.mkdir(parents=True, exist_ok=True)
page_hashes = []
for path in pages:
    with Image.open(path) as img:
        page_hashes.append(hashlib.sha256(img.convert('RGB').tobytes()).hexdigest())
report.write_text(json.dumps({"pdf": str(pdf), "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "pdf_pages": count, "rendered_scale_to": args.scale, "page_images": [str(p) for p in pages], "decoded_rgb_sha256": page_hashes, "contact_sheets": sheets, "visual_review_status": "pending"}, indent=2), encoding="utf-8")
print(json.dumps({"pages": count, "contact_sheets": len(sheets)}))
