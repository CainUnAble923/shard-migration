# Overnight play tests, 2026-10-14-0817

**1 pass, 0 fail, 0 flaky** (1 checks, each run 3 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: working tree at 10f4088
- World: a copy of the test world's automatic backup 2026-10-14-12-07-26, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable True, testCenter.skillGainMultiplier 5.0, clusterf.skillGain.amountMultiplier 5 (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| T-047 | PASS | 3/3 | countdown 'You will enjoy the benefits and relatively safe status of a young player for another 13 days and 23 hours of play time. Say "I want to grow up!" to give it up sooner.' (days and hours: True); confirm gump: ['', "Renouncing 'Young Player' Status"] | [1](transcripts/T-047-run1.txt) [2](transcripts/T-047-run2.txt) [3](transcripts/T-047-run3.txt) |  |

Real shards before: `{"sl-modernuo": "running 2026-10-14T13:06:06.981602409Z sha256:bc04a35bf344c49b3f7599703b9c135d63730e2e4784b4356ee85b4e9a4df2ef", "sl-modernuo-test": "exited 2026-10-14T12:07:27.991600209Z sha256:178e2bdafef4e502c246296dc42370cf3fc25aae9fcb798d6f2e22f814b47839"}`

Real shards after: `{"sl-modernuo": "running 2026-10-14T13:06:06.981602409Z sha256:bc04a35bf344c49b3f7599703b9c135d63730e2e4784b4356ee85b4e9a4df2ef", "sl-modernuo-test": "exited 2026-10-14T12:07:27.991600209Z sha256:178e2bdafef4e502c246296dc42370cf3fc25aae9fcb798d6f2e22f814b47839"}`
