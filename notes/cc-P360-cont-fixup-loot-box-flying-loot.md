# cc-P360: fix-up for P242 (flying loot): merge with main

**Golem:** Bronze. **Date:** 2026-10-21. **Branch:** `golem/Bronze/P360` in both work copies.

## Headlines

- P242 (flying loot out of loot boxes) now merges cleanly with main: the four conflicts were all "both sides
  appended at the same place" with P241 (achievement category icons). Both sides are kept in every file.
- **Version:** P241 shipped the patch notes as 2026.10.21.13, and P242 had used the same number. P242's lines now
  go under a new section **2026.10.21.14** above P241's, and VERSION is 2026.10.21.14. Keeping them under .13 would
  have hidden the flying-loot notes from players who already saw the .13 login bulletin (it shows once per version).
- Tests: package facts **18 of 18**; `scripts\tests` **55 of 55**; `validate-art.py check-registry` **0 of 244 rows
  have problems**; `find-free-art.py --check-registry` **0 of 244 registered IDs are no longer free**. Server gate:
  see "Build" below.

## How the merge was done

The hand-off forbids switching branches, and `golem/Bronze/P360` was created at main (`9b9bea3`). So instead of
checking out P242 and merging main into it, I ran `git merge --no-commit --no-ff golem/Bronze/P242` on P360 in both
copies. The tree is the same either way; the Golem's commit records the merge (MERGE_HEAD is P242).

- shard-migration: no conflicts (P242's notes, its two tools and the preview PNG).
- ShatteredLegacy: four conflicts, resolved as below. `records.json` and the server files merged on their own.

## Conflicts resolved

| File | Resolution |
|---|---|
| `CHANGELOG.md` | P241's Added/Staff lines stay under 2026.10.21.13; P242's Added/Staff lines under a new 2026.10.21.14. |
| `VERSION` | Not a conflict (both had .13); set to 2026.10.21.14 to match the new section. |
| `player-package/vendor/shattered-legacy-art/registry.csv` | P241's ten gump rows (22459-22468), then P242's 54 art rows (15536-15589). |
| `player-package/vendor/shattered-legacy-art/SOURCE.txt` | P241's achievement-icon section, a blank line, then P242's flying-loot section. |
| `player-package/tests/Build-UoOverrides.Tests.ps1` | Ledger: **244 rows, 15 gump rows, 204 art rows** (the figures P242's notes predicted), comment names both sets. Both new facts kept (P241's achievement-icon fact, then P242's flying-loot fact). |

## Build

`docker\uo\build.sh -t sl-modernuo:cc-P360`, each run detached with its log in the session scratchpad,
docker-build lock taken (waited for ShadowIron), Docker VM page cache dropped first (2.9 GB free -> 6.9 GB).

| Run | Result |
|---|---|
| 1 | 2,024 tests, 1 failed: `WispOrbPossessionVerification.APossessedCreatureFightingNeverBecomesItsMastersCombatant(ForestNymph, Naba)`, "the fight did not start". The known wisp-orb flake (P135, P177, P241, P261 notes). |
| 2 | 1 failed: `CovetousVoidSpawnVerification.SetupPlacesTheControllersThePoolTheSpawnersAndThePaths`, an ogre bone crusher at (5500, 1811, 0) out of bounds. The known random-spawn flake (P194, P227, P238 notes). Run 1's wisp test passed. |
| 3 | **green: 2,024 tests, 2,020 passed, 4 skipped, 0 failed**; image `ef98d2aba78f`, VERSION 2026.10.21.14 read back from the container. |

The four `LootBoxFlyingLootVerification` facts and the eight `LootBoxFanfareVerification` facts passed in all three
runs. Neither flake touches anything this merge changed. Both have now recurred many times across prompts and
deserve their own small fix-up prompt.

## For Chase

Nothing new beyond P242's own "For Chase" list (`notes\cc-P242-loot-box-flying-loot.md`): look at the effect in a
client after the player package is rebuilt. With the bump to .14, accounts that already saw the .13 bulletin
(achievement icons) get a second one with the flying-loot notes.

P360 DONE
