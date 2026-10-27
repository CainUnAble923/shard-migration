"""cc-P662: the Wakening Isle's picture set, drawn from the built files (the scratch build's edited/ folder), never
from the plan. P663's server items (the farm addon, the lesson props) are drawn in, marked as such in the captions,
so the pictures show the isle as a player will see it; NPCs, doors and the moongate are not drawn.

    python -P render_isle.py <work folder> <out folder>

topdown.png       the whole isle in radar colours, the route walked by build_isle.py's gate (white), the stops
iso-*.png         in-client style (isorender: the client's tile layout, sloped land)
index.html        the set with captions and Chase's question
"""
import html, json, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from mapbuild import isorender, uofiles  # noqa: E402
import build_isle as B  # noqa: E402

ROOF = 0x049C


def font(n):
    for f in ('arial.ttf', 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def radar_colours():
    data = open(os.path.join(isorender.ART_FOLDER, 'radarcol.mul'), 'rb').read()
    vals = struct.unpack('<%dH' % (len(data) // 2), data)
    rgb = lambda v: (((v >> 10) & 31) * 255 // 31, ((v >> 5) & 31) * 255 // 31, (v & 31) * 255 // 31)
    return [rgb(v) for v in vals]


def extras():
    farm, props, pts, door = B.server_items()
    out = [(x, y, z, tid) for (x, y, z, tid, w) in farm]
    return out, props, pts


def iso(folder, rect, name, out, extra, props, roof=True, maxw=1600, label=''):
    x1, y1, x2, y2 = rect
    sc = isorender.Scene.from_map(folder, 1, x1, y1, x2, y2)
    mf = uofiles.MapFile(folder, 1)
    for (x, y, z, tid) in extra:
        if x1 <= x <= x2 and y1 <= y <= y2:
            sc.statics.append((x, y, z, tid))
    for (x, y, z, tid, what) in props:
        if x1 <= x <= x2 and y1 <= y <= y2:
            sc.statics.append((x, y, mf.get(x, y)[1], tid))
    if not roof:
        sc.statics = [s for s in sc.statics if not (s[3] == ROOF and s[2] >= 20)]
    im = isorender.render(sc, x1, y1, x2, y2)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    im = im.convert('RGB')
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width, 26], fill=(0, 0, 0))
    d.text((6, 4), '%s   x %d-%d, y %d-%d%s' % (label, x1, x2, y1, y2, '' if roof else '   (roof hidden, as the client hides it inside)'),
           fill=(255, 255, 255), font=font(16))
    isorender.save(im, os.path.join(out, name))
    return name


def topdown(folder, out, walk, pts):
    x1, y1 = B.shifted(*B.AREA[:2])
    x2, y2 = B.shifted(*B.AREA[2:])
    s = 4
    col = radar_colours()
    mf = uofiles.MapFile(folder, 1)
    sts = {}
    for st in uofiles.statics_in(folder, 1, x1, y1, x2, y2):
        c = (st[0], st[1])
        if c not in sts or st[2] >= sts[c][0]:
            sts[c] = (st[2], st[3])
    im = Image.new('RGB', ((x2 - x1 + 1) * s, (y2 - y1 + 1) * s))
    px = im.load()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            c = col[0x4000 + sts[(x, y)][1]] if (x, y) in sts else col[mf.get(x, y)[0]]
            for a in range(s):
                for b in range(s):
                    px[(x - x1) * s + a, (y - y1) * s + b] = c
    d = ImageDraw.Draw(im)
    for leg in walk:
        if leg:
            d.line([((x - x1) * s + s // 2, (y - y1) * s + s // 2) for (x, y, z) in leg], fill=(255, 255, 255), width=2)
    f = font(14)
    for (n, label, ox, oy) in B.P.STOPS:
        x, y = B.shifted(ox, oy)
        cx, cy = (x - x1) * s + s // 2, (y - y1) * s + s // 2
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(200, 30, 30), outline=(255, 255, 255), width=2)
        tw = d.textlength(str(n), font=f)
        d.text((cx - tw / 2, cy - 8), str(n), fill=(255, 255, 255), font=f)
        d.text((cx - 20, cy + (12 if n % 2 else -28)), label, fill=(255, 255, 255), font=f, stroke_width=2,
               stroke_fill=(0, 0, 0))
    d.rectangle([0, 0, im.width, 24], fill=(0, 0, 0))
    d.text((6, 4), 'The Wakening Isle as built (map 1 file, site A, x %d-%d, y %d-%d), radar colours; white: the route '
           'the gate walked, beach to moongate. North is up.' % (x1, x2, y1, y2), fill=(255, 255, 255), font=f)
    im.save(os.path.join(out, 'topdown.png'), optimize=True)


def main():
    work, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    folder = os.path.join(work, 'edited')
    extra, props, pts = extras()
    rect = B.shifted(*B.AREA[:2]) + B.shifted(*B.AREA[2:])
    w = B.Walker(folder, rect, [(x, y, z, t) for (x, y, z, t) in extra])
    stops = [B.shifted(x, y) for (_, _, x, y) in B.P.STOPS]
    legs = [w.path(a, b) for a, b in zip(stops, stops[1:])]
    topdown(folder, out, legs, pts)
    S = lambda x1, y1, x2, y2: B.shifted(x1, y1) + B.shifted(x2, y2)
    shots = [
        ('iso-beach-camp.png', S(6200, 1984, 6252, 2016), True, 'Stops 0-3: the west beach (Tamsin), the walking tiles, the camp, the clothes rack; P663 props drawn in'),
        ('iso-meadow-farm.png', S(6248, 1962, 6300, 2002), True, 'Stops 4-5: the signpost, the fenced meadow and P276\'s farm (server items, drawn in)'),
        ('iso-yard.png', S(6296, 1994, 6330, 2022), True, 'Stop 6: the training yard, fenced, gate to the road; dummies, butte, ankh'),
        ('iso-square-bank.png', S(6326, 1975, 6354, 2000), True, 'Stop 7: the trades square and the practice bank'),
        ('iso-square-bank-open.png', S(6326, 1975, 6354, 2000), False, 'Stop 7: the bank inside: Merrin\'s room, corners dressed'),
        ('iso-lodge.png', S(6348, 1996, 6368, 2016), True, 'Stop 8: the League lodge'),
        ('iso-lodge-open.png', S(6348, 1996, 6368, 2016), False, 'Stop 8: the lodge inside: Elara\'s room, corners dressed'),
        ('iso-knoll.png', S(6358, 1974, 6384, 1996), True, 'Stop 9: the standing stones on the knoll'),
        ('iso-dock.png', S(6376, 1988, 6414, 2010), True, 'Stop 10: the dock and its landing (the moongate, a server item, stands on 6832,3991)'),
        ('iso-woods.png', S(6280, 1938, 6350, 1980), True, 'The wooded north hills'),
        ('iso-shore.png', S(6196, 1990, 6226, 2020), True, 'The shore: sand to sea (OSI\'s plain sand, static water) and sand to grass (stock transitions)'),
    ]
    made = []
    for name, r, roof, label in shots:
        made.append((iso(folder, r, name, out, extra, props, roof=roof, label=label), label))
    rep = json.load(open(os.path.join(HERE, 'walk-report.json')))
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % tuple(html.escape(str(v)) for v in r)
                   for r in rep['legs'])
    body = ['<!doctype html><meta charset="utf-8"><title>Wakening Isle renders</title>',
            '<style>body{font-family:sans-serif;background:#111;color:#ddd;max-width:1650px;margin:auto;padding:16px}'
            'img{max-width:100%;border:1px solid #444}td,th{border:1px solid #444;padding:2px 8px}'
            'table{border-collapse:collapse}h2{margin-top:28px}</style>',
            '<h1>The Wakening Isle (cc-P662), built</h1>',
            '<p><b>Chase: approve these renders, or say what to change.</b> The patch ships in the player package only '
            'after your yes. Earlier round: P481\'s sketch, <code>notes/cc-P481-tools/new-isle/</code> (plan.png, '
            'iso-farm.png, iso-east.png).</p>',
            '<h2>Top-down, with the walked route</h2><img src="topdown.png">',
            '<h2>The walk (pinned movement rules on the built files)</h2><table><tr><th>Leg</th><th>To</th>'
            '<th>Walked</th><th>Sketch (P481 11.2)</th></tr>%s</table>' % rows]
    for name, label in made:
        body.append('<h2>%s</h2><img src="%s">' % (html.escape(label), name))
    if os.path.exists(os.path.join(out, 'junctions-1.png')):
        body.append('<h2>Junction sheet</h2>')
        n = 1
        while os.path.exists(os.path.join(out, 'junctions-%d.png' % n)):
            body.append('<img src="junctions-%d.png">' % n)
            n += 1
    open(os.path.join(out, 'index.html'), 'w', newline='\n').write('\n'.join(body) + '\n')
    print('made', len(made) + 1, 'pictures in', out)


if __name__ == '__main__':
    main()
