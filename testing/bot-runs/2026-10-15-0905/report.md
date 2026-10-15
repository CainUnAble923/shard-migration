# Overnight play tests, 2026-10-15-0905

**2 pass, 0 fail, 0 flaky** (2 checks, each run 3 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: working tree at fe7e11b
- World: a copy of the test world's automatic backup 2026-10-15-14-05-01, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable True, testCenter.skillGainMultiplier 5.0, clusterf.skillGain.amountMultiplier 5 (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| P64-1 | PASS | 3/3 | title 'Shattered Legacy 2026.10.15.3'; All patch notes button yes; wiki text none | [1](transcripts/P64-1-run1.txt) [2](transcripts/P64-1-run2.txt) [3](transcripts/P64-1-run3.txt) |  |
| P64-2 | PASS | 3/3 | history gump after All patch notes: yes; bulletin on relog: none (observed during the matching P64-1 run) | [1](transcripts/P64-2-run1.txt) [2](transcripts/P64-2-run2.txt) [3](transcripts/P64-2-run3.txt) |  |

Real shards before: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-15T01:03:09.9003719Z sha256:918d37609f17fc0a63bfc3be68b5be668729ce1b09675dfb18c31b3cfbf5401b"}`

Real shards after: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-15T01:03:09.9003719Z sha256:918d37609f17fc0a63bfc3be68b5be668729ce1b09675dfb18c31b3cfbf5401b"}`
