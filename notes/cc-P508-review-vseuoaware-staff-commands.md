# P508: Review of the P135 vseUOAware staff commands

Reviewed 2026-10-23. Notes only. P135 is on local code `main` at `579ad58f8f478280b03b8cf80f1ee9a5b3001a27`; its implementation commit is `2812511`. The reviewed command, library, and map test files have no differences from that main.

## Findings

1. **Risk: pending targets retain staff powers after demotion.** `server/customizations/StaffHub/ClusterFMapCheckCommands.cs:338` and `:307`: a GM can start `ExportPoints`, be demoted while the target is open, then complete it and write the export because neither the point target nor the bounding-box callback rechecks access; the other targeted commands have the same omission. Check `AccessLevel.GameMaster` again before each callback performs work, and add a regression case that demotes the caller between starting and completing a target.

2. **Bug: a contained item supplies container coordinates.** `server/customizations/StaffHub/ClusterFMapCheckCommands.cs:340`: `PointTarget` accepts any `IPoint3D`, so targeting an item in a backpack exports or checks its container-local X, Y, and Z instead of its world location. Either reject items and mobiles as the refusal text implies, or normalize them with `Item.GetWorldTop()` and `Mobile.Location` as pinned `BoundingBoxPicker.cs:47` does, with a contained-item regression case.

3. **Bug: switching export names silently loses earlier points.** `server/customizations/StaffHub/ClusterFMapCheckCommands.cs:296`: the dictionary holds only one list per staff member, so adding points to `alpha`, then `beta`, then `alpha` replaces `alpha.json` with only the new point; changing facets also replaces the old list, and `clear` at `:283` ignores the supplied name. Keep lists by staff member and export name, explicitly handle mixed facets, and test switching names, returning to a name, and clearing a different name.

4. **Bug: reports overwrite one another within a second.** `server/customizations/StaffHub/ClusterFMapCheck.cs:988`: two reports for the same command in one second share a path, and `File.WriteAllLines` replaces the first report, including when different staff members run it. Allocate a unique file with exclusive creation, and test two writes with the same clock value.

5. **Bug: a malformed JSON coordinate aborts the whole validation.** `server/customizations/StaffHub/ClusterFMapCheck.cs:543` and `:562`: a location such as `{"x":"bad","y":2,"z":0}`, or an array coordinate outside Int32, throws from `GetInt32()` instead of returning false, so the catch in `ClusterFMapCheckCommands.cs:152` discards all results and reports only a file-read error. Check value kinds and use `TryGetInt32`, then test malformed entries between valid entries so each bad spawner is named and the rest still validate.

6. **Risk: the 500-spot limit does not bound file processing on a live shard.** `server/customizations/StaffHub/ClusterFMapCheckCommands.cs:138` and `server/customizations/StaffHub/ClusterFMapCheck.cs:436`: the handler loads the entire file, JSON parsing builds the entire document, every parser continues through the remaining input, and `BadLines` can grow without a cap, so a large file can consume server time and memory even after 500 spots have been accepted. Add a byte limit before loading, bound malformed-entry storage and total parsing work, and test that oversized input is refused before it is fully read.

7. **Risk: marker lifetime and restart cleanup lack behavioral tests.** `server/tests/Misc/MapCheckVerification.cs:361`: the marker fact checks `Expires` and immediately calls `DeleteAll`, so removing the constructor timer at `ClusterFMapCheck.cs:1021` or the deserialization cleanup at `:1027` would leave it passing. Add separate tests that advance the timer and load a saved marker, then assert deletion without calling `DeleteAll`, watching each test fail with its corresponding cleanup disabled before restoring the code.

## Staff access and live reach

No command is registered without a staff check: `ClusterFMapCheckCommands.cs:47` through `:52` register `CheckFootprint`, `ValidateSpots`, `FindStaticProblems`, `Walkable`, `ShoreCheck`, and `ExportPoints` at GameMaster. Pinned `Projects/Server/Commands.cs:293` enforces that access when the command starts; finding 1 concerns the later callbacks.

All commands are declared `CommandShard.Any`. On a server configured as live, the checks can read map data, reports and exports can write under `map-checks`, and `Walkable clear` can delete diagnostic markers; `Walkable overlay` is refused through `OverlayRefusal(IsTestShard, seconds)` at command line 209. This is the intended live reach recorded by P135, not a newly discovered deployment path. The console's `map.*` plans at `scripts/Shard-Console.ps1:3233` only print syntax; I found no shard execution or Haven connection in those plans.

For finding 1, pinned `Projects/Server/Targeting/Target.cs:146` does not repeat command authorization, `Projects/Server/Mobiles/Mobile.cs:1052` does not cancel the pending target on demotion, and `Projects/UOContent/Mobiles/PlayerMobile.cs:3810` only changes `IgnoreMobiles` when access changes. Pinned `Projects/UOContent/Commands/BoundingBoxPicker.cs:68` invokes the callback without an access check. The pinned source checkout was verified at `d4531cd94b739613155225c234900de9f47d2c88`.

## Scope and verification

Read both work-copy `AGENTS.md` files, `docs/direction-decision.md`, `docs/tasks.md`, and `notes/cc-P135-vseuoaware-staff-commands.md`. No separate P135 review note was found beside it. The known dock and bridge heuristic, unknown-tiledata definition, report retention question, and old console-suite failures are already recorded by P135 and are not repeated as findings.

Reviewed these P135 deliverables:

- `server/customizations/StaffHub/ClusterFMapCheck.cs`
- `server/customizations/StaffHub/ClusterFMapCheckCommands.cs`
- `server/tests/Misc/MapCheckVerification.cs`
- `server/tests/Misc/MapCheckRealDataVerification.cs`
- The P135 actions, plans, safety rule, child arguments, output handling, and Map and Art tab in `scripts/Shard-Console.ps1`
- The P135 facts in `scripts/tests/Shard-Console.Tests.ps1`
- The P135 entry in `CHANGELOG.md` and current `VERSION`

The C# facts exercise the library, JSON writers, file resolver, and marker construction/clearing. The console fact at `scripts/tests/Shard-Console.Tests.ps1:7084` checks registration text rather than invoking the C# handlers, so the callback and export-state regressions requested above need handler-level coverage.

These are source-review findings, not runtime reproductions. No tests were added or run, as this prompt specifies no lane tests; command execution in a client, timer dispatch, save/load behavior, and deployed configuration remain unverified here. No Haven connection, Docker operation, deploy, commit, branch change, code edit, or edit under `docs/` was made.

Ran `tools/progress.py --dry-run` with the work-copy path overrides to satisfy the working agreement. Despite its documented print-only mode, it rewrote `tools/progress.json`; restored that initially clean file byte-for-byte from HEAD so this task leaves only this review note. Checked the stop-request file between review steps; it was absent.

Final validation: code work copy clean; the only docs-work-copy change is this note; whitespace check passed; note is under 5 MB and contains no em dashes.

P508 DONE
