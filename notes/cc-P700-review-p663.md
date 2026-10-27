# P700: review of P663

2026-10-27. Review could not proceed because the supplied work copies do not contain P663's implementation or completion notes. This is a missing prerequisite, not a finding against P663. No code changed.

## Scope and evidence

Read both work copies' `AGENTS.md`, `docs/direction-decision.md`, `docs/tasks.md`, P481 sections 4, 7, 11 and 12, and P673 section 1.4. All paths below refer to the supplied work copies, not the original repositories.

Reviewed checkout heads:

- Code: `1ffd5c8d3930a60edf40dbe5c590a5158a172b11`.
- Notes: `76a0822059aa73456b054f113755330728469736`.

Evidence that the requested review target is missing:

- No file matches `notes/cc-P663-*.md`. `git ls-files 'notes/*P663*'` also returns no paths. Consequently, P663's implementation file list and verification record are unavailable.
- `git log --all --oneline --grep=P663` returns no entries in either work copy's local refs. This does not establish the state of any remote or another lane's work copy, which were not checked.
- `server/customizations/CharacterCreation.cs:129` still constructs a single starting city. Line 134 is New Haven at `(3503, 2574, 14)` on `Map.Trammel`. P481 section 7's two-city start choice is absent here.
- `server/customizations/Tutorial/ClusterFTutorial.cs:112` still implements the older account entry path. Lines 125 to 127 welcome the player to New Haven and point to Rook. These are baseline observations, not new defects attributed to P663.
- `server/customizations/Tutorial/TutorialIslandGate.cs:23` still recognizes only the Trammel Haven bounds and Rootdeep. This is the older gate rule that P481 section 12.3 explicitly assigns to the implementation prompt.
- A recursive search of canonical `server/customizations/**/*.cs` found no `HavenSpots` or `StartChoice` identifier. Neither name occurs in tracked filenames. P673's `notes/cc-P673-sos-swap-plan.md:104` explicitly requires P663 to read Haven destinations through `HavenSpots`.

## Review status

No severity-ranked P663 code findings are issued. Reporting the baseline's known missing island behavior as P663 regressions would review the wrong implementation and repeat work already assigned by the design.

| Requested check | Status and remaining work |
|---|---|
| Eligibility table rows | Unverified. Read P663's actual table and follow every row through character creation, first login, account state and staff handling. |
| Choice consumed once | Unverified. The two-city choice implementation and its persisted state are missing. Check first login, reconnect, restart and another character on the account once present. |
| Pets crossing | Unverified. Follow every implemented Fold crossing, including arrival, dock exit and remedial entry. Check controlled pets beyond stock teleport range and confirm which source maps each route covers. |
| Resume at first undone stop | Unverified. Follow saved station keys and current lesson supplies through reconnect, including a record that already completed travel under the old order. |
| HavenSpots completeness | Unverified. No implementation is present. Check the skip start, Rook, dock exit, island gate bounds and Fold mirror destination against P673 section 1.4. |
| Remaining Map.Trammel uses | Unverified for P663. Audit the implementation file list when available, distinguishing core lessons moved to the Fold from trade and wing lessons intentionally retained in Haven. Baseline occurrences are not P663 findings. |
| Earlier review overlap | Deferred with the substantive review. Compare each candidate finding with earlier tutorial reviews before publishing it. No earlier findings are repeated here. |

## Verification and handoff

- Read-only source and local Git inspection only. No build, runtime test or client session was run. Lane tests are none; no tests were added.
- Windows PowerShell 5.1 was confirmed for the inspection commands.
- Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies; exit 0. Its aggregate output is not evidence of P663 completion. Despite its dry-run description, the script writes `tools/progress.json` at line 722 before checking the flag at line 737. Restored that initially clean file from HEAD so this task leaves only this note changed. No tool fix was made.
- No Haven connection, deployment, commit, merge, push or branch switch. No `docs/` edits.
- The stop-request file was absent at the last check.
- To resume: supply work copies containing the completed P663 changes and `notes/cc-P663-*.md`, then perform the review above and replace this blocked status with severity, file:line, behavior and fix for each new finding. No Chase design decision is needed to resolve this prerequisite.

P700 STOPPED: P663 implementation and completion notes are absent from the supplied work copies.
