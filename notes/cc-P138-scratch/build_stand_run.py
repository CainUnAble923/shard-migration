# cc-P138: standing and running frames for the fox ears and tail (Animation 4783), made from the walk art.
#
# Standing (action 4, one frame a direction) and running (action 2, ten frames a direction) had no frames, so the
# ears and tail vanished whenever she stopped or ran. This moves the existing art onto those poses:
#   - directions 0, 2, 3 and 4 use the stage-4 generator as it is (design\kitsune-ears-tail\build_stage4_walk_remaining.py:
#     the same ear and tail shapes, placed by the per-frame guides and, where the tail is behind the body, cut by the
#     body's silhouette), fed the stand and run guides and silhouettes instead of the walk ones;
#   - direction 1, which the art chat drew by hand (stage 3), takes the walk frame of the same index, moves its ears
#     by the crown and head-centre deltas and its tail by the lower-back deltas between the walk and the target
#     frame's guides, and cuts the tail by the target body's silhouette (the tail is behind her in direction 1).
# Output: vendor\shattered-legacy-art\anim-src\4783\a04_d<d>_f00.png and a02_d<d>_f00..09.png (130 x 128, the
# cc-P62 canvas), plus proof strips in notes\cc-P138-scratch\proof\. Run from anywhere:
#     python notes\cc-P138-scratch\build_stand_run.py
import importlib.util, json, os, sys
from PIL import Image

DESIGN = r'D:\ShatteredLegacy\design\kitsune-ears-tail'
SRC = r'D:\ShatteredLegacy\player-package\vendor\shattered-legacy-art\anim-src\4783'
PROOF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proof')
spec = importlib.util.spec_from_file_location('stage4', os.path.join(DESIGN, 'build_stage4_walk_remaining.py'))
S4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S4)
GAME = S4.GAME_SIZE
ACTIONS = {'stand': (4, 1), 'run': (2, 10)}
EAR_ROW = 58   # canvas rows above this are ears (body-relative y < -40), as the walk art is laid out


def silhouette(action, d, i):
    name = '%s_dir%d_f%02d_8x.png' % (action, d, i)
    return Image.open(os.path.join(S4.SIL_DIR, name)).convert('RGBA').resize(GAME, Image.Resampling.NEAREST)


def generated(action, d, i, guide, sil):
    tail = S4.draw_tail(d, i, guide, sil)
    ears = S4.draw_ears(d, i, guide)
    return Image.alpha_composite(tail, ears)


def moved_dir1(action, i, guides, sil):
    walk = Image.open(os.path.join(SRC, 'a00_d1_f%02d.png' % i)).convert('RGBA')
    g0, g1 = guides['walk_dir1_f%02d' % i], guides['%s_dir1_f%02d' % (action, i)]
    ear_dx = (sum(g1['head_x']) - sum(g0['head_x'])) // 2
    ear_dy = g1['crown_y'] - g0['crown_y']
    tail_dx = (sum(g1['body_x_at_lower_back']) - sum(g0['body_x_at_lower_back'])) // 2
    tail_dy = g1['lower_back_row'] - g0['lower_back_row']
    out = Image.new('RGBA', GAME, (0, 0, 0, 0))
    mask = sil.load()
    wp = walk.load()
    op = out.load()
    for y in range(GAME[1]):
        for x in range(GAME[0]):
            if not wp[x, y][3]:
                continue
            if y < EAR_ROW:
                nx, ny = x + ear_dx, y + ear_dy
            else:
                nx, ny = x + tail_dx, y + tail_dy
            if 0 <= nx < GAME[0] and 0 <= ny < GAME[1]:
                if y >= EAR_ROW and mask[nx, ny][3]:
                    continue   # the tail is behind her in direction 1
                op[nx, ny] = wp[x, y]
    S4.remove_small_components(out)
    return out, (ear_dx, ear_dy, tail_dx, tail_dy)


def main():
    guides = S4.load_guides()
    os.makedirs(PROOF, exist_ok=True)
    report = []
    for action, (code, n) in ACTIONS.items():
        strip = Image.new('RGBA', (GAME[0] * n, GAME[1] * 5), (60, 60, 60, 255))
        for d in range(5):
            for i in range(n):
                key = '%s_dir%d_f%02d' % (action, d, i)
                sil = silhouette(action, d, i)
                if d == 1:
                    item, deltas = moved_dir1(action, i, guides, sil)
                else:
                    item, deltas = generated(action, d, i, guides[key], sil), None
                path = os.path.join(SRC, 'a%02d_d%d_f%02d.png' % (code, d, i))
                item.save(path, optimize=False)
                opaque = sum(1 for p in item.getdata() if p[3])
                report.append('%s -> %s: %d px%s' % (key, os.path.basename(path), opaque, (' moved ears %s tail %s' % (deltas[:2], deltas[2:])) if deltas else ''))
                tile = Image.new('RGBA', GAME, (60, 60, 60, 255))
                tile.alpha_composite(sil)    # the body first, as the client draws it; in directions 0 to 2 the tail
                tile.alpha_composite(item)   # was cut by the silhouette, so drawing the item over it is what shows
                strip.paste(tile, (GAME[0] * i, GAME[1] * d))
        strip = strip.resize((strip.width * 2, strip.height * 2), Image.NEAREST)
        strip.save(os.path.join(PROOF, '%s_frames_over_silhouette_2x.png' % action))
    for line in report:
        print(line)


if __name__ == '__main__':
    main()
