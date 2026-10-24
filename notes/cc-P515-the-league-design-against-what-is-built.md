# P515: the League design against what is built

Completed the source comparison requested by the Golem's Codex lane prompt. The full table is in
[cc-P515-league-design-vs-build.md](cc-P515-league-design-vs-build.md), the deliverable named inside
the CC task. This file uses the separate notes filename supplied by the lane wrapper so both requested
paths are present without duplicating the report.

Compared P179, P47, the League institution design, and the relevant feature-queue entries against code
`6f540be8b84f63f76b8852fe638039b363b66a6b`. The design checkout was
`d80e795115eafda1946071aadd9d46516b8680ba`. Both task HEADs equaled local main. Reviewed on
2026-10-24 for the prompt written 2026-10-23; remote main and the running shard were not checked.

The report carries every October 23 answer forward. It marks the shop/Hall/backpack work delivered,
uses the six named chapter milestones, accepts the requisition/Lead changes and immediate standing,
uses the approved Citizen Commission permission ranks, avoids an AP ceiling or title count, drops
Warehouse/Featherweight, and retains the missing Clockwork Scavenger.

Main gaps: common League contracts and payouts, board/caps, banked job rewards, party progress,
promotion jobs, Citizen Commissions and escrow/claims, Client Commission relocation/Infamy, private
trial maps, and the story chapters. P179 goods are largely built. Its remaining work includes per-guild
book actions, paging, complete turn-in routing, and F-34 bank crafting. The report distinguishes current
mixed-craft BOD-book support from an optional new League product, and multi-currency mule upgrades
from the missing general multi-reputation rank rule.

Source-level follow-ups are recorded with evidence and scope: Register layout limits, reset-time binding
cleanup, unwired first-Haul/hunt/loop hooks, partial mule effects, and the outdated evo slot assumption
in the follower curve. They were not fixed in this docs-only task.

Validation: no code or docs/ files changed; no tests added or changed; no lane test/build/game run.
Windows commands ran in Windows PowerShell 5.1. No Haven, deployment, commit, merge, push, or branch
switch. Stop-request file checked between steps.

Ran `tools/progress.py --dry-run` with the work-copy path overrides. It completed, but its implementation
still writes `tools/progress.json` inside `build()` before checking `--dry-run` (`tools/progress.py:722`,
`:737`), despite the documented print-only behavior. Restored that generated change from the initially
clean HEAD; it is not part of this task. Treat this as an existing reporter defect for a separate prompt.
The global progress figures are not League coverage measurements and were not used to size these gaps.

Final checks passed: cited canonical source files exist, line references are within their files,
tables have consistent columns, both notes have no em dashes or trailing whitespace, and each file
is below 5 MB. The code work copy is clean; the migration work copy adds only these two notes.
No work remains in P515.

P515 DONE
