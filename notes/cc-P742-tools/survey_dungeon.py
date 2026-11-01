"""cc-P742: the statics OSI's stock dungeons (Trammel x 5120-6143, y 0-2559) use most, with tiledata names and heights,
to pick the vision chamber's walls, floor and dressing from what OSI actually builds dungeons with.
Usage: python -P survey_dungeon.py [client folder] [name filter]"""
import collections
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from mapbuild import uofiles  # noqa: E402

folder = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "-" else r"D:\UO\tool-trials\client-data-copy"
filt = sys.argv[2].lower() if len(sys.argv) > 2 else ""
td = uofiles.read_tiledata(folder)
st = uofiles.statics_in(folder, 1, 5120, 0, 6143, 2559)
c = collections.Counter(s[3] for s in st)
where = {}
for s in st:
    where.setdefault(s[3], (s[0], s[1], s[2]))


def name(tid):
    t = td[1][tid]
    return "%-20s h%-3d %s" % (t["name"], t["height"], uofiles.flagstr(t["flags"]) if hasattr(uofiles, "flagstr") else "")


shown = 0
for tid, n in c.most_common():
    try:
        info = name(tid)
    except Exception as e:  # noqa: BLE001
        info = repr(e)
    s = str(info)
    if filt and filt not in s.lower():
        continue
    print("0x%04X %6d %s at %s" % (tid, n, s[:90], where[tid]))
    shown += 1
    if shown >= 60:
        break
