# P582: Review of Noted by the System fix-up 2 (P457)

Reviewed 2026-10-24. Notes only. No code changes.

## Scope

P457 commit `9779110da81f23309b0518d79e2309002d3dbb0d` is in local `main`, merged by `bca6999`. Reviewed code work-copy HEAD `608d0b4` and notes work-copy HEAD `b997ee6`. Pinned ModernUO is `d4531cd94b739613155225c234900de9f47d2c88`.

Read both work copies' AGENTS.md, the direction decision and task list, `notes/cc-P457-noted-fixups-2.md`, its Codex review, and the P402 review and its Codex review. The existing P457 review already reports the missing loot exception. That finding is not repeated here.

Inspected these P457 implementation and test files, with their calling paths:

- `server/customizations/ClusterFNotedBySystem.cs`
- `server/customizations/ClusterFAchievements.cs` (changed registration and trigger cache paths)
- `server/patches/BaseCreature-noted-damage-memory.patch`
- `server/patches/PlayerMobile-noted-step.patch`
- `server/patches/CraftItem-fail-streak-achievement.patch`
- `server/patches/Mining.cs`
- `docker/uo/apply-patches.sh` (affected patch registrations)
- `server/tests/Misc/NotedFixupsVerification.cs`
- `server/tests/Misc/NotedBySystemVerification.cs`
- `server/tests/Mobiles/Bosses/CC6Batch8Verification.cs` (changed random-generator scope)

Also checked the resmelt and salvage hook patches, `SmithGuildSalvageBag.cs`, craft-run reject routing, and pinned movement, damage registration, and craft completion code. Code citations below are relative to the code work copy. Upstream citations are relative to `D:/UO/ModernUO-pinned`.

## Findings

1. **bug | `server/customizations/ClusterFNotedBySystem.cs:907`, `:952`: World-item floors still let the terrain underneath count.** The dynamic-item loop only recognizes fire fields; ordinary immovable surface items never participate in floor selection. For example, a world `Static` using the tested floor graphic `0x0491` at Z 20 over snow land at Z 0 returns Snow for feet at Z 20 when there are no map statics, although pinned movement accepts that item as the walking surface (`Projects/UOContent/Engines/Pathing/Movement.cs:365`, `:384`, `:395`, `:430`). Include qualifying world-item surfaces when selecting the supporting floor, and add a regression using a placed immovable floor item over snow rather than only the map-static seam at `NotedFixupsVerification.cs:270`.

2. **bug | `server/customizations/ClusterFNotedBySystem.cs:927`, `:952`: A buried static floor can hide the land actually walked on.** Every passable static surface below the feet is eligible, and any selected surface wins over land without comparing land elevation. Thus snow land at Z 20 with an ordinary floor static at Z 0 classifies as Other for a player walking at Z 20; pinned movement compares land and surface heights and can select the snow land (`Projects/UOContent/Engines/Pathing/Movement.cs:261`, `:353`, `:437`, `:461`). Compare candidate surfaces with the land's walking height before selecting the support, and cover a floor below elevated snow as well as the existing floor above snow case.

3. **risk | `server/tests/Misc/NotedBySystemVerification.cs:511`: The old-item recycling negative no longer tests the age limit.** The old crafted gorget has no recorded crafter, so P457's new `IsCraftedBy` guard rejects it before either age check runs; deleting the FreshRecycleWindow condition would leave this assertion green. Record its crafter before recycling, then add exceptional own-craft cases just outside the ten-second and one-minute windows so each time limit is independently exercised.

## Checks with no additional finding

- No additional path was found that credits recycling another player's craft. The new success hooks pass the produced item, and the eligibility check requires the recycler to be its recorded crafter. The gift negative in `NotedFixupsVerification.cs:394` exercises that identity check.
- No additional issue was found in the bard's healed-to-full exclusion, the empty-at-A/ore-at-B mining reset, the visible owner's 14/15/16-tile boundary, or the follower map and dead-pet exclusions.
- The new counted-tier test uses explicit expected thresholds and checks AP at the threshold and after a repeated event. Previously reported broader integration and persistence gaps are not repeated as new findings.

## Validation and limits

These findings are source traces, not client or running-shard reproductions. The terrain examples describe deterministic classifier inputs and the corresponding upstream movement rules; their occurrence in the current world is unverified. No lane tests were requested, and no tests were added or run. P457's reported green build was not independently rerun.

Ran `tools/progress.py --dry-run` with both work-copy path overrides, exit 0. Its generated `tools/progress.json` was restored byte for byte so the deliverable stays notes-only. No Haven connection, Docker operation, deployment, account operation, code edit, edit under `docs/`, commit, merge, push, or branch switch was performed.

Final checks: the code working tree is clean, and this report is the only notes-repo change. The report is below 5 MB and contains no em dashes. No stop request was present at the finishing checkpoint.

P582 DONE
