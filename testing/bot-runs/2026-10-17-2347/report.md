# Overnight play tests, 2026-10-17-2347

**1 pass, 0 fail, 0 flaky** (1 checks, each run 2 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: working tree at 75f0238
- World: a copy of the test world's automatic backup 2026-10-18-04-45-00, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable True, testCenter.skillGainMultiplier 5.0, clusterf.skillGain.amountMultiplier 5 (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| P139-1 | PASS | 2/2 | BurrowScampSlingerBodyTest: killed True, corpse True; player hits at the end 166/176 | [1](transcripts/P139-1-run1.txt) [2](transcripts/P139-1-run2.txt) |  |

Real shards before: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-17T16:53:00.312451183Z sha256:8e1a1916a7520a854b10e054d3fd8039b05b1a969bbef90a7ff35bdb977d669d"}`

Real shards after: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-17T16:53:00.312451183Z sha256:8e1a1916a7520a854b10e054d3fd8039b05b1a969bbef90a7ff35bdb977d669d"}`
