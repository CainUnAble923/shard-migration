cc-P266 tools: read-only map checks and renders for New Haven's winter decor (the second winter set), plus the few
that WRITE (marked). Run with python -P from this folder (numpy and Pillow are in the user site). The map, statics
and art read are D:\UO\tool-trials\client-data-copy through cc-P237-tools\nhbase.py (SHA-256 equal to the shard's
classic-client-7.0.117.0; this Golem may not open D:\ShatteredLegacy). Nothing here touches a world, a save or a
client file.

art_src.py       the one table of source file -> art ID (47 IDs, 0x3388-0x33B6, and the gump 22469); images() also
                 reads P34's shipped PNGs (0x3C40-0x3C6E) for the renders.
protected.py     the tiles no row may use, and why: P237's sources (doors and swings, every seeded coordinate in
                 server/customizations but this task's own layout, pinned spawners and their ring, pinned decoration,
                 teleporters, P188's walk), with the seeded doors' facings winning over pinned DoorGenerator's guess.
draft.py         WRITES placement.json: P34's 61 rows as they are, plus the 48 new rows (bank inside and out, the
                 square, the main roads, the inn's advent candles).
validate.py      checks every row (exit 1 on any failure) and writes validate.out.txt, the notes table. P34's modes
                 plus wallfoot (a street tile at the foot of a building's wall).
gen_layout.py    WRITES server/customizations/ClusterFWinterDecorLayout.cs (refuses while validate.py fails): the
                 rows, the spawner tiles, and RegisteredIds from registry.csv (both winter blocks).
registry_rows.py WRITES the 47 art rows and the gump row into registry.csv (once; refuses if any ID is there).
convert_art.py   WRITES the 47 PNGs (scripts/anchor-art-frames.py --keep-geometry --black-transparent) and
                 gumps/22469.png (the calendar gump, opaque).
records.py       WRITES (with --write) records.json's 7 tiledata and 6 animdata records; the source of every value.
rend.py          client-view renders with the rows drawn in: preview-<area>.png here (git-ignored); the copies Chase
                 gets are notes/art/winter-decor/*.jpg.
topdown.py       the top-down plan of the town with every row marked: topdown.png (copied to notes/art/winter-decor/).
breaks.py        WRITES the red run's seven breaks, and "restore" (byte copies, SHA-256 checked, no P266-BREAK left).
