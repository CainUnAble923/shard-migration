"""cc-P818: which DarkWoodDoor art stands in a north-south (east) wall. Draws a stone-shop east wall run (0x0057, x 5)
with candidate closed doors in it (y 2: 0x06B3 NorthCW, y 4: 0x06B1 SouthCCW, y 6: 0x06A9 WestCCW for comparison), an
east-west run (0x0058, y 9) with 0x06A9 in it, and each door's open art one tile along its offset in a second copy
(x 9). Guide 11.2: read every facing from the art.

    python -P door_test818.py <out.png>     (PYTHONPATH=<shard-migration>/scripts, MAPBUILD_CLIENT, MAPBUILD_ART)
"""
import sys

from mapbuild import isorender

land = {(x, y): (0x0003, 0) for x in range(-1, 14) for y in range(-1, 13)}
st = []
for y in range(0, 8):
    st.append((5, y, 0, 0x0057))
for x in range(0, 5):
    st.append((x, 9, 0, 0x0058))
for (y, closed) in ((2, 0x06B3), (4, 0x06B1), (6, 0x06A9)):
    st = [s for s in st if not (s[0] == 5 and s[1] == y)]
    st.append((5, y, 0, closed))
st = [s for s in st if not (s[0] == 2 and s[1] == 9)]
st.append((2, 9, 0, 0x06A9))
# open art (closed + 1) at closed + offset: NorthCW (0,-1), SouthCCW (0,0), WestCCW (-1,0); a second wall at x 10
for y in range(0, 8):
    st.append((10, y, 0, 0x0057))
for (y, opened, off) in ((2, 0x06B4, (0, -1)), (4, 0x06B2, (0, 0)), (6, 0x06AA, (-1, 0))):
    st = [s for s in st if not (s[0] == 10 and s[1] == y)]
    st.append((10 + off[0], y + off[1], 0, opened))
sc = isorender.Scene(land, st)
print(sys.argv[1], isorender.save(isorender.render(sc, 0, 0, 12, 11), sys.argv[1]))
