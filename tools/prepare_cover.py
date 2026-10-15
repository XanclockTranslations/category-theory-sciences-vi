"""Preserve the supplied cover art and extend its edge gradient to a B5 canvas.

Vietnamese lettering is an editable vector overlay in frontmatter/cover.tex.
Run with --source-bmp for the first import, or without it to rebuild from PNG.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'translation/assets'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-bmp', type=Path)
    args = parser.parse_args()
    ASSETS.mkdir(parents=True, exist_ok=True)
    original = ASSETS / 'original-cover.png'
    background = ASSETS / 'original-cover-b5.png'
    recipe = ASSETS / 'cover-provenance.json'
    if args.source_bmp:
        with Image.open(args.source_bmp) as supplied:
            art = supplied.convert('RGB')
        art.save(original)
        source = dict(filename=args.source_bmp.name, sha256=sha256(args.source_bmp),
                      format='BMP', supplied_by='User')
    else:
        source = json.loads(recipe.read_text(encoding='utf-8'))['source']
        with Image.open(original) as stored:
            art = stored.convert('RGB')
    width, height = art.size
    canvas_height = round(width * 250 / 177)
    if height > canvas_height:
        raise ValueError('Cover is taller than B5; do not crop original artwork.')
    top = (canvas_height - height) // 2
    bottom = canvas_height - height - top
    canvas = Image.new('RGB', (width, canvas_height))
    if top:
        canvas.paste(art.crop((0, 0, width, 1)).resize((width, top)), (0, 0))
    canvas.paste(art, (0, top))
    if bottom:
        canvas.paste(art.crop((0, height - 1, width, height)).resize((width, bottom)),
                     (0, top + height))
    assert canvas.crop((0, top, width, top + height)).tobytes() == art.tobytes()
    canvas.save(background)
    with Image.open(background) as saved:
        assert saved.crop((0, top, width, top + height)).tobytes() == art.tobytes()
    data = dict(source=source, original_dimensions_px=list(art.size),
                original_rgb_sha256=hashlib.sha256(art.tobytes()).hexdigest(),
                original_png_sha256=sha256(original),
                background_png_sha256=sha256(background),
                canvas_dimensions_px=list(canvas.size), padding_top_px=top,
                padding_bottom_px=bottom, original_pixels_preserved=True,
                method='Lossless RGB import; repeat top/bottom gradient rows; no crop or art retouching.',
                vector_overlay='translation/frontmatter/cover.tex',
                edition_label='Bản dịch máy tiếng Việt',
                ai_model='GPT-6.1 Sol (Ultra)',
                prompting_by='Bế Trọng Nghĩa', prompting_handle='@ichxorya')
    recipe.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    main()
