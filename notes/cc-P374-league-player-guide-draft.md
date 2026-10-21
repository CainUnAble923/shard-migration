# cc-P374: League player-guide draft

2026-10-21, Valorite Codex lane. Documentation only in the two assigned work copies. No code, builds, test shard, deployment, Haven connection, commit, merge, push, or branch switch.

## Deliverable

`notes/wiki-drafts/league.md`: a player-facing draft covering the League's purpose and day-one access, ranks and Renown, work, requisitions and Leads, the reward shop and Hall page, locations, and the broken-sword story. Planned content is labeled `(planned)`. The Sources section links the notes and records contradictions without deciding them.

## Reading

- Both work-copy `AGENTS.md` files, then shard-migration `docs/README.md`, `docs/direction-decision.md`, and `docs/tasks.md` (read only).
- All six requested notes: `cc-P47-league-research.md`, `cc-P48-league-batch-1.md`, `cc-P75-league-rewards-rethink.md`, `cc-P179-league-design-pass.md`, `cc-P229-league-reward-shop.md`, and `cc-P243-league-hall-decor-rewards.md`.
- League-related entries in `docs/feature-queue.md`: F-9, F-12, F-13, F-19, F-24, F-25, F-33, F-34, F-37, F-47, F-48, and F-49; League references elsewhere were searched for context.
- Additional evidence: `cc-P150-requisitions-and-leads.md`, `cc-P203-cont-fixup-requisitions-and-leads.md`, and the summary and League HQ section of `cc-P151-guild-halls-survey.md`. These distinguish completed requisitions and Leads from the still-planned headquarters.
- Read-only spot checks in canonical code: `server/customizations/ClusterFLeagueSystem.cs` registration; `ClusterFLeagueRanks.cs` default table and commentary; `LeagueShop/LeagueShop.cs` stock and title definitions; `LeagueShop/LeagueHall.cs` stock and price settings; `Requisitions/RequisitionSystem.cs` per-character requests, tiers, refresh exception, and turn-in payout; `Requisitions/RequisitionLeads.cs` qualifying kills and the pity guarantee. No generated `server/uo/` files were read.

## Contradictions and editorial handling

- P47's Blaze 11 and Mythril 14 disagree with P48's Blaze 12 and Mythril 15. F-24's "every third rank" also differs from its named milestones. Use metal names without chapter rank numbers; preserve the discrepancy in Sources.
- F-24's six named chapters coexist with its "five trials" wording. Both are recorded in Sources.
- F-19 and the early F-24/F-25 decisions say bonuses per rank, while the later F-24 decision and P48 use milestones. Both versions are recorded; no source was edited to reconcile them.
- The older commission permissions use Steel and Silver, absent from the ladder; P47's proposed Verite and Blaze mappings are not treated as final posting permissions.
- P47, P75, and P179 report no Renown spender; P229 and P243 record built shops. F-13 retains the older statement. The draft identifies the built shops from their build notes without rewriting any earlier source.
- Older notes and F-13 state 2,505 AP; P229 reports 1,955. P229's file summary says nine titles while its picker and three-plus-five description say eight. The draft advertises neither a maximum AP total nor an exhaustive title count. The current source also contains later hidden achievement titles, outside this prompt's source set; they were not added to the guide.
- F-47/F-48 remain future-facing while P150/P203 record requisitions and Leads built. P150 retains live-Lead requests through daily refresh, uses an extra roll with pity rather than promising a literal doubling of natural drops, and uses an area/group/Fame requirement rather than the proposed loot-table test. Both source descriptions remain linked and the differences are explicit.
- F-24 banks future League-job rewards until the Apprentice task; P150 pays requisition standing immediately, even to non-members. The guide does not silently apply either rule to the other system.
- P75's proposed Warehouse, Featherweight satchels, and Scavenger replacement are not approved inventory. P179 recommends different ownership of storage upgrades and asks for decisions. These proposal tensions remain recorded; no proposed utility price or availability was invented.
- P229's tradeable cosmetics/decor and P243's bound Hall deeds are an explicit product distinction, not a conflict to fix. The guide keeps both rules.

P48's promotion thresholds and P243's Hall prices are described as placeholders/proposals in their notes. The draft refers players to displayed promotion requirements and omits Hall prices, while reproducing only P229's recorded starter price table. It adds no new prices, coordinates, quotes, or lore. No System-voice quote was necessary.

## Verification and limits

Editorial review completed against the sources. Read the draft back and checked all requested sections, planned labels, source links, starter shop values, and the distinction between available services and proposals. Every source link resolves locally. The draft contains no em dashes, and neither new file has trailing whitespace.

File-scope review: ShatteredLegacy remains clean. shard-migration has only the two new files named above; `docs/` is unchanged. Both new files are below 5 MB. `git diff --check` reports no tracked-file whitespace problems; the separate text inspection also covered the untracked deliverables.

Ran the existing `python tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing at these work copies: exit 0. Despite the documented print-only behavior, it rewrote `tools/progress.json`. This is an existing defect in our reporting tool: `tools/progress.py:722` writes the JSON inside `build()`, called at line 732 before the dry-run return at line 737. The observed diff changed the generated timestamp to this run's 14:26:37 and refreshed queue data. No README was rewritten. This code defect is recorded here, not fixed in the prose-only task.

Restored only the generated JSON to its clean pre-run HEAD contents and verified `git diff --exit-code -- tools/progress.json` passes. `git restore --worktree` was denied an index lock outside the writable work copy; a read-only `git show HEAD:tools/progress.json` and byte-preserving write inside this work copy completed the restoration. Final scope is again only the two requested notes files. The reporter's unrelated overseer-review items were not acted on.

No automated tests were added or run; this task changes prose only. Local checks used Windows PowerShell 5.1 (5.1.26100.9444). Running-world placement, current configuration, client appearance, and deployment remain unverified. STOP-REQUESTED was checked between work steps and was absent through the final editorial review.

## Timing

The session event file `D:/UO/golem/codex-runs/P374-lane-2.events.jsonl` was created at 14:17:02 CDT. The first successful local clock reading was 14:20:48 CDT. Earlier local command calls stalled; selecting the absolute Windows PowerShell executable restored file access. Final review and cleanup finished at 14:28:13 CDT on 2026-10-21. Elapsed run time from the session event file creation: 11 minutes 11 seconds, including the initial tool delay.

P374 DONE
