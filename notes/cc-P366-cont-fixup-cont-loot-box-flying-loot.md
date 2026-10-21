# cc-P366: second fix-up for P242 (flying loot), merged again with main

**Golem:** Bronze. **Date:** 2026-10-21. **Branch:** `golem/Bronze/P366` (ShatteredLegacy work copy). **Image:**
`sl-modernuo:cc-P366`.

## In plain words

- The flying-loot animations from P242 (the item that arcs out of an opened loot box) can now be merged alongside
  the League Hall decor that reached main while they waited. Both sets of art are kept, and no art numbers changed.
- Players will see both once the next player package is built: flying loot uses art 15536 to 15589, and the
  League Hall decor uses 15592 to 15629.
- The changelog shows the flying-loot lines under version 2026.10.21.15, beside the Golem email changes.
- Nothing for you to do.

## What was merged

In `D:\UO\golems\Bronze\ShatteredLegacy` on `golem/Bronze/P366`:

1. The branch started at `origin/main` `d62d2a4` (P157 merged).
2. `git merge origin/golem/Bronze/P360` (`84ed5f3`: P242 `74d6af4` plus P360) conflicted in six files: the five
   the prompt names, plus `VERSION`.
3. `git merge origin/main` afterwards was a no-op, because the branch already was main. A fetch at the end found
   `origin/main` still at `d62d2a4`, so step 4 had nothing to merge.

The merge is resolved and staged (`MERGE_HEAD` is set). Following the prompt, I made no commit; the Golem's commit
records it as the merge commit.

## The conflicts and how each was resolved

| File | Main side (P243 League Hall, P157) | P242/P360 side | Resolution |
|---|---|---|---|
| `registry.csv` | +38 art rows, 15592-15629 | +54 art rows, 15536-15589 | Main's file byte for byte, then P242's 54 rows appended unchanged. 190 + 38 + 54 = **282 rows**, no duplicate (id, kind). |
| `records.json` | tiledata +38 (15592-15629) | tiledata +9 and animdata +9 (bases 15536, 15542 ... 15584) | Both kept. In the tiledata list, P242's lines come before main's, in ascending ID order. animdata merged without a conflict. Totals: 100 tiledata, 20 animdata. It parses as JSON. |
| `SOURCE.txt` | "League Hall decor" section | "Flying loot" section | Both sections: main's first, then a blank line, then P242's. |
| `Build-UoOverrides.Tests.ps1` | The Kitsune fact excludes 15592-15629; registry counts 228 / art 188; new League Hall fact | Excludes 15536-15589; counts 244 / art 204; new flying-loot fact | The Kitsune filter excludes both ranges. The counts are now **282 rows, 242 art, 15 gump** (gump unchanged). Both new facts are kept. |
| `CHANGELOG.md` | 2026.10.21.15 (P157, Staff) and .14 (P243) | Its own 2026.10.21.14 (Added + Staff) | P242's lines moved under the newer heading, .15: a new `### Added` holds the flying-loot line, and its Staff line goes last under `### Staff`. Main's .14 is unchanged. |
| `VERSION` | 2026.10.21.15 | 2026.10.21.14 | The higher: 2026.10.21.15. |

**Renumbered IDs: none.** P242 uses 15536-15589 and P243 uses 15592-15629. I compared the merge-base, main and
P360 index stages of `registry.csv` by (id, kind):

- no ID collides
- no base row changed on either side
- the two new ranges do not overlap

No reference needed changing. A search of `player-package`, `scripts` and `server\tests` found no other hard-coded
count of 228/244 rows or 188/204 art rows.

## Tests

- **Package tests** (`player-package\tests\`, each run on its own under `powershell.exe`):
  - Build-UoOverrides: 19/19
  - Cliloc-Overrides: 10/10
  - Launch-Settings: 27/27
  - Legion-Scripts: 24, 0 failed
  - Map-Overrides: 7, 0 failed
  - Paperdoll-Bodies: 9/9
  - **Package-Client: 3 of 9.** The six failures are all "No EA client data in
    `D:\UO\golems\Bronze\ShatteredLegacy\client-data\classic-client`". That folder is git-ignored and absent from
    this work copy, and the suite runs a real package build. The merge touches none of `PackageClient.ps1`, the
    client folder or the package builder, so this is the environment, not the merge (unverified against a work copy
    that has client data).
- **P242's server tests** (`LootBoxFlyingLootVerification`, filtered run on `sl-uo-builder:cc-P366`): 4/4 passed.
- **Image:** `docker\uo\build.sh -t sl-modernuo:cc-P366` (under the docker-build lock, after dropping the Docker
  VM's page cache because only 0.9 GB was free): `Built sl-modernuo:cc-P366 with patches applied and 2025 shard
  test(s) passing.`, EXIT=0.

## For the integrator

- **P264 also uses 2026.10.21.15.** P264 (companions B1) was committed on `golem/Bronze/P264` with its own
  `## 2026.10.21.15` section and `VERSION` .15, and it was not on main when I last fetched. Whichever of the two
  merges second will conflict in `CHANGELOG.md` and `VERSION` the same way this one did.

P366 DONE
