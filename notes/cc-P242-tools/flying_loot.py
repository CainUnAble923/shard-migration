"""cc-P242: Clint Bellanger's Flying Loot Animations (CC-BY 3.0) as our animated effect art, IDs 15536-15589.

    python -P flying_loot.py registry <registry.csv>      append the 54 rows (before any PNG); refuses a taken ID
    python -P flying_loot.py frames <scratch dir>         write the reworked 64x128 frames, one folder per animation
    python -P flying_loot.py records <records.json>       append the 9 tiledata and 9 animdata records

Source: D:\\UO\\third-party\\oga-flying-loot\\<name>.png, a 384 x 128 RGB strip of 6 frames, each 64 x 128, pink
(255,0,255) background, the item flying out of a container on an arc and landing, with a flat pure-black drop shadow.

The rework (every change, as CC-BY 3.0 asks to state them):
  1. the pink background becomes transparent;
  2. pure black (0,0,0), which is the drop shadow, becomes transparent: UO art means black as transparent, and an effect
     drawn over a character has no ground to cast a shadow on;
  3. a pixel whose channels are all under 8 (near black, but not black) is lifted to (8,8,8), the darkest colour that
     survives UO's 16-bit art (5 bits a channel), so the item's dark edges never turn into holes;
  4. not resized: the items are already UO's size (a longsword 30 px, a potion 8 px, a ring 5 px, against OSI's
     longsword 0xF61 30 x 30, potion 0xF0C 9 x 17, ring 0x108A 5 x 6), and the arc is about 1.5 times OSI's metal chest
     0xE40 (36 x 45 drawn), so the loot clears the box and lands beside it;
  5. scripts\\anchor-art-frames.py then cuts the six frames to their shared box, centred, bottom row on the tile's tip
     (no pixel changed by that step; it re-reads every PNG against its frame).
Nothing else is changed: no recolouring, no redrawing, the frame order and count are the author's.
"""
import csv
import io
import json
import os
import sys

import numpy as np
from PIL import Image

SRC = r"D:\UO\third-party\oga-flying-loot"
FIRST = 15536
FRAMES = 6
INTERVAL = 1  # animdata frame interval; the server's FlyingLoot sends speed 10, so 100 ms a frame
HOLD = 2      # the landed frame repeats twice more, so the item rests a moment before the effect ends

# (our kind, the author's file, our tiledata name: 19 ASCII characters at most)
ANIMS = [
    ("Blade", "longsword", "flying longsword"),
    ("Bow", "longbow", "flying longbow"),
    ("Staff", "staff", "flying staff"),
    ("Armor", "steel_armor", "flying armor"),
    ("Shield", "shield", "flying shield"),
    ("Jewelry", "ring", "flying ring"),
    ("Gem", "gem", "flying gem"),
    ("Potion", "health_potion", "flying potion"),
    ("Clothing", "clothes", "flying clothes"),
]

LICENSE = ("CC-BY 3.0, Clint Bellanger; changed: pink background and the pure-black drop shadow made transparent, "
           "pixels with every channel under 8 lifted to (8,8,8) for 16-bit art, cut to the six frames' shared box; "
           "not resized, not recoloured; credit Clint Bellanger and Blarumyrran (base icon styles) "
           "(D:\\UO\\third-party\\oga-flying-loot\\SOURCE.txt)")


def base_id(i):
    return FIRST + i * FRAMES


def rework(frame):
    a = np.array(frame.convert("RGB")).astype(np.int32)
    out = np.zeros((a.shape[0], a.shape[1], 4), dtype=np.uint8)
    pink = (a[:, :, 0] == 255) & (a[:, :, 1] == 0) & (a[:, :, 2] == 255)
    black = a.sum(axis=2) == 0
    low = (a.max(axis=2) < 8) & ~black
    keep = ~pink & ~black
    out[:, :, :3] = a.astype(np.uint8)
    out[low, :3] = 8
    out[keep, 3] = 255
    out[~keep] = 0
    return Image.fromarray(out, "RGBA"), int(pink.sum()), int(black.sum()), int(low.sum())


def cmd_registry(path):
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    taken = {line.split(",", 1)[0] for line in text.splitlines() if line and not line.startswith("#")}
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for i, (kind, name, tile) in enumerate(ANIMS):
        for n in range(FRAMES):
            gid = base_id(i) + n
            if str(gid) in taken:
                sys.exit(f"{gid} is already registered")
            what = f"{tile}: loot box opening effect ({kind}), frame {n + 1} of {FRAMES}"
            if n == 0:
                what += " (base ID: has our tiledata and animdata record; cc-P242)"
            source = (f'Clint Bellanger "Flying Loot Animations" (opengameart.org/content/flying-loot-animations) '
                      f"{name}.png frame {n + 1} (x {n * 64}-{n * 64 + 63})")
            w.writerow([str(gid), f"0x{gid:04X}", what, source, LICENSE, "art"])
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text + buf.getvalue())
    print(f"appended {len(ANIMS) * FRAMES} rows")


def cmd_frames(out_dir):
    for i, (kind, name, tile) in enumerate(ANIMS):
        strip = Image.open(os.path.join(SRC, name + ".png"))
        assert strip.size == (64 * FRAMES, 128), (name, strip.size)
        d = os.path.join(out_dir, f"{base_id(i)}-{name}")
        os.makedirs(d, exist_ok=True)
        totals = [0, 0, 0]
        for n in range(FRAMES):
            img, pink, black, low = rework(strip.crop((n * 64, 0, n * 64 + 64, 128)))
            img.save(os.path.join(d, f"f{n}.png"))
            totals = [totals[0] + pink, totals[1] + black, totals[2] + low]
        print(f"{base_id(i)} {name}: pink {totals[0]}, black {totals[1]} transparent; {totals[2]} lifted -> {d}")


def cmd_records(path):
    # records.json is laid out by hand, one record a line, so the new lines go in as text at the end of each array.
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rec = json.loads(text)
    have = {int(t["id"]) for t in rec["tiledata"]} | {int(a["id"]) for a in rec["animdata"]}
    tiles, anims = [], []
    for i, (kind, name, tile) in enumerate(ANIMS):
        b = base_id(i)
        assert b not in have, b
        assert len(tile) <= 19 and tile.isascii(), tile
        # OSI's effect art (the fanfare's sparkle 0x373A): Animation only, weight 255, height 0.
        tiles.append(f'    {{ "id": {b}, "name": "{tile}", "flags": "0x01000000", "weight": 255, "layer": 0, '
                     f'"count": 0, "animId": 0, "hue": 0, "light": 0, "height": 0 }}')
        frames = ", ".join(str(n) for n in list(range(FRAMES)) + [FRAMES - 1] * HOLD)
        anims.append(f'    {{ "id": {b}, "frames": [{frames}], "interval": {INTERVAL}, "start": 0 }}')
    for key, lines in (("tiledata", tiles), ("animdata", anims)):
        head = text.index(f'  "{key}": [')
        close = text.index("\n  ]", head)
        text = text[:close] + ",\n" + ",\n".join(lines) + text[close:]
    after = json.loads(text)
    assert len(after["tiledata"]) == len(rec["tiledata"]) + len(ANIMS)
    assert len(after["animdata"]) == len(rec["animdata"]) + len(ANIMS)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"appended {len(ANIMS)} tiledata and {len(ANIMS)} animdata records")


if __name__ == "__main__":
    {"registry": cmd_registry, "frames": cmd_frames, "records": cmd_records}[sys.argv[1]](sys.argv[2])
