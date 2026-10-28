r"""cc-P678 read only: the winter rows against the community art and Halloween tables and HavenSpots as they stand in
the code copy now (tile clashes, and rows within one tile of one). Writes clash.out.txt."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
CUS = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/'
rows = json.load(open(os.path.join(HERE, 'placement.json')))
out = []
for f in ('ClusterFCommunityArtLayout.cs', 'ClusterFHalloweenDecorLayout.cs', 'Tutorial/HavenSpots.cs'):
    pts = {(int(a), int(b)) for a, b in re.findall(r'\b(3[5-7]\d\d),\s*(2[4-7]\d\d)\b', open(CUS + f, encoding='utf-8').read())}
    same = [r['key'] for r in rows if (r['x'], r['y']) in pts]
    near = [r['key'] for r in rows if (r['x'], r['y']) not in pts and any(abs(r['x'] - x) <= 1 and abs(r['y'] - y) <= 1 for x, y in pts)]
    out.append('%s: %d points; winter rows on one: %s; beside one: %s' % (f, len(pts), same or 'none', near or 'none'))
print('\n'.join(out))
open(os.path.join(HERE, 'clash.out.txt'), 'w', encoding='ascii', newline='\n').write('\n'.join(out) + '\n')
