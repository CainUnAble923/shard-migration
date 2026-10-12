# cc-P67: gain paths 2, craft ceilings for Carpentry, Fletching and Tinkering (batch K), content-skill caps, P61 follow-ups

Builder task, 2026-10-07. Brief: `D:\UO\cc-prompts\cc-P67-craft-ceilings.md`. Engine authority: `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88` (`git rev-parse HEAD` today, "fix: enumerators that end early, repeat entries, or
never end (#2685)"); every pinned file:line below is against it, paths relative to `Projects\UOContent\`. `C\` =
`D:\ShatteredLegacy\server\customizations`, `P\` = `server\patches`, `T\` = `server\tests`. Scratch: `D:\UO\cc-p67-work\`
(`a\` the patched build files copied out of `sl-uo-builder:cc-p66`, which is HEAD's tree; `make-patches.py` writes the four new
patches; `a0\` and `b\` the small-order patch's base and result; `make-red.py` and `red2\` the red tree (`red1\` its first copy,
from 95f4633, never built); `build1.log` to `build4.log`, `build-final.log`, `red2.log`, `detail.log` the printed numbers).

Shard HEAD `95f4633` (P66 committed), tree clean when I started: no clash. Nothing committed, nothing deployed, `docs\` not
touched, `sl-modernuo:latest` not moved, the wiki page not published.

## Status: finished on 2026-10-12

The work was written 2026-10-07. Build 3 ran 997/1000 (the 3 were one ordering mistake in my fact K5, fixed). Build 4 was lost
when **Docker Desktop crashed** and would not restart (its backend could not remove a stale
`%LOCALAPPDATA%\docker-secrets-engine\engine.sock`); I stopped there. Chase brought Docker back and committed the work as
`a6e17fd` (2026-10-10); cc-P71 then committed `b5fe596` on top (its notes record that P67's facts passed in its build). On
resuming I ran, against HEAD `b5fe596`:
- **final build** `build.sh -t sl-modernuo:cc-p67`: **63/63 patches, 1006/1006 shard facts**, image `sl-modernuo:cc-p67` =
  `80c8a1fc217b` (it contains cc-P71 too, since HEAD does);
- **red tree** (`red2`, `make-red.py` on HEAD): **36 failed / 970 passed**, every failure a P67 fact (list below);
- **detailed run** of `CraftCeilingsVerification` in `sl-uo-builder:cc-p67`: 41/41, numbers in `detail.log` and below.

VERSION: P67 started 2026.10.07; cc-P71 has since added 2026.10.10 above it, so `VERSION` reads 2026.10.10. Nothing to change.

## Headlines

1. **Carpentry, Fletching and Tinkering climb to 200 by crafting, with P61's rule** (Part A). `ClusterFCraftGain.CeilingFor`
   now reads one table per material family: `ClusterFMetalTiers` for Blacksmithy and Tinkering, the new `C\ClusterFWoodTiers.cs`
   for Carpentry and Fletching. No new hook: the cc-P61 hunk in `CraftItem-shard-hooks.patch` is unchanged.
2. **The woods are re-gated** to F-28's approved ladder (Ironwood 100, Ghostwood 115, Emberbark 130, Frostbark 140,
   Shadowbark 155, Runewood 170, Voidwood 185, Starwood 200) in both crafts; until now every one needed a flat 100, so no
   wood could carry a craft anywhere. **Tinkering gets the eight post-Valorite metals** at the smiths' tiers.
3. **Every chain reaches 200 with no gap** (fact K1, all four crafts): Blacksmithy stock top 140, Tinkering 130, Carpentry
   140.3, Fletching 130; each is above the first shard material's requirement and every ceiling is the next requirement.
4. **The consume check** (P54): only a recipe whose resources include the material list's base type (the type
   `CraftItem.ConsumeRes` swaps for the pick) and whose stock window has width gets a ceiling. **Logs to boards is not a
   recipe on this shard at all** (pinned `DefCarpentry.cs:94-97`, AOS and SE only); an axe cuts them (`Log.cs:84`), which rolls
   no skill. Kindling (0-0) never teaches.
5. **Harder items teach better** (Part C 2): past an item's maximum the band is (item's own minimum, ceiling). At 150 in Frost
   a kabuto now gains 0.0982 per craft, a plate tunic 0.0931, a dagger 0.0802 (all 0.1094 before). Note: every item is now a
   little slower than P61's slid window; the spread is what Chase asked for (decision 1).
6. **Worn bonuses never stop a craft early** (Part E): the band's top is ceiling + worn bonus, so Base is what is compared. A
   +10 smith in Mythril gains at Base 180 and 187.4 and stops at 187.5, as a smith with nothing worn. A +12.5 smith, whose top
   lands exactly on 200, is not counted twice by P66's cap rule (fact K5; a guard in `ClusterFSkillGain`).
7. **Orders roll among metals that still teach** (Part C 1), small **and large** (cheap in our full `LargeSmithBOD.cs`, built).
   At 150 with the setting on, every post-Valorite order is Frost (was about 2% of a 150 smith's orders).
8. **Four caps at OSI's tops**, each one line in a new pinned patch through `ClusterFSkillClamps`: trap damage level 12 (power
   uncapped, so Remove Trap rides Tinkering), the axe's Lumberjacking bonus 30%, Alchemy's potion strength share 30, the
   deep-water fishing finds at Fishing 120.
9. **Found, not fixed:** `CraftResources.GetType` (`C\ResourceInfo.cs:1092-1097`) stops the Wood range at Frostwood, so
   `GetInfo` returns null for all eight shard woods (decision 6).

---

## Part A: P61's rule for Carpentry, Fletching and Tinkering

**The rule** (`C\ClusterFCraftGain.cs`, header comment): a craft in a shard material can gain its craft skill up to the
material's gain ceiling, the next material's requirement. Below the item's own maximum the window is stock's. From the item's
maximum up it is (item's minimum, ceiling + worn bonus). Only the gain roll; success chance, failure, material loss and the
exceptional chance read the item's own range in `GetSuccessChance` (`Engines/Craft/Core/CraftItem.cs:902-904`) and are
untouched (P61's fact A4 still guards that for Blacksmithy; the same code path serves the other crafts).

**What changed:**
- `C\ClusterFCraftGain.cs`: `CeilingFor(system, item, typeRes)` for all four crafts, `CeilingFor(system, resource)` (the table
  per craft), `Consumes`, the band `(min, ceiling + bonus)`, `Window(m, skill, ...)` with the worn bonus.
- `C\ClusterFWoodTiers.cs` (new): the wood table, `RequiredSkill` and `GainCeiling`, the same shape as `ClusterFMetalTiers`.
- `C\ClusterFLumberjackingExtension.cs:283-331`: the sixteen `AddSubRes` lines read `ClusterFWoodTiers`; Carpentry's boards now
  carry stock's wood clilocs (1044041, and 1072652 "You cannot work this strange and unusual wood."). They had the ingots'
  1044036 and 1044268 ("... metal."), which a carpenter below a wood would now see far more often.
- `C\ClusterFMiningExtension.cs`: `ExtendTinkeringSubResources` (public, idempotent), the eight ingots at
  `ClusterFMetalTiers`, the same clilocs as stock's colored ingots in Tinkering (`Engines/Craft/DefTinkering.cs:589-597`).
- `C\ClusterFSkillGain.cs`: `WornBonus`, `CheckSkillWornBonusIncluded` and the guard in `EffectiveMax` (Part E).

### The chains (fact K1)

Blacksmithy and Tinkering (metals, `ClusterFMetalTiers`):

| Metal | Needs (Base) | Teaches to | Next needs |
|---|---|---|---|
| Iron .. Valorite | 0 .. 99 | the item's own max (Blacksmithy 140, Tinkering 130) | Platinum 112.5 |
| Platinum | 112.5 | 125 | 125 |
| Toxic | 125 | 137.5 | 137.5 |
| Blaze | 137.5 | 150 | 150 |
| Frost | 150 | 162.5 | 162.5 |
| Obsidian | 162.5 | 175 | 175 |
| Mythril | 175 | 187.5 | 187.5 |
| Adamantium | 187.5 | 200 | 200 |
| Celestial | 200 | 200 (teaches nothing: needs the cap) | (cap) |

Carpentry and Fletching (woods, `ClusterFWoodTiers`):

| Wood | Needs (Base) | Teaches to | Next needs |
|---|---|---|---|
| Regular .. Frostwood | 0 .. 100 | the item's own max (Carpentry 140.3, the tetsubo; Fletching 130, the yumi and repeating crossbow) | Ironwood 100 |
| Ironwood | 100 | 115 | 115 |
| Ghostwood | 115 | 130 | 130 |
| Emberbark | 130 | 140 | 140 |
| Frostbark | 140 | 155 | 155 |
| Shadowbark | 155 | 170 | 170 |
| Runewood | 170 | 185 | 185 |
| Voidwood | 185 | 200 | 200 |
| Starwood | 200 | 200 (teaches nothing) | (cap) |

**No gap in any craft.** The fact walks every 0.1 from the stock top to 199.9 and finds a material the crafter can work that
still teaches. Tinkering: stock teaches to 130, and Toxic (125) teaches 125 to 137.5. Fletching: stock to 130, and Ghostwood
(115) teaches to 130 and Emberbark (130) from there. Carpentry: stock to 140.3, and Frostbark (140) teaches to 155. The fact
also asserts each material's requirement in the live craft menu equals its table, so the re-gate and the Tinkering metals
are wired, not only tabled.

### The consume check, per craft (fact K2)

A recipe gets a ceiling only when one of its resources is the craft's material list base type, the test
`CraftItem.ConsumeRes` makes before it swaps in the pick (`CraftItem.cs:615-627`), and its stock window has width.

| Craft | Material list base (pinned) | Consumes it, so teaches past its max in a shard material | Does not |
|---|---|---|---|
| Blacksmithy | `IronIngot` (`DefBlacksmithy.cs:687-704`) | every ingot recipe (all 50 wide) | scale items (`UseSubRes2`, the dragon armor), as P61 |
| Tinkering | `IronIngot` (`DefTinkering.cs:585-597`) | tools, jewelry, parts made of ingots, e.g. wind chimes `:363` (80-130), scissors `:246` (5-55), gold ring `:400` (40-90) | wood parts (e.g. the `AddRes(... typeof(Log) ...)` at `:360`), gem and other non-ingot recipes |
| Carpentry | `Log` (`DefCarpentry.cs:597-607`; ours add the eight boards) | furniture, containers, weapons and the rest of the log recipes (`:99-204`, the tetsubo `:322`, 80-140.3) | recipes of other materials; **logs to boards is no recipe here** (`:94-97`, AOS and SE only; the axe cut at `Log.cs:84` rolls no skill) |
| Fletching | `Log` (`DefBowFletching.cs:262-270`) | bows and crossbows (`:116-128`), shafts (`:96`, 0-40), fukiya darts (`:110`, 50-90) | **kindling** (`:94`, 0-0, a cut: never teaches); arrows and bolts consume shafts, not logs (`:100`, `:104`) |

Printed by the detailed run (Frost ingots, Voidwood boards or logs):
- **Blacksmithy:** 172 recipes consume `IronIngot`. Not: the five dragon pieces (scales) and CrushedGlass (110-135, blue diamond
  and glass sword).
- **Tinkering:** 137 consume `IronIngot`. Not (15): the wood tools and parts (jointing, moulding and smoothing planes, clock frame,
  axle, rolling pin: `Log`), the assembled parts and things made of parts (axle gears, clock parts, sextant parts, clock halves,
  sextant: all 0-0), bola (60-80), potion keg (75-100), void orb (90-104.3).
- **Carpentry:** 152 consume `Log`. Not: acid-proof rope (80-130) and keg (57.8-82.8). No cut recipe exists (no Board recipe).
- **Fletching:** 19 consume `Log`. Cut: kindling (0-0). Not: arrows and bolts (shafts).

Shafts and fukiya darts are stack recipes (decision 2).

### Tinkering's caps, Lockpicking, Remove Trap

- **Trap damage** (`Engines/Craft/DefTinkering.cs:678-682`): a trap's level was Tinkering / 10 and set both `TrapLevel`
  (damage: explosion 10-30 x level, `Items/Containers/TrappableContainer.ExecuteTrap.cs:65`; dart 5-15 x level `:107`; poison
  level `:128`) and `TrapPower` (= level x 9, Remove Trap's window `Skills/RemoveTrap.cs:61`). New patch
  `P\Tinkering-trap-damage-osi.patch`: `TrapLevel` reads `ClusterFSkillClamps.TrapDamageLevel(From)`, Tinkering counted at
  most 120 (level 12). `TrapPower` still reads the whole skill. Fact K7: Tinkering 100 gives level 10 power 90; 120 12/108; 130
  12/117 (was level 13); 200 12/180 (was level 20, explosion 200-600).
- **Remove Trap rides Tinkering**, as P54 B.3 proposed, with no change of its own: a Tinkering 190-200 trap has power 171-180,
  window (power, power + 30), so Remove Trap trains to 200 on tinker traps.
- **Lockpicking: listed for a later batch, not built.** The scaling lives in pinned `Items/Containers/LockableContainer.cs:31-38`
  (lock level, required skill and max lock level all capped at 95), outside this task's files, and the Unlock spell reads the
  same required skill (`Spells/Third/Unlock.cs:66-73`), so raising it needs its own argument and facts.
- **The axe bonus** (`Items/Weapons/BaseWeapon.cs:2544`): `GetBonus(Lumberjacking, 0.2, 100, 10)`, 50% at 200 and outside the
  damage cap. New patch `P\BaseWeapon-axe-bonus-osi.patch`: Lumberjacking counted at most 100 (30%). **This one is live
  today:** extended woods already train Lumberjacking to 148 (39.6%), so those lumberjacks lose up to 9.6 points.

### "Orders that still teach me"

Only Blacksmithy has orders on this shard (searched: no tinker, carpentry or fletching order code in `C\` or `P\`), so the
agreement is the smith's: `ClusterFSmithTeaching.Teaches` reads the same `Window`, worn bonus included (K5 asserts it next to
the craft; P61's A5 still checks 38,318 cases agree).

## Part B: content-skill caps (decision 11)

Gain is not touched for Alchemy, Cooking, Tailoring, Fishing or Inscription. Two caps, one patch each, through
`ClusterFSkillClamps` like P66's:

| Cap | Uncapped code (pinned) | At 200 | OSI's value | Cap |
|---|---|---|---|---|
| Potion strength | `BasePotion.EnhancePotions`, `skillBonus = (int)(Alchemy x 10 / 33)` (`Items/Skill Items/Magical/Potions/BasePotion.cs:210`), used by `Scale` `:227, :237` | 60 | 30 at Alchemy 100 (no Alchemy power scroll in pinned's list) | Alchemy counted at most 100: 30 (`P\BasePotion-alchemy-bonus-osi.patch`) |
| Deep-water fishing finds | `Fishing.MutateType`, `(Fishing.Value - 80) / 4000` for the net, big fish, treasure map and bottle (`Engines/Harvest/Fishing.cs:15-18`, `:183`) | 3% each | 1% at Fishing 120 (OSI's High Seas fishing scroll; pinned lists Fishing under `_hsSkills`, commented out, `Items/Special/Special Scrolls/PowerScroll.cs:63-66`) | a chance that grows with Fishing counts it at most 120 (`P\Fishing-deep-water-finds-osi.patch`); the falling entries (rare fish, boots, nothing; `:19-30`) read the whole skill |

Facts (K7): EnhancePotions 18 at 60, 30 at 100, 150 and 200 (pinned 45 and 60 above 100); deep-water 0.5% at 100, 1% at 120 and
200; creatures as pinned. The axe and the fishing line are also checked in the build tree's source (the axe's damage and the
fishing harvest need tile data the test host has none of).

Cooking, Tailoring and Inscription have no cap in P54; none added.

## Part C: P61 follow-ups

1. **Orders roll among metals that still teach.** `ClusterFSmithTeaching.TeachingMetal(m, chances)`: the stock weights
   renormalized over the metals the smith can work (Base at the requirement) whose ceiling is above Base. With the even tiers
   that is exactly one metal at any Base from 112.5 to 199.9 (Frost 150 to 162.4, Obsidian 162.5 to 174.9, ...), and none
   below 112.5 or at 200, where the roll is as before. Small orders: one hunk in `P\SmallSmithBOD-teaching-orders.patch`
   (regenerated; its second hunk's header was 10 lines off and is now exact). **Large orders: cheap, built** in our full
   `P\LargeSmithBOD.cs`, the same call; the set is still picked first (stock's order), and in a teaching metal every piece the
   smith can make teaches, so it does not matter which set. The 30% and 15% upgrade chances are unchanged. Setting off:
   unchanged. Fact K6: the table from 100 to 200; at 150, 400 small orders on: post-Valorite only Frost; off: other metals too;
   400 large orders on: only Frost.
2. **Harder items teach better.** The band is (item's minimum, ceiling). Gain chance per craft (pinned's formula,
   `Skills/SkillCheck.cs:122-140`, for a smith at the total skill cap; fact K4 prints the same):

   | Item (own range) | Skill | Before (P61): window, roll chance, gain per craft | After: window, roll chance, gain per craft |
   |---|---|---|---|
   | Dagger (-0.4 to 49.6) | 150 | 112.5 to 162.5, 0.750, 0.1094 | -0.4 to 162.5, 0.923, 0.0802 |
   | Plate tunic (75 to 125) | 150 | 112.5 to 162.5, 0.750, 0.1094 | 75 to 162.5, 0.857, 0.0931 |
   | Plate battle kabuto (90 to 140) | 150 | 112.5 to 162.5, 0.750, 0.1094 | 90 to 162.5, 0.828, 0.0982 |
   | Dagger | 160 | 112.5 to 162.5, 0.950, 0.0619 | -0.4 to 162.5, 0.985, 0.0538 |
   | Plate tunic | 160 | 112.5 to 162.5, 0.950, 0.0619 | 75 to 162.5, 0.971, 0.0569 |
   | Plate battle kabuto | 160 | 112.5 to 162.5, 0.950, 0.0619 | 90 to 162.5, 0.966, 0.0583 |

   The same band for all four crafts (it is one function).
3. **Gain speed** is stock's roll over the band, no multiplier.

P61's facts updated to the band: `T\Engines\Craft\PostValoriteGainCeilingVerification.cs` A2 (e.g. 150 Frost plate now
(75, 162.5), was (112.5, 162.5); 150 Frost broadsword (35.4, 162.5)); A1, A3, A4, A5 unchanged and green in build 3.

## Part E: craft ceilings follow worn bonuses

The band's top is `ceiling + (Value - Base)` for a player (`ClusterFSkillGain.WornBonus`, the same `Value - Base` P66's
`EffectiveMax` uses), so the roll stops when **Base** reaches the ceiling and Base never passes it (at stock's 0.1 a gain; with
ClusterF's amount multiplier above 1, the last gain can pass a ceiling by up to 0.4, as it can pass any window's top today).

One trap avoided: P66's rule adds the bonus to any window whose top equals the cap. A Mythril band with a +12.5 item ends at
187.5 + 12.5 = 200 and would get the bonus twice (top 212.5, so Base would run past Mythril's 187.5 to 200). The craft roll goes
through `ClusterFSkillGain.CheckSkillWornBonusIncluded`, which sets a flag `EffectiveMax` honors. P66 decision 6 is resolved by
this: Adamantium and Celestial now carry their own bonus too.

Fact K5 (Mythril plate, real gains through pinned's SkillCheck wrapped by ours): no bonus, +10, +12.5 all gain at Base 187.4
and none at 187.5; +10 gains at 180; the window's top is 187.5 + worn; Base never passes 187.5; `Teaches` agrees.

---

## Facts (`T\Engines\Craft\CraftCeilingsVerification.cs`, 41 cases)

| Fact | What | Green (final build) | Red tree (`red2`, run) |
|---|---|---|---|
| K1 x4 | chains and no gap | green | 3 red (Tinkering, Carpentry, Fletching); Blacksmithy never red by design |
| K2 x4 + kindling | consume check | green | all 5 red (Blacksmithy too: without the consume check CrushedGlass got a ceiling) |
| K3 x16 | windows and real gains | green | 11 red (every band row); the 5 stock rows never red by design |
| K4 | harder items teach better | green | red (slid window: all equal) |
| K5 x8 | worn bonuses | green | the 5 worn rows red; the 3 no-bonus rows never red by design |
| K6 x2 | teaching metal, orders | green | both red |
| K7 x5 | the caps | green | 3 red (trap at 130 and 200; axe, potion and fishing); trap at 100 and 120 never red by design |
| P61 A2 | the band in Blacksmithy | green | 6 red (the band rows) |

`make-red.py`: the four new patches removed; `ClusterFCraftGain` back to HEAD's Blacksmithy-only slid window with no bonus and
no consume check; woods back to a flat 100; no Tinkering metals; `TeachingMetal` always None. 3 + 5 + 11 + 1 + 5 + 2 + 3 + 6 =
36, the red run's count exactly.

Printed numbers (green): K1 tables as above. K5: Base 180 + 10 worn reads 190, window 75-197.5, gains to 180.1; Base 187.4 + 12.5
reads 199.9, window 75-200, gains to 187.5; Base 187.5 + 12.5 reads 200, window 75-200, no gain. K6 at 150: 400 small orders
with the setting on, post-Valorite Frost x135 and nothing else; off, Platinum x11, Toxic x8, Blaze x5, Frost x2; 400 large orders
on, Frost x25 (every one the plate set, the fallback at 150). K7: Lumberjacking 148 axe bonus 30.0% (pinned 39.6%), 200 30.0%
(pinned 50.0%); Alchemy 150 and 200 EnhancePotions 30 (pinned 45, 60); Fishing 200 1.00% per find (pinned 3.00%); traps 100:
level 10 power 90, 120: 12/108, 130: 12/117, 200: 12/180.

## Builds

| Build | Command | Result |
|---|---|---|
| 1 | `build.sh -t sl-modernuo:cc-p67 --tests-only` | 58/58 patches; test project did not compile (my test: `SkillCheck` needs `Server.Misc`; a helper named `Main`) |
| 2 | same | 1000 tests, 993 passed, 7 failed, all mine: `GetInfo` is null for shard woods (decision 6), no Board recipe in this expansion, Skill.Base truncating 187.4 to 187.3 |
| 3 | same | **1000 tests, 997 passed, 3 failed** (K5 checked `Teaches` after the gain) |
| 4 | same | compiled; Docker Desktop crashed before the tests (status) |
| final | `build.sh -t sl-modernuo:cc-p67` on HEAD `b5fe596` | **63/63 patches, 1006/1006**, image `80c8a1fc217b` |
| red | `red2\docker\uo\build.sh -t sl-modernuo:cc-p67-red --tests-only` | 59/59 patches; 1006, **36 failed** (all P67's) |
| detail | `dotnet test` in `sl-uo-builder:cc-p67`, `CraftCeilingsVerification`, verbosity detailed | 41/41 |

P67 itself adds four patches (54 + 4 = 58 at its commit; cc-P71 added five more). No save shape changed; no migration.

## Register lines (the register ends at D-122 in `docs\fidelity-principle.md`; P66's D-123 to D-125 are proposed; next free D-126; cc-P71 has since taken D-130)

- **D-122 amended (cc-P67 A, C, E; Chase 2026-10-05 and 2026-10-06).** Crafting in a shard material (post-Valorite metals for
  Blacksmithy and Tinkering; Ironwood to Starwood for Carpentry and Bowcraft/Fletching, which now need 100, 115, 130, 140,
  155, 170, 185 and 200) can raise the craft skill past the item's own maximum, up to the next material's requirement (the last
  to the 200 cap), only when the recipe uses up the material. Past the item's maximum the roll is stock's over the item's own
  minimum to that ceiling, so harder items teach faster; worn bonuses do not stop it before Base reaches the ceiling. Success,
  failure, material loss and exceptional chance unchanged. Tinkering works the post-Valorite metals. OSI: the item's range
  only | crafts 130-200 by crafting | `visible`
- **cc-P42 G amended again:** "Orders that still teach me" also picks a Society order's post-Valorite metal among those that
  still teach the smith (small and large).
- **D-126 (cc-P67 A).** A tinker trap's damage level counts Tinkering at most 120 (level 12); its disarm difficulty still grows
  with Tinkering. OSI: the same at every value OSI allows | trap damage stops at 120 | `visible`
- **D-127 (cc-P67 A).** An axe's Lumberjacking damage bonus counts Lumberjacking at most 100 (30%). OSI: the same at 100;
  listed because Lumberjacking past 100 is ours | lumberjacks above 100 lose up to 9.6 points | `visible`
- **D-128 (cc-P67 B).** Potion strength from Alchemy counts Alchemy at most 100 (30). OSI: the same | shows only with Alchemy
  bonuses above 100 today | `visible`
- **D-129 (cc-P67 B).** Deep-water fishing finds count Fishing at most 120 (1% each). OSI: the same | shows only with Fishing
  bonuses above 120 today | `visible`

## Patch notes

`CHANGELOG.md`: 2026.10.06 is committed, so a new **2026.10.07** section; `VERSION` 2026.10.06 to 2026.10.07 (no trailing
newline, as before). Added: the three crafts climb by crafting; tinkers work post-Valorite ingots. Changed: the wood ladder;
harder items teach faster; worn bonuses no longer stop craft gains; post-Valorite Society orders come in a teaching metal; the
trap, axe, potion and fishing caps. Not published.

## Deviations and decisions for Chase

1. **The new band is slower than P61's for every item** (Part C 2 table: at 150 in Frost, kabuto -10%, plate tunic -15%,
   dagger -27% per craft). That is what "from the item's own minimum" gives: the roll chance is higher, and pinned's gain
   bonus is (1 - chance) / 2. Hard items now beat cheap ones, as asked. If you want P61's speed back with the spread, the
   place is `ClusterFCraftGain.Window` (for example the band from the item's maximum minus its width), but that is a new
   shape, not what you described.
2. **Shafts and fukiya darts teach Fletching** in a shard wood (they consume the log; `DefBowFletching.cs:96, :110`). They are
   stack recipes (`UseAllRes`): one craft uses every log of that wood in the pack, so a fletcher carrying one Voidwood log at a
   time pays one log per gain roll, against 7 for a bow. In the band their low minimums make them slow trainers (shaft 0-40
   at 190 in Voidwood: roll chance 0.95), but cheap. Say if stack recipes should be left out.
3. **The wood re-gate is visible on its own:** a GM carpenter can no longer work Ghostwood to Starwood (115 to 200). F-28's
   wood bonuses are not built yet, so today the wood only gates and teaches.
4. **Lockpicking past 95/140 is listed, not built** (pinned `LockableContainer.cs:31-38`, and the Unlock spell reads the same
   number). A later batch.
5. **Lumberjacking's own climb** (P54 B.3: raise the extended woods' harvest max, Voidwood 205, Starwood 220) is not in this
   brief and not built; Lumberjacking still stops at 148. The axe cap ships anyway and takes up to 9.6 points from lumberjacks
   at 101-148 today (D-127).
6. **Bug for the list:** `CraftResources.GetType` (`C\ResourceInfo.cs:1092-1097`) ends the Wood range at Frostwood, so
   `GetInfo`, `GetIndex` and everything keyed on them return nothing for Ironwood to Starwood (names, hues and attributes looked
   up that way). `GetFromType` uses its own table and works, which is all this task needs. Belongs with F-28.
7. **OSI tops chosen:** Tinkering and Fishing 120 (OSI's power scrolls that pinned does not carry), Lumberjacking and Alchemy
   100 (no scroll). P66's rule read pinned's list only; by that rule Tinkering and Fishing would be 100. Chase's later wish for
   "appropriate levels at 200" (P71) was for five other effects; these four follow the brief's caps. Say if any should scale.
8. **Docker** (2026-10-07): it crashed during build 4; I quit it and left the stale socket for Chase, who brought it back.
9. **Large orders at 150 are always the plate set** (K6: 400 of 400): with nothing teaching, `PickSets` falls back to the set
   with the highest lowest maximum, and about 6% of them become Frost (the 15% upgrade applies only when stock's colored roll
   is not iron). Reordering the set pick to see the metal first (P61 decision 4) is still open; this rule does not need it.

## For Chase

Already done: Docker is back and the work is committed (`a6e17fd`). Windows PowerShell:

1. Deploy (cc-P71's image is newer and contains P67; if you deploy P71's, skip this): `docker tag sl-modernuo:cc-p67
   sl-modernuo:latest`, then `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -Down` and
   `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild`. The log should say `[ClusterFMiningExtension] Tinkering
   sub-resources registered: Platinum through Celestial.`

In game on the test shard:

2. Carpentry: `[SetSkill Carpentry 150`, Frostbark boards: make stools; Carpentry rises. At 155 no more; Shadowbark gains
   again. At 99.9 the Ironwood entry says "You cannot work this strange and unusual wood."
3. Fletching 150 with Frostbark logs: bows gain. Kindling never does.
4. Tinkering: the material list shows Platinum to Celestial. At 150 with Frost ingots, scissors gain; at 162.5 they stop.
5. Worn bonus: Blacksmithy 180 with a +10 Blacksmithy item, Mythril plate: gains until your base skill reads 187.5.
6. Orders: Blacksmithy 150, "Orders that still teach me" on: ask the Society guildmaster for orders; every post-Valorite one is
   Frost. Turn it off: Platinum, Toxic and Blaze appear again.
7. Traps: Tinkering 200, an explosion trap on a box: the blast is no bigger than a 120 tinker's. Remove Trap still finds it hard.
8. An axe at Lumberjacking 148 hits like one at 100.
9. Promote to `docs\`: the D-122 amendment, the cc-P42 G amendment, D-126 to D-129; decision 6 as a bug.

P67 DONE
