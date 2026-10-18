# cc-P166: move the ears (every gump row above EAR_ROWS) of our two paperdoll gumps down: 3 rows (64783), 2 rows (54783), so they rest on a
# bald scalp (Chase, 2026-10-18: "the ears sit a little high on a bald head"); the tail is not touched. Input: the
# cc-P138 files kept beside this script (old-64783-p138.png, old-54783-p138.png), so a rerun gives the same result.
#     python -P lower_paperdoll_ears.py
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
GUMPS = r'D:\ShatteredLegacy\player-package\vendor\shattered-legacy-art\gumps'
EAR_ROWS = 45
# her ears had 3 rows of air over body 13's scalp, his 2 over body 12's (and 3 over the elf's 14, crown one row lower)
for g, DY in (('64783', 3), ('54783', 2)):
    a = np.array(Image.open(os.path.join(HERE, 'old-%s-p138.png' % g)).convert('RGBA'))
    out = a.copy()
    out[:EAR_ROWS] = 0
    ears = a[:EAR_ROWS]
    region = out[DY:EAR_ROWS + DY]
    out[DY:EAR_ROWS + DY] = np.where(ears[..., 3:4] > 0, ears, region)
    Image.fromarray(out, 'RGBA').save(os.path.join(GUMPS, g + '.png'))
    print(g, 'ears down', DY, 'opaque', int((a[..., 3] > 0).sum()), '->', int((out[..., 3] > 0).sum()))
