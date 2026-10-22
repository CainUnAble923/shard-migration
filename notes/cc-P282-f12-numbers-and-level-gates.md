# P282: F-12 numbers and current-level gates

2026-10-21. Notes/research only. The requested proposal is in
[f12-levels-loops-caps.md](f12-levels-loops-caps.md#proposed-numbers-10-21).
No shard code, configuration or world data changed. No Haven connection, deployment,
image build, account operation, commit, merge, push or branch switch.

The first pass paused at the Golem's usage-window STOP-REQUESTED file after source
reading. Resumed in the same session when the Golem cleared it. That earlier checkpoint
is superseded by this completed-work report; the final status is written only after
the final artifact review.

## Result

- Replaced the obsolete six-loop ladder throughout the F-12 note with creation/loop 0
  cap 50, loop 1 cap 100, then +5 through loop 21 cap 200. The generated loop tables
  enumerate every state. Exactly 20 target scrolls, 105 through 200 in steps of five;
  the first reset needs none. There are 21 resets and 22 cap states.
- Set the reserve size to the approved XP for five levels. Proposed exact valuation
  is the sum of five outgoing-cap transitions C->C+5, with zero at terminal 200.
  One scroll and one reset advance together; acquisition/preview can happen before
  reset, consumption/cap change only in the confirmed at-cap reset transaction.
- Read the later 10-05 ruling identified by the progress report: **S2 curve and raw
  bank credit from level 1 were already approved**. Preserved those decisions in the
  recommendation. C=24/P20 power and old-peak escrow are explicitly comparisons,
  not silent replacements of Chase's decisions. The older 25-percent reserve is
  superseded by P282's five-level instruction.
- Generated all-loop, all-reachable-band tables for steady and cautious throughput,
  with casual 1h/day, regular 3h/day and heavy 6h/day conversions. Main rows use empty
  reserve; full-bank rows include the prior cap's time to fill the bank. Alternatives
  include coefficient comparison, escrow carry and content level capped at 160.
- Added short current-level contract/dive/depth, title, cosmetic and Renown proposals.
  The Setting keeps its loop gate and adds a current-level gate; key sources remain
  reachable before the reset they unlock. No free stat or skill points. Tier 1 newbie
  gear remains immediately wearable after reset and OSI content receives no new gate.
- Recommended +2 Renown for each new account-level claim 2..200, maximum 398, no AP.
  Claims survive reset/deletion; repeated echo levels and alternate characters cannot
  farm the same claim. Titles and existing-asset UI cosmetics remain earned choices.

## Numbers to take to Chase

| Model / reserve | Creation to current 100, steady h | To current 200, steady h | Days to 200 at 1h / 3h / 6h daily |
| --- | --- | --- | --- |
| Approved S2, empty | 10.55 | 334.02 | 334.02 / 111.34 / 55.67 |
| Approved S2, full banks including filling | 10.13 | 406.44 | 406.44 / 135.48 / 67.74 |
| P20 shape C=24, empty, comparison | 32.64 | 239.65 | 239.65 / 79.88 / 39.94 |
| P20 shape C=24, full old-peak escrow including filling, comparison | 32.70 | 240.38 | 240.38 / 80.13 / 40.06 |

Approved S2's opening takes 3 steady hours or 7.99 cautious hours. Cautious empty-bank
creation-to-100 is 28.13h and to-200 is 890.67h. The latter is 296.89 days at 3h/day.
The sharp XP bridge at current level 100 is made explicit for playtest.

**Reserve consequence:** five expensive cap levels of XP can buy many cheap starting
levels. Under approved S2/raw credit, a full cap-100 bank starts loop 2 at 101 plus
96,668.19 XP toward 102. It does not reach 105. The escrow alternative guarantees the
old-ground re-climb but funds the whole next +5 after that re-climb. Retain approved
raw credit unless Chase explicitly changes that ruling; do not claim both properties
at once. Counting the fill cost prevents presenting a bank as free playtime.

Keep S2's starting inputs: exponent 1.5 before 100, early coefficient 7.7598002866,
3h steady opening target, nominal 12.472264969h late-loop construction target subject
to nondecreasing XP, late flat XP 102,272.535 from 105, kill XP 5 x creature level,
base echo min(10, 1 + 0.5 x loop). The actual total is 334.02h, not the nominal 260h
used in P54's solver. Keeper's higher skill echo does not apply to level XP.

## Deliverables and reproduction

All scratch files are under `notes/cc-P282-scratch/`:

| File | Purpose |
| --- | --- |
| approved_baseline.py | Imports P54's solver read-only; recalculates approved S2 with P282's five-level reserve |
| approved-tables.md | Approved curve, band and full-bank tables for review |
| approved-loops.csv | Every loop, both efficiencies, old/new hours, all day schedules, bank credit/fill cost |
| approved-bands.csv | Every reachable band in every loop/style, with hours and 1/3/6h-day conversions |
| approved-xp-table.csv | Unrounded S2 transition costs and cumulative XP |
| xp_curve.py | P20 adaptation: corrected ladder/echo, C=20/24/30/40 comparison, escrow and content-ceiling sensitivity |
| tables.md | Readable comparison tables |
| loops.csv | Comparison loop/schedule values at full precision |
| bands.csv | Comparison band/schedule values at full precision |
| reserve.csv | Comparison full escrow banks, including fill cost |
| coefficients.csv | Power coefficient comparisons |
| verify_curve.py | Numerical checks for the primary baseline and comparison model |
| proposal-template.md | Authored proposal fragment with table insertion points |
| assemble.py | Reassembles the Proposed numbers, 10-21 section from the fragment and generated tables |

From the migration work-copy root:

```text
python -B notes/cc-P282-scratch/xp_curve.py
python -B notes/cc-P282-scratch/approved_baseline.py
python -B notes/cc-P282-scratch/assemble.py
python -B notes/cc-P282-scratch/verify_curve.py
```

The F-12 note contains the approved all-loop/band/full-bank tables, a power-coefficient
comparison and the requested **For Chase** list. The fuller comparison tables stay in
scratch, distinctly labeled. S2 retains P54 floating precision for reproducibility;
future integer config export is not implemented here.

## Evidence and limits

- Read AGENTS.md in both work copies first, followed by the migration direction,
  governing-doc index and task list. Migration `docs/` was only read.
- Read `notes/f12-levels-loops-caps.md` in full; F-12 and relevant F-24 in
  `docs/feature-queue.md`; P20's overview, curve, ranked list and contradictions;
  `notes/cc-P20-scratch/xp_curve.py`; later `notes/f12-decisions-2026-10-05.md`,
  P54 Part A and `notes/cc-P54-scratch/xp_ladder.py` for the approved curve.
- Read current canonical `ShatteredLegacy/server/customizations/ClusterFAccountData.cs`
  lines 9-43 and 648-680: Renown is account-wide; GrantRenown adds spendable and
  LifetimeRenown except for Commission; spending does not reduce LifetimeRenown.
- Read current `ShatteredLegacy/server/customizations/ClusterFLeagueRanks.cs:485-505`
  for source-default thresholds, notably Bronze 2,500. Did not inspect or change live
  League config. This is source-default context, not a live-config assertion.
- The model assumes 120 kills/h at own level (steady), or 60/h at 75% of own level,
  minimum creature level 1 (cautious). Actual throughput, solo survivability, scroll
  acquisition, training/travel downtime and noncombat XP parity are **unverified**.
  The 10-05 XP-source rulings remain in force; their omission from this combat model
  does not remove them. Neither model is measured gameplay or a server implementation.
- Historical skill/stat coverage claims in the old note were not re-audited for this
  numerical task. Later P54 itself corrects some P20-era skill findings. Their original
  citations/dates remain; this task does not present them as newly verified counts.
- No art request: the cosmetic proposal uses existing UI assets/colors and needs no
  new art production. No plugin/skill or external service was needed.

## Validation

- Windows PowerShell **5.1.26100.9444**, Python **3.12.10**. No pwsh, no PowerShell 7
  syntax. `rg` was unavailable; used PowerShell searches. Commands above run locally.
- First copied P20's original script into P282 scratch, then ran the first eight
  numerical checks **before replacing it**: exit 1, three assertion failures and five
  missing-new-API errors. The wrong ladder, coefficient and initial timing were among
  the observed failures. After adaptation, all eight passed.
- Added two checks for approved S2 pace/monotonicity and five-level raw bank credit.
  Their first execution used a deliberately broken scratch baseline: six-hour opening
  and a four-transition bank. Both tests failed (exit 1). Restored the correct baseline
  in a finally block, then all **ten** checks passed. No mutation reached the generated
  tables or old P54 source. These are research checks, not server/lane tests.
- Independently audited the approved CSV band sums against per-loop totals, cumulative
  arithmetic, 1/3/6-day conversions and no bank remainder past any cap. The audit passed.
  Direct P54 model recomputation gave 334.0182844423687h, matching the exported baseline.
- Required `tools/progress.py` completed successfully with SL_SHARD and SL_MIGRATE
  pointing at these work copies and SL_SERVUO at the read-only source. README.md,
  dashboard.html and tools/progress.json refreshed; expansion coverage ran successfully
  without a content diff. The refreshed queue data are tool-derived, not a P282 queue edit.
  No generated artifact was published and no Haven service was contacted.

- Final regeneration of both models and the assembled F-12 section was byte-identical
  on a second pass. All ten numerical checks passed on the final scripts.
- Final `git diff --check` passed. Changed paths are the F-12 notes, this report,
  the enumerated scratch artifacts, and the required local progress outputs
  README.md, dashboard.html and tools/progress.json. No migration docs/ edits;
  ShatteredLegacy remains clean. Every created/modified file is below 5 MB;
  the largest scratch artifact is bands.csv at 63,786 bytes.
- Lane tests: none, as requested. No server build was needed for notes and standalone
  numerical research scripts. All requested deliverables are present.

P282 DONE
