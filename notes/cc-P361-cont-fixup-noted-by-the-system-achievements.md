# CC task P361: fix-up for P263 (the "Noted by the System" achievements), merged with main

## Headlines

- P263 now merges cleanly with main. Main, at `48191cd`, includes P262 (accessory slots), P261 (levelable gear) and
  P243 (Hall decor). Six files had conflicts. Both sides are kept everywhere.
- `docker/uo/build.sh -t sl-modernuo:cc-P361` is green: **2,034 tests, 2,030 passed, 0 failed, 4 skipped**. "Built
  sl-modernuo:cc-P361 with patches applied and 2030 shard test(s) passing."
- One test needed a fix after the merge: P263's count of `noted.*` achievements goes from 45 to 50. P262's five
  accessory achievements use the same `noted.` key prefix and the same hidden Mischief category.
- P262 and P263 had each added a flag to `TitleDef` that hides a title until it is held. They are now one flag,
  `HiddenUntilHeld` (P262's name).

## How the merge was done

The hand-off keeps me on `golem/Copper/P361`, which was at `origin/main` (`48191cd`), and does not let me switch
branches. So I ran `git merge --no-commit --no-ff golem/Copper/P263` into P361 in both work copies. That gives the same
tree as merging main into P263. The merge is staged but not committed; the Golem commits it.

- shard-migration: no conflicts (it only adds `notes/cc-P263-noted-by-the-system-achievements.md`).
- ShatteredLegacy: six files had conflicts, resolved as below.

## Conflicts resolved

| File | Resolution |
|---|---|
| `VERSION` | Took the higher version: `2026.10.21.14` (main). P263 had `.12`. |
| `CHANGELOG.md` | Both sides used `## 2026.10.21.12` for different content. Main's `.14`, `.13` and `.12` (levelable gear) stay as they are. P263's Added, Changed and Staff lines move under `## 2026.10.21.14`, after the Hall decor lines. |
| `docker/uo/apply-patches.sh` | Both blocks kept: main's P262 and P261 patches first, then P263's eight patches. They touch different stock files (AOS and PlayerMobile against Recall, Moongate, Runebook, PetOrders, CraftItem, Resmelt, SalvageBag and SmallBOD). The build applied them all. |
| `server/customizations/ClusterFAchievements.cs` | Union in three places: the `TriggerKind` enum (P262's four members first, then P263's), the earned-line switch, and `RegisterAccessories(); RegisterNoted();`. Main's enum members come first, so they keep their numbers. |
| `server/customizations/LeagueShop/LeagueShop.cs` | P262 added `TitleDef(..., bool HiddenUntilHeld)` and P263 added the same field as `Secret`. Kept `HiddenUntilHeld`. P263's three titles (Larry, the Supervisor, the Brave (citation needed)) now pass `HiddenUntilHeld: true`, after the Unshod title. |
| `server/customizations/LeagueShop/LeagueShopGumps.cs` | Merged without a conflict, but it would not have compiled: it used both `t.Secret` and `t.HiddenUntilHeld`. P263's count of listed titles, which sizes the gump, now uses `HiddenUntilHeld`. P263's skip, which repeated P262's, is removed. |
| `server/tests/Misc/AchievementEarnedLineVerification.cs` | Both counts are now 145 (95 + 5 from P262 + 45 from P263), as P263's notes predicted. |

Fixed after the first build (red, 1 failure):
`server/tests/Misc/NotedBySystemVerification.cs`, in `DataOnlyAchievementsAreHiddenAndNotedTitlesAreSecretUntilHeld`,
now expects 50 `noted.*` achievements, not 45. The rest of that fact passes with P262's five included: every one is
hidden, in Mischief, with a flavor line and a unique title.

## For Chase

- P262's Plate Bottoms Only and Iron Soles count tiles run barefoot in armor. P263's Hot Foot and Snow count tiles
  walked barefoot in armor on lava, fire or snow. They are separate achievements with separate counters, so one step
  on snow can count toward both. I left that as it is.

P361 DONE
