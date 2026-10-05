# P62: check the art's stated alignment against body 401 before encoding anything.
# Canvas pixel (x, y) is body-relative (x - 67, y - 98) in p59anim.decode_runs coordinates (the brief).
# Prints, per frame, the art's bounding box in body coordinates, the body's box, and how many art pixels
# land on body pixels (ears on the head, tail at the hip), then writes a 4x strip.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cc-P59-scratch'))
import p59anim as A
from PIL import Image

ART = r'D:\ShatteredLegacy\design\kitsune-ears-tail\stage3-final\walk_dir1'
OUT = os.path.dirname(os.path.abspath(__file__))
OX, OY = 67, 98

print('body 401 resolves to', A.resolve(401))
body = A.frames(401, 0, 1)
print('walk dir1 frames:', len(body))

tiles = []
for i in range(10):
    art = Image.open(os.path.join(ART, 'walk_dir1_f%02d.png' % i)).convert('RGBA')
    assert art.size == (130, 128), art.size
    ap = [(x - OX, y - OY) for y in range(128) for x in range(130) if art.getpixel((x, y))[3]]
    alphas = sorted({art.getpixel((x, y))[3] for y in range(128) for x in range(130)})
    bp = {(x, y): c for x, y, c in body[i]}
    on = sum(1 for p in ap if p in bp)
    bx = [p[0] for p in bp]; by = [p[1] for p in bp]
    ax = [p[0] for p in ap]; ay = [p[1] for p in ap]
    print('f%02d art %3d px, alphas %s, box x %d..%d y %d..%d | body box x %d..%d y %d..%d | art on body %d'
          % (i, len(ap), alphas if len(alphas) < 6 else '%d values' % len(alphas), min(ax), max(ax), min(ay), max(ay),
             min(bx), max(bx), min(by), max(by), on))
    # composite in canvas space
    im = Image.new('RGBA', (130, 128), (40, 90, 40, 255))
    for (x, y), c in bp.items():
        if 0 <= x + OX < 130 and 0 <= y + OY < 128:
            im.putpixel((x + OX, y + OY), A.rgb(c) + (255,))
    im.alpha_composite(art)
    tiles.append(im)

strip = Image.new('RGBA', (130 * 10, 128))
for i, t in enumerate(tiles):
    strip.paste(t, (130 * i, 0))
strip = strip.resize((strip.width * 3, strip.height * 3), Image.NEAREST)
strip.save(os.path.join(OUT, 'input-overlay-3x.png'))
print('wrote input-overlay-3x.png')
