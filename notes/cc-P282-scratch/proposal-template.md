## Proposed numbers, 10-21

P282, 2026-10-21: **numbers and recommendations only, no server changes.** Chase's 11:45
answer confirms 21 resets, creation at cap 50, loop 1 cap 100, then +5 to cap 200 at loop 21.
There are 22 cap states, 21 resets and 20 scrolls. The six-loop ladder is replaced above.

### Preserve the later decisions

The read-first notes predate `notes/f12-decisions-2026-10-05.md`. That record approved
P54's S2 config-table curve, x10 level echo ceiling, raw reserve credit from level 1 of
the new loop without echo on the credit, zero reserve after cap 200, and loss of overflow.
**Recommend retaining those decisions.** P282 changes reserve size to the approved five
levels; it does not silently replace S2 or change when the bank is credited. P20's +20%
global loop bonus and the old 25%-of-next-step reserve are not used.

The curve is not a single power constant. Keep P54's construction: exponent 1.5 below 100,
scaled to a 3h opening loop, then solve each +5 block for a target 12.472264969h loop,
never allowing XP-to-next to fall. That target comes from P54's nominal 260h budget;
monotonicity forces the actual total to **334.02h**, not 260h.

| Curve input | Recommended starting value | Status |
| --- | --- | --- |
| Levels 1..99 | 7.7598002866 x L^1.5, normalized to steady loop 0 = 3h | Approved S2 baseline; generated exact values in approved-xp-table.csv |
| Levels 100..104 | S2's monotone bridge to the late flat table | Keeps the first +5 block at the solved target |
| Levels 105..199 | About 102,272.54 raw XP per transition, constant | Never falling, rather than a fresh exponential grind |
| Kill XP | 5 x creature level | P20/P54 modeling assumption; playtest before building |
| Level echo | min(10, 1 + 0.5 x loop), only below prior peak | Decided starting shape, same for Keeper/Breaker |
| Extra global loop bonus | None | New ground uses x1; Keeper's higher skill echo never applies to levels |

P54's unrounded XP values are retained here to reproduce the approved curve. A future
integer config export should floor each transition consistently; this task does not ship
that config. No skill points or stat points are awarded for level or reset.
The approved shape has a sharp bridge at 100: about 7,644 XP for 99->100, then 98,339
for 100->101. Keep it visible during playtest; monotonic does not mean smooth.

### Reserve size and scroll/reset interaction

Proposed precise meaning of the approved five levels: at outgoing cap C,
`Rmax(C) = XP(C->C+1) + ... + XP(C+4->C+5)`, using the configured S2 table.
At C=50 it means 50->55, not five cheap levels after the reset. Terminal cap 200 has
Rmax=0 under the 10-05 decision; there is no scroll to 205.

| Rule | Recommendation | Effect on play |
| --- | --- | --- |
| Scroll steps | One target scroll per reset to 105, 110, ..., 200; no scroll for 50->100 | Exactly 20 scrolls, no independent scroll-only cap increase |
| Before reset | Acquire/trade the scroll and preview the reset; do not consume or apply it early | Preparation is allowed without bypassing the loop |
| Confirmed reset | At current cap, consume the next scroll, increment loop and cap, snapshot old peak and reserve, return level to 1, then apply raw reserve once | One proposed atomic transaction; cancellation spends nothing, no duplicate bank |
| Carry | Reserve survives the reset and pays ordinary level costs starting at 1 | Keeps Chase's 10-05 credit ruling; no echo on the bank itself |
| Partial reserve | Buy whole transitions in order and retain residual XP into the next level | No rounding up to a free level; no loss of partial progress |
| Capped earning | Deposit raw eligible XP up to Rmax; no echo at cap; overflow lost, not converted to currency | Bounded progress during scroll hunting; no promise that all capped play banks forever |
| Full-bank display | One message on filling, at most one reminder per 30min, and Reserve: full on the display | Preserves the 10-05 notification decision |
| Cap 200 / later resets | No reserve, no more power scrolls; later resets keep cap 200 and x10 echo for cosmetics/board only | Does not resurrect the dropped separate 20 post-cap loops |

This is a proposed future transaction, not an implemented persistence guarantee. Live XP
awards crossing the old peak must split there: echo applies only to the portion needed
to finish old ground. Applying bank XP never triggers echo. Skills follow Keeper/Breaker
retention, stats stay, and current level resets for both paths.

**Five levels of XP is not a five-level limit on the credited level jump.** With S2, a
full bank at 50 contains 14,552.78 XP and starts loop 1 at level 29 plus partial XP. At
100 it contains 501,528.78 XP and starts loop 2 at **101 plus 96,668.19 XP toward 102**.
That skips the old peak of 100; it does not fill cap 105. Later full banks start at 102.
Those are consequences of the approved raw-credit rule, not an extra reward proposal.

| Alternative | Result | Recommendation |
| --- | --- | --- |
| Credit raw bank from level 1 | Many cheap opening levels can be skipped; the table below measures how many | Retain the 10-05 decision for the first playtest |
| Hold bank in escrow until old peak | Old ground is always played, but a full bank pays the whole +5 frontier | A change of decision if Chase prefers mandatory replay; not assumed in baseline |
| Discard bank on reset | Makes the bank useless for cap advancement | Reject |

Scroll sources must be reachable before the reset they unlock: the first 105 key from
the existing New Haven mini-champ/paragon/boss route, later keys from already accessible
content or League merging. Never put the only required scroll on its own locked floor.
Drop rates, merge cost and scroll waiting time remain outside this model.

### Approved S2: hours at every cap and the three schedules

Steady = 120 kills/hour at own level. Cautious = 60 kills/hour at 75% of own level,
minimum creature level 1. These are assumptions, not telemetry. Casual/regular/heavy
mean **1/3/6 active XP-earning hours per day**; playing longer grants no XP multiplier.
All times exclude travel, training downtime and waiting for scrolls. Noncombat XP is
not modeled. The 10-05 rulings on skill-point XP and XP for acts rather than currency
turn-ins still stand; omitting them here does not withdraw them.

The main table uses empty banks and includes loop 0 in cumulative hours/days. Old h is
1->previous peak, New h is previous peak->new cap. Daily schedules divide active hours,
without rounding to sessions. approved-loops.csv also has each loop's 1/3/6-day values
and both efficiencies, retaining full precision.

<!-- P282:approved-loops -->

On this baseline, loop 1's current-level climb takes 7.55 steady hours, 10.55 including
creation: earned over 3.52 regular days. Skill cap 100 opens immediately on the first
reset; current level 100 is not required to train GM. Fixed old ground 1->50 drops
from 3h to 2h at loop 1 and 0.30h at x10. Whole loops can still grow as new blocks become
remembered ground; the full late loop is not promised to be shorter than the opening loop.

### Approved S2: level bands

A->B includes transitions A through B-1. Base times apply to new ground; divide hours
and days by the eligible echo for remembered portions. Split at the prior peak, never
accelerate a new portion. Old 195->200 only occurs in cosmetic resets after loop 21.
approved-bands.csv includes every reachable band at every loop, both efficiencies and
all three day schedules; the x10 column below illustrates remembered versions of each band.

<!-- P282:approved-bands -->

### Approved S2: full five-level banks, including the cost to fill

The fill time was spent at the previous cap with no echo and is charged to the arriving
loop before its reset. After-credit h starts after the bank has been applied, including
any residual partial XP. The table does not count stored XP as free playtime. The final
row stops at 200 with no outgoing bank. Cap rows use current level, not just owning that cap.

<!-- P282:approved-reserves -->

<!-- P282:approved-sensitivity -->

Full banks take longer end-to-end here: 406.44 versus 334.02 steady hours. Spending raw
bank XP on old levels replaces XP that otherwise would have earned echo, and banking
is done at the prior cap's XP rate. Its purpose is credit for scroll-hunting time already
spent, not a speed bonus. A cautious 1h/day player still takes 7.99 days to 50 and 28.13
to 100 without reserve. These estimates do not prove that the chosen content supports
the assumed kills/hour or that crafting/gathering levels at the same pace.

### Comparison: a single power curve and escrow

P282 also reruns the originally requested P20 shape on the corrected ladder, removing
its old global bonus and using the decided echo. Coefficient choices at steady efficiency,
empty banks:

<!-- P282:coefficients -->

C=24 gives 32.64h to 100 and 239.65h to 200, but its opening 9.28h (24.71h cautious)
misses the later approved 3h/8h opening target. **Do not replace approved S2 with it.**
`tables.md`, loops.csv and bands.csv retain the full all-loop comparison. Its reserve.csv
models the escrow alternative explicitly: a full bank pays the next +5 only after the
old peak, taking 240.38h including filling versus 239.65h empty. The 160 content-ceiling
sensitivity in tables.md clips creature level only, holding kill rate constant. It is a
comparison of XP supply, not proof of suitable content or a new rule to cap player level.

### What current level unlocks

Proposed extra requirements on **our custom combat content**, alongside existing rank,
chapter and job prerequisites. No requirements on OSI items/quests/maps/public dungeon
entrances, no stat gate, and no current-level restriction on pet/stable/bank capacity.
Basic gather/craft/delivery work keeps its normal skill/rank requirements. Permanent
League rank, AP shop ownership, achievements and collection progress survive resets.

| Current level | Custom access | What it does for play |
| --- | --- | --- |
| 1 | Starter practice/outer dungeon band, basic League work, newbie Tier 1 set wearable immediately | Useful reset floor and a route into progression |
| 25 | League combat contract T1, shallow dives, middle dungeon band | Adds objectives before the first cap |
| 50 | Combat T2, standard dives, starter dungeon's deepest band/mini-champ | A finish for loop 0 and a reachable first scroll source |
| 75 | Combat T3 and veteran dives in custom annexes | A destination during the 50->100 climb |
| 100 | Combat T4, elite dives; The Setting subject to its loop gate | A replay milestone before later frontiers |
| 125 / 150 / 175 | Combat T5 / T6 / T7 with corresponding deep-dive variants | Milestones beyond GM without excluding earlier jobs |
| 200, loop 21, epilogue complete | Capstone encounter/replay and the Unbroken title | A visible finish with no stat or skill points |

For **The Setting**, preserve the decided loop gate: floor N needs loop >= N+1, N=1..20.
Add current level >= `95 + 5*N`: floor 1 needs loop 2/current 100; floor 20 needs loop
21/current 195, with epilogue completion at current 200. A reserve can satisfy current
level normally, just as ordinary XP can. Check each entering party member and recheck
entry on recall/login, placing an ineligible returning character at the safe entrance.
Keep accepted dive progress through reset; resume once eligible or abandon voluntarily.
Never use the next inaccessible floor as the only source of its needed scroll.

| First current-level milestone | Proposed permanent title | Purpose |
| --- | --- | --- |
| 25 | First Light | First visible accomplishment |
| 50 | Wayfarer | Completion of the opening climb |
| 75 | Delver | Progress toward the first major level goal |
| 100 | Seasoned Delver | Recognizable major milestone |
| 125 | Deepwalker | Identity across the +5 loops |
| 150 | Riftwalker | Mid-ladder milestone |
| 175 | Legacy Seeker | Capstone approach |
| 200 + loop 21 epilogue | the Unbroken | Uses the already decided story title |

These are earned through current level and kept after reset. Show current level and
loop separately so an earned title is not mistaken for current entry eligibility.
Loop-count prestige titles and hues remain separate; reset does not revoke identity.

| Reward | Recommendation | Purpose |
| --- | --- | --- |
| Renown per level | +2 per previously unrewarded level 2..200, **once per account**, no AP | Small League spending reward without echo/alternate-character/deletion farming |
| Budget | 98 by 50, 198 by 100, 298 by 150, **398 total by 200** | Modest beside source-default Bronze's 2,500 requirement; does not replace jobs/trials/standing |
| Cosmetics | At 50/100/150/200, persistent selectable display border/badge using existing UI assets/colors | Visible milestones, no item properties, duplicate currency or new art |

Durable account claims survive character deletion/reset. Levels credited from reserve
count once, creation at 1 pays zero, repeated/post-cap levels pay zero. Earned Renown
adds to spendable and LifetimeRenown under the existing policy, gives no AP, stats,
skill points, luck or follower slots. The 398 is a new award budget, not an unverified
count of current achievement payouts. Titles and cosmetics are permanent earned choices;
custom combat eligibility is the part current level must re-earn.

### For Chase

- **Settled:** 21-reset ladder, 20 +5 scrolls, five-level reserve, no free skill/stat
  points. Keep 10-05's S2 and raw reserve credit at level 1; no new approval needed
  for those. Confirm the exact five-level valuation and atomic scroll/reset proposal.
- **Keep the S2 starting constants.** First cap 3h steady/8h cautious; creation to 100
  10.55/28.13h. Empty-bank route to 200 is 334.02h steady, or **334.02 / 111.34 / 55.67
  days** at 1/3/6h daily. Scroll waits and noncombat budgets still need playtesting.
- **Five levels of XP can skip many opening levels.** Approved credit starts loop 2
  at 101 with a full bank. Escrow would guarantee replay but fund the whole +5 new
  band; choose it only as an explicit change of the 10-05 credit decision.
- **Use current level for the custom combat/dive/depth gates; keep milestone titles
  and cosmetics after reset.** The Setting keeps both loop and current-level gates.
- **+2 Renown once per account per new level, 398 maximum, no AP.** No repeat currency
  from echo or post-cap resets; no stat/skill-point awards.

Reproduce approved tables with `python -B notes/cc-P282-scratch/approved_baseline.py`;
power/escrow comparisons with `python -B notes/cc-P282-scratch/xp_curve.py`;
numerical checks with `python -B notes/cc-P282-scratch/verify_curve.py`.
This section is assembled from proposal-template.md and the generated tables by
`python -B notes/cc-P282-scratch/assemble.py`. P282's report records validation and
limits. Historical skill/stat claims above retain their dates; this task does not
re-audit them or imply they still describe the current implementation.
