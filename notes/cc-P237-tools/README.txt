cc-P237 tools: read-only map checks and renders for New Haven's community art, plus the few that WRITE (marked).
Run with python -P (numpy and Pillow are in the user site). Nothing here touches a world, a save or a client file.
The client files read are D:\UO\tool-trials\client-data-copy (map, statics and art SHA-256 equal to the shard's
classic-client-7.0.117.0, tool-trials\hashes-*-after.txt): this Golem may not open D:\ShatteredLegacy.

make_base.py     WRITES nhbase.py: cc-P267-tools/bankbase.py with its two paths changed. The loader, pinned's z rules
                 (GetAverageZ, GetTopSurfaceZ, CanFit's blocked test), doors, spawners, decoration, the renderer.
art_src.py       the one table of source file -> art ID (34 IDs, 0x3C88-0x3CA9), and the converted pixels for renders.
facts.py         every image in the seven packs (size, mode, content box) -> facts.out.txt; contact sheets sheet-*.png.
protected.py     the tiles no row may use, and why (doors and swings, every seeded coordinate, pinned spawners and their
                 ring, pinned decoration, teleporters, P188's walk).
survey.py, rooms.py, pick.py, overview.py, campview.py, sandbox.py   the survey: names, floor maps, free tiles, renders.
draft.py         WRITES placement.json, the 44 proposed rows (key, area, x, y, z, item, name, mode, why).
validate.py      checks every row (exit 1 on any failure) and writes validate.out.txt, the notes table.
rend.py          renders each area with the rows drawn in: preview-<area>.png (git-ignored).
registry_rows.py WRITES the 34 registry rows (once; refuses if any ID is there).
convert_art.py   WRITES the 34 PNGs through scripts/anchor-art-frames.py --keep-geometry (--black-transparent for the
                 24-bit BMPs).
records.py       WRITES (with --write) records.json's 19 tiledata and 1 animdata records; the source of every value.
gen_layout.py    WRITES server/customizations/ClusterFCommunityArtLayout.cs (refuses while validate.py fails).
breaks.py        WRITES the red run's five breaks, and "restore" (byte copies, SHA-256 checked, no P237-BREAK left).
