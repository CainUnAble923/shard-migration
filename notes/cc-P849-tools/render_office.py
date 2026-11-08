"""cc-P849: the League field office with its server-placed layout (ClusterFRegistrarOfficeLayout.cs) and the requisitions
board drawn in, once with P827's art and once with this fix's, side by side (isorender, client-correct statics).

    python -P -W ignore notes/cc-P849-tools/render_office.py main|release <code copy> out.jpg
"""
import os
import re
import sys

sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts")
which, code, out = sys.argv[1], sys.argv[2], sys.argv[3]
SITE = {
    # client folder, box, cut Z (roofs and upper floors off), board spot, P827 art, this fix's art
    'main': ('D:/UO/golems/Iron/p708-work/sosclient', (3655, 2544, 3677, 2565), 20, (3663, 2548, 0), 0x1E5F, 0x1E5E),
    'release': ('D:/UO/tool-trials/client-data-copy', (3450, 2592, 3466, 2607), 38, (3458, 2602, 18), 0x1E5E, 0x1E5F),
}[which]
os.environ["MAPBUILD_CLIENT"] = SITE[0]
from mapbuild import isorender as R  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

src = open(os.path.join(code, 'server/customizations/ClusterFRegistrarOfficeLayout.cs'), encoding='utf-8').read()
comps = [(int(i, 16), int(x), int(y), int(z)) for i, x, y, z in
         re.findall(r'new\("\w+", (0x[0-9A-Fa-f]+), "[^"]*", (\d+), (\d+), (-?\d+)\)', src)]
assert comps, 'no layout read'
x1, y1, x2, y2 = SITE[1]
font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 20)
halves = []
for label, art in (('before (P827): 0x%04X' % SITE[4], SITE[4]), ('after (P849): 0x%04X' % SITE[5], SITE[5])):
    sc = R.Scene.from_map(SITE[0], 1, x1, y1, x2, y2)
    sc.statics = [s for s in sc.statics if s[2] < SITE[2]]
    for i, x, y, z in comps:
        sc.statics.append((x, y, z, i))
    bx, by, bz = SITE[3]
    sc.statics.append((bx, by, bz, art))
    im = R.render(sc, x1, y1, x2, y2).convert('RGB')
    d = ImageDraw.Draw(im)
    d.text((10, 10), '%s office, %s at %d,%d,%d' % (which, label, bx, by, bz), fill=(255, 255, 0), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    halves.append(im)
w, h = halves[0].size
sheet = Image.new('RGB', (w * 2 + 10, h), (0, 0, 0))
sheet.paste(halves[0], (0, 0)); sheet.paste(halves[1], (w + 10, 0))
if sheet.width > 2400:
    sheet = sheet.resize((2400, int(sheet.height * 2400 / sheet.width)), Image.LANCZOS)
sheet.save(out, quality=86)
print(out, sheet.size, len(comps), 'layout pieces')
