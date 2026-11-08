# Overnight play tests, 2026-10-20-2315

**1 pass, 0 fail, 0 flaky** (1 checks, each run 1 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: working tree at 83b1f97
- World: a copy of the test world's automatic backup 2026-10-21-04-15-01, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable True, testCenter.skillGainMultiplier 5.0, clusterf.skillGain.amountMultiplier 5 (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| CREATE | PASS | 1/1 | human male: body 400 (want 400), status name 'Bot Human M Ab' (asked for 'Bot Human M Ab'), at (3503, 2574, 14) | [1](transcripts/CREATE-run1.txt) |  |

Real shards before: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-21T03:04:00.675443404Z sha256:29ba19793cab6e20a90a5b9d5c6455710aaa1c3b4816d0d0b5bb4b313f9ce039"}`

Real shards after: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-21T03:04:00.675443404Z sha256:29ba19793cab6e20a90a5b9d5c6455710aaa1c3b4816d0d0b5bb4b313f9ce039"}`
