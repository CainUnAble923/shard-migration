# cc-P50 WRITES player-package/vendor/shattered-legacy-art/art/<id>.png for the 18 chest mimic IDs (15472-15489,
# 0x3C70-0x3C81), through scripts/anchor-art-frames.py --keep-geometry --black-transparent (format and black only).
# The table here is the one place the choice of file per ID is written; registry.csv repeats it per row.
#
# Placement only, never a pixel of the art: before the tool runs, a frame may get rows or columns of pure black
# (transparent once converted) added or empty rows cut, so it stands on the tile where the stock chest stands
# (measured in notes/cc-P50-chest-mimic-monster.md section 1.3):
#   - WE frames +4 rows under: stock 0xE42 has 16 empty rows under its art, Archaaz's WE frames have 12.
#   - Dead frames: wider canvases (65 and 72 px), and TazUO centres a canvas on the tile, so columns go on one side
#     until the chest body inside sits on the column it sits on in frame 1. The tongue frames' bodies sit 3 (Extra 7)
#     and 4 (Extra 8) rows above their canvas bottom, so those empty rows are cut.
# Usage: python convert_art.py [--overwrite]
import os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

M = r'D:/UO/third-party/animated-mimic/Mimic'
OUT = r'D:/ShatteredLegacy/player-package/vendor/shattered-legacy-art/art'
TOOL = r'D:/ShatteredLegacy/scripts/anchor-art-frames.py'
NS, WE = M + '/Animations NS/%d.bmp', M + '/Animations WE/%d.bmp'

# (first id, [(source, left, right, cut_bottom, add_bottom), ...]); one call per group, same-size frames only.
GROUPS = [
    (15472, [(NS % i, 0, 0, 0, 0) for i in (2, 3, 4, 5, 6)]),   # NS stills: teeth, open, tongue 1-3
    (15477, [(NS % i, 0, 0, 0, 0) for i in (2, 3)]),            # NS idle loop: base (frame 2) and its frame (3)
    (15479, [(M + '/Extra/6.bmp', 15, 0, 0, 0)]),               # NS dead, empty
    (15480, [(M + '/Extra/8.bmp', 16, 0, 4, 0)]),               # NS dead, tongue out
    (15481, [(WE % i, 0, 0, 0, 4) for i in (2, 3, 4, 5, 6)]),   # WE stills
    (15486, [(WE % i, 0, 0, 0, 4) for i in (2, 3)]),            # WE idle loop
    (15488, [(M + '/Extra/5.bmp', 0, 15, 0, 4)]),               # WE dead, empty
    (15489, [(M + '/Extra/7.bmp', 0, 16, 3, 4)]),               # WE dead, tongue out
]


def placed(src, left, right, cut, add, tmp, n):
    a = np.array(Image.open(src).convert('RGB'))
    if cut:
        assert (a[-cut:] == 0).all(), '%s: the rows to cut are not empty' % src
        a = a[:-cut]
    h, w = a.shape[:2]
    out = np.zeros((h + add, w + left + right, 3), np.uint8)
    out[0:h, left:left + w] = a
    p = os.path.join(tmp, '%d.png' % n)
    Image.fromarray(out, 'RGB').save(p)
    return p


if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as tmp:
        n = 0
        for first, frames in GROUPS:
            files = []
            for f in frames:
                files.append(placed(*f, tmp, n))
                n += 1
            r = subprocess.run([sys.executable, TOOL, '--files'] + files + ['--first-id', str(first), '--out', OUT,
                                '--keep-geometry', '--black-transparent'] + sys.argv[1:], capture_output=True, text=True)
            print(r.stdout.strip() or r.stderr.strip())
            if r.returncode:
                sys.exit(r.returncode)
