cc-P18 read-only tools. Nothing here writes to a save or a world.

callsite_table.py  Run in D:\ShatteredLegacy. Lists every line using the account guild API at bb51fad (before cc-P18),
                   per file, reads and writes: the A1 table in notes/cc-P18-reset-stone-young-craftx.md section 1.1.
find_acct.py       For each ClusterFAccountPersistence.GetOrCreate(acct) site in the given files, prints the line that
                   defines acct, to show which character was in reach.
stone_spot.py      Standable z and statics for the tiles around the New Haven arrival tile, through cc-P15-tools/fit.py
                   (port of pinned Map.CanFit). Chose the Reset Stone's tile, 3501,2575,14.
redrun.py          The red runs' breaks (A and B), each aimed at one fact; `apply A|B` backs up and breaks, `restore`
                   restores and checks SHA-256. Its paths point at the session scratch folder used on 2026-09-30.
redrun2.py         F-1 red runs C and D (loads redrun.py for the machinery).
