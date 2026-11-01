# Overnight play tests, run

**3 pass, 0 fail, 0 flaky** (3 checks, each run 1 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: (unknown)
- World: a copy of the test world's automatic backup ?, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable None, testCenter.skillGainMultiplier None, clusterf.skillGain.amountMultiplier None (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| P64-1 | PASS | 1/1 | title 'Shattered Legacy 2026.10.31.5'; All patch notes button yes; wiki text none | [1](transcripts/P64-1-run1.txt) |  |
| P64-2 | PASS | 1/1 | history gump after All patch notes: yes; bulletin on relog: none (observed during the matching P64-1 run) | [1](transcripts/P64-2-run1.txt) |  |
| T-039 | PASS | 1/1 | human female at (3634, 2586, 0): message None; welcome gump says 'The Guild Board in the town square lists every guild, what it teaches, and where its guildmaster stands.'; the board is 1 tiles away | [1](transcripts/T-039-run1.txt) | T-039: a new player can find the board by eye |

Real shards before: `{}`

Real shards after: `{}`
