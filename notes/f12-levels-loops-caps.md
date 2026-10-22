# F-12 revised: levels, loops and caps (ladder corrected and numbers proposed 2026-10-21)

**Current rulings:** Chase's 2026-10-03 ladder, reconfirmed 2026-10-21 11:45: 50 at creation,
100 after the first reset, then +5 per loop to 200 at loop 21 (20 scrolls).
**Reserve: XP for 5 levels, approved in P282.** This replaces the queue's older 25-percent reserve.
See "Proposed numbers, 10-21" below for the numerical proposal and the reserve interaction.
The 2026-10-05 decisions also approve P54's S2 curve and raw reserve credit from level 1,
without multiplying the credit by echo. P282 preserves those as the baseline and compares
alternatives explicitly. Current-level rewards below remain proposals, not implemented behavior.

Written 2026-10-01 by the overseer from Chase's decisions in one sitting, against cc-P20's research
(`notes\cc-P20-skill-scaling-research.md`, 236 KB). **This supersedes the max level 1000 design and the
example loop ladder in the F-12 and F-13 entries of `docs\feature-queue.md`.** Where this doc and the
queue entries disagree, this doc governs until the entries are rewritten.

## Why it changed

cc-P20 read all 58 skills one at a time. Storage allows 1000 (skills are ushort tenths, ceiling 6553.5,
`Server/Skills.cs:89-90`), but the game rules do not: **41 of 58 skills break by 1000, and 20 break at
or below 300**, which is the live cap today. Separately, **39 of 58 skills cannot gain past about 160
by play at all**, because each use carries a fixed `maxSkill` above which the check succeeds with no
gain roll (`UOContent/Skills/SkillCheck.cs:58-61`). So a high cap was buying nothing it could reach.

Chase lowered the ceiling to 200. Counted against P20's per-skill table, that removes all 21 skills
whose only breaks are in the 500 and 1000 columns, and defuses both breaks that can hard-fail: the
Discordance divide by zero in the swing timer (needs a -100 effect, which needs 300) and Parry's 100
percent shield block (needs 380). Feint's guaranteed no-damage needs 237 and is also out of reach.

It also matches what the engine already does: **`CharacterCreation.cs:437` rejects any starting skill
above 50**, which is exactly the loop-0 cap, so no character can ever be created above its own cap.

## The model

- **Individual skill cap = max level.** One number per character.
- **Total skill cap = 58 x max level.** Every skill is maxable on one character; this was already the
  recorded F-12 intent and Chase reconfirmed it 2026-10-01. Character identity comes from stats, loop
  progress and titles, not from choosing which skills to train.
- **Current level** climbs within a loop and resets to 1 on reset.
- **Max level ladder:** loop 0 starts at 50; loop 1 at 100; loops 2 through 21 at
  `100 + 5 * (loop - 1)`, ending at 200. Twenty-two cap states, 21 resets, 20 scroll-gated steps.
- **Every reset returns current level to 1**, for Keeper and Breaker alike. Max level rises on this
  ladder. Skill retention follows the later Keeper/Breaker decision in F-12's 2026-10-03 "Ladder
  and reserve": Breaker retains more skills per loop; Keeper gets faster below-peak skill gain.
  A universal skill wipe is no longer the rule. Neither path gets free skill or stat points.
- **Echo XP** on levels the character already reached in an earlier loop accelerates to its
  configured ceiling, making a fixed band of old ground cheaper while new levels use base XP.
- **Power scrolls raise the level cap, not individual skill caps.** They gate every step above 100.
  The first reset unlocks 100 without a scroll. Targets 105, 110, 115, ..., 200 each need one
  scroll paired with one reset; there is no separate scroll-only cap increase.
- **At max level, XP banks into a five-level reserve.** The 10-05 ruling credits it as raw XP
  from level 1 after reset, without echo on the credit. A bank valued at five expensive cap levels
  can buy many cheap opening levels; the tables below show this. Releasing only at the old peak
  is an alternative, not the approved rule.
- **Scroll drops:** champion spawns, paragons and bosses, with the New Haven dungeon's mini champ as
  the first source. This ties the dungeon into progression rather than leaving it a side trip.

## Loop memory: skill and level gain speed (Chase, 2026-10-02, 11:03)

Live only; the test shard keeps its fast test rates during playtesting.

- **Base rate on live: "fast but not crazy fast".** Not test-center speed (today's test shard runs the Test Center
  x5 multiplier plus ClusterF's 3 attempts and x5 amount). The number is set by **playtesting what feels good**.
- **Loop memory: below a skill's previous peak, gain is faster, and the speed-up grows each loop.** "You remember what
  you learned." Above the previous peak, gain is the plain live base rate ("just fast").
- **Starting shape decided 2026-10-03, still subject to playtest:** base echo
  `min(10, 1 + 0.5 * loop)`: x1.5 at loop 1, x3 at loop 4, x6 at loop 10, x10 from loop 18.
  Keeper's higher skill-only echo runs from x1.5 at loop 1 to x50 at loop 21, never below base echo.
- **Level XP uses base echo for everyone.** Only transitions below the previous attained peak
  are accelerated; at the old peak the next transition is new ground and uses base XP. There is
  no extra global +20-percent loop bonus from P20's obsolete curve. Keeper's x50 is not a level-XP multiplier.
- **Shown somewhere, not on every gain** (Chase, 11:03): the player can look it up on the paperdoll or another stat
  display (Chase, 11:04; overseer adds a line at reset), but skill-gain messages stay as they are.
- Does not fix the cc-P20 limit: 39 of 58 skills cannot gain past about 160 by use (fixed `maxSkill`,
  `SkillCheck.cs:58-61`). F-12 still needs a gain path for those (as F-26 plans for Arms Lore).

## Stats (rewritten 2026-10-02: no ceilings)

**Superseded:** the 2026-10-01 table (per-stat 125 to 200 by max level, total 325 to 550, veteran +50) and the
stat-lock plan are withdrawn. cc-P25 surveyed stats past 125 (`notes\cc-P25-stats-above-125-research.md`) and
Chase decided on its findings (`notes\p25-decisions-2026-10-02.md`). Register row: D-101 and D-102.

- **No ceilings of any kind.** No per-stat table, no effective clamp, no total cap, no soft caps inside formulas.
  Reason (Chase): players will face world bosses and champion spawns solo or in small parties.
- **Raw stats gain to the one global `stats.statMax`, which is 500 in both configs** and has been since May 2026
  (`docker\uo\SERVER.md:642`). Every note before cc-P25, this one included, assumed 125.
- **Effective stats are not clamped.** F-12 removes the `Math.Min` in `patches\PlayerMobile-individual-stat-cap.patch`
  (or sets `clusterf.statCaps.individualCap` very high). `Mobile.cs:1868`'s 65000 is the only bound left.
- **A reset keeps stats.** Pinned already never lowers raw stats when `StatCap` drops (`SkillCheck.cs:313-333`).
- **Carry weight stays uncapped** (`100 + 3.5 x Str`, `customizations\ClusterFBackpack.cs:33-42`).
- **Self-bandage keeps pinned's formula** (1.0 s at Dex 200, instant from effective Dex 220). **Pets gain to the same
  cap as players.**

**What this removes from the F-12 build:** the 0x1A stat-lock handler (`arch-f12-stat-lock-verdict-2026-10-01.md`),
the per-level total in `ClusterFStatCaps.Apply`, the `StatCapScroll` retune and the veteran +50.

**Still to do, because they are defects, not ceilings:**
- **D44**, the talisman and quiver stat-bonus leak (`AOS.cs:598` vs `:620`), now unbounded. Fact first, fix if red.
- **D45**, meditation's start chance inverts as Int rises (ours `Meditation.cs:83`).

**Consequences accepted:** stock bosses and champions were balanced for OSI players (about 150 effective, 150 HP)
and will be much easier. F-14's level field on our own creatures is where bosses scale to these players. Thrown
range passes the 18-tile update range from effective Str about 300 (cc-P25 decisions, fact 3).

## What each counter gates

Three counters, and putting a thing on the wrong one is how loop systems turn frustrating.

**Current level** resets every loop, so it gates what should be re-earned:
- ~~Total stat cap~~ **withdrawn 2026-10-02** (no stat ceilings; stats carry through a reset). A reset now
  costs level and the path-specific skill re-climb, so a reset character keeps full stats. The
  proposed current-level content gates below give the level re-climb a job of its own.
- **Level requirements on our gear only**, never on OSI items (the standing F-12 fidelity rule).
  **Exception, Chase 2026-10-01: the newbie dungeon's Tier 1 set carries no level requirement**, so it
  is wearable the moment a character resets. With the set blessed, no-trade and re-obtainable from the
  repeatable quest, Tier 1 is the guaranteed floor of every loop.
- Dungeon floor depth, so the dungeon is loop content rather than cleared once.

**Max level** only ever rises, so it gates permanent capability:
- Individual skill cap, and the total skill cap at 58 x max level.
- **Pet and stable slots (Chase, 2026-10-01).** Deliberately not current level: stabled pets would be
  stranded behind a shrinking slot count on every reset.
- Bank space (F-19's base of 1,000), extended ore access, housing and vendor slots.

**Loop count** only ever rises, so it gates prestige and identity: titles, cosmetic hues, the Legacy
Awakening history, the echo multiplier, and account-wide unlocks for newly created characters.

**Outside the loop entirely.** Collections are identity, not power, and must survive a reset:
P13's grove ledger above all, since it was specified as a long-term collection that eventually grants
teleportation to found groves, plus achievements, renown, guild membership and learned recipes.

### Pet and stable slots: what it costs

- **Follower slots are free.** `Mobile.FollowersMax` is per-mobile and serialized
  (`Server/Mobiles/Mobile.cs:844`, written `:2342`) and we already write it elsewhere
  (`customizations\Mobiles\Bosses\DespiseBosses.cs:50`).
- **Stable slots need a small patch.** `AnimalTrainer.GetMaxStabled` is a static method in a pinned file
  with no hook (`Mobiles/Vendors/NPC/AnimalTrainer.cs:58`), and we override nothing today.
- **It needs doing regardless.** The formula takes a 2 to 5 base from the summed Taming, Animal Lore and
  Veterinary, then adds `(skill - 90) / 10` for each of the three above 100. Verified by the overseer
  2026-10-01: that is 68 slots at 300 in all three, confirming cc-P20's figure, and still **38 at the
  new 200 cap**. OSI's own ceiling is 14.

## Numbers: decision versus proposal

The five-level reserve and +5 scroll/loop steps are now approved. The previous +25 step,
four-scroll plan and six-loop table are replaced throughout this note. Base echo has the
2026-10-03 starting shape above; playtesting still tunes it.

P20's original curve (`XP(L) = floor(40 * L^1.5)`) remains historical at
`notes/cc-P20-scratch/xp_curve.py`. P282 adapts it to the corrected ladder at
`notes/cc-P282-scratch/xp_curve.py` as a comparison. The approved S2 baseline is rerun by
`notes/cc-P282-scratch/approved_baseline.py`; its reproducible tables and recommendations follow below.

## What this costs, from cc-P20's ranked list

**Deleted or shrunk:**
- Rank 11, the bespoke Legacy Scroll line (M): deleted. Power scrolls do the job, and pinned's
  `SpecialScroll` and `PowerScroll` plumbing, including the confirmation gump and consumption, is
  reused rather than patched out.
- Rank 10 inverts from "stop scrolls raising caps" to "point scrolls at level", which is simpler.
- Rank 6, grandfathering: gone. Chase ruled no grandfathering 2026-10-01, and the old live world is
  retired, so there is nobody to grandfather.
- Rank 7, the soft-curve work across about 25 pinned files (L): shrinks a long way, because a 200
  ceiling leaves most runaway magnitudes inflated rather than inverted.
- Rank 9, gain paths (L): shrinks the most. At a 200 cap the six weapon skills (ceiling about 220),
  Focus (200), Parry with a shield (380) and Mining sand (400) already reach it with no new content.
  The other 39 skills need a lift of about 40 points, not 840.

**Still required, unchanged:**
- **Rank 4** (M, about 8 pinned files): the chance-based exploits all sit below 160 and survive the
  lower ceiling. Hiding works in combat from 118; Stealing is never caught from 150; bard skills are a
  certain success from about 150, with Musicianship's uncapped difficulty reduction as the root cause;
  guards cannot reveal anyone hiding at 121+; Tinkering trap damage is uncapped from 120.
- **D42**, the salvage bag ingot dupe, starts at Mining 143 and is live now.
- **Rank 5** is the implementation: a per-character record in `ClusterFAccountData` keyed by serial
  (the `CharacterGuildData` pattern from P18), and `ClusterFSkillCaps.Apply` writing `cap = maxLevel`
  instead of a flat 300. `Apply` is a single chokepoint hooked to `WorldLoad` and `OnLogin`, so this
  is small.

## Rescaling the 200 ceiling forces

- `ClusterFSkillCaps`: individual cap 300 and the total, now both derived from max level.
- `ClusterFStatCaps`: the individual cap of 500 is live (it feeds the effective-stat patch), not dead config.
  Under the 2026-10-02 decision the effective clamp goes; the total of 1500 never binds and can go with it.
- The `skills.grandmaster` and `skills.triple_grandmaster` achievements are keyed to 300
  (`ClusterFAchievements.cs:950, :984-993`) and become unreachable.
- `ClusterFMiningExtension.cs:148-181`: the smithing ingot gates run 100 to 300, so everything above
  200 strands content, Celestial included.
- The Smith Seal catalog sells Blacksmithing scrolls at 305 to 320 (D43). Under this design those
  become level scrolls or they go.
- Pinned's `StatCapScroll` raises a total cap that no longer exists. Drop it from loot, or leave it inert.
- Two stale comments: `ClusterFMiningExtension.cs:148-150` still says scrolls raise the cap to 500, and
  `roadmap.md:457-500` claims Mining progression uses the full 0-300 range.

## A content consequence worth keeping

A 50 cap in loop 0 puts the whole extended resource system out of reach, because all 8 extended ores
require GM Mining at 100. That is not a problem, it is pacing, and the dungeon decision already covers
it: the four New Haven resources (Dawnstone, Burrowhide, Gloomsilk, Rootwood) are specified as a
**starter tier, low skill**, so they are the loop-0 resource game and the extended ores become the
reward for pushing max level to 100.

## Still open

1. Confirm the precise five-level reserve valuation and scroll/reset transaction below.
   Credit from level 1 is already decided (10-05); escrow would be a new decision.
2. Approve or change the current-level content, title, Renown and cosmetic proposal below.
   No free skill or stat points; no current-level stat gate.
3. Playtest the approved S2 curve and kill-XP assumptions. The curve has been rerun on the
   21-reset ladder; numerical tables are estimates, not measured player progression. The
   C=24 power curve is a comparison, not a replacement decision.
4. **F-14's creature scale: answered 2026-10-01 (Chase). Everything above 160 is a custom creature we
   create.** So Bard difficulty (`BaseInstrument.GetBaseDifficulty`, hard cap 160, 68 creatures sitting
   on it including every boss) stays as the scale for ported creatures, and our own creatures carry
   their own level field above it. F-14 does not need a new scale for stock content, only a field on
   ours.
5. **A gain path for every skill, one skill at a time (Chase, 2026-10-02).** cc-P20 found 39 of 58 skills cannot gain
   past about 160 by use, because each use carries a fixed `maxSkill` (`SkillCheck.cs:58-61`). Each needs a use whose
   ceiling follows the cap, as our `Meditation.cs:92` already does (P20 recommendation 3, `cc-P20-skill-scaling-research.md:87`). Start from P20's per-skill
   tables (every gain call and its ceiling, with file:line). Shape: a notes-only pass that proposes a gain path per
   skill, then builder batches by skill group. Only needed once the F-12 cap goes above 160.

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

| Loop | Cap | Echo | Old h | New h | Total h | Cumulative h | Cumulative days 1h/3h/6h |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 50 | 1x | 0.00 | 3.00 | 3.00 | 3.00 | 3.00 / 1.00 / 0.50 |
| 1 | 100 | 1.5x | 2.00 | 5.55 | 7.55 | 10.55 | 10.55 / 3.52 / 1.76 |
| 2 | 105 | 2x | 4.28 | 8.19 | 12.47 | 23.03 | 23.03 / 7.68 / 3.84 |
| 3 | 110 | 2.5x | 6.70 | 7.97 | 14.67 | 37.69 | 37.69 / 12.56 / 6.28 |
| 4 | 115 | 3x | 8.24 | 7.61 | 15.85 | 53.54 | 53.54 / 17.85 / 8.92 |
| 5 | 120 | 3.5x | 9.24 | 7.29 | 16.52 | 70.06 | 70.06 / 23.35 / 11.68 |
| 6 | 125 | 4x | 9.90 | 6.99 | 16.89 | 86.95 | 86.95 / 28.98 / 14.49 |
| 7 | 130 | 4.5x | 10.36 | 6.71 | 17.07 | 104.02 | 104.02 / 34.67 / 17.34 |
| 8 | 135 | 5x | 10.66 | 6.46 | 17.12 | 121.14 | 121.14 / 40.38 / 20.19 |
| 9 | 140 | 5.5x | 10.87 | 6.22 | 17.09 | 138.23 | 138.23 / 46.08 / 23.04 |
| 10 | 145 | 6x | 11.00 | 6.00 | 17.00 | 155.23 | 155.23 / 51.74 / 25.87 |
| 11 | 150 | 6.5x | 11.08 | 5.80 | 16.87 | 172.10 | 172.10 / 57.37 / 28.68 |
| 12 | 155 | 7x | 11.11 | 5.61 | 16.72 | 188.82 | 188.82 / 62.94 / 31.47 |
| 13 | 160 | 7.5x | 11.12 | 5.43 | 16.55 | 205.37 | 205.37 / 68.46 / 34.23 |
| 14 | 165 | 8x | 11.10 | 5.26 | 16.36 | 221.74 | 221.74 / 73.91 / 36.96 |
| 15 | 170 | 8.5x | 11.07 | 5.10 | 16.17 | 237.91 | 237.91 / 79.30 / 39.65 |
| 16 | 175 | 9x | 11.02 | 4.96 | 15.98 | 253.89 | 253.89 / 84.63 / 42.31 |
| 17 | 180 | 9.5x | 10.96 | 4.82 | 15.78 | 269.67 | 269.67 / 89.89 / 44.94 |
| 18 | 185 | 10x | 10.90 | 4.68 | 15.58 | 285.25 | 285.25 / 95.08 / 47.54 |
| 19 | 190 | 10x | 11.36 | 4.56 | 15.92 | 301.17 | 301.17 / 100.39 / 50.19 |
| 20 | 195 | 10x | 11.82 | 4.44 | 16.26 | 317.43 | 317.43 / 105.81 / 52.90 |
| 21 | 200 | 10x | 12.26 | 4.33 | 16.59 | 334.02 | 334.02 / 111.34 / 55.67 |

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

| Band | Base h / days at 1h | Base days at 3h | Base days at 6h | Old h at x10 |
| --- | --- | --- | --- | --- |
| 1->10 | 0.25 | 0.08 | 0.04 | 0.02 |
| 10->25 | 0.79 | 0.26 | 0.13 | 0.08 |
| 25->50 | 1.96 | 0.65 | 0.33 | 0.20 |
| 50->75 | 2.54 | 0.85 | 0.42 | 0.25 |
| 75->100 | 3.01 | 1.00 | 0.50 | 0.30 |
| 100->105 | 8.19 | 2.73 | 1.37 | 0.82 |
| 105->110 | 7.97 | 2.66 | 1.33 | 0.80 |
| 110->115 | 7.61 | 2.54 | 1.27 | 0.76 |
| 115->120 | 7.29 | 2.43 | 1.21 | 0.73 |
| 120->125 | 6.99 | 2.33 | 1.16 | 0.70 |
| 125->130 | 6.71 | 2.24 | 1.12 | 0.67 |
| 130->135 | 6.46 | 2.15 | 1.08 | 0.65 |
| 135->140 | 6.22 | 2.07 | 1.04 | 0.62 |
| 140->145 | 6.00 | 2.00 | 1.00 | 0.60 |
| 145->150 | 5.80 | 1.93 | 0.97 | 0.58 |
| 150->155 | 5.61 | 1.87 | 0.93 | 0.56 |
| 155->160 | 5.43 | 1.81 | 0.90 | 0.54 |
| 160->165 | 5.26 | 1.75 | 0.88 | 0.53 |
| 165->170 | 5.10 | 1.70 | 0.85 | 0.51 |
| 170->175 | 4.96 | 1.65 | 0.83 | 0.50 |
| 175->180 | 4.82 | 1.61 | 0.80 | 0.48 |
| 180->185 | 4.68 | 1.56 | 0.78 | 0.47 |
| 185->190 | 4.56 | 1.52 | 0.76 | 0.46 |
| 190->195 | 4.44 | 1.48 | 0.74 | 0.44 |
| 195->200 | 4.33 | 1.44 | 0.72 | 0.43 |

### Approved S2: full five-level banks, including the cost to fill

The fill time was spent at the previous cap with no echo and is charged to the arriving
loop before its reset. After-credit h starts after the bank has been applied, including
any residual partial XP. The table does not count stored XP as free playtime. The final
row stops at 200 with no outgoing bank. Cap rows use current level, not just owning that cap.

| Loop | Bank XP | Level after credit | Fill prior h | After credit h | Cumulative incl. fill h |
| --- | --- | --- | --- | --- | --- |
| 0 | 0.00 | 1 | 0.00 | 3.00 | 3.00 |
| 1 | 14552.78 | 29 | 0.49 | 6.64 | 10.13 |
| 2 | 501528.78 | 101 | 8.36 | 4.96 | 23.44 |
| 3 | 511362.68 | 102 | 8.12 | 9.89 | 41.45 |
| 4 | 511362.68 | 102 | 7.75 | 11.87 | 61.06 |
| 5 | 511362.68 | 102 | 7.41 | 13.11 | 81.58 |
| 6 | 511362.68 | 102 | 7.10 | 13.90 | 102.59 |
| 7 | 511362.68 | 102 | 6.82 | 14.41 | 123.81 |
| 8 | 511362.68 | 102 | 6.56 | 14.73 | 145.10 |
| 9 | 511362.68 | 102 | 6.31 | 14.92 | 166.33 |
| 10 | 511362.68 | 102 | 6.09 | 15.01 | 187.43 |
| 11 | 511362.68 | 102 | 5.88 | 15.04 | 208.34 |
| 12 | 511362.68 | 102 | 5.68 | 15.01 | 229.03 |
| 13 | 511362.68 | 102 | 5.50 | 14.96 | 249.49 |
| 14 | 511362.68 | 102 | 5.33 | 14.87 | 269.69 |
| 15 | 511362.68 | 102 | 5.17 | 14.77 | 289.62 |
| 16 | 511362.68 | 102 | 5.01 | 14.65 | 309.28 |
| 17 | 511362.68 | 102 | 4.87 | 14.52 | 328.67 |
| 18 | 511362.68 | 102 | 4.73 | 14.38 | 347.79 |
| 19 | 511362.68 | 102 | 4.61 | 14.73 | 367.12 |
| 20 | 511362.68 | 102 | 4.49 | 15.06 | 386.67 |
| 21 | 511362.68 | 102 | 4.37 | 15.40 | 406.44 |

| Profile / reserve | To 100 h | To 200 h | Days at 1h/3h/6h |
| --- | --- | --- | --- |
| Steady empty | 10.55 | 334.02 | 334.02 / 111.34 / 55.67 |
| Cautious empty | 28.13 | 890.67 | 890.67 / 296.89 / 148.44 |
| Steady full banks incl. filling | 10.13 | 406.44 | 406.44 / 135.48 / 67.74 |
| Cautious full banks incl. filling | 26.99 | 1083.83 | 1083.83 / 361.28 / 180.64 |

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

| C | Loop 0 h | Loop 1 h | Creation to 100 h | Loop 21 h | Creation to 200 h |
| --- | --- | --- | --- | --- | --- |
| 20 | 7.73 | 19.47 | 27.20 | 8.37 | 199.70 |
| 24 | 9.28 | 23.36 | 32.64 | 10.04 | 239.65 |
| 30 | 11.60 | 29.20 | 40.80 | 12.55 | 299.56 |
| 40 | 15.46 | 38.94 | 54.40 | 16.73 | 399.43 |

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
