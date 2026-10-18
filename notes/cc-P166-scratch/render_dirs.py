"""cc-P166: the fox ears and tail over the wearer in all eight server directions, as TazUO draws them.

Body, hair and our anim 4783 are decoded from the client data and our sl-anim7.bin through validate-art.py
(the package's encoded frames, not the PNGs), placed at one anchor the way MobileView.DrawInternal does
(:817-826: x -= centerX, or W - centerX mirrored, then the image flipped; y -= height + centerY), and drawn in the
client's order (body, hair, earrings). Server direction -> drawn direction and mirror: Animation.GetAnimDirection.

    python -P render_dirs.py OUT [--src PNGDIR]   one sheet per body x hair, plus per-frame numbers to stdout
    --src: use anim-src PNGs from PNGDIR instead of the encoded file (to preview a change before encoding)
"""
import argparse, importlib.util, json, os, re, sys

import numpy as np
from PIL import Image, ImageDraw

SL = r'D:\ShatteredLegacy'
spec = importlib.util.spec_from_file_location('va', os.path.join(SL, 'scripts', 'validate-art.py'))
va = importlib.util.module_from_spec(spec)
sys.argv_saved = sys.argv
spec.loader.exec_module(va)

SERVER = ['N', 'NE(Right)', 'E', 'SE(Down)', 'S', 'SW(Left)', 'W', 'NW(Up)']
# Animation.GetAnimDirection: server direction -> (drawn direction, mirrored)
DRAWN = {0: (3, True), 1: (2, True), 2: (1, True), 3: (0, False), 4: (1, False), 5: (2, False), 6: (3, False), 7: (4, False)}
ACTIONS = {'walk': 0, 'run': 2, 'stand': 4}
HAIR = {'bald': None, 'short': 0x203B, 'long': 0x203C, 'ponytail': 0x203D}
ORIGIN = (67, 98)

c = va.Client(va.DEFAULT_DATA)
tiles = va.ffa.read_tiles(os.path.join(va.DEFAULT_DATA, 'tiledata.mul'))


def item_anim(item_id):
    import struct
    d = open(os.path.join(va.DEFAULT_DATA, 'tiledata.mul'), 'rb').read()
    return struct.unpack_from('<H', d, va.ffa.tile_offset(item_id) + 14)[0]


def frames(body, action, drawn):
    """[(rgba, cx, cy)] for one body, action, drawn direction, or []."""
    r = c.resolve(body)
    blk = c.records(r['file'], r['start'], r['end'])
    if blk is None or action >= r['actions_read']:
        return []
    rec = blk[action * 5 + drawn]
    if rec[0] == -1 or rec[1] <= 0:
        return []
    with open(c.files[r['file']][2], 'rb') as f:
        f.seek(int(rec[0]))
        data = f.read(int(rec[1]))
    return [fr for fr in va.decode_record(data) if fr is not None]


def png_frames(src, action, drawn):
    out, k = [], 0
    while True:
        p = os.path.join(src, 'a%02d_d%d_f%02d.png' % (action, drawn, k))
        if not os.path.exists(p):
            return out
        img = np.array(Image.open(p).convert('RGBA'))
        # canvas pixel (x, y) is anchor + (x - 67, y - 98): as a frame, centre (67, 98 - h)
        out.append((img, ORIGIN[0], ORIGIN[1] - img.shape[0]))
        k += 1


def place(canvas, fr, mirror, ax, ay):
    img, cx, cy = fr
    h, w = img.shape[:2]
    x = ax - (w - cx) if mirror else ax - cx
    y = ay - (h + cy)
    if mirror:
        img = img[:, ::-1]
    sub = canvas[y:y + h, x:x + w]
    a = img[..., 3:4] > 0
    canvas[y:y + h, x:x + w] = np.where(a, img, sub)


def mask_of(fr, mirror, size, ax, ay):
    m = np.zeros(size[::-1] + (4,), np.uint8)
    place(m, fr, mirror, ax, ay)
    return m[..., 3] > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--src')
    ap.add_argument('--scale', type=int, default=3)
    ap.add_argument('--bodies', default='401,400,606,605')
    ap.add_argument('--hair', default='bald,long,short')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    W, H, AX, AY = 160, 150, 80, 115
    stats = {}
    for body in [int(b) for b in a.bodies.split(',')]:
        for hair in a.hair.split(','):
            hanim = item_anim(HAIR[hair]) if HAIR[hair] else None
            rows = []
            for an, act in ACTIONS.items():
                cells = []
                for sd in range(8):
                    drawn, mir = DRAWN[sd]
                    bf = frames(body, act, drawn)
                    hf = frames(hanim, act, drawn) if hanim else []
                    ef = png_frames(a.src, act, drawn) if a.src else frames(4783, act, drawn)
                    k = 0   # first frame; the client clamps an equip index past its last frame to the last
                    cv = np.zeros((H, W, 4), np.uint8)
                    cv[...] = (60, 60, 60, 255)
                    if bf:
                        place(cv, bf[k], mir, AX, AY)
                    if hf:
                        place(cv, hf[min(k, len(hf) - 1)], mir, AX, AY)
                    if ef:
                        place(cv, ef[min(k, len(ef) - 1)], mir, AX, AY)
                    # numbers: head top (topmost body/hair row), ears bottom, gap
                    if bf and ef:
                        bm = mask_of(bf[k], mir, (W, H), AX, AY)
                        if hf:
                            bm |= mask_of(hf[min(k, len(hf) - 1)], mir, (W, H), AX, AY)
                        em = mask_of(ef[min(k, len(ef) - 1)], mir, (W, H), AX, AY)
                        top = int(np.argmax(bm.any(1)))
                        stats[(body, hair, an, sd)] = (top, em, bm)
                    cells.append(cv)
                rows.append(np.concatenate(cells, 1))
            sheet = Image.fromarray(np.concatenate(rows, 0), 'RGBA').convert('RGB')
            sheet = sheet.resize((sheet.width * a.scale, sheet.height * a.scale), Image.NEAREST)
            d = ImageDraw.Draw(sheet)
            for sd in range(8):
                d.text((sd * W * a.scale + 4, 2), '%d %s' % (sd, SERVER[sd]), fill=(255, 255, 0))
            for i, an in enumerate(ACTIONS):
                d.text((4, i * H * a.scale + 14), an, fill=(0, 255, 255))
            name = 'dirs-%d-%s%s.png' % (body, hair, '-src' if a.src else '')
            sheet.save(os.path.join(a.out, name))
            print('wrote', name)
    return stats


if __name__ == '__main__':
    main()
