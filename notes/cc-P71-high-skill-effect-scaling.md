# cc-P71: High-skill effects scaled to 200 (Nerve Strike, stable slots, Fire Horn, Stealth steps, Healing)

Builder task, 2026-10-10. Brief: `D:\UO\cc-prompts\cc-P71-high-skill-effect-scaling.md`. Engine authority:
`D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88` (`git rev-parse HEAD` today). Every pinned file:line
below is against it, with paths relative to `Projects\UOContent\`. `C\` = `D:\ShatteredLegacy\server\customizations`,
`P\` = `server\patches`, `T\` = `server\tests`. Scratch: `D:\UO\cc-p71-work\` (`make-patches.py` writes the five patches
from LF copies of pinned with the earlier Bandage patch applied; `make-red.py` writes the red tree; `build1.log`,
`build2.log`, `red1.log`, `detail-cc-p71.log`, `detail-cc-p71-red.log` hold the printed numbers).

**Start.** The first pre-check found P67's work uncommitted, so I stopped (Chase commits first). Chase committed it as
`a6e17fd` ("Shard work, 2026-10-10 15:35") and I started from a clean tree. P67's own notes still end `P67 STOPPED` (its
final build, red build and detailed run never ran). Build 1 here was the first full build of HEAD since then: **63/63
patches applied, 1005 of 1006 tests passed**, and the one failure was my own new fixture. So P67's tree builds and its
tests pass; its red tree and detailed run are still not run.

Nothing committed, nothing deployed, no shard restarted, `docs\` not touched, `sl-modernuo:latest` not moved
(`63c7bc32f22a` now; I tagged only `sl-modernuo:cc-p71` and `cc-p71-red`, and the red tree built no image).

## Headlines

1. **Done: five effects scale to 200 instead of growing without bound.** Each one follows pinned exactly up to OSI's top
   skill. Past that it follows one shared curve up to a chosen value at 200, and holds that value above 200 (worn bonuses
   can read over the cap, D-113). Final `docker\uo\build.sh -t sl-modernuo:cc-p71`: **63/63 patches** (58 plus 5 new),
   **1006/1006 shard facts** (1000 before plus 6 new), image `sl-modernuo:cc-p71` = `b66f239333f8`.
2. **Red then green.** On the red tree (`make-red.py`: the five patches and their `apply_patch` lines removed, every API
   kept), **5 failed / 1001 passed**. The five failures are exactly S1 to S5, and each fails at its 200 assertion, after its
   assertions at and below OSI's top have passed. S6 tests only the curve in our own file, so it passes on both trees.
3. **The values at 200** (all in the config table): Nerve Strike **95%** (today certain from 137.5), stable slots **23**
   at 200/200/200 (today 38), Fire Horn **1.10x** the damage at 120 with all four bard skills at 200 (today 2.32x
   measured), Stealth **34** steps (today 40), bandage **72** average at 200/200 (today 93).
4. **One config table, `clusterf.skillScaling.*` in `modernuo.json`.** It sits next to P66's `clusterf.skillGain.*`. It
   holds 12 keys: the switch, the curve's bend, and an OSI top skill plus a value at 200 for each effect. OSI's *value* at
   each top is computed from pinned's own formula and is not a key, so the curve always meets pinned exactly at the top
   (decision 1).
5. **Routed through `C\ClusterFSkillClamps.cs`, which now scales as well as clamps.** Each of the five patches changes one
   read, or one read site, and calls that file.
6. **Players only, all five.** The pinned lines treat creatures the same way, but I counted which creatures can reach
   them: only one creature on the shard has more than 120 in any of these skills (Kepetch Ambusher, Stealth 125,
   `C\Mobiles\Normal\KepetchAmbusher.cs:51`, keeps its 25 steps). Stable slots and Fire Horn are player-only paths anyway.
   Faction guards bandage (`Engines/Factions/Mobiles/Guards/GuardAI.cs`) and read as pinned.
7. **Two brief figures were wrong, checked by counting.**
   - **"Fire Horn damage reads Musicianship."** It reads all four bard skills, weighted Musicianship 1, Provocation 3,
     Discordance 3, Peacemaking 1 (`Items/Skill Items/Misc/FireHorn.cs:121-130`). Musicianship 200 alone is the brief's
     +17%; all four at 200 is **2.33x** (cc-P54's "189-233 per blast"; measured 211 against 91).
   - **"Stable slots ... against 17 today" does not match OSI's top.** Pinned gives **14** at 120/120/120 (5 from the sum
     plus 3 per skill, matching cc-P54's "OSI 14"). It gives 17 at 130 to 139 in all three. What the 17 was meant to be is
     unverified.
   - Also: **Stealth's OSI top is 120, not 142.** Stealth has a 120 power scroll (`Items/Special/Special Scrolls/
     PowerScroll.cs:41`). 142 is only where pinned's gain window ends. The curve is anchored at 120 (24 steps), and it
     gives 28 at 142, the same as pinned.

## The rule and the curve

For each effect: at or below OSI's top skill, and for creatures, pinned's number. Past the top, for a player:

    value = OSI value + (value at 200 - OSI value) x C(t),   t = (skill - top) / (200 - top), held at 1 from 200
    C(t)  = (1 - e^(-k t)) / (1 - e^(-k)),                   k = clusterf.skillScaling.curve, default 1.5

C rises from the first point past the top, each point adds less than the one before, and it reaches exactly 1 at 200. So
there is no cliff and no flat stretch on the curve before 200. With k = 1.5 the share of the rise reached is **40% at
140, 68% at 160 and 87% at 180** (printed by S6: 0.4025, 0.6792, 0.8693). k = 0 makes it a straight line. Integer effects
(slots, steps) truncate as pinned does. Each integer step lands within the 80 points, and the last one lands at 200.

**Alternatives argued (also in `docker\uo\apply-patches.sh`):**
- Clamping at OSI was rejected: Chase asked for 200 to be better than OSI's top, not equal to it.
- Customizations alone were rejected: each read is a local inside a pinned method, and `AnimalTrainer.GetMaxStabled` is
  static with one caller (`:245`) and no hook.
- A separate curve per effect was rejected: one bend, tuned in one place, and the effects stay comparable.
- For stable slots, truncating each skill's share separately was rejected. With 6 at 200 that holds every share flat from
  160 to 199. Summing the three shares and truncating once gives about one slot every 9 points when the skills climb
  together. I found this from the numbers before the final build and changed it.

## The five effects

Each "today" column is pinned's number, measured on the red tree. Each "new" column is the curve's number, measured on
green. At 100 and 120 the two trees agree (detail logs).

### 1. Nerve Strike paralysis (`Items/Weapons/Abilities/NerveStrike.cs:66`, `P\NerveStrike-paralyze-scaled-200.patch`)

Pinned's chance is (150/7 + 4 x Bushido / 7) / 100. It is the ML branch, which this shard runs.

| | OSI anchor (Bushido 120) | 140 | 160 | 180 | today at 200 | **new at 200** |
|---|---|---|---|---|---|---|
| paralysis chance | 0.900 | 0.920 | 0.934 | 0.944 | 1.357 (certain from 137.5) | **0.950** |

Argument: 95% at 200 makes the top Bushido player's opener almost reliable without being a certainty. The defender also
keeps pinned's paralysis immunity window after each paralysis (`ParalyzingBlow.BeginImmunity`), so 95% against 90% is
about one extra freeze per twenty strikes. The value is clamped at 0.99 in code, so no config value can make it certain.

Not scaled, and listed for Chase: the strike's **damage** also grows with Bushido, 15 x (B - 50) / 70 + 0 to 9. That is
15 to 24 at 120 and 32 to 41 at 200. It is not in the brief's five (decision 4).

S1 is a source fact plus a value fact. A player's weapon ability validates against its NetState
(`WeaponAbility.cs:330-339`), and the test host has none, so `OnHit` cannot be reached for a player. On red, the source
line check fails.

### 2. Stable slots (`Mobiles/Vendors/NPC/AnimalTrainer.cs:58-99`, `P\AnimalTrainer-stable-slots-scaled-200.patch`)

Pinned gives 2 to 5 from the sum of the three skills, plus (int)((skill - 90) / 10) for each of Taming, Lore and
Veterinary from 100. That is 3 per skill at 120 and 11 at 200. Past 120, each skill's share becomes 3 + 3 x C. The three
shares are summed and truncated once. The patch is one line, at the `return`.

| Taming/Lore/Vet | OSI anchor (120 each) | 140 | 160 | 180 | today at 200 | **new at 200** |
|---|---|---|---|---|---|---|
| slots, all three | 14 | 17 (pinned 20) | 20 (26) | 21 (32) | 38 | **23** |
| slots, 200/120/120 | | | | | 22 | **17** |

Argument: 23 is nine more than OSI's top, which gives a 200 tamer room for a rotation of the shard's high-end pets
without the slots doubling. Stable slots carry no combat value; their cost to the economy is storage. With Taming stopping near 157 until batch T's harder tames (cc-P66 decision 5), a tamer today
reaches about 20.

### 3. Fire Horn damage (`Items/Skill Items/Misc/FireHorn.cs:121-130`, `P\FireHorn-damage-scaled-200.patch`)

Each bard skill's Fixed value v is scaled to v + 2 x max(0, v - 900), and the weighted average is (M + 3P + 3D + Pc) / 80.
PvM damage is half of that, PvP a third. Past 120, each skill's scaled value becomes 1800 x (1 + 0.10 x C). So all four
at 200 give 1.10x, and one skill alone gives its weight's share (Musicianship alone +1.25%, Provocation alone +3.75%).

| all four bard skills | OSI anchor (120) | 140 | 160 | 180 | today at 200 | **new at 200** |
|---|---|---|---|---|---|---|
| one blast, one target, no fire resist, mid roll (S3) | 91 | 93 (pinned 121) | 96 (151) | 97 (181) | 211 (2.32x) | **100 (1.10x)** |

Argument: the horn is an area attack with no skill check on its damage, and it costs only 4 sulfurous ash. At 2.33x it is 211
per blast every 6 seconds to everything within 2 tiles. At 1.10x it stays a bard's tool. I chose 1.10
over the brief's 1.08 because it is set for all four skills at 200. The brief's +8% read as Musicianship alone, and that
is now +1.25%. PvP gets the same 1.10x on a third of the damage.

### 4. Stealth steps (`Skills/Stealth.cs:102`, `P\Stealth-steps-scaled-200.patch`)

Pinned is (int)(Stealth / 5) under AOS. That is 24 at 120, the OSI top (power scroll), 28 at 142 and 40 at 200. Past 120
the count becomes 24 + 10 x C.

| | OSI anchor (Stealth 120) | 140 | 160 | 180 | today at 200 | **new at 200** |
|---|---|---|---|---|---|---|
| steps (S4) | 24 | 28 (pinned 28) | 30 (32) | 32 (36) | 40 | **34** |

Argument: 34 is ten more than OSI's top. From 120 to 142 it is within one step of pinned's count, and equal at 140 and
142 (28), so a stealther there sees almost no change. It is still short of crossing most dungeon rooms without re-stealthing, so
Detect Hidden and creature reveals keep their meaning. This is the brief's suggestion.

### 5. Heal per bandage (`Items/Skill Items/Misc/Bandage.cs:387-388` pinned, `:397-398` after the pet-mimic patch; `P\Bandage-heal-scaled-200.patch`)

Pinned's AOS amount is min = A/8 + H/5 + 4, max = A/6 + H/2.5 + 4, so the average is A x 7/48 + 0.3 H + 4. Past 120,
each of the healer's two skills is read as 120 + rise x C. The rise is chosen so that 200/200 averages 72; at the default
it is 32.5 points. The same applies to Veterinary and Animal Lore on a pet. Only the amount reads it: the success chance,
cures, resurrections and slips read the whole skill.

| Healing/Anatomy | OSI anchor (120/120) | 140 | 160 | 180 | today at 200 | **new at 200** |
|---|---|---|---|---|---|---|
| heal, mid roll (S5) | 57 | 63 (pinned 66) | 67 (75) | 70 (84) | 93 | **72** |
| heal, 200/120 | | | | | 81 | **67** |

Argument: 72 is +25% over OSI's top, with the range about 54 to 90. A Greater Heal is Magery x 0.4 + 1 to 10
(`Spells/Fourth/GreaterHeal.cs:51-52`): 53.5 at 120 and 85.5 at Magery 200. So a bandage at 200 out-heals a 120 mage's
Greater Heal but stays below a 200 mage's. It also takes several seconds, can slip, and heals or cures in one
application, not both. 93 would have out-healed a 200 Greater Heal from a free action. Bandage delays are a separate
problem (the 500 stat cap, cc-P54) and are not touched here.

## Config keys (`modernuo.json`, written with these defaults on the first start)

| Key | Default | Meaning |
|---|---|---|
| `clusterf.skillScaling.enabled` | `true` | off: all five read as pinned, growing without bound again |
| `clusterf.skillScaling.curve` | `1.5` | the bend k; 0 is a straight line (clamped 0 to 10) |
| `clusterf.skillScaling.nerveStrike.osiTop` | `120` | Bushido where the curve starts (OSI value 0.90 from pinned's formula) |
| `clusterf.skillScaling.nerveStrike.chanceAt200` | `0.95` | at least the OSI value, at most 0.99 |
| `clusterf.skillScaling.stableSlots.osiTop` | `120` | per skill (OSI share 3) |
| `clusterf.skillScaling.stableSlots.perSkillAt200` | `6` | per skill; 23 in all at 200/200/200 |
| `clusterf.skillScaling.fireHorn.osiTop` | `120` | each bard skill (OSI scaled value 1800) |
| `clusterf.skillScaling.fireHorn.damageAt200` | `1.10` | times the damage at the top, all four at 200 |
| `clusterf.skillScaling.stealth.osiTop` | `120` | (OSI 24 steps) |
| `clusterf.skillScaling.stealth.stepsAt200` | `34` | |
| `clusterf.skillScaling.healing.osiTop` | `120` | each of the healer's two skills (OSI average 57.5) |
| `clusterf.skillScaling.healing.averageAt200` | `72` | average heal at 200/200 |

Every value at 200 is held at no less than its OSI value, so a typo cannot drop an effect below OSI's top. Each `osiTop`
is clamped to 50 to 199. At start the server logs `ClusterF skill scaling: curve 1.5; at 200: Nerve Strike 0.9 -> 0.95,
stable slots per skill 3 -> 6, Fire Horn x1.1, Stealth steps 24 -> 34, bandage average 57.5 -> 72.` (the same text S6
prints). The values are read once at start, so a change needs a restart, not a build.

## Facts (`T\Skills\SkillScalingVerification.cs`)

S1 to S5 are one per effect, as above. Each drives pinned's own code (`GetMaxStabled`, `FireHorn.Use` into a 0-fire-resist
mongbat, `Stealth.OnUse`, `BandageContext.OnTick`) with the roll held at the middle, at 100, 120, 140, 160, 180 and 200.
Each asserts pinned's numbers at 100 and 120, the curve's number at 200, and that the effect never falls as skill rises.
S1 is source plus value, for the reason under effect 1. S6 covers the curve itself: 0 at the top, exactly 1 at and past
200, rising with smaller steps each point, held at 200 under a +15 worn bonus (Bushido 215: 0.95), creatures as pinned,
and the switch off giving pinned for players.

## Build

```
& "C:\Program Files\Git\bin\bash.exe" docker/uo/build.sh -t sl-modernuo:cc-p71
```

| Build | Tree | Patches | Facts | Result |
|---|---|---|---|---|
| 1 | first version | 63/63 | 1005/1006 | S5's fixture set the patient's Str to make room for the heal, and a player's hit points do not follow RawStr that way. Fixed by checking the room needed (1 + 93 fits under 100). Also the run that showed P67's HEAD builds |
| 2, final | stable slots summed then truncated | 63/63 | **1006/1006** | image `b66f239333f8` |
| red | `D:\UO\cc-p71-work\red1`, `-t sl-modernuo:cc-p71-red` | 58/58 | 5 failed / 1001 | S1 to S5, each at its 200 assertion (Nerve Strike source line; 38 for 23; 211 for 100; 40 for 34; 93 for 72); no image |

Detailed runs (`verbosity=detailed`, `--filter SkillScalingVerification`) on both builder images printed the tables
above.

## Register line (the register in `docs\fidelity-principle.md` ends at D-122; D-123 to D-129 are proposed in cc-P66 and cc-P67; next free D-130)

| D-130 | **Ours (cc-P71, Chase 2026-10-06, cc-P66 decision 4).** Five effects follow stock up to OSI's top skill and past it one diminishing-returns curve to a set value at 200, held above 200: Nerve Strike's paralysis chance (90% at Bushido 120, 95% at 200), stable slots from Taming, Lore and Veterinary (14 at 120 each, 23 at 200 each), Fire Horn damage (1.10 times at all four bard skills 200), Stealth steps (24 at 120, 34 at 200), the heal per bandage (57.5 average at 120/120, 72 at 200/200). Values in `modernuo.json`. Creatures as stock. OSI: the same at every value OSI allows; listed because skill past OSI's tops is ours (the 200 cap and D-113), and stock's formulas made Nerve Strike certain and these effects grow without bound | 200 is better than OSI's top, bounded | `visible` | `cc-P71` |

## Deviations and decisions for Chase

1. **OSI anchor values are derived, not config keys.** The config holds each OSI top *skill*. The value there is computed
   from pinned's own formula, so the curve cannot start with a jump at the top. If you would rather have the anchor values
   as keys too, that is a small change, but a mismatched key would create exactly that jump.
2. **The five values at 200 are my proposals:** 0.95, 23, 1.10x, 34 and 72. All except Fire Horn are the brief's
   suggestions, or inside its range. Fire Horn is 1.10x for all four skills, against the brief's +8%, which read as
   Musicianship alone. Tune them in `modernuo.json` after playtest.
3. **The curve's bend is shared.** Raise `curve` to front-load the gains, so 140 feels closer to 200, or set it to 0 for
   a straight line.
4. **Nerve Strike's damage still grows with Bushido** (15 to 24 at 120, 32 to 41 at 200, `NerveStrike.cs:55-64`). It is
   not in the brief's five, so it is not scaled here. It is a one-key addition to this table if you want it.
5. **The switch off is pinned, not OSI.** `enabled: false` restores the uncapped growth, including certain Nerve Strike.
   It is a revert switch, not a clamp.
6. **P67 is committed but still `STOPPED`.** This task's build 1 showed its HEAD builds and its tests pass (1000 of the
   pre-P71 facts green). Its red tree and detailed run are still not done.
7. **`tools/progress.py` not run.** Nothing is committed in either repo, so its output would only churn the README.

## For Chase

Commit, then deploy (Windows PowerShell, `;` between commands):

```
cd D:\ShatteredLegacy; git status --short
docker tag sl-modernuo:cc-p71 sl-modernuo:latest
```

Then restart the test shard the usual way. The log should show `[ShardVersion] Shattered Legacy 2026.10.10 ...` and the
`ClusterF skill scaling: ...` line above. `modernuo.json` gains the 12 `clusterf.skillScaling.*` keys. Do not publish the
wiki page (not asked).

In-game checklist (a staff character can `[set` its own skills; test the effects on a player account):

1. Nerve Strike at Bushido 200 against a monster, twenty times: about one strike in twenty does not paralyze. At 120,
   about two in twenty do not.
2. Stable slots: Taming, Lore and Veterinary 200, then stable pets at an animal trainer. The 24th is refused, and 23 fit.
3. Fire Horn: all four bard skills 200, then blast a monster. The damage is close to what it is at 120 (about a tenth
   more), not more than double.
4. Stealth 200, hidden: walk and count. Revealed after about 34 steps. At 120, about 24.
5. Bandages: Healing and Anatomy 200 on a hurt character. Heals land around 54 to 90, not 69 to 117.
6. Change `clusterf.skillScaling.stealth.stepsAt200` to 30 and restart: Stealth 200 gives 30 steps, with no rebuild.
7. `[version` shows 2026.10.10 and the bulletin lists the five lines.

P71 DONE
