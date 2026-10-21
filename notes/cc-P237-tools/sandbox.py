# cc-P237 read only: our pieces on open grass west of town, to read footprints and facings (sandbox.png, git-ignored).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rend, art_src as S, nhbase as B
I = S.ID
def z(x, y): return rend.F.top_surface(x, y)
pieces = [('orc-tent-1', 3436, 2606), ('orc-tent-2', 3446, 2606), ('orc-tent-3', 3456, 2606),
          ('orc-cage', 3436, 2618), ('orc-fire', 3440, 2618), ('orc-meat', 3443, 2618), ('orc-palisade-1', 3447, 2618),
          ('orc-palisade-2', 3451, 2618), ('orc-rug', 3455, 2618),
          ('cart-fruit-a', 3436, 2624), ('cart-fruit-b', 3439, 2624), ('cart-veg-a', 3442, 2624), ('cart-veg-b', 3445, 2624),
          ('lantern', 3448, 2624), ('rail-y', 3451, 2624), ('rail-x', 3453, 2624), ('rail-y-post', 3455, 2624), ('rail-x-post', 3457, 2624), ('rail-post', 3459, 2624),
          ('beam-ew-bottom', 3436, 2629), ('beam-ew-left', 3439, 2629), ('beam-ew-right', 3442, 2629), ('beam-ns-bottom', 3445, 2629), ('beam-ns-left', 3448, 2629), ('beam-ns-right', 3451, 2629),
          ('ptg-beata', 3454, 2629), ('ptg-ophelia', 3456, 2629)]
extra = [(I[k], x, y, z(x, y)) for k, x, y in pieces]
marks = [(k, x, y, z(x, y), (255, 80, 255, 255)) for k, x, y in pieces]
print(B.render(rend.F, 3426, 2596, 3462, 2634, extra=extra, marks=marks, grid=0, out=os.path.join(rend.HERE, 'sandbox.png'), scale=1))
