# P395: wiki drafts cross-check

Reviewed October 22, 2026. Documentation review only.

## Deliverable

- [Cross-check report](wiki-drafts/cross-check-2026-10-22.md): tables comparing draft statements, the feature queue, and source behavior; pages to review; terminology differences; local link dependencies; availability limits; Sources and Contradictions lists.
- The report inventories all 34 original draft files individually. It excludes itself from that input inventory.
- Findings identify review targets without editing the drafts or resolving their design differences. Planned work is marked (planned). The report contains no staff commands, exploit instructions, or hidden-achievement discovery details.

## Reading and evidence

Read AGENTS.md in both work copies first, then the required direction decision, task list, complete feature queue, and every original file under notes/wiki-drafts, including its pages subtree. Compared overlapping guild, crafting, achievement, box, League, tutorial, pet, and progression statements.

Checked the relevant canonical customizations and targeted patches. Checked pinned ModernUO's death-event order, NPC deletion, stock power scroll behavior, and fishing bonus where those questions cross upstream boundaries. The pinned checkout reports d4531cd94b739613155225c234900de9f47d2c88. Did not read server/uo.

The report separates direct disagreements, differences between decided work and implementation, and claims whose deployment remains unverified. For example, it distinguishes an Iron-rank box from a registration achievement box and a loot-table slot from a physical item count. It retains the existing uncertainty about relative gear strength and future XP decisions.

## Verification

- Local Markdown link targets exist. DokuWiki targets were resolved relative to each page namespace against both the draft overlay and docker/wiki/content/pages. None were missing from both local sets. The report lists every dependency supplied by the base wiki, with referring draft lines.
- Local media targets referenced by the draft pages exist in docker/wiki/content/media. Live URLs and heading anchors were not checked.
- Checked cited source paths and line bounds, draft paths and line bounds, table shape, input inventory, file sizes, and report wording. No em dashes or unfinished placeholders remain in the report.
- Ran tools/progress.py in dry-run mode with the two work-copy paths supplied through its path overrides. It exited successfully. Despite its dry-run documentation, its build() function writes tools/progress.json at tools/progress.py:722 before main() checks the dry-run return at line 737. The work copy was clean at entry; restored that generated snapshot to its original HEAD bytes and confirmed it is no longer changed. This is an existing tooling defect in our progress helper, observed from the file diff and confirmed in its source. No helper fix was made in this documentation task. Its broader project-state notices were not treated as verified deployment facts.
- Lane tests: none, as requested. No tests or gates were added, and no build or gameplay tests were run. This work changes no executable behavior.
- Windows PowerShell 5.1 was used for shell work. No connection to Haven, deployment, world access, account changes, commit, merge, push, or branch switch occurred.

## Limits and handoff

Running configuration, deployment, world placement, client appearance, and current live wiki contents remain unverified. Source inspection supports the reported boss-box event-order defect; it was not reproduced in a running shard during this review.

Only this task note and the requested cross-check report are deliverables. Original drafts, code, docs, and base wiki content remain unchanged. Contradictions are left for review, not repaired here.

P395 DONE
