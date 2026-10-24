# P527 run notes: companions and evo pets

The requested design comparison is [cc-P527-companions-design-vs-build.md](cc-P527-companions-design-vs-build.md). It contains the per-item built status, source locations, remaining gaps and sizes, exact evo stage availability, recommended answers to design questions, existing review defects, and suggested implementation order.

Both requested filenames are supplied: this file follows the lane handoff's notes path; the linked report follows the embedded task's output path.

Read both work-copy AGENTS.md files and the direction, task, companion design/review, P41/P45 research, P369/P264 implementation history, P365, F-35, F-12, and relevant later review notes. Local code HEAD equals main at f2853e86ca96c89d8f97a6c3a17c9fd2661ad41d. Local notes HEAD equals main at c170846abd01d3514d9303567ef72d0d18907ea3 before these notes. Pinned ModernUO was verified at d4531cd94b739613155225c234900de9f47d2c88.

The main finding is that companion B1 and evo stage/mount infrastructure exist, while player companion gameplay and several evo progression connections remain unfinished. The existing tutorial loop counter is not connected to either feature's owner-loop provider. P365's Horse and Lizard look like mounts but are EvoPets, not rideable BaseMounts. Known P487/P521 defects and the old six-loop design's conflict with the current ladder remain explicit.

No code or docs-directory files changed. No lane tests or builds were requested or run. No new tests were added. No Haven connection, deployment, commit, merge, push, or branch switch occurred. Runtime, full restart, and client results remain unverified.

## Completion checks

Paused on the Golem's budget request and resumed after the user removed the stop condition. The final source/citation and recommendation review is complete. Another process advanced the notes repository's local main, but the governing companion design, F-12 note, and feature queue are unchanged against the comparison snapshot; the report records both references.

The required progress reporter completed with exit 0 and no stderr or reporter error markers, using the work-copy path overrides. Its dry-run-generated tools/progress.json was restored byte for byte, so no unrelated progress output remains. An initial output-printing helper's console encoding failure was corrected and capture rerun cleanly.

Formatting, file size, citation paths, working-tree scope, and git diff --check were verified. Only the two requested notes files are pending. No code, docs-directory file, service, or generated artifact changed. No required work remains for this notes-only task.

P527 DONE
