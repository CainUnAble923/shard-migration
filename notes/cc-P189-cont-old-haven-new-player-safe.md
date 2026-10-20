# cc-P189: Old Haven safe for new players, and OSI's apprentice training there

Gold Golem, 2026-10-20. Branch golem/Gold/P189 in both repos. Image `sl-modernuo:cc-P189`.

## Headlines

- **The custom mages and Vorlak are out of Old Haven.** `ClusterFSeedOldHaven` now places only ServUO's Drelgor. A new
  staff command, `[ClusterFOldHavenRetire [dryrun]`, removes the 5 OldHavenMage spawners and Vorlak's spawner (and
  what they spawned) from a world that already has them. The classes stay, so nothing that names them breaks.
- **Measured, the custom mobs were not on the walk itself.** On a straight walk from New Haven's east edge to the
  Rootdeep hole, the nearest mage home area is about 42 tiles off and Vorlak's about 86. What a new player meets on the
  walk is pinned's own undead around the hole (37 skeletons and zombies), which Chase keeps. The danger was to anyone
  who goes into the ruins to train, which the New Haven trainers tell them to do: 12 aggressive mages whose Energy Bolt
  does about 41-53 before resists, against a fresh character's roughly 60-80 hit points, and Vorlak, who ignores Young
  protection.
- **The "young player skill boost" is not tied to Young.** On ServUO (and OSI as ServUO models it), the boost is for
  whoever holds a New Haven trainer's quest for that skill: x2 to x4 gain on that skill while standing in the quest's
  training region, from 0 until the quest completes at 50. Young status is never checked. It is ported as such:
  "Old Haven Training" is registered, and the x2-4 applies to the 20 trainers' quests that train there.
- **Drelgor speaks now**: his "Who dares to defile Haven?" broadcast checks for the "Old Haven Training" region, which
  now exists (cc-P129's recorded deviation reverses).
- **A latent achievement starts working**: "Old Haven's Least Welcome Regular" (slay 50 creatures in Old Haven's
  ruins) looks for a region named "Old Haven ..." and there was none on Endless Journey. Now there is.
- Chase decides: the new home for the mages and Vorlak, whether to register ServUO's other five Haven apprentice
  regions, and the deviations below.

## 1. Measurement: what a new character meets, New Haven -> Old Haven hole -> back

The walk is taken as a straight line from New Haven's east edge (3545,2580; pinned's "New Haven" region ends at x
3545, regions.json:1516-1526) to the hole in the ruined Second Bank (3619,2620, `OldHavenBurrowsRegion.ProvisionalEntrance`,
still provisional until P188). The real path follows the ground; the play test below checks it. Distances are UO range
(the larger of dx and dy). "Edge to path" is the centre distance less the spawner's home range, the closest its
creatures' home area comes; a creature notices a player within its perception range (10 for the mages and Vorlak,
their constructors).

Spawners from pinned's `post-uoml/trammel/Outdoors.json` and `shared/trammel/Graveyards.json` (every Trammel spawner
in x 3400-3800, y 2400-2800 was read; the animals, pumpkins and reagent spawners are left out) and our
`ClusterFOldHavenSeeder` (before this change).

| Creature (source) | How many | Spawner, home range | Centre to path | Edge to path | Hits | Fights with | Attacks a Young player? |
|---|---|---|---|---|---|---|---|
| Skeleton (pinned) | 7 | 3635,2625, walk 15 | 16 | 1 | 34-48 | melee 3-7, Wrestling 45-55 | no, unless the player attacks it first |
| Zombie (pinned) | 10 | 3625,2594, walk 15 | 19 | 4 | 28-42 | melee 3-7, Wrestling 35-50 | no, unless attacked |
| Zombie (pinned) | 10 | 3649,2591, walk 15 | 30 | 15 | 28-42 | melee 3-7 | no, unless attacked |
| Skeleton (pinned) | 10 | 3651,2627, walk 15 | 32 | 17 | 34-48 | melee 3-7 | no, unless attacked |
| Zombie, Skeleton, spectral spellbinder (pinned) | 90 (70/70/20 caps) | 3650,2509, 60 | 83 | 23 | 28-50 | melee 3-7; the spellbinder fights only when attacked (FightMode.Aggressor) and has no Magery | no, unless attacked |
| Drelgor the Impaler (ServUO, ours since P129) | 1, 30 min | 3651,2509, 50 | 83 | 33 | 131-136 | melee 6-8, Wrestling/Tactics 60 | no, unless attacked |
| Zombie, Skeleton, spellbinder (pinned) | 4 | 3598,2450, 10 | 130 | 120 | 28-50 | as above | no, unless attacked |
| **Old Haven Mage (ours)** | 12 in 5 spawners, 2-5 min | 3618,2540 (10), 3600,2510 (12), 3645,2495 (10), 3556,2487 (10), 3588,2457 (10) | 52-123 | 42-113 | 90-130 | spells: Magery and EvalInt 65-80, Int 130-160, attacks the closest | no, unless attacked |
| **Vorlak the Impaler (ours)** | 1, 8-15 min | 3622,2488, 6 | 92 | 86 | 450-550 | melee 16-24, Swords 90-100, Tactics 85-95, plate | **yes**: `IgnoreYoungProtection => true` |

How hard each hits, against a fresh character (pinned AOS hit points: 50 + Str / 2, Mobile.cs:2069 and
PlayerMobile.cs:541-560, so about 60-80):

- An Old Haven Mage's spells (pinned `Spell.GetNewAosDamage`, Spell.cs:218-257: dice and bonus x (100 + Int / 10)% x
  (30 + 9 x EvalInt / 100)%): Energy Bolt (EnergyBolt.cs:38, 41-45) does about 41-53, Lightning (Lightning.cs:36,
  24-27) about 24-32, Fireball (Fireball.cs:37, 20-24) about 20-28, all before the player's resists. Two Energy Bolts
  kill a fresh character. Its melee is 4-10.
- Vorlak: 16-24 a swing at Swords 90-100; four or five swings kill a fresh character, and he does not need to be
  attacked first.
- The skeletons and zombies: 3-7 a swing. Drelgor: 6-8.
- Movement speed is pinned's default for each creature's AI; not measured here.

**Young protection decides most of this.** Pinned stops an uncontrolled creature from harming a Young player in a
Young-protected region unless the player is its aggressor or it sets `IgnoreYoungProtection` (Notoriety.cs:205-218,
PlayerMobile.CheckYoungProtection, PlayerMobile.cs:4021-4052). Haven Island is a NoHousingRegion, so Young-protected
(BaseRegion.cs:43). So a Young character walking to the hole is attacked by nothing in this table except Vorlak; the
mages only fight a Young player who hits them (or casts at them) first, and fight anyone not Young (Young ends after 2
weeks of play here, or by renouncing, ClusterFYoungPlayer.cs). Every New Haven trainer quest tells the new player to
"head East out of town to Old Haven and battle the undead there" (pinned NewHavenSkillTraining.cs, e.g. :13-24), so new
players do go into the ruins, and an area spell or a stray attack makes them the mages' aggressor.

**Drelgor is not a danger on the walk**: his home area's edge is about 33 tiles from the path, he does not attack Young
players, and at 6-8 a swing he is the "Cleansing Old Haven" target ServUO meant for apprentice paladins. No change
proposed; he is left exactly as ServUO places him.

## 2. Removed from Old Haven

- `server/customizations/ClusterFOldHavenSeeder.cs`: the Entries table (from :35) holds only Drelgor now; the five
  OldHavenMage entries and Vorlak's are gone, so a fresh world and `[ClusterFSeedOldHaven` (missing, dryrun, replace)
  never place them. `replace` deletes only spawners of the remaining entries, so it no longer touches the old ones
  either. The header is rewritten (ASCII; it also misstated the bounds box, now X 3520-3680 as the code has it).
- New command `[ClusterFOldHavenRetire [dryrun]` (same file, `Retire`): in the seeder's Old Haven box, every spawner
  whose entries are all OldHavenMage, VorlakTheImpaler or DrelgorTheImpaler (Vorlak's name before P129, still
  resolved through his TypeAlias) is deleted, and deleting a spawner deletes what it spawned (pinned
  BaseSpawner.OnDelete -> RemoveSpawns, BaseSpawner.cs:1245-1290). A mage or Vorlak in the box that no spawner owns
  and no player controls is deleted too. A spawner that also spawns something else is reported `[MIXED, KEPT]` and
  left for staff. Declared WorldSetup, Rerun = DeletesAgain, Shard = TestFirst, DryRun = "dryrun", so the console
  shows it red with its dry run; `scripts/tests/Shard-Console.Tests.ps1` (RedMeans... fact) lists it.
- The classes are kept: `OldHavenMage.cs`, `VorlakTheImpaler.cs`.

What references them (grep of both repos, `OldHavenMage|Vorlak|DrelgorTheImpaler|ClusterFSeedOldHaven`; machine
output under testing/ and old notes left out):

| Reference | Effect of the removal |
|---|---|
| `ClusterFAchievements.cs:28, :105, :368` "Old Haven Mages" counted achievement (25 kills), `:1248-1249` | Not earnable until the mages have a new home. Kept. |
| `ClusterFAchievements.cs:29, :106, :374-382, :1251-1252` the hidden "slay Vorlak" achievement | Not earnable until Vorlak has a new home. Kept. Its text names no place. |
| `tests/Misc/AchievementEarnedLineVerification.cs:161-162` | Builds an OldHavenMage itself; unaffected. |
| `tests/Mobiles/Normal/CCP129CreatureVerification.cs:811-827` | Builds Vorlak and spawns him under the old name on Malas; unaffected. |
| `Mobiles/Named/Drelgor.cs` | Not a reference to these; his header comment is updated (section 4). |
| `scripts/tests/Shard-Console.Tests.ps1:730, :777` | Lists `ClusterFSeedOldHaven`; unchanged and still passing. |
| Bestiary | No shard bestiary file names either type (grep found none). |
| Quests | No quest names either (pinned's "Cleansing Old Haven" counts Chivalry skill, not kills). |

## 3. Kept

The stock undead (pinned's spawners, never this seeder's) and ServUO's Drelgor, unchanged. No deviation.

## 4. The apprentice training boost (OSI's, through ServUO)

### What ServUO does, with citations

- The region class, `Scripts/Services/MondainsLegacyQuests/ApprenticeRegion.cs:9-95`: a BaseRegion that, on enter and
  on exit, looks through the player's quests for an incomplete `ApprenticeObjective` whose region this is; for each,
  it sends the objective's enter (or leave) line and adds (or removes) the buff `BuffIcon.ArcaneEmpowerment`, cliloc
  1078511 / 1078512 ("Accelerated Skillgain Skill: ~1_val~").
- The gain, `Scripts/Misc/SkillCheck.cs:404-407`: `if (QuestHelper.EnhancedSkill(pm, skill)) toGain *=
  Utility.RandomMinMax(2, 4);`. `EnhancedSkill` (`Helpers/QuestHelper.cs:802-827`) is true when the player holds an
  incomplete ApprenticeObjective for that skill and stands in (or in a child of) the objective's region.
- Who: the objective holder. **Nothing checks Young.** Every ApprenticeObjective is `(skill, 50, region, enter,
  leave)` on a New Haven trainer (26 trainers, `Scripts/Mobiles/NPCs/*.cs`, listed in the table in
  `Regions/ApprenticeTraining.cs`), completes at 50 (`QuestObjectives.cs:785-805`), and accepting it inside its region
  runs the enter at once (`:807-818`); completing it removes the buff (`QuestHelper.cs:19-33`, from `:820-823`). So the
  boost runs from 0 to 50 on that one skill and stops at 50, whatever the cap. Our 200 cap changes nothing.
- No stacking: a Scroll of Alacrity refuses while any apprentice quest is held (`Items/Consumables/ScrollofAlacrity.cs:71-84`),
  and its branch (`SkillCheck.cs:410-418`) would replace the amount anyway.
- Regions, `Data/Regions.xml:1426-1500`: under "Haven Island", an ApprenticeRegion "Enhanced Tracking Skill" over the
  whole island (Walker's Tracking), and in it "Old Haven Training" (3589,2443, 115 x 100) and "Haven Mountains"
  (3426,2732, 110 x 50, Jacob's Mining); in New Haven, "Springs And Things Workshop" (Amelia, Tinkering), "Haven Dojo"
  (Chiyo, Hiding), "Gorge's Shop" (George Hephaestus, Blacksmithy), "Haven Library" (Jillian, Inscription).
  Twenty of the 26 quests train in Old Haven Training.

The cc-P191 notes (section 1 table, and section 5 item 2) say ServUO's ApprenticeRegion "is only the buff icon" and
"the gain is the same AcceleratedSkill path". The source says otherwise: ServUO's apprentice gain is `EnhancedSkill`,
a separate branch from `AcceleratedSkill` (only the Scroll of Alacrity sets that, ServUO PlayerMobile.cs:670 and
ScrollofAlacrity.cs:128). P191's R4 fact still holds (it tests pinned's acceleration); only its description is wrong.

### What pinned has

- `Regions/ApprenticeRegion.cs`: an empty stub ("TODO: Implement"); `regions.json` has no Old Haven Training.
- Pinned's New Haven quests are its own ML quest system: `Engines/ML Quests/Definitions/NewHavenSkillTraining.cs`,
  26 quests, each `GainSkillObjective(skill, 500, useReal: true, accelerate: true)`. Accepting one sets the player's
  `AcceleratedSkill` for 15 minutes (`GainSkillObjective.cs:122-133`, with its own "TODO"), which multiplies gains by
  2-5 everywhere (`SkillCheck.cs:273-276`). That is pinned's, not ServUO's or OSI's region rule, and it is left alone.

### What changed

- `server/customizations/Regions/ApprenticeTraining.cs` (new):
  - `ApprenticeTraining.Areas`: the 26 ServUO objectives on pinned's quests of the same skill (one trainer per skill on
    both sides), each with its region and the trainer's enter and leave clilocs, the ServUO file:line beside each.
  - `ApprenticeTraining.OnGain`: after a gain of g on a skill, if the player holds that table quest, not completed
    (judged before this gain, as ServUO judges it), and stands in its registered region, adds g x (n - 1) with
    n = RandomMinMax(2, 4): ServUO's `toGain *= n`. Skipped while pinned's acceleration runs on that skill.
  - `ApprenticeTrainingRegion : ApprenticeRegion` (pinned's stub), "Old Haven Training", child of pinned's "Haven
    Island" at the default priority, registered in `Initialize` every start (no saved data, so it exists on a fresh
    world and after any restart). Enter and leave lines and the buff as ServUO. No rule of its own: housing, Young
    protection and the rest are Haven Island's (every Region virtual hands on to Parent, Region.cs:745-880).
  - The area: ServUO's rectangle x 3589-3703, y 2443-2542, plus x 3546-3703, y 2543-2650 so the whole walk from New
    Haven to the hole, and pinned's southern undead spawners, are inside (deviation 5). Checked against pinned's
    regions.json: on Endless Journey only Haven Island is loaded over either rectangle (pinned's "Haven" town and its
    shops end at SE); New Haven ends at x 3545.
- `server/customizations/ClusterFSkillGain.cs`, `ObserveAttempt` and `ApplyAmountBonus`: one call each to `OnGain`.
  Every player gain passes through `ObserveAttempt` (the four pinned handlers and the shard's extra attempts and
  hook G); `ApplyAmountBonus` makes each repeated gain boosted too, as ServUO boosts each Gain call. Not gated on the
  ClusterF rate switch: it is a port, not part of our rate.
- `server/customizations/Mobiles/Named/Drelgor.cs` header: the deviation it recorded reverses.

### How it stacks

- **Young (P18)**: nothing. Neither ServUO nor this port reads Young; P18 changes only how long Young lasts.
- **Pinned's 15-minute acceleration**: never both at once (deviation 1). For the first 15 minutes after accepting,
  pinned's x2-5 applies everywhere; after that, x2-4 in the training region until 50.
- **The shard's rate (ClusterFSkillGain, 2 chance attempts, 1x amount, P191)**: multiplies on top, as ServUO's boost
  sits on top of ServUO's own base rate. With P191's 1x amount there are no repeated gains; if the amount is raised,
  each repeated gain is boosted too.
- **Rootdeep's regions** (the Burrows, the Vault) are at x 5136-5247, far from Old Haven; nothing overlaps.
- **Loops, guild perks, achievements**: none of them changes skill gain (grep of customizations for gain bonuses:
  only ClusterFSkillGain, ClusterFCraftGain's craft windows and the Test Center multiplier, which is test-shard only).
- **Test Center multiplier** (test shard only) scales the gain chance; the boost scales the amount. Both apply there.

### Drelgor's line

With the region, his broadcast (cliloc 1077840: "Who dares to defile Haven? I am Drelgor the Impaler! I shall claim
your souls as payment for this intrusion!", red, sound 0x14) reaches every player in Old Haven Training once a minute
while he is in it too (Drelgor.cs BroadcastMessage). That is ServUO's, and fits the place: he is the quest target the
paladin trainer sends new players to. Because the region now reaches the hole, everyone walking to Rootdeep hears it
once a minute. If that is too much for the tutorial walk, the faithful fix is to leave it; the shard fix would be a
smaller region. Left as ServUO has it.

## 5. A new home for the mages and Vorlak (proposal only; nothing placed)

Places named by pinned's regions.json where it names them; coordinates are pinned's own spawners there.

**Old Haven Mages** (Magic Resist training for mid players; 12 of them, aggressive, Energy Bolt about 41-53):

1. **Deceit, by its Mummy/Skeleton/Zombie rooms** (Trammel, pinned DungeonRegion "Deceit"; spawners at 5163,567 and
   5187,603; which level they are on was not checked). Recommended. Only players who choose a dungeon meet them; Deceit is mostly undead (its spawn file), so spectral mages
   fit; a dungeon is where mid players already go; Young players get pinned's dungeon warning there (BaseRegion.cs:76-81).
2. **Britain Graveyard** (Trammel, pinned NoHousingRegion "Britain Graveyard", stock spawner 1369,1475 of Spectres,
   Wraiths, Skeletons and Zombies). Undead already, mid-level ones, and Britain's healers are close. Against: Britain
   is where many new players start, so the same problem in a busier place (Young protection still applies).
3. **The graveyard east of Moonglow** (stock spawner 4545,1317: Spectres, Shades, Wraiths; pinned names no region
   there, so the place is unverified in game). Moonglow is the mage city, which suits "mages"; quiet; healer in town.

**Vorlak the Impaler** (mini-boss, 450-550 hits, 16-24 a swing, ignores Young protection, 8-15 minute respawn):

1. **Deceit, the bone knights' room** (pinned spawner 5342,582: 8 BoneKnights and SkeletalKnights). Recommended. An
   undead warlord among his knights; a dungeon, so his IgnoreYoungProtection changes nothing (no Young protection in
   dungeons, DungeonRegion.cs:21).
2. **Deceit's deep end** (the Lich and Lich Lord spawner at 5314,748,-20). Tougher company; for a stronger party.
3. **The graveyard north-east of Vesper** (stock spawner 2758,867 of Spectres and Wraiths; no region name in pinned,
   place unverified in game). Outdoors and reachable on foot; but outdoors he attacks Young players, so not
   recommended unless he is made to respect Young protection (that would be a change to our own creature, Chase's call).

Either way the seeder is not the tool: Old Haven's seeder only knows Old Haven. A new home is a small seeder entry of
its own (or a staff-placed spawner) once Chase picks.

## 6. Old Haven after this

Not empty: pinned's own spawners keep about 130 undead in and around the ruins (the 90-cap spawner at 3650,2509 over a
60-tile range, 37 skeletons and zombies by the hole, 4 at the north end), plus Drelgor. The New Haven trainers send
players there for exactly these. **No additions proposed.** If Chase wants more variety later, ServUO adds nothing
here beyond Drelgor (its Spawns/trammel.xml has one "Old Haven" entry, :1515), so anything new would be ours.

## 7. ServUO's other Haven apprentice regions (not added; Chase decides)

| Region (ServUO Data/Regions.xml) | Area | Quest | Proposal |
|---|---|---|---|
| Enhanced Tracking Skill (:1430) | all of Haven Island (3314,2345, 500 x 750) | Walker, Tracking | Add. ServUO nests Old Haven Training inside it; adding it means re-parenting Old Haven Training under it (two regions at the same priority and depth would tie, Region.cs:231-252). |
| Haven Mountains (:1445) | 3426,2732, 110 x 50 | Jacob, Mining | Add. South of New Haven. Note pinned's wildlife spawner at 3450,2734 holds up to 36 Ettins among its 156 animals, so the mountains are no safer than Old Haven was. |
| Springs And Things Workshop (:1488) | 3455,2523, 9 x 10 | Amelia, Tinkering | Check first: our New Haven was rebuilt (ClusterFNewHavenSeeder) and the trainers stand in guild halls (cc-P15), so ServUO's shop rectangles may not hold the workbenches any more. |
| Haven Dojo (:1491) | 3415,2513, 11 x 11 | Chiyo, Hiding | Same check. |
| Gorge's Shop (:1494) | 3465,2535, 7 x 8 | George Hephaestus, Blacksmithy | Same check; it needs a forge and anvil inside. |
| Haven Library (:1497) | 3464,2488, 16 x 11 | Jillian, Inscription | Same check. |

Adding any of them is a few lines in `ApprenticeTrainingRegion.Initialize` (its rectangle and parent); the table already maps
their quests.


## 8. What changed, file:line (D:\ShatteredLegacy)

| File | Change |
|---|---|
| `server/customizations/ClusterFOldHavenSeeder.cs:33` | Entries: Drelgor only (5 OldHavenMage and the Vorlak entry removed). Header rewritten, ASCII. |
| `server/customizations/ClusterFOldHavenSeeder.cs:61, :97-185` | `[ClusterFOldHavenRetire [dryrun]`: `RetiredTypes`, `Retire(dryRun)`. `Seed` is internal now (for the test). |
| `server/customizations/Regions/ApprenticeTraining.cs` (new) | `:64` the 26-quest table; `:161` `OnGain`; `:210` pinned's gain rules for the extra; `:294` the area; `:312` `Initialize` registers "Old Haven Training"; `:324`, `:340` enter and leave. |
| `server/customizations/ClusterFSkillGain.cs:276, :298` | The two `OnGain` calls. |
| `server/customizations/Mobiles/Named/Drelgor.cs:6-9` | Header: the P129 deviation reverses. Code unchanged. |
| `server/tests/Regions/OldHavenNewPlayerSafeVerification.cs` (new) | The facts below. |
| `server/tests/Mobiles/Normal/CCP129CreatureVerification.cs:802-803` | A comment that named the reversed deviation. |
| `scripts/tests/Shard-Console.Tests.ps1:891-894` | The red-commands list gains `[ClusterFOldHavenRetire`. |
| `CHANGELOG.md`, `VERSION` | 2026.10.20.5 (2026.10.20.4 was already committed). |

No saved type changed: no field, no version bump, no migration. The region is registered in code every start and has
no saved data.

## 9. Tests

Built and tested only through the repo's build script, `docker/uo/build.sh -t sl-modernuo:cc-P189` (docker-build lock
taken and released).

**Seen red first.** A build with the tests and a feature-off production tree (the committed seeder with a stub
`Retire` that does nothing and `RetiredTypes` added so the tests compile; the region's `Initialize` not registering;
`OnGain` adding nothing): 1,578 tests, 7 failed, all of them the new ones, each for its own reason:

| Fact | Red (feature off) | Green |
|---|---|---|
| S1 seeder places Drelgor and no mage or Vorlak | `DoesNotContain` failed: the mage and Vorlak spawners were placed | pass |
| S2 retire removes exactly the mages and Vorlak (one under the old name), their creatures and a stray; keeps Drelgor's, the stock skeleton spawner's spot, a mixed spawner and a mage spawner outside Old Haven; dry run changes nothing | 5 of 5 should-be-gone items still there | pass |
| A1 the region covers ServUO's rectangle and the walk, not New Haven | 3589,2443 was plain "Region" (none) | pass |
| A2 Drelgor's broadcast test holds at his home and at the hole | region name null | pass |
| A3 quest holder in the region: x2 (roll 0) and x4 (roll 0.99, below 10.0: 4 becomes 16); outside x1 | expected 2, got 1 | pass |
| A4 nobody else: no quest, Young without the quest, another skill's quest, at 50, an unregistered region's quest, pinned's acceleration running (x2 alone, not both); a non-Young holder does get it; the gain that reaches 50 is still boosted | expected 2, got 1 | pass |
| A5 buff shows inside with the quest only, goes on leaving | false | pass |
| A6 the table is pinned's 26 accelerated quests, one skill each, 20 in Old Haven Training | passed (a table check: the red tree had the table too) | pass |

**Green**: 1,578 tests, 1,574 passed, 4 skipped, 0 failed ("Built sl-modernuo:cc-P189 with patches applied and 1574
shard test(s) passing"). Includes P191's R4 (pinned's acceleration under the shard rate) and P129's Drelgor fact.

**Shard Console facts** (`scripts/tests/Shard-Console.Tests.ps1`): the red-commands fact failed first with the new
command present ("got [...,[ClusterFOldHavenRetire,...]"), and passes after the list update. The run shows 23 other
failures, all present before this change and unrelated (Golem buttons, Haven deploys, P107-P208 ops facts on this PC);
none touches world commands.

Not done: the removal on the test shard's world. The container console takes only save, shutdown and restart
(notes/port-recipe.md:571-573), so an in-game staff command needs a client; it is in For Chase, dry run first. S2 is
the proof on a test world built in the test host.

## Deviations and decisions for Chase

Deviations (for `docs/fidelity-principle.md`; agents do not edit docs):

1. **Pinned's 15-minute acceleration is kept alongside ServUO's region boost** (they never apply at once). ServUO has
   only the region boost; pinned adds a 15-minute x2-5 anywhere on accepting the quest. Removing pinned's would be a
   patch to pinned; not done.
2. **The extra gain is added after pinned's gain** with pinned's rules (down-locked skill may drop, total cap),
   instead of inside one Gain call. Same amounts; the down-lock roll is a second roll.
3. **Accepting the quest inside the region**: the line and buff come at the first boosted gain, not at accept (pinned
   has no accept hook). Completing removes the buff at that gain.
4. **The buff shows the skill's display name** ("Resisting Spells"), not ServUO's enum name.
5. **Old Haven Training is larger than ServUO's**: ServUO's x 3589-3703, y 2443-2542, plus x 3546-3703, y 2543-2650
   (the walk to the Rootdeep hole and the undead by it). The prompt asked for it; it also means Drelgor's line reaches
   the whole walk.
6. **Reversed**: P129's "Drelgor never speaks" deviation is gone.

Decisions:

- **The "young player skill boost" is not about Young** on ServUO: it comes from the New Haven trainers' quests. Ported
  that way. If you want every Young player boosted in Old Haven regardless of quests, that is a shard rule, not a
  port, and needs your say-so.
- **New home** for the mages and Vorlak: section 5 (recommended: Deceit for both). Until then their two achievements
  ("Old Haven Mages" x25, the hidden Vorlak one) cannot be earned.
- **ServUO's other Haven apprentice regions**: section 7 (recommended: Enhanced Tracking Skill and Haven Mountains now;
  the four New Haven shops after checking our New Haven layout).
- **Drelgor's line once a minute** along the tutorial walk: kept as ServUO has it. Say if it should be quieter.
- `ClusterFAchievements.NotifyOldHavenVisit` (`ClusterFAchievements.cs:1302`, the "visit Old Haven" event) is still
  wired to nothing; the new region's OnEnter would be the natural hook. Not done (not asked).
- P191's notes misdescribe ServUO's apprentice gain (section 4); their tests are fine.
- P188 (Rootdeep goes in) had not landed; the hole is still `OldHavenBurrowsRegion.ProvisionalEntrance` (3619,2620).
  If P188 moves the hole, check it stays inside Old Haven Training (x 3546-3703, y 2543-2650). No P188 file was edited.

## For Chase

**Live world, after this build is deployed** (in game, as Administrator; also on the console's World tab, red, with
its dry run):

```
[ClusterFOldHavenRetire dryrun
[ClusterFOldHavenRetire
```

The dry run lists each spawner it would delete, with its entries and spawned count, and any stray mage or Vorlak. On a
world seeded by the old seeder expect 6 spawners (5 mage, 1 Vorlak) and up to 13 creatures. A `[MIXED, KEPT]` line
means a spawner someone added other creatures to: it is left for you. Run the same two lines on the test shard first.
The region needs nothing: it registers itself at start.

**Play test (test shard, `sl-modernuo:cc-P189`, about 15 minutes):**

1. On the test shard run `[ClusterFOldHavenRetire dryrun`, then `[ClusterFOldHavenRetire`. Check the ruins: no Old
   Haven Mages, no Vorlak; skeletons, zombies, spellbinders and Drelgor still there.
2. Make a fresh character (Young). In New Haven take Dimethro's wrestling quest ("The Rudiments of Self Defense") or
   Alefian's Magic Resist one.
3. Walk east to the ruins and on to the Rootdeep hole in the Second Bank (3619,2620). On crossing x 3546 you should get
   the trainer's line and an "Accelerated Skillgain" buff icon, and hear Drelgor's challenge within a minute.
   Nothing should attack you on the way.
4. Fight a skeleton by the hole bare-handed: Wrestling should rise in jumps of 0.2 to 0.4 (after the first 15 minutes;
   in those minutes pinned's own x2-5 applies everywhere and the region adds nothing on top).
5. Walk back west into New Haven: the leaving line, and the icon goes.
6. A second fresh character with no quest: no line, no icon, normal gains.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

(code: 9 files pending, docs: 1. Nothing over 5 MB; the largest touched file is Shard-Console.Tests.ps1 at 606 KB.
No scratch in either repo: the red-build logs and the scan scripts are in the session scratchpad.)

P189 DONE
