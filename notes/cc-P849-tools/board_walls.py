"""cc-P849 item 3: the two requisitions board arts, 0x1E5E and 0x1E5F, each drawn on the floor tile in front of a north wall
and of a west wall (guide 11.2: when two readings disagree, render both and keep the one that draws whole). Four small
rooms, one board each, on a flat stock lawn; client-correct statics (hallbase), the server's Z for a wall-hung item.

    python -P -W ignore notes/cc-P849-tools/board_walls.py out.jpg
"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'cc-P708-tools', 'p281sos'))
import hallbase as H  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
H.CLIENT = H.uofiles.CLIENT = 'D:/UO/tool-trials/client-data-copy'
F = H.Facet(1)
X, Y, Z = 3479, 2619, 10
tiles = []
font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 18)
for art in (0x1E5E, 0x1E5F):
    for wall in ('north', 'west'):
        extra = [(0x0036, X, Y, Z)]
        extra += [(0x0034, x, Y, Z) for x in range(X + 1, X + 4)]
        extra += [(0x0035, X, y, Z) for y in range(Y + 1, Y + 4)]
        extra += [(0x0519, x, y, Z) for x in range(X + 1, X + 4) for y in range(Y + 1, Y + 4)]
        at = (X + 2, Y + 1) if wall == 'north' else (X + 1, Y + 2)
        extra.append((art, at[0], at[1], Z))
        out = os.path.join(os.environ.get('TEMP', '.'), 'bw.png')
        H.render(F, X - 1, Y - 1, X + 4, Y + 4, extra=extra, grid=0, out=out, scale=2)
        im = Image.open(out).convert('RGB')
        d = ImageDraw.Draw(im)
        d.text((8, 8), '0x%04X on the %s wall' % (art, wall), fill=(255, 255, 0), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
        tiles.append(im)
w = max(t.width for t in tiles); h = max(t.height for t in tiles)
sheet = Image.new('RGB', (w * 2 + 10, h * 2 + 10), (0, 0, 0))
for k, t in enumerate(tiles):
    sheet.paste(t, ((k % 2) * (w + 10), (k // 2) * (h + 10)))
sheet.save(sys.argv[1], quality=88)
print('wrote', sys.argv[1], sheet.size)
