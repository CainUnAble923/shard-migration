# P399: Guilds index page

Date: October 22, 2026.

## Scope and changes

- Added `notes/wiki-drafts/guilds.md`, a player-facing draft index with the League followed by every guild in the supplied roster, joining guidance, rewards, guide links, and play-style choices.
- Kept Sources and Contradictions at the end. Recorded source differences without changing the source documents or choosing new rules.
- No code, configuration, existing wiki page, or `docs/` edits. No Haven connection, deployment, commit, merge, push, or branch switch.

## Reading and evidence

Read both work copies' `AGENTS.md`, plus `docs/direction-decision.md` and the task-list context. Read the following draft sources:

- `notes/wiki-drafts/league.md`
- `notes/wiki-drafts/society-of-smiths.md`
- `notes/wiki-drafts/artificers-order.md`
- `notes/wiki-drafts/order-of-the-alembic.md`
- `notes/wiki-drafts/gathering-guilds.md`
- `notes/wiki-drafts/rangers-custodians-healers.md`
- `notes/wiki-drafts/thieves-den.md`
- `notes/wiki-drafts/glossary.md`
- `notes/wiki-drafts/crafting-changes.md`, the existing shared guide referenced by the glossary for guilds without dedicated pages.

Also read `notes/wiki-drafts/new-haven-start.md` to check the glossary's suggested destination for the remaining guilds. That page no longer supplies their guild details, so those index links point directly to the glossary entries instead.

Reviewed the feature queue's section inventory and guild-relevant decisions, including F-3, F-9, F-20, F-24, F-33, F-37, F-38, F-43, and F-47 through F-51. It supplies comparison context rather than new gameplay claims in the table.

## Coverage and limits

The index has 18 guild rows plus a separate League row, counted from the table and compared with F-9's skill roster and F-49's hall roster. The guild list is:

1. Warriors' Brotherhood
2. Arcane Society
3. Healers' Covenant
4. Rangers' League, also called the Outriders
5. Miners' Compact
6. Society of Smiths
7. Tinkers' Union
8. Thieves' Den
9. Twin Paths Dojo
10. Keepers of the Last Door
11. Foresters' Union
12. Tailors' Circle
13. Maritime Brotherhood
14. Merchants' Exchange
15. Bards' Consortium
16. Artificers' Order
17. Order of the Alembic
18. The Custodians

Outriders is an alias, not an extra guild. Smiths' Fellowship and Healers' Circle are retained only in Contradictions as historical or conflicting names.

The supplied drafts have no dedicated guides for Warriors, Arcane, Tinkers, Tailors, Maritime, Merchants, Bards, the Dojo, or Keepers. Used the glossary and existing shared crafting guide, and marked guild-specific rewards not covered for Warriors, Merchants, Bards, the Dojo, and Keepers. This does not claim they have no rewards. Did not invent contacts, currencies, prices, rank thresholds, or rewards to fill those gaps.

This task summarizes draft pages as requested; implementation, current settings, world placement, and running-shard availability were not independently verified. The draft says availability is unchecked. Planned halls, trials, broader League jobs, Herbalism, and Fishing/Cartography deeds are labeled `(planned)`.

## Validation

- Reviewed every table row against the linked drafts and compared the named roster with F-9 and F-49. The table contains the League and the 18 guilds listed above, with no duplicate Outriders row.
- Read-only link review found 24 distinct local destinations, including section anchors, with no missing files or anchors. All roster rows have the requested five columns.
- The player draft has no em dashes, staff commands, exploit instructions, hidden-achievement details, or invented gameplay numbers. Its only command is the documented player Guild Directory command. Sources and Contradictions are its final sections.
- Both new files are below 5 MB. `git diff --check` passed; changed-file review shows only the requested draft and task notes in the docs work copy and no changes in the code work copy.
- Lane tests: none, as specified. No tests or gates added. Review commands ran under Windows PowerShell 5.1; no build or gameplay tests were needed for this prose-only task.
- Ran `tools/progress.py --dry-run` with work-copy path overrides in report-only mode. The script normally writes `tools/progress.json` from inside its report builder even with `--dry-run`; an in-memory `Path.write_text` wrapper suppressed that generated write. The report completed without changing progress files, the README, or dashboards. Its unrelated review backlog was left for the overseer.
- Checked `D:\UO\golem\codex-runs\P399-Verite.STOP-REQUESTED` between steps; no stop request was present at the recorded checkpoints.

## Outcome

The draft index and notes are ready for the Golem's review and commit. Missing guild-guide detail is explicit, planned features are labeled, and source contradictions remain unresolved.

P399 DONE
