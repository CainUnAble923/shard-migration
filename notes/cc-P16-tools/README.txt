cc-P16 read-only tools and their outputs. Nothing here writes to a save or a world.

camp_z.py        Part A 2: land z and GetAverageZ (port of pinned Map.cs:243-296) for every layout
                 component and NPC tile, statics on the tile, and a port of Map.CanSpawnMobile
                 (Map.cs:1137-1275, land and statics) for the NPC tiles. Reads the server's own client
                 files through design/mine-camp-tents/uorender.py. Output: camp_z.out.txt.
camp_items.py    Part A 4: every top-level Trammel item (decoded per pinned Item.Serialize,
                 Item.cs:816-1080) and mobile in x 3485-3525, y 2735-2765 of a COPY of a save, flagging
                 any on a layout tile. Run in a folder holding SerializedTypes.db, Items.*, Mobiles.*.
                 Outputs: items_test.out.txt (test save 2026-09-30 15:05), items_live.out.txt (live save
                 2026-09-29 13:50).
p17_collide.py   P17's 125 New Haven decoration entries against the camp tiles. Output: p17_collide.out.txt.
gen_layout.py    WRITES two files in D:\ShatteredLegacy: server/customizations/ClusterFMineCampLayout.cs
                 and server/tests/Misc/MineCampLayoutDesignCopy.cs, from design/mine-camp-tents/layout.json.
                 Re-run after any change to the design file.
