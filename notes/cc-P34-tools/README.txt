cc-P34 read-only map tools and their outputs, plus the few that WRITE (marked). Loaders: nhbase.py (map1, statics,
tiledata with land names, through design/registrar-office/uorender.py). Nothing here touches a world or a save.

tiles.py         per tile: land name, land z, GetAverageZ, the statics, a GetTopSurfaceZ port, walkway, blocked.
floormap.py      an ASCII map of one floor (walls, furniture, floor) for a box and z.
protected.py     the tiles no row may use, from the seeders' own tables, pinned's door offsets and spawn data.
pick.py          candidate tiles: free floor tiles near a point, wall-art tiles in a room.
candidates.out.txt  the candidates the placement was chosen from (lamp posts, entrances, walls, tables, pier).
draft.py         WRITES placement.json, the proposed rows.
validate.py      checks every row of placement.json (exit 1 on any failure) and prints the notes table:
                 validate.out.txt.
gen_layout.py    WRITES server/customizations/ClusterFWinterDecorLayout.cs from placement.json (refuses while
                 validate.py fails).
convert_art.py   WRITES the 47 PNGs (scripts/anchor-art-frames.py --keep-geometry --black-transparent).
registry_rows.py WRITES the 47 registry rows (once).
rend.py          renders an area with extra items (our PNGs for our IDs): square.png, docks.png, town.png,
                 preview-square.png (the square with the decor), preview-inn.png (roof on).
breaks.py        WRITES the red run's breaks and "restore" (byte copies, SHA-256, no P34-BREAK left).
