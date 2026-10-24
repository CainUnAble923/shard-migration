# P505: Review of the kitsune paperdoll refit

2026-10-23. Notes only. P138 commit `61c4291` is an ancestor of local `main` at `579ad58`, which is also the code work copy's HEAD. Read both working agreements, the direction and task documents, P138's notes and generators, P166's follow-up, and the P138-related finding in P379's review. No separate P138 review was found beside its notes.

Reviewed the canonical item and its C# tests, both gumps, registry and animation records, animation sources and encoder, fit specification and checker, Python fit tests, package staging and animation gates, launcher override code, and relevant package tests. Client behavior was checked against the local TazUO source used by P138.

## New findings

1. **risk**, `scripts/build-equip-anims.py:364`, `player-package/Build-PlayerPackage.ps1:197`: Removing an entire required action/direction from the source passes both the encoder's round-trip check and the package animation gate, so P138's disappearing-while-standing defect could return without a refusal. Add a regression test and an explicit Animation 4783 coverage requirement for actions 0, 2 and 4 in directions 0 through 4, with their expected frame counts, while keeping intentionally unsupported actions optional.

2. **risk**, `scripts/check-paperdoll-fit.py:147`, `scripts/check-paperdoll-fit.py:252`, `scripts/tests/test_check_paperdoll_fit.py:150`: The SFW body check does not detect moved hips if the crown stays unchanged, and the tail check still trusts the old JSON box, so changed body art can leave the tail detached while the gate passes. Pin each measured body's alpha silhouette or validate its lower-back geometry against the specification, and add a test that moves the hips while preserving the crown.

These are confirmed validation gaps, not claims that the committed assets currently lack standing frames or have detached paperdoll tails. No additional current rendering bug was confirmed.

## Evidence and checks

- For finding 1, copied only Animation 4783's sources and its equipment record to ignored scratch, omitting `anim-src/4783/a04_d2_f00.png`. Encoding returned 0, `--check` returned 0 and printed `anim7 matches`, but reading slot 400, action 4, direction 2 returned no block. Invoking the actual `Test-EquipAnims` and `Get-Anim7SlotEnd` functions extracted from the package builder under Windows PowerShell 5.1 returned zero failures on those files. The whole package builder was not run.
- For finding 2, copied the SFW bodies and shifted body 13's pixels from row 80 downward by 20 columns to the right, preserving its crown and upper body. At the tail root's row 111, the body's left edge moved from column 80 to 100 while the gump root stayed at column 79. `Fit.check()` still returned true with no failures.
- The unchanged committed art passed `python scripts/check-paperdoll-fit.py`: gumps 54783 and 64783 on bodies 12/14 and 13/15, respectively. The actual Topless and Nude add-ons are absent here and were skipped.
- All 13 existing `test_check_paperdoll_fit.py` tests passed. Initial attempts could not create fixture children because of sandbox permissions on Python's temporary directories; the successful run supplied scratch roots created with ordinary directory permissions through an in-memory `tempfile.mkdtemp` replacement. No test file was changed.
- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File player-package/tests/Paperdoll-Bodies.Tests.ps1`: all nine existing facts passed. No tests were added. The shard C# suite and launcher suites that contact the test shard were not run.

## Asset inventory and limits

No new collision or missing kitsune package source was found in the checks below:

- Registry entries occur once each for item art 15420, Animation 4783, male gump 54783 and female gump 64783. Their sources are `player-package/vendor/shattered-legacy-art/art/15420.png`, `gumps/54783.png`, `gumps/64783.png`, and `anim-src/4783/`.
- For each drawn direction 0 through 4, `anim-src/4783/` contains `a00_d<direction>_f00.png` through `f09.png`, `a02_d<direction>_f00.png` through `f09.png`, and `a04_d<direction>_f00.png`. These are all 105 expected walk, run and stand sources, grouped explicitly here rather than inferred from the notes.
- The only vendored overrides named 54783.png and 64783.png are the shard's own gumps. The package builder stages both registered gumps and rejects clashes with the other vendored gump sets.
- Read-only checks against `D:\ShatteredLegacy\client-data\classic-client` found neither gump in `gumpartLegacyMUL.uop`, `gump.def` or the gump field of `Equipconv.def`. Animation 4783 has no EA tiledata reference, animation-definition reference or occupied people slot in `anim.idx`; item 15420 has no EA tiledata flags or name. This was not a full fresh collision scan of maps, multis, tileart and animation UOP files.

P138/P166 already document unsupported actions, hood behavior, male overlap, the West/North tail correction, bald-head placement and the standing East/South tail issue. P379 already documents the male registry row's incorrect hex spelling. Those are not repeated as new findings.

Fresh ZIP contents and live client appearance remain unverified. No code, tests, docs directory, live server, branch or deployment was changed. Scratch is under `downloads/p505-review/`, proven ignored by `.gitignore:55`; no scratch file exceeds 5 MB.

P505 DONE
