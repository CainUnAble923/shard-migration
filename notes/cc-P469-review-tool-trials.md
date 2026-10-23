# P469: review of P214 tool trials

Reviewed 2026-10-23. Notes only. No product code changed.

## Scope

P214 trialed desktop tools, not an in-game trial system. There are no P214 tool-use or durability hooks, player rewards, or logout recovery paths to review, so there are no findings in those requested categories. No separate P214 review was found beside `notes/cc-P214-tool-trials.md`.

The findings below concern the desktop tools P214 evaluated. They do not repeat its network-call findings, UOP limitations, missing facet picker, unsupported region metadata, or deferred SpriteMotion trial.

Paths used below:

- `R/`: `D:/UO/third-party/code/uo-region-editor/UORegionEditor-main/`
- `T/`: `D:/UO/third-party/code/uotinker/uotinker-0.2.0/`
- `M/`: `D:/UO/ModernUO-pinned/`, pinned to `d4531cd94`.

## Findings

1. **bug** | `T/src/Core.cs:1153`: Saving tiledata twice in the same second reuses the backup filename and overwrites the original backup because `File.Copy` allows replacement; a probe saved "first" and then "second" and left only the backup containing "first", losing the pre-edit version. Use a unique filename created without overwrite for every backup, including the equivalent art, gump, and table backup paths at `Core.cs:318`, `Core.cs:584`, and `Tables.cs:14`.

2. **bug** | `R/ModernUoJson.cs:107`: Importing the valid ModernUO area `{"x":100,"y":200,"width":5,"height":6}` silently creates a one-tile region at 0,0 because missing corner fields default to zero, although pinned ModernUO accepts this format in `M/Projects/Server/Json/Converters/Rectangle3DConverter.cs:110`. Support the loader's alternate rectangle formats or reject unsupported input before importing it, and add a regression case using this example.

3. **bug** | `R/ModernUoJson.cs:49`: Importing a ServUO region with type `Jail` and exporting ModernUO preserves `"$type":"Jail"`, which the pinned loader does not register, even after selecting ModernUO as the target; its registered name is `JailRegion` (`M/Projects/UOContent/Regions/RegionJsonRegistration.cs:14`). Validate type names against the pinned loader and require an explicit mapping for incompatible ServUO names before exporting, with a ServUO import to ModernUO export regression test.

4. **risk** | `T/src/SelfTest.cs:115`: The data checks only append observed values to a report, so wrong saved values, pixel mismatches, or an incorrect backup can still finish normally and return exit code zero through `T/src/MainForm.cs:866`; the checksum rejection check at `SelfTest.cs:414` likewise only logs failure. Make incorrect results fail the test process and add offline regression tests for backup collisions and save failures rather than treating the diagnostic report as an assertion suite.

## Evidence and limits

Read P214's complete notes and existing trial reports, the editor's model, import/export paths and tests in `Program.cs`, and uotinker's save, backup, UI lifecycle, and self-test paths. Checked the actual pinned region registration and rectangle converter rather than relying on the editor's comments about supported types.

Small probes invoked the existing P214 assemblies from `D:/UO/tool-trials/`, without launching their GUI or self-test entry points. SHA-256 comparisons confirmed that `ModernUoJson.cs`, `ServuoXml.cs`, `Core.cs`, and `SelfTest.cs` in the trial source match their intake copies.

Observed results:

- Rectangle round trip: the width/height example exported as `{"x1":0,"y1":0,"x2":1,"y2":1}`.
- Actual ServUO XML import followed by ModernUO export: the `Jail` type remained `Jail`.
- Tiledata saves: both returned no error, `SAME_SECOND=True`, `BACKUP_PATH_REUSED=True`, `BACKUP_COUNT=1`, and `BACKUP_NAME=first`.

Probes used a synthetic tiledata file under the work copy's ignored `downloads/p469-review-probes/` directory, verified with `git check-ignore`. No client data, installed tool, profile setting, or upstream source was changed. The small probe driver and fixtures remain in that ignored directory for reproduction. The PowerShell driver ran with Windows PowerShell 5.1 (`powershell.exe`). These were defect reproductions, not new committed tests or fixes.

Unverified: full shard loading of the invalid type, GUI interaction, simulated interrupted writes, and SpriteMotion execution. No claim of an in-game reproduction is made. Existing self-tests were inspected, not rerun; in particular, uotinker's self-test would repeat the network activity P214 already documented. No Haven connection, deployment, build of the shard, or commit was performed.

`tools/progress.py --dry-run` completed against these work copies. It unexpectedly rewrote `tools/progress.json` despite the dry-run flag; that generated change was restored so this review delivers only this notes file. Its shared project status warnings were outside this review's scope and were left unchanged.

P469 DONE
