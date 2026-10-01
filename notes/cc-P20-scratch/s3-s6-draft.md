## 3. Gains past 120

### 3.1 The formula (pinned) and our overrides

Pinned `UOContent/Skills/SkillCheck.cs`:

- A ranged check `CheckSkill(skill, min, max)` returns false with no gain roll when value < min, and
  **returns true with no gain roll when value >= max** (`:53-61` location, `:161-169` target).
  A direct-chance check returns true with no gain roll when chance >= 1.0 (`:84-87`, `:190-193`).
- Otherwise `CheckSkill` (`:94-145`): below 10.0 base every use gains (`:106-109`). Above it, if the
  region and the anti-macro check allow (`:104`, `:110`, `:198-206`):

      gc = ( (Skills.Cap - Skills.Total) / Skills.Cap  +  (skill.Cap - skill.Base) / skill.Cap ) / 2   (:112-114)
      gc = ( gc + (1 - chance) * (success ? 0.5 : 0.0) ) / 2                                          (:116-117, AOS)
      gc = gc * GainFactor, floor 0.01                                                                  (:119-124)

  Call the two halves A (total-cap headroom) and B (this skill's headroom). Both are **fractions of
  the cap**, so the formula has no absolute scale: a skill at 150 of cap 300 rolls exactly what a skill
  at 500 of cap 1000 rolls.
- `Gain` (`:208-254`) adds 1 fixed point (0.1) (1-4 below 10.0), clamped to `CapFixedPoint`
  (`:252`), and only while `Skills.Total < Skills.Cap` for players (`:250`).
- `GainFactor` is 1 for all 58 skills (`Distribution/Data/skills.json`, 58 entries counted, all `1`).
- Anti-macro is **off** by default (`AntiMacroSystem.cs:97`). Live value not checked (the live
  `Configuration/antimacro.json` is inside the container); unverified.

Ours, on top (`server\customizations\ClusterFSkillGain.cs`, live defaults):

- **3 gain rolls per use** (`chanceAttempts` 3, `:8`, `:97-112`): the base handler is re-run up to two
  more times while the skill is Up and below cap; only the first result counts for success.
- **5x amount per gain** (`amountMultiplier` 5, `:9`, `:127-139`): each gain calls `SkillCheck.Gain`
  four more times, so one gain is 0.5 points, not 0.1.
- `ClusterFSkillCaps.cs:82-89`: "unlimited" total means `Skills.Cap = 58 x individual cap` (17,400.0 at
  300). This keeps term A near 1 for any real character. **In OSI, A is the main brake** (it falls to 0
  as Total nears 700); here it never brakes.
- `TestCenterSkillGain.cs` multiplies GainFactor on a Test Center shard only.
- `customizations\Meditation.cs:92` passes the skill's own cap as maxSkill, so Meditation never hits
  the "no challenge" ceiling.

### 3.2 How the chance behaves toward 300, 500 and 1000

It does **not** stall and it **cannot go negative** (B >= 0 because `Gain` never passes the cap,
and the floor is 0.01). With A near 1, the lowest it reaches is about 0.24 per roll at the cap
itself. What stops gains past 120 is not the formula but **the gain ceiling**: every pinned use
with a fixed `maxSkill` below the player's value returns "no challenge" and never rolls. Section 2
lists each skill's ceiling. So the real question per skill is whether any use still has a
`maxSkill` (or a direct chance below 1.0) above 120.

### 3.3 Phase 4F's "natural gain slowdown past 200 is sufficient"

**False.** The formula is relative to the cap, so there is no slowdown that starts at 200. With a
cap of 500, a skill at 200 rolls B = 0.6, the same as 120 of 300 today. The two things that do slow a
player past 200 are (a) the gain ceilings, which stop gains entirely rather than slowing them, and (b)
the point count, which grows linearly with the cap (1000 points of skill is 2,000 gain events at 0.5
each). Neither is a tuning dial.

### 3.4 Estimated gain per use

Model: `notes\cc-P20-scratch\gain_model.py` (a direct transcription of `SkillCheck.cs:112-124` plus
ClusterFSkillGain). Assumptions: AOS rules, GainFactor 1, anti-macro off, a character with 7 skills at
the stated value (sets Total), an "easy" use the player succeeds at 90 percent of the time and a "hard"
use at 50 percent, **and a use whose maxSkill is above the player's value** (otherwise the answer is 0).
"gc" is the chance per roll; "pts/use" is expected skill points per use with 3 rolls and 0.5 per gain.

Live today, cap 300 (total cap 17,400):

| skill | A | B | gc easy | gc hard | pts/use easy | pts/use hard |
|---|---|---|---|---|---|---|
| 50 | 0.980 | 0.833 | 0.476 | 0.516 | 0.714 | 0.774 |
| 100 | 0.960 | 0.667 | 0.429 | 0.469 | 0.644 | 0.704 |
| 120 | 0.952 | 0.600 | 0.410 | 0.450 | 0.616 | 0.676 |
| 200 | 0.920 | 0.333 | 0.336 | 0.376 | 0.504 | 0.564 |
| 300 | 0.879 | 0.000 | 0.242 | 0.282 | 0.363 | 0.423 |

Cap 1000 (total cap 58,000):

| skill | A | B | gc easy | gc hard | pts/use easy | pts/use hard |
|---|---|---|---|---|---|---|
| 50 | 0.994 | 0.950 | 0.508 | 0.548 | 0.763 | 0.823 |
| 100 | 0.988 | 0.900 | 0.494 | 0.534 | 0.742 | 0.802 |
| 120 | 0.986 | 0.880 | 0.489 | 0.529 | 0.733 | 0.793 |
| 200 | 0.976 | 0.800 | 0.466 | 0.506 | 0.700 | 0.760 |
| 300 | 0.964 | 0.700 | 0.438 | 0.478 | 0.658 | 0.718 |
| 500 | 0.940 | 0.500 | 0.382 | 0.422 | 0.574 | 0.634 |
| 1000 | 0.879 | 0.000 | 0.242 | 0.282 | 0.363 | 0.423 |

For comparison, OSI rules (total cap 700, no ClusterF boost, 7 skills): gc hard 0.31 at 50, 0.11 at
90, 0.07 at 100, with 0.1 points per gain. **At 300 our rate per use is about 60 times OSI's at 100.**

Uses to climb from 0 to the cap, if a use at that success rate always exists: cap 50: 82-92; cap 100:
164-183; cap 300: 492-549; cap 500: 820-914; **cap 1000: 1,640-1,828 uses**. At one use every 5
seconds that is about 2.5 hours per skill to 1000.

So with today's gain settings, **skill gain is not what paces the loop system: the level cap is.** A
player will sit at each loop's skill cap long before the next loop, unless gains are slowed. That is
fine if intended (the cap is the gate) but it means the 50 -> 1000 skill journey is decided almost
entirely by the XP curve in section 6 and by whether content exists above each gain ceiling.

Recommendation: keep pinned's formula, but (1) make the total cap a real number per loop or apply a
per-loop gain divisor if gains should take time, and (2) give each skill at least one use whose
`maxSkill` follows the skill's cap (as `Meditation.cs:92` already does), or the skill cannot move past
its ceiling at all.

## 6. A first XP curve (FIRST DRAFT for Chase)

Script: `notes\cc-P20-scratch\xp_curve.py`. Every number is a placeholder to react to.

- **XP to the next level: `XP(L) = 40 x L^1.5`** (rounded down). Total to reach level N is about
  `16 x N^2.5`.
- **XP per kill: `5 x creature level`** (F-14 creature level), so XP per kill grows with the player.
  Time per level then grows as `L^0.5`, and a loop to cap N takes time proportional to `N^1.5`.
- **Later loops faster**: +20 percent XP per completed loop (loop 13 earns 3.6x).
- **Echo XP**: x2 XP on levels the character already reached in an earlier loop, so the replayed
  1 to (previous cap) stretch goes quickly and the new levels carry the weight.
- XP from skill gains, crafting, gathering and discoveries can feed the same pool; not modeled here.

| level | XP to next | total XP to reach |
|---|---|---|
| 1 | 40 | 0 |
| 5 | 447 | 680 |
| 10 | 1,264 | 4,439 |
| 25 | 5,000 | 47,513 |
| 50 | 14,142 | 275,783 |
| 100 | 40,000 | 1,580,001 |
| 200 | 113,137 | 8,994,376 |
| 300 | 207,846 | 24,837,556 |
| 500 | 447,213 | 89,218,979 |
| 1000 | 1,264,911 | 505,331,643 |

Two assumptions:
- **A, steady**: 120 kills an hour, creatures at the player's own level.
- **B, cautious**: 60 kills an hour, creatures at 75 percent of the player's level.
- A third column shows A if the strongest content sits at level 300 (so kills past 300 earn a 300
  rate). That is the real risk: see section 5 on whether content exists that high.

| loop | cap | hours A | hours B | hours A, content tops at 300 | cumulative A | cumulative B |
|---|---|---|---|---|---|---|
| 0 | 50 | 15 | 41 | 15 | 15 | 41 |
| 1 | 100 | 30 | 81 | 30 | 46 | 122 |
| 2 | 150 | 42 | 113 | 42 | 88 | 235 |
| 3 | 200 | 53 | 141 | 53 | 141 | 376 |
| 4 | 250 | 63 | 167 | 63 | 203 | 542 |
| 5 | 300 | 71 | 190 | 71 | 275 | 733 |
| 6 | 350 | 80 | 212 | 82 | 354 | 945 |
| 7 | 400 | 87 | 233 | 95 | 442 | 1,178 |
| 8 | 500 | 123 | 327 | 154 | 564 | 1,505 |
| 9 | 600 | 144 | 385 | 207 | 709 | 1,890 |
| 10 | 700 | 165 | 441 | 268 | 874 | 2,331 |
| 11 | 800 | 185 | 495 | 337 | 1,060 | 2,826 |
| 12 | 900 | 205 | 546 | 412 | 1,265 | 3,372 |
| 13 | 1000 | 224 | 596 | 493 | 1,488 | 3,968 |

Reading it: loop 0 is two to five evenings to a week, which meets F-12's "first cap in days, not
weeks". GM (100) arrives after about 46 to 122 hours. Max level is a long-term prestige goal of
1,500 to 4,000 hours. The single coefficient 40 scales every row linearly; the exponent 1.5 sets how
much the late loops stretch.
