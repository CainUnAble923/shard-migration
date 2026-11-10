"""cc-P862: isorender of the Battle Chess board in its default spot (rim north-west corner 3673,2629,0, main's SoS Trammel),
with the Haven inn north of it, from P678's SoS reader: the same 100 pieces BattleChessBoard lays (rim of sandstone
stairs at Z 0, marble squares at Z 5). Roofs over Z 19 are cut so the inn's rooms show.
  python -P placerender.py out.jpg"""
import os
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, "D:/UO/golems/Iron/shard-migration/notes/cc-P678-tools/winter")
sys.path.insert(0, "D:/UO/golems/Iron/shard-migration/scripts")
import sosbase as B  # noqa: E402
from mapbuild import isorender as iso  # noqa: E402

BX, BY, BZ = 3673, 2628, 0
CORNERS = {(0, 0): 0x0775, (9, 0): 0x0778, (0, 9): 0x0777, (9, 9): 0x0776}


def piece(i, j):
    if (i, j) in CORNERS:
        return CORNERS[(i, j)]
    if j == 0:
        return 0x076F
    if j == 9:
        return 0x076D
    if i == 0:
        return 0x0770
    return 0x076E


out = sys.argv[1]
x1, y1, x2, y2 = 3656, 2604, 3700, 2648
F = B.facet()
land = {(x, y): F.land(x, y) for x in range(x1 - 2, x2 + 4) for y in range(y1 - 2, y2 + 4)}
st = [(x, y, z, i) for (x, y) in land for i, z in F.statics(x, y) if z < 19]
for i in range(10):
    for j in range(10):
        if i in (0, 9) or j in (0, 9):
            st.append((BX + i, BY + j, BZ, piece(i, j)))
        else:
            f, r = i - 1, 8 - j
            st.append((BX + i, BY + j, BZ + 5, 0x050F if (f + r) % 2 == 0 else 0x0512))
im = iso.render(iso.Scene(land, st), x1, y1, x2, y2, art=iso.Art()).convert("RGB")
im.thumbnail((1000, 1000))
im.save(out, quality=85)
print(out, im.size)
