# cc-P66: gain paths 1, clamps first (batch X) and the shared gain hook G

Builder task, 2026-10-06. Brief: `D:\UO\cc-prompts\cc-P66-clamps-and-hook-g.md`. Engine authority: `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88` (`git rev-parse HEAD` today); every pinned file:line below is against it, paths
relative to `Projects\UOContent\`. `C\` = `D:\ShatteredLegacy\server\customizations`, `P\` = `server\patches`, `T\` =
`server\tests`. Scratch: `D:\UO\cc-p66-work\` (`make-patches.py` writes the seven patches from LF copies of pinned with the
earlier patches applied; `count-keys.py` checks the row-key counts against a simulated build tree; `make-red.py` the red tree;
`build1.log` to `build-final.log`, `red1.log`, `detail.log` the printed numbers).

Shard HEAD `29db3d5`, tree clean when I started. Nothing committed, nothing deployed, no shard restarted, `docs\` not
touched, `sl-modernuo:latest` not moved (`daa499b0941b` before and after).

**Order:** the brief says P66 runs after P65. P65 (`cc-P65-evo-pets-framework.md`) has not run: its prompt is still outside
`cc-prompts\completed\` and there is no P65 notes file. Chase asked for P66 directly and the tree was clean. P65's prompt names
none of the files touched here (grep for ClusterFSkillGain, skill names, CHANGELOG, VERSION: no hits), so the only shared
file is `CHANGELOG.md`/`VERSION`, and whoever runs P65 adds to the 2026.10.06 section if it is still uncommitted.

## Headlines

1. **Both parts done.** Final `docker\uo\build.sh -t sl-modernuo:cc-p66`: **54/54 patches** (47 plus 7 new), **959/959
   shard facts** (876 before plus 83 new), image `sl-modernuo:cc-p66` = `97555b28ef96`.
2. **Red then green.** Red tree (`make-red.py`: the seven patches removed, the hook's three new behaviours switched back to
   HEAD's, every API kept): **33 failed / 926 passed**, and the 33 are exactly the new facts that should fail (all eight
   Part A cases, all 19 hook G rows, G2 to G6, and the one row-key line the Detect Hidden patch carries). Printed numbers
   below are from both trees.
3. **Part A: seven clamps, every one at OSI's own top.** Each patched pinned line reads a player's skill through
   `C\ClusterFSkillClamps.cs`, which counts it at most at OSI's highest Value (the power-scroll cap, else 100). Creatures
   are untouched, and nothing changes at or below OSI's range (facts at 100 and 120 show pinned's numbers on both trees).
   Today's live exploit, measured on the red tree: **block chance 0.950** at Parry 200 / Bushido 120 / Evasion / a two-hander
   (now 0.600036, OSI's own top). Stealing: a 127.5 thief with +22.5 worn **was never caught** (now as at 120).
4. **The guard half of item 2 needs no clamp, because guards reveal nothing.** Probed: a warrior guard's Reveal runs Detect
   Hidden, which opens a target cursor (`Skills/DetectHidden.cs:33`), and nothing ever answers a guard's cursor (BaseGuard is
   a Mobile, not a BaseCreature, so no AI handles it). A guard adjacent to a **Hiding 0** hider leaves them hidden. cc-P54's
   "guards blind from Hiding 121" was read, not probed; guards are blind at every Hiding, in pinned and in ServUO pub57 alike.
   Decision 1.
5. **Part B: hook G is in, for all 17 skills, none of the casting schools.** Below each use's stock maximum the hook does
   nothing; at or past it, a gain-only roll on (row min, Cap + worn bonus). Detect Hidden gains past 100 only from a scan that
   **found** a hider, a trapped chest or container, or a hidden floor or faction trap. The worn-bonus rule (decision 7) is in
   the same hook. `SkillEvents.SkillUsed` now fires **once** per use (red tree: 3 with ClusterF's 3 attempts).
6. **Two brief counts were wrong, checked by counting:** the Musicianship reduction lives in **three** bard files, not
   "BaseInstrument plus two" (BaseInstrument has no reduction; it carries the Musicianship gain roll, a G row). The "five cap
   uses" are **four** call sites (`C\Meditation.cs:115`, `Items/Weapons/BaseWeapon.cs:2524, :2527`, `Spells/Base/Spell.cs:625`);
   the rule here reaches every call whose maximum is the cap, which is also `MagerySpell.cs:55, :82`, `MysticSpell.cs:121`
   (gated below 111, so moot) and `BaseWeapon.cs:2597, :2600` (pre-AOS, dead).

---

## Part A: batch X, clamps first

**The rule, once.** A pinned effect that reads a player's skill with no upper bound becomes certain or immune when skill
passes OSI's top. OSI's top Value: the power-scroll cap where one exists (`Items/Special/Special Scrolls/PowerScroll.cs:9-54`:
Parry :18, Magic Resist :25, Musicianship :29, Stealing :40, Bushido :48, all 120), else 100 (Hiding, Detect Hidden,
Tracking). On OSI an item bonus stops at the cap (`Misc/AOS.cs:1357-1358` builds item mods with ObeyCap; D-113 lifted that
here), so the cap is also OSI's top Value. Each clamp counts a **player's** skill at most at that top **for that effect
only**; the skill itself still grows and every other use reads the whole skill. Creatures read as pinned, so ServUO's
creatures above OSI's tops are unchanged.

**Alternatives argued (once for all seven; also in `docker\uo\apply-patches.sh`):** clamping the skill everywhere (rejected:
the skills are meant to grow past OSI, only these effects break); customizations alone (impossible: each line is inside a
pinned method or a private target class with no hook); clamping creatures too (rejected: changes ServUO creature behaviour,
e.g. a Kepetch Ambusher with Hiding 125). Each patch is one or two lines that call `ClusterFSkillClamps`, so the values and
their reasons live in one file of ours.

| # | Exploit (pinned line) | OSI value | Clamp (patch) | Fact (T\Skills\SkillClampsVerification.cs), red tree -> green |
|---|---|---|---|---|
| 1 | **Stealing's caught test**: `caught = Stealing.Value < Random(150)` (`Skills/Stealing.cs:337`). Gear (D-113) takes a 127.5 thief to 150: never caught | Stealing 120: caught 1 in 5 (rolls 121-149) | `Stealing-caught-osi-skill.patch` (applied after cc-P57's stack patch, same file): a player counts at most 120 | X1, rolls 101/110/121/125/149: 127.5 + 22.5 worn caught **F F F** (red) -> **F F T T T**, identical to a 120 thief; 100 and 120 as pinned on both trees |
| 2 | **Hiding's combat range**: `min((100 - H) / 2 + 8, 18)` (`Skills/Hiding.cs:53`), negative from 118, so a combatant never blocks | Hiding 100: range 8 | `Hiding-combat-range-osi.patch`: a player counts at most 100 | X2: Hiding 150, combatant 5 tiles: hidden **True** (red) -> **False**; 9 tiles hides; Hiding 100 as pinned |
| 2b | **Guard reveal**: cc-P54 read "blind from 121" (`ArcherGuard.cs:64, :159`, `WarriorGuard.cs:81, :170`) | n/a | **none**: guards reveal nobody (probe below) | `T\Skills\GuardRevealProbe.cs`: guard's UseSkill(DetectHidden) True, its target `DetectHidden+InternalTarget`, a Hiding 0 hider still hidden |
| 3 | **Detect Hidden radius**: `(int)(DH / 10)` (`Skills/DetectHidden.cs:145`): 20 tiles at 200, past the screen | DH 100: 10 tiles | `DetectHidden-osi-radius-found-gain.patch` hunk 1: the radius counts a player at most 100; the hider contest (`:197-198`) still reads the whole skill | X3: DH 200, hider 15 tiles: revealed **True** (red) -> **False**; 9 tiles found; DH 100 as pinned |
| 4 | **Musicianship reduction**: `diff -= (Mus - 100) / 2`, uncapped (`Skills/Peacemaking.cs:164-169`, `Provocation.cs:133-138`, `Discordance.cs:155-160`): 50 off at 200, 40 more than OSI's top allows, so certainty at bard 125/130 instead of 165/170 | Musicianship 120: 10 off | `Bard-musicianship-reduction-osi.patch` (three files, one patch): a player counts at most 120 | X4, all three skills, the same two mongbats per run: red, Peacemaking at Mus 100 -27.72..22.28, at 200 **-77.72..-27.72 (50 below)**; green, at 100 -26.83..23.17, at 120, 150 and 200 **-36.83..13.17 (10 below)**. 100 -> 120 is -10 on both trees (each run's mongbats roll their own difficulty) |
| 4b | **Block chance**: `CheckParry` (`Items/Weapons/BaseWeapon.cs:1491-1574`) | the highest pinned gives at OSI's tops: Parry 120, Bushido 120, Evasion with GM Anatomy and Tactics (`Spells/Bushido/Evasion.cs:175-205`, scalar 1.5), two-hander: **0.600036** | `BaseWeapon-block-chance-osi.patch`: both `CheckSkill(Parry, chance)` returns pass a player's chance through `BlockChance`, at most 0.600036 | X5: Parry 200 / Bushido 120 / Evasion / Bardiche **0.950061** (red) -> **0.600036**; Parry 120 / Bushido 120 0.600036 both trees; Parry 100 / Bushido 100 0.293072 both; shield at Parry 200 0.55 both |
| 5 | **Tracking radius**: `10 + (int)T / 10 * 10` (`Skills/Tracking/Tracking.cs:166`): 210 tiles at 200 | Tracking 100: 110 tiles | `Tracking-radius-osi.patch`: a player counts at most 100 | X6 (source and value fact: the radius is only observable through a client gump): the build tree's line reads the clamp (red: absent), Tracking 200 counts 100, 90 counts 90 |
| 6 | **Nether Cyclone**: drain `(M + I) / 1200 - R / 800` (`Spells/Mysticism/NetherCycloneSpell.cs:81`): from Resist 160 a 120/120 mystic's drain goes negative (gives stamina and mana) | Resist 120 | `NetherCyclone-resist-osi.patch`: a player victim's resist counts at most 120 | X6: line present (red: absent), Resist 200 counts 120, drain against a 120/120 mystic 0.05 >= 0; a creature's 150 counts 150 |

Rows 5 and 6 are not in the brief's Part A list; cc-P54 B.3 names both as the clamp that must ship with the Tracking and
Resisting Spells G rows, which this task opens, so they are here. A known pinned quirk is left as it is: Nether Cyclone's
drain is negative **inside** OSI's range too (Mysticism 83 + Focus 0 against Resist 120: 0.069 - 0.15), so the clamp keeps
pinned's behaviour at every value OSI allows and only stops a resister past 120 making it worse.

**The guard probe, and a mistake caught.** My first version of `GuardRevealProbe` passed for the wrong reason:
`UseSkill` returned **False** because the test host never registers Detect Hidden's skill handler (`DetectHidden.cs:25-28`
is an `Initialize` the fixture does not call), so the probe never reached the code it claimed to test. The detailed run
printed it; the probe now calls `DetectHidden.Initialize()` as the server does and asserts the cursor was opened. Final
output: `guard UseSkill(DetectHidden) returned True; guard target Server.SkillHandlers.DetectHidden+InternalTarget; hider
(Hiding 0) hidden True`. ServUO pub57's guards make the same call (`Scripts\Mobiles\NPCs\WarriorGuard.cs:356`,
`ArcherGuard.cs:325`); ServUO answers the cursor only in `MageAI` (`Scripts\Mobiles\AI\MageAI.cs:1593-1597`), which guards
do not use.

What still reveals a high hider: players with Detect Hidden (the contest reads the whole skill, and DH now climbs with Hiding,
Part B), and creature AI, whose chance keeps a floor of DH / 10 (`Mobiles/AI/BaseAI/BaseAI.cs:1151-1153`). That floor means
no hider is immune to creatures, but the chance falls: a DH 100 creature against Hiding and Stealth 200 is 14 percent a
check, against 49 percent at 100/100. Not clamped (it is a falling chance, not an immunity); listed for Chase.

---

## Part B: hook G (`C\ClusterFSkillGain.cs`)

**What changed in the file.** It still wraps pinned's four handlers (`Skills/SkillCheck.cs:33-40`). Three jobs now:

1. **Rate, unchanged in effect.** The first attempt is pinned's handler. ClusterF's further attempts call pinned's public
   `SkillCheck.CheckSkill` (`:108`) with the same window, instead of re-running the handler, so **`SkillEvents.SkillUsed`
   (raised only by the four handlers, `:52, :87, :174, :207`) fires once per use** (fact G6: 1; red tree: 3). Each attempt's
   chance is recomputed from the current Value, as the re-run handler did. The amount multiplier is as before.
2. **Worn bonuses (decision 7).** For a player, any call whose maximum is the skill's own cap is tested against
   `Cap + (Value - Base)`, so a worn bonus no longer stops it before Base reaches the cap. Every such call is a gain-only roll
   (list in headline 6). Done in the hook rather than three pinned patches: one rule, no upstream lines touched, and it also
   catches a cap-following call added upstream later. The cost is that it keys on `max == Cap`, which a literal maximum can
   equal by coincidence: on this shard only our Blacksmithy craft windows that end at exactly 200 (cc-P61's Adamantium and
   Celestial ceilings) do, and those are gain-only too, so they now behave the same way (decision 6).
3. **Hook G (decision 8).** After the stock result, if the caller is a player, the call's Value is at or above its stock
   maximum (pinned "no challenge", `SkillCheck.cs:65-67, :187-189`), the call matches a row, and Base is below the cap: one
   gain-only roll through `SkillCheck.CheckSkill` on (row min, row max + worn bonus), then ClusterF's further attempts when its
   rate is on. The use's own outcome is the stock one. Its own switch, `clusterf.skillGain.pastStockCeiling` (default true),
   independent of ClusterF's rate switch, so the live x1 rate (decision 17) keeps the paths. Anti-macro keys are pinned's
   (a `Point2D` for location rows, `:72-73`; the target for target rows).

**Rows** (`ClusterFSkillGain.TryRow`; every key a pinned literal, pinned by `T\Skills\SkillGainRowKeysVerification.cs`).
Chances are fact G1's printed values (row min, Cap 200, no bonus).

| Skill | Stock call(s) and ceiling | G rule | Chance at stock top / at 150 |
|---|---|---|---|
| Hiding | `Skills/Hiding.cs:73` location (0, 100); friend's house (-100, 0) stays stock | (0, Cap) | 0.50 / 0.75 |
| Stealth | `Skills/Stealth.cs:96-100` (-20 + 2AR, 60 + 2AR), AR < 42 (:91): 142 | from Value 142 only, any armor: (stock min, Cap). Below 142 the armor ladder is stock | AR 0: 0.736 at 142; AR 41: 0.580 at 142 |
| Detect Hidden | `Skills/DetectHidden.cs:151, :175` (0, 100): 100 | not a table row: the patched scan calls `DetectHiddenFound` when it **found** something; chance Value / (Cap + bonus) | fact G3 |
| Snooping | `Skills/Snooping.cs:84` target (0, 100) | (0, Cap) | 0.50 / 0.75 |
| Poisoning | `Skills/Poisoning.cs:124` target, the potion's window: Greater (60, 100), Deadly/Darkglow/Parasitic (95, 100) | (potion min, Cap); Lesser and Regular never qualify | Greater 0.286 / 0.643; Deadly 0.048 / 0.524 |
| Healing, Veterinary | `Items/Skill Items/Misc/Bandage.cs:444-445` (0, 120), result discarded | (0, Cap); creature self-heals (60-90) excluded | 0.60 / 0.75 |
| Begging | `Skills/Begging.cs:111` target (0, 100) | (0, Cap) | 0.50 / 0.75 |
| Forensics | `Skills/ForensicEval.cs:36` (40, 100), `:54` (0, 100) | (stock min, Cap) | 0.375 / 0.688; 0.50 / 0.75 |
| Animal Lore | `Skills/AnimalLore.cs:59`, `AnimalTaming.cs:372, :393` target (0, 120) on a creature | the creature's own tame window, Taming's with no owners (`AnimalTaming.cs:396-406`): (MinTameSkill - 0.1, MinTameSkill + 49.9). A rabbit trains nothing | Raptor (107.1): 0.26 at 120, 0.86 at 150, nothing from 157 |
| Musicianship | `Items/Skill Items/Musical Instruments/BaseInstrument.cs:528` (0, 120), every bard use | (0, Cap), only with clamp 4 | 0.60 / 0.75 |
| Tracking | `Skills/Tracking/Tracking.cs:163` (21.1, 100), after a successful track | (21.1, Cap), with clamp 5 | 0.441 / 0.721 |
| Taste ID | `Skills/TasteID.cs:37` target (0, 100), food only | (0, Cap) | 0.50 / 0.75 |
| Camping | `Items/Skill Items/Camping/Kindling.cs:38` (0, 100) | (0, Cap) | 0.50 / 0.75 |
| Resisting Spells | `Spells/Base/SpellHelper.cs:371`, `Spells/Necromancy/PainSpike.cs:59`, `MindRot.cs:58`, `CorpseSkin.cs:70`, `BloodOathSpell.cs:82`, all (0, 120), gain-only; the sixth (0, 120) call, `Items/Skill Items/Misc/FireHorn.cs:175`, runs only pre-AOS | (0, Cap), with clamp 6 | 0.60 / 0.75 |
| Bushido | `Spells/Bushido/MomentumStrike.cs:67` (RequiredSkill 70, 120), a second-target hit | (70, Cap), with clamp 4b | 0.385 / 0.615 |
| Stealing | `Skills/Stealing.cs:285-304, :316` (weight x 10 - 22.5, + 27.5), at most 10 stones since cc-P57: 127.5 | only the full 10-stone steal, (77.5, Cap), with clamp 1 | 0.408 at 127.5 / 0.592 |

Not rows (fact G7): Magery, Necromancy, Chivalry, Spellweaving, Mysticism at their top windows. Chase: their path above
about 120 is a Training Ward or a quest line.

**Order kept:** Hiding, Detect Hidden and Stealing rows ship in the same build as clamps 1, 2 and 3, and the red tree shows
each clamp's fact red without its patch.

**Detect Hidden and traps (Chase's addition).** Pinned's trap-reveal paths, all routed into the same roll by one call at the
end of the scan (`DetectHidden.cs:257`, patched: `else { ClusterFSkillGain.DetectHiddenFound(src); }`):
- **Treasure chests and trapped containers:** targeting any `TrappableContainer` with a trap (`DetectHidden.cs:147-163`):
  every treasure-map chest, paragon chest, dungeon chest and fillable container (`TreasureMapChest`, `ParagonChest`,
  `BaseTreasureChest`, `FillableContainer`, `TreasureChestLevel1-4`, all `LockableContainer`), our Shame chests
  (`C\Items\Containers\TreasureChestMod.cs`, `MagicTrap`) and a tinker's own trapped box.
- **Floor traps:** the area scan's hidden `BaseTrap`s (`:234-252`; High Seas needs DH 75, `:237`). In pinned only
  `FlameSpurtTrap` starts hidden (`Items/Traps/FlameSpurtTrap.cs:16`); faction traps too (`:217-233`, its own (80, 100) roll).
- **Not routed (no player action, no gain call):** a faction trap revealing itself to a passer-by
  (`Engines/Factions/Items/Traps/BaseFactionTrap.cs:173`) and passive player detection (`:61-128`).
Fact G3, DH 150: a scan that finds nothing 150 -> 150; one that reveals a hider 3 tiles off 150 -> 150.1; targeting a trapped
metal box 150 -> 150.1 (red tree: 150 for all three).

**Facts (`T\Skills\SkillGainPastStockCeilingVerification.cs`, P54 B.5's list, the hook installed over pinned's handlers,
rolls held at 0):** G1, a theory over the 19 stock calls the rows key on: (a) at the stock maximum - 0.1 hook G rolls nothing,
so the roll is pinned's own; (b) at the stock maximum and at 150 it rolls below certainty and a use raises Base; (c) at
Base = Cap nothing, and Base stays at the cap; (d) a worn +15 at Base 185 reads 200 and still rolls and gains; (e) a creature
gets nothing. G2 Musicianship 150 playing gains (150 -> 150.1; red 150); Lore keys on the creature. G3 above. G4 a 10-stone
steal at 150 gains (red: no). G5 Tactics 185 + 15 worn, the `BaseWeapon.cs:2524` call: 185 -> 185.1 (red 185); at 200 none.
G6 SkillUsed once. G7 the schools. **Row keys:** 45 lines, each asserting the exact text in its pinned file **and** how many
times it appears in all of `Projects/UOContent` (customizations included), so an upstream change to a number, or a new use
with the same key, stops the build; counts checked first against a simulated tree (`count-keys.py`, 45 of 45). **P53's Part C
facts** (`SkillBonusAboveCapVerification`, 4) re-run green in the same suite.

---

## Build

```
& "C:\Program Files\Git\bin\bash.exe" docker/uo/build.sh -t sl-modernuo:cc-p66
```

Final: `[patches] All 54 patches applied successfully.`, `Total tests: 959, Passed: 959`, `Built sl-modernuo:cc-p66 with
patches applied and 959 shard test(s) passing.`, image `97555b28ef96`. Red tree (`D:\UO\cc-p66-work\red1`, same command with
`-t sl-modernuo:cc-p66-red`): 47 patches, 959 tests, **33 failed**, no image. Five builds of the real tree in all: the first two failed
on my own facts (the bard fact made new mongbats per call, whose rolled stats change their difficulty; the block fact equipped
a weapon with no layer, because the test host loads no tile data), the third was green, the fourth carries the corrected guard
probe, and the fifth only three comment corrections (the Musicianship figure, below), so the image matches the tree.

## Register lines (the register ends at D-122; P62 to P65 added none)

| D-123 | **Ours (cc-P66 B, Chase 2026-10-05, decision 8).** Hiding, Stealth, Detect Hidden, Snooping, Stealing, Poisoning, Healing, Veterinary, Begging, Forensic Evaluation, Animal Lore, Musicianship, Tracking, Taste Identification, Camping, Resisting Spells and Bushido keep gaining by use past their stock ceiling (100, 120, Stealth 142, Stealing 127.5) up to the cap; below it the roll is stock's. Detect Hidden past 100 gains only when a scan finds a hider or a trap; Animal Lore past 120 on the creature's tame window. OSI: no gain once a use is no challenge | these skills train to 200 | `visible` | `cc-P66` B |
| D-124 | **Ours (cc-P66 B, Chase 2026-10-05, decision 7).** A use whose gain window ends at the skill's cap (Tactics, Anatomy, Evaluating Intelligence, Spirit Speak, Meditation and the like) tests against cap plus worn bonuses, so skill items no longer stop gains before the cap. OSI: worn bonuses count, so a +15 item stops those gains 15 below the cap | no need to strip gear to train | `visible` | `cc-P66` B |
| D-125 | **Ours (cc-P66 A, Chase 2026-10-05, decision 9).** Seven effects count a player's skill at most at OSI's top Value: Stealing's caught chance (120), Hiding's combat range (100), Detect Hidden's radius (100), Musicianship's bard-difficulty reduction (120), the final block chance (0.600036, OSI's highest), Tracking's radius (100), resist against Nether Cyclone's drain (120). Creatures as stock. OSI: the same at every value OSI allows; listed because skill past OSI's tops is ours (the 200 cap and D-113), and a player there sees these stop growing | high skill never makes these certain | `visible` | `cc-P66` A |

---

## Deviations and decisions for Chase

1. **Guards reveal no hider at all** (Part A, probed; pinned and ServUO alike). So nothing to clamp, and Hiding past 100
   changes nothing about guards. Whether OSI's guards reveal hidden criminals is unverified. A fix (answer the guard's cursor
   with its own Detect Hidden scan, as ServUO's MageAI does for mages) would be ours and is not built. Yours: leave, or queue it.
2. **Detect Hidden's radius is clamped at OSI's 10 tiles**, as the brief says, not cc-P54's alternative of 18 (the screen).
   So DH past 100 buys a better contest against hiders and a trap-reveal gain, not reach.
3. **The block cap takes something live away.** Today a Parry 200 / Bushido 120 player with Evasion and a two-hander blocks
   95 percent of weapon hits (one-hander 82.5); now 60. Shield users are untouched (Parry 200 with a shield is 0.55, under the
   cap). Players only.
4. **Not clamped, opened or grown by this task** (each from cc-P54 B.3 or found here; none an immunity, so left for you):
   - Nerve Strike's paralysis is certain from Bushido 137.5 (`Items/Weapons/Abilities/NerveStrike.cs:66`; OSI's top 90
     percent); cc-P54 listed it with the Bushido row. A one-line clamp like the others if you want it.
   - Stable slots from Lore and Veterinary 200: cc-P54 counts 5 + 11 + 11 + 11 = 38 at 200/200/200 against 17 today
     (`Mobiles/Vendors/NPC/AnimalTrainer.cs:58-97`); with Taming still stopping near 157, about 33. cc-P54 put the clamp in
     batch T.
   - Fire Horn damage reads Musicianship (1/8 of the weight, `Items/Skill Items/Misc/FireHorn.cs:125-130`): about +17 percent
     PvM per blast at Musicianship 200 (cc-P54).
   - Creature AI against high hiders: a DH 100 creature finds Hiding and Stealth 200 14 percent a check against 49 percent at
     100/100 (floor DH / 10 stays).
   - Stealth steps grow with Value (40 at 200 against 28 at 142), Healing per bandage grows (cc-P54: 57.5 average at 120/120,
     93.2 at 200/200).
5. **Animal Lore stops at 157 until there are harder tames.** Its window is the creature's tame window and the hardest tame
   on the shard is the Raptor, 107.1. Batch T's MinTameSkill 150.1 creature gives the window to 200.
6. **The worn-bonus rule keys on "maximum equals the cap".** It reaches the four named uses and every other gain-only call
   that passes the cap (headline 6), and, by coincidence, Blacksmithy craft windows that end at exactly 200 (cc-P61's Adamantium
   and Celestial ceilings), which are gain-only too. A craft ceiling below 200 (Mythril 187.5) still stops at ceiling - bonus.
   Say if you want craft ceilings to follow worn bonuses too.
7. **Hook G has its own switch** (`clusterf.skillGain.pastStockCeiling`, default true, written to `modernuo.json` on the first
   start) and runs whether ClusterF's rate is on or off, so the live x1 rate keeps the gain paths.
8. **Stealth past 142 trains in any armor**, and **Stealing past 127.5 only on 10-stone steals**: the floors cc-P54 set, so the
   armor ladder and the heaviest steal keep meaning below them.
9. **Bug for the list:** guards' Reveal does nothing (decision 1); kind: pinned's and ServUO's alike, so ours to fix only if
   you want it. Also a test-host fact for later builders: items get no layer (no tile data), and skill-use handlers registered
   in an `Initialize` (Detect Hidden) are not registered.

## For Chase

Deploy (after you commit; Windows PowerShell, `;` between commands):

```
cd D:\ShatteredLegacy; git status --short
docker tag sl-modernuo:cc-p66 sl-modernuo:latest
```

Then restart the test shard the usual way. The server log should say `[ShardVersion] Shattered Legacy 2026.10.06 ...` and
`ClusterF skill gain: rate enabled, 3 chance attempt(s), 5x gain amount; past stock ceilings on.` (rate as your config has
it). `modernuo.json` gains `clusterf.skillGain.pastStockCeiling: true`. Do not publish the wiki page (not asked).

In-game checklist (a staff character can set skills with `[set` on itself; test as a player account where noted):

1. Hiding: set Hiding 150, attack a monster, step 5 tiles away and hide: "You can't seem to hide right now." At 9 or more
   tiles it works. Hide repeatedly away from fights: Hiding rises past 100.
2. Detect Hidden 150: search an empty spot several times, no gain; have a second character hide nearby, search, they are
   revealed and Detect Hidden can rise. Target a trapped treasure chest: "[trapped]" and a gain chance. Hiders 15 tiles away
   are not found.
3. Stealing: a 127.5 thief with Shadow Dancer Leggings (+20) or Animal Form: steal repeatedly from a monster's pack; you
   are sometimes caught (about 1 in 5 rolls once past 120).
4. Musicianship 200 bard: Peacemaking a hard creature is no easier than at Musicianship 120. Play an instrument: Musicianship
   rises past 120.
5. Block: Parry 200, Bushido 120, Evasion, a two-handed weapon: you no longer block nearly every hit.
6. Tactics 185 with a +15 Tactics item worn: fight and watch Tactics still rise toward 200.
7. `[ClusterFSkillGain` (admin): reports the rate and "past stock ceilings on".

P66 DONE
