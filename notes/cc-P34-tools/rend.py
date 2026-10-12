# cc-P34 read only: renders an area of Trammel with the map, statics, optional extra items (our PNGs for our
# own IDs, EA art otherwise) and marks. Through design/registrar-office/uorender.py (render, Map.cs-free).
import sys, os
from PIL import Image
exec(open('nhbase.py').read())
OURS = r'D:/ShatteredLegacy/player-package/vendor/shattered-legacy-art/art'
_static = RNS['Art'].static
def _ours(self, i):
    p = os.path.join(OURS, '%d.png' % i)
    if 15424 <= i <= 15470 and os.path.exists(p): return Image.open(p).convert('RGBA')
    return _static(self, i)
RNS['Art'].static = _ours
def go(name, x0, y0, x1, y1, extra=(), marks=(), grid=5, scale=1):
    print(name, RNS['render'](1, x0, y0, x1, y1, extra=list(extra), marks=list(marks), grid=grid, out=name + '.png', scale=scale))
if __name__ == '__main__':
    a = sys.argv[1:]
    go(a[0], *[int(v) for v in a[1:5]], grid=int(a[5]) if len(a) > 5 else 5, scale=float(a[6]) if len(a) > 6 else 1)
