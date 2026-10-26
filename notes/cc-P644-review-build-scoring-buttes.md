# P644: review of P632 scoring buttes

Reviewed October 26, 2026. Docs-only review. No code changed.

P632 correctly delivers P571's first ordered stage, BUTTE-A. I found no current artwork, mapping, or tiledata defect. The findings below are low-severity regression-test gaps. They do not establish a current player-facing bug or exploit.

## Scope and authority

Reviewed code commit `bfee2f8c47a002fa3c697a2f7e84c5a7ef2ea7a4`, merged as `313d94d`, against current code HEAD `a3f017e`. Notes HEAD at review start was `f9f965cc334a92b562a8107a10f3c02f549dded6`.

Read both work copies' AGENTS.md, the direction decision, governing-document list and task list. Read `cc-P632-build-scoring-buttes.md`, its Codex review, `cc-P571-design-butte-and-deed.md`, its Codex review, and the earlier P405 review. P632's and P571's reviews reported no findings. P405's missing engine hooks were already addressed in the design and are not repeated here.

Chase's answers were checked in `D:/UO/overseer/decisions-2026-10-22.md:23` and `decisions-2026-10-23.md:60`. The first requires art proof and names the yard and deed destinations. The second accepts P571's defaults. P632's artwork-only scope follows P571's BUTTE-A section. Scoring, house deeds, crafting, public placement and installed-client proof belong to BUTTE-B through BUTTE-D. Their absence from this stage is not a finding.

Code paths below are relative to the ShatteredLegacy work copy. Notes paths are relative to this repository's `notes/`.

## Findings

### 1. Low: the mapping test allows the wrong ring or ammo picture

**Location:** `server/tests/Items/ScoringArcheryButteArtVerification.cs:49`, especially the fixed-point assertions at `:55`.

**What happens:** The test verifies uniqueness, the overall ID range, facing blocks and five exact state/facing pairs. It does not verify every state's exact picture. For example, swapping the offsets for `ArrowInner` and `ArrowMiddle` in `ScoringArcheryButteArt.ItemId` preserves every assertion: the IDs remain distinct, both facing sets stay in range, and none of the fixed points changes. A later scoring component would then show middle for an inner hit and inner for a middle hit while this test stayed green. The broad facing assertions also permit some arrow and bolt states to trade blocks.

**Evidence:** This is an assertion-coverage finding from reading the test and switch table, not a claimed executed C# mutation. The current switch is correct against the registered source filenames. P571's Package and records acceptance row explicitly calls for a broken mapping to fail its check. P632's recorded mutations cover a missing PNG, record height, C# weight and enum numbering, but not this semantic mapping error.

**Fix:** Assert a literal expected `(display, east ID, south ID)` table for all logical states. Keep it independent of the production block constants and offset calculation. Demonstrate failure by swapping inner and middle, then restore and pass. Include a south-facing invalid enum fallback alongside the existing east case.

### 2. Low: the package parity fact leaves tiledata fields unchecked

**Location:** `player-package/tests/Build-UoOverrides.Tests.ps1:340`.

**What happens:** The new fact compares name, flags, weight, height and animId, but omits layer, count, hue and light. It can therefore report that the records match the server while those shipped fields differ. The current records correctly have zero in every omitted field. This is a missing regression guard, not evidence that P632 currently ships mismatched tiledata.

**Evidence:** Under Windows PowerShell 5.1.26100.9711, I extracted and invoked the existing `TheScoringButteRecordsAreTheServersTableAndEveryPictureIsThere` fact with its existing assertion helpers against a temporary minimal copy of the relevant tree. Baseline passed. Changing only record 46690's layer from 0 to 1 still passed, although the server's `ItemData` constructor supplies 0. A control mutation changing height to 9 failed with `expected [10] but got [9]. height of 46690`. Restoring the records passed. All mutations were outside both repositories. P571's art section requires the full relevant stock record, and its acceptance table requires matching server/client tiledata.

**Fix:** Extend the fact to assert all four omitted fields against their intended zero values, then exercise each assertion with a temporary nonzero mutation. Assert the corresponding exposed server fields in `EveryPictureHasTheStockButtesRecord` where applicable. Keep the client binary layout and ModernUO's field interpretation distinct when choosing those assertions.

## Verification and non-findings

Reviewed the complete P632 source/data changes:

- `server/customizations/Items/Addons/ScoringArcheryButteArt.cs`
- `server/customizations/ShatteredRunestone.cs`
- `server/tests/Items/ScoringArcheryButteArtVerification.cs`
- `player-package/tests/Build-UoOverrides.Tests.ps1`
- `player-package/vendor/shattered-legacy-art/SOURCE.txt`
- `player-package/vendor/shattered-legacy-art/records.json`
- `player-package/vendor/shattered-legacy-art/registry.csv`
- Every PNG listed below under `player-package/vendor/shattered-legacy-art/art/`.

Also read the conversion tool, relevant package staging/override code, pinned ModernUO `Projects/Server/TileData.cs`, and the downloaded source manifest and butte script. The downloaded script is reference material only; P632 does not install it.

An independent read-only pixel comparison checked every PNG against its named BMP under `D:/UO/third-party/code/archery-butte-hits/Archery Butte/`. Expected conversion was RGB unchanged, pure black alpha 0, every other pixel alpha 255, with the original 66 by 81 canvas retained. Every comparison passed. This is the measured file list; SHA-256 values are PNG prefixes:

| PNG | Source relative to Archery Butte/ | SHA-256 prefix |
|---|---|---|
| 46690.png | Arrows/Arrow East Bullseye.bmp | 5930db299779 |
| 46691.png | Arrows/Arrow East Inner.bmp | a672734f42c3 |
| 46692.png | Arrows/Arrow East Middle.bmp | 44d25efc74d0 |
| 46693.png | Arrows/Arrow East Outer.bmp | 92365b3b2934 |
| 46694.png | Arrows/Arrow East Total Miss.bmp | 12142973b06d |
| 46695.png | Arrows/Arrow South Bullseye.bmp | 1e10a4fd103a |
| 46696.png | Arrows/Arrow South Inner.bmp | c261c32e458c |
| 46697.png | Arrows/Arrow South Middle.bmp | f2ea5d5277ef |
| 46698.png | Arrows/Arrow South Outer.bmp | 6920f77a2257 |
| 46699.png | Arrows/Arrow South Total Miss.bmp | fbb3122dab3c |
| 46700.png | Bolts/Bolt East Bullseye.bmp | dba00ab172dc |
| 46701.png | Bolts/Bolt East Inner.bmp | 3c2427adbde4 |
| 46702.png | Bolts/Bolt East Middle.bmp | 7f4f053915aa |
| 46703.png | Bolts/Bolt East Outer.bmp | 52f180d588d2 |
| 46704.png | Bolts/Bolt East Total Miss.bmp | f632dd2d2c61 |
| 46705.png | Bolts/Bolt South Bullseye.bmp | d1a05bfb22f9 |
| 46706.png | Bolts/Bolt South Inner.bmp | 98a849a7cbc8 |
| 46707.png | Bolts/Bolt South Middle.bmp | c065eda76607 |
| 46708.png | Bolts/Bolt South Outer.bmp | 51386fcb7418 |
| 46709.png | Bolts/Bolt South Total Miss.bmp | 2014e5dbab7d |

The registry IDs and tiledata IDs independently checked as exactly 46690 through 46709, once each. Enum values and current state/facing mappings match the design. `ShatteredLegacyArt.Apply` calls the new record application. The record array is within pinned ModernUO's 65,536-entry item table.

Read stock 0x100A and 0x100B from `D:/UO/UOAlive/UOAlive 7.0.116.0/tiledata.mul`, whose SHA-256 is `44f48a4598dbe6e29a157ee11433e18202772719d344a3fdf1d2d624c48af35c`. Both match every shipped butte record: name `archery butte`, flags `0x8040`, weight 255, height 10, and layer/count/animId/hue/light all 0. This independently confirms the concrete stock values reported by P632; it does not certify every file in that client installation.

Another temporary probe duplicated registry row 46690 in place of 46691. The new focused fact still passed. I did not promote that result to a separate defect: `Build-PlayerPackage.ps1:783` already rejects an art PNG absent from the registered ID set. The shipped registry is correct, and the focused-fact result alone does not prove that a bad registry can ship.

P632 adds no saved entity class or inherited save fields. Its enum is explicitly numbered for later use. Save/load, ammo recovery, deed duplication and tutorial-loan exploit behavior cannot be exercised in this stage because no scoring component or deed exists yet. Those remain acceptance work in the recorded follow-up stages, rather than newly discovered omissions.

## Limits and final checks

No new test was added. No full server gate, full package suite, package build, free-slot rescan, installed-client check or world save/load was run for this docs-only review. P632's historical green build and stale-client package-suite results were read, not independently rerun. Distribution permission and the required clean install/update visual proof remain explicitly unverified as the design and P632 already state. They are not new findings here.

The executed package probes invoked only the existing focused fact and assertion helpers, avoiding the full suite's launcher/network paths. Scratch script: `%TEMP%/P644-review-existing-fact.ps1`. Scratch data: `%TEMP%/P644-butte-review-dca96ef3f96f4fb991634a3f0078aca9`. Neither contains a file over 5 MB.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` set to these work copies; exit 0. The reporter still writes `tools/progress.json` during dry run, so its original bytes were restored in finally and SHA-256 equality checked. Its filename census is not a behavioral verification or a new coverage claim.

Document checks passed: valid UTF-8, no em dashes, no replacement characters or trailing whitespace, and below 5 MB. Both repositories passed `git diff --check`. The reviewed P632 files are unchanged between its implementation commit and current code HEAD.

No Haven connection, deployment, service action, commit, merge, push or branch switch. No `docs/` edits. Only this notes file is changed. Stop-request checks between steps found no request.

P644 DONE
