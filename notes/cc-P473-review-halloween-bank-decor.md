# P473: Review of the P267 Halloween bank decor

Reviewed October 23, 2026. Notes only. No implementation changes.

Read `cc-P267-halloween-bank-decor.md` first. No separate P267 review was present beside it. The findings below do not repeat its client walkthrough, community art, or placement caveats.

## Findings

1. **bug** - `server/customizations/ClusterFSeasonalSwitch.cs:206`: If staff place decor on October 23 after an out-of-season check, save, and next start the shard on November 3, both checks see `LastAutomatic == false`, so cleanup never runs and the nondecaying decor stays up until staff clear it or the following season ends. Persist enough timing information to recognize a season that passed during downtime, preserve the intended early preview behavior, and add an October 23 placement to November 3 restart regression case.

2. **risk** - `server/tests/Misc/HalloweenDecorVerification.cs:85`: The placement fact checks banker distance and teleporter tiles but has no door, swing, or approach exclusions, so replacing `britain/lantern-1` with an impassable pumpkin at the generated bank door at Trammel `1438,1692,0` still passes its assertions. Check the compiled layout against independently maintained protected door tiles and paths, or make the build verify the generated C# against the validated placement data, with a door-blocking mutation required to fail.

## Evidence

For finding 1, a temporary .NET 10 probe compiled the unchanged `ClusterFSeasonalSwitch.cs` with minimal host stubs and placement/removal delegates. A normal October 24 to November 3 sequence called removal once; an October 23 check, simulated staff placement, and next check on November 3 called removal zero times and left the simulated pieces present. The probe exited 1 because cleanup was expected. This verifies the switch branch, not a full world restart; the saved boolean is round-tripped by the existing persistence test, and the placement command does not update it (`ClusterFHalloweenDecorSeeder.cs:92`).

For finding 2, a separate temporary probe compiled the actual generated layout and the extracted placement fact, using throwing assertion helpers and a stub for map-name lookup. The original rows passed; changing only the row in memory to the pumpkin and door coordinates above also passed, so the probe exited 1 because rejection was expected. The door coordinates came from P267's map scanner, and stock tiledata marks `0x4691` impassable. No source or placement file was mutated. The offline validator is not called by `docker/uo/build.sh` or `apply-patches.sh`.

Both probes ran against existing code before any fix. No fixes or permanent tests were added. Their temporary project files remain under `scripts/shard-console-cache/p473/`, proven ignored with `git check-ignore`; automatic approval review rejected folder cleanup as "blocked by policy." The largest scratch file is 162,304 bytes.

## Checks and limits

- Re-ran `notes/cc-P267-tools/validate.py` against the local client files and pinned ModernUO `d4531cd94b739613155225c234900de9f47d2c88`: exit 0, 316 rows, zero failing, 21 banks. The artifact files are `notes/cc-P267-tools/placement.json` and `server/customizations/ClusterFHalloweenDecorLayout.cs`; every generated row matched the JSON exactly, including coordinates, item ID, name, hue, and mode.
- No currently blocked banker or door was identified by those map checks. Actual movement and door use in a client remain unverified.
- No additional rerun duplication defect found. Placement considers both tracked and stray item keys (`ClusterFHalloweenDecorSeeder.cs:161`), while clear deletes tracked and stray decor and leaves unrelated item types alone (`:203`). Existing tests cover repeat placement, repeat clearing, filtered clearing, state serialization, stale serials, and stray cleanup.
- The existing automatic-state test visits the season opening before its end (`HalloweenDecorVerification.cs:175`), so it does not cover finding 1. Related seasonal assertions in `WinterDecorVerification.cs` and `Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonVerification.cs` also visit the opening.
- No full build, xUnit suite, game client, live account, container, or Haven connection was used. No lane tests were required. PowerShell commands ran in Windows PowerShell 5.1; the probes used the installed .NET 10 SDK.
- Ran the required progress report with work-copy paths and `--dry-run`. It nevertheless rewrote `tools/progress.json`; that generated change was restored so the deliverable remains this review note only.

## Files reviewed

Paths below are relative to the code work copy unless prefixed with `shard-migration/`.

- `server/customizations/ClusterFSeasonalSwitch.cs`
- `server/customizations/ClusterFHalloweenDecorSeeder.cs`
- `server/customizations/ClusterFHalloweenDecorLayout.cs`
- `server/tests/Misc/HalloweenDecorVerification.cs`
- Related seasonal assertions in `server/tests/Misc/WinterDecorVerification.cs` and `server/tests/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonVerification.cs`
- Relevant placement entries in `server/customizations/ClusterFNewHavenSeeder.cs`
- `docker/uo/build.sh`, `docker/uo/apply-patches.sh`, `docker/uo/COMMANDS.md`, Halloween entries in `CHANGELOG.md`, and `VERSION`
- `shard-migration/notes/cc-P267-halloween-bank-decor.md`
- `shard-migration/notes/cc-P267-tools/bankbase.py`, `gen.py`, `validate.py`, `gen_layout.py`, and `placement.json`
- Pinned source: `Projects/Server/Serialization/GenericPersistence.cs`, `Persistence.cs`, `Projects/Server/Items/Item.cs`, `Projects/UOContent/Misc/DoorGenerator.cs`, and `Projects/UOContent/Items/Construction/Doors/BaseDoor.cs`

P473 DONE
