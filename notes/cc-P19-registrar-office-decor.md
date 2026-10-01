# cc-P19: decor for the League Registrar's field office

Date: 2026-09-30. Agent: Claude Code. Pinned ModernUO `7c9215d97`. Built in `D:\ShatteredLegacy`, **not committed**.
No world was changed: nothing placed, moved or removed on live or test; no shard deployed, restarted or recreated.
Save files were read from copies only. `sl-modernuo:latest` was not moved (`33aef6969ccb` before and after).
Image: `sl-modernuo:cc-p19-office` = `1fc199be9380`.

**Gate before starting.** `git --no-optional-locks status` in `D:\ShatteredLegacy` at `a917b3d`: clean. P16 is committed
(`5a8b67f`, and its red-run fix in `1672f2c`); P17 (`bb51fad`); P21 after it (`29cb496`, `a917b3d`). I could not
verify that no other prompt was working in `D:\ShatteredLegacy` beyond the clean tree; nothing changed under me.

Read-only tools and their outputs: `notes/cc-P19-tools/` (README there). `gen_office_layout.py` and `breaks.py` there
WRITE to `D:\ShatteredLegacy` (the generator and the red-run breaks).

> **Headlines**
>
> 1. **Built:** three prop addons from the design file (outside 5, office 10, quarters 3), the two signs named
>    "League of Extraordinary Citizens", `[ClusterFSeedRegistrarOffice [status|dryrun]`, and the Registrar seeded facing
>    West. **333 tests pass** (5 new). Every new fact was watched red on a break of its own (section 5).
> 2. **Part A: no stop.** 17 of 18 props equal the server's surface z (`Map.GetTopSurfaceZ`); the hourglass is +3 by
>    design, standing on the books (height 3). Nothing is on any prop tile on the test or live save.
> 3. **The brief's doorway premise does not hold on the test world.** 3457,2599 carries **pinned `[DoorGen`'s SouthCW
>    door 0x06AD**, not P17's NorthCW 0x06B3: P17's seeder keeps its door out when any door is already on the tile. The
>    test image post-dates P17 and P17's seeder did run there (its front door is present), so this is not a stale image.
>    **That door swings onto the desk's north tile**, over the books and hourglass. It still opens and closes (pinned does
>    not fit-check opening); it draws over the desk when open, as it already did over the map's table. Not a blocker;
>    worth the overseer's eye in the screenshot (section 1.2). P17's front door, and P17's doorway door where it is
>    placed, swing into walls with nothing of ours in the way.
> 4. **Changing her facing alone would have turned the Registrar on live at its next start**, because both shards
>    repair New Haven NPCs at world load. World load now accepts her old North facing; turning her is
>    `[ClusterFSeedNewHaven repair`, Chase's call (section 3.5).
> 5. **Two brief details were off:** the Registrar's entry is at `ClusterFNewHavenSeeder.cs:69`, not `:60`; and live's
>    copy has neither P17 door, but a DoorGen door at 3457,2601,**38**, inside the roof (not touched).

---

## 1. Part A: facts

### 1.1 Z table (A1)

The server's surface z is pinned **`Map.GetTopSurfaceZ(Point3D p)`** (`Projects/Server/Maps/Map.cs:491-565`): the highest
of the land's average z (`GetAverageZ`, `:237-296`) and every static whose tiledata is Surface or Wet, at its top
(`tile.Z + CalcHeight`), that is at or below `p.Z`. It also counts non-movable world items (`:536-560`); those are
covered separately in 1.3. Ported in `office_z.py` over the map files the server reads
(`map1LegacyMUL.uop`, `staidx1.mul`, `statics1.mul`, `tiledata.mul` in `D:\ShatteredLegacy\client-data\classic-client`,
the folder both containers mount; P16 section 1.3 hashed them identical across host, test and live). Probe at the
layout z, so a match means a surface exactly there.

| # | Area | Component | Tile | Layout z | Server z | Match | What the surface is |
|---|---|---|---|---|---|---|---|
| 1 | outside | potted tree 0x11C9 | 3458,2595 | 15 | 15 | yes | land, average z (corner z 19) |
| 2 | outside | wooden signpost 0x0B97 | 3463,2597 | 13 | 13 | yes | land (grass static 0x0D32 at 14+0 is above 13) |
| 3 | outside | wooden sign 0x0BCF | 3463,2597 | 13 | 13 | yes | same tile as 2 |
| 4 | outside | wooden signpost 0x0B98 | 3460,2595 | 15 | 15 | yes | land |
| 5 | outside | wooden sign 0x0BD0 | 3460,2595 | 15 | 15 | yes | same tile as 4 |
| 6 | office | books 0x1E25 | 3458,2600 | 24 | 24 | yes | table 0x0B83 at 18 + 6 |
| 7 | office | inkwell 0x2D61 | 3458,2601 | 24 | 24 | yes | table 0x0B84 at 18 + 6 |
| 8 | office | scroll 0x2270 | 3458,2601 | 24 | 24 | yes | table 0x0B84 |
| 9 | office | hourglass 0x1810 | 3458,2600 | 27 | 24 | yes, stacked +3 | table top 24; it stands on the books (24 + books height 3 = 27), as `registrar.py` meant (`TBL+3`) |
| 10 | office | bookcase 0x0A99 | 3461,2597 | 18 | 18 | yes | floor, slate 0x049C at 18 |
| 11 | office | bookcase 0x0A9A | 3458,2602 | 18 | 18 | yes | floor |
| 12 | office | bulletin board 0x1E5F | 3458,2598 | 18 | 18 | yes | floor (bearskin rug 0x1E39 at 18+0) |
| 13 | office | candelabra 0x0B26 | 3461,2600 | 18 | 18 | yes | floor |
| 14 | office | flowerpot 0x11CA | 3460,2597 | 18 | 18 | yes | floor (rug) |
| 15 | office | globe 0x1047 | 3461,2598 | 18 | 18 | yes | floor |
| 16 | quarters | wooden chest 0x0E42 | 3456,2597 | 18 | 18 | yes | floor |
| 17 | quarters | bookcase 0x0A9A | 3454,2602 | 18 | 18 | yes | floor |
| 18 | quarters | scroll 0x2272 | 3454,2598 | 24 | 24 | yes | table 0x0B3A at 18 + 6 (a lantern static sits on it at 23) |

**Verdict: no stop.** 17 of 18 equal the server z exactly; the 18th, the hourglass, is 3 above it by design: it stands
on the books, whose tiledata height is 3 (`props_tiledata.out.txt`). The books are not Surface, so `GetTopSurfaceZ` would
not count them even once placed (`:536-560` reads only Surface or Wet items); this matters only for what the server
would say stands there, not for the drawing. The stack is what P16 did with its pickaxe on the crate (+3).
The floor is the slate static at z 18 over a stone static at 13+10 (bridge, so 13+5 = 18); land is 13 to 14 under it.
The map's own furniture is as the brief says: bed 3454-3455,2597, dresser 3454,2600-2601, the side table 3454,2598,
the desk table 3458,2600-2601, and **a chair static 0x0B58 at 3459,2601**, the Registrar's tile.

### 1.2 The doors, and walking (A2)

**The brief's premise holds for the front door and not, on the test world, for the office doorway.**

What is on each door tile, from the map and the saves (1.3):

| Tile | Map static | P17 entry (`ClusterFNewHavenServicesSeeder.cs:93`, `:97`; `NewHaven.cfg:63`, `:72`) | Test world | Live world (2026-09-29 copy) |
|---|---|---|---|---|
| 3459,2596 front | wooden stairs 0x073B at 13 (top 15); no door static | `DarkWoodDoor 0x06A9 WestCCW` z15 | **P17's door** 0x06A9, serial 0x40067DBF (placed by `[ClusterFSeedNewHavenServices`, see 1.3) | no door |
| 3457,2599 doorway | none (a gap in the dividing wall 0x0008 at 2598 and 2600) | `DarkWoodDoor 0x06B3 NorthCW` z18 | **DoorGen's door** 0x06AD (SouthCW), serial 0x40004158 | no door at z18 |

- **Where the doorway's 0x06AD comes from: pinned `[DoorGen`.** It is not in pinned's decoration data (no line at
  3457 2599 in `Distribution/Data/Decoration`). `DoorGenerator` (`Projects/UOContent/Misc/DoorGenerator.cs:341`,
  Developer) finds a north frame at (x, y) and a south frame at (x, y+2) and adds a `SouthCW` `DarkWoodDoor` between
  (`:567-569`, `:480-519`). The two wall statics 0x0008 at 3457,2598 and 3457,2600 are that pair. 0x06AD is
  `0x6A5 + 2 * SouthCW(4)` (`Doors.cs:147-152`, facings `:5-15`). Its low serial puts it with the world-generation
  items of 2026-09-29.
- **So on any world where `[DoorGen` ran, P17's doorway door is never placed.** P17's seeder keeps a door entry out when
  any `BaseDoor` stands on its tile within 8 z (`ClusterFNewHavenServicesSeeder.cs:293-317`, the test at `:317`, the rule pinned's
  `FindItem` would otherwise enforce by deleting the old door, `Decorate.cs:1135-1168`). On the test world that is what
  happened. Where `[DoorGen` did not run, P17 places 0x06B3 NorthCW there. Which a "fresh world" gets therefore depends on
  whether `[DoorGen` is part of making it; the console's fresh-world sequence does not list it
  (`scripts/Shard-Console.ps1:1273-1296`), but the test world has it. **Unverified which is meant.**
- **Live is different again.** Its copy has no door on either tile at floor height, and a `DarkWoodDoor 0x06AD` at
  **3457,2601,38**, inside the thatch roof (serial 0x40011441). Not touched, not mine; recorded for the overseer.

How each door swings (pinned `BaseDoor`): opening moves the door by its facing's offset with **no fit check**
(`Open` setter, `BaseDoor.cs:79-115`, the move at `:90-93`; `Use`, `:336-381`); closing requires its closed tile free of
Surface or Impassable items and of mobiles (`CanClose` / `CheckFit`, `:254-310`). Offsets `:13-28`.

| Door | Opens to | What is there | Props on the closed tile | Props on the swing tile | Verdict |
|---|---|---|---|---|---|
| front, P17 WestCCW 0x06A9 | 3458,2596 (offset -1,0) | wall static 0x0007 | none | none | swings and closes |
| doorway, P17 NorthCW 0x06B3 | 3457,2598 (offset 0,-1) | wall static 0x0008 | none | none | swings and closes |
| doorway, DoorGen SouthCW 0x06AD (test world) | **3458,2600** (offset +1,+1) | **the desk's north tile**: table static, and with this task the books (24) and hourglass (27) | none | **books, hourglass** | opens and closes (no fit check on opening; the closed tile is clear). **Draws over the desk when open** |

The last row is the one visible consequence: on the test world the open doorway door already swings onto the map's
desk; with the props it also overlaps the books and hourglass. It does not stop the door being used. Fact 3 pins both
that it opens and closes and that the books are on its swing tile, so a later change cannot hide it.

**Walking with the props in place.** Port of `Map.CanSpawnMobile(x, y, 2, 34, canSwim false, cantWalk false)`
(`Map.cs:1137-1275`, from `notes/cc-P16-tools/camp_z.py`) with every layout component on the tile added at its z
(`office_z.out.txt`, last table). No component is on any of these tiles:

| Tile | What | Standable z |
|---|---|---|
| 3459,2595 | outside the front door (tree to its west, signpost to its east) | 14 |
| 3459,2597 | inside the front door | 18 |
| 3459,2598, 3459,2599 | the way from the door to the desk | 18 |
| 3456,2599 / 3458,2599 | either side of the office doorway | 18 |
| 3459,2600 | north of the Registrar, beside the desk | 18 |
| 3460,2600 / 3460,2601 / 3460,2602 | east of the Registrar, where a visitor stands | 18 |

The desk itself (3458,2600-2601) is not a walking tile: it is a table static against the dividing wall at x 3457, so
"in front of the desk" is the Registrar's side, x 3459-3460. A player uses each door from the tile on either side
(`OnDoubleClick`, range 2, `BaseDoor.cs:414-423`); all four are clear.

### 1.3 Server items on these tiles (A3)

**Which image the test world runs.** `sl-modernuo-test` runs image `33aef6969ccb` (`sl-modernuo:latest`, built
2026-09-30 16:24, started 16:52). Its `UOContent.dll` contains `ClusterFNewHavenServicesSeeder`,
`ClusterFMineCampSeeder` and `ShardCommandAttribute` (grep inside the container), so it **post-dates P17** (and P16,
P21). Its config has `clusterf.newHavenServices.seedOnWorldLoad` False, so P17's decoration is on that world only if
someone ran the command, **and someone did**: the front door 0x06A9 (serial 0x40067DBF) and P17's `Static 0xBA1` at
3450,2607,27 (serial 0x40067DF9, `ClusterFNewHavenServicesSeeder` entry, P16 section 1.4) are both there with
consecutive high serials. **So this is not the false all-clear the brief warned about**: the world carries P17's run,
and the doorway's missing 0x06B3 is P17's own rule at work (1.2), not a stale image.

`office_items.py` (adapted from P16's `camp_items.py`; items per pinned `Item.Serialize`, `Item.cs:816-1080`; no item
carried bounce data, so none was skipped) over copies of the saves, box x 3448-3468, y 2590-2608:

- **Test** (copy of 2026-09-30 20:30): 4 items. DarkWoodDoor 0x06AD 3449,2606,30; Static 0x0BA1 3450,2607,27 (P17);
  **DarkWoodDoor 0x06AD 3457,2599,18** (DoorGen, the doorway); **DarkWoodDoor 0x06A9 3459,2596,15** (P17, the front
  door). Mobiles: a hawk, and **Elara Voss (LeagueRegistrar) 3459,2601,18**.
- **Live** (copy of 2026-09-29 13:50; may be stale): 2 items. DarkWoodDoor 0x06AD 3449,2606,30; **DarkWoodDoor 0x06AD
  3457,2601,38** (in the roof). Mobiles: a cat, three birds, a cow, and the **LeagueRegistrar ("League Registrar", an
  older build) 3459,2601,18**.
- **On a component tile: nothing, on either save.** The doors above are the only items inside the house.

### 1.4 The Registrar today (A4)

- **Faces North.** The seeder entry is at **`ClusterFNewHavenSeeder.cs:69`**, not `:60` as the brief says (line 60 is the
  Walker entry): `3459, 2601, Direction.North, 18`. `ApplyEntry` sets that facing (`:179-194` at HEAD).
- **Her desk is West of her**: the table statics 0x0B83/0x0B84 at 3458,2600 and 3458,2601 (1.1). She sits on the chair
  static at her own tile. Which way the chair graphic 0x0B58 faces was not checked against art; unverified.
- **Both shards repair her on world load.** `clusterf.newHavenSeeder.repairOnWorldLoad` is True on test
  (`Configuration-test/modernuo.json`) and live (`server/uo/modernuo/Configuration/modernuo.json`, the live bind
  mount). So **changing the entry's facing alone would have turned her on live at its next start**, without Chase
  running anything. Section 3.5 is how that is avoided.

---

## 2. What changed, file by file

All in `D:\ShatteredLegacy\server`. ASCII in every file touched (checked byte by byte). No pinned file, patch,
`Distribution/Data`, `docker/` or `scripts/` touched.

| File | What |
|---|---|
| `customizations/ClusterFRegistrarOfficeLayout.cs` (new, generated) | the design file as a C# table: 18 components in design order, the three area arrays, the design file's SHA-256. Uses P16's `MineCampComponent` record; `Group` is the design's `area` |
| `customizations/ClusterFRegistrarOfficeSeeder.cs` (new) | `RegistrarOfficeOutsideAddon`, `RegistrarOfficeAddon`, `RegistrarQuartersAddon`; sign naming; `[ClusterFSeedRegistrarOffice [status\|dryrun]` with its `[ShardCommand]`; setting `clusterf.registrarOffice.seedOnWorldLoad` (default False) |
| `customizations/ClusterFMineCampSeeder.cs` | P16's placement loop is now `SeedAddons(label, noun, addons, dryRun)`; P16's `Seed` calls it with "mine camp", "tents" and its two tents, so P16's output is unchanged word for word (its facts still pass). The office calls the same loop. No second placer |
| `customizations/ClusterFNewHavenSeeder.cs` | the Registrar's entry faces **West**, with `.WasAt(3459, 2601, 18, Direction.North)`; `WasAt` takes an optional old facing (`LegacyDirection`), and world-load repair accepts the legacy tile **with the legacy facing**. Entries that name no old facing behave as before |
| `tests/Misc/RegistrarOfficeVerification.cs` (new) | 5 facts (section 4) |
| `tests/Misc/RegistrarOfficeLayoutDesignCopy.cs` (new, generated) | `layout.json` verbatim, and its SHA-256 |

In this repo: `notes/cc-P19-tools/` (generator, Part A tools and outputs, break script). **Re-run
`gen_office_layout.py` after any change to `layout.json`**, then build; fact 1 fails until the table matches.

---

## 3. Part B

### 3.1 Layout as data (B1)

P16's mechanism, unchanged in shape: a generated C# table plus a verbatim, hash-checked copy of the design file for the
test, because the build installs only `.cs` from `server/customizations` and the test container holds nothing from
`design/` (P16 section 3.1). The same gap P16 recorded applies: an edit to `layout.json` that nobody re-generates is not
caught. P16's proposed one-line Dockerfile `COPY` would close it for both; still out of scope.

### 3.2 Props and grouping (B2)

**One addon per area: outside (5), office (10), quarters (3).** P16 grouped by structure (one per tent); the closest
equivalent here is the design's own areas, and it lets a later change to one room be re-seeded without touching the
other two. Each addon sits at its area's first component and places every component at its design tile and z
(fact 2 checks all 18). Components are plain pinned `AddonComponent`s: not movable, not decaying, no deed,
double-click does nothing (P16 section 1.1 has the citations). **The bookcases, chest and bulletin board are not
containers or boards**: they are `AddonComponent`s showing those graphics, so there is nothing to open or post to.

### 3.3 The signs (B3)

After the outside addon builds its components, the two whose item ids are 0x0BCF and 0x0BD0 get
`Name = "League of Extraordinary Citizens"`. A single click shows `Name` when it is set, with tooltips off
(`Item.OnSingleClick`, `Item.cs:4069-4110`) and on (`OnAosSingleClick`, `:4050-4067`, which sends the property list's
header; `AddNameProperty` puts `Name` there, `:1825-1850`). `Name` is saved with the item (`Item.Serialize`, flag
0x100), so it survives a restart. The signposts and the other 16 props keep their tile names (fact 4).

### 3.4 Seeder and command (B4)

`[ClusterFSeedRegistrarOffice` (Administrator) places each of the three addons whose type is not already on Trammel;
a second run places nothing (fact 2). `status` or `dryrun` lists what it would place, the origin and component count,
and any foreign item on its tiles (listed, never moved or deleted). Declared
`[ShardCommand(WorldSetup, Rerun = Skips, Shard = TestFirst, DryRun = "dryrun")]`, so P21's console lists it.

**"The fresh world gets the office decor": by command or by setting, not by default.** World load places the props only
if `clusterf.registrarOffice.seedOnWorldLoad` is True (default False), the rule P16 and P17 both used: the other seeders
run at every world load on live, so a default-True would change live at its next start without Chase running anything.
For a fresh world, run the command after the New Haven sequence, or set the setting True on that world's config.
**Not done here (scope: `scripts/` is not mine): adding a "registrar office" sequence to the console's
`$script:WorldSetupOrder`** (`Shard-Console.ps1:1273`). The command appears on the World setup tab anyway, under "no
order established". It has no ordering dependency on P17's doors: it places nothing on a door tile whichever door is there.

### 3.5 Facing (B5)

The seeded direction is now **West**, so a new world places her facing the desk. For an existing world:

- **World load does not turn her.** Both shards repair New Haven NPCs at world load (1.4). The entry names her old tile
  and facing (`WasAt(3459, 2601, 18, Direction.North)`), and world-load repair accepts an NPC on the old tile with the
  old facing, exactly as P17 did for old tiles. Fact 5 pins: North on her tile is left alone at world load and repaired
  by the command; West is left alone by both; any other facing is repaired by both, as before.
- **How she gets turned (a world-state step, Chase's call):** `[ClusterFSeedNewHaven repair` (dry run first:
  `[ClusterFSeedNewHaven dryrun`). It is already in the console's New Haven sequence. **It repairs every New Haven NPC
  that is off its entry, not only her**, which is what it already did; on a world where it has run since PT-05 she is the
  only change. Alternative for her alone: `[set Direction West` targeting her (pinned `[set`; not tried here).

---

## 4. Tests

`server/tests/Misc/RegistrarOfficeVerification.cs`:

| # | Fact | What it pins |
|---|---|---|
| 1 | `TheLoadedLayoutIsTheDesignFile` | the table equals the verbatim design file (hash checked), component for component (area, id, name, x, y, z), in order; each area array is exactly the design's components of that area; 18 = 5 + 10 + 3 counted |
| 2 | `SeedingTwicePlacesTheDecorOnce` | a dry run places nothing; two real runs place exactly one addon of each of the three types ("placed 3 of 3", then "0 of 3"); all 18 components are plain `AddonComponent`s at their design tiles on Trammel, not movable, not decaying, no deed |
| 3 | `NoComponentSitsOnADoorItsSwingOrTheRegistrarTile` | places P17's two door entries **with P17's own code** (its `Decoration` entries at 3459,2596 and 3457,2599, built by pinned `DecorationList`; asserts their headers), seeds, then: no component on either door tile, on either door's swing tile (pinned `BaseDoor.GetOffset`), or on the Registrar's seeded tile; each door opens, is free to close, and closes back. Then swaps in DoorGen's SouthCW door: its swing tile is the desk's north tile, a prop is there, and it still opens and closes |
| 4 | `BothSignsReportTheLeagueName` | exactly two sign components, 0x0BCF at 3463,2597,13 and 0x0BD0 at 3460,2595,15; each has the name and the property-list header a single click sends; every other outside component has no name |
| 5 | `TheRegistrarFacesHerDeskAndWorldLoadLeavesAnOldOneAlone` | the entry faces West at 3459,2601,18, legacy facing North; North on her tile: world load leaves her, the command repairs her; West: neither touches her; South: both repair |

The brief's test 3 ("not on P17's two door tiles or the Registrar's tile") is fact 3's first half; the swing tiles and
the open/close cycle are added because a door is not a clear tile.

---

## 5. Red and green runs

All through `docker/uo/build.sh` (red runs with `--tests-only`, which builds no image). Breaks applied by
`notes/cc-P19-tools/breaks.py` to byte-copied sources, each marked `P19-BREAK`; restored from the copies, SHA-256 checked
equal, and `grep -rl P19-BREAK server` empty before the final build.

| Run | Breaks | Result |
|---|---|---|
| build 1 | none | **333 passed**; image built. The 5 new facts passed; 328 is 333 minus those 5, not a separately measured before-count |
| red A | (1) hourglass z 27 to 28 in the office area table; (2) the shared placer never sees an existing addon; (4) the signs never named; (5) the Registrar's `WasAt` without the old facing | **328 passed, 5 failed**, each on its own break: fact 1 (area table differs at the hourglass, z 28 vs 27); fact 2 (6 addons, expected 3); fact 4 (name null); fact 5 (legacy facing West, expected North: it tripped on the declaration check before the world-load assertions); and **P16's `SeedingTwicePlacesExactlyTwoTents`** (4 tents, expected 2), expected, since break 2 is in the placer both now share |
| red B | (3) the flowerpot moved to 3457,2598 (the P17 doorway door's swing tile) and the globe to 3459,2601 (the Registrar's tile), in the area table only | **331 passed, 2 failed**: fact 3, naming both ("0x11CA at (3457, 2598, 18) is on where the doorway door swings", "0x1047 at (3459, 2601, 18) is on the Registrar's tile"); fact 1, expected (the table no longer matches the design) |
| final | none, restored and hash-checked | `docker/uo/build.sh -t sl-modernuo:cc-p19-office`: **333 passed**, "Built sl-modernuo:cc-p19-office with patches applied and 333 shard test(s) passing." Image `1fc199be9380`; `sl-modernuo:latest` still `33aef6969ccb` |

Not watched red separately: fact 3 with a prop on a **door** tile itself (red B moved props onto a swing tile and the
Registrar's tile; all five tiles go through the same check). The `Item.Amount <= 0` errors in every run's log come from
other facts' corpses and appear in all four runs.

---

## 6. Checklist for Chase

1. **Commit** with `D:\UO\Commit-ShardWork.ps1`. Six files in `D:\ShatteredLegacy` (section 2), plus this note and
   `notes/cc-P19-tools/` here.
2. **Rebuild the test shard** from the console ("Rebuild through the gates"); the gate should say 333 passed. That build
   retags `sl-modernuo:latest`; `sl-modernuo:cc-p19-office` is this task's image.
3. **On the test shard**, as Administrator:
   1. `[ClusterFSeedRegistrarOffice dryrun`: it should say it would place 3 of 3 (5, 10 and 3 components) and list
      nothing already on their tiles. Then `[ClusterFSeedRegistrarOffice`.
   2. `[ClusterFSeedNewHaven dryrun`, then `[ClusterFSeedNewHaven repair`: turns the Registrar West (and repairs any other
      New Haven NPC off its entry, as it always has).
   3. `[go 3460 2600 18` to look inside. Then walk in through the front door (3459,2596) and talk to the Registrar.
      Single-click both signs: "League of Extraordinary Citizens". Open the office doorway door (3457,2599) and look at
      where it swings (section 1.2: onto the desk on this world).
4. **Screenshot the office** for the overseer to compare with `design/registrar-office/after_interior_zoom.png`; one with
   the doorway door open as well.
5. **Live-world commands** (Administrator, in game, after the test shard looks right):

   | Command | What it does | Re-run |
   |---|---|---|
   | `[ClusterFSeedRegistrarOffice dryrun` | lists what would be placed; changes nothing | safe |
   | `[ClusterFSeedRegistrarOffice` | places the three prop addons (18 items); moves and deletes nothing | safe: an addon of that type already on Trammel is never placed again (fact 2) |
   | `[ClusterFSeedNewHaven dryrun` | lists NPCs it would create or repair; changes nothing | safe |
   | `[ClusterFSeedNewHaven repair` | turns the Registrar West; also moves or turns any other New Haven NPC off its entry, and creates missing ones | safe: a second run repairs nothing (an NPC on its entry is skipped) |

   **Live has neither P17 door** in the 2026-09-29 copy. If `[ClusterFSeedNewHavenServices` has not run on live, the
   office has an open doorway and no front door until it does; that is P17's step (its own checklist), independent of
   this one. **And after the next live start on an image with this change, she still faces North** until the repair
   command runs; that is by design.

Open, unverified:
- Nothing was run in a client: the look of the props, the signs' text in a client, and the door overlapping the desk.
- Whether a "fresh world" is meant to include `[DoorGen`, which decides which doorway door it gets (1.2).
- The chair static's own facing on her tile (1.4); whether the live save copy is current.
