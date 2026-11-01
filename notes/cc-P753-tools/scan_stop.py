"""cc-P753: candidate travel stops for the Custodians' hall near its south doors (1560,974), by fact 2, 3 and 6's checks
of tools/tests/test_guild_hqs_sos.py: standable, not water, open sky, joined on foot to the guildmaster and Hammerhill's
bank, and the figure's cover.

    SL_SHARD_REPO=D:/UO/golems/Iron/ShatteredLegacy python -P -W ignore notes/cc-P753-tools/scan_stop.py
"""
import os
import sys

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'tools', 'tests'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos'))
import numpy as np  # noqa: E402
import test_guild_hqs_sos as T  # noqa: E402
import hallbase as H  # noqa: E402
from walk import Walk  # noqa: E402

T.H = H
os.environ.setdefault('MAPBUILD_ART', H.CLIENT)
from mapbuild import isorender as iso  # noqa: E402

art = iso.Art(art_folder=H.CLIENT, client=H.CLIENT)
h = T.halls()['custodians']
npc = T.pt(h['npc'])
W = Walk(1, T.BOX['Hammerhill'], pad=0)
start = T.FROM['Hammerhill']
g = [hh for hh in W.heights(start[0], start[1]) if abs(hh - start[2]) <= 5]
bank = (start[0], start[1], min(g, key=lambda v: abs(v - start[2])))
reach = W.flood(bank)
beside = [(npc[0] + dx, npc[1] + dy, hh) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy
          for hh in W.heights(npc[0] + dx, npc[1] + dy) if abs(hh - npc[2]) <= 3]
print('guildmaster reached from the bank:', any(t in reach for t in beside))
rows = []
for y in range(972, 982):
    for x in range(1552, 1570):
        for z in W.heights(x, y):
            if abs(z - 5) > 6:
                continue
            lid = W.F.land(x, y)[0]
            wet = H.LAND[lid][0] & H.WET and not any(H.iflags(s[0]) & H.SURF for s in W.F.statics(x, y))
            roof = W.F.roof_over(x, y, z)
            joined = (x, y, z) in reach
            cov = T.figure_covered(iso, art, np, x, y, z)
            ok = not wet and not roof and joined
            rows.append((cov, abs(x - 1560) + abs(y - 974), x, y, z, ok, wet, roof, joined))
for r in sorted(rows, key=lambda r: (not r[5], r[0] > 0.05, r[1])):
    print('%s (%d,%d,%d) cover %3.0f%%  dist %d  wet %s roof %s joined %s' % (
        'OK ' if r[5] else '-- ', r[2], r[3], r[4], r[0] * 100, r[1], bool(r[6]), bool(r[7]), r[8]))
