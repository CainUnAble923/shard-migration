# P604: patch notes for the rest of October 25

## Deliverables and scope

Wrote [the October 25 follow-up draft](cc-P604-patch-notes-2026-10-25b.md). This file is the outer lane's requested work record; the dated file is the task body's deliverable, following P594's two-file format. Both are explicitly requested Markdown files.

Read AGENTS.md in both work copies first, then the direction decision, task-list guidance, P594's draft, evidence note, and review. Both work copies started clean. Used only local history and files, without a fetch or remote request.

Code snapshot: `8b0ccb80c00aedd9898be6f453d419b0a2119f2c`, identical to P594's code cutoff. Notes baseline: P594 merge `77e596653055dc87ab02c1b6c9736a11d695f2ce`. Notes cutoff: P603 merge `995251a`. Coverage follows first-parent merges after P594 on October 25, 2026, in America/Chicago. The inventory below lists every merge in that interval.

No additional code merge falls after P594's cutoff. P479's implementation note merged into the notes repo after P594, but its code merge was already included in P594. A later note does not establish another code release. Generated progress and play-test reporting changes in the interval are reporting artifacts, not new game behavior or P604 test results.

## Merge inventory

| Notes merge | Task | Treatment |
| --- | --- | --- |
| `3346006` | P479, Tinker maintenance | Newly available implementation note. P594 already covered code merge `8b0ccb8`. Main Docker, timeout, and mail work is reported in the external Golem kit, outside the code repo. No new player feature or independently verified cleanup is announced. |
| `a1792e2` | P593, League Chapter 2 | Story draft acknowledged as a proposal. No playable trial, reward, or map release claimed. |
| `a749dc1` | P595, play-test plans | Pending plans for P454-P460 and P372. No executed or passing test claimed. P456 has no identified scope in that note and is not invented here. |
| `0b2576e` | P596, questions round 3 | Repair policy and Chapter 2 editing choices collected; recommendations are not decisions or repairs. |
| `0e67b68` | P598, High Seas review | Corrects P594's reward-access claim and adds the player cancellation warning. Further review findings remain unresolved; no exploit instructions published. |
| `e8043cc` | P599, High Seas guide refresh | Draft now covers merged fishing mechanisms and their acquisition limits. No publication, spawn placement, or new implementation claimed. |
| `e69b346` | P600, Hammer guide | New draft for available tiers and order crafting, with existing review caveats. No new tier or repair claimed. |
| `910e90c` | P601, League Chapter 3 | Story draft acknowledged without publishing plot reveals or promising a working encounter. |
| `40ecdca` | P602, Rangers guide refresh | Documents the existing elixir sale and proposed Tracking Ping. No new sale or Ping implementation announced. |
| `995251a` | P603, later play-test plans | Pending fishing, hammer, and staff-maintenance checks; no results or new service behavior claimed. |

## Evidence and editorial choices

Paths below are relative to the code work copy unless linked into this notes repo.

- Compared local first-parent history with P594's recorded cutoffs. The code snapshot did not advance. Read the new notes, relevant guide additions, and their source records. The table distinguishes implementation, review, writing, and proposed checks instead of turning each task title into a feature announcement.
- **Fishing rewards:** directly read `server/customizations/Services/Expansions/High Seas/Quests/ProfessionFishQuest/ProfessionalFisherQuest.cs`, `PlayerFishingEntry.cs`, and `FishQuestHelper.cs`. `BuildLines` fixes orders to one line and clamps the quantity to 20; the greatest per-fish award is three points. The resulting maximum of 60 is below tier 2's 100-point threshold. `Complete` passes this order's points to the reward helper, not accumulated reputation. The first reward row contains bait, lava traps, guide books 1 and 2, power scrolls, and poles, without hooks or the Oracle. Charybdis bait requires a later tier. This source finding supports [P598's stronger restriction](cc-P598-review-high-seas-second-half.md) and corrects P594's suggestion that the reachable rewards included hooks and the Oracle.
- **Cancellation:** directly read `ProfessionalFisherQuest.cs` and `ShippingCrate.cs`. The in-progress window offers Close; crate drop overrides prevent ordinary disposal. P598's parent/interface walk found no usable cancellation path. Read pinned `D:/UO/ModernUO-pinned/Projects/UOContent/Multis/Boats/BaseBoat.cs`, whose dry-dock check rejects a nonempty hold. The warning is a source finding, not a runtime reproduction. No staff command or deletion procedure is published.
- **Fishing guide:** inspected the actual diff to [high-seas-fishing.md](wiki-drafts/high-seas-fishing.md) and [P599's evidence](cc-P599-guide-high-seas-refresh.md). Its corrections preserve built-versus-obtainable distinctions, missing ingredients, dormant pie effects, and unfinished Corgul access. P598's item-handling and delivery findings are acknowledged without steps for exploiting them. No fishing code changed after that review.
- **Hammer guide:** read [the draft](wiki-drafts/hammer-of-hephaestus.md), [P600's source record](cc-P600-guide-hammer.md), and P594's hammer evidence. The supplement describes a documentation addition and preserves known whole-small-deed consumption, recovery, and tooltip limits. It does not repeat every existing feature as newly merged work.
- **Rangers guide:** inspected its actual diff and [P602's evidence](cc-P602-guide-rangers-refresh.md). Directly read `server/customizations/OutridersGuildmasterGump.cs`, `Tutorial/TutorialPetCare.cs`, and `Items/Consumables/ElixirOfRebirth.cs` to confirm the preexisting sale and use paths. The guide's Ping section explicitly describes an unimplemented proposal. No new Ping capability is asserted.
- **Story and decisions:** read [P593's handoff](cc-P593-league-story-chapter-2-draft.md), [P601's handoff](cc-P601-league-story-chapter-3-draft.md), and [P596's reconciliation](cc-P596-questions-for-chase-round-3.md). All describe drafts or unresolved choices. Kept later plot reveals out of the patch notes.
- **Play tests and maintenance:** read the scope, plan inventories, and validation limits in [P595](cc-P595-playtest-plans-10-25.md) and [P603](cc-P603-playtest-plans-10-25b.md), plus [P479's implementation note](cc-P479-tinker-docker-prune.md). Plans remain pending. P479 reports work in an external kit; this task did not run or independently validate that kit, prune images, compact disks, or send mail.

## Validation and limits

Documentation only; lane tests are none. No tests or gates were added, so no failing/passing cycle applies. No build or gameplay test was run. Running version, effective settings, installed player package, fish-monger placement, guide publication, playable chapters, deployed kit, and actual player outcomes remain unverified.

- Commands ran under Windows PowerShell 5.1.26100.9711. No PowerShell tests were needed or run.
- Ran the required progress reporter with work-copy overrides and `--dry-run`. Suppressed its known unconditional `tools/progress.json` write for that exact path in memory, without changing tool source. The report completed and the original snapshot remained byte-identical. No generated reporting changes are delivered.
- Compared the merge table with local first-parent history from P594 through P603. Every merge matches exactly and in order. The unchanged code HEAD also matches P594's recorded cutoff.
- Checked both files directly for ASCII text, relative Markdown links, trailing whitespace, final newlines, and the 5 MB limit. All checks passed. ASCII text excludes em dashes. Reviewed the draft for plain American English, release boundaries, hidden achievement spoilers, story spoilers, and exploit instructions.
- `git diff --check` passed in both work copies. Final scope inspection found only these two new notes files; the code work copy is clean. No code, docs directory, service inventory, configuration, package, save, account, or test result changed.
- No Haven connection, deployment, external message, commit, merge, push, or branch switch occurred. Stop-request checks were clear between research, drafting, and validation. No P604 work remains.

P604 DONE
