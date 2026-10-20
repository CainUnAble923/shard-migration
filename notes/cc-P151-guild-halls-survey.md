# cc-P151: Survey of sites for the guilds' real halls (F-49)

Gold Golem, 2026-10-20. Read-only survey. **Nothing was placed, built, started or changed in any world.** No shard,
Docker or world command was run. Nothing player-facing changed, so there are no patch notes. `docs\` was not edited.

## How this was done (and what it could not see)

- **Map data:** the client map files in `D:\ShatteredLegacy\client-data\classic-client` (`map{0,1,3,4,5}LegacyMUL.uop`,
  `staidx*/statics*.mul`, `tiledata.mul`), read by a small reader (`cc-P151-tools/uomap.py`). It was spot-checked against
  the vseUOAware `inspect_map_coordinate` tool: Trammel 1415,3780 gives land 0x040A z0, statics 0x000B z0 and 0x05CF z32
  from both.
- **Pinned spawns:** this PC has no `D:\UO\ModernUO-pinned`, so pinned's `Distribution/Data` was fetched read-only from
  GitHub at the build pin `d4531cd94b739613155225c234900de9f47d2c88` (`docker/uo/Dockerfile:3`) into the scratchpad.
  The shard imports `post-uoml/**` and `shared/**` and never `uoml/**` (`ClusterFStockSpawnData.cs:17`), so the survey
  read only those two folders.
- **Building names:** from pinned `signs.cfg` (the `[SignGen` data) with names decoded from the client's compressed
  `Cliloc.enu`. The decoder is a Python port of pinned `Projects/Server/Client/BwtDecompress.cs`
  (`cc-P151-tools/bwt.py`). It decodes 123,489 strings with headers 2/1, and cliloc 1016093 reads "Court of Truth".
- **Buildings** were found as connected tiles under a roof or a static floor (`survey.py`). **Open plots** are
  rectangles where every tile is passable, dry land with no wall, roof, floor, impassable or taller-than-2 static, and
  the land z spread is 4 or less, kept 2 tiles clear of every pinned spawner (`survey.py`, `rect.py`). This is a
  heuristic, not the server's `CanFit`. Each design pass must still check its exact footprint in game.
- **Our own placements:** grepped every coordinate in `server/customizations` outside New Haven. Outside New Haven we
  place things only in Ter Mur: the Royal City gargoyle vendors and moongate (`ClusterFRoyalCitySeeder`), the Artificers'
  Guildmaster (`ClusterFInstitutionSeeder`), and the Fountain of Fortune and its steps at 1121,957 (not in Royal City).
  The Cleanup Officer and Clean Up barrels are placed only by `[ClusterFPlaceCleanUp` at the caller's tile, and P33
  placed nothing (`notes/cc-P33-clean-up-britannia.md:4`).
- **Not verified (no world save was read):** player houses, items staff placed by hand, and whether `[DecorateMag`
  (pinned's ruined-Magincia decoration, a separate command from `[Decorate`) was ever run. Inside the town regions
  player houses cannot exist, because pinned `GuardedRegion.AllowHousing` returns false (`GuardedRegion.cs:151`). Of the
  picks, only the Dojo's north field (outside Zento's region) and the Papua plot (one tile outside Papua's region) could
  have a player house nearby.
- **Travel network:** none exists yet. The only mention is a roadmap line, "guild travel networks"
  (`D:\ShatteredLegacy\roadmap.md:632`). The Staff Hub Travel tab is staff-only. So every row below says "no stop yet",
  and each hall's travel-network stop has to be new.
- **Distances** are in tiles, the larger of the x and y difference. A moongate across water is named but marked "none
  in town".

## Summary (one row per F-49 row)

| # | Guild | Town | Facet | Pick | Coordinates (x1,y1 to x2,y2) | Conflicts | Travel |
|---|---|---|---|---|---|---|---|
| 1 | The League (HQ) | Britain, Castle British | Trammel | Reuse the castle keep (Castle Britannia) | 1320,1586 to 1366,1665, z30 floors | none inside; Order guards at the gate 1400,1623/1628; Lord's Arms armourer 1362,1574 | Britain gate 1336,1997 (372); First Bank of Britain 1425,1690 (82) |
| 2 | Warriors' Brotherhood | Jhelom | Trammel | Reuse "Brothers in Arms" (Weapons Guild sign) | 1352,3696 to 1376,3720 (25x25) | none inside; Baker 1364,3732; Dueling Pit and hirelings next door | Jhelom gate 1499,3771 (135); Jhelom bank 1317,3773 (65) |
| 3 | Arcane Society | Moonglow | Trammel | Reuse The Lycaeum | 4278,915 to 4336,1017 (complex) | none | Moonglow gate 4467,1283 (317); bank 4471,1156 (190) |
| 4 | Healers' Covenant | Empath Abbey (Yew) | Trammel | Reuse the Abbey church (centre of the Empath Abbey complex) | 623,816 to 647,856 | none inside; same complex: Yew innkeeper 610,810 and Yew bank 652,820 | Yew gate 771,752 (136); bank in the Abbey's east wing 652,820 (17) |
| 5 | Rangers' League | Skara Brae | Trammel | Reuse Counselor's Guild | 608,2112 to 632,2144 (25x33) | none inside; Town crier 603,2141; stock Rangers' Guild (RangerGuildmaster) 552,2136 | Skara gate 643,2067 (61); bank 587,2146 (33) |
| 6 | Miners' Compact | Minoc | Trammel | Reuse Minoc Town Hall | 2416,520 to 2440,536 (25x17) | none | Minoc gate 2701,692 (273); Bank of Minoc 2503,552 (75) |
| 7 | Society of Smiths | Serpent's Hold | Trammel | New hall in the open court east of the stock forge | 3018,3372 to 3045,3399 (28x28, z15) | stock Blacksmith and BlacksmithGuildmaster 3007,3408 (next door, by design); Provisioner 3008,3389 | no gate in town; bank 2880,3472 (151) |
| 8 | Tinkers' Union | Vesper | Trammel | Reuse The Musician's Hall (Bardic Guild sign, no bard) | 2880,736 to 2904,752 (25x17) | none | no gate in Vesper (Minoc 2701,692 is 191); Mint of Vesper 2881,684 (60) |
| 9 | Thieves' Den | Buccaneer's Den | **Felucca** (judgment call) | Reuse Buccaneer's Bath | 2655,2072 to 2681,2096 | none inside; stock ThiefGuildmaster in Pirate's Den 2648,2184 | Felucca gate 2711,2234 (150); bank 2731,2192 (108). Trammel has no gate here |
| 10 | Twin Paths Dojo | Zento (Tokuno) | Tokuno | New hall in the north field outside the town wall | 744,1170 to 765,1191 (22x22, z25) | none (stock Musha-Shugyo Dojo is in use, see details) | Makoto-Jima gate 802,1204 (48); Zento bank 729,1249 (69) |
| 11 | Keepers of the Last Door | Umbra (Malas) | Malas | Reuse the empty building on the west side | 1983,1351 to 1999,1365 (17x15) | none inside; Blacksmith 1977,1365 | Umbra gate 1997,1386 (28); Umbra Bank 2048,1343 (57) |
| 12 | Foresters' Union | Yew | Trammel | Reuse Yew Mill | 544,808 to 567,831 (24x24) | none | Yew gate 771,752 (216); bank 652,820 (97) |
| 13 | Tailors' Circle | Nujel'm | Trammel | Reuse Counselor's Guild | 3760,1184 to 3783,1207 (24x24) | none inside; Jeweler 3778,1172; tavern 3769,1218 | no gate in Nujel'm; Bank of Nujelm 3764,1317 (122) |
| 14 | Maritime Brotherhood | Ocllo | **Felucca** (judgment call) | Reuse the empty building in north Ocllo | 3600,2496 to 3616,2512 (17x17) | none | no Ocllo gate on either facet; Felucca Bank of Ocllo 3695,2511 (87) |
| 15 | Merchants' Exchange | Magincia | Trammel | New hall on the open town centre | 3704,2170 to 3725,2191 (22x22, z20) | none inside; town crier 3721,2161, innkeeper 3699,2163; `[DecorateMag` rubble unverified | Magincia gate 3563,2139 (151); Bank of New Magincia 3734,2149 (31) |
| 16 | Bards' Consortium | Britain | Trammel | Reuse The King's Men Theater | 1440,1576 to 1460,1600 (21x25) | none inside; stock Conservatory of Music (Bard, BardGuildmaster) next door | Britain gate 1336,1997 (409); First Bank 1425,1690 (102) |
| 17 | Artificers' Order | Royal City (Ter Mur) | Ter Mur | New hall on the plaza where the post stands | 790,3424 to 803,3441 (14x18, z-10) | our Artificers' Guildmaster stands here at 797,3431; gargoyle Jeweler 779,3431 and Farmers 794,3446 | Royal City gate 850,3525 (93); bank 833,3439 (37) |
| 18 | Order of the Alembic | Papua (Lost Lands) | Trammel | New hall at the swamp's west edge (judgment call) | 5638,3240 to 5651,3253 (14x14, z-3..3) | none | no gate in the Lost Lands; Ye Olde Loan & Savings 5669,3131 (115) |
| 19 | Custodians (Clean Up Britannia) | Britain | Trammel | Reuse the empty brick hall beside the bank | 1447,1701 to 1474,1716 (about 26x15) | none inside; Butcher 1449,1723 | Britain gate 1336,1997 (288); First Bank 1425,1690 (35) |

Of the 19 picks: 14 reuse a stock building and 5 place a new hall (Smiths, Dojo, Merchants, Artificers, Alembic).
Three sit off Trammel because their town is not on it: Zento (Tokuno), Umbra (Malas) and Royal City (Ter Mur). Two
are proposed for Felucca (Thieves' Den, Maritime), and those two are questions below.

## Details per guild

Each guild lists up to three candidates, then its conflicts, travel and pick. "Felucca" says whether the same spot
exists there: the Trammel and Felucca maps are identical in most towns, and every Felucca difference is counted.

### 1. The League (HQ): Britain, Castle British grounds (Trammel)

- **Facet:** Trammel. Felucca has the same castle (0 tiles differ in the keep).
- **Candidates:**
  1. **Reuse the castle keep** (Castle Britannia, sign 1400,1622): the inner keep, 1320,1586 to 1366,1665, floors at
     z30, about 47x80 across many rooms. Pinned spawns nothing inside it, and pinned has no Lord British NPC.
  2. **New hall in the east courtyard**, inside the walls between the keep and the east wing: 1362,1584 to 1381,1607
     (20x24, flat z30, 0 blocked tiles).
  3. **New hall in the south-east courtyard:** 1362,1664 to 1383,1681 (22x18, flat z30, 0 blocked). The west lawn,
     1308,1576 to 1323,1595 (16x20) and 1308,1644 to 1323,1669 (16x26), is also open, but it is narrow.
- **Conflicts:** Order guards at the castle gate (1400,1623 and 1400,1628, `TownsPeople.json`). The Lord's Arms armourer
  (1362,1574) and a tailor (1388,1588) trade inside the walls near candidate 2. There are no houses (town region).
- **Room for an HQ:** yes. The grounds hold two clean 20x24 and 22x18 courtyards, and the keep itself is unused.
- **League field office today:** New Haven, Trammel. The League Registrar stands at 3459,2601,18
  (`ClusterFNewHavenSeeder.cs:71`), with props from `ClusterFRegistrarOfficeSeeder`, and the guild gump labels it
  "Field Office, New Haven" (`ClusterFGuildSystem.cs:913`). It stays as the chapter.
- **Travel:** Britain moongate 1336,1997 is far south (372). First Bank of Britain 1425,1690 (82). No travel stop yet.
- **Pick:** reuse the keep. It is the castle itself, it is unused, and it needs no placed building. If a hall of the
  League's own is wanted, candidate 2 is the fallback. This is a question for Chase below.

### 2. Warriors' Brotherhood: Jhelom (Trammel)

- **Facet:** Trammel. Felucca matches (0 tiles differ).
- **Candidates:**
  1. **Brothers in Arms**, Weapons Guild sign 1368,3713: 1352,3696 to 1376,3720 (25x25), no spawner inside.
  2. **Counselor's Guild**, sign 1425,3704: 1408,3696 to 1432,3720 (25x25), no spawner inside.
  3. **Hand of Death / Jhelom Armory**, Armourers' Guild sign 1440,3864: 1424,3864 to 1448,3888 (25x25), no spawner
     inside.
- **Conflicts:** the "First Defense" blacksmith (Blacksmith and BlacksmithGuildmaster) is next door at 1384,3696. The
  Jhelom Dueling Pit (sign 1376,3752) holds pinned hireling spawns. A Baker spawner is at 1364,3732. Jhelom has no stock
  WarriorGuildmaster.
- **Travel:** Jhelom moongate 1499,3771 (135, east side of the island). Jhelom Bank and Jeweler 1317,3773 (65).
- **Pick:** Brothers in Arms. It is a weapons guild building, it is empty, and it stands by the Dueling Pit.

### 3. Arcane Society: Moonglow (Trammel)

- **Facet:** Trammel. Felucca has the Lycaeum, with 105 tiles differing across the complex.
- **Candidates:**
  1. **The Lycaeum** (sign 4308,1012): 4278,915 to 4336,1017. It is a complex of halls (two 18x32 wings at 4286,948 and
     4318,948, plus smaller halls) round a brick court at 4304,980 to 4323,995. There are no spawners in it.
  2. **Moonglow Academy of Arts** (sign 4528,1069): 4520,1056 to 4536,1072 (17x17), no spawners.
  3. **Counselor's Guild by the bank** (sign 4477,1130): 4468,1118 to 4481,1134 (14x17), no spawners.
- **Conflicts:** the Encyclopedia Magicka (Mages' Guild sign 4548,873; 4534,848 to 4558,872) holds the stock
  MageGuildmaster, so it was not used.
- **Travel:** Moonglow moongate 4467,1283 is far from the Lycaeum (317). First Bank of Moonglow 4471,1156 (190).
  Candidate 3 is 25 from the bank.
- **Pick:** the Lycaeum. It is the iconic seat of magic learning, it is unused, and it is big enough for shop, trial and
  requisitions. Its distance from the gate and bank is the cost; a travel stop at the Lycaeum solves it.

### 4. Healers' Covenant: Empath Abbey, by Yew (Trammel)

- **Facet:** Trammel. Felucca matches (10 tiles differ).
- **Where the Abbey is:** the sign "Empath Abbey" is at 636,856. The walled complex is 600,808 to 671,855, with "Ye Olde
  Winery" south of it (sign 624,886) and vine rows at 593,841 to 616,861.
- **Candidates:**
  1. **The Abbey church**, the cross-shaped centre of the complex: 623,816 to 647,856. No spawner inside.
  2. **Ye Olde Winery:** 608,872 to 623,895 (16x24), no spawner.
  3. **The chapel south of Yew**, 640,1080 to 656,1096 (17x17). It already holds the stock Healer and
     HealerGuildmaster (643,1083), so it is a share, not a free site.
- **Conflicts:** the complex's wings hold the Yew InnKeeper (610,810) and the Yew Banker and Minter (652,820). The
  church between them has none. The Healer of Yew (528,960) is a separate building.
- **Travel:** Yew moongate 771,752 (136). The bank is in the Abbey's own east wing (17).
- **Pick:** the Abbey church. It is the named Abbey, it is empty, and the bank is in the same complex.

### 5. Rangers' League: Skara Brae (Trammel)

- **Facet:** Trammel. Felucca matches (0 tiles differ).
- **Candidates:**
  1. **Counselor's Guild** (signs 617,2144 and 624,2112): 608,2112 to 632,2144 (25x33), no spawner.
  2. **Skara Brae Town Hall** (sign 576,2209): 544,2200 to 576,2224 (33x25), no spawner inside; a Provisioner spawner
     stands at its corner, 578,2227.
  3. **The stock Rangers' Guild** (sign 576,2145): 552,2136 to 576,2160 (25x25). It holds pinned's RangerGuildmaster
     (562,2148), so it would be shared.
- **Conflicts:** a town crier at 603,2141; the RangerGuildmaster above.
- **Travel:** Skara Brae moongate 643,2067 (61). Bank of Skara Brae 587,2146 (33).
- **Pick:** Counselor's Guild. It is the largest free building, it is beside the bank, and it is nearest the gate.
  Sharing the stock Rangers' Guild is a question for Chase.

### 6. Miners' Compact: Minoc (Trammel)

- **Facet:** Trammel. Felucca has the Town Hall, with 39 tiles differing.
- **Candidates:**
  1. **Minoc Town Hall** (sign 2428,536): 2416,520 to 2440,536 (25x17), no spawner.
  2. **New hall on the plain south-east of town**, toward Minoc's south: 2532,612 to 2557,630 (26x19, z0, 10 of 494
     tiles blocked by trees). The open ground runs on east to 2719,591; for example 2644,546 to 2661,563 (18x18, z0) is
     nearer the moongate.
  3. **The Matewan** (Miners' Guild sign 2459,492): 2443,475 to 2467,499 (25x25). It holds pinned's MinerGuildmaster
     (2455,487), so it would be shared.
- **Conflicts:** none at candidate 1.
- **Travel:** Minoc moongate 2701,692 is far east (273 from the Town Hall; 148 from 2644,546). Bank of Minoc 2503,552
  (75).
- **Pick:** Minoc Town Hall. It is a free stock building in the middle of town, near the bank and the forge.

### 7. Society of Smiths: Serpent's Hold (Trammel)

- **Facet:** Trammel. Felucca matches (4 tiles differ).
- **Candidates:**
  1. **New hall in the open court east of the forge:** 3018,3372 to 3045,3399 (28x28, flat z15, 1 tile blocked).
  2. **New hall in the south-east court:** 3026,3434 to 3045,3457 (20x24, z15).
  3. **New hall in the north court:** 2970,3360 to 2987,3373 (18x14, z15).
- **Why no reuse:** the free roofed structures found inside the walls are small. The largest, 2878,3406 to 2897,3425
  (20x20, at z35, half of it floored), looks like the west tower; its interior was not checked. The stock forge
  (3000,3400 to 3016,3416) holds pinned's Blacksmith and BlacksmithGuildmaster (3007,3408).
- **Conflicts:** the stock forge is next door to candidate 1, which suits a smiths' hall. A Provisioner (3008,3389) and
  a Bowyer (3051,3367) are nearby. The "Supplies" sign (3016,3386) hangs at the court's edge.
- **Travel:** no moongate on the island. Bank 2880,3472 (151). The hall needs a travel stop more than most.
- **Pick:** candidate 1. It is the largest flat court, and it sits beside the forge.

### 8. Tinkers' Union: Vesper (Trammel)

- **Facet:** Trammel. Felucca matches (0 tiles differ).
- **Candidates:**
  1. **The Musician's Hall** (Bardic Guild sign 2904,737): 2880,736 to 2904,752 (25x17), no spawner.
  2. **The Colored Canvas** (sign 2905,720): 2896,704 to 2912,720 (17x17), no spawner.
  3. **Counselor's Guild** (sign 2848,929): 2832,928 to 2856,960 (25x33), no spawner. An unnamed 25x42 building at
     2959,721 to 2983,762 is also free.
- **Conflicts:** none at the picks. The stock TinkerGuildmaster is at "The Gadget's Corner" (2888,784 to 2904,800),
  about 50 tiles south.
- **Travel:** Vesper is not on the Trammel moongate list; the nearest gate is Minoc 2701,692 (191). The Mint of Vesper
  2881,684 (60).
- **Pick:** The Musician's Hall. It is free, it is the right size, and it sits between the bank and the stock tinker.

### 9. Thieves' Den: Buccaneer's Den (Felucca proposed)

- **Facet: Felucca is proposed, and it is a judgment call.** Both facets have the same town (3 tiles differ at the
  pick). Felucca has a public moongate at Buccaneer's Den (2711,2234); Trammel does not, and its gate list has New Haven
  instead (`PublicMoongate.cs:194` and `:213`). Buccaneer's Den is the pirate and red town.
- **Candidates:**
  1. **Buccaneer's Bath** (sign 2666,2096): 2655,2072 to 2681,2096, no spawner on either facet.
  2. **New hall:** 2714,2152 to 2731,2167 (18x16) by the healer.
  3. **New hall:** 2690,2224 to 2703,2237 (14x14) near the waterfront.
- **Conflicts:** pinned's ThiefGuildmaster is in "Pirate's Den" (2648,2184 to 2664,2208), a separate building.
- **Travel:** on Felucca, the gate 2711,2234 (150) and the bank 2731,2192 (108). On Trammel there is no gate, so a
  travel stop would be the only way in apart from boats.
- **Pick:** Buccaneer's Bath, on Felucca. If Trammel is kept, use the same building there.

### 10. Twin Paths Dojo: Zento, Tokuno (Tokuno)

- **Facet:** Tokuno, which is the only facet with Zento.
- **Candidates:**
  1. **New hall in the north field**, just outside the town wall (Zento's region begins at y1192): 744,1170 to 765,1191
     (22x22, flat z25, 9 of 484 tiles blocked by trees).
  2. **The stock "Iroha Armorer and Musha-Shugyo Dojo"** (sign 768,1298): 735,1296 to 789,1316 (55x21). It is a real
     dojo, but pinned trades in it: three Armorer spawners, an Armorer and Weaponsmith pair, and a Bowyer (749,1303 and
     others). It would be a share.
  3. **New hall in the plaza by the bank:** 746,1248 to 759,1259 (14x12, z25), small.
- **Conflicts:** none at candidate 1. It is outside the town region, so a player house could be near it (not checked).
- **Travel:** Makoto-Jima moongate 802,1204 (48). Zento bank 729,1249 (69).
- **Pick:** candidate 1, a new hall by the gate. Sharing the stock dojo is a question for Chase.

### 11. Keepers of the Last Door: Umbra, Malas (Malas)

- **Facet:** Malas, which is the only facet with Umbra.
- **Candidates:**
  1. **Reuse the empty building on the west side:** 1983,1351 to 1999,1365 (17x15), floored, no spawner.
  2. **New hall on the open dirt just north of it:** 1988,1332 to 2005,1349 (18x18, z-90..-85, 9 tiles blocked).
  3. **New hall in the south-east open ground:** 2104,1413 to 2119,1428 (16x16, flat z-90).
- **Conflicts:** the Blacksmith and BlacksmithGuildmaster at 1977,1365 are next door. The Necromancer Amphitheater (sign
  2038,1385) is in use by the Mage, Alchemist and MageGuildmaster spawner (2023,1379) and the Herbalist (2025,1387).
- **Travel:** Umbra moongate 1997,1386 (28). Umbra Bank 2048,1343 (57).
- **Pick:** candidate 1. It is a free stock building, the nearest to the gate.

### 12. Foresters' Union: Yew (Trammel)

- **Facet:** Trammel. Felucca matches (0 tiles differ).
- **Candidates:**
  1. **Yew Mill** (sign 547,832): 544,808 to 567,831 (24x24), no spawner.
  2. **The large unnamed building north-west of the mill:** 496,768 to 538,807 (43x40), no spawner.
  3. **The unnamed building south of the Abbey:** 640,936 to 656,952 (17x17), no spawner.
- **Conflicts:** none. The Mill is a separate building about 80 tiles west of the Abbey church (row 4), so the two Yew
  halls are apart.
- **Travel:** Yew moongate 771,752 (216). The bank in the Abbey 652,820 (97).
- **Pick:** Yew Mill. It is a timber and mill building, it is free, and it is near the Abbey without sharing it.

### 13. Tailors' Circle: Nujel'm (Trammel)

- **Facet:** Trammel. Felucca matches (0 tiles differ).
- **Candidates:**
  1. **Counselor's Guild** (sign 3776,1196): 3760,1184 to 3783,1207 (24x24), no spawner.
  2. **Nujel'm Theater** (sign 3753,1240): 3728,1216 to 3751,1239 (24x24), no spawner.
  3. **Unnamed building in the north:** 3768,1119 to 3792,1141 (25x23), no spawner.
- **Conflicts:** a Jeweler at 3778,1172 and the tavern at 3769,1218 are nearby. The stock TailorGuildmaster is at "Tailor
  of the Isle" (3760,1248 to 3783,1271).
- **Travel:** no moongate on Nujel'm. Bank of Nujelm 3764,1317 (122).
- **Pick:** Counselor's Guild. It is free and in the shop quarter, which leaves the Theater for later.

### 14. Maritime Brotherhood: Ocllo (Felucca proposed)

- **Facet: Felucca is proposed, and it is a judgment call.** On Trammel, Ocllo is **Old Haven**: the old Haven town,
  abandoned. Pinned spawns undead there (Zombie, Skeleton, spellbinder spawners in `post-uoml/trammel/Outdoors.json`) and
  no vendors. Our own `ClusterFOldHavenSeeder` adds mage spawners, Vorlak the Impaler and Drelgor there; its area is
  X 3520 to 3680, Y 2420 to 2600 (`ClusterFOldHavenSeeder.cs:296`). Felucca's Ocllo is the living town: bank, healer,
  tailor, smith, and the bard guildmaster.
- **Candidates:**
  1. **Felucca: the empty building in north Ocllo**, 3600,2496 to 3616,2512 (17x17), no spawner.
  2. **Felucca: the empty building at 3656,2495 to 3672,2512** (17x18), no spawner. The "First Academy of Music"
     (3672,2472 to 3696,2480) is also free.
  3. **Trammel: the same buildings in Old Haven.** They are free, but they lie inside our Old Haven seeding area and
     among pinned's undead. The Old Haven docks (signs "Mapmakers of Haven" 3634,2640 and "The Albatross Bar and Grill"
     3665,2657) are south of our area, but pinned Skeleton spawners stand there (3635,2625 and 3651,2627).
- **Conflicts:** none at the Felucca picks. On Trammel, the Old Haven content above.
- **Travel:** neither facet has an Ocllo gate. On Felucca, the Bank of Ocllo is 3695,2511 (87). On Trammel, the New
  Haven gate 3450,2677 is on the same island (173).
- **Pick:** candidate 1 on Felucca. Trammel has no living Ocllo, and putting the hall in Old Haven would fight our own
  tutorial content. This is a question for Chase.

### 15. Merchants' Exchange: Magincia (Trammel)

- **Facet:** Trammel. Felucca matches (0 tiles differ).
- **What the map shows:** in the client map, the centre of Magincia is open grass on both facets. Pinned's signs still
  hang there and its vendors stand in the open (innkeeper 3699,2163; baker 3683,2171; town crier 3721,2161). The south
  waterfront has buildings. If `[DecorateMag` was run, it would add ruin rubble here (`DecorateMag.cs:36`). That is
  unverified, so check in game before the design pass.
- **Candidates:**
  1. **New hall on the centre near the bank:** 3704,2170 to 3725,2191 (22x22, flat z20, 0 blocked).
  2. **New hall:** 3680,2178 to 3701,2199 (22x22, flat z20, 0 blocked).
  3. **New hall by the stock Merchants' Guild:** 3726,2228 to 3749,2251 (24x24, flat z20, 0 blocked). The tiny stock
     Merchants' Guild (3704,2244 to 3709,2252) holds pinned's MerchantGuildmaster.
- **Conflicts:** none inside candidate 1. The town crier and innkeeper stand just outside it (2 to 9 tiles). There is no
  New Magincia housing or bazaar port of ours (`Services/New Magincia` holds only `Yeast.cs`).
- **Travel:** Magincia moongate 3563,2139 (151). Bank of New Magincia 3734,2149 (31).
- **Pick:** candidate 1. It is flat, open, and 31 tiles from the bank.

### 16. Bards' Consortium: Britain (Trammel)

- **Facet:** Trammel. Felucca matches (0 tiles differ).
- **Candidates:**
  1. **The King's Men Theater** (signs 1441,1584 and 1454,1600): 1440,1576 to 1460,1600 (21x25), no spawner.
  2. **Counselor's Guild, north Britain** (sign 1505,1528): 1496,1512 to 1512,1528 (17x17), no spawner.
  3. **Unnamed building, east Britain:** 1560,1736 to 1584,1752 (25x17), no spawner.
- **Conflicts:** Lord British's Conservatory of Music (1434,1546 to 1476,1568) is next door, with pinned's Bard and
  BardGuildmaster (1455,1557). That suits the theatre. The Saw Horse carpenter (1430,1597), a tanner (1431,1612), a
  bowyer (1470,1578) and the Healer of Britain (1471,1611) are nearby.
- **Apart from the League:** the theatre is across the moat, east of the castle. It is about 80 tiles from the east
  courtyard and about 105 from the keep, and it is a different building and district. If more distance is wanted,
  candidate 3 is about 230 tiles from the keep.
- **Travel:** Britain moongate 1336,1997 (409). First Bank of Britain 1425,1690 (102).
- **Pick:** The King's Men Theater.

### 17. Artificers' Order: Royal City, Ter Mur (Ter Mur)

- **Facet:** Ter Mur, which is the only facet with Royal City.
- **The existing post:** our `ArtificersGuildmaster` at Ter Mur 797,3431,-10, facing west, placed on every world load by
  `ClusterFInstitutionSeeder.cs:98` to `:107` and listed in `GuildLocations` as not Seeded
  (`ClusterFGuildStarterPath.cs:229`). The map shows that tile on an open stone plaza (790,3424 to 803,3441, flat z-10),
  west of the gargoyle jeweler's shop. **It cannot serve as the real hall as is.** It is one NPC standing outdoors,
  with no room for the full shop, requisitions or a trial.
- **Candidates:**
  1. **New hall on the post's own plaza:** 790,3424 to 803,3441 (14x18, flat z-10, 0 blocked). The guildmaster would
     move inside it.
  2. **Reuse the unused building north of the bank:** 809,3344 to 841,3373 (33x30, floors z-20), no spawner.
  3. **Reuse the unused building east:** 892,3389 to 925,3406 (34x18), no spawner.
- **Conflicts:** our Royal City seeder places the gargoyle Jeweler at 779,3431 and Farmers at 794,3446 and 799,3446,
  matching pinned `post-uoml/termur/Vendors.json`. The plaza is a walkway between them.
- **Travel:** Royal City moongate 850,3525 (93). Royal City bank 833,3439 (37).
- **Pick:** candidate 1. Players already find the Artificers there; a 14x18 hall is tight, so if it is too small,
  candidate 2 is the larger reuse. This is a question for Chase.

### 18. Order of the Alembic: Papua, Lost Lands (Trammel)

- **Facet:** Trammel (Lost Lands). Felucca matches (0 tiles differ).
- **What the map shows:** Papua is swamp. No plot passes the strict test (flat within 4 and fully clear), and every
  stock building holds a pinned vendor.
- **Candidates:**
  1. **New hall at the west edge:** 5638,3240 to 5651,3253 (14x14, z-3..3, 0 blocked). It needs a floor to level the
     6-z spread.
  2. **New hall at the south edge:** 5698,3308 to 5711,3321 (14x14, z-3..3, 0 blocked).
  3. **Share "Tricks of the Trade" and "The Reagent Shoppe"** (5723,3182 to 5762,3209). This is Papua's magic and
     alchemy shop, holding pinned's Mage, Alchemist and MageGuildmaster (5731,3192) and the Herbalist and Alchemist
     (5714,3202). It suits the swamp-herbs theme, but it is in use.
- **Conflicts:** none at candidates 1 and 2. Candidate 1 is one tile outside Papua's region, so a player house could be
  near it (not checked).
- **Travel:** the Lost Lands have no public moongate. Ye Olde Loan & Savings 5669,3131 (115 from candidate 1).
- **Pick:** candidate 1, a new hall. Sharing the alchemy shop is a question for Chase.

### 19. Custodians (Clean Up Britannia): Britain (Trammel)

- **Facet:** Trammel. **Felucca does not match:** a different building stands there (379 tiles differ).
- **Candidates:**
  1. **The empty brick hall beside the bank:** about 1447,1701 to 1474,1716 (26x15; brick, carpet, marble columns, slate
     roof), no sign, no spawner.
  2. **Artists' Guild** (sign 1444,1670): 1440,1660 to 1455,1671 (16x12), no spawner, 25 tiles from the bank.
  3. **Counselor's Guild, east Britain** (sign 1634,1673), by the east bank (1650,1608). Its size was not measured.
- **Conflicts:** a Butcher at 1449,1723. No Cleanup Officer is placed anywhere by the server; it is placed only by
  command, and whether staff placed one in Britain is unverified.
- **Apart from the Bards and the League:** it is south of both, by the First Bank of Britain.
- **Travel:** Britain moongate 1336,1997 (288). First Bank of Britain 1425,1690 (35).
- **Pick:** candidate 1. It is the biggest free building next to the bank, which suits a trade-in service.

## Decisions for Chase

1. **League HQ:** reuse Castle British's keep (the castle itself), or place a new League hall in the castle's east
   courtyard (1362,1584 to 1381,1607)?
2. **Thieves' Den facet:** Felucca (Buccaneer's Den has a moongate there, and it is the pirate and red town) or
   Trammel (no gate; it needs a travel stop)?
3. **Maritime Brotherhood facet:** Felucca Ocllo (a living town), or Trammel, where Ocllo is the abandoned Old Haven
   full of our own tutorial and undead content? Or move the Maritime hall to another port on Trammel?
4. **Rangers' League:** the free Counselor's Guild by the bank, or share the stock Rangers' Guild with pinned's
   RangerGuildmaster?
5. **Twin Paths Dojo:** a new hall by the Makoto-Jima gate, or share the stock Musha-Shugyo Dojo with pinned's
   armourers?
6. **Artificers' Order:** a new 14x18 hall on the plaza where the post already stands, or reuse the larger free building
   north of the bank (809,3344 to 841,3373)?
7. **Order of the Alembic:** a new hall on a swamp-edge plot, or share Papua's stock magic and alchemy shop?

## Files

- `notes/cc-P151-tools/`: the read-only scripts that produced every coordinate above. They read the client files and a
  copy of pinned `Distribution/Data` placed beside them in `../muo` (fetched at `d4531cd94`), and `bwt.py` writes the
  decoded cliloc that `survey.py` reads from `../out/cliloc.pkl`.
  - `uomap.py`: map, statics and tiledata reader.
  - `bwt.py`: cliloc decoder.
  - `survey.py`: per town, the buildings, signs, open plots and spawners.
  - `ascii.py`: top-down tile maps.
  - `rect.py`: checks one rectangle.
  - `final.py`: travel distances and the Felucca comparison.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`. Neither repo was blocked on
the first run. The docs repo listed this note and the six `cc-P151-tools/*.py` files as pending.

```
Repo Result
---- ------
code clean
docs dry run
```

P151 DONE
