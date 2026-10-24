# P540: shard glossary update

October 24, 2026. Unattended Codex lane, Valorite tower. Documentation only.

## Result

Updated [the glossary](wiki-drafts/glossary.md) with the current tutorial core and optional wings, lesson supplies and controls, pet care, living reward mounts and statuettes, and the October 23 League answers. Added explicitly planned entries for quest markers, mining and harvest quotas, Town Houses, and P481's custom facet and tutorial island. Existing terms were retained. The glossary itself supplies the full term list.

The League entries now follow the recorded answers: six story chapters, Blaze and Mythril for chapters four and five, milestone bonuses, planned commission permissions, delivered Renown spenders, no published AP ceiling or title count, accepted requisition and Lead behavior, immediate non-member requisition standing, retired Warehouse and Featherweight proposals, and the retained planned Scavenger. The old contradictions section now identifies these as settled instead of presenting an unanswered choice. Hidden achievement triggers and hidden titles remain undisclosed.

Only the glossary and this required task note changed. No code or other guide was edited.

## Evidence and status boundaries

Read both work-copy AGENTS.md files first, plus the direction decision and task list. Canonical code was read from this lane's ShatteredLegacy/server/customizations, never server/uo. Related draft guides and implementation notes supplied context; a guide's claim of placement was not treated as evidence of running availability.

| Topic | Sources inspected | Treatment in the glossary |
|---|---|---|
| Core lessons and wings | `Tutorial/TutorialStations.cs`, `TutorialCoreTrials.cs`, `TutorialWingTrials.cs`, `TutorialTradeTrials.cs`, and `TutorialRecruiter.cs`; [current tutorial guide](wiki-drafts/new-player-tutorial.md), P289/P475/P480/P290/P291 context | Built New Haven lessons and action-based completion, required core versus optional wings, loaned supplies and skill, Hint and arrow, reset, and the existing vision. The new start area remains planned. |
| Pet care | `Tutorial/TutorialPetCare.cs:94`, `:136`, and the current tutorial guide | Sera is the core resurrection contact; Tobin handles pets. Young players pay no vet fee, but pet skill loss still applies. The corpse must fade first. |
| League answers | `docs/feature-queue.md:2018` under F-24, recording Chase's October 23 acceptance of P376's recommendations; [P376](cc-P376-league-decisions.md) | The recorded answers govern plans. They do not turn an unbuilt feature into a delivered one. The earlier League guide still contains superseded questions; only this glossary was authorized for editing. |
| League built behavior | `ClusterFLeagueRanks.cs:485`, `ClusterFBankLimit.cs:25`, `Requisitions/RequisitionLeads.cs:182` and `:210`, `RequisitionTable.cs:71` | Named story milestones, bank growth by milestone, Lead qualification and the source-default guarantee. Remaining bonus types and commissions stay planned. |
| Reward mounts | `Mobiles/Mounts/RewardMounts.cs:59` and `:114`, `RewardMountStatuette.cs:50`, `LeagueShop/LeagueShop.cs:122`; [mounts guide](wiki-drafts/mounts.md) and P365 context | Built definitions and routes; consumed statuettes call bonded living mounts, with one follower slot and horse-level source stats. Evo animals and reusable veteran figurines are separate. Eligible Tamer/Boss box availability and current player-package delivery are not promised. |
| Quest markers | [P522 review](cc-P522-review-quest-markers.md); no `QuestMarkers.cs` or `QuestMarkers` reference in the current tracked server/package source; pending P363 and P520 prompts below | Planned/pending integration in this work copy. The exclamation mark offers a quest; the question mark indicates a ready turn-in, per the requested design. No claim of a completed implementation review. |
| Mining quotas | `ClusterFWorkOrderSystem.cs:405` (Raw Ore Sample) and its Ore Refinement Run definition still require Iron Ore; no quota implementation found in current customizations; [P417 design](cc-P417-gathering-orders-design.md), especially its P416 dependency discussion | P416's mine-after-acceptance change stays planned here. P417's broader personal harvest quotas are proposals, with gathered goods kept. No second metal, issuance cadence, price, or payout is invented as a settled rule. |
| Town Houses | [P409 design](cc-P409-town-houses-design.md) and [P542 integration note](cc-P542-cont-fixup-town-houses-design.md) | Planned leaseholds, signs, credit, grace, belongings crates, and sublets. P409's rent/sale choice, tuning, limits, and eligibility remain open; recommendations are not presented as approved rules. |
| New facet plan | P481 queued prompt below and the current tutorial guide's planned-area section | Planned new facet, tutorial island, one-direction route ending in New Haven, private visibility plus a private vision, and character creation start-or-skip choice. No map index, size, or client support claim is supplied as verified. |

Pending prompt files read as requirements, without executing their operational instructions:

- `D:/UO/cc-prompts/merging/cc-P363-quest-markers-keys-gates.md` and `cc-P520-cont-fixup-quest-markers-keys-gates.md`.
- `D:/UO/cc-prompts/queue/cc-P416-stone-mining-gate.md`.
- `D:/UO/cc-prompts/queue/cc-P481-new-player-start-area-design.md`. No P481 completion note exists in this work copy. Its later direction favors a new facet and mixed privacy, while still requiring design and Chase's choice before construction.

## Verification limits

Source review establishes definitions and integration state in these work copies, not deployment. Running-world settings, placement, spawns, client appearance, player-package publication, and the final choices for the planned systems remain unverified. No Haven connection, live service inspection, Docker command, deployment, account operation, commit, merge, push, or branch switch occurred.

No lane tests were requested and no new tests were added for this prose-only edit. Shell commands used Windows PowerShell 5.1, observed version `5.1.26100.9711`. The progress generator was not run because its writes would exceed the task's explicit two-file scope; P525 also records that its dry-run mode writes progress.json.

## Editorial checks

Passed: relative links and reference definitions (including the League decision anchor), alphabetical term placement, preservation of every original term, unique entries, table structure, no em dashes, changed files below 5 MB, and git diff --check. Final status confirms a clean code work copy and only the requested glossary and this note changed in the notes work copy. No tests or build were needed. No work remains for P540.

Stop request received at the completion boundary. The glossary and checks are complete; no glossary work remains. Request: Find a stopping point: the 5-hour window is at 99% (the hard stop is 95%: past 100% Codex spends credits)

Resumed October 24 after the Golem cleared the stop request. The work copies still contain only the completed glossary update and this note. Rechecked relative links, reference definitions, plain punctuation, file sizes, whitespace, and scope. No further glossary edits were needed.

P540 DONE
