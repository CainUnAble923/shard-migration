# cc-P100: Visual Builder for staff, with recorded erase and wipe

2026-10-14. Builder in `D:\ShatteredLegacy`; staff only. **After Kamras's ServUO Visual Builder, Architect Edition**
(`D:\UO\third-party\code\visual-builder\ServUOVisualBuilder.cs`, from servuo.dev). Rewritten for ModernUO, not copied.
The credit is in the code header and in the palette's title.

## Headlines

- **`[VBuild`** (GameMaster) opens a palette built from `TileData.ItemTable` (`DynamicGump`, 24 art tiles a page). You
  can search by name, by decimal ID or by hex ID (`0x0A99`). Pick the art, hue and Z offset, then use **Paint**
  (repeats until Escape), **Fill box** (at most 20 x 20), **Erase**, **Wipe box** (at most 50 x 50), **Hue an item**,
  **Nudge** (X, Y and Z, plus or minus) and **Undo**. Everything placed is a plain `Static`.
- **Erase and wipe record every item before deleting any of them**: type, ID, hue, name, location, map, and whether
  the session had placed it. Undo puts each one back as it was. Every other action is also one undo step: paint, fill,
  hue and nudge. The history is capped at 100 steps per staff member.
- **World mode** is off by default and Administrator only (`[VBuild world on`). In world mode, erase and wipe also
  remove Statics the builder did not place, and only items whose type is exactly `Static`. Without it, they only touch
  what this session placed. The access check sits in the rule itself, not only in the command, so a GameMaster is
  refused even with the flag forced on.
- **Step 4 decision: the undo history is saved with the world** (`ClusterFVisualBuilderStore`, a `GenericPersistence`),
  so it survives a restart. World mode is not saved: it is off after every restart. Why, below.
- **Tests:** 7 new facts. **1,147 of 1,147** shard tests pass in `build.sh` on the final tree (1,140 before, plus 7),
  and the image `sl-modernuo:cc-p100` is built. All 7 went red under deliberate breaks first.
- **One flaky test outside this task** failed in one of my builds and passed when rerun. It belongs to P79's loot boxes
  and is logged below as a bug candidate.

## Step 4: why saved, not cleared

The point of P100 is that a wipe can always be undone. Clearing the history at restart would break that promise at
the worst moment (a crash in the middle of an edit). So the history is saved, and it is saved **as part of the world
save** rather than in a file of its own, so the two can never disagree:
- an item a wipe deleted after the last save is still in that save, and so is the record of deleting it, or neither is;
- a file written at the moment of the wipe would, after a crash, put back an item the restored save already has, which
  would make a duplicate.

Undo looks items up by serial when it runs (`World.FindItem`). Anything gone by then (deleted by hand, decayed) is
skipped and counted out. World mode starts off after a load, deliberately: a dangerous mode should never come back on
by itself.

## What changed, with file:line

| File | What |
|---|---|
| `server/customizations/ClusterFVisualBuilder.cs` (new, 40 KB) | Header with the credit and the four changes from the original (:14-31). Caps (:35). `[VBuild` registered (:46). The rules: `SetWorldMode` (:65), `CanModify` (:81). The tools: `Paint` (:115), `Fill` (:134), `Erase` (:163), `Wipe` (:179), `SetHue` (:206), `Nudge` (:222), `Undo` (:254). `Remove` records everything before the first delete (:317, :328). The catalog `Search` (:365). The command, declared WorldSetup with dry run `status` (:414). The session and `Rename` (:523, :547). The save, `ClusterFVisualBuilderStore` (:613). The palette gump (:752). The targets (:932). |
| `server/tests/Misc/VisualBuilderVerification.cs` (new, 12 KB) | the 7 facts |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.7, one `### Staff` line |

**Changes from the original, as the cc-P93 assessment asked:**
1. Erase and wipe record what they delete, so undo puts it back. The original's undo only deleted what it had placed
   (`ServUOVisualBuilder.cs:132-160`), so a wipe could not be undone.
2. World mode is Administrator only and off after a restart. The original's was GameMaster, with a session toggle.
3. Every action is an undo step, including hue and nudge, and the history is saved with the world. The original kept
   it in memory.
4. Caps: a fill box is at most 20 x 20, a wipe box at most 50 x 50. Both are refused before anything is touched.

Mechanical ModernUO changes: `DynamicGump`/`BuildLayout`, `OnResponse(NetState, in RelayInfo)`,
`CloseGump<T>()`, `BoundingBoxPicker` for boxes. Left out on purpose: the original's 16 name-guessing categories
(search covers it) and Clone (`[Tile`, `[Add` and `[StampLayout` cover it).

**Commands:** `[VBuild` (palette), `status` (reports only; the declared dry run), `undo`, `nudge <dx> <dy> [dz]`,
`world on|off`, `forget` (drop your session's history; items stay). Turning world mode on is written to the command log.

## Tests (each seen failing first)

`server/tests/Misc/VisualBuilderVerification.cs`, in Trammel x 5900 to 5925, y 3950 to 3975. Every fact deletes what
it placed (`Dispose` sweeps the area).

1. **`WipeThenUndoRestoresEveryItem`.** 3 painted Statics (two hued, one named) and a 2 x 2 fill, plus one Static
   nobody placed through the builder. A protected wipe of the box removes exactly the 7 placed items, not the other one.
   Undo brings all 7 back with the same ID, hue, name and place, still owned by the session.
2. **`WorldModeIsRefusedBelowAdministrator`.** A GameMaster and a Seer are refused `world on`. With the flag forced on,
   they still cannot erase or wipe a Static they did not place. For an Administrator it is off by default; once on,
   the wipe removes the two plain Statics and never the door. Undo puts both back, and they are not adopted into the
   session.
3. **`TheFillBoxIsCapped`.** 21 x 1 and 1 x 21 are refused, with nothing placed and nothing to undo. 20 x 20 places
   400, and undo removes all 400. The wipe's own cap: 51 x 1 is refused.
4. **`UndoOfAnEraseKeepsTheOlderStepsPointingAtTheItem`.** Paint, erase, undo: the item is back under a new serial.
   A second undo (of the paint) removes that new item.
5. **`TheUndoHistorySurvivesASaveAndLoad`.** An Administrator's world-mode wipe is saved, then everything is reset (a
   restart) and loaded again. World mode is off, the wipe undoes exactly, and the paint step before it is still there.
   An unknown version is refused loudly.
6. **`HueAndNudgeAreUndoStepsToo`.** Hue, then nudge (0, 2, 1); undo reverses each in turn, then the fill. Re-hueing a
   Static the session did not place is refused.
7. **`ThePaletteSearchesByNameAndId`.** On a small fake tile table (the test host loads no tile data): by name with
   case ignored, decimal ID, hex ID. Unnamed tiles are left out, and the list stops at the maximum ID.

**Red, on purpose.** First, one scratch build with seven breaks, then the file restored (`cmp`-identical):
- nothing recorded on delete;
- world mode without the access check, both places;
- no fill cap;
- no rename after a put-back;
- nudge not pushed as a step;
- no exact-ID search.

Result: `Total tests: 1147, Failed: 7`, every new fact. The messages were `Expected: 7 Actual: 0` (wipe undo),
`Value is null` (world mode), `Expected: 0 Actual: 21` (cap) and `Collections differ` (search). The erase fact went red
from the first break, which hid the rename break. So the rename break ran alone in a second scratch build, restored
again: `Failed: 2`, the erase fact and the save fact. Scratch builder images removed.

**Full suite:** `build.sh -t sl-modernuo:cc-p100` on the final tree: `Total tests: 1147, Passed: 1147`, image built
(`5a45b959afec`, 1.29 GB). That was my second run of the full gate. The first failed on one test, next section.

## A flaky test, not this task's (for the bug list)

`LootBoxFanfareVerification.ContentsAreRolledAtEarnAndOpeningHandsOverExactlyThoseThenTheBoxIsGone` (P79) failed once
at `Assert.False(item.Deleted)` (`server/tests/Misc/LootBoxFanfareVerification.cs:212`). It passed in the other four
builds.
- **What I saw:** that run's roll was "Mythril Box: 12000 gold, 200 Renown, 60 x Iron Ore, 5 x Star Sapphire,
  **60 x Bandage**, 50 x Shadowbark Board, **60 x Bandage**".
- **What I think happens, not probed:** when the pool rolls the same stackable twice, handing the box over drops the
  second stack into the backpack, where it merges into the first and is deleted. The fact then sees a held item deleted.
- **Which kind:** ours. Either the fact should count by type and amount, or the roller should merge duplicates at earn
  time. It is random, so it can fail any `build.sh` run, the overnight bot's included.

Proposed line for `docs\bug-list.md`: "D95 (or next free): P79's loot-box hand-over fact fails when the pool rolls one
stackable twice (the second stack merges into the first on drop and is deleted); flaky (failed 1 of 5 builds in
cc-P100; the true rate is unmeasured). Fix the fact or merge duplicates at roll time."

## Deviations and decisions for Chase

- **Undo is saved with the world** (step 4). The consequence: a wipe made after the last save, followed by a crash,
  rolls back with the world, so there is nothing to undo, because the items are simply back.
- **World mode only touches items whose type is exactly `Static`**, not subclasses, doors, addons or containers. Those
  hold properties a record of ID, hue and name could not restore. This is narrower than the original, which allowed
  any `is Static`.
- **Map statics (the map files) are never touched.** Erase on one says so. `[Wipe` from pinned does not touch them
  either.
- **Hue an item** follows the same rule as erase: protected mode re-hues only what the session placed.
- **Nudge moves the last paint or fill**, not a targeted item (the original had an Edit gump for that). Undo, then
  re-place, does the same job.
- **Restored items get new serials.** Older undo steps are re-pointed at them, so the history stays right.
- **Categories and Clone are left out** (above). Say if you want the categories.
- `[VBuild` is declared WorldSetup / Skips / TestFirst with dry run `status`, so the console's World setup tab lists it.
  Opening the palette places nothing; what you do with it places things.

## For Chase

The image `sl-modernuo:cc-p100` is built (gates passed). To try it on the test shard:
1. Deploy it to test: Shard Console, Test shard tab, Deploy, pick `sl-modernuo:cc-p100`.
2. Log in as staff and stand in a corner of New Haven. Type `[VBuild`.
3. Search `bench`, `barrel` or `flower`, pick one, and **Paint** a few. Set a hue, then **Fill box** a small 3 x 3 floor
   (try 21 x 21 once: it is refused). **Nudge** it a tile.
4. **Wipe box** over the whole corner. Everything you placed goes; the town's own decoration stays.
5. **Undo**: everything comes back. Undo again until the corner is as it was.
6. Optional, as Administrator: `[VBuild world on`, wipe a box with some loose decoration, undo, `[VBuild world off`.
7. Optional: restart the test shard after a wipe and a save, then `[VBuild undo`. It still puts things back.

## Repo size and preflight

- No file over 5 MB: the new files are 40 KB and 12 KB. Scratch logs and the mutant script stayed in the session
  scratchpad and `%TEMP%`. The mutant builder images were removed.

`Commit-ShardWork.ps1 -DryRun`: code has 4 files pending (`CHANGELOG.md`, `VERSION`, `ClusterFVisualBuilder.cs`,
`VisualBuilderVerification.cs`), docs has 1 (this note).

```
Repo Result
---- ------
code dry run
docs dry run
```

P100 DONE
