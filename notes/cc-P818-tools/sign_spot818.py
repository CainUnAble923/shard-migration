"""cc-P818: where the League lodge's name sign can stand by the new east walk: every tile near the walk's mouth that
passes build_isle.signs_off_path (road within 3 south, none north or beside), using the driver's own road."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'cc-P662-tools'))
import build_isle as B
farm, props, pts, farm_door = B.server_items()
land, statics, report, info = B.plan_spliced(farm, props, pts)
road = {B.shifted(*c) for c in info['road']}
ok = []
for x in range(6784, 6796):
    for y in range(3978, 3992):
        if not B.signs_off_path([(x, y, None, 0xA854, 'lodge sign')], road):
            ok.append((x, y))
print('road near the walk:', sorted(c for c in road if 6784 <= c[0] <= 6795 and 3980 <= c[1] <= 3995))
print('sign spots:', ok)
