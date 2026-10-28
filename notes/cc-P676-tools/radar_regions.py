"""cc-P676 item 5: a top-down picture of Trammel's regions over the SoS radar map.

    python -P radar_regions.py <SoS map folder> <regions-trammel.json> <out folder> [x1 y1 x2 y2 name ...]

The radar map: each tile's colour from the client's radarcol.mul, the highest static on it if any, else its land
(0x4000 + item id for a static, as the client's own radar). Outlines by kind: guarded towns red, dungeons purple,
no-housing (keeps, docks, unfinished land) orange, wild areas and isles green, other plain regions grey. Writes
<out>/regions-sos.png (the whole facet at 1/4) and, for each crop given, <out>/crop-<name>.png at full size.
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles  # noqa: E402

W, H = 7168, 4096
KIND = {'TownRegion': (230, 30, 30), 'GuardedRegion': (230, 30, 30), 'DungeonRegion': (170, 60, 220),
        'NoHousingRegion': (255, 150, 0), 'BaseRegion': (40, 200, 60)}
OTHER = (160, 160, 160)


def radar(folder):
    pal = np.frombuffer(open(os.path.join(uofiles.CLIENT, 'radarcol.mul'), 'rb').read(), dtype='<u2')
    ids, _ = uofiles.load_land(folder, 1)            # (W, H) land ids
    col = pal[ids.astype(np.int64) & 0x3FFF].copy()
    idx = np.frombuffer(open(os.path.join(folder, 'staidx1.mul'), 'rb').read(), dtype='<i4').reshape(-1, 3)
    sta = np.frombuffer(open(os.path.join(folder, 'statics1.mul'), 'rb').read(), dtype=np.uint8)
    nb = (W // 8) * (H // 8)
    off, ln = idx[:nb, 0].astype(np.int64), idx[:nb, 1].astype(np.int64)
    ok = (off >= 0) & (ln > 0)
    blocks = np.nonzero(ok)[0]
    counts = ln[ok] // 7
    starts = off[ok]
    rec_block = np.repeat(blocks, counts)
    rec_off = np.repeat(starts, counts) + 7 * (np.arange(counts.sum()) - np.repeat(np.cumsum(counts) - counts, counts))
    tid = sta[rec_off].astype(np.int64) | (sta[rec_off + 1].astype(np.int64) << 8)
    cx, cy = sta[rec_off + 2].astype(np.int64), sta[rec_off + 3].astype(np.int64)
    z = sta[rec_off + 4].astype(np.int8).astype(np.int64)
    x = (rec_block // (H // 8)) * 8 + cx
    y = (rec_block % (H // 8)) * 8 + cy
    order = np.argsort(z, kind='stable')               # later (higher) statics overwrite lower ones
    x, y, tid = x[order], y[order], tid[order]
    col[x, y] = pal[(0x4000 + tid) & 0x7FFF]
    c = col.T.astype(np.uint32)                        # (H, W), ARGB1555
    rgb = np.stack([((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31], axis=-1)
    return rgb.astype(np.uint8)


def draw(img, regions, scale, ox=0, oy=0, width=1):
    d = ImageDraw.Draw(img)
    for r in regions:
        colour = KIND.get(r.get('$type', 'Region'), OTHER)
        for a in r.get('Area', []):
            box = [(a['x1'] - ox) / scale, (a['y1'] - oy) / scale, (a['x2'] - ox) / scale - 1, (a['y2'] - oy) / scale - 1]
            if box[2] < 0 or box[3] < 0 or box[0] > img.width or box[1] > img.height:
                continue
            box[2], box[3] = max(box[0], box[2]), max(box[1], box[3])  # a rect under a pixel at this scale
            d.rectangle(box, outline=colour, width=width)


def main():
    folder, path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out, exist_ok=True)
    regions = json.load(open(path, encoding='utf-8'))
    rgb = radar(folder)
    whole = Image.fromarray(rgb).resize((W // 4, H // 4), Image.BILINEAR)
    draw(whole, regions, 4)
    whole.save(os.path.join(out, 'regions-sos.png'))
    rest = sys.argv[4:]
    for i in range(0, len(rest), 5):
        x1, y1, x2, y2, name = int(rest[i]), int(rest[i + 1]), int(rest[i + 2]), int(rest[i + 3]), rest[i + 4]
        crop = Image.fromarray(rgb[y1:y2, x1:x2]).resize(((x2 - x1) * 2, (y2 - y1) * 2), Image.NEAREST)
        draw(crop, regions, 0.5, x1, y1, width=2)
        crop.save(os.path.join(out, 'crop-%s.png' % name))
    print('wrote', out)


if __name__ == '__main__':
    main()
