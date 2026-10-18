"""cc-P166: zoom chosen server directions out of render_dirs sheets, one sheet's three actions under the other's.
    python -P zoom.py OUT.png SHEET [SHEET ...] [--dirs 0,5,6,7]"""
import argparse
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('sheets', nargs='+'); ap.add_argument('--dirs', default='0,5,6,7')
a = ap.parse_args()
W, H = 480, 450
dirs = [int(x) for x in a.dirs.split(',')]
tiles = []
for s in a.sheets:
    im = Image.open(s)
    for r in range(3):
        tiles.append([im.crop((c * W + 105, r * H + 75, c * W + 375, r * H + 415)) for c in dirs])
out = Image.new('RGB', (len(dirs) * 540, len(tiles) * 680))
for j, row in enumerate(tiles):
    for i, t in enumerate(row):
        out.paste(t.resize((540, 680), Image.NEAREST), (i * 540, j * 680))
out.save(a.out)
