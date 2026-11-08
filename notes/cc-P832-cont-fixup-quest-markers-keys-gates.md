# cc-P832: fix-up for P363 (quest markers, keys and coloured moongates): bring it up to date with main

## In plain words

- **P363's quest markers, keys and coloured moongates now sit cleanly on top of today's main.** These are the gold "!" and "?" over people with a quest for you, the locked top-grade loot boxes and boss doors that need their own key, and the blue, red, black and white moongates. The merge had stopped on eight files. Each now keeps both sides.
- **Top-grade loot boxes keep the newer rarity colours and still come locked.** Main's rarity roll (Common to Legendary) and P363's Vault-key lock now work together on the same box. A boss kill still sometimes drops a Vault key.
- **The art lives side by side.** P363's 72 new pictures (IDs 46592-46663) do not clash with main's mounts, archery butte and Finishers banner (46672-46710). The art list, the records file and the credits list keep both sets.
- **For you:** nothing to decide. Players need the next player package to see the new art.

## State

Iron Golem, 2026-11-08, on `golem/Iron/P832` in both work copies. I did not commit, merge or switch branches.

**How P363 got onto this branch.** The prompt says to check out `golem/Iron/P363` and merge `main` into it. The
Golem's hand-off says to stay on `golem/Iron/P832` and not merge or switch branches. P814 and P820 met the same
conflict; I did what they did. `golem/Iron/P832` starts at main (code `cd7037c`, docs `8e232dde`). I applied P363's
whole change (`git diff --binary origin/main...origin/golem/Iron/P363`, `git apply -3`) to the working tree of both
copies and resolved the conflicts there. The Golem's commit carries P363 and the resolution together. P363's own
commit is not an ancestor of this branch, so merging P832 lands P363.

- Docs copy: P363's notes and `notes/cc-P363-tools/p363_art.py`, applied with no conflict.
- Code copy: 86 files staged (the 72 art PNGs, P363's four new server files and its facts, and the files below).
  `VERSION` and `Cliloc-Overrides.Tests.ps1` show no net change from main: main already has the same version and the
  same fixture growth.

## The conflicts and how I resolved them

| File | Resolution |
|---|---|
| `VERSION` | Main's `2026.11.08`, the higher one (P363 had `2026.10.23.7`). |
| `CHANGELOG.md` | P363's own `2026.10.23.7` section is gone. Its three Added lines are now an `### Added` block under `## 2026.11.08`, and its four Staff lines are added to that section's Staff list. Main's lines are unchanged. |
| `player-package/vendor/shattered-legacy-art/registry.csv` | Both sides' rows: main's 189 (through 46710), then P363's 72 (46592-46663). No ID appears twice; 888 rows in all. |
| `.../records.json` | Both sides' tiledata records; a comma added after main's last. Valid JSON: 379 tiledata, 65 animdata. P363's animdata had merged without a conflict. |
| `.../SOURCE.txt` | Main's sections (UI skins through the Finishers banner), then P363's "Quest markers, gem tokens and quest keys, coloured moongates" section. |
| `player-package/tests/Build-UoOverrides.Tests.ps1` | The records fact's carve-out keeps main's ranges and adds 46592-46663. The ledger gets main's counts plus P363's 72 art: **888** rows (was 816), **745** art rows (was 673); body 74 and gump 68 unchanged. P363's own fact and its bigger fixtures (1,460 groups, 46,720 entries) had merged without a conflict. |
| `server/customizations/LootBoxes/ClusterFLootBoxes.cs` | `MakeBox` keeps main's (cc-P763) rarity roll and season slot. The box is now `ShardKeys.NeedsKey(tier) ? new ShardLockedLootBox(...) { Rarity = r } : new LootBox(...) { Rarity = r }`. `ShardLockedLootBox` derives from `LootBox` and adds no saved fields, so main's version-1 save of `Rarity` covers it. `OnBossKilled` keeps main's grade and trophy name, then P363's `ShardKeys.OnBossKilled(pm, Utility.RandomDouble())`. |
| `server/customizations/ShatteredRunestone.cs` | Both art loaders: main's `ScoringArcheryButteArt.Apply()` and `FinishersBannerArt.Apply()`, then P363's `ShardItemArt.Apply()`. |

**Art IDs checked.** Main has no registry row, PNG or record anywhere in 46592-46663. Its newest art starts at 46672
(P365's mount items). So the two sets do not overlap, and nothing was renumbered.

## Something red that was already red on main

`Build-UoOverrides.Tests.ps1`'s `TheCommunityArtRecordsAreTheServersTableAndEveryRowIdIsRegisteredWithItsPng` failed
with "the layout has 36 rows". It fails the same way on a clean export of main (`git archive origin/main`): 28 of 29.
cc-P678 (`9472de8`) moved the community art into the author's Haven on the SoS map and cut
`ClusterFCommunityArtLayout.cs` to 36 rows on purpose. The fact's floor (`-ge 40`, from P237) was never updated. I
lowered it to 36, with a comment naming P678.

## Tests

**Package facts** (each `player-package\tests\*.Tests.ps1`, run with `powershell -File`):

| File | Result |
|---|---|
| `Build-UoOverrides.Tests.ps1` | **30 of 30** after the fix above (29 of 30 before; main alone: 28 of 29) |
| `Cliloc-Overrides`, `Launch-Overrides`, `Launch-Settings`, `Legion-Scripts`, `Map-Overrides`, `Music-Overrides`, `New-Profile-Defaults`, `No-TazUO-Page`, `Paperdoll-Bodies`, `Prof-Overrides`, `Redrawn-Art`, `Ui-Skins` | all pass |
| `Package-Client.Tests.ps1` | 3 of 9: "the real build above did not produce a zip" |

`Package-Client.Tests.ps1` is not one P363 ran. It runs a real package build, which needs the `package` lock and the
client data. My sweep over the folder started it without the lock. It produced no zip and changed nothing in the work
copy (`git status` shows only the staged change). I did not run it again.

**The gated build.** `docker\uo` build script, tag `sl-modernuo:cc-P832`. I ran it detached under the `docker-build`
lock, with 11 GB free on the PC and 13.6 GB in the Docker VM, then released the lock.

| Run | Result |
|---|---|
| 1 | 3,314 tests, **1 failed**, no image: `CC6Batch8Verification.BaseSABossAwardsAnArtifactToADamagerAndTheDragonDropsItsHead`. The message was `Assert.Contains() Failure ... Not found: typeof(Server.Items.ShardKey)`. |
| 2 | **EXIT=0: 3,314 tests, 3,308 passed, 6 skipped, 0 failed.** Image `sl-modernuo:cc-P832` (`77e40377`) built. |

**The run 1 failure** came from the two sides meeting. The fact kills a Stygian Dragon 60 times, then expects every
item in the killer's pack to be one of the boss's artifacts. Since cc-P763, main's boss kills run through
`ClusterFLootBoxes.OnBossKilled`. P363 added a Vault key to that path, given on 25% of kills
(`ShardKeys.OnBossKilled`), so over 60 kills a key turns up almost every time. The key is meant to be there. The fact
in `server/tests/Mobiles/Bosses/CC6Batch8Verification.cs` now deletes a `ShardKey` from the pack and skips it,
with a comment. Every other item is still checked against the boss's artifact lists.

## Files

- **Code copy, P363's change:** the art PNGs 46592-46663; `QuestMarkers.cs`, `ShardItemArt.cs`, `ShardKeys.cs`,
  `ShardMoongates.cs`; edits to `ClusterFSmithBODSystem.cs` and `EodonGeneration.cs`;
  `server/tests/Misc/QuestMarkersKeysGatesVerification.cs`.
- **Code copy, merged here:** the eight conflict files listed above.
- **Code copy, from this task:** the floor in `Build-UoOverrides.Tests.ps1` and the key skip in
  `CC6Batch8Verification.cs`.
- **Docs copy:** P363's notes and `notes/cc-P363-tools/p363_art.py`, and this file.

P832 DONE
