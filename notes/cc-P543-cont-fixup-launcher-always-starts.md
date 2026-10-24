# CC task P543: fix-up for P411 (the launcher must always start the game): its docs did not merge

**Golem:** Iron. **Date:** 2026-10-24. **Branch:** `golem/Iron/P543` in both work copies.

## In plain words

- The launcher fix from P411 is already in main: the integrator pushed the code (`0de0d9e`) before it stopped.
- What was left out is P411's write-up, two notes files. They are now on this branch and merge cleanly.
- The stop was not about P411. The overnight bot's log (`soak.txt`, 10.2 MB) sat uncommitted in the integrator's
  copy, and that is over the public repos' 5 MB limit.
- Nothing for you to do.

## What changed

- **shard-migration:** I added `notes/cc-P411-launcher-always-starts.md` and
  `notes/cc-P411-launcher-always-starts-codex-review.md`. They are taken from `golem/Iron/P411` (`d14200e`) and staged.
  The hand-off says not to switch branches, so I checked out only these two files onto `golem/Iron/P543`, which
  already starts at main. That gives the same result as merging main into P411. There were no conflicts: P411 changed
  only these two files.
- **ShatteredLegacy:** nothing to do. `golem/Iron/P543` is at `0de0d9e`, main's merge of P411. Main changed nothing
  under `player-package/` after P411's commit (`git diff bd6118b 0de0d9e -- player-package` is empty). There are no
  CHANGELOG or VERSION conflicts to settle.

## Tests

These are the gates P411 ran, run again on the merged code under the package lock. The exit code is the number of
failed facts.

| Gate | Result |
|---|---|
| Build-UoOverrides | 23 passed, exit 0 |
| Cliloc-Overrides | 10 passed, exit 0 |
| Launch-Overrides | 8 passed, exit 0 |
| Launch-Settings | 27 passed, exit 0 |
| Map-Overrides | exit 0 |
| Music-Overrides | 7 passed, exit 0 |
| Legion-Scripts | exit 0 |
| Paperdoll-Bodies | 9 of 9 passed, exit 0 |
| Ui-Skins | 4 passed, exit 0 |

Nothing under `server\` or `docker\uo\` changed, so there was no image build.

## The refused file

`testing/bot-runs/2026-10-24-0130/transcripts/soak.txt` is committed on main as an empty file, and my copy matches.
The 10.2 MB copy exists only in the integrator's own working tree. If it is still there when the integrator merges
again, the same refusal comes back. Emptying it there, or running `git checkout --` on it, clears that. That copy is
another desk, so I did not touch it.

P543 DONE
