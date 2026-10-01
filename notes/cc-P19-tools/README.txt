cc-P19 tools and their outputs. Read-only unless marked WRITES.

office_z.py          Part A 1 and 2: for every layout component and the door, doorway and Registrar tiles, land z,
                     GetAverageZ, the statics on the tile, and a port of pinned Map.GetTopSurfaceZ(Point3D)
                     (Map.cs:491-565); then a walkability table with the props in place (Map.CanSpawnMobile port
                     from notes/cc-P16-tools/camp_z.py); then every static in the house box. Reads the server's
                     own client files through design/registrar-office/uorender.py. Output: office_z.out.txt.
props_tiledata.out.txt  tiledata name, height and flags of every prop id and the three door ids.
office_items.py      Part A 3, adapted from notes/cc-P16-tools/camp_items.py: every top-level Trammel item and mobile
                     in x 3448-3468, y 2590-2608 of a COPY of a save, flagging any on a layout, door or Registrar
                     tile. Run in a folder holding SerializedTypes.db, Items.*, Mobiles.*.
                     Outputs: items_test.out.txt (test save copy 2026-09-30 20:30), items_live.out.txt (live save
                     copy 2026-09-29 13:50).
gen_office_layout.py WRITES server/customizations/ClusterFRegistrarOfficeLayout.cs and
                     server/tests/Misc/RegistrarOfficeLayoutDesignCopy.cs in D:\ShatteredLegacy from
                     design/registrar-office/layout.json. Re-run after any change to the design file.
breaks.py            WRITES: the red-run breaks (A, B) and "restore", which puts byte copies back and checks
                     SHA-256 and that no P19-BREAK marker is left.
