# cc-P793: do the three-frame bursts differ around the walker? (P769's check: prove animation with a burst, not one still.)
import sys
from PIL import Image, ImageChops
d = "D:/UO/golems/Iron/shard-migration/notes/cc-P793-shots/"
for stem in ("3-walking", "5-ridden-walking"):
    a, b, c = [Image.open(d + "%s-%s.jpg" % (stem, x)).convert("L").crop((340, 60, 800, 690)) for x in "abc"]
    for n, (p, q) in (("a-b", (a, b)), ("b-c", (b, c))):
        h = ImageChops.difference(p, q).point(lambda v: 255 if v > 40 else 0)
        print(stem, n, "changed pixels", sum(1 for v in h.getdata() if v))
