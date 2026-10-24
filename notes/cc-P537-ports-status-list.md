# P537 work record: every ServUO port in one status list

October 24, 2026. Deliverable: [cc-P537-ports-status.md](cc-P537-ports-status.md).

The report gives each named port family its prompts, local-main merge state, recorded tester route or verification limit, open fix-ups and next step. Earlier creature/equipment batches link to their original file lists. It includes the Port, reward, ride-along, design-source, later and dropped dispositions, plus the CODE-INTAKE assessment families, without treating a download or proposed native rebuild as a merged port.

## Work and evidence

- Read both work-copy AGENTS.md files, direction-decision.md, docs/README.md, tasks.md and the feature queue's port entries. Kept ModernUO as the engine and all writing under notes/.
- Reconciled port-list-2026-10-13.md/json and tools/port-list.json with CC/S implementation notes, the P1xx port notes, P193-P199 and their merge fix-ups, and code main's history. Did not use filename-stem completion as behavioral evidence.
- Read the intake assessment summaries and relevant follow-ups in P93, P98, P100, P104, P211, P212, P268 and P405. Checked canonical files and main history for implemented exceptions. P93's proposed P96/P97 and P212's proposed P223/P224 labels were reused; the draft numbers alone do not establish implementation.
- Read the later review and follow-up evidence for Eodon, BODs, fishing, cleanup, Blackthorn, Underworld, monster stealing, Exodus, Wrong/Covetous and Halloween. Used P429, P476 and P533 to preserve proposed fix ownership without reporting drafts as merged fixes.
- Checked testing/play-tests.json for dated passes and remaining open groups. Read the October 2 fountain and October 3 Despise/board/stealable client records. P122 has October 18 player passes; P119/P121 have partial passes; the later port groups still have open checks.
- Inspected canonical source and file histories for the named integrations, including AthenaeumIsle.cs, existing Aloron/Darden armor, the Underworld fountain generator, TreasureMapInfo loot, Pet Training taming hooks, cleanup accounting and bag/sweep paths. Did not read server/uo/.

## Corrections carried into the list

- P197 reached main while its note remained PAUSED. Its subsystem/client acceptance is unfinished. The named continuation P352 is stale because main's P352 is fog of war.
- P209/P221/P245/P271/P354 resolved integration of their port work. Those completed merge fix-ups do not complete the separately documented missing gameplay systems.
- Fishing remains a partial implementation, and Blackthorn's city invasion remains deferred. Staff-spawned sea champions are not a natural summoning route.
- P198's statement that Aloron/Darden items are unported contradicts their existing canonical folders and S1/CC9 history. The remaining recipe/drop integration must reuse the items.
- P530 predates the P414/P415 cleanup merges. Contracts now count points, old bundles have a conversion, and corpse menus/loot-right checks exist. Other P432 accounting, bag replacement, store and sweep findings are not all resolved by those changes.
- Despise has dated partial client verification and subsequent possession fixes, not a blanket current client pass. Shame's combined T-007 check remains open. Fountain placement and walking have dated client evidence but the final-paver coin test was not recorded.
- P142 saves monster-stealing state and adds the Life Shield Lotion consumer. P127's original in-memory-state and unwired-lotion descriptions are historical; Balm of Protection still needs its consumer.

## Snapshot and concurrent main change

Work-copy HEADs stayed code 491bb490b1f343bc99bac1f7207fbb1a847d3535 and notes 0e6ee6e922c2dea91e91554a0b0fe4bb704f6bde on their assigned P537 branches.

During the resumed run main advanced to code 82ba93fdd3e047646cdf63cb4f468b9a30b90270 and notes 7bad9b4602b82ee478cc4fc8430882c02495fa01. Read that delta and its P427 note directly using git show/diff without switching branches. P427 adds the ported craft-deed store-bought-item refusal; the list includes it. The other changed implementation paths concern native level gear, achievements and art metadata, not additional content ports. Compared the relevant port play-test statuses/results across that notes delta: unchanged.

## Verification and limits

Lane tests: none. No tests added, so no new red/green requirement arose. No builds or gameplay tests run for this prose-only task. Historical test results are attributed to their source notes; review findings were not newly reproduced.

Ran tools/progress.py --dry-run against these work copies. The tool still attempts to write tools/progress.json before its dry-run return. Suppressed that one write in memory, verified the existing file stayed byte-identical and did not regenerate README/dashboard or change any generated output. Its global stem counts are not used as a port acceptance measure.

Document checks cover relative links, table-column consistency, ASCII/no em dashes, trailing whitespace and the 5 MB limit. Repository checks confirm the code work copy is clean and only these two P537 notes are changed in the migration work copy. Windows PowerShell 5.1 ran shell commands. No docs/ edit, Haven connection, deployment, account operation, commit, merge, push or branch switch.

Current deployed image, published player package, saved-world placements and full current client acceptance remain unverified. The report says so and assigns the next verification step rather than inventing a tester-ready result.

The first sitting paused when the Golem's usage window reached 95 percent. This same session resumed on the user's instruction after the stop file was removed. The research, consolidation and document checks are complete; no P537 implementation work is outstanding.

P537 DONE
