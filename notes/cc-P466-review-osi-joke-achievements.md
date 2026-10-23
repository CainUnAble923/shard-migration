# P466: OSI joke achievements review

Reviewed 2026-10-23. Notes only. No code changes.

The review found two bugs in death attribution and one risk in temporary tracking. I found no joke progress counter that resets on a normal saved restart, and no ordinary event path that repeatedly awards the same achievement's rewards to one account.

## Findings

1. **F01 | bug | `server/customizations/ClusterFJokeAchievements.cs:283`.** A nonfatal chicken hit followed by a fatal container trap with no attacker can award Fowl Play, because the lookup returns the last credited attacker rather than the source of the fatal hit: damage entries last up to two minutes, and damage with a null source does not replace them (`pinned/Projects/Server/Mobiles/Mobile.cs:59`, `:5806`, `:5981`; `pinned/Projects/UOContent/Items/Containers/TrappableContainer.ExecuteTrap.cs:88`). Track the source of the current fatal damage, reject unattributed deaths, and add a regression that takes a chicken hit before dying to a trap; the guard branch at line 286 uses the same lookup and needs the same protection when guard hits are nonfatal.

2. **F02 | bug | `server/customizations/ClusterFJokeAchievements.cs:264`, `:290`; `server/patches/BaseExplosionPotion-self-blast-achievement.patch:7`.** Surviving your own blast leaves a marker valid for one second, so a subsequent fatal tick from poison you inflicted on yourself can earn Self-Detonation even though the explosion did not kill you (`pinned/Projects/UOContent/Items/Skill Items/Magical/Potions/Poison Potions/BasePoisonPotion.cs:19`; `pinned/Projects/UOContent/Mobiles/PlayerMobile.cs:3743`; `pinned/Projects/UOContent/Misc/Poison.cs:139`). Scope the marker to the explosion's actual damage call and clear it in a `finally` block, then add a negative test for a surviving blast followed by fatal self-poison within the window.

3. **F03 | risk | `server/customizations/ClusterFJokeAchievements.cs:253`, `:259`, `:264`.** The self-blast dictionary removes a player only when that player dies, so a survivor's expired marker retains a strong reference through logout and even character deletion; the timestamp check does not expire entries on its own. Remove the marker after the damage call, or add expiration and deletion cleanup if the timed design stays, and test that nonfatal blasts and character deletion leave no retained entries.

These are issues in our achievement hooks, not defects to copy from ServUO or report against pristine ModernUO. The missing tests above are additional gaps: `server/tests/Misc/JokeAchievementsVerification.cs:366` covers direct fatal hits and self-damage without an earlier blast, but does not cover these mixed damage sequences or tracking cleanup.

## Checks with no additional finding

- **Restart persistence:** `ClusterFJokeAchievements.cs:207` creates stable string counter names, and `:213` updates the account counter store. `ClusterFAchievements.cs:1823` writes every named counter, `:1853` reads them, and `:1679` restores the store, so scissors, worn-tool, and footwear progress have a persistence path. `_selfBlast` is transient damage context, not progress that should survive a restart. A real server restart was not exercised.
- **Repeat awards and abuse:** `ClusterFAchievements.cs:1336` inserts the earned key into an account-wide set before AP, Renown, and loot box work; an already present key returns before those effects. `:1253` orders tiers by threshold, so prerequisites are granted before later tiers. Cheap refusals and deliberate deaths can earn the specified awards once, but I found no ordinary repeat-event or alternate-character bypass of that guard.
- **Accidental earns:** eating while full, bandaging an unhurt player, ghost speech, and the other refusal moments are intentionally easy to trigger during ordinary play. Outside the death attribution findings, I found no new mismatch between a reviewed hook and its stated event.
- **Existing disclosures:** P231 already records self-bandaging, keyword-based Soul Searching, the bandage-only Placebo scope, loot boxes for jokes, omitted tool-wear routes, the untested harvest and second craft-overload hooks, and fishing tested at `SendSuccessTo`. Those are not repeated as new findings. P402 already requests broader shared persistence and account-wide reward regression coverage for the achievement system.

## Scope and evidence

Code HEAD: `4c2af575317a96153369b1dadd19892b549eb7ea`. Notes HEAD before this report: `31711e0618dc51bb7665b87e048b5931f6908f87`.

Read both work copies' `AGENTS.md`, `docs/direction-decision.md`, `docs/tasks.md`, `notes/cc-P231-osi-joke-achievements.md`, and the original completed P231 prompt. No separate P231 review note was present; checked the related P379 merge review and P402 review and its Codex review to avoid repeating their findings.

Reviewed these code inputs, all relative to the code work copy:

- `server/customizations/ClusterFJokeAchievements.cs`, the relevant trigger, definition registration, grant, counter, and persistence paths in `server/customizations/ClusterFAchievements.cs`, and `server/customizations/Meditation.cs`.
- `server/patches/Scissors-running-achievement.patch`.
- `server/patches/Begging-untrustworthy-achievement.patch`.
- `server/patches/Food-too-full-achievement.patch`.
- `server/patches/Bandage-unhurt-patient-achievement.patch`.
- `server/patches/CraftItem-tool-worn-achievement.patch`.
- `server/patches/HarvestSystem-tool-worn-achievement.patch`.
- `server/patches/Beverage-hiccup-achievement.patch`.
- `server/patches/Fishing-shoes-achievement.patch`.
- `server/patches/BaseExplosionPotion-self-blast-achievement.patch`.
- The hook registration and replacement routing in `docker/uo/apply-patches.sh`, P231's changelog entry, and the current `VERSION`.
- `server/tests/Misc/JokeAchievementsVerification.cs` and `server/tests/Misc/AchievementEarnedLineVerification.cs`; searched `server/tests/` for the joke keys, damage markers, and persistence APIs before identifying missing coverage.
- The shared reward guard and downstream achievement box path in `server/customizations/LootBoxes/ClusterFLootBoxes.cs`.

`pinned/` citations mean the read-only `D:\UO\ModernUO-pinned` checkout at `d4531cd94b739613155225c234900de9f47d2c88`, whose working tree was clean. Checked the corresponding hook branches and the damage, player death, trap, and poison implementations there, along with shard patches that could affect those paths. Line numbers refer to the reviewed work copy or pristine pinned source, not P231's older builder tree.

## Validation and limits

This was a source review with no lane tests, as requested. No new tests were added, no existing tests or build were run, and no runtime or client reproduction is claimed. Actual exploit timing, memory cost, and restart behavior remain unverified; the suggested regression cases belong in a later code task.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` set to these work copies; it exited 0. The tool writes `tools/progress.json` even in that mode, so its original bytes were restored immediately to keep this task notes-only.

No Haven connection, deployment, account operation, commit, merge, push, or branch switch was performed. No files under `docs/` were edited.

Final checks: the code working tree is clean, and the only notes-repo change is this report. The report is below 5 MB, contains no em dashes, and whitespace checks passed. No stop request was present at completion.

P466 DONE
