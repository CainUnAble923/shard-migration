"""cc-P707: the shot list for isle-shots.ps1: the vision at the stones (a frame burst, TazUO's own Legion script starts
it), then the five stops. The trainee (--character) is moved between shots by Iron's Admin: Location and LogoutLocation
(its map stays its tutorial copy). Z is the standing height at each spot, from the isle overlay (cc-P480's Grid).

    python -P gen_shots.py <out shots.json> --map <overlay folder> --tiledata <client folder> [--character "Crystal Shots"]
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "cc-P480-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
import playthrough as base
sys.path.insert(0, HERE)
import islegrid  # cc-P707: surfaces over water are standable (the dock)

# viewpoints: where the trainee stands for each picture (the stop in view, the trainee beside it)
STOPS = [
    ("stop0-beach", (6639, 3994), "the beach: Tamsin, two tiles up the road"),
    ("stop5-farm", (6713, 3982), "the farm gate: Wren, Tobin, the cabbage rows"),
    ("stop6-yard", (6734, 4001), "the training yard: the echo rat and Sera"),
    ("stop7-trades", (6762, 3984), "the trades square: the practice bank's door"),
    ("stop10-dock", (6828, 3991), "the dock: the moongate to New Haven"),
]
STONES = (6794, 3983)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--map", required=True)
    ap.add_argument("--tiledata", required=True)
    ap.add_argument("--character", default="Crystal Shots")
    a = ap.parse_args()
    grid = base.Grid(a.map, a.tiledata, (6594, 3905, 6865, 4049))

    def move(xy):
        z = grid.stand.get(xy)
        if z is None:
            raise SystemExit("no standing height at %s" % (xy,))
        p = "(%d,%d,%d)" % (xy[0], xy[1], z)
        w = 'where playermobile Name == "%s"' % a.character
        return ["[global set Location %s %s" % (p, w), "[global set LogoutLocation %s %s" % (p, w)]

    shots = [{"name": "vision", "character": a.character, "commands": move(STONES), "legion": "IsleVision.py",
              "settle": 14, "frames": 32, "frameMs": 1500, "what": "the loop vision, a burst over its 45 seconds"}]
    for name, xy, what in STOPS:
        shots.append({"name": name, "character": a.character, "commands": move(xy), "what": what})
    json.dump(shots, open(a.out, "w"), indent=1)
    for s in shots:
        print(s["name"], s["commands"][0])


if __name__ == "__main__":
    main()
