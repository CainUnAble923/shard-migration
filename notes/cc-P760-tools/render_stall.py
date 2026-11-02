"""cc-P760: isorender of the Festival Peddler's stall in New Haven, the map's own land and statics with the stall's pieces
(FestivalMarket.Pieces, relative to the peddler's tile) added. The peddler is drawn as a marker (a standing person is not
art): a red diamond on her tile.

    python -P render_stall.py <x> <y> <z> out.png [pad]
Env: PYTHONPATH=scripts, MAPBUILD_CLIENT=D:\\UO\\tool-trials\\client-data-copy (isorender's own settings).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import isorender  # noqa: E402
from PIL import ImageDraw  # noqa: E402

# Keep in step with FestivalMarket.Pieces (server/customizations/RewardStores/FestivalStore.cs).
PIECES = [
    (0, 1, 0, 0x0B7C), (1, 1, 0, 0x0B7D),   # the table, in front of her (one long east-west table)
    (-1, 0, 0, 0x0E3D),                      # a crate, behind
    (1, 0, 0, 0x0E77),                       # a barrel, behind
    (-2, -1, 0, 0xA854),                     # the signpost north of the path into the stall, reading from the south
]

FOLDER = os.environ.get('STALL_MAP', 'D:/UO/tool-trials/client-data-copy')  # the shard's overlay folder for the real New Haven

if __name__ == '__main__':
    x, y, z, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    pad = int(sys.argv[5]) if len(sys.argv) > 5 else 9
    x1, y1, x2, y2 = x - pad, y - pad, x + pad, y + pad
    sc = isorender.Scene.from_map(FOLDER, 1, x1, y1, x2, y2)
    for dx, dy, dz, tid in PIECES:
        sc.statics.append((x + dx, y + dy, z + dz, tid))
    im = isorender.render(sc, x1, y1, x2, y2)
    try:
        px, py = isorender.tile_px(im, x, y)
        py += 22 - z * 4
        d = ImageDraw.Draw(im)
        d.polygon([(px, py - 6), (px + 10, py), (px, py + 6), (px - 10, py)], outline=(255, 0, 0, 255), fill=(255, 0, 0, 160))
    except Exception as ex:  # the marker is a help, not the proof
        print('marker:', ex)
    print(out, isorender.save(im, out))
