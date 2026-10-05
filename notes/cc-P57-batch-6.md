# cc-P57: batch 6 (Seal prices, post-Valorite deed value, ore harvest by tier, our own clilocs, guildmaster choice, achievements layout, Stealing stacks)

Builder task, 2026-10-05. Brief: `D:\UO\cc-prompts\cc-P57-batch-6.md`. Engine authority: `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88` (`git rev-parse HEAD` today); every pinned file:line below is against it. TazUO
facts are at our shipped commit `3212623f` (clone `D:\UO\cc-p40-work\tazuo-3212623f`, P40's), checked against the shipped
binaries in `D:\UO\TazUO\client` (26.0909.63). `C\` = `D:\ShatteredLegacy\server\customizations`, `P\` = `server\patches`,
`T\` = `server\tests`, `PKG\` = `player-package`, `PIN\` = `D:\UO\ModernUO-pinned\Projects`. Scratch: `D:\UO\cc-p57-work\`
(`make-red.py` the red trees, `red1.log`, `red2.log`, `detail.log` the printed numbers, `tazprobe\` the TazUO probe).
Shard HEAD `b8e525d` (P56 committed), tree clean when I started. Nothing committed, nothing deployed, no shard restarted,
`sl-modernuo:latest` not moved (`9d6829869880` before and after), nothing published.

**Clash:** while I worked, someone else wrote in `D:\ShatteredLegacy`: `CHANGELOG.md` and `VERSION` (a 2026.10.05 section)
and a new `design\satchel-icons\` folder (files from 08:31 to 09:01). They are not mine and I did not touch them. Two of
the new CHANGELOG lines go stale with this batch: "Mining them still needs 100" (Part C) and the menu labels "Knowledge"
and "Use" (Part D). Whoever owns the CHANGELOG should update them.

## Headlines

1. **All seven parts done.** Final `docker\uo\build.sh -t sl-modernuo:cc-p57`: **46/46 patches** (45 plus
   `Stealing-stack-weight.patch`), **837/837 shard facts** (785 + 52 new cases in the seven new classes), image `sl-modernuo:cc-p57` = `d5519301f920`. Package: gates 1 to 6 and
   `-CheckZip` green on a fresh build in `D:\UO\cc-p57-work\pkg\`; package and Shard-Console tests green (9 + 8 + 20 + 95).
2. **Red then green.** Server red tree 1 (every part undone): **44 failed** / 793 passed. Red tree 2 (Part A's catch: the
   bank's item part reading the price): **13 failed**. Package red (the new cliloc facts against HEAD's package scripts):
   **9 of 9 failed**. The cliloc gate went red twice by hand: once in the staging build, once in `-CheckZip` on a doctored zip.
3. **Part A has a cost to name:** with prices x3 and the bank's item part at the old prices, a banked Seal buys a third of
   what it did, **including against OSI's own item**. Valued at the new prices, banking falls below what OSI hands a
   non-member on **553 of 918** deed shapes (a small iron 10 regular banks 52 Seals; the shovel OSI gives now costs 150).
   Bank >= OSI holds with OSI's item valued at the baseline (the unit the bank pays in): 918 of 918. Both cannot be true at
   once; this is the decision Chase asked for, and it is written as one below (decision 1).
4. **Part D: both P52 unknowns settled, with the shipped client:** TazUO reads `Cliloc.enu` through `-uofilesoverride`
   (`ClassicUO.Assets/ClilocLoader.cs:89` calls `GetUOFilePath`, which consults the override first,
   `UOFileManager.cs:103-108`, loaded first at `:144`), and it reads an uncompressed file as is (it decompresses only when
   byte 3 is 0x8E, `ClilocLoader.cs:123`). Proved by a probe that loads the **shipped** `ClassicUO.Assets.dll`, points the
   override at our file and calls the client's own `Clilocs.Load("enu")`: 1900000 "Breed", 1900001 "Smelt Ore", 1900002
   "Metal Familiarity", and EA's 3006132 "Use", 124,003 entries.
5. **Part G was real** (probed): pinned at Stealing 150 lifts a 15-stone pile of 150 ingots whole with a skill window of
   127.5 to 177.5. One clamp fixes it; at every Stealing up to 100 the code is byte-for-byte pinned's behaviour (facts G2).
6. **The "Requires?" in Chase's screenshot did not come from our text:** HEAD's source already wrote `Requires: ` (bytes
   checked; the fact F4 was green on the red tree). Two lines of the gump did use glyphs the client font lacks (U+2591 in
   the progress bar, U+2713 in the Quests tab; EA's `unifont1.mul` has no entry for either), and rows overlapped, so the
   "?" was most likely one of those or an overlap artifact. Unproven; every gump line is ASCII now and on its own line.

## What changed (all uncommitted)

Shard (`D:\ShatteredLegacy`):
- `C\SmithSealCatalogGump.cs` (A): `PriceFactor = 3`, each line's `BaseCost` (the cc-P56 price) and `Cost = BaseCost x 3`.
- `C\ClusterFSmithBODSystem.cs` (A, B, E): the comment on the bank, `ItemMultiplier`, the post-Valorite item part, the
  guildmaster's `AddCustomContextEntries` and `GuildmasterBulkOrderEntry`.
- `C\ClusterFMiningExtension.cs` (C): the post-Valorite harvest table follows `ClusterFMetalTiers`.
- `C\ShardClilocs.cs` (D, new), `C\PackMule.cs`, `C\CompactOreSatchel.cs`, `C\HammerOfHephaestus.cs` (D): the three numbers.
- `C\SmithBulkOrderChoiceGump.cs` (E): 400 wide, solid panel.
- `C\ClusterFAchievements.cs`, `C\ClusterFGumpText.cs` (new) (F): measured row heights, two tab rows, solid panels.
- `P\Stealing-stack-weight.patch` (new) and its argued comment in `docker\uo\apply-patches.sh` (G).
- Facts new: `T\Misc\SmithSealPriceVerification.cs` (A, B), `T\Engines\Harvest\PostValoriteHarvestVerification.cs` (C),
  `T\Misc\ShardClilocVerification.cs` (D), `T\Misc\GuildmasterBulkOrderChoiceVerification.cs` (E),
  `T\Misc\AchievementsLayoutVerification.cs` (F), `T\Skills\StealingStackWeightVerification.cs` (G), helper
  `T\Misc\GumpTextWidth.cs`. Updated: `SmithBankValueVerification` (valued at baseline; A2 prints the new-price count),
  `SmithRunicPricesVerification` (x3), `RegularSmithBODVerification` H7 (baseline), `SmithOrdersTeachVerification` fact 5
  (Celestial row), `ContextMenuLabelVerification` C1, `OreSatchelVerification` C1, `HammerHeldBonusVerification` (new numbers).
- Package: `PKG\payload\app\Build-UoOverrides.ps1` (the text half), `PKG\Build-PlayerPackage.ps1` (the cliloc gate, staging),
  `PKG\vendor\shattered-legacy-cliloc\entries.json` and `registry.csv` (new), `PKG\tests\Cliloc-Overrides.Tests.ps1` (new).
- No save shape changed; no migration JSON.

This repo: this note only.

## Part A: Seal catalog prices x3, the bank's item part at the old prices (P56 decision 1)

**Cause.** P56's bank pays the deed's gold x1.25 plus the catalog price of OSI's best item for the deed
(`OsiRungSeals`, checked against the live catalog). Raising prices would have raised the item part with them: nothing bought back.

**Change.**
- `C\SmithSealCatalogGump.cs:54-64`: `PriceFactor = 3`; each catalog line keeps the old price as `BaseCost`, and the gump
  charges `Cost = BaseCost x PriceFactor`. One factor for every line, so the ladder and every relation stay.
- The bank's item part reads `OsiRungSeals` (`C\ClusterFSmithBODSystem.cs:356-381`), constants equal to the baseline, so it
  does not move with the price. Fact A1 now rebuilds the ladder from `BaseCost`, so a baseline change not carried into the
  table still fails the build. The gold part is unchanged.
- **Bank >= OSI, re-run:** 918 shapes, 0 failures, tightest 0.12 Seals (small iron 15 regular), with OSI's item valued at
  the baseline. Valued at the new price, 553 of 918 fall below (headline 3). Rule argued: the Seal is the unit the bank pays
  and OSI's item is valued in that unit at the baseline; the catalog price is now a sink above it. The other rule the brief
  allows (item part reads the price) is exactly the catch; red tree 2 is that rule and fact P2 catches it.
- Existing Seal balances: untouched (fact A5, and nothing rescales them).
- **Factor: x3 kept.** x5 would put a Valorite runic at about 18 hours of dedicated play (below); x3 at about 10.7. Both
  are "long goal" territory; x3 is the smallest step that makes the Gold runic an evening's work rather than an hour.

**Pace** (my estimate: a dedicated crafter with ingots on hand fills about **10 small deeds and 1 large an hour** at the
guild, which has no cooldown, only the 3 small / 1 large cap; not measured). Seals per deed are the build's own averages
over 2,000 small and 1,000 large deeds generated for a member (fact P3): 316.7 small / 1,036.4 large at 100 Blacksmithy,
332.6 / 1,142.7 at 120. So about 4,200 Seals an hour at 100, 4,470 at 120. The bank is the same before and after; only
prices change.

| Item | Old price | New price | Hours at 100 before | after | Hours at 120 before | after |
|---|---|---|---|---|---|---|
| Sturdy Shovel | 50 | 150 | 0.01 (0.7 min) | 0.04 (2.1 min) | 0.01 | 0.03 |
| Mining Gloves +5 | 600 | 1,800 | 0.14 (8.6 min) | 0.43 (26 min) | 0.13 | 0.40 |
| Smith Guild Salvage Bag | 250 | 750 | 0.06 (3.6 min) | 0.18 (11 min) | 0.06 | 0.17 |
| Gold Runic Hammer | 3,600 | 10,800 | 0.86 | 2.57 | 0.81 | 2.42 |
| Valorite Runic Hammer | 15,000 | 45,000 | 3.57 | 10.71 | 3.36 | 10.07 |
| Platinum Runic Hammer (coming soon) | 22,500 | 67,500 | 5.35 | 16.06 | 5.04 | 15.11 |

**Facts** (`T\Misc\SmithSealPriceVerification.cs`): P1 (4 categories) every price is the old one x3 and its baseline the
old one; P2 (8 rows) the stock-metal rows of P56's table bank exactly what they banked under P56 (52, 305, 579, 264, 739,
2,386, 16,886, 9,001); P3 (100, 120) the pace numbers above. Plus `SmithBankValueVerification` A1 to A5 and
`SmithRunicPricesVerification` (now x3, buy button charges 10,800 / 16,200 / 27,000 / 45,000).

## Part B: post-Valorite item part scales at half the gold step (P56 decision 2)

**Change** (`C\ClusterFSmithBODSystem.cs:416, :445-459`): `ItemMultiplier = 1 + (goldMultiplier - 1) / 2`, applied to the
larger of the deed's own rung and its Valorite rung, rounded up. Platinum x1.25, Toxic 1.5, Blaze 1.75, Frost 2.0, Obsidian
2.25, Mythril 2.5, Adamantium 2.75, Celestial 3.0. Gold part unchanged.

**Table** (exceptional plate, 20, middle of the gold roll; printed by fact B1; "before" is P56's bank):

| Metal | Small: gold part + item | Small before | Small after | Large: gold part + item | Large before | Large after |
|---|---|---|---|---|---|---|
| Platinum | 170 + 300 x1.25 | 470 | **545** | 2,829 + 15,000 x1.25 | 17,829 | **21,579** |
| Toxic | 227 + 300 x1.5 | 527 | **677** | 3,771 + 15,000 x1.5 | 18,771 | **26,271** |
| Blaze | 283 + 300 x1.75 | 583 | **808** | 4,714 + 15,000 x1.75 | 19,714 | **30,964** |
| Frost | 340 + 300 x2 | 640 | **940** | 5,657 + 15,000 x2 | 20,657 | **35,657** |
| Obsidian | 396 + 300 x2.25 | 696 | **1,071** | 6,599 + 15,000 x2.25 | 21,599 | **40,349** |
| Mythril | 453 + 300 x2.5 | 753 | **1,203** | 7,542 + 15,000 x2.5 | 22,542 | **45,042** |
| Adamantium | 510 + 300 x2.75 | 810 | **1,335** | 8,485 + 15,000 x2.75 | 23,485 | **49,735** |
| Celestial | 566 + 300 x3 | 866 | **1,466** | 9,428 + 15,000 x3 | 24,428 | **54,428** |

At the new prices a large Celestial exceptional plate deed buys 1.2 Valorite runics (45,000); a Celestial runic (450,000,
coming soon) is about 8 such deeds. Metals still bank in order (A4 green).

**Facts:** B1 (16 rows) the table: after = gold part + ceil(item x multiplier), multiplier as listed, after > before.
`SmithOrdersTeachVerification` fact 5's Celestial range moved by +30,000 (53,438 to 55,417).

## Part C: post-Valorite ore harvest needs its tier, like OSI's metals (P56 decision 3)

**Stock's rule, cited:** pinned's mining table (`PIN\UOContent\Engines\Harvest\Mining.cs:115-187`) gives Dull Copper ..
Valorite `reqSkill` 65, 70, 75, 80, 85, 90, 95, 99, and the forge smelts them at the same 65 .. 99
(`PIN\UOContent\Items\Resources\Blacksmithing\Ore.cs:168-179`). Each window is `reqSkill - 40` to `reqSkill + 40` (Dull Copper
25-105 .. Valorite 59-139); iron 0, 0-100.

**Change** (`C\ClusterFMiningExtension.cs:94-111, :153-157`): each post-Valorite ore: required = its tier
(`ClusterFMetalTiers`), window tier - 40 to tier + 40. Platinum 112.5 (72.5-152.5) .. Celestial 200 (160-240). Before:
required 100 for all (windows 65-140 .. 80-155).

- **Vein weights:** unchanged (8 .. 1, 1,036 in all, fact C4); veins stay permanent.
- **A miner under the tier** in such a vein gets the vein's fallback, iron, every time, as stock does for a Valorite vein
  under 99 (`HarvestSystem.MutateResource`, `PIN\UOContent\Engines\Harvest\Core\HarvestSystem.cs:346-349`). At the tier they
  get the ore when the vein does not fall back (stock's 50%) and the skill check passes: (skill - min) / 80, so one half at
  the tier, as Valorite at 99. Celestial's window runs to 240, so at the 200 cap it stays at one half. The Gargoyle's
  Pickaxe still bumps a vein to the next one (Valorite to Platinum), where a miner under 112.5 gets iron.
- Harvest and smelt now line up for every metal; P56's "dig what you cannot smelt" gap is closed.

**Facts** (`T\Engines\Harvest\PostValoriteHarvestVerification.cs`): C1 the eight requirements and windows; C2 a tenth under
the tier gives iron at rolls 0, 0.5 and 0.99, at the tier the ore; C3 iron and the eight stock colors unchanged, same under/at
behaviour; C4 vein weights.

## Part D: our own client clilocs (P56 Part C proposal)

### The two unknowns (settled first)

1. **Does `-uofilesoverride` cover `Cliloc.enu`? Yes.** `ClilocLoader.Load(lang)` builds the name `Cliloc.enu` and calls
   `FileManager.GetUOFilePath` (`TazUO src\ClassicUO.Assets\ClilocLoader.cs:69-72, :89`); `GetUOFilePath` looks the
   lowercased name up in the override map first (`UOFileManager.cs:103-108`); the map is loaded before any loader
   (`UOFileManager.cs:144`, Clilocs at `:150`). The list's key is lowercased (`ClassicUO.IO\UOFilesOverrideMap.cs:40`), so
   `cliloc.enu=<path>` matches. With a language other than enu, the client reads `Cliloc.enu` (ours) for English and the
   other file over it (`:97-108`); our numbers are in no other file, so ours still show.
2. **Does it accept the uncompressed format? Yes.** `ReadCliloc` decompresses only when byte 3 is 0x8E (`:123`, the version
   test there is commented out); an uncompressed table starts `02 00 00 00 01 00`.
3. **Proved against the shipped binaries**, not only the source: `D:\UO\cc-p57-work\tazprobe\` references
   `D:\UO\TazUO\client\ClassicUO.Assets.dll`, `ClassicUO.IO.dll`, `ClassicUO.Utility.dll` (26.0909.63), sets the override list
   to the one `Build-UoOverrides.ps1` wrote, and calls the client's own `fm.Clilocs.Load("enu")`. Output: the path resolves to
   our copy; 1900000 Breed, 1900001 Smelt Ore, 1900002 Metal Familiarity, 3006132 Use, 3006143 Smelt, 1112530 Knowledge,
   3006152 Bulk Order Info; 124,003 entries. Not yet seen in a running client on screen (For Chase, check 10).

### The pipeline

- **Our entries:** `PKG\vendor\shattered-legacy-cliloc\entries.json` (228 bytes: the block and three entries), shipped as
  `app\cliloc-entries.json`. **Registry:** `PKG\vendor\shattered-legacy-cliloc\registry.csv`, beside the art registry: the
  block **1,900,000 to 1,999,999** and one row per number (never reuse one). Counted in EA's `Cliloc.enu` today: 124,000
  entries, highest below 3,000,000 is 1,166,081, **0** in 1,200,000-2,999,999, highest 3,011,032.
- **Step** (`PKG\payload\app\Build-UoOverrides.ps1`, run by `Play.ps1` before every start, as for the art): reads the
  player's `Cliloc.enu` (only read), decompresses it (TazUO's `BwtDecompress`, BSD 2-Clause, ported to C# 5 for Windows
  PowerShell's `Add-Type`), inserts our entries in number order, writes the table uncompressed to `app\uo-overrides\Cliloc.enu`
  and adds `cliloc.enu=<path>` to `files-override.txt`. A stamp (`cliloc-stamp.txt`: the source's size and time, our entries'
  SHA-256) skips the work when nothing changed: **1.4 s** to build against EA's file (compile included), **14 ms** when
  unchanged. An EA patch or a package with new entries rebuilds. A number of ours that the player's file already uses is
  skipped with one yellow line, EA's text kept.
- **Art and text are independent now:** either failing is one yellow line and the other still ships; only when neither
  produced anything does the game start without an override (the old all-or-nothing behaviour is kept for the art alone,
  so `Build-UoOverrides.Tests.ps1`'s 8 facts pass unchanged).
- **Size:** 5,061,718 bytes written (EA's table 5,061,666 + 52 for our three entries).
- Nothing of EA's ships: gate 4 still refuses any `uo-overrides` path and EA names; `cliloc-entries.json` is ours.

### Server side

`C\ShardClilocs.cs`: `Breed = 1_900_000`, `SmeltOre = 1_900_001`, `MetalFamiliarity = 1_900_002`. The pack mule's breed entry
(`C\PackMule.cs:233-235`), the ore satchels' smelt entry (`C\CompactOreSatchel.cs:311-316`) and the hammer's entry
(`C\HammerOfHephaestus.cs:928-930`, "Knowledge" before) use them. **Packet path:** pinned sends any number above 0x7FFF as is
(`PIN\Server\ContextMenus\ContextMenuEntry.cs:39-48`); a menu holding a number outside 3,000,000-3,032,767 needs the newer
packet (`ContextMenu.cs:51-54`), which a 7.0 client gets (`ContextMenuSystem.cs:149`) and which writes the number as an
int32 (`:189-191`). Fact D1 reads it off the wire.

### A player who has not updated

TazUO looks the number up in its table (`PopupMenuGump.cs:49`); a number it does not have gives `null`, which draws as an
empty label (`RenderedText.Create` turns it into ""), and the click box is the label's size (`:67`), so the row is **blank and
cannot be clicked**: the mule cannot be bred, the satchel cannot smelt, the hammer's panel cannot be opened from the menu.
The server cannot tell which table a client has (no packet says), so it cannot fall back per player. Options: (a) publish the
package before the server deploy and rely on the launcher's update offer (it asks at every start, `Play.ps1:221-246`); (b)
hold this server change until the package has been out a while. **Recommended (a)**, in that order (For Chase, steps 1-4).
Staff and anyone starting `TazUO.exe` directly bypass the step and see blank rows.

### Gates and facts

- **Cliloc gate** (`PKG\Build-PlayerPackage.ps1`, `Test-ClilocEntries`): the file is plain ASCII (no BOM, printable bytes
  and line breaks only), parses, the block is 1900000-1999999, every number is in it, once, with a non-empty printable text
  that matches `registry.csv`. Run on the vendored file before staging (throws "CLILOC GATE") and on
  `app/cliloc-entries.json` in the finished zip (gate 4). Watched red: staging with 1900002 changed to 2900002 stopped the
  build; a zip with a non-ASCII text failed `-CheckZip` ("not plain ASCII (2 other bytes, the first 0xC3)").
- **Package facts** (`PKG\tests\Cliloc-Overrides.Tests.ps1`, 9): round trip on a synthetic file (our entries in order,
  every other byte identical, uncompressed header); a taken number skipped and said; stamp skip and rebuilds; no
  `Cliloc.enu` is one yellow line and the art still ships; EA's real file read only (hash unchanged), all 124,000 entries
  identical in the copy, in order, ours added (skips, saying so, on a machine without it); the shipped entries pass the gate;
  eight bad files fail it; server constants = entries.json = registry; `Play.ps1` in a sandbox starts the game with the list
  holding `cliloc.enu=`.
- **Server facts** (`T\Misc\ShardClilocVerification.cs`): D1 (3) the mule, satchel and hammer menus on the wire carry
  1900000, 1900001, 1900002 and not 3006132, 3006143, 1112530; D2 the numbers are in the block.

## Part E: guildmaster Small/Large, and the choice gump's layout (D81)

**Cause.** The guildmaster's stock "Bulk Order Info" (`PIN\UOContent\Mobiles\Vendors\BaseVendor.cs:1330-1332`) calls
`CreateBulkOrder`, our override of which calls `TryCreateBOD` (`C\ClusterFSmithBODSystem.cs:101-105`): a deed, no choice. The
hint "Bank: Seals. Cash out: gold, a chance at an item." is **297 pixels** in the client's label font at x 54, so it ended
at 351 in a 340-wide gump. The gump drew an alpha region.

**Change.** `C\ClusterFSmithBODSystem.cs:77-91`: the guildmaster's `AddCustomContextEntries` swaps entry 3006152 for
`GuildmasterBulkOrderEntry` (`:598-619`), which opens `SmithBulkOrderChoiceGump` (members only, as the stock entry was).
`C\SmithBulkOrderChoiceGump.cs:30-36, :55-56`: 400 wide (widest label now ends at 353 of 400), tile 2624 under the inside
instead of the alpha region, as the Staff Hub (P52 F). The text widths are real glyph widths: EA's `unifont1.mul`, the font
TazUO draws gump labels and HTML in (`RenderedText.cs:50-60` maps 0xFF to font 1; `HtmlControl.cs:63`), widths summed as
`FontsLoader.GetWidthUnicode` does (`:1230-1255`), table in `T\Misc\GumpTextWidth.cs` and `C\ClusterFGumpText.cs`.

**Facts** (`T\Misc\GuildmasterBulkOrderChoiceVerification.cs`): E1 the menu has 3006152 once, clicking it opens the choice and
hands out no deed (red tree: a deed and the accept gump); E2 every label ends inside the frame for every mode, teaching on and
off, 50 and 100 skill, with and without Back; E3 opaque in every state.

## Part F: achievements gump layout (D80)

**Causes.** Rows were a fixed 64 pixels, five a page, but an earned row with a wrapped flavor, an Earned line and a progress
line needs up to 5 lines (90 pixels), so its last line ran under the next title. Tab labels sat at button + 18 over a 30-wide
button (EA's gump 4011 is 30 x 22, read from `gumpartLegacyMUL.uop`) and were cut to fit one row ("Discov"). Alpha region.
Glyphs the font lacks: U+2591 (progress bar), U+2713 (Quests), and the 16-pixel U+2501 dashes ran headings past the frame.

**Change** (`C\ClusterFAchievements.cs`): each row is built as lines of colored runs (`RowLines`), measured with
`ClusterFGumpText` 8 pixels short of its block, and gets `lines x 18 + 4` pixels (at least the icon's 48); a page holds the
whole rows that fit above the pager (`Paginate`). Lines: title and points; flavor or description; the Earned line on its own
line; **"Requires: <title>" on its own line** under the description; "Progress: n/m". Tabs: full words (All, Combat, Skills,
Exploration, Mining / Crafting, Legacy, Discovery, Quests) in two even rows of fixed 108-pixel columns, labels at button + 34.
Text starts at 68 beside an icon (the widest icon, 0x1B76, is 50 x 44). ASCII headings and "[x]" in Quests. Solid tile 2624
on the gump and on the Achievement Unlocked popup (the popup's layout is unchanged; it fit, with at most 4 lines in its 5).

**Facts** (`T\Misc\AchievementsLayoutVerification.cs`): F1 every page of nine tabs (105 rows): each block at least as tall as
its wrapped lines, no row or heading overlaps another, icons end inside their row, all between the tab rule and the pager,
every label ASCII and inside the frame; F2 nine full words, rows of five and four in the same columns, each label clear of its
button and the next column; F3 opaque gump and popup; F4 "This Is Fine" reads "Requires: Getting Into It" on its own line;
F6 all 74 popups fit (most lines: 4).

## Part G: Stealing stack exploit (D82)

**Probe first** (`T\Skills\StealingStackWeightVerification.cs`, against the tree as it was, red tree 1): pinned's private
`StealingTarget.TryStealItem` called by reflection, the skill check recorded through `Mobile.SkillCheckTargetHandler`, the
amount roll at its top. Stealing 150 and a 15-stone pile of 150 ingots: the whole pile, window **127.5 to 177.5**; 200 and
200 ingots: window 177.5 to 227.5. Red. So the flaw P54 read is real: the unit weight passes the 10-stone test
(`PIN\UOContent\Skills\Stealing.cs:261-263`) and the amount is up to Stealing / 10 stones (`:272-276`).

**Rule argued.** OSI documents "You may not take items that weigh more than your skill level divided by 10" (UOGuide,
Stealing) and OSI's top Stealing is 100, so 10 stones; pinned and ServUO pub57 both hard-code the same 10 for an item
(`MaxWeightToSteal`, `Stealing.cs:33`; pub57 `Scripts\Skills\Stealing.cs:291`) and both compute the stack amount from skill / 10
(pub57 `:299`), which never exceeds 10 at their caps. OSI and both servers let a thief take **part** of a heavier pile, so
"the weight test uses the whole pile" taken literally (refuse any pile over 10 stones) would depart from them. The rule:
**what is taken, a part or the whole pile, weighs no more than `MaxWeightToSteal`**: `maxAmount` from
`min(Stealing / 10, MaxWeightToSteal)` (`P\Stealing-stack-weight.patch`, one line). A whole pile is then taken only when it
weighs 10 or less, and no window passes 127.5, the single-item path's own top. At every Stealing up to 100 this is
identical to pinned. **No deviation line:** it is OSI's rule at OSI's range; it departs from nothing OSI had.
Alternatives rejected in `apply-patches.sh` (whole-pile test before a partial steal; capping the window numbers; a
customization, impossible because the target class is private).

**After:** 150 or 200 with 15 or 20 stones: takes 100 ingots (10 stones), window 77.5 to 127.5. **Normal steals** (G2,
30/60/90/100, a 5-stone pile and a single 5-stone item): the same amount and window as pinned's formula (e.g. 30: 30 ingots,
7.5 to 57.5).

**Does the flaw let Stealing gain anywhere else?** No other path: the sigil check is (80, 80), no gain
(`Stealing.cs:185`); the single item is capped at 10 stones (`:263`, window to 127.5); the pickpocket dip gains up to its
`MaxSkill` and refuses at it (`Items/Addons/PickpocketDips.cs:61, :85`). With the patch Stealing's gain stops at 127.5
everywhere. **Still open (not this batch):** "never caught from 150" reads `Stealing.Value` (`:337`), and item and temporary
bonuses count above the cap since cc-P53 C (D-113): Shadow Dancer Leggings +20, Burglar's Bandana +10, our Mark of Travesty
+10, Animal Form +10, so a 127.5 thief with gear reads 150 and is never caught. Decision 4.

**P54's Hiding and guard thresholds** (from `notes\cc-P54-scratch\b-thief-heal.md`, not re-probed): Hiding gains stop at 100
today (`Skills/Hiding.cs:73`). The hide-in-combat range `min((100 - H) / 2 + 8, 18)` (`Hiding.cs:53`) is 8 at 100, 3 at
110, 1 at 114, 0 at 116 and negative from **118**, where combat no longer blocks hiding. Guards have Detect Hidden 100
(`ArcherGuard.cs:64`, `WarriorGuard.cs:81`) and the contest is +/-10 (`DetectHidden.cs:197-198`), so Hiding **121+** is
invisible to guards; the Slasher of Veils (DH 127.1) is blind from 148. None is reachable while Hiding stops at 100; any
Hiding gain path must ship with those clamps (P54).

## Facts, red then green

| Fact | Red | Green |
|---|---|---|
| A: P1 (4), `SmithRunicPricesVerification` (5) | red1 (factor 1) | green |
| A: P2 (8) | **red2** (the catch); green on red1 by design (the bank never moved) | green |
| A: P3 (2), `SmithBankValueVerification` A1-A5 | **never red by design**: guards (pace numbers; bank >= OSI at baseline) | green |
| A/B: `SmithOrdersTeachVerification` fact 5 | red1 (Celestial row, B) and red2 (4 rows) | green |
| B: B1 (16) | red1 | green |
| C: C1, C2 | red1 | green |
| C: C3, C4 | **never red by design**: stock ores and weights unchanged | green |
| D: D1 (3), D2, `ContextMenuLabelVerification` C1, `OreSatchelVerification` C1, `HammerHeldBonusVerification` (2) | red1 | green |
| E: E1, E2, E3 | red1 | green |
| F: F1, F2, F3 | red1 (HEAD's gump) | green |
| F: F4, F6 | **never red**: HEAD already said "Requires:" and its popup fit (headline 6) | green |
| G: G1 (2) | red1 (no patch: windows to 177.5 and 227.5) | green |
| G: G2 (4) | **never red by design**: normal steals as pinned | green |
| Package: `Cliloc-Overrides.Tests.ps1` (9) | 9/9 red against HEAD's package scripts | 9/9 |
| Cliloc gate (staging, `-CheckZip`) | red by hand, both | green |

red1: 837 tests, **44 failed**, 793 passed. red2: 837 tests, **13 failed** (P2 8, fact 5 4, A4 1), 824 passed.

## Builds

| Build | Command | Result |
|---|---|---|
| 1 | `build.sh -t sl-modernuo:cc-p57 --tests-only` | **46/46 patches; 837/837** |
| red1 | `red1\docker\uo\build.sh -t sl-modernuo:cc-p57-red1 --tests-only` | 45/45 (no Stealing patch); 837, 44 failed |
| red2 | `red2\docker\uo\build.sh -t sl-modernuo:cc-p57-red2 --tests-only` | 46/46; 837, 13 failed |
| detail | `dotnet test` in `sl-uo-builder:cc-p57`, the seven new classes, verbosity detailed (no image) | 69/69; numbers in `detail.log` |
| final | `build.sh -t sl-modernuo:cc-p57` | **837/837, image `d5519301f920`**; builder stage a cache hit on build 1 (same inputs), so its 46/46 is build 1's; `latest` still `9d6829869880` |
| package | `Build-PlayerPackage.ps1 -Out D:\UO\cc-p57-work\pkg` | gates 1-6 green; `ShatteredLegacy-2026.10.05.0853.zip`, 76 MB, 740 files |
| package | `-CheckZip` on it | gates 4, 5, 6 passed |
| package tests | `Cliloc-Overrides` 9/9, `Build-UoOverrides` 8/8, `Launch-Settings` 20/20; `scripts\tests\Shard-Console` 95/95 | green |

The 110 "Item.Amount <= 0" stack traces in each server log are pre-existing (P56's logs have the same 110). Docker answered
throughout. Builder tags made: `sl-uo-builder:cc-p57`, `-red1`, `-red2`. The package zip in `D:\UO\cc-p57-work\pkg` is a test
build, not for publishing (it records "uncommitted player-package changes"); build again after the commit.

## Deviations and decisions for you

Register lines (next free D-121):
- **D-121 Ours (cc-P57 A, Chase 2026-10-05).** Seal catalog prices are three times their cc-P56 values; the bank values OSI's
  item at the old price, so a banked deed buys a third of the item OSI hands a non-member for it. | Seals buy less | `visible`
- **D-116 (amend), cc-P57 B:** a post-Valorite deed's item part is multiplied by 1 + (m - 1) / 2 (Platinum 1.25 .. Celestial 3).
- **D-119 (amend), cc-P57 C:** post-Valorite ore also needs its tier to mine (window tier +/- 40, stock's pattern); "Harvest
  stays at 100" is gone.
- **D-120 (amend), cc-P57 D:** the pack mule says "Breed" (our cliloc); the trash bag stays on stock "Clean Up Britannia".
  Our numbers 1,900,000+ ship with the package (not an OSI deviation; a client-policy note under
  `client-policy-2026-10-02.md`).
- The existing Small/Large choice deviation (cc-P42 F) now also covers the guildmaster's single-click menu (E).
- Part G: none (OSI's rule at OSI's range).

Decisions:
1. **Part A's trade (headline 3):** prices x3 with the bank at the old prices means members get a third of OSI's item per
   deed in buying power (553 of 918 shapes below OSI at new prices). If that is not wanted, the only way to keep "bank >= OSI
   in buying power" is the item part reading the price, which makes the rise buy back nothing on item-heavy deeds. A middle
   course: a smaller factor (x2) or pricing only the runic hammers up.
2. **Part B:** a large Celestial exceptional plate deed is 54,428 Seals (1.2 Valorite runics at new prices). Say if that is
   still too steep.
3. **Part D rollout:** publish the package before deploying the server, or un-updated players see blank, unclickable
   entries (no server fallback is possible).
4. **Stealing above 150 by gear:** never caught from 150 reads Value, and bonuses count above cap (D-113). Clamp the caught
   test to Base, or to 100 + something? Not built.
5. **The popup** is opaque now too, for the same reason as the gump; one line to undo if you preferred it translucent.
6. **CHANGELOG lines** another writer added today go stale with C and D (Clash, top).

## For Chase

Package first (Part D), then the server. Commands in Windows PowerShell; build commands from Git Bash where noted.

1. Commit both repos (P57 is uncommitted; the CHANGELOG/VERSION/`design\satchel-icons\` changes are someone else's).
2. Build the package from the commit: `D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1 -Notes "Our own menu words: Breed, Smelt Ore, Metal Familiarity"`
   (gates 1-6 must pass), then `D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1 -CheckZip <the new zip>`.
3. Publish it as usual (`D:\UO\haven-migration\Publish-PlayerPackage.ps1`, per `docker\downloads\README.md`), then run `Play TEST Shard.bat` on your PC and accept the update.
4. Check the copy was made: `Get-Content "<your Shattered Legacy folder>\app\uo-overrides\files-override.txt"` shows a
   `cliloc.enu=` line.
5. Deploy the server to the test shard: `docker tag sl-modernuo:cc-p57 sl-modernuo:latest`, then
   `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -Down`, then `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild`.

In game on the test shard:

6. **Prices (A):** open the Seal catalog: Sturdy Shovel 150, Mining Gloves +5 1,800, Salvage Bag 750, Valorite runic 45,000.
   Hand in a small iron 10 regular deed as a member: still +52 Seals.
7. **Post-Valorite (B):** `[add SmallSmithBOD` until a Celestial exceptional 20, fill it (`[SetSkill Blacksmith 200`), bank it:
   about 1,466 Seals (was about 866).
8. **Mining (C):** `[SetSkill Mining 112.4`, mine in a Platinum vein (`[go` to one you know): iron only. `[SetSkill Mining 112.5`:
   Platinum ore about half the time.
9. **Guildmaster (E):** single-click the Society guildmaster, Bulk Order Info: the Small/Large gump opens, opaque, and the line
   under "Completed orders" fits.
10. **Menu words (D):** single-click your tamed pack mule: "Breed"; a Reinforced Ore Satchel in your pack: "Smelt Ore"; a Hammer
    of Hephaestus in your pack: "Metal Familiarity" (opens the panel). Then start `app\tazuo\TazUO.exe` directly (no launcher,
    no override) and single-click the mule: the breed row is blank (what an un-updated player sees).
11. **Achievements (F):** `[achievements`, page through All and Combat: no row overlaps, tabs read in full on two rows, the
    gump is opaque; "This Is Fine" shows "Requires: Getting Into It" on its own line.
12. **Stealing (G):** a thief at `[SetSkill Stealing 150`, a pile of 150 iron ingots in a pack on the ground beside you: a
    steal takes at most 100 (10 stones), never the whole pile.
13. Promote to `docs\`: D80, D81, D82 closed in `bug-list.md`; D-121 and the amendments in `fidelity-principle.md`; the cliloc
    block in the client policy.

P57 DONE
