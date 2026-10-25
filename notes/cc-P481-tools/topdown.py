"""cc-P481: top-down plan renders for the new player start area options.

Radar colours from the client files (one colour per tile: the topmost static's, else the land's), scaled up, with
the plan drawn on top: zones (boxes), lesson stops (numbered dots) and the walking route between them. Route lengths
are counted on foot over the map files with an 8-direction search (UO counts a diagonal step as one tile), using the
same reduced Movement.cs rules as P188's Walk (land Impassable or Wet blocks; an Impassable non-Surface static within
PersonHeight 16 blocks; StepHeight 2 up). Doors and other server items are not in the map files, so a leg that
crosses a door is marked and counted straight (Chebyshev) instead.

Read only: needs MAPBUILD_CLIENT pointing at a 7.0.117.0 client folder (D:/UO/UltimaOnlineVanilla here).

  python -P topdown.py region <x1> <y1> <x2> <y2> <scale> <out.png>
  python -P topdown.py plan <plan.json> <out.png>
"""
import collections, heapq, json, os, sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles  # noqa: E402

CLIENT = uofiles.CLIENT
FACET = 1
IMP, WET, SURF = 0x40, 0x80, 0x200
PERSON, STEP = 16, 2


def rgb555(c):
    return (((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31)


class Area:
    def __init__(self, x1, y1, x2, y2, folder=CLIENT):
        self.rect = (x1, y1, x2, y2)
        self.m = uofiles.MapFile(folder, FACET)
        self.land, self.items = uofiles.read_tiledata(folder)
        self.sts = collections.defaultdict(list)
        for s in uofiles.statics_in(folder, FACET, x1, y1, x2, y2):
            self.sts[(s[0], s[1])].append(s)
        self.rc = np.frombuffer(open(os.path.join(folder, 'radarcol.mul'), 'rb').read(), dtype='<u2')
        self._stand = {}

    def colour(self, x, y):
        top = None
        for s in self.sts.get((x, y), []):
            if top is None or s[2] >= top[2]:
                top = s
        i = 0x4000 + top[3] if top else self.m.get(x, y)[0]
        return rgb555(int(self.rc[i])) if i < len(self.rc) else (0, 0, 0)

    def image(self, scale):
        x1, y1, x2, y2 = self.rect
        w, h = x2 - x1 + 1, y2 - y1 + 1
        im = Image.new('RGB', (w, h))
        px = im.load()
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                px[x - x1, y - y1] = self.colour(x, y)
        return im.resize((w * scale, h * scale), Image.NEAREST)

    def stand(self, x, y):
        k = (x, y)
        if k in self._stand:
            return self._stand[k]
        x1, y1, x2, y2 = self.rect
        r = None
        if x1 <= x < x2 and y1 <= y < y2:
            t = self.m.get(x, y)
            lf = self.land[t[0]][0]
            if not (lf & (IMP | WET)):
                zs = [self.m.get(x, y)[1], self.m.get(x + 1, y)[1], self.m.get(x, y + 1)[1], self.m.get(x + 1, y + 1)[1]]
                z = (min(zs) + max(zs)) // 2
                top = z
                for s in self.sts.get(k, []):
                    it = self.items[s[3]]
                    if it['flags'] & SURF and s[2] + it['height'] >= top and s[2] <= z + PERSON:
                        top = max(top, s[2] + it['height'])
                r = top
                for s in self.sts.get(k, []):
                    it = self.items[s[3]]
                    if (it['flags'] & IMP) and not (it['flags'] & SURF) and s[2] < top + PERSON and \
                            s[2] + max(it['height'], 1) > top:
                        r = None
                        break
        self._stand[k] = r
        return r

    def path(self, a, b, limit=200000):
        """Shortest 8-direction walk a->b (Dijkstra, unit steps), or None."""
        if self.stand(*a) is None or self.stand(*b) is None:
            return None
        prev = {a: None}
        dist = {a: 0}
        q = [(0, a)]
        n = 0
        while q:
            d, c = heapq.heappop(q)
            if c == b:
                out = []
                while c:
                    out.append(c)
                    c = prev[c]
                return out[::-1]
            n += 1
            if n > limit:
                return None
            cz = self.stand(*c)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if not dx and not dy:
                        continue
                    nb = (c[0] + dx, c[1] + dy)
                    nz = self.stand(*nb)
                    if nz is None or nz - cz > STEP:
                        continue
                    if dx and dy and (self.stand(c[0] + dx, c[1]) is None or self.stand(c[0], c[1] + dy) is None):
                        continue  # Movement.cs refuses a diagonal past a blocked corner
                    if nb not in dist or d + 1 < dist[nb]:
                        dist[nb] = d + 1
                        prev[nb] = c
                        heapq.heappush(q, (d + 1, nb))
        return None


def font(size):
    for f in ('C:/Windows/Fonts/segoeuib.ttf', 'C:/Windows/Fonts/arialbd.ttf'):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def draw_plan(base, plan, area=None):
    """base: an RGB image of the plan rect at plan['scale'] px a tile. Draws zones, stops, route. Returns (im, legs)."""
    x1, y1 = plan['rect'][0], plan['rect'][1]
    s = plan['scale']
    im = base.convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    f = font(max(11, s * 3))
    fs = font(max(10, int(s * 2.4)))

    def P(x, y):
        return ((x - x1) * s + s // 2, (y - y1) * s + s // 2)

    for z in plan.get('zones', []):
        a, b = P(z['x1'], z['y1']), P(z['x2'], z['y2'])
        col = tuple(z.get('colour', (255, 255, 255)))
        d.rectangle([a[0] - s // 2, a[1] - s // 2, b[0] + s // 2, b[1] + s // 2], outline=col + (255,),
                    width=max(2, s // 2), fill=col + (z.get('alpha', 40),))
        d.text((a[0] + 2, a[1] + 1), z['name'], fill=col + (255,), font=fs, stroke_width=2, stroke_fill=(0, 0, 0, 255))
    legs = []
    stops = plan.get('stops', [])
    for i in range(len(stops) - 1):
        a, b = tuple(stops[i]['at'][:2]), tuple(stops[i + 1]['at'][:2])
        p = None
        if area is not None and not stops[i + 1].get('straight') and not stops[i].get('straight'):
            p = area.path(a, b)
        if p:
            legs.append((stops[i]['label'], stops[i + 1]['label'], len(p) - 1, 'walked'))
            pts = [P(*c) for c in p]
        else:
            legs.append((stops[i]['label'], stops[i + 1]['label'], max(abs(a[0] - b[0]), abs(a[1] - b[1])),
                         stops[i + 1].get('how', 'straight')))
            pts = [P(*a), P(*b)]
        dash = stops[i + 1].get('how') in ('gate', 'boat', 'teleport')
        colr = (255, 230, 40, 255) if not dash else (90, 220, 255, 255)
        d.line(pts, fill=(0, 0, 0, 200), width=max(4, s + 2))
        d.line(pts, fill=colr, width=max(2, s - 1))
    for i, st in enumerate(stops):
        c = P(*st['at'][:2])
        r = max(6, int(s * 2.2))
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=(200, 30, 30, 255), outline=(255, 255, 255, 255), width=2)
        num = str(st.get('num', i))
        tw = d.textlength(num, font=fs)
        d.text((c[0] - tw / 2, c[1] - r * 0.75), num, fill=(255, 255, 255, 255), font=fs)
        d.text((c[0] + r + 3, c[1] - r), st['label'], fill=(255, 255, 255, 255), font=fs, stroke_width=2,
               stroke_fill=(0, 0, 0, 255))
    im = Image.alpha_composite(im, ov)
    total = sum(l[2] for l in legs if l[3] not in ('gate', 'boat', 'teleport'))
    hd = ImageDraw.Draw(im)
    title = plan.get('title', '') + ('   walk: %d tiles' % total if stops else '')
    hd.rectangle([0, 0, im.size[0], f.size + 10], fill=(0, 0, 0, 200))
    hd.text((6, 4), title, fill=(255, 255, 255, 255), font=f)
    return im.convert('RGB'), legs, total


def main():
    if sys.argv[1] == 'region':
        x1, y1, x2, y2, sc = map(int, sys.argv[2:7])
        Area(x1, y1, x2, y2).image(sc).save(sys.argv[7], optimize=True)
        return
    plan = json.load(open(sys.argv[2]))
    x1, y1, x2, y2 = plan['rect']
    area = Area(x1, y1, x2, y2)
    for st in plan.get('stops', []):
        # a stop on a tree or rock moves to the nearest tile a player can stand on, and says so
        x, y = st['at'][:2]
        if not st.get('straight') and area.stand(x, y) is None:
            near = min(((abs(x - a) + abs(y - b), (a, b)) for a in range(x - 6, x + 7) for b in range(y - 6, y + 7)
                        if area.stand(a, b) is not None), default=None)
            if near:
                print('stop %s moved %s -> %s' % (st['label'], (x, y), near[1]))
                st['at'] = list(near[1])
    im, legs, total = draw_plan(area.image(plan['scale']), plan, area)
    im.save(sys.argv[3], optimize=True)
    for l in legs:
        print('%-28s -> %-28s %4d  %s' % l)
    print('total walk', total)


if __name__ == '__main__':
    main()
