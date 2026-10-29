"""cc-P725: a labelled contact sheet of a third-party pack's images (read only), to judge them by eye.
    python -P packsheet.py out.png <folder> [max]"""
import glob, os, sys
from PIL import Image, ImageDraw
out, folder = sys.argv[1], sys.argv[2]
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 40
files = sorted(f for e in ('bmp', 'png', 'tif', 'tiff') for f in glob.glob(os.path.join(folder, '**', '*.' + e), recursive=True))[:mx]
cw, ch, cols = 160, 220, 8
sheet = Image.new('RGB', (cw * cols, ch * ((len(files) + cols - 1) // cols or 1)), (70, 70, 70))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB'); im.thumbnail((cw - 6, ch - 20))
    x, y = (i % cols) * cw, (i // cols) * ch
    sheet.paste(im, (x + 3, y + 3)); d.text((x + 3, y + ch - 14), os.path.basename(f)[:24], fill=(255, 255, 0))
sheet.save(out); print(out, len(files))
