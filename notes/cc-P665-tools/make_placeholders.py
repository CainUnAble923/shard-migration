"""cc-P665: the two reserved vision panels as plain placeholders (a dark 800 x 600 field with a label), so the package's
"one PNG per registered gump ID" gate holds until Chase's drawings replace them. Not art: a stand-in, like P147's button.

    python -P make_placeholders.py <code copy>
"""
import os, sys
from PIL import Image, ImageDraw

ROOT = sys.argv[1]
OUT = os.path.join(ROOT, 'player-package', 'vendor', 'shattered-legacy-art', 'gumps')
PANELS = {23209: 'vision panel 1: the broken sword (placeholder)', 23210: 'vision panel 2: the League crest (placeholder)'}

for gump_id, label in PANELS.items():
    im = Image.new('RGBA', (800, 600), (18, 18, 24, 255))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 799, 599), outline=(70, 70, 84, 255), width=2)
    w = d.textlength(label)
    d.text(((800 - w) / 2, 294), label, fill=(150, 150, 165, 255))
    path = os.path.join(OUT, '%d.png' % gump_id)
    im.save(path, optimize=True)
    print(path, os.path.getsize(path), 'bytes')
