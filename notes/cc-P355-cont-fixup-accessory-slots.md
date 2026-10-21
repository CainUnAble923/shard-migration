# cc-P355: fix-up for P262 (accessory slots), so it merges into main

## Headlines

- P262's branch merged with current main in both repos. Two conflicts (VERSION, CHANGELOG.md), both resolved
  keeping every line.
- **The red test was not P262's.** It was `CreatureLevelsVerification.BelowPinnedsCapTheUncappedDifficultyIsPinnedsExactly`
  (from P239, already on main), which is flaky: it failed on my second test run with
  `GiantSerpent: 74.38, 76.38 against pinned 74.38`, and passed on the first. Fixed in the test; P262's code is unchanged.
- Green: `docker\uo\build.sh -t sl-modernuo:cc-P355`, **2,000 tests, 1,996 passed, 0 failed, 4 skipped**, both P262
  patches (`AOS-accessory-container-aggregation.patch`, `PlayerMobile-accessory-hooks.patch`) applied. Three
  `--tests-only` runs after the fix were also green.

## How the merge was done

The hand-off put both work copies on `golem/Copper/P355` (at `origin/main`) and says not to switch branches, so I
merged `golem/Copper/P262` into `golem/Copper/P355` instead of checking out P262 and merging main into it. The tree is
the same either way; the Golem commits it on P355.

## Conflicts resolved

| File | Resolution |
|---|---|
| `ShatteredLegacy\VERSION` | main `2026.10.21.10` against P262 `2026.10.21.8`: the higher, `2026.10.21.10` |
| `ShatteredLegacy\CHANGELOG.md` | P262 wrote its lines under `2026.10.21.8`, which main had since used for the Golem test accounts. P262's three Added lines and its Staff line moved under `2026.10.21.10`, alongside main's Staff line there. The `.9` and `.8` sections are main's, unchanged |

shard-migration merged cleanly (P262's notes file only).

## What changed (beyond the merge)

`server\tests\Mobiles\CreatureLevelsVerification.cs`: the test read pinned's `BaseInstrument.GetBaseDifficulty` and our
`UncappedDifficulty` 12 times each and asserted every value of ours was among pinned's. Both roll (a Giant Serpent moves
between 74.38 and 76.38), so twelve reads of pinned sometimes missed a value ours had read. Ours is still read 12
times; pinned is now read at least 12 times and up to 400, stopping once it has seen every value ours gave. A value of
ours that pinned truly never gives still fails after 400 reads.

This is very likely the one failure in the integrator's run of P262 (its log was cut before the failure line; the totals
match: 2,000 tests, 1 failed).

P355 DONE
