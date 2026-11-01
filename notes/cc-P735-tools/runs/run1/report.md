# Overnight play tests, run

**1 pass, 0 fail, 0 flaky, 2 could not run** (3 checks, each run 1 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: (unknown)
- World: a copy of the test world's automatic backup ?, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable None, testCenter.skillGainMultiplier None, clusterf.skillGain.amountMultiplier None (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| P64-1 | ERROR | 0/1 | LoginFailed: no character list after the game login (the server closed the connection) | [1](transcripts/P64-1-run1.txt) |  |
| P64-2 | ERROR | 0/1 | RuntimeError: P64-1 did not run first | [1](transcripts/P64-2-run1.txt) |  |
| T-039 | PASS | 1/1 | human female at (3634, 2586, 0): message None; welcome gump says 'The Guild Board in the town square lists every guild, what it teaches, and where its guildmaster stands.'; the board is 1 tiles away | [1](transcripts/T-039-run1.txt) | T-039: a new player can find the board by eye |

## Fail, Flaky and could-not-run, every run

- **P64-1 ERROR** (Fresh account login: bulletin with the current version, All patch notes, no wiki button)
  - run 1 ERROR: LoginFailed: no character list after the game login (the server closed the connection) ([transcript](transcripts/P64-1-run1.txt))
- **P64-2 ERROR** (All patch notes opens the history; a relog shows no bulletin)
  - run 1 ERROR: RuntimeError: P64-1 did not run first ([transcript](transcripts/P64-2-run1.txt))

Real shards before: `{}`

Real shards after: `{}`
