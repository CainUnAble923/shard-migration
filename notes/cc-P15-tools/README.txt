cc-P15 read-only world tools. Nothing here writes to a save or a world.

nh_mobiles.py  Lists mobiles in a box on Trammel from a COPY of a ModernUO save (run in a folder holding
               SerializedTypes.db, Mobiles.idx, Mobiles.bin). Index entry: flag byte, u64 type hash,
               u32 serial, i64 created, i64 position, i32 length (33 bytes). Location is found by the
               Mobile.Serialize layout (pinned Mobile.cs:2297-2416): Point3D, then Body, Name, ... Map.
nhmap.py       Loads the client map1 / statics1 / tiledata / Cliloc through
               D:/ShatteredLegacy/design/mine-camp-tents/uorender.py.
fit.py         Port of pinned Map.CanFit (Projects/Server/Maps/Map.cs:925-1010) and GetAverageZ
               (:243-285), height 16, over the client map, statics and pinned's New Haven decoration
               items (Distribution/Data/Decoration/Trammel/*haven*.cfg). surfaces(x, y) lists the z's a
               mobile can stand at. Checked against 341 spawned or walking NPCs of the test world: all fit.
rend.py        Renders an area with NPCs marked and statics above a z cut hidden (go2).

Usage (from the folder with the save copy): python nh_mobiles.py > nh_mobiles.txt; then exec fit.py.
