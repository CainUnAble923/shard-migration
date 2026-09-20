# Which of these documents govern

Twenty files accumulate fast, and a reader cannot tell from a filename which four actually
decide anything. This is that list. **If a document is not in the "live" table, do not plan
from it.**

## Live: read these

| Document | What it decides |
|---|---|
| `tasks.md` | **The** task list. Everything else defers to it |
| `subsystem-policy.md` | when to build a missing subsystem, when to patch upstream, standing decisions |
| `fidelity-principle.md` | port unchanged, and the running log of every deliberate deviation |
| `gap-register.md` | every decline and gap in one place, with what closes each |
| `patch-backlog.md` | what ModernUO is missing and the patch that would close it, ranked by leverage |
| `bug-list.md` | defects to look at fixing: ours, ServUO's copied on purpose, and ModernUO's |
| `how-this-works.md` | the loop, who does what, why the lines fall where they do |
| `upstream-watch.md` | what ModernUO is building, and what a pinned-commit bump risks |
| `community-scripts-wishlist.md` | the separate custom-content lane and its rules |

## Reference: correct, but narrow

`content-menu.md` (four rows measured properly, the rest explicitly unverified),
`flat-namespace-problem.md`, `client-analysis.md`, `highseas-eodon-feasibility.md`,
`eodon-separability.md` (conclusion sound, file table corrected three times).

## History: do not plan from these

`migration-plan.md`, `port-triage.md`, `implementation-status.md` — written for a
migrate-to-ServUO plan that was not taken.
`backlog.md` — absorbed into `tasks.md`.
`workstreams.md`, `work-split.md`, `shard-inventory.md` — superseded; each says so at the top.
`direction-decision.md` — the decision is settled and still binding; the document is the record
of how it was reached, including four reversals. Do not reopen it.

## The rule that produced this file

**Every number in `docs/` is wrong until someone re-measures it.** Ten counts have moved under
scrutiny, two of them after driving a decision, and three more were weak-filtered figures being
read as raw. Live counts come from `python tools/progress.py`; anything typed by hand is a
snapshot with a date on it.
