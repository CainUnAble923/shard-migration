# P596: round 3 questions work record

October 25, 2026. Notes only. The question list is [cc-P596-questions-for-chase-3.md](cc-P596-questions-for-chase-3.md), the task-body filename. This record uses the separate Notes path supplied by the unattended wrapper.

## Work completed

Read AGENTS.md in both work copies first, then the governing-document index, direction decision, task list, and standing question answers. Both work copies started clean. Code HEAD: `8b0ccb80c00aedd9898be6f453d419b0a2119f2c`. Notes HEAD: `a749dc112f668c7a712a63afd7fcb9e85425cbd9`.

Compared the P532 and P574 question tables and P574 reconciliation with the newer material. The new list separates four repair policy choices, R01-R04, from six nonblocking Chapter 2 editing choices, S01-S06. Each row supplies source lines, options, a recommendation, and its consequence. Defaults remain proposals. No question is being sent to Chase during this unattended collection.

P586 C1 maps to R01. C2 maps to R02/R04, with A1's mixed-bonus valuation issue isolated as R03. P593 questions 1-6 map in order to S01-S06. Guide caveats, known defects, missing test coverage, factual copy corrections, and operator handoffs are reconciled outside the question tables. No earlier question table was rewritten.

Read the current P452 brief instead of relying on P579's historical empty-file observation. It remains populated in waiting and requests an attended run or investigation of repeated unattended read denials. The list records that operator dependency separately from its policy choices. No denied file was read and no workaround was attempted.

Distinguished the two P587 notes by filename and subject. P584's review is now available, despite being absent at P586's snapshot; its findings add repair work rather than a new design vote. Existing accepted choices from the overseer decision logs and F-24 were excluded from the new voting list.

## Source inventory

Paths in this list are relative to the migration work copy unless an absolute path is given. Read relevant sections in context; screening guide headings or question words alone did not establish a new decision.

- Baselines: `notes/cc-P532-open-questions-for-chase.md`, answer-check context in `notes/cc-P532-open-questions-sweep.md`, `notes/cc-P574-questions-for-chase-2.md`, `notes/cc-P574-questions-for-chase-round-2.md`, and `notes/cc-P574-questions-for-chase-round-2-codex-review.md`.
- Fix synthesis: `notes/cc-P586-codex-findings-to-fixes-6.md`, `notes/cc-P586-codex-findings-to-fix-drafts-6.md`, and `notes/cc-P586-codex-findings-to-fix-drafts-6-codex-review.md`.
- Appraiser context: `notes/cc-P579-design-requisitions-appraiser-numbers.md` and read-only `D:/UO/cc-prompts/waiting/cc-P452-fix-requisitions-fix-up-appraiser-magic-test.md`.
- Reviews and merge context: `notes/cc-P584-review-guild-hall-seeder.md`, `notes/cc-P587-review-hammer-t3.md`, `notes/cc-P587-review-hammer-t3-codex-review.md`, and `notes/cc-P587-cont-fixup-high-seas-fishing-second-half.md`.
- Tutorial: `notes/cc-P588-tutorial-text-pass.md`, especially its scope and source-findings sections, plus `notes/wiki-drafts/new-player-tutorial.md`.
- Rootdeep: `notes/cc-P589-guide-rootdeep.md` and `notes/wiki-drafts/rootdeep.md`.
- Halloween: `notes/cc-P590-guide-sorcerers-dungeon-event.md`, `notes/cc-P590-guide-sorcerers-dungeon.md`, and `notes/wiki-drafts/sorcerers-dungeon.md`.
- Eodon: `notes/cc-P591-guide-eodon.md` and `notes/wiki-drafts/eodon.md`.
- Achievements: `notes/cc-P592-guide-achievements-refresh.md` and `notes/wiki-drafts/achievements-and-loot-boxes.md`, including its contradiction/resolution section.
- Story: `notes/cc-P593-league-chapter-2-draft.md`, its reward/retry context and closing questions; `notes/cc-P593-league-story-chapter-2-draft.md`; and `notes/cc-P593-league-story-chapter-2-draft-codex-review.md`.
- Answer context: `notes/codex-questions.md`, relevant `docs/league-storyline.md` and `docs/feature-queue.md` passages, and read-only `D:/UO/overseer/decisions-2026-10-22.md` and `D:/UO/overseer/decisions-2026-10-23.md`, including the later continuation.

## Scope and verification limits

No code, tests, prompts, guides, configuration, or files under docs/ were changed. No Haven connection, build, deployment, shard or account action, commit, merge, push, or branch switch occurred. No art was made or requested. Lane tests are none; no new test or gate requires a red/green cycle.

Shell commands run under Windows PowerShell 5.1. Ripgrep is unavailable; local searches used PowerShell, Git, and Python. This is a notes reconciliation, not independent verification of the cited reports' technical or runtime claims. Actual access-denial resolution, retained saves, economy balance, map placement, client behavior, release state, and story implementation remain unverified.

## Verification results

Ran the required `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE set to these work copies. It completed successfully and produced 234 output lines. Its known unconditional write to tools/progress.json was suppressed for that exact path in memory, without editing the tool or changing any generated file. The JSON remained byte-identical, SHA-256 `21bbb59516e610cfcbb391b36415c62d6dd1680d9cf4c551f50d977e3e545acc`. General progress figures are not evidence for this questions task.

Editorial checks confirmed ten unique complete question rows: R01, R02, R03, R04, S01, S02, S03, S04, S05, and S06. Relative Markdown links resolve, and every numeric source reference points to a nonblank line in its source. Both deliverables are ASCII, contain no em dashes or trailing whitespace, have final newlines, and are below 5 MB. Repository whitespace checks pass; the final inspection also covers these untracked files directly. No lane tests apply, and none were added or run.

Final scope check: both recorded HEADs and all tracked files are unchanged. The code work copy is clean; the only notes-repo changes are the two requested P596 Markdown files. Stop-request checks were clear between steps and at the final checkpoint. Collection and verification are complete; no P596 work remains.

P596 DONE
