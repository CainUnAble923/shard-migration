"""cc-P749: copy the proof shots into notes/cc-P749-tools/shots, shrunk to 960 wide: tazuo-<name> from the real
character's walk, tester-<name> from the Tester spots.
Usage: python -P copy_shots.py <p749-proof folder> <out folder>
"""
import os
import re
import sys

from PIL import Image

P, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
TAZUO = ["lying-02", "lying-10", "getting-up-02", "getting-up-05", "getting-up-08", "getting-up-12", "up-day",
         "up-wreck-beach", "path-chat-sign", "path-farm", "pests", "cleared", "wren-hint", "pip", "table-bandages",
         "healed", "farm-from-road", "fountain", "bank-front", "lodge-front", "lodge-inside", "dock-landing-frame"]
n = 0
for name in TAZUO:
    Image.open(os.path.join(P, "tazuo1", name + ".jpg")).convert("RGB").resize((960, 622)).save(
        os.path.join(OUT, "tazuo-" + name + ".jpg"), quality=80)
    n += 1
for d in ("shots", "shots2"):
    for f in sorted(os.listdir(os.path.join(P, d))):
        if f.endswith(".jpg") and not re.search(r"-f[0-9]+.jpg$", f):
            Image.open(os.path.join(P, d, f)).convert("RGB").resize((960, 622)).save(
                os.path.join(OUT, "tester-" + f), quality=80)
            n += 1
print(n, "shots")
