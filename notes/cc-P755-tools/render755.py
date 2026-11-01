"""cc-P755: client-view renders (P708's hallbase on the SoS land) of the moved pieces, old spot marked red, new spot and
stop marked green/cyan. Writes notes/cc-P755-review/render-*.jpg.
    SL_SHARD_REPO=D:/UO/golems/Iron/ShatteredLegacy python -P -W ignore notes/cc-P755-tools/render755.py
"""
import os, sys
DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos'))
import hallbase as H
F = H.Facet(1)
OUT = os.path.join(DOCS, 'notes', 'cc-P755-review')
os.makedirs(OUT, exist_ok=True)
SIGN = 0xA854
RED, GREEN, CYAN = (255, 60, 60, 255), (60, 255, 60, 255), (60, 220, 255, 255)


def z(x, y):
    return F.avgz(x, y)


jobs = [
    ('render-mountain-sign.jpg', (3690, 2732, 3716, 2756), [(SIGN, 3702, 2742, z(3702, 2742))],
     [('old 3702,2745 (in the road)', 3702, 2745, z(3702, 2745), RED), ('new 3702,2742', 3702, 2742, z(3702, 2742), GREEN)],
     None, 'cc-P755: mountain-path signpost moved onto the grass north of the road'),
    ('render-stable-sign.jpg', (3596, 2604, 3620, 2626), [(SIGN, 3608, 2614, 0), (0x0FFA, 3605, 2620, 0), (0x1036, 3606, 2619, 0), (0x0F34, 3605, 2619, 0)],
     [('old 3610,2613 (in the lane)', 3610, 2613, 0, RED), ('new 3608,2614', 3608, 2614, 0, GREEN), ('door', 3607, 2615, 0, CYAN)],
     15, 'cc-P755: stables signpost moved to the porch strip, north of the door path (roofs off)'),
    ('render-stable-sign-roofs.jpg', (3596, 2604, 3620, 2626), [(SIGN, 3608, 2614, 0)],
     [('new 3608,2614', 3608, 2614, 0, GREEN)], None, 'cc-P755: stables signpost with the barn roof on'),
    ('render-housing-stop1.jpg', (3698, 2582, 3720, 2608), [(SIGN, 3713, 2591, z(3713, 2591)), (SIGN, 3704, 2604, z(3704, 2604))],
     [('stop 1 new 3712,2593', 3712, 2593, z(3712, 2593), GREEN), ('stop 1 old 3709,2594', 3709, 2594, z(3709, 2594), RED),
      ('stop 2', 3704, 2605, z(3704, 2605), CYAN), ('door', 3707, 2591, 20, CYAN)],
     None, 'cc-P755: housing stop 1 moved within 2 tiles of its sign (3713,2591)'),
]
for name, box, extra, marks, roofs, label in jobs:
    size = H.render(F, *box, extra=extra, marks=marks, out=os.path.join(OUT, name), hide_roofs_above=roofs, label=label)
    print(name, size)
