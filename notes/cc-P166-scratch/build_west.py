# cc-P166: the fox tail seen from behind (drawn direction 3: server West, and North mirrored) and the ears' height.
#
# Chase, 2026-10-18 11:28 (screenshot_2026-10-18_11-28-01.png, standing West): the tail is off. In drawn direction 3
# the stage-4 generator laid the tail over her legs, root at the lower back, tip only 4-5 px to the viewer's right
# of it (build_stage4_walk_remaining.py tail_points, direction 3), so it reads as a stripe painted down the back of
# her thigh, not a tail. Facing up-left her back is toward the viewer's lower right, so behind her is the viewer's
# right: the tail now leaves the lower back and sweeps out past the hip there and down to knee height, the
# profile's (direction 2) S-curve foreshortened, drawn over the body (we see her back). Same palette, widths,
# tip, sway and bob as every other direction; only the path changes.
#
# Ears: the world ears sit on the skull's very top, so on a bald head (hair adds a row there) they stand clear of
# it at the sides. All 105 frames' ear pixels move down EAR_DY rows.
#
#     python -P build_west.py --out DIR      write the changed frames to DIR (preview), anim-src untouched
#     python -P build_west.py --write        write them into anim-src\4783 (then build-equip-anims.py)
import argparse, json, os, sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cc-P138-scratch'))
import build_stand_run as B   # the cc-P138 helpers: the stage-4 generator (B.S4), silhouettes, SRC

S4 = B.S4
EAR_ROW = B.EAR_ROW   # canvas rows above this are ears
EAR_DY = 1
ACTIONS = (('walk', 0, 10), ('run', 2, 10), ('stand', 4, 1))
_old_points = S4.tail_points


def tail_points(direction, frame, guide):
    if direction != 3:
        return _old_points(direction, frame, guide)
    left, right = map(int, guide['body_x_at_lower_back'])
    center = (left + right) // 2
    y = int(guide['lower_back_row'])
    sway, bob = S4.TAIL_SWAY[frame], S4.TAIL_BOB[frame]
    return [
        (center, y),
        (center + 2, y + 2),
        (right - 1, y + 5),
        (right + 2 + round(sway * 0.25), y + 9),
        (right + 5 + round(sway * 0.50), y + 12 + bob),
        (right + 7 + sway, y + 15 + bob),
        (right + 6 + sway, y + 18 + bob),
    ]


S4.tail_points = tail_points


def lower_ears(img, dy):
    a = np.array(img)
    ears = a[:EAR_ROW].copy()
    out = a.copy()
    out[:EAR_ROW] = 0
    moved = np.zeros_like(a)
    moved[dy:EAR_ROW + dy] = ears
    keep = moved[..., 3:4] > 0
    out = np.where(keep, moved, out)
    return Image.fromarray(out, 'RGBA')


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--out')
    g.add_argument('--write', action='store_true')
    a = ap.parse_args()
    dest = B.SRC if a.write else a.out
    os.makedirs(dest, exist_ok=True)
    guides = json.loads(open(S4.GUIDES_JSON, encoding='utf-8').read())
    guides = guides.get('frames', guides)
    n = 0
    for action, code, frames in ACTIONS:
        for d in range(5):
            for i in range(frames):
                name = 'a%02d_d%d_f%02d.png' % (code, d, i)
                if d == 3:
                    img = B.generated(action, d, i, guides['%s_dir3_f%02d' % (action, i)], B.silhouette(action, d, i))
                else:
                    img = Image.open(os.path.join(B.SRC, name)).convert('RGBA')
                lower_ears(img, EAR_DY).save(os.path.join(dest, name))
                n += 1
    print('wrote %d frames to %s' % (n, dest))


if __name__ == '__main__':
    main()
