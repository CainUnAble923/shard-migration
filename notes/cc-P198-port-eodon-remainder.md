# cc-P198: the Eodon remainder, and the Eodon moongate in Ter Mur

Written 2026-10-21 by the Gold Golem (Claude Opus 5.5), on branch golem/Gold/P198 of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Gold\cc-P198-port-eodon-remainder.md`. Pinned ModernUO (`D:\UO\ModernUO-pinned`) is the
authority for every engine citation; ServUO pub57 (`D:\UO\ServUO-pub57`) is the source. Nothing was committed, nothing
touched the live shard, and nothing was placed in any world except the throwaway test world, which was put back
exactly as it was (section 5). ASCII only.

## Headlines

1. **The Eodon gate was never "a command that did not run".** Chase's guess (10-19 15:14) was the natural one, but
   no command anywhere places it. Pinned lists Valley of Eodon as a moongate *destination* for TOL clients
   (`Projects/UOContent/Items/Misc/PublicMoongate.cs:268-276`, `TerMurEodon`, chosen at `:355-356`), so the gump
   sends players to 719,1863,40; but pinned's `[MoonGen` only generates Trammel, Felucca, Ilshenar, Malas and Tokuno
   (`:105-109`) and pinned has no `[DecorateTOL`. ServUO places the gate in `[DecorateTOL`
   (`Scripts/Services/Expansions/TimeOfLegends.cs:75-76`), which was never ported. Our `ClusterFRoyalCitySeeder` places
   the Royal City gate and no other. So every world, test and live, has the destination and no gate: the ring of dirt.
   The test world's own start-up line said so before the fix: `[Eodon] 0 objects placed by GenEodon; Eodon moongate at
   (719, 1863, 40): MISSING`.
2. **The fix is a new command, `[GenEodon` (with `dryrun`), the P196 `[GenBlackthorn` shape:** the Eodon gate (skipped,
   and said so, if another public moongate already stands within a tile), ServUO's two climbing vines, and the Eodon
   spawners. `[DeleteEodon` takes it all down; a re-run replaces, never doubles. Proved on this PC's test shard
   (section 5): dry run, generate, save, restart, reload clean with the 345 creatures, delete.
3. **Eodon had no spawns at all.** Pinned's `Data/Spawns` has zero spawners in Eodon's box (Ter Mur x 0-1087,
   y 1344-2495; 65 Ter Mur spawners, none there). ServUO's come from `Spawns/Eodon.xml`. 46 of its 65 rows are now a
   data table (`EodonSpawns`), 345 creatures: dinosaurs, the six tribes, jungle, swamp, lava and desert wildlife,
   wandering shamans, the silverback gorillas. Dropped: Myrmidex (by name), the Valley of One quest line (CC3's
   decline), Hawkwind (a quest NPC).
4. **The port row: 6 of 19 before, 16 of 19 after** (`tools/progress.py`, stem proxy; the port list 736 to 746 of
   983). Ported: Anchisaur, Gallusaurus, DesertScorpion, GreaterPhoenix, Infernus, DragonTurtleHatchling,
   BritannianInfantry, EodonTribesman (enum, base, warrior, shaman, chieftan), CardOfSemidar, ClimbingVine, and
   DragonTurtleScute, the last type of `Resources.cs` (the other three came with P129's tigers; the proxy cannot count
   it because the file's stem is `Resources`). Plus one forced leaf dependency outside the row: WanderingShaman.
   **Left (3):** `DragonTurtle.cs` (the champion; next prompt), `EodonRewardTitleScroll.cs` (declined: ServUO's
   quest-reward title framework), `Resources.cs` (done in substance, uncountable by stem).
5. **Client check: nothing blocked.** Every body, item, gump and map spot is in the 7.0.117.0 data (section 3).
6. **Tests:** 21 new facts in `server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs`, every one seen red
   on its own assertion (17 sabotages, one run, 20 red, nothing else red; then one more for the status fact). Full
   suite green through `docker/uo/build.sh`: **1,934 passed, 4 skipped (pre-existing), 0 failed**, image
   `sl-modernuo:cc-P198` (`1e52dfa72dee`).
7. **Q-064's Eodon recipe drop is still open and is not done here** (section 7): it is a recipe-and-garment port of its
   own, with a design question for the shard's recipe gating.

## 1. What changed, file by file

All in `D:\ShatteredLegacy`. New ported files mirror ServUO's path under `server/customizations/` (the P129 choice for
the tiger pelts; CC3's dinosaurs went to `Mobiles/Normal/`, so the row now lives in two places, both stated).

| File (lines) | ServUO source | What it is |
|---|---|---|
| `server/customizations/Services/Expansions/Time Of Legends/Mobiles/Anchisaur.cs` (64) | same path (103) | Values verbatim. Disarm/ParalyzingBlow as `GetWeaponAbility` (`:53-54`). Dropped: AttacksFocus, DragonBlood, the Rampage-mastery `OnThink` (no Skill Masteries here; D row 1) |
| `.../Mobiles/Gallusaurus.cs` (68) | same (86) | Tamable 102.0, 3 slots; Block (`:58`); GraspingClaw on the ability profile (`:52`, cc-P121) |
| `.../Mobiles/DesertScorpion.cs` (58) | same (72) | Lethal poison; ServUO's two `SetDamageType(Physical, ...)` calls kept, so it deals 40% physical and nothing else (`:34-35`, what ServUO runs) |
| `.../Mobiles/GreaterPhoenix.cs` (51) | same (64) | AI_Mage, 500-700 packed gold, no loot pack (ServUO has none); GraspingClaw |
| `.../Mobiles/Infernus.cs` (167) | same (169) | `OnActionCombat` drops a trail of fire round its target every 10-15 s (`:64-77`, `:79-97`); nested `FireItem` (`:99-166`), 50-85 fire damage on step or each one-second tick, 30-40 s life, deletes itself after a load (ServUO's wrote no data at all) |
| `.../Mobiles/DragonTurtleHatchling.cs` (85) | same (111) | FightMode.Aggressor kept; BleedAttack; DragonBreath on the profile; `OnCarve` drops four scutes on a wild one's corpse (`:75-84`); `StatLossAfterTame` for the absent `OnAfterTame` (D row 2) |
| `.../Mobiles/BritannianInfantry.cs` (100) | same (122) | HealChance 1.0 as `CanHeal` (`:74`); the Myrmidex `IsEnemy` branch dropped (inactive in ServUO too) |
| `.../Mobiles/EodonTribesman.cs` (689) | same (752) | `EodonTribe`, `BaseEodonTribesman` (`:44-206`: the tribe as `[SerializableField(0)]`, per-tribe resistances, `AggressiveAction` rally and yell `:156-180`, aggressor-only `IsEnemy` `:182-194`), `TribeWarrior`, `TribeShaman`, `TribeChieftan` with every tribe's body, hue, hair and outfit (SetWearable is cc-P194's extension). Names from pinned's savage lists, built on first use |
| `.../Items/DragonTurtleScute.cs` (24) | `Items/Resources.cs:135` | ICommodity, 0x9BCE, 1123910 |
| `.../Items/CardOfSemidar.cs` (82) | same (101) | The seven legend cards; picture gump `:45`, name `:47-54`; the default constructor deals one of the first four, as ServUO |
| `.../Items/ClimbingVine.cs` (43) | same (82) | The climb (`:33-42`); placement moved into `[GenEodon` (ServUO's `Initialize` re-adds a pair at every start; D row 6) |
| `.../EodonSpawns.cs` (159) | `Spawns/Eodon.xml` (65 rows) | The 46 kept rows as data, the P196 `BlackthornSpawns` shape; Barako rows spawn in a z 100-110 band (`:128-130`) for XmlSpawner's `/Z/100` |
| `.../EodonGeneration.cs` (209) | `TimeOfLegends.cs:51-84` (`DecorateTOL_OnCommand`) | `[GenEodon [dryrun]` / `[DeleteEodon`; the gate-beside check (`:157`); the console verb `eodon` (`:51-63`) and a start-up status line (`Configure`, `:65-76`; `Status` `:89`) |
| `server/customizations/Mobiles/NPCs/WanderingShaman.cs` (46) | `Mobiles/NPCs/WanderingShaman.cs` (61) | Forced leaf dependency of the spawns (eleven rows): a WanderingHealer in tribal dress; `ChangeRace => false` is `CheckMorph` doing nothing |
| `server/customizations/Services/Pet Training/PetTrainingHelper.cs` | | One comment (`:10-12`): it named DragonTurtleHatchling as a type the shard lacked |
| `server/tests/Services/PetTraining/PetTrainingVerification.cs` | | `TheTablesAreServUOs` asserted the hatchling was missing (`:317`); it now asserts its definition resolves |
| `server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs` (894) | | The 21 facts (section 4) |
| `CHANGELOG.md`, `VERSION` | | `2026.10.21.8`: Added (the valley, its gate, tribes, wildlife, vines) and Staff (`[GenEodon`, the unplaced creatures) |

In `D:\UO\shard-migration`: this file; `testing/bot-triage.md` (the P198 group) and `testing/playtest-steps.json`
(P198-1 to P198-6).

Dependency check first (port recipe): every `new X(` and base type in the 13 files resolved against pinned and ours
before writing; the equipment of all eighteen tribesmen exists in pinned (`Tekagi`, `PlateMempo`,
`DecorativePlateKabuto`, `WildStaff`, `JinBaori`, `Yumi` and the rest); `SetSpecialAbility`, `SpecialAbility`,
`SetWearable` and `BattleRegion` exist (ours, cc-P121/P194; pinned `Regions/BattleRegion.cs`). Not present anywhere:
`SkillMasterySpell`, `RampageSpell`, `MasteryInfo`, `ShowSpellMantra`, `TeleportsTo`, `BaseRewardTitleToken`/`Deed`.
No stem collides with pinned.

## 2. The gate, the spawns and the vines

**Where the gate is defined** (Chase's question, 10-18): pinned defines only the destination
(`PublicMoongate.cs:275`); ServUO the destination (`Scripts/Items/Functional/PublicMoongate.cs:378`) and the
placement (`TimeOfLegends.cs:75-76`). Our seeders: `ClusterFRoyalCitySeeder.EnsureMoongate` (Royal City, 850,3525,-38)
only. No decoration file anywhere names 719,1863 (pinned ships no `Data/Decoration/TimeOfLegends`; the only pinned
decoration file with a PublicMoongate is Felucca's `_star room.cfg`). Map at 719,1863 (7.0.117.0 map5): land 0x0078,
z 40, no statics: the ring of dirt, and nothing on it.

**Duplicates:** on the test world the only other Ter Mur gate is Royal City's (the dry run lists every Ter Mur gate:
`Public moongate already on Ter Mur at (850, 3525, -38)`). `[GenEodon` refuses to place beside another gate, so a gate
hand-placed on live with `[add PublicMoongate` would be left alone, and the dry run would say so first.

**The spawn table** (`EodonSpawns.cs`, generated by `gen_eodon_spawns.py` in the session scratchpad from
`Spawns/Eodon.xml`; the header carries the field mapping): name, centre, rectangle, walking range, count and delays are
the XML's (1-2 minutes, as 60-120 s), one entry per type at its MX, the tribe as the entry's constructor argument
(pinned's spawner parses it, `BaseSpawner.cs:1024-1047`). No row uses proximity, time of day, sequences, groups,
despawn or triggers (checked over all 65). Dropped:

| Dropped | Rows | Why |
|---|---|---|
| MyrmidexLarvae/Drone/Warrior | part of 4 (Eodon_Desert #1-#4) | out of scope by name; the spiders and scorpions stay, so those rows ask for 3-6 instead of 8-17 |
| TRex, GreatApe, VolcanoElemental, CubEnclosure (x3), NestWithEgg (x4), SirGeoffery, the five tribal high chiefs | 15 | the Valley of One quest line (`Quests/Eodon/Valley of One Quest/`), declined with its quest framework in CC3 |
| Hawkwind (Eodon), hawkwind2 and an xmlquestnpc "lord blackthorne" (Trammel) | 3 | `Quests/Eodon/Hawkwind`, a quest |
| WanderingShaman at MX=0 | 3 entries | XmlSpawner never spawns them |

Kept: 46 rows, 345 creatures. On the real map every one of them spawned (99 mobiles before, 444 after; section 5),
the Barako clifftop included.

## 3. Client check

Against `D:\ShatteredLegacy\client-data\classic-client-7.0.117.0` (and repeated on the server's `classic-client`, which
on this PC is 7.0.114; same answers). Scripts in the session scratchpad (`tilecheck.py`, `uopcheck.py`, the UOP hash
read directly because vseUOAware's `render_gump` refuses even stock gump 5100 on this file: a tool fault, not data).

- **Bodies** (`mobtypes.txt`): 1292 Dino_Anchisaur, 1286 Dino_Gallusaurus, 717, 832 Phoenix, 159, 1294
  Dragon_Turtle_Baby, 400/401, 605/606 (elves): all present.
- **Items** (`tiledata.mul`, rendered where unnamed): 0x9BCE (scute art), 0x9C14/0x9C15 legend cards, 0x1AA1 vines,
  0x19AB fire, 0xF6C moongate, 0x2684 (the Barrab shaman's robe graphic), hairs 0x2046, 0x2047, 0x203B, 0x203C,
  0x2FC1, 0x2FD0: all present.
- **Gumps** (`gumpartLegacyMUL.uop`): 39904-39910 and 39914, the card pictures: all present.
- **Map** (map5): 719,1863 z 40 (the gate); 678,1759 z 40 (the vines' foot); 679,1757 has a floor at z 100 (the
  clifftop the vines reach).

**Blocked on client data: nothing.**

## 4. Tests

`server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs`, 21 facts. Every expected value is a literal read
off the ServUO file. Red proof: 17 sabotages in one `--tests-only` run (Anchisaur body and hides, Gallusaurus's
ability, the tribe not saved, TribeWarrior not constructible, Jukari fire 90, the Sakkhra chieftain's Yumi a Bow, the
rally matching other tribes, fire damage 10-20, three scutes, the shaman's mask unhued, the scute's label, Krampus's
picture, the vine climbing from above, the gate at z 41, the gate-beside distance, the Jukari row's count): **20 red,
each on its own assertion, nothing else red.** The 21st (`TheStatusLineSaysWhetherTheGateStands`) was added with the
console verb and seen red alone on a sabotaged status line. The port was restored from a backup and re-checked.

| Fact | What it pins |
|---|---|
| `EachCreatureResolvesAndConstructsWithItsServUOValues` | the seven creatures: name, corpse, body, hue, fame, karma, AI, fight mode, perception 16, Medium speed, own generator |
| `TheCreaturesCarryServUOsNumbers` | hits, meat, hides, taming, the scorpion's 40% physical, gold, the infantry's blessed kit; the hatchling's slots 3-4 (below) |
| `TheAbilitiesAreServUOs` | GraspingClaw, DragonBreath; Block, BleedAttack; Anchisaur's Disarm/ParalyzingBlow |
| `EachCreatureSurvivesASaveAndReload` | round trips, a tribesman's tribe written non-default |
| `ASpawnerFillsWithEachCreatureAndEachTribe` | a spawner fills with each, and with all 18 tribe/role pairs by argument |
| `EachTribesmanIsBuiltForItsTribe` | 18 builds: name, hue, race and body, the one 100% resistance (base), Barrab's poison immunity, hits, fame, unmovable kit |
| `EachTribeCarriesServUOsWeapon` | nine weapons and hues, the unarmed Urali, the shaman's range, gold and bandages |
| `AnAttackedTribesmanRalliesItsOwnTribeAndFightsOnlyAggressors` | aggressor-only enemies, the rally, the yell, the yell clearing after 6 minutes |
| `TheInfernusLaysATrailOfFireThatBurns` | fire round the target, 50-85 damage, burns out by 41 s, a reloaded fire deletes itself |
| `AWildHatchlingCarvesFourScutes` | four on a wild corpse, none on a tame one |
| `TheWanderingShamanIsAHealerInTribalDress` | parent, title, only the mask as clothing, bone arms and legs, the staff |
| `TheItemsConstructAndSurviveASave` | scute, card, vine: art, label, commodity, round trips |
| `EachCardShowsItsOwnPictureAndName` | the seven pictures and names; the default deals one of four |
| `TheVineClimbsOnlyFromBesideAndBelowIt` | the climb and its three refusals |
| `PinnedSendsTOLPlayersToTheSpotTheGateGoesOn` | pinned's TerMurEodon entry is 719,1863,40, the gate's spot |
| `TheDryRunPlacesNothing` | no item added; the report |
| `GenEodonPlacesTheGateTheVinesAndTheSpawnersAndReplacesThemOnARerun` | 1 gate, 2 vines, 46 spawners on Ter Mur; a re-run replaces; delete removes |
| `TheStatusLineSaysWhetherTheGateStands` | the start-up/console line, missing and present |
| `GenEodonLeavesAnotherGateAlone` | a hand-placed gate beside the spot: no second gate, and delete leaves it |
| `TheSpawnTableIsEodonXmlWithoutMyrmidexOrTheQuestLine` | 46 rows, no Myrmidex or quest types, ServUO's numbers spot-checked, the Barako z 100 rows |
| `EveryEntryInTheTableSpawns` | every type/argument pair in the table spawns |

Two facts in older files changed on purpose: `PetTrainingVerification.TheTablesAreServUOs` (the hatchling now
resolves). The first green attempt also turned `CC6Batch3...Bloodworm` and `CC6Batch8...Medusa` red: my Infernus fact
killed a 50-hit player at 1000,1000 Ter Mur, where those facts stand, and the corpse reached them. The facts now use
200,3900 and a 150-hit player. And one flake caught on a later green run: ServUO's Infernus "centre always burns" test
compares world coordinates, so a drop places nothing one time in 512; the port keeps that, the fact drops until
something burns.

Runs, all through `docker/uo/build.sh` under the docker-build lock, builder tag `sl-uo-builder:cc-P198`: four
`--tests-only` cycles to green (an xUnit analyzer error; then the six failures above; then the infantry gold, which is
250-300 plus the Rich loot pack's gold), the red run, a full green build, the status fact's red run, two more full
builds (the start-up hook moved to Configure; the flake). **Final: 1,937 tests, 1,934 passed, 4 skipped, 0 failed;
image `sl-modernuo:cc-P198` `1e52dfa72dee`.**

## 5. Test shard (client-free)

Under the test-shard lock, 07:25 to 07:35 Chicago time. This PC has no game client, so the proof is the server console
(`winpty docker attach`, cc-P267's route) and the container log. Before starting, the test save
(`server/lib/uo/modernuo-test/Saves`) and `shard-commit.json` were copied to the session scratchpad.

| Step | Logged |
|---|---|
| `Start-TestShard.ps1 -Image sl-modernuo:cc-P198` | `[ShardVersion] Shattered Legacy 2026.10.21.7`, `Loading world done (652 items, 99 mobiles)`, healthy. Only the standing WRNs (`stats` already registered; `testCenter.skillGainMultiplier` retired). The first start showed no `[Eodon]` line: the hook was in Initialize, after the load. Moved to Configure and rebuilt; second start: `[Eodon] 0 objects placed by GenEodon; Eodon moongate at (719, 1863, 40): MISSING (run [GenEodon).` |
| `eodon dryrun` | `Public moongate already on Ter Mur at (850, 3525, -38) (not placed by GenEodon).` `Dry run, nothing changed. A run would delete 0 objects ... the Valley of Eodon public moongate at (719, 1863, 40) on Ter Mur. 2 climbing vines ... 46 spawners asking for 345 creatures.` |
| `eodon generate` | `Eodon: 1 moongate, 2 climbing vines, 46 spawners.` `Eodon generation complete.` |
| `eodon status` | `49 objects placed by GenEodon; ... present (GenEodon's).` |
| `save`, `docker restart -t 60` | `Loading world done (1962 items, 444 mobiles)`, no exception, no error; `[Eodon] 49 objects ... present`. **345 more mobiles: every requested creature spawned on the real map, and all of them reloaded.** |
| `eodon delete`, `eodon status` | `removed 49 objects GenEodon placed.` then `MISSING` |
| `-Down`; the save copied back; `-SkipBuild` | the test shard back on `sl-modernuo:latest`, `Loading world done (652 items, 99 mobiles)`; `shard-commit.json` restored |

**Why the test world was put back rather than left with the gate:** the generated world holds the new types
(tribesmen, the shaman, the vines, spawners naming them). Until P198 is merged, any Golem who starts the shared test
shard on an image without them would load a save with types its server does not have. So the proof was run and the
save restored; the test world gets the gate for good with the one command below, once the test shard runs a build
with P198 in it. The `good-2ab20d7-dirty` tag the start script put on my image was removed (a dirty image is not a
roll-back target); `sl-modernuo:cc-P198` stays.

## 6. Deviations and decisions for Chase

Rows for the fidelity register (agents never edit `docs/`):

| # | What | ServUO | Here | Why |
|---|---|---|---|---|
| 1 | Anchisaur's masteries | casts Rampage or arms move 740 every 45-70 s in combat | does neither | Skill Masteries are not on this shard (no type in pinned or ours; BasePeerless notes the same) |
| 2 | Hatchling taming | first tame caps skills and takes 55% off each | `StatLossAfterTame` (stats halved) | pinned has no `OnAfterTame`; the port recipe's nearest thing, the Raptor precedent |
| 3 | Tribesmen masteries | the AI gets their weapon skill's masteries | none | same as row 1 |
| 4 | Shamans' spell words | spoken (`ShowSpellMantra`) | silent | pinned's `Spell.SayMantra` speaks for players only (`Spell.cs:457`); a pinned patch would be needed, for one creature type |
| 5 | Tribesmen and infantry vs Myrmidex | `IsEnemy` asks the invasion when it is active | aggressor test only | the invasion is out of scope; ServUO with it inactive is identical |
| 6 | Climbing vines | placed by `Initialize` at every start, and doubled at every restart (it looks at 687,1759, places at 678,1759) | placed by `[GenEodon`, replaced on a re-run | a world command, like everything else placed; ServUO's coordinates kept |
| 7 | Eodon spawn | `[XmlLoad Spawns/Eodon.xml` | 46 of 65 rows, no Myrmidex or quest rows | scope; the desert rows lose their Myrmidex share of MaxCount |
| 8 | Barako village spawn height | XmlSpawner sets Z = 100 after placing | spawn bounds z 100-110 | pinned's spawner picks z inside its bounds |
| 9 | Infernus fire after a restart | written with no data (would corrupt the load) | saved empty and deleted after load | same player outcome, no broken record |
| 10 | No SmartSpawning | n/a in Eodon.xml | | (no change: every row is SmartSpawning False) |
| 11 | Hatchling control slots | ServUO's 5, clamped by its pet training to 4 (3 if it rolled low) | the same, through cc-P130 | faithful; noted because a reader of the file sees 5 |

Decisions, for Chase:

1. **Run `[GenEodon` on live?** Players then get a gate into the valley and 345 creatures there (tribes are innocent
   until attacked; dinosaurs and lava creatures are not). Commands below. Nothing places it by itself.
2. **The Dragon Turtle champion** (next prompt): pinned's `ChampionSpawnType.DragonTurtle` and its spawn table are
   commented out (`Engines/CannedEvil/ChampionSpawnInfo.cs:19`, `:123`), so it needs a pinned patch to enable, plus
   ServUO's `DragonTurtleEgg` artifact (pinned's `BaseChampion.GetArtifact` is not virtual), a `TeleportsTo`
   behaviour pinned lacks, the bubble debuff (pinned has `BuffIcon.DragonTurtleDebuff`), and ServUO's two champion
   spawns (Ter Mur 451,1696,65 and Felucca 7042,1889,60).
3. **The Eodon title scroll:** declined. `EodonTribeRewardTitleToken` and its eight deeds sit on ServUO's
   `BaseRewardTitleToken`/`BaseRewardTitleDeed`, the Mondain's Legacy quest-reward framework CC3 declined; they are
   rewards of the Myrmidex and Valley of One quests, both out.

## 7. Q-064's Eodon recipe drop: still open, left for the next prompt

`TimeOfLegends.CheckRecipeDrop` (ServUO `TimeOfLegends.cs:98-133`) is still absent: nothing in ours handles a death
inside Eodon (`SpellHelper.IsEodon` exists only inside our treasure-map code). It is not done here because it is not a
hook alone: a third of its drops are Aloron and Darden armour (now portable: the armour set-bonus subsystem CC3 found
missing is in the tree, with its tests under `server/tests/Items/Artifacts/Equipment/Armor/Sets/`; none of the 12
pieces is ported), and two thirds are recipe scrolls 560-566 (the seven garments, not ported,
`notes/q-064-recipe-garments.md`), 570-577 (Tiger Pelt) and 580-584 (Dragon Turtle Hide), whose items exist but whose
recipes are registered nowhere (D32). Those recipes also meet the shard's own recipe gating (F-43,
`Engines/Craft/ClusterFRecipeGate.cs`), which wants a decision on whether an Eodon kill can hand out a gated recipe.
This prompt made two pieces of that cheaper: Eodon now has creatures to die there, and `DragonTurtleScute` (the
Dragon Turtle Hide recipes' material, D32/Q-066) now exists, dropped by the hatchling. **Left for the next prompt:**
the seven garments, the twenty recipe registrations, the 12 armour pieces, the death hook, and Chase's call on gating.

## For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) once P198 is merged, before trying these. Then, as admin,
`[GenEodon dryrun` (read it: it lists every gate already on Ter Mur and says whether it will place the Eodon one), then
`[GenEodon` once. To try it in game:

1. **The gate:** at any public moongate (Britain `[go 1336 1997 5`) pick Ter Mur, Valley of Eodon. You land at
   `[go 719 1863 40`, on the ring of dirt, beside a blue gate; it takes you back to Royal City.
2. **The tribes:** `[go 701 2106 40` (Jukari), `[go 362 1848 0` (Kurak), `[go 150 1769 80` (Barrab),
   `[go 412 1595 40` (Urali), `[go 554 1467 40` (Sakkhra). They leave a player alone; attack one and the rest of that
   tribe nearby turns on you, one shouting Ahhhh-OOOO! Ahhh-OOOO!.
3. **The vines:** `[go 678 1760 40`, double-click the vines: you climb to 679 1757 100, the Barako village.
4. **The wildlife:** `[go 425 1404 40` (dinosaurs and the swamp), `[go 506 1582 40` (jungle), `[go 175 1861 0` (the
   desert), `[go 856 2132 40` (lava). Worth seeing by eye: whether the anchisaur and gallusaurus animate.
5. **The unspawned ones:** `[add Infernus` (fight it: patches of fire), `[add DragonTurtleHatchling` (kill and carve:
   four scutes), `[add CardOfSemidar` (double-click: a legend card), `[add BritannianInfantry`, `[add GreaterPhoenix`.
6. **Test world boot and generation:** done by CC on this PC's test shard (section 5).

**Live, when you choose** (Administrator, in game; nothing else needed, the build carries it):

```
[GenEodon dryrun
[GenEodon
```

Read the dry run first. It should list Royal City's gate (850, 3525, -38) as already there and say it will place the
Valley of Eodon gate at (719, 1863, 40); if it says "no Eodon moongate", a gate is already beside the spot and nothing
needs placing. `[DeleteEodon` undoes it. The server console has the same: `eodon dryrun`, `eodon generate`,
`eodon status`, `eodon delete`; every start logs one `[Eodon]` line saying whether the gate stands.

## Play-test items added

Through the For Chase list; Who in `testing/bot-triage.md` (P198 group), steps in `testing/playtest-steps.json`:
P198-1 BOT-PARTIAL (the gate), P198-2 BOT-PARTIAL (the tribes), P198-3 BOT (the vines), P198-4 BOT-PARTIAL (the
wildlife), P198-5 BOT-PARTIAL (infernus, hatchling, card), P198-6 CC (done, section 5).
`tools/tests/test_play_who.py`: 18 tests, the same two pre-existing failures P194 and P196 recorded (older items with
no Who or Where, now 96 of them, none P198's).

## Port-list numbers

`SL_SHARD=D:/ShatteredLegacy python tools/progress.py`: Eodon remainder **6 of 19 before, 16 of 19 after**; the port
list **736 to 746 of 983** files (4 of 16 systems in, unchanged). Counted by hand against the 19 ServUO files: 17 done
in substance (`Resources.cs` complete across P129 and this task), `DragonTurtle.cs` left, `EodonRewardTitleScroll.cs`
declined.

## Repo size rule

No new file over 5 MB in either repo (the largest new file is the 894-line test, about 45 KB). Scratch (build logs,
the generator scripts, the test-world backup, the port backup used for the red run) is in the session scratchpad,
outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, first run, no BLOCKED:

```
Repo Result
---- ------
code dry run
docs dry run
```

Code: 19 files (the 13 port files, the test, the two Pet Training edits, CHANGELOG.md, VERSION). Docs: this file,
`testing/bot-triage.md`, `testing/playtest-steps.json`, and four files `tools/progress.py` rewrote when I counted the
port list (`README.md`, `dashboard.html`, `tools/progress.json`, `tools/expansion-coverage.json`: the Eodon row 6 to 16
of 19, the port list 736 to 746). The dry run also lists P180, P181 and P185 as prompts whose notes are not finished;
they are other Golems' and untouched.

P198 DONE
