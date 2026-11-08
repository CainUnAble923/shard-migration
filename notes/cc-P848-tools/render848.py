"""cc-P848: isorender of the release (stock) New Haven round the jail, with the jail, the fixed Haven signs and the
housing stops drawn in.

    python -P -W ignore notes/cc-P848-tools/render848.py <release code copy> out.jpg [x1 y1 x2 y2] [roofless]
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'cc-P801-tools'))
import gen_jail as G  # noqa: E402  (puts cc-P708-tools/p281sos on the path)
import hallbase as H  # noqa: E402

code, out = sys.argv[1], sys.argv[2]
box = [int(a) for a in sys.argv[3:7]] if len(sys.argv) >= 7 else [3445, 2582, 3490, 2627]
roofless = 'roofless' in sys.argv
client, ox, oy, fz = G.SITES['stock']
H.CLIENT = H.uofiles.CLIENT = client
F = H.Facet(1)
extra = [(i, ox + x, oy + y, fz + z) for role, i, x, y, z in G.layout() if not (roofless and role in ('roof', 'gable'))]
extra += [(i, ox + x, oy + y, fz + z) for i, x, y, z in G.SERVER_PLACED]
src = open(os.path.join(code, 'server/customizations/Tutorial/NewHavenLessons.cs'), encoding='utf-8').read()
signs = [(int(x), int(y), n) for x, y, n in re.findall(r'new\(0xA854, new Point3D\((\d+), (\d+), -?\d+\), "([^"]+)"\)', src)]
for x, y, n in signs:
    extra.append((0xA854, x, y, F.avgz(x, y)))
m = re.search(r'HousingStop\(int i\) => i == 0 \? Ground\((\d+), (\d+)\) : Ground\((\d+), (\d+)\)', src)
stops = [(int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))]
marks = [('stop %d' % (k + 1), x, y, F.avgz(x, y), (255, 80, 80, 255)) for k, (x, y) in enumerate(stops)]
marks += [('', x, y, F.avgz(x, y), (80, 200, 255, 255)) for x, y, n in signs if 'Housing' in n]
print('signs', signs)
print('stops', stops)
H.render(F, box[0], box[1], box[2], box[3], extra=extra, marks=marks, grid=5, out=out,
         hide_roofs_above=(fz + 18) if roofless else None, label='release New Haven: jail, Haven signs (blue), housing stops (red)')
print('wrote', out)
