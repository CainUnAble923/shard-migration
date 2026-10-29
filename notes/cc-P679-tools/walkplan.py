"""cc-P679: the dungeon entrances SoS rebuilt, as walks for walk_entrances.py.

    python -P walkplan.py <overlay> <code copy>

An entrance is a Trammel teleporter in the shipped teleporters-sos.json whose source is on the surface (x < 5120), whose
far end is in the dungeon strip (x >= 5120), and whose source's 3 x 3 SoS changed (changed.py). For each, the walk starts
on an open neighbour of the source (not itself a teleporter source), at that tile's floor nearest the source's Z
(within 10: a mouth may slope up), and steps onto the source; the far end is where the walker must arrive. One walk per entrance (the first tile of a row).
Writes walks.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import changed  # noqa: E402

# Cardinal steps first: a diagonal step also needs both tiles beside it open (pinned Movement), which a cave mouth rarely has.
DIRS = {(0, -1): 'n', (1, 0): 'e', (0, 1): 's', (-1, 0): 'w', (1, -1): 'ne', (1, 1): 'se', (-1, 1): 'sw', (-1, -1): 'nw'}


def main():
    folder, code = sys.argv[1], sys.argv[2]
    both = changed.Both(folder)
    S = both.sos
    data = json.load(open(os.path.join(code, 'server', 'data', 'teleporters-sos.json'), encoding='utf-8'))
    srcs = {(e['src']['map'], *e['src']['loc'][:2]) for e in data} | \
           {(e['dst']['map'], *e['dst']['loc'][:2]) for e in data if e['back']}
    walks, seen = [], set()
    for e in data:
        s, d = e['src'], e['dst']
        if s['map'] != 'Trammel' or d['map'] != 'Trammel' or s['loc'][0] >= 5120 or d['loc'][0] < 5120:
            continue
        x, y, z = s['loc']
        key = (x // 4, y // 4, d['loc'][0] // 16, d['loc'][1] // 16)
        if key in seen or not both.changed(x, y):
            continue
        start = None
        for (dx, dy), name in DIRS.items():
            fx, fy = x - dx, y - dy
            if ('Trammel', fx, fy) in srcs:
                continue
            tops = [t for t in S.open_tops(fx, fy) if abs(t - z) <= 10]  # a slope up to the mouth (Deceit: 5 to 14)
            if tops:
                start = (fx, fy, min(tops, key=lambda t: abs(t - z)), name)
                break
        seen.add(key)
        walks.append({'src': [x, y, z], 'dst': d['loc'], 'start': list(start[:3]) if start else None,
                      'dir': start[3] if start else None})
    json.dump(walks, open(os.path.join(HERE, 'walks.json'), 'w'), indent=1)
    for w in walks:
        print(w)


if __name__ == '__main__':
    main()
