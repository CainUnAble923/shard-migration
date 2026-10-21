# CC task P272: fix-up for P158 (Codex as a second agent): its branch did not merge into main

Iron, 2026-10-21.

## Headlines

- P158 now merges with main. Three conflicts in ShatteredLegacy are resolved: `CHANGELOG.md`, `VERSION` and
  `scripts/tests/Shard-Console.Tests.ps1`. Both sides are kept in all three.
- shard-migration merged on its own, with no conflicts.
- Nothing is red that is not red on main: the console tests fail the same 13 facts as main, and P158's own fact
  passes. Nothing under `server\` or `docker\uo\` changed, so there was no Docker build.
- Not committed. The merge is staged in both work copies for the Golem to commit.

## How it was merged

The hand-off put both work copies on `golem/Iron/P272` and said not to switch branches. `golem/Iron/P272` was exactly
`main` (`e1c8232` in ShatteredLegacy, `c614500` in shard-migration). So instead of checking out P158 and merging main
into it, I ran `git merge --no-commit --no-ff golem/Iron/P158` on P272. The result is the same tree, and P158 and main
are both its parents.

## Conflicts resolved (ShatteredLegacy)

| File | Main's side | P158's side | Resolution |
|---|---|---|---|
| `VERSION` | `2026.10.21.2` | `2026.10.20.19` | The higher one: `2026.10.21.2` |
| `CHANGELOG.md` | new headings `2026.10.21.2` (P177's guild menu Staff line) and `2026.10.21` (P228) | heading `2026.10.20.19`, one Staff line (Codex reviews and the Codex lane) | P158's Staff line moves under `## 2026.10.21.2` / `### Staff`, after P177's. Its old heading is dropped |
| `scripts/tests/Shard-Console.Tests.ps1` | `P222_TheTinkersButtonsRunTinkerPs1AfterTheirPhraseAndNothingElse` | `P158_TheCodexTodayRowSaysTheReviewsAndTheLaneRuns` | Both facts, P222 first, each closed with its own `}` |

`scripts/Shard-Console.ps1`, `AGENTS.md` and `scripts/tests/test_agents_md.py` merged without a conflict. So did
shard-migration's `AGENTS.md`, `tools/tests/test_agents_md.py` and P158's two notes files.

## Tests

| Suite | Result |
|---|---|
| `scripts/tests/Shard-Console.Tests.ps1` (merged tree) | 438 facts, 425 passed, 13 failed. P158 and P222 both pass |
| the same suite on main (an export of `main`, run from a short path) | 437 facts, 424 passed, 13 failed: **the same 13 facts** |
| code repo `scripts/tests` (Python) | 55 OK |
| docs repo `tools/tests` (Python) | 172 run, 3 failed: `test_mapops` shipped patch and the two `test_play_who` real-file facts, the same 3 P158's notes say fail on a clean HEAD |

The 13 console failures on both trees are: PlayerCommandsNeverAppearInTheWorldTab,
RedMeansTestOnlyUnclassifiedOrAPlainRunThatDeletesAndNothingElse, the three EveryWindowAction / WithTheToggleOn facts,
the two P83 link facts, the two P101 facts, P107, and the three P135 facts.

P158's tests in `D:\UO\golem` (`Codex.Tests.ps1`, `Golem.Tests.ps1`) were not rerun. That repo is not in this merge,
and none of its files changed here.

The main baseline first failed with "path too long" from the scratchpad, because the console's file hashing passes the
260-character limit. I ran it from `D:\UO\golems\Iron\p272m` instead, then deleted that folder.

P272 DONE
