# P213: the merger resolves CHANGELOG.md and VERSION conflicts itself

## Headlines

- When a merge's **only** conflicts are in `CHANGELOG.md` and/or `VERSION` (in either repo), Shadow Iron settles them
  inside the merge. It no longer aborts and writes a fix-up for them.
- **Any other conflicting file** still means: abort both repos, one fix-up named after the original prompt (P208's
  rule). Nothing is left half merged.
- After the two files are settled, the merge continues as usual: the build when the server changed, then the merge
  commit through `Commit-ShardWork.ps1 -Merge`, then the push.
- This is live already. `D:\UO\golem` is not a repo, so Shadow Iron's next round uses it (P209, Bronze's P193 fix-up,
  is the next merge that will meet it).

## How the two files are merged

- **CHANGELOG.md**:
  - Main's file stays exactly as it is.
  - Above main's newest entry goes **one new entry** holding what the branch added since the merge base. That covers
    whole new sections, and items the branch added under an existing heading.
  - The entry's lists go in the file's order: Added, Changed, Fixed, Staff, then any other.
  - Nothing of main's is dropped or rewritten. An item already present in main's file is not copied twice. The
    header and its `<!-- -->` comment (which contains an example heading) are untouched.
- **VERSION** and the new entry's heading get the **next version**, later than both sides.
  - The prompt asked for "the existing helper", but there is none. `Commit-ShardWork.ps1` never writes VERSION; the
    agents write it by hand. The only rule is CHANGELOG.md's own header: the date (`2026.09.30`), and a second update
    the same day is `.2`, then `.3`.
  - `Get-NextShardVersion` implements exactly that rule, once. It uses today's date unless a side is already later,
    and takes one past the highest number on that date across main's VERSION, the branch's VERSION and every heading
    on both sides.
- If the branch's CHANGELOG.md changes cannot be read as entries, or anything is still unmerged after writing, the
  resolution reports why. The merge is then aborted and a fix-up is written as before.
- Blobs are read as raw UTF-8 through `git cat-file`, because a PowerShell pipe re-decodes text in the console's code
  page. The files are written as UTF-8 without a BOM, with main's line endings.

## Files

Backups `*.bak-20261020-P213`.

- `D:\UO\golem\Golems.ps1`:
  - Invoke-Integrate's conflict branch now calls `Resolve-NotesConflict`.
  - New functions: `Get-NextShardVersion`, `Get-GitBlobText`, `Split-Changelog`, `Merge-ChangelogText`,
    `Resolve-NotesConflict`.
- `D:\UO\golem\tests\Golem.Tests.ps1`: two new facts, 16 checks, green.
  - `P213_TheNextVersionIsLaterThanBothSides`: same day, a plain date, an older day, a side already ahead.
  - `P213_CHANGELOGAndVERSIONConflictsAreSettledAndAnyOtherConflictIsStillAFixUp`, four real merges through Shadow
    Iron's round on fake repos:
    - CHANGELOG-only: both entries kept, the branch's on top under `.2`.
    - VERSION-only: the entry carries the new version, not the branch's.
    - Both files: newer than both sides; main's entries kept once; committed, pushed and clean.
    - Both files plus a README conflict: a fix-up; main, VERSION and the tree untouched; no MERGE_HEAD.
- `D:\UO\golem\README.md`: a CHANGELOG.md and VERSION paragraph in "Shadow Iron merges".
- Regression runs:
  - `P208_*`: 52 of 52 pass.
  - `P184_*`: 102 pass, 5 fail. The two facts behind those 5 checks (overlapping Touches, Touches/git queue) fail the
    same way on the pre-P208 code. They predate the overseer's parallel `server` area today.

## Item 5 (optional): the merger stamping VERSION: not done

Golem branches still bump VERSION. Stopping that would mean changing the instructions every agent follows (AGENTS.md
and the CHANGELOG.md header say "the newest section's version also goes in VERSION"). It would also leave a
branch's test-shard image without a version heading for its own notes. Neither change is small. With this prompt the
bump no longer costs a fix-up anyway: the merger replaces the branch's version with a fresh one at merge time.

## For Chase

Nothing to do. If a merged entry ever looks wrong, it is one new section at the top of CHANGELOG.md and easy to edit by
hand.

P213 DONE
