# CC task P236: Chase's satchel and guild bag icons, shipped

Iron, 2026-10-21. Both repos were clean on `golem/Iron/P236` when I started.

## Headlines

- **Six of the ten approved icons ship**, as new art IDs **0x3380-0x3385** (13184-13189). They go to fourteen classes:
  - ore satchel: all five ore tiers;
  - lumber satchel: all three lumber tiers;
  - hunter's satchel: all three hunter tiers;
  - the Artificers' Essence Satchel, now in the decided purple **0xDC**;
  - the Gemologist's Satchel;
  - the Smith Guild Salvage Bag.
- **Four icons wait for an item**, because no class exists for them yet: the Arcane Society reagent pouch (hue 0x12B
  decided), the tailor's cloth satchel, the maritime fisher's creel and the Healers' Covenant satchel. The table below
  says which guild each one waits on.
- **Satchels already in the world move over on load.** Each family's base class is now saved as version 1. A version 0
  item still on its stock graphic takes the new icon. An item a staff member gave another graphic keeps it, and so
  does an Artificer's Satchel a staff member gave another hue. A version 1 item is never moved, so staff can set the
  stock graphic back later.
- **Nothing else about the containers changes.** Each keeps the gump, bounds and drop sound it had: the satchels 0x3C,
  the two bags the stock bag's 0x3D. Tests prove it.
- **The lumber tier hues are not green**, as the queue entry said. 0x84C is dark blue, 0x60 light blue and 0x26C purple
  (render below). I changed nothing; a proposal is under decisions.
- **The player package carries the art.** It was built to scratch with every gate green and holds the six PNGs byte for
  byte and the six records. Not published. A player without the update sees each slot's "UNUSED" placeholder.

## Part 1: icons and classes

| Icon (design\satchel-icons\) | Art ID | Classes | Hue each class sets |
|---|---|---|---|
| `ore_satchel` | 0x3380 / 13184 | `CompactOreSatchel` (T1), `ReinforcedOreSatchel`, `SurveyorsSatchel`, `DeepdelversSatchel`, `MasterExpeditionSatchel` | the tier's metal (cc-P55): none, Gold, Verite, Valorite, Platinum |
| `lumber_satchel` | 0x3381 / 13185 | `ForestersLumberSatchel`, `SeasonedLumberSatchel`, `ArboristLumberSatchel` | 0x84C, 0x60, 0x26C (unchanged; Part 5) |
| `hunters_satchel` | 0x3382 / 13186 | `HuntersSatchel`, `SeasonedHuntersSatchel`, `WardensFieldSatchel` | 0x5B5, 0x5B2, 0x4B5 (unchanged) |
| `artificers_satchel` | 0x3383 / 13187 | `ArtificersSatchel` | **0xDC** (was 0x497) |
| `gemologists_satchel` | 0x3384 / 13188 | `GemologistsSatchel` (`Items\Containers\`) | 1177 (unchanged) |
| `smith_guild_salvage_bag` | 0x3385 / 13189 | `SmithGuildSalvageBag` | 1154 (unchanged) |

What the prompt's citations say now (re-verified on this tree):
- `HuntersSatchel.cs:109` was `base(0xA272)`.
- `SmithGuildSalvageBag.cs:35` was `BagItemID = 0xE76`.
- `ArtificersSatchel.cs:32-33` was 0xA272 and hue 0x497. The prompt said `:33` `0xA272`; the graphic was on `:32`.
- The ore and lumber tiers do derive from `CompactOreSatchel` and `ForestersLumberSatchel`.
- `GemologistsSatchel` is a `Bag` (stock 0xE76).

**Not shipped: the icons with no item.** `grep` over `server\customizations` and `server\patches` finds no class
for any of these four.

| Icon | Waits on |
|---|---|
| `arcane_society_reagent_pouch` (hue 0x12B decided) | the Arcane Society (mages' guild) |
| `tailors_cloth_satchel` | the tailors' guild |
| `maritime_fishers_creel` | the fishers' guild (Maritime) |
| `healers_covenant_satchel` | the Healers' Covenant |

The icons are kept in `design\satchel-icons\`. Shipping one later is a registry row, a PNG, a record and the class.

## Part 2: IDs, registry, PNGs, records

- **Slots.** I ran `python scripts\find-free-art.py --data D:\UO\UltimaOnlineVanilla --pinned D:\UO\ModernUO-pinned
  --placeholder --run 6`. It found 51 runs; the two longest were 0x337B-0x3420 (166 IDs) and 0x3C82-0x3D11 (144).
  - Bronze's P237 (not yet merged; read from its branch with `git show`, nothing checked out) takes 0x3C88-0x3CA9 from
    the second run. So I took **0x3380-0x3385**, 8-aligned, from the first, clear of anything P237 adds.
  - `--explain`: all six read "FREE; art placeholder".
  - `--check-registry` afterwards: "0 of 146 registered IDs are no longer free".
- **`registry.csv:148-153`**, written before the PNGs. Each row says what the icon is and which classes use it. Source:
  "Ours: Chase's own source art, made into a 44x40 icon by Codex (D:\ShatteredLegacy\design\satchel-icons\<name>.png,
  byte for byte ...)". License: "ours, Chase via Codex, 2026-10-05". Kind: art.
- **PNGs `art\13184.png` to `art\13189.png`**: the design files copied byte for byte (`cmp` identical). Each is 44x40
  RGBA, alpha 0 or 255, with 86 to 341 exact-gray pixels.
- **`records.json:32-37`**: one tiledata record each, copied from the stock graphic it replaces, plus PartialHue.
  Values read from `D:\UO\UltimaOnlineVanilla\tiledata.mul` (vseUOAware `get_item_tile`):

  | Stock graphic | Its record | Ours |
  |---|---|---|
  | 0xA272 "Ore_Satchel_east" | Container 0x00200000, weight 3, height 1 | 0x00240000, weight 3, height 1 (13184-13187) |
  | 0xE76 "bag" | Container \| ArticleA 0x00204000, weight 2, height 2 | 0x00244000, weight 2, height 2 (13188, 13189) |

  - Names, at most 19 ASCII characters: "ore satchel", "lumber satchel", "hunter's satchel", "artificer's satchel",
    "gemologists satchel" (the apostrophe would make 20), "smith salvage bag".
  - The `about` text says the same.
  - The client's slots hold no record (no name, flags 0), so the launcher's `Build-UoOverrides.ps1` writes ours. It
    skips only a slot EA has named (`:126`).
- **`SOURCE.txt:256`**: a section with author, license, files, the four held back, and where each record value comes
  from.
- **Server.** `server\customizations\SatchelArt.cs` (new):
  - the IDs and stock graphics (`:31-40`);
  - the decided hue and the old one (`:43-44`);
  - `Records` (`:46`), the server's copy of records.json, and `Apply` (`:56`);
  - `MoveFromStock` (`:65`).
  
  `ShatteredLegacyArt.Apply` (`ShatteredRunestone.cs:58-59`) calls `SatchelArt.Apply()`, as P34 and P50 did for their
  tables.

## Part 3: the classes

- `CompactOreSatchel.cs:89`, `ForestersLumberSatchel.cs:45`, `HuntersSatchel.cs:109`, `ArtificersSatchel.cs:32`,
  `SmithGuildSalvageBag.cs:35`, `GemologistsSatchel.cs:40`: each points at its `SatchelArt` ID. The subclasses
  construct through these, so all fourteen classes are covered.
- `ArtificersSatchel.cs:33`: hue `SatchelArt.ArtificersHue` (0xDC).
- **Gumps kept.** A container's gump, bounds and drop sound come from `containers.cfg` by ItemID (pinned
  `Server/Items/Container.cs:146-149`, `:187`).
  - 0xA272 has no line there, and neither do our IDs, so the satchels keep the default. Their own `DefaultGumpID` is
    0x3C.
  - The two `Bag` classes had 0xE76's line (gump 0x3D, bounds 29,34,108,94, sound 0x48). They now override
    `UpdateContainerData` to keep it (`SmithGuildSalvageBag.cs:53-54`, `GemologistsSatchel.cs:78-79`).
- **The Arcane Society hue 0x12B** has no class to go on yet (see Part 1).

## Part 4: items already in the world

- `[SerializationGenerator(0, false)]` became **`(1, false)`** on the six base classes:
  - `CompactOreSatchel.cs:50`, `ForestersLumberSatchel.cs:28`, `HuntersSatchel.cs:29`;
  - `ArtificersSatchel.cs:27`, `SmithGuildSalvageBag.cs:29`, `GemologistsSatchel.cs:6`.

  Their subclasses stay at version 0 and need nothing: the base layer carries the art.
- **Version 0 goes through each class's legacy `Deserialize(IGenericReader, int)`.** The generator calls it for a
  version that has no `MigrateFrom`, as pinned's `ChampionSkull` (version 2) does. These classes have no fields, so
  no `migrations\*.v0.json` is needed. In it, `SatchelArt.MoveFromStock` sets the new ID only if the item is still on
  the stock graphic:
  - `CompactOreSatchel.cs:338-340`, `ForestersLumberSatchel.cs:136-138`, `HuntersSatchel.cs:117-119`;
  - `SmithGuildSalvageBag.cs:49-51`, `GemologistsSatchel.cs:74-76`.
- `ArtificersSatchel.cs:149-159`: also 0x497 to 0xDC; any other hue stays.
- Setting ItemID while loading is safe here. Item's setter (pinned `Item.cs:628-646`) changes only the pile weight,
  and our record has the stock weight, so the weight change is zero. All the satchels set their own weight anyway.

## Part 5: the lumber tier hues (reported, not changed)

Rendered with the client's `hues.mul` the way the client does it: PartialHue, so only exact grays take the hue. The
render is `notes\cc-P236-art\lumber_hues.png`, made by `hue_sample.py` beside it.

| Code | Comment says | hues.mul name | Renders as (mid colour) |
|---|---|---|---|
| 0x84C (`ForestersLumberSatchel.cs:46`) | dark forest green | Birds #23 | **dark blue** (41,74,123) |
| 0x60 (`SeasonedLumberSatchel.cs:32`) | forest green | Hue (102->20319) | **light blue** (82,123,164) |
| 0x26C (`ArboristLumberSatchel.cs:20`) | teal/forest tint | Hue (3140->25209) | **purple** (115,90,123) |

The queue entry is right. Proposal under decisions.

`notes\cc-P236-art\in_game_hues.png` (`preview_in_game_hues.py`) shows every shipped icon in every class's hue, so you
can compare it with the client.

## Part 6: a client without the update, and the package

- **Without the update** the client draws each ID's own art, the "UNUSED" placeholder. `find-free-art.py
  --placeholder` picked these slots so that a missing update shows. The client also has no record for those slots, so
  the satchel shows no name; the server's name and properties still show. Updating fixes both.
- **With the update** the launcher puts the six PNGs in `app\tazuo\ExternalImages\art\` and writes the six records
  into its copy of the player's tiledata.mul.
- **The package build carries the art.** `Build-PlayerPackage.ps1 -Out <scratchpad>\pkg -UoData D:\UO\UltimaOnlineVanilla`
  ran under the `package` lock and passed every gate. Gate 4 checks one PNG per registered art ID. It built
  `ShatteredLegacy-2026.10.21.0643.zip`: 98 MB, 744 files, TazUO 3212623f + 3 patches.
  - The zip holds 116 art PNGs. The six are byte-identical to `art\13184.png`-`13189.png`, and `app\art-records.json`
    has the six records.
  - **Not published.**
  - The work copy had no `vendor\vc-runtime\vcruntime140.dll` (git-ignored). I copied it from the source its
    `SOURCE.txt` names (`C:\Program Files\Microsoft Visual Studio\18\Community\...\Microsoft.VC145.CRT\`). Its SHA-256,
    184146852727..., matches that file's. Still git-ignored (`.gitignore:69`).

## Tests

**Server: `server\tests\Items\SatchelIconsVerification.cs`, 44 test cases:**

| Fact | What it checks |
|---|---|
| `EachClassConstructsWithItsRegistryIdAndHue` (14 classes) | each class constructs with its registry ID and its hue; ore tiers their `TierHue`; the Artificer's 0xDC |
| `EachKeepsItsContainerGump` (14) | gump 0x3C (satchels) or 0x3D (bags), and the stock graphic's bounds and drop sound |
| `TheServerKnowsEachNewIdAsTheClientDoes` | `SatchelArt.Apply` puts six records in `TileData.ItemTable`: the name, PartialHue, Container, weight and height |
| `AnOldGraphicMovesOnLoadAndAStaffChoiceStays` (14) | round trip: a version 0 save on the stock graphic loads on the new ID; version 0 on another graphic (0xE75) keeps it; version 1 on the stock graphic keeps it; a new item keeps its ID |
| `AnOldArtificersSatchelTakesTheDecidedHueAndAStaffHueStays` | version 0 in 0x497 loads in 0xDC; version 0 in 0x21 keeps it |

The test writes a version 0 save by saving the item and setting the art layer's version to 0. `(n, false)` writes each
layer's version as a 4-byte int, and the layers below it have no fields. The test checks it finds a 1 there first.

**Package: `player-package\tests\Build-UoOverrides.Tests.ps1:403`,
`TheSatchelIconRecordsAreTheServersTableAndEachIsOursWithItsPng`.** It checks:
- `SatchelArt.Records` against records.json: IDs, order, names (at most 19 ASCII), flags by value, weight, height;
- PartialHue and Container set, and no animdata;
- six registry rows, license "ours, Chase via Codex, 2026-10-05";
- each a 44x40 PNG, the size read from the PNG header (no `Add-Type`).

The fact before it now leaves out 13184-13189 (`:251-253`) and counts 146 rows, 5 gumps and 116 art (`:291-296`).

Runs, all through `docker/uo/build.sh -t sl-modernuo:cc-P236 --tests-only` under the `docker-build` lock, started
detached:

| Run | Tree | Result |
|---|---|---|
| red 1 | tests plus a `SatchelArt` stub (empty table, marked P236-RED), classes as they were | did not build: my test declared `namespace Server.Tests.Items`, which the patch step refuses (`must declare 'namespace ShatteredLegacy.Tests'`). Fixed |
| red 2 | same | did not compile: xUnit1026 (theory parameters a method does not use). Fixed by logging them |
| **red 3** | same | **1956 tests, 30 failed, 1922 passed, 4 skipped. The 30 are exactly the new facts.** Construct: "Expected 13187, Actual 41586". Migration: the art layer saves as version 0. Server table empty. The 14 gump facts passed, as they should: they guard behaviour that must not change |
| green 1 | implementation | 15 failed: the migration facts, on the test's own check. It looked for a 1-byte version; `(1, false)` writes 4 bytes. The test's offset was fixed; the server code did not change |
| **green 2** | same | **1956: 1952 passed, 4 skipped, 0 failed** |
| **mutation** | five marked breaks (`P236-BREAK`): M1 ore moves to the lumber ID; M2 `MoveFromStock` ignores the staff's graphic; M3 the Artificer's hue never moves; M4 the Gemologist's container data follows its ItemID; M5 `Apply` drops PartialHue | **17 failed, each for its own break and no other test**: M1 the 5 ore migrations ("Expected 13184, Actual 13185"); M2 the other 9 ("Expected 3701", 0xE75); M3 the Artificer's hue ("Expected 220, Actual 1175"); M4 the Gemologist's gump ("Expected 61, Actual 60"); M5 the server-records fact |
| **final** | breaks restored by byte copy (`cmp` identical, no `P236-BREAK` or `P236-RED` left), plus CHANGELOG and VERSION | **1956: 1952 passed, 4 skipped, 0 failed**; the 44 satchel cases passed |

`--tests-only` builds no runtime image, so no `sl-modernuo:cc-P236` image exists. `sl-modernuo:latest` is untouched.

Package and art gates:

| Check | Result |
|---|---|
| `Build-UoOverrides.Tests.ps1`, red (the stub, no records) | the new fact FAIL: "expected [6] but got [0]. six records in C#" |
| same, green | **11 of 13 pass**. The 2 that fail, `PlayStarts...`, need the test shard ("Cannot reach TEST SHARD ... shatteredlegacyuo.com:2594"), as the file's header says |
| same, HEAD in a `git archive` copy (nothing checked out) | `TheServersCopyOfTheRecordsIsRecordsJsonAndEveryIdIsRegistered` already failed on main: "expected [137] but got [140]". P147's three gump rows never moved the count. Fixed here |
| `scripts\validate-art.py --data D:\UO\UltimaOnlineVanilla check-registry` | "0 of 146 rows have problems", the six "ok" |
| `find-free-art.py --check-registry` | "0 of 146 registered IDs are no longer free" |
| no EA file | the six PNGs are Chase's (registry and SOURCE.txt); the records are ours, values read from the client, nothing copied from EA's files |
| PNG count equals registry art rows | the build's gate 4 (116 = 116), and the package fact's six |

## Website credits

The design folder has no `SOURCE.txt`; the art is ours. Credit line if wanted: "Satchel icons: Chase, Shattered
Legacy". The registry rows and `SOURCE.txt:256` say the same.

## Deviations and decisions for Chase

1. **The lumber tier hues** (Part 5). The comments say green; the hues are blue, light blue and purple. **Proposed:**
   follow the ore satchel's own ladder (cc-P55):
   - T1 Forester none (the icon's own leather);
   - T2 Seasoned Gold 0x8A5;
   - T3 Arborist Verite 0x89F (an olive green).

   If you want them green, 0x7D6 "Snakes #5" for T1 and 0x59B "Greens #34" for T2 both read as forest green on the icon
   (`lumber_hues.png`, bottom row). Say which and it is a three-line change, with existing satchels moved the way
   cc-P55 moved the ore hues. Nothing changed now.
2. **The Smith Guild Salvage Bag is no longer all blue.** With PartialHue only the icon's gray metal takes 1154; the
   leather stays brown (`in_game_hues.png`). The same goes for every satchel: the hue now tints only what the icon drew
   gray. That is what "exact grays for PartialHue" means. If you want the whole bag blue, that is an icon change, not
   code.
3. **The hunter's tier hues** look unlike their comments too: 0x5B2 "richer brown" renders green and 0x4B5 "deep forest
   brown" maroon. Reported only; the prompt did not ask about them.
4. **IDs from the first free run, not the next one after the mimic**, to stay clear of Bronze's P237 (0x3C88-0x3CA9).
5. **No `client-data` in my work copy**, so `find-free-art.py` and `validate-art.py` read `D:\UO\UltimaOnlineVanilla`
   (`--data`). Its tiledata.mul is the 3,188,736-byte format the tools expect. The real `D:\ShatteredLegacy` is another
   desk. If the shard's client-data differs from it, rerun `find-free-art.py --explain 0x3380 0x3381 0x3382 0x3383 0x3384
   0x3385` there.
6. **Two stale count asserts fixed** in the package's `TheServersCopyOfTheRecordsIsRecordsJsonAndEveryIdIsRegistered`.
   They have been red on main since P147.
7. **A staff member's graphic on the two bags no longer changes their gump.** They keep 0xE76's container data whatever
   their ItemID. Before, the gump followed the ItemID.
8. **The Read tool was denied** (unattended run) for `docker\uo\build.sh` and for `server\customizations\ShatteredRunestone.cs`
   in the code work copy. I wanted to read build.sh's options and the lines around `ChestMimicArt.Apply()`. Instead I
   took the build command from earlier notes, and made each edit with a small Python script that requires an exact
   single match and keeps line endings. Nothing else was needed.

## For Chase

What to check in the client, after the package with this build is published and the server runs it:
1. Open the launcher so it updates, then log in on a character with each satchel. The ore, lumber and hunter's
   satchels, the Artificers' Essence Satchel, the Gemologist's Satchel and the Smith Guild Salvage Bag show the new
   icons. Compare them with `notes\cc-P236-art\in_game_hues.png`.
2. Ore tiers: the ore pile in the bag takes the tier's metal colour (T1 gray, T2 gold, T3 olive, T4 blue-gray, T5
   silver).
3. The Artificer's satchel is purple.
4. Open each: same gump as before (the satchels the backpack-style one, the two bags the bag one).
5. A satchel that was in the world before the update shows the new icon after the server restarts.
6. A client without the update shows "UNUSED" in those six spots until it updates.

Decisions: the lumber hues (1) and, if you care, the hunter's hues (3).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P236 -NoRefresh`
(the hand-off's work copies in place of the real folders). It commits nothing; neither repo is BLOCKED:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code: 21 files**: CHANGELOG.md, VERSION, the package fact, SOURCE.txt, records.json, registry.csv, the six PNGs, the
  seven changed classes, SatchelArt.cs and SatchelIconsVerification.cs.
- **docs: 5 files**: this note and `notes\cc-P236-art\` (two PNGs of 30 and 39 KB, two scripts).

No file is over 5 MB. The scratch (test logs, the package zip, the HEAD copy) is in the session scratchpad, outside
both repos. The vendored `vcruntime140.dll` is git-ignored (`git check-ignore`: `.gitignore:69`).

P236 DONE
