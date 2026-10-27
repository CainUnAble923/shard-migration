"""cc-P662: candidate sheets drawn with isorender before the build picks its art (playbook section 6: pick from a
render on the ground it goes on, never from tiledata names).

    python -P candidates.py <out folder>

stones.png      standing-stone candidates on grass, each in a ring of three
testhouse.png   an 11 x 9 room in the 0x001A-0x001D stone set with OSI's measured roles (corner 0x001A, north-south
                0x001B, east-west 0x001C, post 0x001D), a south door gap, board floor, and the shingle roof
                (0x05D0 rising, 0x05CE ridge, 0x05CF falling); without a roof, with the shingle roof, and with OSI's
                flat slate roof (0x049C at +20) over the visible room (floor, south ring row, east ring column)
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import isorender, walls as W  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

GRASS = 0x0003
STONE = {'corner': 0x001A, 'ns': 0x001B, 'ew': 0x001C, 'post': 0x001D}


def stones(out):
    cands = [0x1772, 0x01DA, 0x00DB, 0x134F, 0x1350, 0x1351, 0x135D, 0x135E, 0x11B6]
    tiles = []
    for i, tid in enumerate(cands):
        land = {(x, y): (GRASS, 0) for x in range(-1, 6) for y in range(-1, 6)}
        st = [(1, 1, 0, tid), (3, 1, 0, tid), (2, 3, 0, tid)]
        im = isorender.render(isorender.Scene(land, st), 0, 0, 4, 4)
        d = ImageDraw.Draw(im)
        d.text((4, 4), '0x%04X' % tid, fill=(255, 255, 255, 255))
        tiles.append(im)
    w = max(t.width for t in tiles)
    h = max(t.height for t in tiles)
    sheet = Image.new('RGBA', (w * 3, h * 3), (0, 0, 0, 255))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 3) * w, (i // 3) * h))
    isorender.save(sheet.convert('RGB'), os.path.join(out, 'stones.png'))


def house(roofed):
    floor = {(x, y) for x in range(1, 10) for y in range(1, 8)}
    door = (5, 8)
    ring = W.ring_of(floor) - {door}
    Wt = lambda c: c in ring
    st = []
    for (x, y) in sorted(ring):
        for tid, role in W.wall_pieces(Wt, x, y, {k: '0x%04X' % v for k, v in STONE.items()}):
            st.append((x, y, 0, tid))
    for (x, y) in floor | {door}:
        st.append((x, y, 0, 0x04A9 + (x + y) % 4))
    if roofed == 'flat':
        # the visible room: the floor plus the south ring row and the east ring column (their slabs stand on the
        # far edge), so the slate meets the outer face of every wall and never overhangs north or west
        for x in range(1, 11):
            for y in range(1, 9):
                st.append((x, y, 20, 0x049C))
    elif roofed:
        ys = range(0, 9)
        for i, y in enumerate(ys):
            mid = 4
            tid = 0x05D0 if i < mid else (0x05CE if i == mid else 0x05CF)
            z = 20 + 3 * (i if i <= mid else 2 * mid - i)
            for x in range(0, 11):
                st.append((x, y, z, tid))
    land = {(x, y): (0x0071, 0) for x in range(-2, 13) for y in range(-2, 12)}
    return isorender.render(isorender.Scene(land, st), -1, -1, 11, 10)


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    stones(out)
    a, b, c = house(False), house(True), house('flat')
    sheet = Image.new('RGBA', (a.width + b.width + c.width, max(a.height, b.height, c.height)), (0, 0, 0, 255))
    sheet.paste(a, (0, 0))
    sheet.paste(b, (a.width, 0))
    sheet.paste(c, (a.width + b.width, 0))
    isorender.save(sheet.convert('RGB'), os.path.join(out, 'testhouse.png'))


if __name__ == '__main__':
    main()
