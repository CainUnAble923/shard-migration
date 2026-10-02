# cc-P27: defect batch 1 (D14 Fountain of Fortune, Imbuing essences from the bank, the reach repair, SOURCE.txt)

2026-10-02. Agent: Claude Code. Brief: `D:\UO\cc-prompts\cc-P27-defect-batch-1.md`. Pinned ModernUO `7c9215d97`; pinned
paths below are under `D:\UO\ModernUO-pinned\Projects\`. "Ours" paths are under `D:\ShatteredLegacy\`; HEAD line
numbers are `0f4c989`. Built in `D:\ShatteredLegacy`, **not committed**. Nothing was placed in any world; no shard was
deployed, restarted or recreated. `sl-modernuo:latest` was not moved (`486fd6a07ee1` before and after). Tools:
`notes\cc-P27-tools\`.

> **Headlines**
>
> 1. **All four parts are done. 391 shard tests pass** (383 before, 8 new). Image `sl-modernuo:cc-p27` =
>    `5fac2f1ecef7`. Two red runs; every new fact was seen failing for the reason its break targets; every broken
>    file was restored byte-identical by SHA-256 (section 5).
> 2. **Part A (D14):** `[ClusterFSeedFountainOfFortune dryrun`, then `[ClusterFSeedFountainOfFortune`, places the
>    fountain at OSI's point, **Ter Mur 1121, 957, -42**. It has its own small seeder file and is never run at world
>    load. Nothing blocks any of its 16 tiles there. But **the point is the middle of a pool**: all 16 tiles are on
>    water land, as at ServUO's own coordinates. A coin can be thrown from five shore tiles, three tiles from the
>    fountain's edge. Whether players can walk to those tiles depends on how pinned climbs land slopes, which my map
>    reader only approximates (section 1.2). **The in-game check decides it.** I placed it at OSI's point and did not
>    move it.
> 3. **Part B (F-11 widened):** imbuing takes its essence through `GuildResources`, in its order: pack loose, pack
>    satchels, bank loose, bank satchels. The gump says where they are: "3 essences of Swing Speed Increase: 1 in
>    pack, 2 in bank". **Found on the way: an essence inside the Artificers' Essence Satchel could never be used to
>    imbue.** The satchel is issued on joining and holds only essences, but the old check read only the top level
>    of the pack. It is now used, after loose essences in the pack and before the bank.
> 4. **Part C (`reach`):** pinned is now read with `server\patches` applied by `apply-patches.sh`'s own steps and
>    flags, and a later `typeof` in an `AddCraft` is a read. **Gate 9 at HEAD reads 2 delivered, not 0.**
>    **340 and 219-of-219 do not move** at the audit's tree (`8a52998`): neither uncomment patch existed then. Every
>    other number that moved is in section 3.4. Both fixes and both facts they forced me to update were watched
>    red. **The suite still has one failure that predates me:** the twin-sweep fact names `GauntletsOfAnger`, which
>    cc-P8 deleted (D35).
> 5. **Part D:** SOURCE.txt now says the "MMH7" file names are a misnaming and the art is cleared by Chase,
>    2026-10-02. Nothing else in the package changed.
> 6. **Two things the tool shows that I did not fix, both for the overseer:** P22's `GuildResources.SatchelTypes`
>    makes `GemologistsSatchel` read as reached (it only reads types), and `Putrefaction` stays a known over-reach
>    (section 3.5).

---

## 0. Before starting

- `git --no-optional-locks status` in `D:\ShatteredLegacy`: clean at `0f4c989` (P26). Nothing else was building.
- Read: P22 section 4 (F-11), `p22-decisions-2026-10-01.md`, `arch-reachability-verdict-2026-10-01.md` section 3,
  `p26-decisions-2026-10-02.md`.
- **Numbering:** no clash. `cc-prompts` holds P25 (stats research, its notes appeared beside mine while I worked),
  P27 (this) and P28 (launcher account profiles). P26 is done.
- **No commit landed in either repo during the task** (both `git log`s unchanged at 07:50; red runs 07:36-07:40 and
  07:40-07:44, each broken window only as long as its build).

---

## 1. Part A: D14, the Fountain of Fortune

### 1.1 Facts, confirmed

- The fountain: `server\customizations\Items\Addons\FountainOfFortune.cs`, a `BaseAddon`, 16 components, graphics
  0x1731-0x173F and 0x1741 (ServUO skips 0x1740, ported unchanged), offsets -2..+1 on both axes (`:33-60`).
  Tests: `server\tests\Items\Addons\FountainOfFortuneVerification.cs`.
- Q-021 (`notes\codex-questions.md:1128-1205`): ServUO's only placement is
  `Services/Underworld/Generate.cs:183-185`, Ter Mur `(1121, 957, -42)`; answer: place it there.
- **Nothing placed it.** `grep -rn "FountainOfFortune\|1121, *957"` over `server\customizations`, `server\tests`,
  `server\patches`: only the class, `LuckyCoin.cs:39` (the target check), `TanglingRoots.cs:80`
  (`UnderProtection`), the luck patch and the tests. Pinned `Projects` and `Distribution/Data`: no hit.
- **The coin's target:** `LuckyCoin.cs:35`, range 3, on an `AddonComponent` whose `Addon` is a fountain; anything else
  gets 1113369 "That is not sacred waters." Range is a square (pinned `Server/Mobiles/Mobile.cs:3031`), checked in
  `Target.Invoke` with `CanSee` and line of sight (`Server/Targeting/Target.cs`, `Invoke`).
- **Ter Mur is on in both shards:** `MapSelectionFlags.TerMur: true` in `server\uo\modernuo\Configuration\` and
  `Configuration-test\expansion.json` (identical files). Map files: pinned reads `map5LegacyMUL.uop`, `staidx5.mul`,
  `statics5.mul` (`Server/TileMatrix/TileMatrix.cs:102,121,133`; `Distribution/Data/map-definitions.json` index 5,
  1280 x 4096), all present in `client-data\classic-client`. Region: `DungeonRegion "Underworld"`, 898,808 to
  1280,1231 (`regions.json:3938`).

### 1.2 The client map at 1121, 957, -42 (`cc-P27-tools\fountain_fit.py`, `fountain_reach.py`)

Both run from `notes\cc-P15-tools` over P15's port of `Map.CanFit` (`fit.py`), switched to map 5. Pinned ships no Ter
Mur decoration, so only the client statics count.

- **Every component fits in the sense that nothing blocks it.** Pinned `BaseAddon.CouldFit`
  (`UOContent/Items/Addons/BaseAddon.cs:148-180`) asks `map.CanFit(x, y, z, height 6, checkBlocksFit false,
  checkMobiles true, requireSurface c.Z == 0)` per tile. No static stands on any of the 16 tiles, and the land is
  not impassable above z-42, so with `requireSurface` false all 16 pass.
- **None has a floor.** All 16 tiles are land 0xA8-0xAB, tiledata "water", flags 0xC0 (impassable, wet), z-42. The
  point is the middle of a pool about 12 x 12, ringed by statics (`cc-P27-tools\pool_grid.py` draws it). With `requireSurface` true, as a deed placement would ask, every tile fails
  "no surface". `MoveToWorld`, which is what ServUO uses and what the seeder uses, asks for neither. **So the fountain
  stands in water, as at ServUO's coordinates.** I took that to be OSI's layout (a fountain in a pool) and did not
  look for another spot: no nearer dry 4 x 4 would be the OSI point, and Q-021 says not to relocate.
- **Where a player can throw a coin from:** standable tiles within 3 (square) of a component: **1116,952; 1117,952;
  1116,959; 1116,960; 1117,961**, all z-42 on the shore. The test uses 1117,952, exactly 3 from the corner tile
  1119,955.
- **Whether they can walk there: likely, not proven.** My walk model is approximate (8-way steps between P15's
  standable surfaces, no doors, no pinned `Movement` code). Pinned's teleporters into the Underworld box land at the
  Trammel entrance (4194,3260 to 1127,1215) and from Ter Mur 519,919 to 1125,1075,-117. From those, with a step-up
  limit of 2 or 4 the shore is not reached (about 1,000 to 1,900 tiles reached). With 6 or 10 it is (about 20,000
  tiles, all five shore tiles). Pinned's movement climbs land slopes by corner height, which my per-tile surface
  model treats like stairs, so the low limits understate it. **Unverified; checklist item 3 settles it.** Line of
  sight from the shore is also unverified: the test host has no map tiles, so its LOS check passes trivially.

### 1.3 Placing it: a seeder of its own, `ClusterFFountainOfFortuneSeeder.cs`

Command: **`[ClusterFSeedFountainOfFortune [dryrun]`**, Administrator, declared `[ShardCommand(WorldSetup, Rerun =
Skips, Shard = TestFirst, DryRun = "dryrun")]` (P21's gate passes). Never at world load: it registers a command and
nothing else (`:28-31`). Duplicate-safe: a `FountainOfFortune` within 5 tiles of the point counts as present
(`FindNear`, `:49-58`). Ter Mur not loaded: reports and places nothing.

Why its own file and not a row in an existing seeder:
- `ClusterFGuildHallSeeder` walks `GuildLocations` rows of **mobiles** (type, facing, `CantWalk`, home range). An
  addon fits none of that.
- `ClusterFRoyalCitySeeder` is the only Ter Mur seeder, but it is the gargoyle vendor seeder (D34's territory,
  tabled), it seeds at world load whenever no gargoyle vendor exists (`ClusterFRoyalCitySeeder.cs:105,110-115`), and
  its seed deletes human vendors first. A fountain row there would ride on both.
- The New Haven and Institution seeders run at every world load. A row there would put the fountain on the live
  world at its next start without Chase running anything.

The console's World setup tab lists it by itself, under "every other world command" (`scripts\Shard-Console.ps1:1478-
1505`); it is not in `$script:WorldSetupOrder` because it has no order relationship to anything.

### 1.4 Tests (`server\tests\Items\Addons\FountainOfFortunePlacementVerification.cs`)

1. `ADryRunPlacesNothing`: no fountain near the point after a dry run; the report says "would place" at
   (1121, 957, -42).
2. `RunTwiceItPlacesOneFountainAtTheOsiPoint`: two runs, exactly one fountain, at the point, Ter Mur, 16
   components on Ter Mur; the second report says "already there". Then, with that one deleted and one placed by hand
   3 east and 2 north, a third run places none.
3. `ALuckyCoinThrownFromTheShoreReachesTheSuccessPath`: seeded fountain; a player at 1117,952,-42 double-clicks a
   stack of 2 coins and targets the component at 1119,955 **through the coin's own target** (`Target.Invoke`). One coin
   is spent and the daily cooldown is set, which only `FountainOfFortune.OnTarget` does. The existing facts call
   `OnTarget` directly, so the coin-to-fountain path had no fact.

**No saved type changed.**

---

## 2. Part B: Imbuing essences from the pack, then the bank

### 2.1 Every place the imbue path counts or takes an essence (`ArtificersImbueGump.cs`, HEAD lines)

| HEAD line | What | Now |
|---|---|---|
| `:724` | item view: `CountEssencesFor`, decides `needsEss` (button greyed) and "[essence ready]" | count from `GuildResources` (pack + bank) |
| `:788`, `:814` | property view: count, "N essence(s) in pack." | "Discovery: 3/10 uses - 3 essences: 1 in pack, 2 in bank" |
| `:906`, `:917`, `:940-943` | confirm view: count, "(you have: N)", Apply shown only if one is held | "(you have 3 essences of X: 1 in pack, 2 in bank)"; refusal says "in your pack or bank" |
| `:1375-1387` | apply: `FindEssenceInPack`, refuse if none | `GuildResources.Has(EssenceCost)` (now `:1376-1386`) |
| `:1421-1425` | apply, on success: `essence.Delete()` | `GuildResources.TryConsume` **first**, before shards and gold are taken; if it cannot, nothing is (now `:1416-1428`) |
| `:1636-1653` | the two helpers, top level of the pack only, counting stacks | `EssenceCost`, `CountEssences`, `DescribeEssences` (now `:1648-1665`) |

Not on the imbue path, left alone: essences **made** by disenchant, extract and craft (`:1471`, `:1526`, `:1580`, all
into the pack); `ArtificersSatchel.cs:77` (its tooltip count) and the Mastery gump's per-satchel count (`:149`), which
describe one satchel's contents. No other file counts or takes a `PropertyEssence` (grep).

`EssenceCost(key)` is `GuildCost.Where(item is PropertyEssence with that PropertyKey, 1, "Essence of key")`, so the
order and exclusions are `GuildResources.Candidates`' own, unchanged (pack before bank as the outer rule, Chase
2026-10-01). `PropertyEssence` is not stackable (`PropertyEssence.cs`, no `Stackable`), so items and amount agree.

**What widens, beyond the bank:** essences in any bag in the pack, and in the Artificers' Essence Satchel, now count
(before: top level only). **What narrows:** a blessed essence, or one in a locked or locked-down container, no longer
counts (the F-11 exclusions). I know of no way an essence becomes blessed.

### 2.2 Tests (`server\tests\Misc\ImbueEssenceSourcesVerification.cs`)

Every fact imbues through the gump's own buttons: target the item, the first property (Swing Speed Increase, checked
by the gump's own title), tier 1, Apply. At standing 15,000 its tier 1 has difficulty about 54, so Imbuing 100 always
passes. The test host never runs `SkillCheck.Initialize`, so the fixture sets pinned's handler
(`Mobile.SkillCheckLocationHandler`, `Server/Mobiles/Mobile.cs:1772`; without one every `CheckSkill` is false).

1. `AnEssenceInThePackOnlyIsTaken`: applied, the pack's essence gone, one discovery counted.
2. `AnEssenceInTheBankOnlyIsTaken`: count (0 pack, 1 bank); applied; the bank's gone.
3. `SplitBetweenPackAndBankThePacksIsTakenAndTheGumpSaysWhere`: 1 in pack, 2 in bank. `DescribeEssences` and the
   confirm view read "3 essences of Swing Speed Increase: 1 in pack, 2 in bank"; the pack's is taken, both bank ones
   stay.
4. `NoneOfTheRightPropertyIsRefusedAndNothingIsTaken`: essences of another property in pack and bank. The confirm
   view reads "0 essences ...: 0 in pack, 0 in bank"; Apply (pressed anyway, as a crafted response could) changes
   nothing: property 0, both other essences there, shards, gold and discoveries unchanged.
5. `AnEssenceInTheSatchelInThePackGoesBeforeALooseOneInTheBank`: the satchel's is taken, the bank's stays.

"One short" here is "none": an imbue takes exactly one essence.

---

## 3. Part C: the `reach` repair (`tools\content_index.py`, `tools\test_content_index.py`)

Read only against `D:\ShatteredLegacy`: three `git archive` exports in the scratchpad, `8a52998` (the audit's HEAD,
757 `.cs`, as the audit says), `0f4c989` (HEAD), and HEAD plus my uncommitted P27 files ("working tree"). Each export
carries `docker/uo/apply-patches.sh`.

### 3.1 Fix 1: pinned with our patches applied

`pinned_as_built` reads `apply-patches.sh` itself (`apply_steps`: its `apply_patch "$PATCHES/..."` and `replace_file`
lines, in its order), stages a scratch copy of each pinned file those steps touch (LF, as the build's Linux checkout
has it), and applies them with the script's flags: GNU `patch -p1 --forward --ignore-whitespace --fuzz=0 --batch`. A
patch that does not apply stops the tool. `Reach` then reads every pinned file from its patched copy where there is
one, for both the name pass and the reference pass. The old pass that read each `.patch`'s added lines as a root of
its own is gone (cc-P7 2.7's fault: an uncomment patch changes only comment markers, so its live lines are context).

Three choices, each forced by a measurement:
- **Only `$PATCHES` steps are staged.** Copying `server\customizations` replacements over pinned too made our
  `HammerOfHephaestus.cs`'s five extra types (`ReinforcedHammerOfHephaestus` among them) read as pinned's, and our
  content count fell by one at `8a52998` (1,060 types to 1,055, 891 content to 890). Those files are read as ours, as
  before; the stock files they replace are still read, as before.
- **An export must carry `apply-patches.sh`** (`git archive HEAD server docker/uo/apply-patches.sh`). Without it the
  tool stops and says so rather than guess what the build applies. The audit's reproduction line
  (`reachability-audit.md` section 9, `git archive HEAD server`) needs that one path added.
- **The "no source" list now excludes only commented-out construction** (`pinned-comment:new` or `:typeof`), as the
  gate grouping above it already did. Patched pinned now carries our patches' prose comments, and one ("PetMimic" in
  patched `BaseWeapon.cs:1652`) hid `PetMimic` from the list. The old any-comment rule had also hidden `Glasses` and
  `Note`, because pinned's prose says "glasses" and "Note:".

### 3.2 Fix 2: every `typeof` after the first in an `AddCraft` is a read

`ref_kind` asks `first_typeof_in_call` (no earlier `typeof` at depth 0 in the same call) and returns `('check',
'AddCraft')` for any later one, on both sides. ServUO `DefTinkering.cs:614` no longer reads as a source of
`CrystalShards`. **Residual, counted:** three `AddCraft` calls of 1,779 have a first argument that is not a `typeof`
literal (ServUO 2 of 1,063: `DefTinkering.cs:341-342`, `Core.AOS ? typeof(SmithyHammer) : typeof(SmithHammer)`;
pinned 0 of 656; ours 1 of 60: `TailoringCraftRegistrations.cs:85`, `AddCraft(type, ..., typeof(Cloth), ...)`). In
those the rule reads a product as a read, or a resource as the product. All three name pinned types only, so no
number of ours moves.

### 3.3 Facts, and each watched red (`cc-P27-tools\tool_red.py`)

New: `test_reach_an_uncomment_patch_makes_pinned_code_live` (`MyrmidonGloves` by `new` at patched `Miasma.cs:54`,
`GreymistChest` at patched `LadyLissith.cs:53`) and
`test_reach_a_later_typeof_in_addcraft_is_a_resource_not_a_product` (a snippet through `ref_kind`, and
`CrystalShards` with no `DefTinkering` source but its other sources kept).
Updated, because the tree moved under them, with a line in each saying why:
`test_reach_pinned_code_left_commented_out_is_reported` now uses `GrizzleGauntlets` at `Ilhenir.cs:163` (no patch of
ours uncomments it; cc-P7's patch uncommented the old example). `test_reach_static_access_runs_no_instance_code` now
computes the closure from `TanglingRoots` alone, which reads `FountainOfFortune.UnderProtection`. That shows the rule
on real code whether or not a seeder exists. It also asserts the whole tree now reaches the fountain by `new` in
`ClusterFFountainOfFortuneSeeder`: **gate 14 is built by Part A.**

Suite: **25 tests before, 27 after.** On the working-tree export (what HEAD becomes when Chase commits): 26 pass, 1
fails. The unchanged tool on HEAD already failed 2 of 25: the static-access fact (P22's false reach, 3.5) and the
twin fact (`GauntletsOfAnger`, deleted by cc-P8 for D35). The second is still failing and is not mine; I left it.
On bare HEAD the rewritten static fact errors, because it records the post-P27 tree.

Red, one rule reverted per copy, full suite each (working-tree export):

```
none               -> FAILED (failures=1)  twin (stale, before my change)
patched pinned     -> FAILED (failures=2)  test_reach_an_uncomment_patch_makes_pinned_code_live, twin
addcraft resource  -> FAILED (failures=2)  test_reach_a_later_typeof_in_addcraft_is_a_resource_not_a_product, twin
pinned comments    -> FAILED (failures=2)  test_reach_pinned_code_left_commented_out_is_reported, twin
acting rule        -> FAILED (failures=2)  test_reach_static_access_runs_no_instance_code, twin
```

Each revert reddens its own fact and no other. The S9 reproduction facts pass in every copy: `Index`/`row` are untouched.

**A mistake of mine, repaired:** while making the file ASCII I wrote `content_index.py` back with a script that
opened it for writing before encoding, and the encode failed, leaving it empty. I restored it from the identical copy
`tool_red.py` had written at 07:48 (after my last edit), converted back to LF, reviewed the whole diff against HEAD
(my changes only), and re-ran everything after: the suite, all five red cases and `reach_numbers.py` on all three
exports gave the same results, line for line.

### 3.4 Every number that moved (`cc-P27-tools\reach_numbers.py`, and `reach --sources --twins` diffed in full)

| Export | Number | Before | After |
|---|---|---|---|
| `8a52998` (audit) | unreachable ported content files, costumes excluded (the **340**) | 340 | **340** |
| | of Appendix A's 340, still not reached | 340 | 340 |
| | **219-of-219** | 219 of 219 | **219 of 219** |
| | gate 9 delivered (7 files) | 0 | 0 (its patches came later) |
| | ServUO sources of `CrystalShards` | 3 | 2 (`DefTinkering.cs:614` gone) |
| | `--sources` group `DefTinkering.cs` | 17 files, 18 types | 16 files, 17 types |
| | "no source anywhere" list | 76 | 78 (+`Glasses`, +`Note`) |
| | types / content / reached content | 1,060 / 891 / 404 | unchanged |
| HEAD `0f4c989` | **gate 9 delivered** | **0** | **2** (`GreymistChest`, `MyrmidonGloves`) |
| | content types reached | 562 of 928 | 564 |
| | ported content files reached / unreached | 309 / 300 | 311 / 298 |
| | unreachable, costumes excluded | 268 | 266 |
| | of Appendix A's 340, still not reached | 271 | 269 |
| | of the 219, still not reached | 168 | 168 |
| | `--sources` group `DefTinkering.cs` | 3 files | 2 files |
| | "no source anywhere" list | 77 | 79 (+`Glasses`, +`Note`) |
| | roots: 55 and 1 reached "by `StealableArtifacts`/`Loot` patch" | per patch | folded into `root:pinned` (73) |
| HEAD + P27 (working tree) | ported content files unreached | 296 | 294 |
| | gate 14 (fountain, 3 files) | 3 of 3 | 3 of 3 |

Part A's own effect, either tool: gate 14 goes from 1 of 3 at HEAD to 3 of 3, and 4 more ported files are reached
(300 to 296 with the old tool, 298 to 294 with the new one). At HEAD the 1 is `GemologistsSatchel`, through the
false reach in 3.5.

### 3.5 Not fixed, recorded

- **`Putrefaction` (per-method liveness):** not fixed, as briefed. Reach is decided per type, so
  `BasePeerless.PackResources`, which nothing calls, counts as live through `SlasherOfVeils` (craft-registrations
  4.1.2). A known over-reach of one type, for the audit's section 6 table.
- **New, found here: `GuildResources.SatchelTypes` (P22) reads as reach.** At HEAD the tool reports
  `GemologistsSatchel` reached "by typeof in GuildResources (GuildResources.cs:72)". That array is used only in
  `IsInstanceOfType` (`IsSatchel`), a read. The fix is one name in `READER_SITES` (`SatchelTypes`) and a fact. I
  did not make it because it is outside the two fixes briefed. With Part A in, the satchel is genuinely reached
  anyway (the fountain's reward, `FountainOfFortune.cs:90`).
- **The twin fact is stale** (above): a replacement example is a one-line change for whoever owns the suite next.

---

## 4. Part D: SOURCE.txt

`player-package\vendor\shattered-legacy-art\SOURCE.txt`, the License paragraph only: the "MMH7 runestone" names "are a
misnaming, not a sign of where the art came from. Cleared for use, and to ship to players, by Chase on 2026-10-02
("the art is fine just missnamed"; shard-migration notes\p26-decisions-2026-10-02.md, item 1)". "NO LICENSE STATED"
stays, because it is still a fact about the download. Nothing reads or hashes the file (grep over `.ps1 .py .cs .json
.sh`). The F-8 register text (P26 section 11) is the overseer's to change.

---

## 5. Builds, red and green (`docker\uo\build.sh -t sl-modernuo:cc-p27`, Git Bash)

| Run | Result | Notes |
|---|---|---|
| 1 | builder failed | my test's `FindItemsByType(...).Where(...)`: CS0411 (it is not an `IEnumerable` LINQ can infer). Rewritten as a loop. The shard code compiled. |
| 2 | **391 / 391**, image `d4566cb094dd` | green on the first test run |
| red 1 (`cc-P27-tools\mutate.py apply R1`) | **8 failed / 383 passed** | six breaks; all 8 new facts failed, each on its target assertion |
| red 2 (`mutate.py apply R2`) | **3 failed / 388 passed** | two breaks aimed at the three facts red 1 failed for other reasons |
| final, after restore | **391 / 391**, image `sl-modernuo:cc-p27` = **`5fac2f1ecef7`** | same sources as run 2 (SHA-256 checked) |

Test totals: **383 before (P26), 391 after.** No red run built an image (the test gate stopped them).

- **Red 1 breaks and what each failure said:** dry run places anyway (dry-run fact: "collection was not empty"); the
  existing fountain never found (run-twice fact: "contained 2 items"); the coin's range 2 (coin fact: amount 2,
  not 1); the essence not taken on success (pack-only: pack not empty); the check sees the pack's top level only
  (bank-only: "an essence in the bank was not used"; satchel: "the imbue did not apply"); the gump stops saying
  where (split: `DescribeEssences` string differs; none: confirm text missing).
- **Red 2 breaks:** no refusal before the skill check, and the essence taken is the last candidate, the bank's, with
  none found not a refusal. Split: "the pack's essence should be used first". None: Swing Speed 15 applied with no
  essence. Satchel: "the satchel in the pack should be used before the bank". Pack-only and bank-only stayed green,
  as they should (one candidate each).
- **Restore:** after each red run the three or one mutated files came back from backup and SHA-256 matched the
  pre-break hash: "identical" for every file, both times.

---

## 6. File by file

```
D:\ShatteredLegacy
  server\customizations\ClusterFFountainOfFortuneSeeder.cs          NEW  Part A seeder and command
  server\customizations\ArtificersImbueGump.cs                      M    Part B: helpers, check, take, gump lines
  server\customizations\GuildResources.cs                           M    one header line: essences use it now
  server\tests\Items\Addons\FountainOfFortunePlacementVerification.cs NEW  Part A, 3 facts
  server\tests\Misc\ImbueEssenceSourcesVerification.cs              NEW  Part B, 5 facts
  player-package\vendor\shattered-legacy-art\SOURCE.txt             M    Part D, license paragraph
D:\UO\shard-migration
  tools\content_index.py                                            M    Part C fixes 1 and 2, no-source filter;
                                                                         one literal U+FEFF written as '\ufeff'
                                                                         so the file is ASCII (same character)
  tools\test_content_index.py                                       M    2 new facts, 2 updated
  notes\cc-P27-tools\                                               NEW  fountain_fit.py, fountain_reach.py,
                                                                         pool_grid.py, reach_numbers.py, mutate.py,
                                                                         tool_red.py
  notes\cc-P27-defect-batch-1.md                                    NEW  this note
```

All ASCII, LF. `tools\progress.py` not run: it rewrites `README.md` and `tools\progress.json`, which are not mine to
change in this task. `docs\` not touched (its `feature-queue.md` change in the working tree predates me).

---

## 7. Deviations for the register

- **Part A (D14): none.** The fountain is placed at ServUO's, and so OSI's, point, by the same `MoveToWorld`. One
  difference no player sees: ServUO also adds it to `WeakEntityCollection "sa"` (`Generate.cs:185`), ServUO's
  bookkeeping for deleting the SA decoration. Ours has no such collection; the seeder finds it by type and place.
  When D14 is promoted, the S2 entry's bullet "Nothing places a fountain yet" in `docs\fidelity-principle.md` can
  close.
- **Part B: amend F-11's line** (P22 section 9) to: "**F-11:** our guild systems take costs and turn-ins from the bank
  as well as the pack, never equipped, blessed or locked-up items. Since cc-P27 this includes the essence an
  Artificers' imbue takes (pack first, then bank, satchels after loose stock in each), which before could come only
  from the top level of the pack. No OSI behaviour changes: OSI crafting and BODs stay pack-only, and the Artificers'
  imbuing is ours (pinned has no imbuing). The Hammer of Hephaestus upgrade's gold is now pack then bank."

---

## 8. Left for Chase (and the overseer)

1. **Is the fountain reachable on foot, and in sight from the shore?** (1.2) If not, the choices are a teleporter or
   a spot on dry land, and either is a deviation to record. I did not pick one.
2. **Overseer:** schedule `SatchelTypes` into `READER_SITES` and a new example for the twin fact (3.5), and add
   `docker/uo/apply-patches.sh` to the audit's reproduction line (3.1).
3. **Overseer:** the F-8 register text still says "possibly from Might & Magic Heroes VII" (P26 decision 1).

---

## Checklist for Chase

PowerShell 5.1; one command per line.

1. **Commit.**

   ```
   D:\UO\Commit-ShardWork.ps1
   ```

2. **Put this build on the test shard**, your usual way. `sl-modernuo:cc-p27` = `5fac2f1ecef7` is built and green;
   the test compose runs `sl-modernuo:latest`.

3. **Place the fountain on the test shard** (Administrator, in game). The dry run should say "would place at (1121,
   957, -42) in Ter Mur"; the second line places it; running it again should say "already there". `[go x y z` keeps
   your current facet, so move yourself to Ter Mur first (`[set map TerMur`, then target yourself; or `[props` on
   yourself and set Map).

   ```
   [ClusterFSeedFountainOfFortune dryrun
   [ClusterFSeedFountainOfFortune
   [ClusterFSeedFountainOfFortune
   [set map TerMur
   [go 1117 952 -42
   ```

   Then: the fountain should stand in the middle of the pool. From 1117,952 (the shore, three tiles from its corner),
   double-click a lucky coin and target the fountain: a coin is spent and you get a reward or a buff, not "That is
   not sacred waters". **Then the part I could not check:** walk to that shore from the Underworld's entrance
   (Trammel 4194,3260 is the way in), without `[go`. If you cannot, tell the overseer before it goes live.

4. **Imbue with essences split between pack and bank.** As an Artificer who has not mastered the property, put one
   essence of it in your pack and two in your bank (the bank need not be open). The property and confirm views
   should read "3 essences ...: 1 in pack, 2 in bank". Apply: on success the pack's essence is gone and both bank
   ones stay. Then, with the pack's gone, imbue again: it should take one from the bank.

5. **Optional:** put an essence in the Artificers' Essence Satchel, none loose, and imbue. Before this build that
   was refused.

6. **Live, when you want it there:** step 3's first two lines on the live shard after it runs this build.
