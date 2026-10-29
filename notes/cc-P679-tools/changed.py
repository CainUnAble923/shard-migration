"""cc-P679: did SoS change the land or statics round a tile? Stock is P167's scratch client (EA's Trammel with our old
Rootdeep patch, which only touched void far from any teleporter)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sosland  # noqa: E402
from mapbuild import uofiles  # noqa: E402

STOCK = os.environ.get('SL_STOCK_TRAMMEL', r'D:\UO\cc-p167-work\scratch-client')


class Both:
    def __init__(self, sos_folder, stock_folder=STOCK):
        self.sos, self.stock = sosland.land(sos_folder), sosland.land(stock_folder)

    def changed(self, x, y, r=1):
        """True when any tile within r differs in land id, land Z or its set of statics."""
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                X, Y = x + dx, y + dy
                if not (0 <= X < 7168 and 0 <= Y < 4096):
                    continue
                if int(self.sos.ids[X, Y]) != int(self.stock.ids[X, Y]) or int(self.sos.zs[X, Y]) != int(self.stock.zs[X, Y]):
                    return True
        s1 = sorted(uofiles.statics_in(self.sos.folder, 1, x - r, y - r, x + r, y + r))
        s2 = sorted(uofiles.statics_in(self.stock.folder, 1, x - r, y - r, x + r, y + r))
        return s1 != s2
