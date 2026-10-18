# cc-P138: refit the fox ears and tail paperdoll gump (64783, made in P62 for EA's female body 13) to the Siege of
# Sosaria bodies the shard ships (P81/P103), and make the male gump 54783 from the same art.
#
# The art is moved, not redrawn: the ears component and the tail component of the committed 64783.png are shifted
# by whole pixels (no scaling: the SoS head is 21-23 px wide against EA's 16, and the 34 px ears already overhang
# EA's hair; they read right on both). A single stray pixel at (81, 121) in the old file is dropped.
#
#   python notes\cc-P138-scratch\refit_gumps.py            writes the two PNGs into vendor\shattered-legacy-art\gumps\
#
# Offsets (measured in notes\cc-P138-kitsune-paperdoll-refit.md, section 2):
#   64783 (bodies 13 and 15, crown row 33, head centre x 92):  ears (+2, -25)  tail (0, -14)
#   54783 (bodies 12 and 14, crown row 30, head centre x 92):  ears (+2, -28)  tail (0, -16)
import os, sys
from PIL import Image

ART = r'D:\ShatteredLegacy\player-package\vendor\shattered-legacy-art\gumps'
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'old-64783.png')   # the P62 file, kept here as the source
OFFSETS = {64783: ((2, -25), (0, -14)), 54783: ((2, -28), (0, -16))}


def components(im):
    a = im.split()[3]
    w, h = im.size
    px = {(x, y) for y in range(h) for x in range(w) if a.getpixel((x, y))}
    seen, out = set(), []
    for p in sorted(px):
        if p in seen:
            continue
        stack, comp = [p], []
        seen.add(p)
        while stack:
            x, y = stack.pop()
            comp.append((x, y))
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)):
                if n in px and n not in seen:
                    seen.add(n)
                    stack.append(n)
        out.append(comp)
    return sorted(out, key=len, reverse=True)


def main():
    src = Image.open(SRC).convert('RGBA')
    comps = components(src)
    tail, ears, stray = comps[0], comps[1], comps[2:]
    print('source: tail %d px, ears %d px, stray %s' % (len(tail), len(ears), [c for c in stray]))
    for gump, (ed, td) in OFFSETS.items():
        out = Image.new('RGBA', src.size, (0, 0, 0, 0))
        for pts, (dx, dy) in ((ears, ed), (tail, td)):
            for x, y in pts:
                out.putpixel((x + dx, y + dy), src.getpixel((x, y)))
        path = os.path.join(ART, '%d.png' % gump)
        out.save(path, optimize=True)
        print('wrote', path, 'ears', ed, 'tail', td, 'opaque', sum(1 for p in out.getdata() if p[3]))


if __name__ == '__main__':
    main()
