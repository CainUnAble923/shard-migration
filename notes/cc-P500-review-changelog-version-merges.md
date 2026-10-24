# P500: review of CHANGELOG and VERSION merge handling

Reviewed 2026-10-23. Findings only. No code or tests changed.

## Source and scope

Read both work copies' AGENTS.md, the direction decision, the task list, and `notes/cc-P213-cont-changelog-version-merges.md`. No separate P213 review was found beside those notes.

P213's notes are in migration main through merge `5ff30d1` and implementation-notes commit `9e8a68e`. As those notes explain, its code lives outside Git in `D:\UO\golem`, so there is no implementation commit in code main to compare; reviewed the active implementation named by the notes rather than treating this as an absent change.

Files reviewed:

- `D:\UO\golem\Golems.ps1`: version selection, blob reading, changelog splitting and merging, conflict resolution, and its integration call site.
- `D:\UO\golem\tests\Golem.Tests.ps1`: P213 facts and their fixture setup.
- `D:\UO\golem\README.md:699`: documented P213 behavior.
- `ShatteredLegacy\CHANGELOG.md`: format contract.
- `ShatteredLegacy\server\customizations\ShardVersion.cs:84`: the consumer's parsing rules.

## Findings

1. **bug**, `D:\UO\golem\Golems.ps1:1045` and `:1066`: Comment tracking stops after the first version heading, and merging sorts comment delimiters with ordinary content, so a branch entry containing a commented example with `## 2099.01.01`, `### Added`, and a draft bullet exposes the draft, misclassifies the real bullet, leaves a dangling `<!--` that hides main's entries from the consumer, and makes version selection jump to 2099. Parse comments throughout the file and merge only visible entries, with a regression covering a commented example inside a version section.

2. **risk**, `D:\UO\golem\Golems.ps1:1060` and `:1067`: Duplicate filtering ignores audience, so a new player-facing Added bullet identical to a historical Staff bullet is silently dropped while another new bullet allows the resolution to succeed, leaving the intended announcement visible only to staff. Include audience in duplicate identity and add a case with an old Staff bullet repeated in a new player section.

3. **risk**, `D:\UO\golem\Golems.ps1:1060`: Only dash bullets enter the main-side duplicate table, although the shard consumer accepts star bullets too, so identical `* Shared entry.` bullets on both sides survive twice after merging. Normalize both supported bullet markers before duplicate comparison and test identical star bullets on both sides.

4. **risk**, `D:\UO\golem\tests\Golem.Tests.ps1:2619`: The P213 merge cases add whole new sections but do not exercise the promised additions under existing headings or the unreadable-changelog fallback, so regressions in either path can pass the current suite. Add an existing-section addition case and a malformed-input case that verifies both repositories return to their original state without a merge left in progress.

## Verification

- Ran `powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\Golem.Tests.ps1 -Only P213`: all four version-helper checks passed; the integration fact failed during fixture setup because Git's local push could not create a signal pipe (`Win32 error 5`), before any P213 merge assertions ran. End-to-end merge, commit, push, and rollback behavior remain unverified in this run.
- Ran direct exploratory calls to the existing functions in Windows PowerShell 5.1 without changing them. The comment example produced a new Added section with the hidden draft and real fix, followed by a Fixed section containing a dangling comment opener; `Split-Changelog` plus `Get-NextShardVersion` selected `2099.01.01.2` from that commented heading.
- A second probe used a historical Staff item `- Old entry.` and a branch Added section containing that item plus `- Branch entry.`; only the latter reached the new player section, and the former remained under Staff in main's history.
- A third probe used identical `* Shared entry.` lines on both sides and another branch addition; the merged output contained the shared item twice.
- No backward version result was found for valid versions in the helper checks. The comment case selects an unintended future version; it does not demonstrate a backward version.
- These probes demonstrated current defects; no new test or fix was added, so no red-to-green claim is made. The reported gaps come from reading the existing tests, not from the fixture setup failure.
- Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies; exit 0. It rewrote `tools/progress.json` despite that switch, so restored that generated change; only this review note remains changed. No Haven connection or deployment was made.

P500 DONE
