"""cc-P814: what stands on and round each fixed New Haven signpost, read from the client's own map, and the fact's data.

The gate's test host loads no client files, so a fact cannot read statics there (MapCheckRealDataVerification's note). This reads
statics1.mul for a box round every 0xA854 in HavenPieces and writes it as a table the fact checks in the gate.

    python -u -P -W ignore notes/cc-P814-tools/sign_statics.py <client folder> <code copy> [check x y ...]
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts', 'mapbuild'))
client, code = sys.argv[1], sys.argv[2]
os.environ['MAPBUILD_CLIENT'] = client
import uofiles as U

RADIUS = 4
src = open(os.path.join(code, 'server/customizations/Tutorial/NewHavenLessons.cs'), encoding='utf-8').read()
signs = [(int(x), int(y), n) for x, y, n in re.findall(r'new\(0xA854, new Point3D\((\d+), (\d+), -?\d+\), "([^"]+)"\)', src)]
assert signs, 'no signs read'
boxes, tiles = [], set()
for x, y, name in signs:
    found = U.statics_in(client, 1, x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS)
    boxes.append((x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS))
    tiles.update((q[0], q[1]) for q in found)
    print(x, y, name, ': statics in the box', len(found), ', on its tile', [hex(q[3]) for q in found if (q[0], q[1]) == (x, y)])
if len(sys.argv) > 3 and sys.argv[3] == 'check':
    v = [int(a) for a in sys.argv[4:]]
    for i in range(0, len(v), 2):
        print(v[i], v[i + 1], [(q[2], hex(q[3])) for q in U.statics_in(client, 1, v[i], v[i + 1], v[i], v[i + 1])])
    sys.exit(0)


def wrap(items):
    out, line = [], '       '
    for it in items:
        c = ' ' + it + ','
        if len(line) + len(c) > 118:
            out.append(line)
            line = '       '
        line += c
    return '\n'.join(out + [line])


text = TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'HavenSignTileVerification.cs.template')).read()
text = text.replace('@BOXES@', wrap('(%d, %d, %d, %d)' % b for b in boxes)).replace('@TILES@', wrap('(%d, %d)' % t for t in sorted(tiles)))
out = os.path.join(code, 'server/tests/Tutorial/HavenSignTileVerification.cs')
open(out, 'w', newline='\n').write(text)
print('wrote', out, len(tiles), 'tiles')
