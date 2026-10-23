# P495: Review of usable ankhs and the P137 play-test fixes

Reviewed 2026-10-23. Notes only. No code changes.

P137 is in local `main`: code commit `c0a1d9adaa83f17f816a60f7cd7274ccb34ba421` is an ancestor of `main`. Reviewed code HEAD `579ad58f8f478280b03b8cf80f1ee9a5b3001a27` and notes/tools HEAD `f1c6c3ca1a73aefbe8185e7d8e5c624b4560f9be`. The reviewed files match local `main`; no remote fetch was needed.

Read `notes/cc-P137-usable-ankhs-and-playtest-fixes.md` first. No separate P137 review was found beside it. The findings below do not repeat its reported defects.

## Findings

1. **bug** | Code `docker/test-queue/server.py:624`, `:629`, `:633`; notes repo `tools/codereload.py:99`, `:143`: A failed reload can leave earlier modules and the failing module partly updated, then reopen the request gate and return success to the watcher, which stops retrying that fingerprint while the log claims the old code is running. Replace in-place failure recovery with a controlled process restart after a reload error, and add coverage for a later module failing after an earlier one changed and for a module raising after changing its globals.

2. **bug** | `server/customizations/ClusterFAnkhs.cs:43`: `IsWorkingAnkh` counts rejuvenation ankhs and `DespiseAnkh` as resurrection sources, but the former replenish living players' resources and the latter issue WispOrbs, so the survey can falsely promise resurrection and the seeder can skip a placement beside an item that cannot resurrect anyone. Restrict this predicate to actual resurrection sources and classify the other interactive ankhs separately, with regression coverage for both kinds.

3. **bug** | `server/customizations/ClusterFAnkhs.cs:233`: `Sightings` excludes working ankh items, so an ordinary working ankh placed on a tile without matching map-static art disappears from the survey entirely, including standalone seeded ankhs. Include working item heads and deduplicate matching static/item sightings by map and location, with a test that calls `Sightings` for a standalone ankh rather than supplying its sighting by hand.

4. **risk** | Pinned ModernUO `Projects/UOContent/Items/Construction/Ankhs.cs:43` and `Projects/UOContent/Gumps/ResurrectGump.cs:193`: The shrine offer retains the ghost as its healer instead of the ankh, and confirmation checks the current tile's fit without retaining or rechecking the shrine's range or map, allowing an offer to be carried away before acceptance according to the source path. Reproduce this with an actual accepted offer, then consider an ankh-specific confirmation that retains the shrine and rechecks the player's death state, the shrine's existence, map, and range; this is inherited upstream behavior, not a P137 regression.

5. **risk** | `server/tests/Misc/AnkhVerification.cs:190`, `:222`: The ghost test passes on a refusal message or an open gump without accepting resurrection, and the living-player test only exercises tithing, leaving successful resurrection, its fame penalty, and attempted resurrection while alive untested. Add a standable test surface and exercise acceptance, cancellation, region refusal, and the living player's resurrection action, asserting the alive transition and a positive fame value's expected 10 percent loss only on successful resurrection.

6. **bug** | Pinned ModernUO `Projects/UOContent/Items/Construction/Ankhs.cs:22`: The resurrection context entry uses `from.Alive` as its enabled flag, so a ghost receives a disabled Resurrect entry and the actual context-menu response handler refuses its click, although walking up or double-clicking still uses a separate path. Correct the flag to `!from.Alive` through the shard's patch layer and test the ghost and living entries' enabled states plus the real response handler; this is an inherited upstream defect exposed by the new placements, not a P137 regression.

## Evidence and limits

- Finding 1 was reproduced without a service or network connection. An in-memory loader supplied two modules to the real `codereload.reload_modules`, and an AST extraction executed the current server's actual `reload_tools` function with its real gate. The first module changed `VALUE` from 1 to 2; the second also changed its value and then raised a controlled exception. Observed output:

  ```text
  new tools code NOT loaded, still running the old: P495 controlled reload failure
  reload_tools returned: True
  module values after rejected reload: 2 2
  gate reopened: yes
  ```

- For finding 2, pinned `Items/Addons/RejuvinationAnkhs.cs:13` restores hits, mana, or stamina on living double-click; its movement handler at `:62` only sends a peace message. Our `Items/Functional/DespiseAnkh.cs:43` only issues an aligned WispOrb. Pinned `Items/Addons/AddonComponent.cs:145` delegates living double-click to the addon, and `Projects/Server/Items/Item.cs:4462` refuses dead double-click by default. Neither addon implements resurrection. These classifications were verified from source, not in a client.
- Finding 3 follows the actual `Sightings` enumeration, not just the classifier: map statics are enumerated first, then working item types are explicitly filtered out. Existing `TheSurveyReadsStaticsAndSaysWhichAnkhsWork` supplies sightings directly and therefore does not exercise that omission.
- Finding 4 is source-verified but unverified in a running shard or client. `Projects/Server/Mobiles/Mobile.cs:4568` still enforces `Region.OnResurrect`, so this is a missing shrine-proximity check, not evidence that region resurrection bans are bypassed.
- For finding 6, `Ankhs.cs:57` assigns the supplied flag directly to `Enabled`, and `Projects/UOContent/Context Menus/ContextMenuSystem.cs:95` requires `e.Enabled` before invoking the entry. P137's living-menu test checks entry numbers and directly invokes the tithing entry, so it does not catch the ghost's disabled resurrection action. This was verified from source, not a client.
- No new penalty bypass or unintended living-player resurrection benefit was found in P137's normal `AnkhWest`/`AnkhNorth` path. Pinned `Ankhs.cs:32` rejects a living mobile, and `ResurrectGump.cs:261` applies the positive-fame loss. Murderer stat loss is deliberately disabled for this shard's AOS-or-later era by `ResurrectGump.cs:31`; its absence is not a P137 defect. Tithing and the separate rejuvenation ankhs' resource benefit are existing behavior.
- No additional finding was established in the reviewed non-magic disenchant guards, essence delivery, backpack routing, fight watcher, or play-test sorting changes. This is a source review, not a claim that those systems passed a fresh full shard build.

## Files inspected

Code paths named by P137 were reviewed through their P137 diffs and current implementations: `ClusterFAnkhs.cs`, `ArtificersImbueGump.cs`, `ArtificersSatchel.cs`, `ClusterFBackpack.cs`, `docker/test-queue/server.py`, and `tools/playtest-bot/uobot/checks.py`; tests were `server/tests/Misc/AnkhVerification.cs`, `server/tests/Misc/UnravelSatchelVerification.cs`, and `tools/playtest-bot/tests/test_bot.py`. `CHANGELOG.md` and `VERSION` were checked in the P137 diff.

In the notes repo, reviewed P137's changes to `tools/codereload.py`, `tools/playwho.py`, `tools/progress.py`, `tools/tests/test_codereload.py`, `tools/tests/test_play_who.py`, and `tools/tests/test_self_judging.py`, along with the original notes' explanation of its triage and steps changes. Followed the resurrection path in read-only `D:\UO\ModernUO-pinned`, verified at `d4531cd94b739613155225c234900de9f47d2c88`, and the custom Despise addon. Did not read the generated `server/uo` tree.

## Validation

- Existing `python -B -m unittest tests.test_bot.P119FightWatch` passed its three named tests in `tools/playtest-bot/tests/test_bot.py`: top-up and kill detection, dead-fighter reporting, and timeout.
- Existing `tools/tests/test_codereload.py` ran nine tests: the two `GateFacts` tests and the `NestedWork` test passed; the three `WatcherFacts` and three `TheService` tests errored in setup because newly created temporary directories denied child-file access. Retrying with TEMP and TMP under the writable work copy produced the same permission errors. No service test reached startup, and these environmental errors are not reported as product bugs.
- The in-memory reload probe above reproduced finding 1 independently of that temporary-directory failure. No new test files were added and no implementation was changed.
- All shell commands ran in Windows PowerShell 5.1 (`5.1.26100.9711`). No shard build or C# tests were run for this notes-only review. No Haven connection, deployment, commit, merge, push, or branch switch was made.
- `tools/progress.py --dry-run` completed with exit code 0, using SL_SHARD and SL_MIGRATE for these work copies. Despite dry-run, its build step rewrote `tools/progress.json`; that incidental change was inspected and restored byte-for-byte from HEAD to preserve the prompt's single-notes-file scope.
- Test scratch was kept under `tools/playtest-bot/cache/p495`, proven ignored with `git check-ignore`. Automatic approval review rejected recursive cleanup as blocked by policy; the inaccessible temporary directories remain ignored. The temporary tests failed before copying tools or writing their module files. No large output file was created.

P495 DONE
