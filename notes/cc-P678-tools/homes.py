r"""cc-P678: the new homes of our New Haven NPCs and guild posts in the author's Haven town (Chase 2026-10-27:
stock pre-UOML Haven plus our pieces). One row per NPC: the building chosen for it, and the tile placer.py picks in it,
each tile checked open on SoS with its floor Z. Groups run in order and later ones avoid earlier tiles.
    python -P homes.py > out/homes.csv
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import placer  # noqa: E402
import soswalk  # noqa: E402

START = (3634, 2586)   # HavenSpots.Start

# (building, box x1 y1 x2 y2, yard?, near (x, y) or None, [(kind, name), ...])
# kind: seed (ClusterFNewHavenSeeder.Entries), guild (GuildLocations.All, seeded), lookout (GuildLocations.Lookouts),
# post (Appraiser's League posts), office (the registrar). Stock guildmasters (unseeded rows) are not placed: their
# row points at the stock spawner's tile instead (see STOCK below).
GROUPS = [
    ("League field office", (3659, 2548, 3673, 2561), False, (3660, 2549),
     [("office", "League Registrar"), ("post", "Appraiser"), ("guild", "custodians")]),
    ("Haven Magery School", (3640, 2464, 3654, 2478), False, (3641, 2465),
     [("seed", "Lyle"), ("seed", "Alefian"), ("seed", "Gustar"), ("seed", "Jillian"), ("seed", "Kaelynna"),
      ("seed", "Mithneral"), ("guild", "arcane"), ("guild", "artificers")]),
    ("Order of the Alembic hall", (3600, 2496, 3616, 2512), False, (3608, 2497),
     [("guild", "alembic"), ("seed", "Sadrah")]),
    ("the Proving Grounds", (3728, 2575, 3736, 2591), True, (3729, 2576),
     [("guild", "warriors"), ("seed", "Aelorn"), ("seed", "Dimethro"), ("seed", "Churchill"), ("seed", "Robyn"),
      ("seed", "Recaro"), ("seed", "Alden Armstrong"), ("seed", "Jockles"), ("seed", "Tyl Ariadne")]),
    ("the Bullseye Marksmen", (3742, 2575, 3750, 2586), True, (3743, 2577),
     [("seed", "Andric"), ("seed", "Kashiel")]),
    ("the Haven inn", (3664, 2608, 3680, 2624), False, (3665, 2609),
     [("seed", "Asandos")]),
    ("A Stitch in Time", (3680, 2464, 3704, 2488), False, (3681, 2465),
     [("seed", "Clairesse")]),
    ("Carpenters of Haven", (3632, 2496, 3648, 2512), False, (3633, 2497),
     [("seed", "Lowel"), ("seed", "Hargrove")]),
    ("Haven Clockworks and Tinker Shop", (3656, 2495, 3672, 2512), False, (3657, 2497),
     [("seed", "Nibbet"), ("seed", "Amelia Youngstone")]),
    ("the Healers of Haven", (3659, 2575, 3674, 2586), False, (3660, 2577),
     [("seed", "Andreas Vesalius"), ("seed", "Avicenna")]),
    ("the Second Bank of Haven", (3615, 2609, 3631, 2623), False, (3624, 2616),
     [("seed", "Sarsmea Smythe"), ("guild", "merchants")]),
    ("The Haven Blacksmith", (3632, 2612, 3646, 2624), False, (3634, 2616),
     [("seed", "George Hephaestus")]),
    # The harbour hall on stilts (3592-3611, 2660-2675) was the first choice; the walk finds no way onto its floor.
    ("the east cottage (Twin Paths dojo)", (3736, 2561, 3744, 2568), False, (3737, 2562),
     [("guild", "dojo"), ("seed", "Ryuichi"), ("seed", "Chiyo"), ("seed", "Jun"), ("seed", "Walker"),
      ("seed", "Hamato")]),
    ("the east house (Keepers of the Last Door)", (3728, 2632, 3736, 2640), False, (3729, 2633),
     [("guild", "keepers"), ("seed", "Mulcivikh"), ("seed", "Morganna")]),
    ("The Haven Thieves' Guild", (3688, 2504, 3704, 2520), False, (3689, 2512),
     [("guild", "thieves"), ("lookout", "thieves")]),
    ("the Bardic Guild in Haven", (3655, 2528, 3679, 2544), False, (3657, 2529),
     [("guild", "bards")]),
    ("the docks", (3640, 2648, 3672, 2662), True, (3652, 2656),
     [("seed", "Norton"), ("guild", "maritime")]),
    # ClusterFInstitutionSeeder's (inst); the guild rows "rangers" and "foresters" point at the same tile.
    ("the farmhouse stables", (3704, 2584, 3712, 2592), False, (3705, 2585),
     [("inst", "rangers")]),
    ("the Woodsman in Haven", (3736, 2680, 3752, 2696), False, (3737, 2681),
     [("inst", "foresters")]),
]

# Unseeded guild rows point at the stock guildmaster's spawner in pinned uoml/trammel/Vendors.json (the town's own),
# or at the vet farmhouse for the Outriders (the institution seeder places that one).
STOCK = [
    ("healers", "the Healers of Haven", (3665, 2581, 0)),
    ("smithing", "The Haven Blacksmith", (3645, 2617, 0)),
    ("tinkers", "Haven Clockworks and Tinker Shop", (3667, 2506, 0)),
    ("tailoring", "A Stitch in Time", (3687, 2477, 0)),
]


def main():
    taken = []
    walk = soswalk.Walk((3568, 2460, 3761, 2712))
    reach = walk.flood(START)
    print("kind,name,building,x,y,z")
    for building, box, yard, near, who in GROUPS:
        # only tiles the walk reaches from the start, standing on the floor itself (not on a table or a step)
        bad = [p for p in walk.stand if p not in reach]
        tiles = [t for t in placer.pick(*box, 4 * len(who), near, avoid=taken + bad, yard=yard)
                 if walk.stand.get(t[:2]) == t[2]]
        tiles = [t for i, t in enumerate(tiles) if all(abs(t[0] - u[0]) > 1 or abs(t[1] - u[1]) > 1 for u in tiles[:i])]
        if len(tiles) < len(who):
            raise SystemExit("%s: only %d tiles for %d" % (building, len(tiles), len(who)))
        for (kind, name), (x, y, z) in zip(who, tiles):
            taken.append((x, y))
            print("%s,%s,%s,%d,%d,%d" % (kind, name, building, x, y, z))
    for key, building, (x, y, z) in STOCK:
        print("stock,%s,%s,%d,%d,%d" % (key, building, x, y, z))


if __name__ == "__main__":
    main()
