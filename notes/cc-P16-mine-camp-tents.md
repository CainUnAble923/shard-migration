# cc-P16: mine camp tents for the Miners' Compact Liaison and Survey Archivist

Date: 2026-09-30. Agent: Claude Code. Pinned ModernUO `7c9215d97`. Built in `D:\ShatteredLegacy`, **not committed**.
No world was changed: nothing placed, moved or removed on live or test; no shard deployed, restarted or recreated.
`sl-modernuo:latest` was not moved (`16b0f49e6828` before and after). Image: `sl-modernuo:cc-p16-minecamp` = `77bb7dabdc94`.

**Gate before starting.** `git --no-optional-locks status` in `D:\ShatteredLegacy` at `897e7ae`: clean. P15 is committed
(`99d5273`), P17 (`bb51fad`), and P18 after it (`88d5153`, `897e7ae`). P15 did not change which NPC type represents the
Miners' Compact: `GuildLocations` maps `mining` to `MinersCompactLiaison`, so that is the type moved.

Read-only tools and their raw outputs: `notes/cc-P16-tools/` (README there). Saves were read from copies taken
2026-09-30: test `Saves-test` (15:05) and live `Saves` (2026-09-29 13:50; live may have moved on since).

> **WARNING: `D:\ShatteredLegacy` HEAD (`5a8b67f`, "Shard work, 2026-09-30 15:27") holds this task's files with red run
> B's two deliberate breaks in them, and it appears to be pushed** (`git status -sb`: `main...origin/main`, nothing ahead).
> The commit ran while red run B was in progress, so it captured `ClusterFMineCampLayout.cs` with the crate on the
> Liaison's tile and `ClusterFMineCampSeeder.cs` with a line that **creates NPCs** in `[ClusterFMoveMineCampNpcs`. Both
> lines carry the marker `// P16-BREAK`. At that commit the gate fails (3 tests; section 6, red B): **do not deploy it.**
> **The working tree is correct**: restored byte-identical to the green sources, no marker left, and the final build of it
> passed 323. The fix is to commit the working tree as it is now; the two files show as modified, and their diff is
> exactly the removal of those two lines. I did not commit (brief). The same 15:27 run committed `notes/cc-P16-tools/` in
> this repo, before this note existed.

> **Headlines**
>
> 1. **Built:** two tent addons from the design file, `[ClusterFSeedMineCamp [status|dryrun]`,
>    `[ClusterFMoveMineCampNpcs [dryrun]`, and the two NPCs' fresh-world tiles moved to the tent openings, facing East.
>    **323 tests pass** (5 new). Every new fact was watched red on a break of its own (section 6).
> 2. **Part A found no stop condition.** The worst tent z is off by exactly 2 (the Miners' tent's south wall), at the
>    limit, not over it. Map files are byte-identical between host, test container and live container. Nothing is on
>    any of the 45 tiles, on the test or the live save, and none of P17's 125 entries is within 135 tiles.
> 3. **The brief's "within 15 tiles" holds for the Liaison only.** The Archivist's new tile is **20** tiles from her
>    old one (dx 20, dy 7). With the coordinate change alone, world load would have placed a **second Archivist** on
>    every world that has one (test does). The seeder now takes the old tile too (`wasAt`), as P17 did; a fact proves it.
> 4. **Live had no Survey Archivist** in the 2026-09-29 save (test has one). So the next live start on a new image will
>    **create** her, and after this change it creates her at the tent opening, not at the old spot. Section 4.3.
> 5. **The layout ships as a generated C# table.** The design file cannot reach the test container without a Dockerfile
>    change, which is out of scope; the test compares the table with a verbatim, hash-checked copy (section 3.1).

---

## 1. Part A: facts

### 1.1 Addons, components and uneven ground (A1)

- `BaseAddon.AddComponent(c, x, y, z)` stores the offset and moves the component to addon location + offset
  (pinned `Projects/UOContent/Items/Addons/BaseAddon.cs:134-146`). `OnLocationChange` and `OnMapChange` re-place every
  component at its own offset (`:241-265`). So **each component keeps its own z offset**; nothing flattens it.
- `CouldFit` (`:148-204`) checks each component with `Map.CanFit` and **also requires a house** (`CheckHouse`, `:164`,
  `:206-211`: `house != null`). So outside a house it always refuses. **But nothing on the placement path calls it.**
  It is called only by deeds (`BaseAddonDeed.cs:87`, `BaseAddonContainerDeed.cs:124`), the flip attribute
  (`FlippableAddonAttribute.cs:63`) and houses (`BaseHouse.cs:1074`). `Item.MoveToWorld` runs no fit check. An addon
  placed by a seeder on uneven ground is therefore not refused, and its components sit at exactly the given z.
- Components: `AddonComponent(itemID)` sets `Movable = false` (`AddonComponent.cs:100-104`), so `Decays` is false
  (`Projects/Server/Items/Item.cs:331`: `Movable && Visible && Spawner == null`); the addon itself is invisible and not
  movable (`BaseAddon.cs:27-33`). Double-click calls `OnComponentUsed`, empty in `BaseAddon` (`:237-239`). `Deed` is
  null (`:37`), and `OnChop` does anything only inside a house its chopper owns (`:92-132`). Light sources (brazier,
  candle) get their light from `ApplyLightTo` (`AddonComponent.cs:103`, `:190`).

### 1.2 Z table (A2)

Land z is `Map.Tiles.GetLandTile(x, y).Z`; average z is `Map.GetAverageZ` (pinned `Projects/Server/Maps/Map.cs:237-285`,
`FloorAverage` `:286-296`), ported in `camp_z.py`. **No tile has a static on it.** For tents, the "base" is the piece's z
minus its height above the wall base in `camp.py` (roofs +14 and +11), compared with the average z.

**MinersCompactTent** (21 components)

| Tile | Piece | Layout z | Land z | Avg z | Match |
|---|---|---|---|---|---|
| 3494,2744 | tent wall 0x036F | 5 | 6 | 6 | off 1 |
| 3495,2743 | tent wall 0x036E | 5 | 4 | 5 | yes |
| 3496,2743 | tent wall 0x036E | 5 | 5 | 5 | yes |
| 3497,2743 | tent wall 0x036D | 5 | 5 | 5 | yes |
| 3495,2745 | tent wall 0x0369 | 5 | 7 | 7 | **off 2** |
| 3496,2745 | tent wall 0x0369 | 5 | 7 | 7 | **off 2** |
| 3497,2745 | tent wall 0x0368 | 5 | 7 | 7 | **off 2** |
| 3495,2744 | tent roof 0x0603 | 19 (base 5) | 6 | 6 | off 1 |
| 3496,2744 | tent roof 0x0603 | 19 (base 5) | 6 | 6 | off 1 |
| 3497,2744 | tent roof 0x0633 | 16 (base 5) | 5 | 6 | off 1 |
| 3495,2742 | bedroll 0x0A58 | 5 | 6 | 5 | yes |
| 3496,2742 | iron ingots 0x1BF0 | 5 | 5 | 5 | yes |
| 3496,2742 | iron ingot 0x1BEF | 6 (+1) | 5 | 5 | yes |
| 3497,2742 | barrel 0x0E77 | 5 | 5 | 5 | yes |
| 3499,2742 | brazier 0x0E31 | 2 | 2 | 2 | yes |
| 3498,2743 | crate 0x0E3F | 4 | 5 | 4 | yes |
| 3498,2743 | pickaxe 0x0E86 | 7 (+3) | 5 | 4 | yes |
| 3499,2743 | iron ore 0x19B8 | 3 | 3 | 3 | yes |
| 3500,2743 | iron ore 0x19BA | 3 | 3 | 3 | yes |
| 3500,2744 | sledge hammer 0x0FB4 | 2 | 3 | 2 | yes |
| 3500,2742 | shovel 0x0F39 | 2 | 2 | 2 | yes |

**SurveyArchivistTent** (22 components)

| Tile | Piece | Layout z | Land z | Avg z | Match |
|---|---|---|---|---|---|
| 3492,2754 | tent wall 0x036F | 5 | 6 | 6 | off 1 |
| 3493,2753 | tent wall 0x036E | 5 | 6 | 6 | off 1 |
| 3494,2753 | tent wall 0x036E | 5 | 6 | 6 | off 1 |
| 3495,2753 | tent wall 0x036D | 5 | 6 | 6 | off 1 |
| 3493,2755 | tent wall 0x0369 | 5 | 6 | 6 | off 1 |
| 3494,2755 | tent wall 0x0369 | 5 | 6 | 6 | off 1 |
| 3495,2755 | tent wall 0x0368 | 5 | 6 | 5 | yes |
| 3493,2754 | tent roof 0x0603 | 19 (base 5) | 6 | 6 | off 1 |
| 3494,2754 | tent roof 0x0603 | 19 (base 5) | 6 | 6 | off 1 |
| 3495,2754 | tent roof 0x0633 | 16 (base 5) | 6 | 6 | off 1 |
| 3496,2756 | brazier 0x0E31 | 4 | 5 | 4 | yes |
| 3497,2753 | writing table 0x0B4A | 3 | 4 | 3 | yes |
| 3497,2753 | map 0x14EB | 8 (+5) | 4 | 3 | yes |
| 3497,2753 | candle 0x0A0F | 8 (+5) | 4 | 3 | yes |
| 3496,2753 | bench 0x0B5F | 4 | 5 | 4 | yes |
| 3496,2755 | globe 0x1047 | 4 | 5 | 4 | yes |
| 3497,2755 | wooden chest 0x0E42 | 2 | 3 | 2 | yes |
| 3497,2755 | scroll 0x2270 | 6 (+4) | 3 | 2 | yes |
| 3497,2755 | scroll 0x2272 | 6 (+4) | 3 | 2 | yes |
| 3493,2752 | wooden box 0x09AA | 6 | 8 | 6 | yes |
| 3493,2752 | sextant 0x1057 | 9 (+3) | 8 | 6 | yes |
| 3494,2756 | bedroll 0x0A59 | 6 | 6 | 6 | yes |

**NPC tiles**

| Tile | NPC | Layout z | Land z | Avg z | Standable |
|---|---|---|---|---|---|
| 3498,2744 | Liaison (to) | 4 | 5 | 4 | yes, `CanSpawnMobile` lowest z = 4 |
| 3496,2754 | Archivist (to) | 4 | 6 | 4 | yes, `CanSpawnMobile` lowest z = 4 |
| 3510,2748 | Liaison (from) | 0 | 0 | 0 | yes, 0 |
| 3516,2747 | Archivist (from) | 1 | 1 | 1 | yes, 1 |

Standable is a port of `Map.CanSpawnMobile(x, y, minZ, maxZ, canSwim false, cantWalk false)` (`Map.cs:1137-1275`,
blocker ranges per `ApplyBlockerMask` `:1410-1422`) over land and statics, z - 16 to z + 16. World items are not in
the port; section 1.4 shows there are none on these tiles, and no component sits on either (fact 3).

**Verdict: no stop.** The rule was "a tent wall or roof off by more than 2"; the maximum is exactly 2, on the Miners'
tent's south wall (3495-3497, 2745, average 7, one corner 8). **What it looks like:** those three walls start 2 below
the ground, so their bottom 2 z (8 pixels) are hidden by the land. The overseer should look for it in the screenshot.
Every deco z equals the server's average z plus its stack offset, so the props sit on the ground as rendered.

### 1.3 Same map files (A3)

The server reads, from its one data directory `/var/lib/uo/client-data/classic-client` (both `modernuo.json`s):
`map1.mul` if present, else `map1LegacyMUL.uop` (pinned `Projects/Server/TileMatrix/TileMatrix.cs:94-111`), `staidx1.mul`
(`:121`), `statics1.mul` (`:133`), and `tiledata.mul`. There is no `map1.mul`. Diff patches (`stadif*`) are off: they are
enabled only below client 7.0.9 (`TileMatrixPatch.cs:57-70`) and neither config sets `maps.enable*DiffPatches`; the
server detects 7.0.114.40 (Q-063). Both containers mount `D:/ShatteredLegacy/client-data/classic-client` (docker
inspect), the folder the mockup's `uorender.py` reads (as `~/mnt/ShatteredLegacy/client-data/classic-client`).

SHA-256, identical in all three places (host, inside `sl-modernuo-test`, inside `sl-modernuo`):

| File | SHA-256 |
|---|---|
| map1LegacyMUL.uop | 76a5bcfb70c3d74b738aa04b8886abd2efcfc423ca9bc151e0033cd448ca3686 |
| staidx1.mul | 66cb7739ece177e78f23f60f91f7df674d67f8f9284dc89e5b34cbf08c918015 |
| statics1.mul | ebfbba6d9222e46781a7ec27e0ecd89758ae9a1e2f7738fe674aef19fdf1521e |
| tiledata.mul | f5360f51f5709b5995985a6497f5441665144a4e051741f2474eef1d6f0a3a93 |

I could not hash the mockup's own copy (it ran in another environment). As a stand-in, every deco z in `layout.json`
is reproduced exactly from these files by camp.py's own formula (table above), which a different map would not do.
Q-063 still applies: players on EA's current 7.0.117.0 data may draw this area differently; not checked.

### 1.4 What is on the 45 tiles (A4)

`camp_items.py` decoded every item of each save copy per pinned `Item.Serialize` (`Item.cs:816-1080`); none carried a
bounce record, so none was skipped. Box x 3485-3525, y 2735-2765:

- **Test** (2026-09-30 15:05): 16 items. 13 reagents at 3489,2750, 3494,2760 and 3499,2759; the spawner at 3506,2746; the
  south mine Forge 3508,2746 and Anvil 3510,2746 (`ClusterFSouthMineDecor`). 6 mobiles: Gervis, a Miner, Mugg, Jacob
  Waltz 3511,2744, the **Liaison at 3510,2748,0** (serial 0x1), the **Archivist at 3516,2747,1** (serial 0x2).
- **Live** (2026-09-29 13:50): 3 items (spawner, Forge, Anvil). 5 mobiles: Gervis, a Miner, Mugg, Jacob Waltz 3511,2744,
  and the **Liaison at 3510,2748,0** (named "Miners' Compact Liaison", an older build). **No Survey Archivist.**
- **On a component tile, an NPC destination tile, or the tile in front of an opening: nothing, on either save.**
  The client statics on those tiles: none (1.2). `server/tools/StaticsEditor` (an old client-side statics injector for
  this camp) was never applied to the server's files; its tiles are all at x 3507 and east anyway.

**P17's 125 entries.** `p17_collide.py` parsed all 125 `DecorEntry` lines of `ClusterFNewHavenServicesSeeder.cs`:
no exact collision; the nearest to any camp tile is `Static 0xBA1` at 3450,2607, **135 tiles** away; no entry is south of
y 2607, and the camp is at y 2742-2756. The Healer spawner is at 3462,2559,35. **No collision.**

---

## 2. What changed, file by file

All in `D:\ShatteredLegacy\server`. ASCII in every file touched. No pinned file, patch or `Distribution/Data` touched.

| File | What |
|---|---|
| `customizations/ClusterFMineCampLayout.cs` (new, generated) | the design file as a C# table: 2 addons, 43 components, 2 NPC moves, the design file's SHA-256 |
| `customizations/ClusterFMineCampSeeder.cs` (new) | `MinersCompactTentAddon`, `SurveyArchivistTentAddon`; `[ClusterFSeedMineCamp [status\|dryrun]`; `[ClusterFMoveMineCampNpcs [dryrun]`; setting `clusterf.mineCamp.seedOnWorldLoad` (default False) |
| `customizations/ClusterFInstitutionSeeder.cs` | Liaison 3498,2744,4 and Archivist 3496,2754,4, both facing East; each keeps its old tile as `wasAt`, so world load counts an NPC within 15 of the old tile as present; Archivist's "temporary" comment removed; header says why |
| `customizations/ClusterFGuildStarterPath.cs` | the `mining` directory entry's tile is 3498,2744,4 facing East (was 3510,2748,0) |
| `customizations/MinersCompactLiaison.cs`, `SurveyArchivist.cs` | the location line in the class comment. `SurveyArchivist.cs` also had 5 non-ASCII characters in comments (em dashes, box rules), replaced with `-` because the file was touched |
| `tests/Misc/MineCampVerification.cs` (new) | 5 facts (section 5) |
| `tests/Misc/MineCampLayoutDesignCopy.cs` (new, generated) | `layout.json` verbatim, and its SHA-256 |

Generator (in this repo): `notes/cc-P16-tools/gen_layout.py`. **Re-run it after any change to `layout.json`**, then
build; the test fails until the table matches.

---

## 3. Part B: the build

### 3.1 Layout as data (B1)

**Chosen: a generated C# table**, `ClusterFMineCampLayout.cs`. Why:
- There is no data folder from our tree that the image ships. `apply-patches.sh` installs only `.cs` from
  `server/customizations` and reports the rest as "not installed" (`mirror_cs_tree`, `apply-patches.sh:67-117`, the notice at `:112-116`), and
  `Distribution/Data` is pinned (P17 found the same, section 1.3).
- A table is typed (item ids as ints, facing as `Direction`) and a malformed one fails the build, not the shard's start.

**The design file stays the source of truth, with one gap.** The test container is the builder image, which holds
`server/customizations`, `server/tests`, `server/migrations` and `server/patches` and nothing from `design/`
(`docker/uo/Dockerfile:40-53`). So the test cannot open `design/mine-camp-tents/layout.json` itself. The generator
writes the design file **verbatim** into `MineCampLayoutDesignCopy.cs` alongside its SHA-256, and fact 1 parses that copy,
checks its hash, and compares it with the table component for component. That catches any hand edit to the table or the
copy. **It does not catch an edit to the design file that nobody re-generates.** Closing that needs one Dockerfile line
(`COPY design/mine-camp-tents/layout.json /design/mine-camp-tents/layout.json`) and the fact reading that path; that is
outside this task's scope (`docker/`), so it is proposed here, not done.

### 3.2 Two addons (B2)

One class per tent, each building its components from the table in its constructor. The addon sits at its first
component (the tent's west wall); every component is placed at its offset from there, so each lands on its design tile
and z exactly (fact 2 checks all 43). Components are plain pinned `AddonComponent`s: not movable, not decaying, no deed,
double-click does nothing (1.1). The crate, chests, barrel and box are props.

### 3.3 Seeder (B3)

`[ClusterFSeedMineCamp` (Administrator) places each tent whose type is not already on Trammel; a second run places
nothing (fact 2). `status` or `dryrun` lists what it would place, the origin and component count, and any foreign item
already on its tiles (listed, never moved or deleted). **World load does not place the tents** unless
`clusterf.mineCamp.seedOnWorldLoad` is True (default False, written into `modernuo.json` on first start), for the reason
P17 gave: the other seeders run at every world load on live, and adding placement there would change live at its next
start without Chase running anything.

### 3.4 NPC positions for fresh worlds (B4)

In `ClusterFInstitutionSeeder`, both NPCs are now at their layout `to` tiles, facing East. **World load changes nothing
for an NPC near its old spot:** the duplicate check now matches an NPC of the type within 15 tiles of the new tile **or**
of the old tile (`wasAt`). It never moves anything; that is the command's job (B5). This is the P17 shape.

**What it means for existing worlds, by NPC:**
- **Liaison:** old 3510,2748 to new 3498,2744 is 12 tiles, inside 15; it would have been left alone even without
  `wasAt`. It stays at the old spot, facing South, until the move command.
- **Archivist:** old 3516,2747 to new 3496,2754 is **20 tiles**, outside 15. **The brief's premise does not hold for
  her.** Without `wasAt`, world load on the test world (which has her at 3516,2747) would have placed a second Archivist
  at the tent. Red run A removed her `wasAt` and fact 5 saw exactly that (3 NPCs where 2 were expected).
- **An NPC standing anywhere else** (more than 15 from both tiles) is not seen, and world load places a new one at the
  tent, as it always did for a missing NPC. Neither save has that case.

### 3.5 Existing worlds: the move command (B5)

`[ClusterFMoveMineCampNpcs [dryrun]` (Administrator), per NPC in the layout:
1. One already at its new tile, facing East, with home and `CantWalk` set: reported, not touched.
2. Otherwise the nearest of the type within 15 tiles of its old tile is moved: new tile, facing East, home the new tile,
   range 0, `CantWalk`. Any more of the type near the old spot are counted and left where they are.
3. None near the old spot: reported, with the one near the new tile if any. **It never creates an NPC.**

It reports each move by name and serial, from and to. A second run moves nothing (fact 4).

### 3.6 Directory arrow (B6)

**Confirmed: it targets the mobile.** `ShowTheWay` finds the guildmaster with `GuildLocation.Find()`, which searches 15
tiles around the directory tile for the type (`ClusterFGuildStarterPath.cs:171-196`), then makes
`new GuildDirectionArrow(pm, npc, npc.Location, map, ...)` (`:585`), whose timer follows the target when it moves
(`:643-647`). The directory **tile** was a fixed point, 3510,2748,0, used for the search centre and the "is not at" text;
it is now 3498,2744,4. Since the two are 12 apart, an unmoved Liaison is still found from the new tile (fact 4 checks the
arrow's target both before and after the move).

---

## 4. Loose ends

1. **Tents on uneven ground:** the Miners' tent's south walls start 2 z below the ground (1.2). Within the rule; visible
   only as a slightly shorter wall. If the overseer wants it flush, the fix is in the design (per-wall z), then re-generate.
2. **Live's Archivist.** Live had none on 2026-09-29, probably because live runs an older image (`docs/bug-list.md` D25/D29,
   as P17 noted). When live starts on an image carrying this change, world load **creates** her at 3496,2754,4 by the
   tent opening, **whether or not the tents have been seeded**. Before this change the same start would have created her
   at 3516,2747. Either way it is a creation, not a move, and it happens once. Worth knowing before the next live deploy.
3. **Not checked in a client.** The render, the walls' look at z 5, and walking into the tents have only been reasoned
   from the map data and the mockup. The checklist below covers it.
4. The live save copy is from 2026-09-29 13:50; live may have changed since.

---

## 5. Tests

`server/tests/Misc/MineCampVerification.cs`:

| # | Fact | What it pins |
|---|---|---|
| 1 | `TheLoadedLayoutIsTheDesignFile` | the table equals the verbatim design file (hash checked), component for component (group, id, name, x, y, z), in order; 21 + 22 = 43 counted; the NPC moves (type, from, to, facing) |
| 2 | `SeedingTwicePlacesExactlyTwoTents` | a dry run places nothing; two real runs place exactly one tent of each type; all 43 components are plain `AddonComponent`s at their design tiles on Trammel, not movable, not decaying, no deed |
| 3 | `NoComponentSitsOnAnNpcTileOrInFrontOfAnOpening` | each tent has exactly one opening (the east column tile with no wall); the tile east of it is that tent's NPC tile; no component on it or on either NPC tile |
| 4 | `TheMoveCommandRunTwiceMovesEachNpcOnceAndCreatesNone` | with none on the world it creates none; a dry run moves nothing; run 1 moves both from their old tiles, run 2 moves none; same two mobiles, same mobile count; the Miners' Compact arrow targets the Liaison before and after the move |
| 5 | `WorldLoadLeavesMineCampNpcsNearTheirOldSpotsAndPlacesNewOnesAtTheTents` | the institution seeder leaves both at their old tiles and facing, and creates no second one; on a world without them it places both at the openings facing East; run again it places no more |

Fact 3's opening rule reads the layout rather than a hard-coded tile, so it holds if the design moves a tent.

---

## 6. Red and green runs

All through `docker/uo/build.sh`. Breaks were applied by a script to backed-up copies, restored from the copies, checked
byte-identical by SHA-256 after each run, and grepped for markers: none left.

| Run | Breaks | Result |
|---|---|---|
| build 1 | none | did not compile: xUnit2000, `Assert.Equal` arguments the wrong way round in fact 1; fixed |
| build 2 | none | **323 passed**; image built. The 5 new facts all passed; 318 is 323 minus those 5, not a separately measured before-count |
| red A | (1) the pickaxe's z 7 to 8 in the table; (2) the seeder never finds an existing tent; (4) the move's "already in place" check off; (5) the Archivist's `wasAt` removed | **319 passed, 4 failed**, each on its own break: fact 1 (pickaxe z 8, expected 7); fact 2 (4 tents, expected 2); fact 4 ("moved: 1 of 2" on the second run: the Liaison moved again); fact 5 (3 NPCs, expected 2: a second Archivist) |
| red B | (3) the crate moved to 3498,2744, the Liaison's tile; (4b) the move command creates an NPC when none is found | **320 passed, 3 failed**: fact 3 (crate in front of the opening and on the Liaison's tile); fact 4 (created Garrett Ashveil and Velara Thorne on an empty world); fact 1 with break 3 (expected: the table no longer matches the design) |
| final | none, restored and hash-checked | `docker/uo/build.sh -t sl-modernuo:cc-p16-minecamp`: **323 passed**, "Built sl-modernuo:cc-p16-minecamp with patches applied and 323 shard test(s) passing." Image `77bb7dabdc94`; `sl-modernuo:latest` still `16b0f49e6828` |

---

## 7. Checklist for Chase

1. **Commit** with `D:\UO\Commit-ShardWork.ps1`. All 8 of this task's files are already in `5a8b67f`, which also has
   the two red-run breaks (warning at the top). Committing now removes them: `git diff` in `D:\ShatteredLegacy` should
   show only the two `// P16-BREAK` lines going. Plus this note here (the tools are already in `4b7654e`).
2. **Rebuild the test shard** from the console ("Rebuild through the gates"); the gate should say 323 passed. That build
   retags `sl-modernuo:latest`; `sl-modernuo:cc-p16-minecamp` is this task's image.
3. **On the test shard**, as Administrator:
   1. `[ClusterFSeedMineCamp dryrun`: it should say it would place both tents, 21 and 22 components, and list nothing
      already on their tiles. Then `[ClusterFSeedMineCamp`.
   2. `[ClusterFMoveMineCampNpcs dryrun`, then `[ClusterFMoveMineCampNpcs`: it should report moving Garrett Ashveil
      from 3510,2748,0 and Velara Thorne from 3516,2747,1. Run it again: "already at", 0 of 2.
   3. `[go 3498 2744 4` and `[go 3496 2754 4` to look. Talk to both NPCs (their gumps should open as before).
   4. On a character, open the Guild Board, choose the Miners' Compact and "Show me the way": the arrow should lead to
      the Liaison at the tent.
4. **Screenshot the camp** for the overseer to compare with `design/mine-camp-tents/v3_closeup.png`. Look at the Miners'
   tent's south wall (section 4.1) and whether both NPCs stand clear of the tent pieces.
5. **Live-world commands** (Administrator, in game; after the test shard looks right):

   | Command | What it does | Re-run |
   |---|---|---|
   | `[ClusterFSeedMineCamp dryrun` | lists what would be placed; changes nothing | safe |
   | `[ClusterFSeedMineCamp` | places the two tents (43 components); moves and deletes nothing | safe: a tent of that type already on Trammel is never placed again (fact 2) |
   | `[ClusterFMoveMineCampNpcs dryrun` | lists what would move; changes nothing | safe |
   | `[ClusterFMoveMineCampNpcs` | moves the Liaison (and the Archivist, if one is near her old spot) to the tent openings; **creates nothing** | safe: a second run moves nothing (fact 4) |

   **On live, the Archivist may not exist yet** (none in the 2026-09-29 save). If so, the move command reports "none near
   its old spot". The next start on the new image creates her at the tent opening (section 4.2). Running the move after
   that start reports her "already at" the tent.
   A fresh world gets the NPCs at the tents from world load. Suggest adding `[ClusterFSeedMineCamp` to the console's World
   setup list next to `[ClusterFSeedNewHavenServices`, or set `clusterf.mineCamp.seedOnWorldLoad` to True for fresh worlds.

Open, unverified:
- Nothing was run in a client (section 4.3).
- The mockup's own copy of the map files was not hashed; equivalence rests on reproducing its z values (1.3).
- Whether the live save copy is current.
