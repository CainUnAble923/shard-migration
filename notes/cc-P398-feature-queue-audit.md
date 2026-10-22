# P398: feature queue audit

Date: 2026-10-22. Docs-only review in the Valorite work copies.

Read both working agreements, the direction decision, task list, document index,
feature queue, and the referenced prompt notes. Checked canonical customizations,
patches, tests, client patches, and player-package sources. Did not read the stale
server build tree. The pinned ModernUO checkout is at
`d4531cd94b739613155225c234900de9f47d2c88`.

Starting code HEAD: `b240bb4d6e47d72ab6be6aafc202b6b28833a7c1`.
Starting notes HEAD: `e3d2a0a060e36215a2c20a19d891ae30c023f806`.

Deliverable: `notes/feature-queue-audit-2026-10-22.md`. It covers every F-number,
including the dropped F-2, distinguishes the queue's wording from source status,
lists additional built features, and ends with Sources and Contradictions.

The audit content is written. Each of the 51 F-number entries appears once, with
the queue's status and line reference, source status, missing scope, file:line
evidence, and known building prompts. The same file lists additional implemented
features and ends with Sources and unresolved Contradictions. The row table is the
file list supporting this entry count.

Main findings: pending queue labels outlast builds of the shop, client fog,
community/winter art, Events, climbing boots, Rootdeep, and requisitions. Player
progression, the League contract engine, tutorial lessons, crafting bank access,
and some mule effects remain partial. The veteran stat-cap reward, wider BOD
training rules, rolled gathering contracts, dismount sources, inn rooms, epic
crafting, and Herbalism are not implemented as the queue describes. The audit
distinguishes existing foundations from those missing features.

Validation completed:

- Matched the complete F-1 through F-51 row set, including dropped F-2, against the
  queue; no missing or duplicate IDs.
- Checked that cited source files exist and line references are within bounds;
  checked every queue-entry line reference. Corrected the climbing test path.
- Checked table column widths, trailing whitespace, and ASCII punctuation. The
  final section is Contradictions. Both deliverables are well below 5 MB.
- Reviewed source behavior to correct an initial overstatement about High Seas
  profession quests. Those remain planned. Also recorded the missing veteran
  stat-cap override rather than treating the completed shop as the whole of F-13.
- Both repositories pass `git diff --check`. The code work copy is unchanged.

Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE pointing at these
work copies; exit 0. Its counts were not used to infer feature behavior. Found an
existing reporter defect: despite the advertised print-only option, it writes
`tools/progress.json` from the render path at `tools/progress.py:722`, before the
dry-run return at line 737. Restored that generated file byte-for-byte from HEAD.
No reporter fix was made because P398 is notes-only. This is ours to fix in a
separate task; the source order and observed generated diff prove the finding.

No code or docs directory changes remain. No tests were added or run. No build,
live inspection, Haven connection, deployment, account operation, commit, merge,
push, or branch switch.

## Pause and resume

The Golem stop-request file appeared during final validation. Its reason is that
the Codex five-hour usage window reached the configured hard stop. Earlier
between-step checks were clear. Finished the validation step and restored the
unintended generated progress file, then stopped.

Resumed on 2026-10-22 after the Golem cleared the stop request. Both repository
HEADs still match the audited snapshots. Rechecked feature coverage, queue line
references, source-file references, table shape, punctuation, whitespace, file
sizes, and final Sources/Contradictions section order. All checks pass. Both
repositories pass `git diff --check`; the only pending files are the two requested
notes files. The code work copy remains clean. The stop request remains absent.

Final handoff review is complete. No implementation, lane tests, or other required
work remains.

P398 DONE
