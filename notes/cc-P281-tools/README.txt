cc-P281 tools: the guild halls' map checks, the server table's generator, and the proof. Run with python -P (numpy and
Pillow are in the user site). They read the client files in D:\UO\tool-trials\client-data-copy (map, statics, multis
and art SHA-256 equal to the shard's classic-client-7.0.117.0) and pinned ModernUO's Distribution/Data. Only gen.py,
setpick.py and breaks.py write anything, and only into this Golem's ShatteredLegacy copy. PNGs here are git-ignored.

The data: ShatteredLegacy design/guild-halls/halls.json (one row per hall). Edit it, run check.py, then gen.py.

hallbase.py      a copy of cc-P237-tools/nhbase.py (cc-P267's bankbase): the facet loader, pinned's z rules, the doors
                 pinned's DoorGenerator would place, spawners, decoration, teleporters, the client-view renderer.
walk.py          the walk model: standable heights per tile (CanFit's blocked test with pinned's decoration items),
                 doors passable, a step of 3 (10 onto or off a Bridge piece); coarser than pinned Movement.Check.
survey_halls.py  per hall, a floor map with doors, spawners, decoration and the stock sign spots (signs.cfg).
pick.py          proposes a main door, a travel stop and guildmaster tiles per hall (the first draft of halls.json).
setpick.py       WRITES one field of halls.json: python -P setpick.py <hall> <npc|sign|travel|building|decor0|hall> k=v
findplot.py      where OSI's Guild House (multi 0x74) fits near a point: clear, flat, off decoration and spawners.
multidump.py     a multi's components from MultiCollection.uop.
check.py         the map checks of every hall (exit 1 on a failure); writes check.out.txt, the notes table.
gen.py           WRITES server/customizations/ClusterFGuildHallPlacementData.cs and the tests' design copy
                 (refuses while check.py fails); --verify says whether both match the design file.
preview.py       client-geometry renders of every hall with its marks (G guildmaster, s sign, T travel stop, D decor).
shots.py         the proof's shot list for notes/cc-P265-tools/proof.ps1 (places every hall, then one shot per hall).
proof-shard.ps1  a private test shard on 127.0.0.1:2596 from the bot shard's copied world (never 2593 or 2594).
breaks.py        WRITES the red runs' six breaks, and "restore" (SHA-256 checked).
