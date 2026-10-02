# cc-P38: ModernUO upgrade, part 2 of 3: the engine bump to upstream d4531cd9

2026-10-02. Brief: `D:\UO\cc-prompts\cc-P38-engine-upgrade.md`. Work is in `D:\ShatteredLegacy` and
`D:\UO\shard-migration` (AGENTS.md, tools), **uncommitted**. Neither shard was deployed, restarted or recreated;
`sl-modernuo:latest` was not moved. No commit landed in either repo while I worked (`a529979` / `17a0ef5` at start
and end). Gate image `sl-modernuo:cc-p38` (`45b7523ae54b`), builder `sl-uo-builder:cc-p38` (`8c9e0653cfb7`).

Citations: **P:** pinned `7c9215d97`, **U:** upstream `d4531cd94`, both under `Projects/`. Unmarked line numbers in
our own files are today's working tree.

## Headlines

1. **The bump is green.** `build.sh -t sl-modernuo:cc-p38`: **36/36 patches at `--fuzz=0`, 451/451 shard tests**
   (P37's 455, minus the 5 purge facts, plus 1 new mining fact). Upstream's own suites on the same builder:
   **Server.Tests 893 passed, 17 skipped, 0 failed. UOContent.Tests 1,095 passed, 91 skipped, 1 failed** (item 2).
   `hook_audit.py`: **0 real mismatches** (8 raw, all explained, section 4).
2. **The one upstream failure is our approved deviation meeting upstream's test of the old behaviour. Decision
   needed.** `ImportCleanupTests.Import_DuplicateLocation_ReplacesExistingSpawner` (U:UOContent.Tests/Tests/Engines/
   Spawners/Json/ImportCleanupTests.cs:138-173, added by #2505) asserts that importing a spawner deletes an existing
   same-type spawner at the same x,y. That delete is exactly what P32's `ImportSpawners-guid-key.patch` removes
   (PT-07, 338 stacked spawners lost; red-proved in P32). It is not a regression. P30's upstream-suite run predates
   P32, which is why nobody saw it. I did not patch upstream's test unasked. **Decision 1** below.
3. **D49 done and measured.** `<=` -> `<` (`HarvestDefinition-vein-boundary.patch`). **Starwood now 6,192 of
   6,246,932 lumber banks (expected 6,030, ratio 1.03); Celestial 1,113 of 1,171,705 mining banks (expected 1,131,
   ratio 0.98).** Celestial was 0 before, **measured** now (P37 had deduced it). Red-proved: with the patch put back
   to `<=`, exactly those two facts fail (449/451), each naming 0 banks.
4. **Both load proofs pass on copies, with a TTY attached and no prompt of any kind.** P37's post-purge test save:
   207,152 items, 35,199 mobiles, 2.81 s, saved on stop, `.idx` header **05**, no `SerializedTypes.db`. P30's live
   save copy: 192,177 items, 34,982 mobiles, 2.38 s, the same. Zero error, warning or deserialize lines in either log.
5. **P39 cannot run the purge on the image the test shard runs today.** `[ClusterFPurgeUpgradeCollisions` exists
   only in `sl-modernuo:cc-p37` (checked in each image's `UOContent.dll`: latest 0, cc-p37 2, cc-p38 0). The test
   shard runs `latest` (`246b0d5813e5`), which predates P33 and P37. So P39 runs the purge on `cc-p37`, and after
   the purge save the rollback image is `cc-p37`, not `latest`. I tagged it `sl-modernuo:pre-bump-purge-7c9215d97`
   so P37's "scratch to delete" list cannot take it. The checklist (section 11) is written that way.
6. **Two of the four file deletions this task needed were blocked by the session's permission classifier,
   and then the files were gone anyway.** `ClusterFPurgeUpgradeCollisions.cs`, `PurgeUpgradeCollisionsVerification.cs`,
   `CraftItem.cs` and `CraftContext.cs` (customizations). My `rm` calls were reported as denied; when Chase ran
   `Remove-Item` the paths no longer existed. I cannot say who removed them. Nothing is lost: all four are in HEAD
   `a529979`, and the two craft files' content is in the new patches (byte-identical result, section 4).
7. **The bump stayed inside P30's 4 units.** Beyond the trial replay it took the craft and D49 patches, two compile
   fixes from P33's tests, and the test edits.

## 1. Rollback tags (recorded before any build)

| Tag | Image ID | What |
|---|---|---|
| `sl-modernuo:pre-bump-7c9215d97` | `246b0d5813e5a127...` | `sl-modernuo:latest` at the start, as the brief asked. **Predates P33 and P37.** |
| `sl-uo-builder:pre-bump-7c9215d97` | `ea126d1c449376914a13...` | `sl-uo-builder:latest` at the start |
| `sl-modernuo:pre-bump-purge-7c9215d97` | `0e65420330ca...` | `sl-modernuo:cc-p37`: pinned engine **with** P33, P37 and the purge command. The right rollback once the test shard has saved on it (headline 5). |

`sl-modernuo:latest` is still `246b0d5813e5`, and `sl-uo-builder:latest` is still `ea126d1c4493`. The test shard
(`sl-modernuo-test`, image `246b0d5813e5`) and live (`sl-modernuo`, image `uo-modernuo`) were both running before
and after, untouched.

## 2. Upstream: anything newer?

`git fetch origin main` in `D:\UO\ModernUO-upstream` at the start: `FETCH_HEAD` = `d4531cd94b739613...`. Nothing
landed after the target, so there was nothing to weigh.

## 3. What changed, grouped (`D:\ShatteredLegacy`, 70 files, +344/-3,131)

**Trial replay.** `git apply` of `notes\cc-P30-tools\trial-changes-head-045b313.diff` onto HEAD `a529979`: 53 of 54
files clean. I applied it without `--3way`, to keep the index untouched. The one conflict was `docker/uo/Dockerfile`,
because P37 moved the ARG; I set it by hand (re-pin below). The replay brings: the 101 `[SaveFlag]` rewrites (8 files),
the API fixes in 10 customization files, the 16 test fixes, the 4 rebased patches (CraftGumpItem-MakeX,
UOContentFixture-npc-speeds retargeted to `TestServerInitializer`, BaseCreature-can-auto-stable,
StealableArtifacts) and P32's rebased ImportSpawners-guid-key, and the `"$type"` discriminator in
`SpawnerImportVerification.cs` (brief item 4: **already in the replay, nothing more needed**).

**P33/P37 drift since the trial.**
- `CleanUpBritanniaPointsVerification.cs` (3 sites) and `CustodianLayerVerification.cs` (1): `BufferWriter` lost its
  types-queue argument (U:Server/Serialization/BufferWriter.cs:61-72), the same fix P30 made in 14 other tests.
  These were the first build's only errors.
- P33's `TrashBarrel-` and `TrashChest-clean-up-britannia.patch` apply at fuzz 0 with no change.
- P33's points framework: **upstream ships none of its 17 type names** (`PointsSystem`, `PointsType`,
  `PointsEntry`, `PointsSystemPersistence`, `CleanUpBritannia*`, `CleanUpTrash`, `CleanupTrashBarrel`,
  `TheCleanupOfficer`, `ShameCrystals` and the rest; grepped as declarations in U:, 0 hits).
- P37's purge command and its test are deleted (headline 6). The shard-console fact
  `RedMeansTestOnly...` loses the two purge rows again.

**Collisions (closes D-57).** `type_delta.py` on HEAD's customizations: the 11 types. On the working tree: **0**.
The 10 files are deleted, and `WindOfCorruption.cs` keeps only `WindOfCorruptionHuman`. The script's "upstream
REMOVED" list names `MemoryMapFileWriter`, cited once in `TypeIdentityVerification.cs`, which the replay already
fixes.

**Craft replacements -> patches** (section 4). New `CraftItem-shard-hooks.patch` (21 hunks, +118/-30) and
`CraftContext-shard-hooks.patch` (2 hunks, +31). `apply-patches.sh` drops their `replace_file` lines and their
name exclusions. With the exclusions gone, a stray copy of either file left in customizations would be copied into
`Misc/` and fail the build as a duplicate type, which is the right failure. Comments in `ClusterFCraftRun.cs:16` and
`CraftXVerification.cs:4` now point at the patch.

**D49** (section 5). New `HarvestDefinition-vein-boundary.patch`. `ClusterFMiningExtension` gets a public
`ApplyExtendedVeins(HarvestDefinition)`, as P37 gave lumber, so a test can probe a fresh definition. Live
behaviour is unchanged (same code, same startup log line). `PermanentGrovesVerification` fact 3 is flipped, and a new
fact 4 covers mining.

**Fixture patch name.** P30 suggested renaming `UOContentFixture-npc-speeds.patch` to
`TestServerInitializer-shard-bootstrap.patch`. **Not done**: with deletions blocked in this session, a rename was not
safe to attempt. Its `apply-patches.sh` comment now says what it targets and why. Rename it with
`git mv` in any later change if you want the name to match.

**P37 7.4, `PlayerCommandsNeverAppearInTheWorldTab`: the test's assumption, fixed.** `version` is a real Player
command (`ShardVersion.cs:243`, F-15 in P22). The fact's rule, that player commands stay out of the World tab, held all
along; only its hardcoded list of names predated `version`. The list now includes it. Red: it failed at HEAD with
exactly that difference. Green: console suite **84/84**.

**P37 7.6, the D19 comment.** It was not yet a no-op. While live stays on pinned, its save is idx v3 and has
`SerializedTypes.db`, and the copy is what lets a fresh test world read live's accounts (P30 run 5 loaded that live
save on the new engine with the file present). Both seeders (`test-shard.sh:45-52`, `Start-TestShard.ps1:78-86`)
now say so, and that it becomes a no-op once live saves on the new engine. A v3 `Accounts` without the file on the
new engine was **not probed**.

## 4. Craft patches and the hook audit

- The trial's merged `CraftItem.cs`/`CraftContext.cs` (ours on upstream) diffed against U: gives the two patches.
  On a fresh U: tree, both apply at `--fuzz=0` and reproduce the merged files **byte for byte** (`cmp`).
- `hook_audit.py` (HEAD's `CraftItem.cs` against the merged one): 35 hook lines before, 35 after, **8 mismatches,
  0 real**:
  - 2 pairs (`Refused(m_From, ...)` and the "no prompt in the middle of a Craft X run" comment, `CompleteCraft#1`
    -> `#2`): the audit attributes nested-class code to the last 8-space-indented method. These lines are in
    `InternalTimer.OnTick` (merged `CraftItem.cs:1971`, `:2026`), and upstream's second `CompleteCraft` overload
    (the hue one) now precedes the timer. Same method before and after.
  - 1 pair (`-- Shattered Legacy extended lumber --`, `<class>` -> `InitTypesTable#1`): upstream turned the types
    table into `InitTypesTable()` (merged `:66`). The block sits in the same list, after `YewLog`.
  - 1 pair (`if (!ClusterFCraftRun.Refused(from, craftSystem, 1044153 ...` -> `else if`, `Craft#1`): same method.
    Upstream added a `T2ACraftSystem.Enabled` branch before it (merged `:966-970`).
  - The failed-attempt hook that P30's naive merge misplaced is on the live overload (`AfterAttempt`, merged
    `:1711`, the no-hue `CompleteCraft`). The hue overload (`:1729`) carries no hook and is reached only through
    T2A paths (U:QueryMakersMarkGump.cs:63, CraftItem timer with `m_ResHue`), which are off for us
    (`Core.UOTD`, P30 2b).
  - The three Craft X tests that caught P30's misplacement pass.
- `CraftContext`: 2 hook lines, 0 mismatches.

## 5. D49: the vein boundary, and stock shares before and after

The patch changes one line, U:UOContent/Engines/Harvest/Core/HarvestDefinition.cs:155 (identical at P:). Values
come from `StableRandom.First(seed, VeinWeights)` (U:Server/Random/StableRandom.cs:25), a randomized bank's
`Utility.Random(1000)` (`:138`), or a respawn's `Utility.Random(VeinWeights)` (U:HarvestBank.cs:63), all `0..N-1`.
So `<` gives each vein exactly its weight. With `<=`, the first vein got one value extra and the last one fewer.

**Exact shares (of 1,036 values), before -> after.** Every vein not listed is unchanged.

| | first vein | last vein |
|---|---|---|
| Lumber (ours) | Log 491 -> **490** | Starwood 0 -> **1** |
| Mining (ours) | Iron 497 -> **496** | Celestial 0 -> **1** |
| Stock ModernUO, for reference (1,000 values) | Log/Iron one fewer | Frostwood 9 -> 10, Valorite 13 -> 14 |

The stock row is reasoning from the same rule; our shard runs the extended lists, so the stock last veins are
mid-list for us and unchanged. The shift is one value per 1,036: the first vein gives up about 0.1% of the world
to the last.

**Measured over every bank cell of six facets** (deterministic; `groves-detail.log`):

| Lumber (4x3 banks, 6,246,932) | weight | banks | ratio | | Mining (8x8 banks, 1,171,705) | weight | banks | ratio |
|---|---|---|---|---|---|---|---|---|
| Log | 490 | 2,943,961 | 1.00 | | Iron | 496 | 557,541 | 0.99 |
| Oak | 300 | 1,829,478 | 1.01 | | DullCopper | 112 | 128,791 | 1.02 |
| Ash | 100 | 591,574 | 0.98 | | ShadowIron | 98 | 111,676 | 1.01 |
| Yew | 50 | 296,392 | 0.98 | | Copper | 84 | 96,798 | 1.02 |
| Heartwood | 30 | 185,817 | 1.03 | | Bronze | 70 | 77,106 | 0.97 |
| Bloodwood | 20 | 120,200 | 1.00 | | Gold | 56 | 61,863 | 0.98 |
| Frostwood | 10 | 54,100 | 0.90 | | Agapite | 42 | 48,883 | 1.03 |
| Ironwood | 8 | 53,924 | 1.12 | | Verite | 28 | 31,229 | 0.99 |
| Ghostwood | 7 | 36,362 | 0.86 | | Valorite | 14 | 12,992 | 0.82 |
| Emberbark | 6 | 39,908 | 1.10 | | Platinum | 8 | 9,812 | 1.08 |
| Frostbark | 5 | 31,301 | 1.04 | | Toxic | 7 | 7,391 | 0.93 |
| Shadowbark | 4 | 27,637 | 1.15 | | Blaze | 6 | 7,360 | 1.08 |
| Runewood | 3 | 17,003 | 0.94 | | Frost | 5 | 6,751 | 1.19 |
| Voidwood | 2 | 13,083 | 1.08 | | Obsidian | 4 | 4,920 | 1.09 |
| **Starwood** | 1 | **6,192** | **1.03** | | Mythril | 3 | 4,097 | 1.21 |
| | | | | | Adamantium | 2 | 3,382 | **1.50** |
| | | | | | **Celestial** | 1 | **1,113** | **0.98** |

**Watch: Adamantium sits at 1.495, just inside the fact's 0.5 to 1.5 band.** The numbers are deterministic, so the
fact is not flaky, but any change to the vein list or the seed will move it. The spread is wider for mining because
the seed `x*17 + y*11 + map*3` over 8x8 banks has far fewer distinct values than over 4x3 ones (reasoning, not
measured). Whether that band is the right tolerance is a test-design question, not a defect.

**Red proof.** The patch's `+` line went back to `<=` (marked `MUTATION`), in a tests-only build to its own builder
tag: **449 passed, 2 failed**, exactly facts 3 and 4: "Log: exact share 491, weight 490; StarwoodLog: exact share 0
... 0 banks, expected about 6030" and the same for Iron 497 and Celestial "0 banks, expected about 1131". Restored
from backup (`cmp` identical, `grep MUTATION` = 0), then the green build above.

Bug-list row (overseer's): ModernUO's defect, ours to patch, fine to report publicly (not exploit-class).

## 6. Patches: rebase and red proof

- **Local stage** (`stage-tree.sh` against U:): "All 36 patches applied successfully", 659 structured
  customizations, 76 test files. The Docker gate printed the same.
- **Red proof of every patch, cumulative in `apply_patch` order on a `git archive` of U:** for each patch, the real
  file dry-runs clean, and a copy with one context line of its first hunk mutated is **refused at `--fuzz=0`**. Then
  the real one is applied and the next is tried. **36 real clean, 36 mutated refused.** (`redproof.sh`,
  `redproof.txt`. The 37th line of my order list was `apply_patch() {`, the same `grep '^apply_patch'` miscount P30
  recorded; it is not a patch.)
- That covers every rebased patch, including P32's `ImportSpawners-guid-key` and P29's `AOS-stat-bonus-names` (D44,
  still our own patch, nothing sent upstream), plus the three new ones.
- **Replacements:** the other 10 `replace_file` targets are byte-identical between P: and U: (`git diff --stat`
  empty for all 10), so no upstream drift is hidden under them.

## 7. Re-pin

| Where | Change |
|---|---|
| `docker/uo/Dockerfile:3` | `ARG MODERNUO_COMMIT=d4531cd94b739613155225c234900de9f47d2c88` (full hash). The banner prints it: both proof logs say `Commit: d4531cd94b73...`. |
| `docker/uo/docker-compose.yml:8` | `MODERNUO_COMMIT: "d4531cd94b739613155225c234900de9f47d2c88"`. **Protected; stage it by hand** (section 10). **Caution:** live is built from this `build:` block, so until the runbook's step 2 replaces it with `image:`, any `docker compose build` or `up --build` for live would now build the new engine, and live's first save on it is one-way. Live is not to be rebuilt before the wipe. |
| `docker/uo/SERVER.md:38-39` | build pin `d4531cd94`; live still runs `7c9215d97` (0.15.6.52) until the wipe. The new engine's version number is not recorded (not read). |
| `ShatteredLegacy/AGENTS.md:83`, `README.md:56` | `d4531cd94`, with `7c9215d97` as the before. |
| `shard-migration/AGENTS.md` | layout lines (36 `.patch`, 10 replacements; pin `d4531cd94`); the ModernUO-pinned paragraph (re-checked out, **4,214** `.cs` files, and the rule that a citation before 2026-10-02 is as of `7c9215d97`); "Five customizations are upstream replacements" now names `ResourceInfo` instead of `CraftItem` and says where the other five are; the S3 "3,991 pinned files" marked `at 7c9215d97`. |
| `tools/progress.py` | The bump heading **counts** patches (`server/patches/*.patch`) and replacements (`replace_file` lines). It said "17 patches, 5 replacements" from a hand-kept table that also lists one patch twice. It now prints 36 and 10 and lists all ten replacements, and says the table is a partial risk register. I ran it; README, progress.json, dashboard and expansion coverage refreshed. |
| `tools/README.md:57` | The ServUO exporter's compile claim is "verified against `7c9215d97`, not re-verified against `d4531cd94`". |
| `D:\UO\ModernUO-pinned` | Fetched `d4531cd94` from the local `D:\UO\ModernUO-upstream` (no network) and checked out detached. **HEAD `d4531cd94b739613155225c234900de9f47d2c88`**, clean, **4,214** `.cs` by both `git ls-files` and `find`. To roll back: `git -C D:\UO\ModernUO-pinned checkout --detach 7c9215d97`. |

**`D:\UO\ModernUO-reference`:** a partial clone (promisor) still at `7c9215d97`. **Retire it.**
`D:\UO\ModernUO-upstream` is a full clone with both commits and every one between, so nothing needs the reference
copy. I did not delete it.

Not touched: `entrypoint.sh` (P37 already made it read the ARG); the console captures and old build logs under
`scripts/` that quote `7c9215d97` (historical records); briefs P34 to P36, which name `7c9215d97` and need the hash
changed by whoever runs them after this lands.

## 8. Gates, with counts

| Gate | Result |
|---|---|
| `build.sh -t sl-modernuo:cc-p38`, run 1 | patches 36/36; compile **failed**: 7 errors, P33's two tests (section 3) |
| run 2 | **36/36 patches, 451/451 shard tests, image built** (`build2.log`) |
| upstream Server.Tests on `sl-uo-builder:cc-p38` | **893 passed, 17 skipped, 0 failed** (P30: identical) |
| upstream UOContent.Tests, same builder, shard tests filtered out | **1,095 passed, 91 skipped, 1 failed** (headline 2). P30's 1,504 passed included its 408 shard tests; 1,504 - 408 = 1,096, which is this run's 1,095 passed + 1 failed. The failing test was already in P30's tree; it passed there only because P32's patch did not exist yet. |
| `hook_audit.py` | 0 real mismatches (section 4) |
| patch red proof | 36/36 refused when mutated (section 6) |
| D49 red proof | 449/451, exactly facts 3 and 4 (section 5) |
| shard console suite (PowerShell) | **84/84** (it was 83/84 at HEAD, and 82/84 once the purge files went) |

Skips are upstream's tile-data tests (no client files in the builder), as in P30.

## 9. Load proofs (copies only, `--network none`, no published ports, parent mount, TTY attached)

`D:\UO\cc-p38-work\loadproof.sh` runs the image detached with `-t`, so any console prompt would block and show in
the log. It waits 150 s and then `docker stop`s, which triggers SaveOnShutdown (D36).

| Run | Save | Config | Result |
|---|---|---|---|
| `load-test` | P37 run B's purged save (`D:\UO\cc-p37-work\runB\lib\Saves`, idx **03**) | run B's test config (has `pathfinding.prebakeMaps: "False"`) | banner `d4531cd94b73...`; **207,152 items, 35,199 mobiles, 2.81 s**; listening; no prompt; "saved in 721 ms"; idx **05**; `SerializedTypes.db` gone |
| `load-live` | P30's live copy (`D:\UO\cc-p30-upgrade-work\load\Saves-live-orig`) | a copy of today's live `Configuration` (has the prebake key) | **192,177 items, 34,982 mobiles, 2.38 s**; listening; no prompt; "saved in 558 ms"; idx **05**; no `SerializedTypes.db` |

The live copy is P30's, from before D40. Today's live save stops at D40's prompt on any image (P37), and that world
is retired. Neither run touched a real save.

## 10. What Chase stages and commits

Stage the protected compose file by hand, then run the commit script as usual:

```powershell
cd D:\ShatteredLegacy; git add docker/uo/docker-compose.yml
```

The three new patch files (`CraftItem-shard-hooks.patch`, `CraftContext-shard-hooks.patch`,
`HarvestDefinition-vein-boundary.patch`) are untracked; `Commit-ShardWork.ps1` should pick them up with the rest.
**Before you commit, check that the diff shows the 14 deletions** (10 collision files, the purge command and its
test, `CraftItem.cs`, `CraftContext.cs`).

In `D:\UO\shard-migration`: `AGENTS.md`, `tools/progress.py`, `tools/README.md`, the progress outputs and this note
are mine. `docs/feature-queue.md` (the overseer's 16:20 handoff edit) and `notes/skills-design.md` were already
modified and are not mine.

## 11. P39 checklist for Chase (test shard only; live is not touched)

**Never run `Start-TestShard.ps1` without `-SkipBuild` during P39.** Without it, the script runs `build.sh` with the
default tag and rebuilds `sl-modernuo:latest` from HEAD, which is now the new engine.

The test stack runs whatever `sl-modernuo:latest` is (`docker-compose.test.yml:31`). P39 therefore moves `latest`
twice: first to `cc-p37` for the purge, then to `cc-p38`.

1. **Rollback copies of the current world** (it is idx v3 and loads on `latest`/`246b`):
   ```powershell
   Copy-Item D:\ShatteredLegacy\server\lib\uo\modernuo-test D:\UO\p39-rollback\modernuo-test-before-purge -Recurse
   ```
2. **Put the test shard on the purge image (same engine, `7c9215d97`):**
   ```powershell
   docker tag sl-modernuo:pre-bump-purge-7c9215d97 sl-modernuo:latest
   cd D:\ShatteredLegacy\docker\uo; .\Start-TestShard.ps1 -SkipBuild
   ```
   The image changed, so compose recreates the container. Wait for "Listening" (the script waits for it).
3. **Purge** (in game as Administrator, or `docker attach sl-modernuo-test`, detach with Ctrl-P Ctrl-Q;
   console verbs `purgecollisions dryrun` / `purgecollisions`):
   - `[ClusterFPurgeUpgradeCollisions dryrun`: expect about 107 creatures + 1 item, plus anything spawned since
     (P37 run B: 108).
   - `[ClusterFPurgeUpgradeCollisions`: expect "TOTAL: deleted N, held 27 spawner(s) for 30 min".
   - `[save`
   - `[ClusterFPurgeUpgradeCollisions dryrun` again: expect **"would delete 0"**.
4. **Stop within 30 minutes** (the spawner hold): `docker compose -f D:\ShatteredLegacy\docker\uo\docker-compose.test.yml stop`.
   SaveOnShutdown saves on stop. Then copy the purged save, still idx v3, as the rollback point:
   ```powershell
   Copy-Item D:\ShatteredLegacy\server\lib\uo\modernuo-test D:\UO\p39-rollback\modernuo-test-after-purge -Recurse
   ```
   Check with `Format-Hex D:\ShatteredLegacy\server\lib\uo\modernuo-test\Saves\Mobiles\Mobiles.idx -Count 4`:
   the first byte should be `03`.
5. **Check the test config has the prebake answer**, or the first boot blocks:
   `Select-String prebakeMaps D:\ShatteredLegacy\server\uo\modernuo\Configuration-test\modernuo.json` should show
   `"False"`.
6. **Point the test stack at the new engine and boot:**
   ```powershell
   docker tag sl-modernuo:cc-p38 sl-modernuo:latest
   cd D:\ShatteredLegacy\docker\uo; .\Start-TestShard.ps1 -SkipBuild
   ```
   Expect the banner `Commit: d4531cd94b73...`, **no prompt**, "Loading world done" at about 207k items and 35k
   mobiles, then "Listening". 14 feature-flag JSONs appear in `Configuration-test\FeatureFlags` (P30); that is
   expected. **From the first save on, this world cannot go back to `7c9215d97`.**
7. **Client checks** (from P30's plan; record as T-rows in `docs\client-test-queue.md`):
   - [ ] Craft gump opens normally (not a T2A menu); **Craft X** in both modes (keep going and stop on failure),
         including a failed attempt mid-run
   - [ ] New Haven quest board opens and lists quests
   - [ ] BOD "Combine this deed with contained items" (small and large)
   - [ ] Smith salvage bag (D42 ingot return)
   - [ ] Despise: Wisp Orb possession, the possessed pet is not auto-stabled on logout
   - [ ] Individual stat cap
   - [ ] Young status and its countdown text
   - [ ] A stealable-artifact slot (in particular one at or after slot 80)
   - [ ] A Ter Mur spawn that named a purged type (Slith, StoneSlith, ToxicSlith, Raptor) refills with upstream's
         creatures; Spellbinder spawns in Old Haven's two Trammel spawners
   - [ ] **Starwood chopping**: a GM lumberjack can now get Starwood (about 1 bank in 1,036, so expect to search).
         The logging book records the find.
8. **If anything fails, roll back:**
   ```powershell
   cd D:\ShatteredLegacy\docker\uo; docker compose -f docker-compose.test.yml stop
   Rename-Item D:\ShatteredLegacy\server\lib\uo\modernuo-test modernuo-test.new-engine-aside
   Copy-Item D:\UO\p39-rollback\modernuo-test-after-purge D:\ShatteredLegacy\server\lib\uo\modernuo-test -Recurse
   docker tag sl-modernuo:pre-bump-purge-7c9215d97 sl-modernuo:latest
   .\Start-TestShard.ps1 -SkipBuild
   ```
   Set the new-engine world aside; do not delete it. Then revert the P38 commits in both repos, and
   `git -C D:\UO\ModernUO-pinned checkout --detach 7c9215d97`. Use `pre-bump-7c9215d97` (`246b`) only with the
   **before-purge** copy, because the after-purge save was written by an image that has P33's types.

## 12. `docs\` for the overseer (I did not edit `docs\`)

**The `docs\README.md` line:**

> file:line citations into ModernUO in docs/ and notes/ dated before 2026-10-02 are as of pinned `7c9215d97` unless
> they say otherwise; from cc-P38 the pin is `d4531cd94` (upstream `d4531cd94b739613155225c234900de9f47d2c88`).

**Register.** Method: regex `[\w.]+\.cs:\d+(-\d+)?` over `docs\*.md`. That gives 127 citations, 82 of them to a
basename that exists in P:, and **43 citations into 23 files that changed between P: and U:**. (P30 counted 122 /
66 / 41 with a narrower regex, before P33 and P37 added docs text.) For each one, the line text at P: was looked up
in U:. **None of the 43 cites code that changed:** 35 moved with their text intact, 6 are unchanged at the same line,
1 text now appears twice, and 1 is a false hit (it cites ServUO). Full list with line text in
`D:\UO\cc-p38-work\cite-register.txt` (script `cite.py`).

A decision or a D-number rests on these (re-cite at U:):

| docs line | cites (P:) | at U: | rests on it |
|---|---|---|---|
| bug-list.md:34 | Item.cs:732, :2150; BaseArmor.cs:166; BaseWeapon.cs:199 | :787, :2251; :155; :187 | **D27** |
| bug-list.md:48 | AOS.cs:598; OutgoingMobilePackets.cs:523-542 | :723; unchanged | **D44** (U: line matches P30 section 8) |
| bug-list.md:52 | BaseWeapon.cs:386-388 | :374 | **D48** |
| bug-list.md:156, fidelity-principle.md:121 | MeleeAI.cs:9-10 | :11 | **D-44** (GreenGoblinScout flee) |
| bug-list.md:210 | Main.cs:333-348 | :503 | **D36** (SaveOnShutdown) |
| bug-list.md:285 | MLQuestEntry.cs:520 | :519 | **E3** |
| fidelity-principle.md:104 | MageAI.cs:70 | unchanged | necromancer AI deviation |
| feature-queue.md:298-301 | Account.cs:21; PlayerMobile.cs:4149, :4121 | unchanged; :3798, :3770 | **F-5 Young** (P18's patches; both apply at U:) |
| patch-backlog.md:37, :38, :40, :41, :52 | Repair.cs:169; BaseCreature.cs:106; AnimalTaming.cs:444; LootPack.cs:515-523; MageAI.cs:68-325 | unchanged; :107; :443; unchanged; unchanged | **P10, P11, P13, P14** and the necro AI row |
| gap-register.md:209, :211 | Mobile.cs:6104; PlayerMobile.cs:4139 | :6160; :3788 | gap rows 2 and 4 |
| client-test-queue.md:56, :64 | Stealing.cs:256; SkillCheck.cs:119 | :263; :133 | T-023, T-031 |

Informational only (feature-queue.md, 19 citations): RewardSystem.cs:559-564, :576-594 -> :558, :575;
BaseInstrument.cs:250 -> :249; Mobile.cs:7812 -> :7921; Container.cs:154-159, :88-103 -> :151, :89; Main.cs:267-270
-> :437; BaseWeapon.cs:700-711, :711, :986, :2088-2091 -> :673, :684, :959, :2076; BaseArmor.cs:595-631, :631,
:763-766, :510-522 -> :569, :605, :737, :485; LootPack.cs:722-730 -> :725; BaseRanged.cs:239-281 -> :215;
**BaseRunicTool.cs:705, whose text now occurs at two lines in U:** (one of them is P32's patched line; re-read
before citing). **gap-register.md:234 `BaseWeapon.cs:2320` is a ServUO citation**, matched by basename only: not
a ModernUO reference.

## 13. Decisions and open items

1. **Upstream's `Import_DuplicateLocation_ReplacesExistingSpawner`** (headline 2). Options:
   - (a) A test patch onto that one upstream test, expecting the existing spawner to be kept (our PT-07 behaviour),
     argued like S8's fixture patch. **I recommend this.** It turns the gate's "0 failed" back into a real check,
     and a later upstream change to the importer would stop the build.
   - (b) Record it as a known, expected failure in the gate notes.
   - (c) Drop PT-07. Not recommended: it brings back the loss of 338 stacked spawners.

   Either way, P32's upstream report of the defect now has a sharper form: upstream's own test asserts the
   delete-by-location.
2. **The fixture patch rename** (section 3): optional, `git mv`, plus one `apply_patch` line.
3. **`ModernUO-reference`**: retire (section 7).
4. **Scratch to delete when P39 passes:**
   - `D:\UO\cc-p38-work\`: copies of the test and live saves, with accounts, under `load-*`; plus logs and scripts.
   - `sl-uo-builder:cc-p38-red`: my red-proof builder, about 5 GB. I left it, because deletion was being blocked.
   - P37's and P30's scratch as they listed it, **except `sl-modernuo:cc-p37`/`pre-bump-purge-7c9215d97`**, which
     P39 needs.
5. **Numbering:** no clash. P38 matches the overseer's 16:20 handoff in `docs\feature-queue.md`.

## Files from this task

- `D:\UO\cc-p38-work\`: `build1.log` (P33 compile errors), `build2.log` (green), `build-red.log` (D49 red),
  `groves-detail.log` (share tables), `suite-server.log`, `suite-uocontent.log`, `load-test/`, `load-live/`
  (`run.log` each), `redproof.sh` and `redproof.txt`, `stage.log`, `cite.py` and `cite-register.txt`, `td-head.txt`
  and `td-now.txt` (type deltas), `points-types.txt`, `craft/` (patch sources), `d49/`, `loadproof.sh`,
  `HarvestDefinition-vein-boundary.patch.bak`.
