"""cc-P177: render dumped gumps (GUMPJSON lines) to PNG, as cc-P169's render.py does, plus item art (GumpItem) and a
survey row per gump. Usage: render2.py LOG OUTDIR PREFIX  (writes PREFIX-<name>.png and PREFIX-survey.json)."""
import json, os, re, runpy, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = runpy.run_path(os.path.join(HERE, 'render.py'), run_name='lib')
I = runpy.run_path(os.path.join(HERE, 'itemart.py'), run_name='lib')
Canvas = R['Canvas']


def blit_item(c, x0, y0, iid, hue=0):
    w, h, p = I['item'](iid)
    ramp = R['hue_ramp'](hue) if hue else None
    for y in range(h):
        for x in range(w):
            px = p[y][x]
            if px[3]:
                X, Y = x0 + x, y0 + y
                if 0 <= X < c.w and 0 <= Y < c.h:
                    rgb = px[:3]
                    if ramp:
                        rgb = ramp[min(31, (rgb[0] + rgb[1] + rgb[2]) // 3 * 32 // 256)]
                    c.px[Y][X] = rgb


def render(entries, path):
    bg = next((e for e in entries if e['type'] == 'GumpBackground'), None)
    if bg:
        W, H = bg['Width'] + 40, bg['Height'] + 40
    else:  # an image-built gump (the Clean Up store): fit what it draws
        W = max(e.get('X', 0) + e.get('Width', 60) for e in entries if 'X' in e) + 60
        H = max(e.get('Y', 0) + e.get('Height', 40) for e in entries if 'Y' in e) + 60
    c = Canvas(W, H)
    page = 0
    for e in entries:
        t = e['type']
        if t == 'GumpPage':
            page = e.get('Page', 0)
            continue
        if page > 1:
            continue
        X, Y = e.get('X', 0) + 20, e.get('Y', 0) + 20
        if t == 'GumpBackground':
            c.background(X, Y, e['Width'], e['Height'], e['GumpID'])
        elif t == 'GumpAlphaRegion':
            c.alpha(X, Y, e['Width'], e['Height'])
        elif t == 'GumpImageTiled':
            c.blit(X, Y, e['GumpID'], tw=e['Width'], th=e['Height'])
        elif t == 'GumpImage':
            c.blit(X, Y, e['GumpID'], hue=e.get('Hue', 0))
        elif t == 'GumpButton':
            c.blit(X, Y, e['NormalID'])
        elif t == 'GumpItem':
            blit_item(c, X, Y, e['ItemID'], e.get('Hue', 0))
        elif t == 'GumpLabel':
            c.text(X, Y, e.get('Text') or '', R['label_rgb'](e['Hue']))
        elif t in ('GumpHtml', 'GumpHtmlLocalized'):
            if e.get('Text'):
                c.html(X, Y, e['Width'], e['Height'], e['Text'])
    c.save(path)
    return W - 40, H - 40


def survey(name, entries):
    t = lambda k: [e for e in entries if e['type'] == k]
    bg = t('GumpBackground')
    first = bg[0] if bg else {}
    tiled = t('GumpImageTiled')
    pages = sorted({e.get('Page', 0) for e in t('GumpPage')})
    return {
        'name': name,
        'size': '%dx%d' % (first.get('Width', 0), first.get('Height', 0)),
        'frame': sorted({b['GumpID'] for b in bg}),
        'inside': 'alpha (see-through)' if t('GumpAlphaRegion') else ('solid 2624' if any(e['GumpID'] == 2624 for e in tiled) else 'none'),
        'rules': sorted({e['GumpID'] for e in tiled if e['GumpID'] != 2624}),
        'buttons': sorted({e['NormalID'] for e in t('GumpButton')}),
        'label_hues': sorted({e['Hue'] for e in t('GumpLabel')}),
        'html_colours': sorted({m.upper() for e in t('GumpHtml') for m in re.findall(r'COLOR=#([0-9A-Fa-f]{6})', e.get('Text') or '')}),
        'images': sorted({e['GumpID'] for e in t('GumpImage')}),
        'items': len(t('GumpItem')),
        'crest': 'none',
        'pages': len(pages),
        'p169': any(e['GumpID'] in (211, 5231) for e in t('GumpImage')),
        'title': next((e.get('Text') or '' for e in t('GumpLabel') if e['Hue'] in (1153, 1154, 1152)), ''),
    }


if __name__ == '__main__':
    log, out, prefix = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    rows = []
    for line in open(log, encoding='utf-8', errors='replace'):
        m = re.search(r'GUMPJSON (\S+) (\[.*\])\s*$', line)
        if m:
            name = m.group(1)
            entries = json.loads(m.group(2))
            p = os.path.join(out, '%s-%s.png' % (prefix, name))
            render(entries, p)
            rows.append(survey(name, entries))
            print(p)
        m = re.search(r'(GUMPERR \S+ .*)$', line)
        if m:
            print(m.group(1))
    json.dump(rows, open(os.path.join(HERE, '%s-survey.json' % prefix), 'w'), indent=1)
