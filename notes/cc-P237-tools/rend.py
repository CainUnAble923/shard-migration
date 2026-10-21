# cc-P237 read only: client-view renders with our art drawn in (our converted pixels for our IDs; EA's art for the
# rest, as the client draws it). Writes preview-<area>.png here only (git-ignored).
#   python rend.py <area|all>      renders the area boxes below with the placement.json rows of that area
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
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
    'market': (3498, 2566, 3518, 2586, None),
    'field': (3440, 2576, 3462, 2596, None),
    'tailor': (3490, 2544, 3506, 2558, 30),
    'docks': (3494, 2578, 3526, 2614, None),
    'road': (3500, 2530, 3520, 2566, None),
    'office': (3450, 2590, 3466, 2604, 30),
    'healer': (3450, 2543, 3468, 2562, 45),
    'inn': (3490, 2510, 3512, 2532, 40),
    'mage': (3462, 2484, 3492, 2504, 60),
    'bard': (3406, 2594, 3422, 2606, 70),
    'camp': (3582, 2604, 3612, 2634, None),
}


def render_area(name, rows, out=None, scale=0.8, grid=2, marks=True):
    x0, y0, x1, y1, hide = AREAS[name]
    extra = [(r['itemId'], r['x'], r['y'], r['z']) for r in rows if x0 <= r['x'] <= x1 and y0 <= r['y'] <= y1]
    mk = [(r['key'] if marks else '', r['x'], r['y'], r['z'], (255, 80, 255, 255)) for r in rows
          if x0 <= r['x'] <= x1 and y0 <= r['y'] <= y1] if marks else []
    out = out or os.path.join(HERE, 'preview-%s.png' % name)
    return B.render(F, x0, y0, x1, y1, extra=extra, marks=mk, grid=grid, out=out, scale=scale, hide_roofs_above=hide,
                    label='%s (cc-P237 draft)' % name)


if __name__ == '__main__':
    rows = json.load(open(os.path.join(HERE, 'placement.json'))) if os.path.exists(os.path.join(HERE, 'placement.json')) else []
    names = list(AREAS) if sys.argv[1] == 'all' else sys.argv[1:]
    for n in names:
        print(n, render_area(n, rows, scale=1.0, grid=0))
