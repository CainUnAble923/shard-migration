# P401: review of the P282 loop and power scroll ladder

Reviewed October 22, 2026. Notes only. No code changes.

No bug found in the implemented ladder arithmetic. It matches Chase's answer: cap 50 at creation, cap 100 after graduation into loop 1, then +5 per loop through cap 200 at loop 21, requiring 20 scroll steps. The complete player level and scroll system is still planned, so this is a review of the existing hooks and the gaps around them.

P282 itself was numerical research, not a server implementation. P371 supplied the character loop counter, graduation integration, and `MaxLevelFor`; its notes and the wiki draft explicitly describe the remaining work.

## Findings

1. **risk** `server/customizations/ClusterFSkillCaps.cs:185`: The active player policy applies the global default 200 cap even at loops 0 and 1, and its fixed-point conversion at line 154 permits configured caps above 200; `ClusterFLoops.ResetLevelAndSkillsForF12` at `server/customizations/Tutorial/ClusterFLoops.cs:40` remains empty, so the correct ladder helper enforces neither player levels nor skill caps. When implementing F-12, derive each player's training caps from permanent maximum level at creation, graduation, later resets, login, and load, bounded at 200, while preserving the separately approved treatment of bonuses and existing skill values.

2. **risk** `server/customizations/Tutorial/ClusterFLoops.cs:54`: `CompleteLoop` accepts any higher loop number and immediately records and rewards it, without checking the next sequential loop, current level, confirmation, or a matching scroll, so a future caller could record loop 21 directly from loop 0 without consuming the 20 scrolls. Before exposing later loops, add a validated reset transaction that consumes exactly the next target scroll for loops 2 through 21 and applies the reset and cap together, while keeping graduation scroll-free and later cosmetic loops at cap 200; current production callers only request graduation into loop 1, so this is an integration risk rather than a demonstrated player exploit.

3. **risk** `server/tests/Tutorial/GraduationLoopVerification.cs:273`: `LadderMatchesTheDecision` checks the numeric helper, while the graduation case at line 71 verifies that skills stay unchanged, leaving actual creation/graduation cap application and the 20 scroll/reset transactions untested. With the F-12 implementation, add tests for the full 0 through 21 ladder, scroll-free graduation, 20->21 consuming only the 200 scroll, wrong or missing scrolls, skipped steps, cancellation, repeated confirmation, persistence, and a later cosmetic loop retaining cap 200 without a 205 scroll.

These are existing implementation and coverage gaps, already acknowledged in P371, rather than regressions introduced by P282. No additional bug or nit was found in the reviewed ladder code.

## Boundary and scroll checks

`server/customizations/Tutorial/ClusterFLoops.cs:31` returns 50 for nonpositive inputs and otherwise computes `100 + 5 * (Math.Min(loop, 21) - 1)`. Clamping before multiplication prevents both values above 200 and overflow for a large positive loop input.

| Loop input | Helper maximum | Scroll to enter under the design |
| ---: | ---: | --- |
| 0 | 50 | None, creation |
| 1 | 100 | None, graduation |
| 2 | 105 | 105 |
| 20 | 195 | 195 |
| 21 | 200 | 200 |
| 22 | 200 | None, later cosmetic loop |
| int.MaxValue | 200 | No higher cap |

The scroll targets are 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, and 200. That is 20 targets, corresponding to entry into loops 2 through 21, with no scroll for loop 1 and no target 205.

The existing theory includes loop inputs 0, 1, 2, 20, 21, and int.MaxValue. It already covers both requested endpoints and a large input; the test gap is principally actual progression behavior, not a missing assertion that loop 21 maps to 200.

Source tracing confirms that `MaxLevelFor` has no production callers in customizations or patches. `ClusterFTutorial.cs:76`, `:176`, and `:232` call `Graduate`, which requests loop 1; the existing `TutorialVerification.cs:216` calls `CompleteLoop` with loop 2 directly to check Young status, without a scroll.

There is no working loop-scroll conversion at `server/customizations/LootBoxes/ClusterFLootBoxes.cs:238`: combining fragments only displays a message. Pinned ModernUO `Projects/UOContent/Items/Special/Special Scrolls/PowerScroll.cs:252` compares the named skill's cap with the scroll value, and line 272 writes that skill's cap, not a character maximum or loop count. Under the default 200 skill cap, stock 105 through 120 scrolls are refused; they do not implement entry into loop 2. No customization or patch replacing that behavior was found.

The active skill policy's values above 200 are a separate issue from the safe ladder formula. `server/tests/Misc/TwoHundredCapVerification.cs:98` deliberately preserves a manual 300 setting after the one-time rescale marker, and line 104 preserves a manually configured 250; this is existing override policy. Its line 135 case deliberately retains previously earned skill above 200, and `ClusterFSkillBonusAboveCap.cs:29` admits item and temporary bonuses above the training cap; neither is an off-by-one error in loop progression.

## Evidence and validation

Read both work-copy AGENTS.md files, the direction decision, and task list. Required prior reading:

- `notes/cc-P282-f12-numbers-and-level-gates.md`
- `notes/cc-P282-f12-numbers-and-level-gates-codex-review.md`
- `notes/cc-P371-graduation-is-the-first-loop.md`
- `notes/cc-P371-graduation-is-the-first-loop-codex-review.md`
- `notes/wiki-drafts/levels-loops-and-scrolls.md`
- Relevant ladder and scroll sections of `notes/f12-levels-loops-caps.md`.

Primary code and test files read for these findings:

- `server/customizations/Tutorial/ClusterFLoops.cs`
- `server/customizations/Tutorial/ClusterFTutorial.cs`
- `server/customizations/ClusterFSkillCaps.cs`
- `server/customizations/ClusterFSkillBonusAboveCap.cs`
- `server/customizations/LootBoxes/ClusterFLootBoxes.cs`
- `server/tests/Tutorial/GraduationLoopVerification.cs`
- `server/tests/Misc/TutorialVerification.cs`
- `server/tests/Misc/TwoHundredCapVerification.cs`
- Read-only pinned ModernUO `Projects/UOContent/Items/Special/Special Scrolls/PowerScroll.cs`, at verified commit `d4531cd94b739613155225c234900de9f47d2c88`.

Searched canonical customizations, patches, and tests for ladder callers and scroll integration. Did not read the generated `server/uo` tree. The prior P371 review's travel findings are outside this cap/scroll review and are not repeated here.

Re-ran the existing numerical checks with `python -B notes/cc-P282-scratch/verify_curve.py`: all 10 passed. These are research checks, not server behavior tests. No tests were added or changed, and no lane tests or server build were run, as requested. Runtime graduation, actual cap enforcement, scroll/reset atomicity, live settings, and client behavior remain unverified.

Windows PowerShell was version 5.1.26100.9444. Required `tools/progress.py --dry-run` completed with both path overrides pointing to these work copies; its incidental `tools/progress.json` write was restored byte-for-byte to keep this review limited to the requested notes. No Haven connection, deployment, account operation, commit, merge, push, branch switch, or `docs/` edit occurred.

Final checks: both repositories passed git diff --check. The code work copy is clean; the only docs-work-copy change is this notes file, below 5 MB and without em dashes.

P401 DONE
