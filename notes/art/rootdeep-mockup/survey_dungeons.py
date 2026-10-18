"""cc-P141: which floors and walls OSI's own Trammel dungeons use, by count, read through vseUOAware's (fixed) UOP
map reader. Feeds the look swatches: every stock candidate in the mockup is a tile a real dungeon is built from."""
import json, re, sys, collections
sys.path.insert(0, '.')
from vse import Vse

DUNGEONS = {  # pinned Distribution/Data/regions.json, Trammel DungeonRegion areas (first rectangle)
    'Covetous': (5376, 1793, 5577, 2048), 'Deceit': (5122, 518, 5370, 770), 'Despise': (5377, 516, 5631, 1022),
    'Shame': (5377, 2, 5634, 262), 'Wrong': (5633, 511, 5886, 1021), 'Terathan Keep': (5120, 1530, 5374, 1788),
    'Orc Cave': (5281, 1283, 5373, 1386), 'Destard': (5120, 770, 5371, 1028), 'Hythloth': (5898, 2, 6136, 246),
}
LINE = re.compile(r'^\((\d+), (\d+)\): land 0x([0-9A-F]+) \(\d+\), Z=(-?\d+)(.*)$')
STAT = re.compile(r'^\s+- tile 0x([0-9A-F]+) ')

out = {}
with Vse() as v:
    for name, (x1, y1, x2, y2) in DUNGEONS.items():
        land, stat = collections.Counter(), collections.Counter()
        for y in range(y1, y2, 64):
            for x in range(x1, x2, 64):
                t = v.call('inspect_map_region', {'x': x, 'y': y, 'width': min(64, x2 - x), 'height': min(64, y2 - y), 'facet': 1})
                for ln in t.splitlines():
                    st = STAT.match(ln)
                    if st:
                        stat[int(st.group(1), 16)] += 1
                        continue
                    m = LINE.match(ln)
                    if m and int(m.group(3), 16) not in (0x244, 0x1, 0x2):
                        land[int(m.group(3), 16)] += 1
        out[name] = {'land': land.most_common(12), 'statics': stat.most_common(30)}
        print(name, 'land', [hex(a) for a, _ in land.most_common(6)], 'statics', [hex(a) for a, _ in stat.most_common(10)], flush=True)
json.dump(out, open('dungeon-survey.json', 'w'), indent=1)
