# cc-P266 read only: client-view renders with the winter rows drawn in (our converted pixels for our IDs, P34's
# shipped PNGs for its set, EA's art for the rest, as the client draws it). Writes preview-<area>.png here
# (git-ignored: notes/cc-P*-tools/*.png) and copies the set Chase gets to notes/art/winter-decor/ (committed, small).
#   python -P rend.py all | <area> ...
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, '..', 'cc-P237-tools'))
import nhbase as B
import art_src

_OURS = art_src.images()
_A = B.art()
_orig = _A.static
def _static(sid):
    if sid in _OURS: return _OURS[sid]
    return _orig(sid)
_A.static = _static

F = B.Facet(1)

# area: (x0, y0, x1, y1, hide roofs and upper floors above this z, or None)
AREAS = {
    'bank-inside': (3476, 2562, 3496, 2583, 25),
    'bank-outside': (3470, 2556, 3500, 2590, None),
    'square': (3494, 2562, 3520, 2588, None),
    'road-inn': (3488, 2526, 3512, 2544, 40),
    'road-main': (3486, 2552, 3518, 2568, None),
    'road-east': (3512, 2562, 3530, 2578, None),
    'road-healer': (3476, 2538, 3496, 2552, None),
    'inn': (3490, 2510, 3512, 2532, 40),
    'town': (3410, 2480, 3545, 2640, None),
}


def render_area(name, rows, out=None, scale=1.0, grid=2, marks=True, new_only_marks=True):
    x0, y0, x1, y1, hide = AREAS[name]
    inside = [r for r in rows if x0 <= r['x'] <= x1 and y0 <= r['y'] <= y1]
    extra = [(r['itemId'], r['x'], r['y'], r['z']) for r in inside]
    mk = []
    if marks:
        for r in inside:
            new = r.get('new', False)
            if new_only_marks and not new: continue
            mk.append((r['key'], r['x'], r['y'], r['z'], (255, 80, 255, 255) if new else (120, 200, 255, 255)))
    out = out or os.path.join(HERE, 'preview-%s.png' % name)
    return B.render(F, x0, y0, x1, y1, extra=extra, marks=mk, grid=grid, out=out, scale=scale, hide_roofs_above=hide,
                    label='%s (cc-P266 draft; magenta = new rows, blue = P34 rows)' % name)


def load_rows():
    rows = json.load(open(os.path.join(HERE, 'placement.json')))
    for k, r in enumerate(rows):
        r['new'] = k >= 61
    return rows


if __name__ == '__main__':
    rows = load_rows()
    names = list(AREAS) if sys.argv[1] == 'all' else sys.argv[1:]
    for n in names:
        if n == 'town':
            print(n, render_area(n, rows, scale=0.5, grid=10, marks=True, new_only_marks=False))
        else:
            print(n, render_area(n, rows, scale=1.0, grid=2, marks=True, new_only_marks=False))
