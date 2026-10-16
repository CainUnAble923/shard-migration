# Overnight play tests, 2026-10-16-1250

**0 pass, 0 fail, 1 flaky** (1 checks, each run 3 times; 3/3 PASS, 0/3 FAIL, anything else FLAKY).

The bot produces evidence; it never marks a result. Chase marks on the play-test page.

- Code under test: working tree at 773313e
- World: a copy of the test world's automatic backup 2026-10-16-17-50-01, accounts wiped (TestAccountWipe), bot accounts only
- testCenter.enable True, testCenter.skillGainMultiplier 5.0, clusterf.skillGain.amountMultiplier 5 (T-002 and T-031 depend on them)
- Rule 1 (live 2593 and test 2594 untouched): held; both containers' state and start time identical before and after

| Id | Result | Runs passed | Evidence (last run) | Transcript | Left for Chase |
|---|---|---|---|---|---|
| P129-1 | FLAKY | 1/3 | BloodFox: killed True, corpse True; OsseinRam: killed True, corpse True; LeatherWolfFellow: killed True, corpse True; GargishOutcast: killed True, corpse True; ParoxysmusSwampDragon: killed True, corpse True; Drelgor: killed True, corpse True; player hits at the end 176/177 | [1](transcripts/P129-1-run1.txt) [2](transcripts/P129-1-run2.txt) [3](transcripts/P129-1-run3.txt) |  |

## Fail, Flaky and could-not-run, every run

- **P129-1 FLAKY** (Six of cc-P129's ported creatures spawn, fight back and die to a player, leaving a corpse)
  - run 1 FAIL: BloodFox: killed True, corpse True; OsseinRam: killed False, corpse False; LeatherWolfFellow: killed False, corpse False; GargishOutcast: killed False, corpse False; ParoxysmusSwampDragon: killed False, corpse False; Drelgor: killed False, corpse False; player hits at the end 0/176 ([transcript](transcripts/P129-1-run1.txt))
  - run 2 FAIL: BloodFox: killed True, corpse True; OsseinRam: killed False, corpse False; LeatherWolfFellow: killed False, corpse False; GargishOutcast: killed False, corpse False; ParoxysmusSwampDragon: killed False, corpse False; Drelgor: killed False, corpse False; player hits at the end 0/177 ([transcript](transcripts/P129-1-run2.txt))
  - run 3 PASS: BloodFox: killed True, corpse True; OsseinRam: killed True, corpse True; LeatherWolfFellow: killed True, corpse True; GargishOutcast: killed True, corpse True; ParoxysmusSwampDragon: killed True, corpse True; Drelgor: killed True, corpse True; player hits at the end 176/177 ([transcript](transcripts/P129-1-run3.txt))

Real shards before: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-16T10:49:38.914509482Z sha256:f9c8ee2a211894a22902c5d16d4c46005ac4271d3474bafe482dcf52271e64ad"}`

Real shards after: `{"sl-modernuo": "absent", "sl-modernuo-test": "running 2026-10-16T10:49:38.914509482Z sha256:f9c8ee2a211894a22902c5d16d4c46005ac4271d3474bafe482dcf52271e64ad"}`
