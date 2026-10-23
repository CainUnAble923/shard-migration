# P467: review of P237 New Haven community art

Reviewed 2026-10-23. Code checkout: `4c2af57`; notes checkout: `9acce9f`.
Docs only. No code, art, registry, or test files changed.

Read `cc-P237-new-haven-community-art.md` and
`cc-P237-new-haven-community-art-codex-review.md` first. The earlier review's light-shape
and boardwalk-beam findings are excluded from the findings below.

## New findings

1. **risk** | `shard-migration/notes/cc-P237-tools/gen_layout.py:7`:
   The generator named by `server/customizations/ClusterFCommunityArtLayout.cs:1`
   reads the registry and writes its output in the old Bronze worktree, while
   `protected.py:17` also checks Bronze's customizations, so following the regeneration
   instructions from another checkout can validate stale placement constraints and
   overwrite the wrong branch's layout. Accept explicit code and notes roots, pass
   them through the validator and protection loader, and test that generation targets
   only the selected checkout.

2. **risk** | `player-package/tests/Build-UoOverrides.Tests.ps1:456`:
   The lantern animation assertions check the base ID and registration of whatever
   frames the JSON supplies, but reducing the frames to `[0]` still passes the
   unchanged P237 fact and would leave the lantern showing one frame without flicker.
   Assert the intended `0,1,2,1,0,0,1,0` sequence, interval `6`, and start `0`, and
   check the lantern's encoded animdata bytes with an independent expected value.

No additional runtime bug was confirmed. No new stock art ID collision, duplicate
art ID, missing registry row, or door or protected-path conflict was found in the
checked data.

## Evidence and verification

- Read the P237 implementation and its tests:
  `server/customizations/ClusterFCommunityArtSeeder.cs`,
  `server/customizations/ClusterFCommunityArtLayout.cs`,
  `server/customizations/ShatteredRunestone.cs`,
  `server/tests/Misc/CommunityArtVerification.cs`, and
  `player-package/tests/Build-UoOverrides.Tests.ps1`.
  Read the package's `vendor/shattered-legacy-art/registry.csv`, `records.json`,
  and `SOURCE.txt`, plus the P237 tools `art_src.py`, `nhbase.py`, `protected.py`,
  `validate.py`, and `gen_layout.py`.
- Checked the complete P237 art block, IDs `15496` through `15529`
  (`0x3C88` through `0x3CA9`), using `scripts/find-free-art.py`'s `World` and
  `reasons` methods against the stock client at
  `D:/ShatteredLegacy/client-data/classic-client-7.0.117.0` and pinned ModernUO
  `d4531cd94b739613155225c234900de9f47d2c88`. All slots have placeholder art and
  no stock collision reported by those checks. Expected uses in this checkout's
  server code were excluded, as in `--check-registry`.
- Checked `registry.csv` for duplicate art IDs and `records.json` for duplicate
  tiledata and animdata IDs. None found. The P237 package fact also verifies each
  registered PNG, the server record values, the animation frame registrations,
  and the generated `RegisteredIds` list.
- Compared every shipped PNG in `art/15496.png` through `art/15529.png` with its
  converted source from `art_src.py`: dimensions and RGBA pixels match throughout.
  The source file list is `art_src.py`'s `_GROUPS` table.
- Compared all placement tuples in `placement.json` with
  `ClusterFCommunityArtLayout.cs`: identical. Ran `validate.check` for every row
  with its normal shared key and tile sets: all 44 rows passed. For this read-only
  run, loaded the tools in memory and redirected their Bronze code and script
  paths to the current work copies; did not call the generator or the validator's
  output-writing `main`. The full row list is `placement.json` and
  `ClusterFCommunityArtLayout.cs:18` onward.
- Ran the existing
  `TheCommunityArtRecordsAreTheServersTableAndEveryRowIdIsRegisteredWithItsPng`
  fact under `powershell.exe`, Windows PowerShell `5.1.26100.9444`: passed.
  Evaluated its original AST command and assertion functions without the suite's
  animation-build setup or Play facts. Ran that same fact against a temporary
  copy of `records.json` with only lantern `15500`'s frames reduced to `[0]`:
  it still passed. Deleted the temporary fixture; the tracked records were never
  modified. This is a coverage probe, not a new test.
- Confirmed the one-frame consequence in
  `player-package/payload/app/Build-UoOverrides.ps1:194`, which writes the supplied
  frame count and offsets, and local TazUO
  `ClassicUO.Client/Game/Managers/AnimatedStaticsManager.cs:100`, which cycles
  those offsets. No client was launched.
- Ran `tools/progress.py --dry-run` with both roots pointed at these work copies.
  It completed, but its `build()` writes `tools/progress.json` even in dry-run mode.
  Restored that generated change to its initially clean version; only this review
  note remains changed.

Unverified: live-world contents, player-built obstacles, visual overlap in a running
client, and in-game walking through the layout. The offline validator checks anchor
tiles and its defined protection rules; it does not prove complete sprite footprints
or route connectivity. The C# suite, full package suite, Docker build, and package
build were not run for this notes-only review. No Haven connection, deployment,
world mutation, or commit was made.

P467 DONE
