# cc-P54 slice b: Animal, Bard and Misc skills, gain ceilings vs the 200 cap

Scope: Animal Taming, Animal Lore, Herding, Musicianship, Peacemaking, Provocation, Discordance, Tracking,
Item Identification, Taste Identification, Camping, Cartography (12 skills).

Authority: pinned ModernUO `D:\UO\ModernUO-pinned` at d4531cd94b739613155225c234900de9f47d2c88 (checked with
`git rev-parse HEAD`). Pinned paths are relative to `Projects\`. `C\` = `D:\ShatteredLegacy\server\customizations`,
`P\` = `D:\ShatteredLegacy\server\patches`. Read-only research; nothing built or run.

Gain rule used (pinned `UOContent\Skills\SkillCheck.cs`): range checks return false with no roll when
Value < min (:62, :184) and true with NO gain roll when Value >= max (:67, :189). Direct-chance checks return
true with no roll at chance >= 1.0 (:100, :220). A gain needs Base < Cap (:248). All of these compare
**Value** (Base plus skill mods), not Base. Since cc-P53, item skill bonuses go above the cap
(`P\PlayerMobile-skill-bonus-above-cap.patch`, `C\ClusterFSkillBonusAboveCap`), so any worn bonus
(Outrider crooks +5/+10/+15 Taming and Peacemaking, +10 Lore at `C\OutridersCrook.cs:82, :83, :85`;
Mark of Travesty +10; Mapmaker's Glasses +1..5) lowers the **Base** at which a use stops gaining by the
bonus amount. Ceilings below are Value ceilings.

Shard wrapper: `C\ClusterFSkillGain.cs:36-47` replaces all four `Mobile.SkillCheck*Handler`s; each wrapper
(`:63`, `:70`, `:77`, `:90`) calls the pinned handler with the same min/max/chance through
`RunBoostedCheck` (`:97`), up to 3 attempts and 5x amount, gated by Base < Cap (`ShouldBoost`, `:141-147`).
It never changes min, max or chance, so it never moves a ceiling. Confirmed.

Our code has **no** gain call for any of the 12 skills. Grep of every `CheckSkill`, `CheckTargetSkill`,
`CheckDirect*`, `SkillCheck.*` in `C\` and `P\` (tests excluded): the only calls are Imbuing
(`C\ArtificersImbueGump.cs:1485, :1563, :1625`), Blacksmithy (`C\ClusterFSmithBODSystem.cs:281`,
`C\ClusterFSmithCommissions.cs:658, :729`), Meditation (`C\Meditation.cs:115`; the brief's ":92" has moved
to :115) and the regen replacement (`C\RegenRates.cs:41`). No patch in `P\` touches AnimalTaming, AnimalLore,
BaseInstrument, Peacemaking, Provocation, Discordance, Tracking, ItemIdentification, TasteID, Kindling,
FireHorn, ShepherdsCrook or TreasureMap (grep of all 50 files in `P\`). Every call below is pinned and
unpatched, except the craft path (pinned `CraftItem.cs`, patched by `P\CraftItem-shard-hooks.patch`,
whose only `GetSuccessChance` hunk adds a DevTestingCrystal bypass at the top; min/max untouched).

Work orders (`C\ClusterFWorkOrderSystem.cs:151, :183`) gate on Taming (29 to 99), Lore (20, 30) and
Tracking (30) but contain no gain call (0 `CheckSkill` in the file). Guild gate
`C\ClusterFGuildSystem.cs:161` (Musicianship 30): gate only.

Pinned search: all `Check*Skill` calls in `UOContent` and `Server` naming one of these skills, plus every
call that passes a skill variable (19 sites, read one by one: craft `CraftItem.cs:893`, `Repair.cs:75`,
`HarvestSystem.cs:147`, `ArcheryButteAddon.cs:185`, `TrainingDummies.cs:67`, `Bandage.cs:444-445`,
`NinjaWeapons.cs:274`, `BaseWeapon.cs:1340`, `RegenRates.cs:41`, `Stealing.cs:285, :300`, `Stealth.cs:96`,
`SpecialMove.cs:179`, `Spell.cs:625, :628`, `MomentumStrike.cs:67`, `SamuraiMove.cs:9`, `NinjaMove.cs:9`).
Only `CraftItem.cs:893` (Musicianship as a carpentry secondary, Cartography as main) and `Bandage.cs:444`
(Animal Lore as the Veterinary secondary) reach this group. No direct `SkillCheck.Gain` call in pinned.

Hardest targets that exist (re-verified on d4531):
- Highest MinTameSkill: **107.1, pinned `UOContent\Mobiles\Monsters\Reptile\Raptor.cs:38`**. (P20 cited a shard
  `Raptor.cs:50`; that file is gone. Raptor is pinned now, extended by `P\Raptor-pack-friends.patch`.)
  Next: Fire Steed 106.0 (`FireSteed.cs:42`), Greater Dragon 104.7. Ours: highest 102.0 (Dimetrosaur, Najasaurus,
  Saurosaurus, `C\Mobiles\Normal\*.cs:43/41/44`), then Skree 95.1. No code changes MinTameSkill at runtime (grep).
- Tame owners: refused at `Owners.Count >= MaxOwners` (`AnimalTaming.cs:170, :323`), `MaxOwners = 5`
  (`Mobiles\BaseCreature.cs:169`), so at most 4 prior owners (+24).
- Bard difficulty: `GetBaseDifficulty` hard-caps at 160 under SE (`BaseInstrument.cs:299-301`); it is static,
  no override hook. `GetDifficultyFor` (`:307`): exceptional -5, each slayer slot -10 if it slays, +10 if the
  target is in an opposing super-slayer group. Only three items carry two slayers (Gwenno's Harp
  Repond+ReptilianDeath, Iolo's Lute Silver+Exorcism, one Tokuno greater artifact that is a weapon).
  For +20 a creature would have to be super-slain by both opposing groups (undead and arachnid, or humanoid and
  elemental/fey); I found none (not exhaustive: **unverified**). So practical max D = **170** (single opposing
  slayer), theoretical 180. P20 used 180.
- Creatures at the 160 cap (P20's s5 CSV, parsed at the older commit 7c9215d97, not re-run: unverified on
  d4531): 70 of 694 (36 pinned, 34 ours); 64 calmable, 62 provokable, 65 discordable.
- Treasure maps: levels 1-6 have min skill 70 at most (`TreasureMap.cs:371-383`). Level 7 maps exist on this
  shard (pinned `ParagonChest.cs:187` makes level+1, so a level-6 paragon gives a 7; ours `C\Mobiles\Normal\
  Allosaurus.cs:51` has `TreasureMapLevel => 7`) and fall through to `_ => 0.0`, i.e. decode window 0-60.

---------------------------------------------------------------------------------------------------------------

## (i) Summary table

Musicianship reduction r = max(0, (Mus - 100) / 2), subtracted from bard difficulty
(`Peacemaking.cs:166-169`, `Provocation.cs:135-138`, `Discordance.cs:157-160`). Bard ceilings below assume
r = 0 (Musicianship <= 100); with Musicianship at its own use-ceiling 120, r = 10 and every bard target ceiling
drops by 10. **The higher a bard's Musicianship, the lower the bard skills' gain ceilings.**

| Skill | Gain calls (file:line, pinned/ours, min/max or chance) | Ceiling now | P20 ceiling (confirmed/corrected) | Reaches 200? |
|---|---|---|---|---|
| Animal Taming | `Skills\AnimalTaming.cs:406` pinned, CheckTargetSkill(MTS + 6*Owners - 0.1, MTS + 6*Owners + 49.9) (minSkill built :396-403); gate Value >= MTS at :184 | **157.0** fresh Raptor; **181.0** Raptor with 4 prior owners | 157.0 / 181.0 confirmed; source corrected (pinned Raptor.cs:38, not shard) | No, STALLED |
| Animal Lore | `Skills\AnimalLore.cs:59` pinned target 0-120; `AnimalTaming.cs:372, :393` pinned passive target 0-120; `Items\Skill Items\Misc\Bandage.cs:444` pinned location 0-120 (Vet secondary, `GetSecondarySkill` :185-189) | **120** | 120 confirmed | No, STALLED |
| Herding | `Items\Weapons\Staves\ShepherdsCrook.cs:146` pinned target (MTS - 30, MTS + 30 + Random(10)) (:133-134); herdable = Tamable, not paragon (:85-117) | **146.1** (Raptor, on a Random(10) = 9 roll; 137.1 guaranteed) | 146.1 confirmed; source corrected (pinned Raptor) | No, STALLED |
| Musicianship | `Items\Skill Items\Musical Instruments\BaseInstrument.cs:528` pinned location 0-120 (result discarded, success = Mus/100 at :530); `Items\Skill Items\Misc\FireHorn.cs:77` pinned direct chance 0.5 + (Mus - 77.5) * 0.02 (:72-75) -> 1.0 at 102.5; craft secondary 45-50 (`Engines\Craft\DefCarpentry.cs:405-426`, `C\Engines\Craft\CarpentryCraftRegistrations.cs:61`, `C\Engines\Craft\KingsCollectionCarpentryRecipes.cs:63-79`) via `CraftItem.cs:893` | **120** | 120 confirmed | No, STALLED |
| Peacemaking | `Skills\Peacemaking.cs:83` pinned area location 0-120; `:171` pinned target (diff - 25, diff + 25), diff = D - 10 - r (:163-169) | **175** target vs D160 (r = 0); 185 with an opposing-slayer instrument (D170); 165 / 175 at Mus 120; area 120 | P20 "120 area / 175-195": 175 confirmed, 195 corrected to 185 (no D180 target found) | No, STALLED |
| Provocation | `Skills\Provocation.cs:154` pinned target (diff - 25, diff + 25), diff = avg(D1, D2) - 5 - r (:131-138); refused if paragon with base D >= 160 (:66) | **180** (pair at D160, r = 0); 190 with opposing slayer vs both; 170 / 180 at Mus 120 | P20 "180-200": 180 confirmed, 200 corrected to 190 | No, STALLED |
| Discordance | `Skills\Discordance.cs:168` pinned target (diff - 25, diff + 25), diff = D - 10 - r (:154-160) | **175** (D160, r = 0); 185 opposing slayer; 165 / 175 at Mus 120 | P20 "175-195": 175 confirmed, 195 corrected to 185 | No, STALLED |
| Tracking | `Skills\Tracking\Tracking.cs:129` pinned location 0-21.1 (success); `:163` pinned location 21.1-100 (passive, after success) | **100** | 100 confirmed | No, STALLED |
| Item Identification | `Skills\ItemIdentification.cs:44` pinned target 0-100, IIdentifiable items only | **100** | 100 confirmed | No, STALLED (F-14 Appraisal owns its future) |
| Taste Identification | `Skills\TasteID.cs:37` pinned target 0-100, Food only | **100** | 100 confirmed | No, STALLED |
| Camping | `Items\Skill Items\Camping\Kindling.cs:38` pinned location 0-100 | **100** | 100 confirmed | No, STALLED |
| Cartography | `Items\Maps\TreasureMap.cs:413` pinned location (min, min + 60), min from `:371-383` (L5/L6 70; L7+ 0); craft `Engines\Craft\DefCartography.cs:91-94` max 99.5 via `CraftItem.cs:893` | **130** (L5/L6 map) | 130 confirmed | No, STALLED |

**12 of 12 stalled.** Highest any of them can roll today is Provocation 190 (opposing-slayer instrument, Musicianship
<= 100); nothing in this group can roll a gain at 199.9.

---------------------------------------------------------------------------------------------------------------

## (ii) Proposals, one per stalled skill

### A shared ours-only hook (used by several proposals below)

`C\ClusterFSkillGain.cs` already sits between every gain call and pinned (`:36-47`) and sees skill, target,
min and max. A small **"extension" table** there can add a gain-only roll when, and only when, the stock call
returned "no challenge" (Value >= max): the stock result is returned unchanged, then, if the call matches a table
row, it calls the public `SkillCheck.CheckSkill(from, skill, amObj, chance)` (pinned `SkillCheck.cs:108`) with a
chance from the row's extended window. Below the stock max nothing changes at all (bit-identical to pinned), so
OSI fidelity below 100/120 is untouched by construction. Builder facts:
- Rows are keyed by (skill, handler kind, stock min, stock max, target type). Exact pairs in this group:
  Musicianship location (0, 120) occurs only at `BaseInstrument.cs:528`; Tracking location (21.1, 100) only at
  `Tracking.cs:163`; TasteID target (0, 100) with `Food` only at `TasteID.cs:37`; Camping location (0, 100) only at
  `Kindling.cs:38`; Animal Lore **target** (0, 120) with `BaseCreature` at `AnimalLore.cs:59`, `AnimalTaming.cs:372,
  :393` (the Vet bandage call `Bandage.cs:444` is a location call, so a target-only row excludes it).
  These literal keys break silently on an upstream bump: add a verification test that asserts each pinned line
  still holds the literal (the project's `T\...Verification.cs` pattern).
- For location rows, amObj is a `Point2D(X / size, Y / size)` with `size = AntiMacroSystem.Settings.LocationSize`
  (pinned `SkillCheck.cs:72`), so anti-macro still applies.
- Route the extra roll through `RunBoostedCheck` (`:97`) so the shard's 3 attempts / 5x apply uniformly.
- Calling `SkillCheck.CheckSkill` directly (not the base handler) avoids firing `SkillEvents.InvokeSkillUsed` twice.
- Fallback if the hook is rejected: a one-line pinned patch per site (`max = value < stockMax ? stockMax : Cap`),
  i.e. 5 new `.patch` files under the fuzz-0 gate in `docker\uo\apply-patches.sh`.

### Animal Taming: option (b), harder tame targets (our custom creatures)

- (a) skipped: Taming's difficulty is MinTameSkill, max 107.1 in all existing content; letting the window follow
  the cap would make easy creatures train to 200.
- (b): add custom tamables above 107.1. The existing roll then reaches 200 with no formula change: ceiling =
  MTS + 49.9 fresh, so **MinTameSkill >= 150.1 gives a fresh ceiling of 200.0** (at Value 199.9 the chance is
  0.998, still a roll); with 4 prior owners MTS 126.1 suffices. The gate `AnimalTaming.cs:184` (Value >= MTS) means
  a ladder is needed, e.g. rungs at about 115, 130, 150.1, and a top rung at **170.1** (serves Herding, below).
  Each rung must be tamable by a real player: `ControlSlots` <= `FollowersMax` (`:164`), not `CanAngerOnTame` unless
  intended (95% anger at `:208`). These are the F-14 "above 160" custom creatures; their stats and bard D are F-14's.
- Files: new creature classes in `C\Mobiles\...` (ours), plus spawns. No pinned change.
- Coupling: control chance (`BaseCreature.cs:1777-1841`, ML branch) uses Taming and **Lore** against MTS. Lore is
  stuck at 120: vs MTS 150.1, Taming 200 + Lore 120 gives (2994 - 4214)/2 = -610, clamp 22% (`:1839`). Taming
  for gain then releasing works; keeping the pet needs the Lore proposal below.
- Worn bonuses: with a Warden's crook (+15) and Mark of Travesty (+10), Value is Base + 25, so the gain stops at
  Base 175 vs MTS 150.1; unequip, or give the top rung MTS >= 175.1.
- Fidelity: nothing below 100/120 changes (new creatures only).
- Exploits: none of the cc-P20 rank-4 list is touched. New between 160 and 200: **stable slots**
  (`AnimalTrainer.cs:58-97`): at Taming/Lore/Vet ceilings today (157/120/120) a tamer gets 5 + 6 + 3 + 3 = 17; at
  200/200/200 it is 5 + 11 + 11 + 11 = **38**. Recommend a clamp in the same batch (pinned patch, `GetMaxStabled`).

### Animal Lore: guarded (a) on the existing target use, keyed on MinTameSkill (shared hook)

- Plain (a) (window 0..Cap, the Meditation pattern) rejected: at Lore 60 the success chance of the lore gump
  (`AnimalLore.cs:59`) would fall from 50% to 30%, an OSI-visible change.
- Guarded: extension row on the Lore target calls; only when Value >= 120, extended window = the creature's own
  tame window (MTS - 0.1, MTS + 49.9). Against pinned creatures that tops out at 157.0 (Raptor); against the
  MTS 150.1 rung it reaches 200.0. Lore and Taming then train on the same targets, and the Lore that control of
  those pets needs is reachable.
- Files: `C\ClusterFSkillGain.cs` (ours). No pinned patch.
- Fidelity: none below 120 (extension only fires at Value >= 120).
- Exploits: no rank-4 item touched. New 160-200: stable slots (above); pet bandage heal Lore term
  (`Bandage.cs:387-388`, min L/8, max L/6 as secondary) goes from 15-20 at 120 to 25-33 at 200, about +13 HP per
  bandage: mild; control chance rises to 99% vs high rungs (intended).

### Herding: option (b), the same top tame rung

- (a) skipped for the same reason as Taming.
- (b): Herding max = MTS + 30 + Random(10). To roll at 199.9 on every attempt, MTS >= 170.1 (window 140.1 to
  200.1-209.1). MTS 150.1 gives 180.1-189.1, not enough. So the ladder's top rung at **MTS 170.1** carries Herding
  to 200 (herding needs only `Tamable`, not the herder's Taming).
- Files: the creature from the Taming batch. No code.
- Fidelity: none. Exploits: Herding has no combat effect; none.

### Musicianship: guarded (a), the Meditation pattern on the self-check (shared hook), plus a mandatory clamp

- `BaseInstrument.cs:528` is a self-check with no target and its result is discarded (success is Mus/100 at
  `:530`), the same shape as Meditation. Extension row: Value >= 120 -> window (0, Cap).
- Fidelity: none below 120.
- **Exploit check: worse unless clamped.** Every point of Musicianship above 100 subtracts 0.5 from bard
  difficulty, uncapped (root cause in cc-P20 rank 4). Today Musicianship stops at 120 by use (r = 10), so certain
  Peacemaking/Discordance vs D160 needs skill >= D - 10 - r + 25 = **165**, Provocation **170**. With Musicianship 200
  (r = 50) certainty comes at skill **125 / 130**, i.e. reachable much sooner. It also lowers every bard skill's own
  gain ceiling by 40. So this proposal ships only with a clamp: count Musicianship at most 120 in the reduction
  (r <= 10) at `Peacemaking.cs:166-169`, `Provocation.cs:135-138`, `Discordance.cs:157-160` (3 pinned patches).
  The clamp changes nothing below Value 120; it does change item-boosted bards above 120 Value (OSI allowed 120 +
  items): flag for the deviation register.
- Fire Horn (new break 160-200): damage weights Musicianship 1 of 8 with the GM tripling past 90
  (`FireHorn.cs:115-145`). Musicianship 200 alone raises PvM horn damage about 17%; with all four bard skills at
  200, PvM 189-233 and PvP 126-155 per blast (vs 81-100 / 54-66 at 120). Clamp the horn's skill inputs at 120 in
  the same batch (pinned patch).

### Peacemaking, Provocation, Discordance: option (b), opt-in bard difficulty above 160 for our creatures

- (a) skipped: the target difficulty D is capped at 160 for every creature, so past 160 it means nothing; a
  cap-following window would train to 200 on rabbits.
- (b): the 160 cap is inside pinned `GetBaseDifficulty` (`BaseInstrument.cs:299-301`, static). One pinned patch:
  before the cap, ask an ours hook (e.g. `C\ClusterFBardDifficulty`, an interface or type table) whether this
  creature carries an explicit difficulty above 160, and return it. **Opt-in only**: 34 of our creatures already
  compute far above 160 uncapped (Despise bosses up to 3317 raw in the s5 CSV), so simply uncapping ours would make
  them unbardable. Targets needed for 200 (with the Musicianship clamp, r <= 10): Peacemaking and Discordance
  ceiling = D + 5 -> **D >= 195** (185 with an opposing-slayer instrument); Provocation ceiling = avg D + 10 ->
  **a pair at D >= 190**. Peacemaking needs `Uncalmable` false (`Peacemaking.cs:146`), Discordance `BardImmune`
  false (`Discordance.cs:143`), Provocation `Unprovokable` false (`:113, :117`) and **not paragon** (`:66` and
  `BaseCreature.cs:4029` refuse paragons with base D >= 160). A D 200 creature still resists a 200 bard 10% of the
  time (peace chance at 200: (200 - 155) / 50 = 0.9), which is the right shape.
- Without the Musicianship clamp the bard skills cannot reach 200 even here: at Musicianship 200 a D 200 target
  gives a Peacemaking ceiling of 165.
- Readers that follow automatically: `Discordance.cs:190` halves the effect at base D >= 160; `AnimalLore.cs:142`
  shows D in the lore gump; F-14 reads the same function for creature levels.
- Files: `P\BaseInstrument-...patch` (pinned, new), `C\ClusterFBardDifficulty.cs` (ours, new), the Musicianship clamp
  patches above (3), the opt-in creatures (ours, can be the same F-14 creatures), Discordance effect clamp
  (in the same Discordance patch), Fire Horn clamp (pinned patch).
- Fidelity: no existing creature changes. The Musicianship clamp is the only OSI-visible change, above 120 Value.
- Exploits: makes nothing below 160 sooner (with the clamp, certainty vs D160 stays at 165 / 170, as today).
  New 160-200 breaks, all in cc-P20's list: Discordance effect `-20 + (int)((S - 100) / -2.5)` (`Discordance.cs:183`)
  is -44 at 160, **-60 at 200** (OSI max -28): resists -60, target skills x0.4, swing 2.5x slower; halved vs D >= 160
  (`:190`). Not the divide-by-zero (that is at -100, S 300). Recommend the clamp at about -28 to -32 in the same
  batch. Peacemaking range `8 + S/15` (`BaseInstrument.cs:212`): 18 at 160, 21 at 200 (vs 16): mild; area peace
  is already certain from 120 (`Peacemaking.cs:83`). Fire Horn as above.

### Tracking: guarded (a), the Meditation pattern on the passive (shared hook)

- The passive `Tracking.cs:163` (21.1, 100) is a self-check with no target or difficulty, like Meditation.
  Extension row: Value >= 100 -> window (21.1, Cap). (b) has nothing to work with: tracking players
  (`:304-354`) is not a gain call.
- Fidelity: none below 100.
- Exploits: none of the rank-4 list. New 160-200 (cc-P20's "Tracking range"): search radius
  `10 + (int)V / 10 * 10` (`Tracking.cs:166`) = 170 at 160, **210 at 200** (arrow range x2 = 420); stalking bonus
  `10 + T/10` = 30 at 200 feeds Backstab (+30%) and Surprise Attack's malus (with Ninjitsu 200: 33 + 30 = 63, still
  below the 100 divide-by-zero point). Recommend clamping the radius (pinned patch at `:166`) in the same batch,
  or accept 210 as a server-cost decision.

### Item Identification: defer to F-14 (Appraisal); option (c) by F-14's new creature use

- Its only use is `ItemIdentification.cs:44` (0-100, unidentified `IIdentifiable` items). F-14 renames it Appraisal and
  gives it a creature use whose difficulty can be the creature's level, which past 160 is exactly the custom
  creatures above. That use, not this one, is the natural route to 200. Not designed here. A guarded extension of
  the 0-100 item call would train it to 200 on any unidentified item: skip.

### Taste Identification: guarded (a) (shared hook)

- `TasteID.cs:37` target (0, 100) on Food: no difficulty in pinned. Extension row: Value >= 100 -> (0, Cap).
- Fidelity: none below 100. Exploits: TasteID has no effect past 100 (cc-P20); none.

### Camping: guarded (a) (shared hook)

- `Kindling.cs:38` location (0, 100), consumes a kindling per attempt. Extension row: Value >= 100 -> (0, Cap).
- Fidelity: none below 100. Exploits: Camping has no effect past 100; none.

### Cartography: option (b), harder treasure maps

- (a) skipped: decode difficulty is the map level, meaningful only to 70.
- (b): decode window is (min, min + 60), so a level with **min >= 140** reaches 200. `GetMinSkillLevel`
  (`TreasureMap.cs:371-383`) is private and non-virtual: a pinned patch adding e.g. level 7 = 100 (window 100-160) and
  level 8 = 140 (140-200). Level 7 already drops here (pinned `ParagonChest.cs:187`, ours `Allosaurus.cs:51`) and
  decodes at 0-60 today: giving it min 100 makes those maps unusable below 100, an OSI-visible change (to a pinned
  quirk). Level 8 needs a source (ours: loot on the F-14 high creatures, or a quest reward).
  Unverified for levels 7-8: chest fill (`TreasureMapChest.cs:175-305`: gold level*1000, TrapPower level*25 so 200 at
  L8, `RequiredSkill` switch at :197 has no 7/8 case shown), map label clilocs (`TreasureMap.cs:117-130`,
  1041510 + level), guardian spawn tables (`TreasureMap.Spawn`). A builder must read those.
- Alternative (c), ours only: a custom map item with its own decode `CheckSkill(Cartography, 140, 200)` and its own
  chest. No pinned patch, more code. Pick (b) if the level 7/8 paths in pinned turn out clean, else (c).
- Exploits: none of the rank-4 list. New 160-200: map extents (cosmetic: world map covers the facet at about 182,
  cc-P20); chest trap power 200 at level 8 (unverified damage path).

---------------------------------------------------------------------------------------------------------------

## (iii) Lines moved since P20 (7c9215d97 -> d4531cd94)

| P20 citation | Now | Status |
|---|---|---|
| SkillCheck.cs:53-61 / :161-169 (no challenge) | :62, :67 / :184, :189 | moved |
| SkillCheck.cs:84-87 / :190-193 (direct >= 1.0) | :95, :100 / :215, :220 | moved |
| AnimalTaming.cs:185 gate | :184 | moved |
| AnimalTaming.cs:397-407 roll | :396-406 (check :406) | moved |
| AnimalTaming.cs:373, :394 passive Lore | :372, :393 | moved |
| AnimalTaming.cs:209 anger | :208 | moved |
| BaseCreature.cs:159 MaxOwners | :169 | moved |
| BaseCreature.cs:1408-1474 control chance | :1777-1841 (clamp :1839) | moved |
| BaseCreature.cs:4304-4306 bonding | :4598-4600 | moved |
| shard Mobiles\Normal\Raptor.cs:50 (107.1) | pinned Mobiles\Monsters\Reptile\Raptor.cs:38 | file changed (shard copy gone) |
| BaseInstrument.cs:527-532 CheckMusicianship | :526-531 (CheckSkill :528) | moved by 1 |
| BaseInstrument.cs:213 GetBardRange | :212 | moved |
| BaseInstrument.cs:250-306 GetBaseDifficulty, cap :298-301 | :249-305, cap :299-301 | moved by 1 (F-14 cites :250; now :249) |
| BaseInstrument.cs GetDifficultyFor :308 | :307 | moved |
| Bandage.cs:375-393 heal formula | :387-388 | moved |
| Discordance.cs:177-201 effect | :183-190 | moved (approx; :183, :187, :190 verified) |
| DefCartography.cs:85-88 | :91-94 | moved |
| shard CraftItem.cs:877-895 (full replacement) | pinned CraftItem.cs:893, patched by P\CraftItem-shard-hooks.patch (no full replacement now) | corrected |
| C\ClusterFWorkOrderSystem.cs:151, :183 | :151, :183 | unchanged |
| C\OutridersCrook.cs:82-85 | :82, :83, :85 | unchanged |
| AnimalLore.cs:49, :54, :59; AnimalTrainer.cs:58; Bandage.cs:444, :240; ShepherdsCrook.cs:133-146; Peacemaking.cs:83, :163-171, :99; Provocation.cs:66, :131-154, :93, :122; Discordance.cs:154-168; FireHorn.cs:72-77; DefCarpentry.cs:405-426; Tracking.cs:129, :163, :166; ItemIdentification.cs:44; TasteID.cs:37; Kindling.cs:38; TreasureMap.cs:371-417 | same | unchanged |
| Brief: C\Meditation.cs "around :92" | :115 | moved |

Not re-verified (not gain calls): Peacemaking duration :190-201, Bandage :500-502, FireHorn damage :115-160,
Tracking player chance :304-354, map extent files.

---------------------------------------------------------------------------------------------------------------

## (iv) Batch sizing

| Batch | Skills | Size | Files | Notes |
|---|---|---|---|---|
| B1 gain-extension hook | Tracking, Taste ID, Camping (and the hook Lore and Musicianship use later) | S | `C\ClusterFSkillGain.cs` (ours); one verification test pinning the 5 literal call sites; optional pinned patch for the Tracking radius (`Tracking.cs:166`) | No overlap with cc-P53 (it only read `ClusterFSkillGain.cs:141-147`). |
| B2 tame ladder | Animal Taming, Animal Lore, Herding | M | 3-4 new creature classes in `C\Mobiles\...` (MTS about 115 / 130 / 150.1 / 170.1), spawns; Lore row in the B1 hook; stable-slot clamp patch on `AnimalTrainer.cs:58-97` (pinned) | Creature stats and levels are F-14's; needs B1. |
| B3 bard | Musicianship, Peacemaking, Provocation, Discordance | M-L | new `P\BaseInstrument-*.patch` (`:299-301`) + `C\ClusterFBardDifficulty.cs`; Musicianship clamp patches on `Peacemaking.cs`, `Provocation.cs`, `Discordance.cs` (the last also clamps the effect at `:183-187`); `FireHorn.cs` input clamp patch; Musicianship row in the B1 hook; opt-in creatures with D 190-200 (a provokable non-paragon pair) | Shares `BaseInstrument.GetBaseDifficulty` with F-14 (creature levels read it): do F-14's design first or together. 5 new pinned patches under the fuzz-0 gate. |
| B4 maps | Cartography | M | `P\TreasureMap-*.patch` (`:371-383`) plus whatever levels 7-8 need in `TreasureMapChest.cs` / labels / spawns (unverified), or an ours map item (c) | Level 8 drop source from F-14 creatures. |
| (F-14) | Item Identification | - | F-14 Appraisal | Not designed here. |

None of these files is touched by cc-P53's change list (`C\ClusterFSkillCaps.cs`, metal tiers, smith files,
Meditation, RegenRates, TestCenter, PlayerMobile bonus patch) or F-26 (Arms Lore). F-14 overlaps B3 (bard
difficulty) and owns Item Identification. cc-P53's above-cap item bonuses matter to every row: worn skill bonuses
raise Value and stop gains that much earlier in Base.
