# cc-P98: Building Duplicator as the capture step for layout JSON

2026-10-14. Builder in `D:\ShatteredLegacy`; staff only. **After Kamras's Building Duplicator for ServUO**
(`D:\UO\third-party\code\building-duplicator\BuildingDuplicator.cs`, from servuo.dev): rewritten for ModernUO, not
copied. The credit is in the code header too.

## STOP FIRST: every build is blocked by a NuGet security advisory (needs Chase's decision)

Since about 09:40 today, `dotnet publish` in the builder stage fails at restore, before any code compiles:

```
error NU1902: Warning As Error: Package 'System.Security.Cryptography.Pkcs' 10.0.0 has a known moderate severity vulnerability, https://github.com/advisories/GHSA-2fmv-rv2c-59x7
error NU1903: Warning As Error: Package 'System.Security.Cryptography.Pkcs' 10.0.0 has a known high severity vulnerability, https://github.com/advisories/GHSA-846f-f764-76mx
```

- **It is not this task's code.** Probed on the clean P95 commit `61db33c`, in the `D:\UO\test-shard-src` worktree,
  with one scratch file added so Docker could not reuse its cached publish layer: the same two errors, exit 1.
  Without that file the build passes, but only because it is cached. This morning's builds passed for the same
  reason, or because the advisory was not yet published.
- **The cause:** pinned ModernUO's `Directory.Build.props:15` has `TreatWarningsAsErrors` true, so NuGet's audit
  warning about a transitive package becomes an error. `UOContent.csproj:24` already deletes that DLL from the output,
  which suggests upstream does not ship it.
- **What it blocks:** `build.sh`, `Start-TestShard.ps1` (Rebuild, `-Commit`), the overnight bot's build, and every
  queued prompt that builds (P99 on).
- **Options:**
  1. `-p:NuGetAuditLevel=critical` on the `dotnet publish` line in `docker/uo/Dockerfile`. Moderate and high advisories
     stop failing the build; a critical one still does. One line, ours.
  2. `-p:NuGetAudit=false`: no audit at all. This is what I used **in a scratch copy only** to verify P98 (below).
  3. Pin a fixed `System.Security.Cryptography.Pkcs` through a patch to pinned's props. That is an upstream-file patch,
     so its alternatives go in `notes\` first. Which version fixes both advisories is **unverified**.
  4. Wait for upstream to bump it.

  My suggestion: option 1 now (it keeps critical advisories as a gate), then 3 or 4.
- **Not changed:** `docker/uo/Dockerfile` and `build.sh`. The gate's security behavior is Chase's call.

## Also outstanding from P97 (not this task)

The live container `sl-modernuo` was still at the world-load prompt `Delete the object and continue? (y/n/a)` when
checked during P97 (details in `notes\cc-P97-bug-reports.md`). Not re-checked or touched here.

## Headlines

- **`[CaptureLayout <name> [area] [minZ maxZ]`** (GameMaster). Two corners make the box, which is refused over
  **64 x 64 before a single tile is read**. It writes `<world folder>\layout-captures\<name>.json` in the shape the
  layout generator reads, plus `name`, `source`, `origin` and a `hue` per component:
  - it keeps the items in the box and the map statics, read with `GetStaticTiles` (no multi tiles);
  - it skips houses and boats (`BaseMulti`), doors, addon bases and hidden items (spawners, teleporters).
- **`[StampLayout <name>`** checks **the whole file first**, then places the layout where you target. Each component
  becomes a plain `Static` of its ID and hue, so nothing of value can be duplicated. Subcommands:
  - `check <name>`: checks only;
  - `nudge <dx> <dy> [dz]`: moves the last stamp;
  - `undo`: removes it, including a stamp that stopped part way, because every item is in the undo list **before** it
    is placed.
- **No AddOn `.cs` export:** pinned ModernUO has `[AddonGen`.
- **Tests:** 5 new facts. **1,140 of 1,140** shard tests passed, on a scratch builder with the NuGet audit off (see
  above). All 5 went red under 4 deliberate breaks of the behaviors they guard.

## What changed, with file:line

| File | What |
|---|---|
| `server/customizations/ClusterFLayoutCapture.cs` (new) | Header with the credit and the four changes from the original (:15-36). Commands registered (:60-61). `CheckBox` (:70), `Capture` (:92), `ToJson` (:160), `Parse` (:201), `Stamp` (:336), `Undo` (:372), `Nudge` (:393). `[CaptureLayout` declared DevTool (:427). `[StampLayout` declared WorldSetup, rerun Duplicates, TestFirst, dry run `check` (:479). The records (:574-578). |
| `server/tests/Misc/LayoutCaptureVerification.cs` (new) | the 5 facts |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.5, one `### Staff` line |

**The file** (example):

```
{
  "map": "Trammel",
  "name": "guild-room",
  "source": "[CaptureLayout by Chase at 2026-10-14T15:00:00Z, box 3450,2590 to 3462,2603, z -128 to 127",
  "origin": { "x": 3450, "y": 2590, "z": 18 },
  "components": [
    { "area": "main", "id": "0x0A99", "name": "bookcase", "x": 3461, "y": 2597, "z": 18, "hue": 0 }, ...
  ]
}
```

- `map` and `components` (`area`, `id` as `0xHHHH`, `name`, `x`, `y`, `z` in world coordinates) are the design shape
  that `notes/cc-P31-tools/gen_office_layout.py` and `RegistrarOfficeVerification` read.
- `hue`, `origin`, `name` and `source` are extra, and the generator ignores them.
- Components are in a fixed order (y, x, z, id, hue), so two captures of the same area are byte-identical apart from
  `source`.

**Where captures go:** the world folder, beside `Saves`, in `layout-captures\`:
- test shard: `D:\ShatteredLegacy\server\lib\uo\modernuo-test\layout-captures\`;
- live: `...\server\lib\uo\modernuo\layout-captures\`.

Both are git-ignored: `git check-ignore -v` gives `.gitignore:58:server/lib/` for each. They are staff-only by
access: the commands are GameMaster, and the folder is on the host.

## Tests (each seen failing first)

`server/tests/Misc/LayoutCaptureVerification.cs`, in Trammel at x 5960 to 5965, y 3910 to 3913. Every fact deletes
what it placed.

1. **`ACaptureRoundTripsThroughTheGeneratorToTheSameTable`.** The fixture:
   - four statics (two hued) at different z;
   - a hidden item, a `MetalDoor` and a `StoneOvenEastAddon`.

   The capture keeps the statics and the oven's components, plus any map statics the test host has there (none, it
   loads no maps). It leaves out the door, the oven's base and the hidden item. The JSON is then read the way the
   generator reads it (area, hex id, name, x, y, z, as `RegistrarOfficeVerification.TheLoadedLayoutIsTheDesignFile`
   does) and equals the fixture's table row for row. Read back through `Parse`, it gives the same pieces, hues
   included, with the same origin and map.
2. **`TheSizeCapRefusesABigBoxBeforeReadingAnything`:** 65 x 4 and 4 x 65 are refused with `TilesRead` 0; 64 x 64 is
   read.
3. **`ABadLineStopsTheStampBeforeAnythingIsPlaced`:** two good components and one bad one fail with exactly
   `component 3: ...` and no layout. The five bad ones are a non-hex id, z 300, an empty area, x as text and hue -1.
   An unknown map and broken JSON are refused too. A checked layout that would land past z 127 places nothing, and
   leaves nothing to undo.
4. **`UndoAfterAPartialStampRemovesEveryPlacedItem`:** a 6-piece stamp stopped while placing the 4th leaves 3 in the
   world. Undo removes 4: the 3, and the one it was holding.
5. **`NudgeMovesTheLastStampAndUndoRemovesIt`:** the placed pieces are `Static`, not movable, with the hue. Nudge
   (0, 2, 1) moves both, undo removes them, and there is nothing left after.

**Red, on purpose** (one scratch build; the file then restored, `cmp`-identical). Four breaks:
- the cap checked only after reading;
- a bad component skipped and the rest placed;
- undo pushed after the loop (the original's way, `BuildingDuplicator.cs:458`);
- every area written as "main".

Result: `Total tests: 5, Failed: 5`.
- The cap fact: `Expected: 0` tiles read.
- The bad-line fact: `Value is not null`.
- The partial-undo fact: `Expected: 4`.
- The round-trip fact: collections differ.
- The nudge fact also failed, from items the undo mutant left behind.

**Two mistakes of mine the first green run caught:**
- The test host loads no tile data, so `TileData.MaxItemValue` is 0 there and every ID was masked to 0. The code now
  uses the full 16 bits when no tile data is loaded.
- A fact's "past z 127" case did not actually go past it, placed items, and they leaked into the other facts. Every
  stamping fact now undoes everything in `finally`.

**Full suite:** `Total tests: 1140, Passed: 1140` (1,135 before, plus 5). That is the scratch builder
`sl-uo-builder:cc-p98-noaudit`, from a copy of `docker/uo/Dockerfile` (in the session scratchpad) whose only change is
`-p:NuGetAudit=false` on the publish line. The tests ran exactly as `build.sh` step 2 runs them. Re-run on the final
tree, CHANGELOG included: `Total tests: 1140, Passed: 1140`. **`build.sh` itself cannot pass until the blocker above is decided.**

**Not done:** the manual capture on the test shard (below, for Chase). The overnight bot can type commands but cannot
answer the two-corner box picker as written.

## Deviations and decisions for Chase

- **Undo is in memory.** It is lost when the shard restarts, as the original's was. A stamp is then plain statics; to
  remove one after a restart, use `[Wipe` on its box or delete by hand. Making undo survive a restart would mean a
  saved record of every stamp; say if you want that.
- **Hidden items are skipped too** (the prompt said multis, doors and addon bases), so spawners and teleporters in a
  room are never re-stamped as visible statics.
- **Addon components are kept**, as plain statics, as the original kept them; only the addon's base is skipped. So a
  captured oven is re-stamped as its graphics, not as a working oven.
- **One `[StampLayout` command with subcommands** rather than three commands, so the console's World setup tab shows one
  declared world command with its dry run (`check`).
- **A name is not overwritten:** `[CaptureLayout` refuses a name that already exists.
- **A layout can be stamped on another facet** than it was captured on; the message says so.

## For Chase

**First, the build blocker above.** Nothing builds until it is decided, the overnight bot included.

**Then, once a build with this code is on the test shard, capture and re-stamp one guild hall room:**
1. Log in to the test shard as staff and stand in the room (for example, a New Haven guild hall).
2. `[CaptureLayout hall-test` and target two opposite corners of the room. It should say "Captured N pieces as
   hall-test" with the file path.
3. Walk to an empty spot and run `[StampLayout check hall-test`. It should say "checks out" and place nothing.
4. `[StampLayout hall-test` and target the spot. The room's furniture appears there.
5. If it is a little off, `[StampLayout nudge 1 0` (x, y, then optional z).
6. `[StampLayout undo` removes all of it.

The file is in `D:\ShatteredLegacy\server\lib\uo\modernuo-test\layout-captures\hall-test.json`. Copy it into `design\`
when you want it to become a seeded structure.

Also, when convenient: the scratch images `sl-uo-builder:cc-p98-noaudit`, `cc-p98-mut` and `probe-audit` (about 5 GB
each) were removed at the end of this task. Check with `docker images sl-uo-builder`.

## Repo size and preflight

- No file over 5 MB: the new files are 23 KB and 13 KB.
- Captures go to the git-ignored world folder (proof above).
- The scratch Dockerfile and logs stayed in the session scratchpad.

`Commit-ShardWork.ps1 -DryRun`: code has 4 files pending (`CHANGELOG.md`, `VERSION`, `ClusterFLayoutCapture.cs`,
`LayoutCaptureVerification.cs`); docs has 1 (this note).

```
Repo Result
---- ------
code dry run
docs dry run
```

**Why this ends STOPPED and not DONE.** P98's work is complete and verified (above). But every build is blocked until
Chase decides the NuGet audit question at the top. DONE would hand the queue the next prompt, which cannot build.
STOPPED holds the queue and emails Chase. P98's files are uncommitted and ready: commit them with the Console's Commit
tab (or say go) once the build question is answered.

P98 STOPPED: work complete and verified, but every build is blocked by NuGet audit errors NU1902/NU1903 on System.Security.Cryptography.Pkcs 10.0.0 (needs Chase to choose a fix before the queue goes on)
