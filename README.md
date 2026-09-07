# Shattered Legacy: ServUO content on ModernUO

Working repo for **staying on ModernUO** and pulling selected ServUO content into it,
piece by piece. Reversed from the original migrate-to-ServUO plan on 2026-09-06; see
`docs/direction-decision.md` for why.

This repo is the shared source of truth for everyone working on the migration,
human or agent. If a decision is not written down here, it is not decided.

## Why we are doing this

ModernUO declares expansions through `EJ` but never implemented the content.
Measured by file count in each tree:

| Content | ServUO pub57 | ModernUO main |
|---|---|---|
| High Seas | 134 | 0 |
| Time of Legends / Eodon / Myrmidex | 74 | 0 |
| Ter Mur / Stygian | 18 | 5 (spawn data only) |

Target scope is the **full post-ML world including naval combat and Eodon**, which is
precisely the content ModernUO lacks. See `docs/direction-decision.md` for why porting
the other way was costed and rejected.

## What we give up

ServUO targets `net48` and runs under Mono off Windows, versus ModernUO's .NET 10.
Serialization goes from source-generated back to hand-written. This is a deliberate
trade of engineering quality for content reach. Do not relitigate it in code review.

## Layout

```
docs/     decisions and plans. Read these first.
tools/    converters and migration scripts (spawners, accounts)
notes/    working notes, scratch findings, anything not yet a decision
```

## Start here

1. `docs/migration-plan.md` - the seven phases, in order
2. `docs/direction-decision.md` - why ServUO and not the reverse port
3. `docs/shard-inventory.md` - what we actually have to migrate, and the revised Phase 2 scope
4. `docs/client-analysis.md` - what UOAlive and Immortal Realms customized, and the
   custom-facet finding that changes our map plans

## Current status

- [x] Direction decided: migrate to ServUO
- [ ] **URGENT** Deploy/restart the ModernUO image so startup enforces SHA2 password hashing
      (enforcement is staged in the shard infrastructure repo; live state is unverified)
- [x] Custom surface counted: **~131 files / ~39,900 lines**, already isolated from
      upstream. No Core bucket. See `docs/shard-inventory.md`
- [x] Shard located: `shattered-legacy-infrastructure` (builds ModernUO from pinned commit)
- [x] Add `client-data/` and `server/uo/` to that repo's `.gitignore`
- [ ] Stand up stock ServUO pub57 reference shard
- [x] Create the independent `ServUO-work` scratch clone; keep the pub57 reference pristine
- [ ] Write spawner JSON to XmlSpawner XML converter
- [ ] Write accounts exporter (MUO binary to ServUO accounts.xml)

## Migration progress

<!-- PROGRESS:START -->
**Direction: staying on ModernUO.** ServUO content is pulled in piece by piece. There is no total to reach, so there is no single completion percentage here by design.

```
Setup health   ██████████████████████  7/7   blocking defects resolved
```

| Setup defect | Resolved |
|---|---|
| CraftContext members (RepeatCount, RepeatItem, RepeatTypeRes) recovered | yes |
| ResourceInfo extended wood enum members (8) recovered | yes |
| OutridersGuildmaster recovered | yes |
| server/customizations compiles standalone | yes |
| apply-patches.sh fails on failed patch | yes |
| stale server/customizations/migrations removed | yes |
| RegenRates routing made explicit | yes |

**Patches:** 15 total, **0 currently failing to apply**, 8 triaged, 3 found obsolete. `apply-patches.sh` fails the build on a failed patch, so a green build means every patch applied.

### Content moved over: 60 of 2,045 candidate files (2.9%)

```
TOTAL                          █░░░░░░░░░░░░░░░░░   60/2045    2.9%

Items/Resource                 █████████░░░░░░░░░   29/61     47.5%
Items/Artifacts                █░░░░░░░░░░░░░░░░░   11/325     3.4%
Items/Equipment                █░░░░░░░░░░░░░░░░░    8/148     5.4%
Services/Expansions            █░░░░░░░░░░░░░░░░░    6/175     3.4%
Mobiles/Normal                 █░░░░░░░░░░░░░░░░░    4/138     2.9%
Items/Addons                   █░░░░░░░░░░░░░░░░░    1/169     0.6%
Items/Containers               █░░░░░░░░░░░░░░░░░    1/31      3.2%
Mobiles/NPCs                   ░░░░░░░░░░░░░░░░░░    0/222     0.0%
Services/Revamped Dungeons     ░░░░░░░░░░░░░░░░░░    0/150     0.0%
Services/XmlSpawner            ░░░░░░░░░░░░░░░░░░    0/97      0.0%
Items/Decorative               ░░░░░░░░░░░░░░░░░░    0/88      0.0%
Quests                         ░░░░░░░░░░░░░░░░░░    0/84      0.0%
Items/Quest                    ░░░░░░░░░░░░░░░░░░    0/78      0.0%
Items/Consumables              ░░░░░░░░░░░░░░░░░░    0/59      0.0%
Services/CleanUpBritannia      ░░░░░░░░░░░░░░░░░░    0/52      0.0%
Items/StoreBought              ░░░░░░░░░░░░░░░░░░    0/51      0.0%
Items/Functional               ░░░░░░░░░░░░░░░░░░    0/49      0.0%
Services/New Magincia          ░░░░░░░░░░░░░░░░░░    0/40      0.0%
Services/BulkOrders            ░░░░░░░░░░░░░░░░░░    0/28      0.0%
```

_Counted by matching ServUO file stems (excluding those stock ModernUO already has) against `server/customizations`. Auto-counted, never hand-edited._

**Ported systems logged: 36**

| Content | Task | Notes |
|---|---|---|
| PlagueRat | P1 | P1 reference port. 88 lines to 55. Builds, spawns, survives save/reload. No speed override: SpeedClass Medium, per the Q-008 answer (ModernUO's npc-speeds.json fallback is the standing rule for all ported creatures). |
| GreaterPoisonElemental | P2 | P2 timed port, headless. 123 lines to 80. Compiles clean, server starts, world saves and reloads; type registration proven by reflection over the shipped assembly. Adds PackItem, multi-AddLoot, an OnDeath override, AI_Mage and the two-argument stat overloads over what PlagueRat covered. No speed override, per Q-008. An instance in a saved world is NOT verified: headless has no spawn - batched for a later client spot check. |
| LuckyCoin | P2, completed by S2 | Forced dependency of GreaterPoisonElemental; ModernUO has no LuckyCoin. P2 ported it without OnDoubleClick because that targets a FountainOfFortune (Q-010). S2 built the Fountain and RESTORED OnDoubleClick and its InternalTarget, so Q-010 is CLOSED and docs/fidelity-principle.md should drop its entry. Pinned by ShatteredLegacy.Tests.FountainOfFortuneVerification.DoubleClickingACoinInTheBackpackAsksForATarget. Reused by 12 Mobiles/Normal creatures, of which 1 (GreaterPoisonElemental) is in the tree today. |
| RaptorTeeth | CC3 | ICommodity stackable resource. ServUO's TextDefinition Description becomes ModernUO's int DescriptionNumber; the Constructable X()/X(int) pair collapses to one [Constructible] X(int amount = 1). |
| AncientPotteryFragments | CC3 | Forced dependency of Raptor; ModernUO has none. Trivial Item, ported complete, no deviation. One extracted type per file, per the LuckyCoin precedent (Q-010). |
| PerfectBanana | CC3 | Forced dependency of SilverbackGorilla; ModernUO has none. Trivial stackable Item, ported complete, no deviation. |
| RaptorClaw | CC3 | Boomerang artifact. Boomerang, Slayer, Attributes and WeaponAttributes.HitLeechStam all exist in ModernUO. Only IsArtifact dropped: it is a ServUO-only Server.Item virtual whose every consumer (pigments, NaturalDye, AlterItem, RunicReforging) is also ServUO-only, so it has zero readers in ModernUO. |
| StretchedDinosaurHide | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| CarvedMyrmydexGlyph | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| WakuOnASpit | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| SacredLavaRock | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| WhiteTigerFigurine | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| DragonTurtleHatchlingNet | CC3 | One of six TOL tribal reward decorations split out of a single ServUO file, one type per file. Derives from Item, not ModernUO's BaseDecorationArtifact, because ServUO sets ShowArtifactRarity=false and ModernUO's base adds the rarity line unconditionally; the three members that base contributes are reproduced so the rendered properties match ServUO exactly. |
| Allosaurus | CC3 | Three SetWeaponAbility calls become one GetWeaponAbility() over Utility.Random(3). GenerateLoot's IsChampionSpawn branch collapses to the non-champion arm and SetToChampionSpawn is dropped: ModernUO's BaseCreature has neither, and its ChampionSpawn never calls back into the creature. AttacksFocus dropped. |
| Archaeosaurus | CC3 | Two SetWeaponAbility calls become GetWeaponAbility() over Utility.RandomBool(). DragonBlood => 6 dropped: ModernUO has neither the carving property nor the item. AttacksFocus dropped. |
| Dimetrosaur | CC3 | SetWeaponAbility x2 become GetWeaponAbility(). Two behaviours dropped with no ModernUO equivalent: SetAreaEffect(AreaEffect.PoisonBreath), and OnAfterTame, which quartered Hits on first tame - StatLossAfterTame gives AnimalTaming's ScaleStats(0.50) instead. FruitsAndVegies -> FruitsAndVeggies. AttacksFocus and the champion-spawn hooks dropped. |
| Najasaurus | CC3 | Clean. Its only PetTrainingHelper call is in the version-0 deserialize upgrade path, which new content at version 0 never runs, and the constructor already sets Poisoning skill and HitPoison - so dropping it is a no-op. AttacksFocus dropped. |
| Saurosaurus | CC3 | SetWeaponAbility(ConcussionBlow) becomes GetWeaponAbility(). SetSpecialAbility(TailSwipe) and SetSpecialAbility(LifeLeech) dropped - PetTrainingHelper, which ModernUO lacks; ServUO's own source carries the comment "Missing: Life Leech, Tail Swipe ability". DragonBlood => 8 dropped. AttacksFocus dropped. |
| SilverbackGorilla | CC3 | The only candidate creature calling no PetTrainingHelper method. Banana-throw OnActionCombat ported intact: the 13-argument MovingParticles overload with EffectLayer, AOS.Damage and Region.IsPartOf(string) all exist unchanged. DateTime.UtcNow -> Core.Now. |
| Raptor | CC3 | The only ported creature with real persisted state: m_IsFriend becomes [SerializableField(0, setter: "private")] and ServUO's delete-on-deserialize becomes [AfterDeserialization(false)]. The Raptor()/Raptor(bool) Constructable pair collapses to one [Constructible] Raptor(bool isFriend = false). Pack-friend spawn timer, PackInstinct.Ostard, Map.CanFit and AIObject.Action all port unchanged. SetWeaponAbility(BleedAttack) becomes GetWeaponAbility(). Drops AncientPotteryFragments and RaptorClaw, both ported alongside. |
| Eodon core content (17 files) | CC3 | Six dinosaurs, Raptor, RaptorClaw, RaptorTeeth, six TOL decorations, PerfectBanana, AncientPotteryFragments. Four build batches, zero failures. All 17 types verified registered by reflection over the shipped assembly. Deviations logged in docs/fidelity-principle.md. |
| SetItem (SetItem enum, ISetItem, SetHelper) | S1 | The Mondain's Legacy armour set-bonus subsystem. Ported to ModernUO's IPropertyList, StatMod and AosSkillBonuses APIs. Omits SetHelper.GetSetSlayer (ModernUO's SlayerName has no Dinosaur/Myrmidex; consumers are BaseWeapon combat code, out of scope) and the IFishingAttire branch (no such interface in ModernUO; Fisherman set not ported). Deviations D-2 and D-4 in notes/s1-armour-sets.md. |
| BaseSetArmor | S1 | The key design decision of S1. ServUO puts set state on BaseArmor itself; doing that in ModernUO would mean bumping BaseArmor's [SerializationGenerator(9)] to 10 and owning a migration for an upstream file. Instead this additive abstract class at version 0 carries the state and set content derives from it. Behaviourally identical for set content, because no stock ModernUO armour is a set item (verified at runtime). |
| PlayerMobile set resistances | S1 | Additive partial class, no patch needed: PlayerMobile is already partial and is not source-generated. Overrides the GetItemResistance virtual that Mobile-set-item-resistance-hook.patch introduces. |
| TigerPelt armour (8 files) | S1 | CC3 called these 'itself set-bonus content'. That was wrong: grep SetID over all eight returns nothing. They are plain BaseArmor leaf armour and were never blocked. Ported unchanged, re-parented to BaseSetArmor so the Aloron pieces that derive from them can carry set state. Weight moves from a ctor assignment to a DefaultWeight override, the ModernUO idiom. |
| Aloron's Armor set (8 files) | S1 | The CC3 decline, reversed. Four-piece set (SetItem.Aloron), SetAttributes BonusMana 15 / LowerManaCost 20, SetSelfRepair 3, per-piece resist bonuses 8/8/9/8/8. Verified at runtime: four pieces worn gives 60/60/60/60/60 resists and BonusMana 15 through AosAttributes.GetValue. Two deviations: AbsorptionAttributes.EaterCold=2 omitted (SAAbsorptionAttributes is a separate missing subsystem that drags in three more), and the Dinosaur Slayer omitted along with its tooltip line, rather than advertise a bonus that does nothing. D-1 and D-2 in notes/s1-armour-sets.md. |
| Armour set-bonus subsystem + Aloron set + TigerPelt | S1 | First subsystem built rather than ported. Unblocks 114 further ServUO files. Three patches, one of them the first into the ModernUO core project (Mobile.ComputeResistances), allowed because no UOContent hook exists and the alternative was copied upstream logic. Four deviations logged, all omissions. |
| FountainOfFortune | S2 | BaseAddon with a reward loop, three static tables, a defrag timer and a resurrect hook. Subsystem-shaped, so it ships with a test per docs/subsystem-policy.md - the first content task to use S4's route. Needs server/patches/PlayerMobile-fountain-luck-bonus.patch: ServUO routes the luck reward through PlayerMobile.RealLuck, which ModernUO does not have, and its three luck consumers all read Mobile.Luck. ModernUO's ResurrectGump takes no callback, so FountainResurrectGump subclasses it rather than patching upstream. Two reward cases are unreachable in ServUO too (Random(4) over a six-case switch) and were ported unchanged. NOTHING PLACES ONE: ServUO builds it in Services/Underworld/Generate.cs, which is not ported. Q-021. |
| GemologistsSatchel | S2 | The reward branch that blew S2 past its estimate. Reads Imbuing.IngredTypes, a 42-entry Type[] at Services/LootGeneration/Imbuing/Core/Imbuing.cs:1735, of which 35 were missing from ModernUO. Not a subsystem pull-in - all 35 are leaf items - so all 35 were ported (Q-020, Chase chose option A). The 42-entry array now lives in this file as a private static, verbatim and complete; verified at runtime as length 42 with no nulls. |
| SolesOfProvidence | S2 | Sandals with Attributes.Luck = 80. Loses ServUO's IsArtifact override: ModernUO has no such member and every ServUO consumer of it (RunicReforging, BasePigmentsOfTokuno, NaturalDye, AlterItem, ArcaneGem) is also absent, so it is inert. Deviation D-1. |
| Imbuing ingredient set (35 leaf items) | S2 | EnchantedEssence and RelicFragment are core cluster members; the other 33 are forced dependencies of GemologistsSatchel. All are Item or Item,ICommodity stackables with an ItemID and a cliloc and nothing else - grep for 'new X(' across all 31 Resource files returns zero matches. Files are named after the class, so ServUO's SeedRenewal.cs, LavaSerpenCrust.cs and ElvenFletchings.cs become SeedOfRenewal.cs, LavaSerpentCrust.cs and ElvenFletching.cs; the TypeAlias attributes are carried across unchanged. These are Stygian Abyss drops that CC5 and CC6 want regardless, so the overrun buys reusable content. |
| Fountain of Fortune cluster (38 files) | S2 | Reverses the second decline. Restores LuckyCoin's OnDoubleClick for all 12 coin droppers. One patch: PlayerMobile.Luck, because ServUO routes the reward through RealLuck which ModernUO lacks. Ships with a regression test. Nothing places a fountain yet - Q-021 gives the OSI coordinates. |
| JourneyToTheAthenaeumIsle + QueenZhah | S5 | First ServUO quest on ModernUO's MLQuest engine. SlayObjective -> KillObjective, 10x ObtainObjective -> 10x CollectObjective with ShowDetailed=false carrying clilocs 1150933-1150942, BaseReward -> ItemReward. Registered from a Configure() hook via MLQuestSystem.Register, because apply-patches.sh mirrors .cs only and Data/MLQuests.cfg is CRLF data. Deviation D-S5-3: QueenZhah is undressed, her seven gargoyle items (~470 ServUO lines) are all absent from ModernUO. Pinned by 5 tests in ShatteredLegacy.Tests.AthenaeumIsleQuestVerification. |
| MinionOfScelestus | S5 | Kill-objective target for the S5 quest. Stats, resistances, skills, loot, HitPoison, treasure level, mount knockoff and home-return are verbatim. Two deviations: D-S5-1 loses SetSpecialAbility(DragonBreath) (Pet Training, CC6 decline, Saurosaurus precedent); D-S5-2 loses TaintedLifeAura, which would need additive patches into BaseWeapon and AOS. ServUO's Poison.Parasitic maps to ModernUO's Poison.LethalParasitic (Misc/PoisonKinds.cs). Not spawned - batched for the client spot check. |
| GargishDocuments (12 types) + BaseLocalizedBook + Note | S5 | The ten Collect-objective targets, the reward book, and the two base classes underneath them. Forced dependencies found by the array walk, ported to the leaf per LuckyCoin: ModernUO's Items/Books has BaseBook/BookContent/BookPageInfo, all authored-text, none cliloc-paged, so this is additive and not a duplicate. Both reader gumps were rewritten from ServUO's Gump API onto DynamicGumpBuilder - a real rewrite, and UNVERIFIED without a client. D-S5-4: ChronicleOfTheGargoyleQueen1.Initialize() became a static initializer; the values are constants so behaviour is identical. |
| SAAbsorptionAttributes + DamageEaterContext | S6 | Subsystem, not content. Additive against BaseAttributes, which ModernUO already ships. The property reaches items through an additive IAbsorptionItem interface rather than fields on BaseArmor/BaseWeapon/BaseJewel/BaseClothing, so no upstream serialization version is bumped - S1's decision, reused. BaseSetArmor is the only carrier today, at serialization field 11. The effect reaches combat through AOS-damage-eater-hook.patch, 16 added lines in Projects/UOContent/Misc/AOS.cs at ServUO's own call site. Pinned by six tests in ShatteredLegacy.Tests.AbsorptionAttributesVerification, of which ColdDamageThroughAosDamageReachesTheEater was proved to fail with the patch skipped. |

### Task list (15 of 22 done)

```
Tasks          ███████████████░░░░░░░  15/22   Foundation and the port pipeline
```

| | Task | Status | Notes |
|---|---|---|---|
| `F1` | Recover the three missing pieces so customizations compiles standalone | done | Verified by a clean Docker build during F3, now meaningful because a patch failure can no longer pass silently. |
| `F2` | Make apply-patches.sh fail on a failed patch | done | Runner fails on a failed patch and mirrors customization subdirectories. Resolves Q-002. |
| `F3` | Triage the seven failing patches | done | Eight broken, not seven. Five repaired, three removed as absorbed by our own full-file replacements. None obsolete due to ModernUO changing. |
| `F4` | Delete stale server/customizations/migrations/ | done | 3 PetMimic JSONs diverging from the canonical v0-v8 set. |
| `F5` | Make RegenRates routing explicit | done | Works by accident today: both land in Misc/ so ours overwrites. |
| `P1` | Validate the port recipe with one real port | done | PlagueRat ported, built, spawned, saved and reloaded intact. Both draft fidelity traps were wrong (range perception was backwards; ServUO ignores its own speed args) and are corrected in notes/port-recipe.md. Three of the five F3 patches exercised at runtime: bandage-on-PetMimic and talisman durability both work; MAKE X works with no button overlap but its label uses an HTML colour where AddLabel wants a hue, so it renders invisible. See notes/cc1-p1-runtime-validation.md. Open: Q-008 (speed model), and new evidence on Q-007 (forcing SHA2 breaks new-account login on the live shard). |
| `P2` | Second port, timed, using only the recipe | done | GreaterPoisonElemental, ~20 min headless. Per-file work ~1:10, warm build cycle 0:44, so build cycles are NOT the dominant cost. A batch of 20 is about an hour. Bigger finding: of 462 Mobiles/Normal files only 275 (60%) are clean - 132 call Pet Training methods ModernUO lacks, 89 reference a missing type. CC6 batches draw from the clean 60%. See notes/cc2-timed-port.md. |
| `C1` | Eodon core content | done | 17 files ported, 12 declined - not the 'about 22' the docs claimed, wrong for the third time. Six dinosaurs, Raptor, RaptorClaw, RaptorTeeth, six TOL decorations. Declined with evidence: the eight Aloron pieces (armour set-bonus subsystem), the Valley of One quest line (8 files on ServUO's ML quest framework, a subsystem port), MoonstonePowerGenerator (Myrmidex content, matched on 'moonstone'). Time of Legends 53/157 to 59/157. Eleven deviations logged. See notes/cc3-eodon.md. |
| `S1` | Armour set-bonus subsystem | done | Spike passed. SetItem.cs plus three targeted patches (44 added lines, 6 changed), no upstream logic copied, no upstream serialization version bumped. Aloron set and TigerPelt ported. My 187 unblock figure was wrong: the real number is 114. Bump checklist in notes/s1-armour-sets.md section 3. |
| `S4` | Test route for ported subsystems | done | server/tests/<path> mirrors into Projects/UOContent.Tests/Tests/<path> through mirror_cs_tree(), the same F2 mechanism structured customizations use, with the same destination-must-not-already-exist guard. S1's tests are committed and green - four [Fact] methods, not the six docs/tasks.md claims (Q-019). No patch to an upstream project file was needed: UOContent.Tests.csproj has no <Compile Include> items and is already in ModernUO.slnx. Four negative proofs, all failing the build: a failing assertion, a test that does not compile, a wrong namespace, an upstream path collision. Three of the four fail docker build itself; a failing assertion fails docker/uo/build.sh, because every ModernUO fixture needs io_uring and docker build cannot relax seccomp (Q-018). build.sh is now the build command. See notes/s4-test-route.md. |
| `S2` | Fountain of Fortune cluster | done | 38 files, 2,292 lines, 1 patch, 5 tests. Closes Q-010: LuckyCoin.OnDoubleClick restored across all 12 coin droppers. My ~900-line estimate was wrong in both directions: the core is 465 lines, but GemologistsSatchel reads a 42-entry Imbuing table and 35 entries were missing. All 35 were dependency-free leaf items, so they were ported. First content task to use S4's test route. |
| `S3` | Cost every remaining decline | done | Measurement only. Found the error under every count on this project: 3,134 of ServUO's 6,144 files are types ModernUO already declares. CC6's backlog is 137, not 360. Best ratio is SAAbsorptionAttributes; biggest surprise is that ModernUO already ships an ML quest engine with 205 of ServUO's 408 quests; strongest decline is Skill Masteries. See notes/s3-decline-costs.md. |
| `S5` | Translate one ML quest onto ModernUO's engine | done | JourneyToTheAthenaeumIsleQuest translated onto ModernUO's ML quest engine end to end. 6 files, 1,063 ServUO lines in, 745 out, plus a 284-line test with 5 facts. Gated build green at 14 tests. THE MAPPING HOLDS for 4 of 5 objective types: Slay->Kill and Obtain->Collect are identical and are proven by test; Apprentice->GainSkill holds (upstream already made this exact translation in NewHavenSkillTraining.cs) but loses region-scoped acceleration and needs cap x10; Deliver->Deliver holds but the destination name moves to a [QuesterName] attribute and Quest.StartingItem has no counterpart (Q-025); Escort->Escort holds and its dropped fame/compassion parameters are unused across all 30 ServUO call sites. THE REAL FINDING is not the mapping: of the 203 missing quests, 164 use one standard objective type and translate mechanically, but 39 hand-write a BaseObjective subclass with no counterpart - 25 of them InternalObjective. QuestionAndAnswerObjective is 2 of those 39, not the tail. Also: it is the ONLY quest in all 408 that uses two standard objective types, and Valley of One is a poor first batch (3 of its 7 need a hand-written objective). Registration uses MLQuestSystem.Register rather than Data/MLQuests.cfg, which apply-patches.sh cannot carry; that API has zero upstream callers, so a test guards it. Found a gap in the S4 route: no BaseCreature can be constructed in a test without the npc-speeds.json table (Q-026). Answers Q-023. See notes/s5-quest-spike.md. |
| `S6` | SAAbsorptionAttributes | done | SAAbsorptionAttributes built, gated build green at 20 tests, A5 CLOSED: EaterCold = 2 restored on all eight Aloron pieces and a completed set demonstrably eats cold damage. 1,031 lines against the ~1,120 budget: SAAbsorptionAttributes.cs 342, the damage-eater slice of SAPropEffects.cs 402 (of ServUO's 768 - the other eight PropertyEffect kinds are weapon properties for systems this shard lacks), 223 test, 25 patch, 31 BaseSetArmor delta, 8 Aloron lines. ONE UOContent patch and NO core patch, so cheaper on a bump than S1. S3's three dependency claims all verified in ServUO and two are stronger than stated: Enhancement's only absorption writer (EnhancementTimer) is never constructed anywhere in ServUO, and SkillMasterySpell's absorption switch has one arm, CastingFocus, which is not an eater - both terms are zero in ServUO too, not merely here. THE EATER DOES NOT REDUCE DAMAGE: it schedules a heal three seconds later for a share of the hit, and gap-register A5 plus s3-decline-costs section 6 both describe it wrong (Q-027). '57 unblocked' is a reference count: 8 finished, 5 carrier-ready, 31 need one of four small carrier classes, 13 were blocked by other subsystems all along (Q-028). The four carriers are deliberately NOT built - that is more than the shape the brief allowed, and it is S1 section 8's boundary exactly; build each with the content batch that needs it. Patch proved to fail when skipped. Needed no BaseCreature, so D1/Q-026 did not bite. See notes/s6-absorption.md. |
| `S8` | Finish the test route | done | Both S4-route defects fixed in the route, not in consumers. (1) UOContentFixture-npc-speeds.patch adds the NPCSpeeds.Configure call the upstream test fixture omits, so any test constructs a stock or ported BaseCreature with no scaffolding - Q-026, whose STATED CAUSE was wrong: the data file was always in the test output directory, nothing ever called Configure (Q-031). (2) server/tests/Route/ShardTestClock.cs is the one correct way to advance time; Timer.Slice turns the wheel without moving Core.Now, which made S6's first eater test measure regeneration - Q-029. apply-patches.sh now fails the build for a test that drives the wheel or registers speeds by hand, and S5's and S6's workarounds are deleted rather than relocated. Five negative proofs run and reverted. 27 tests green through build.sh; Server.dll, ModernUO.dll and UOContent.dll are byte-identical to the S6 image, so the shipped server is provably unchanged. |
| `S7` | Services/PointsSystems | todo | 12 files, 2,857 lines, unblocks 55. Hard dependency of both Vice vs Virtue and City Loyalty. Costed and available, not scheduled. |
| `C2` | Revamped Dungeons | todo | 255 files. Unblocked: F2 added subdirectory mirroring. One chat per dungeon: Despise 4, Shame 11, Wrong 26, Covetous 29, Exodus 38, Blackthorn 147. |
| `C3` | High Seas, cheap half | todo | ~78 files. Fishing, rare fish, sea creatures, food. Skip anything touching BaseGalleon or cannons. |
| `C4` | Creatures and NPCs | todo | ~360 files. Only 275 (60%) are clean on both dependency checks: 89 (19%) reference a type ModernUO lacks, 132 (29%) call a BaseCreature method it does not have. Batches of ~20, drawn from the clean 60%, about an hour each per the P2 measurement. See notes/cc2-timed-port.md. |
| `C5` | Decoration, housing, crafting | todo | Addons, Decorative, New Magincia, Items/Resource, BulkOrders. 0% dependency. |
| `C6` | Artifacts and equipment | todo | ~473 files, 1-2%. Selectively: pieces anchoring a dungeon or quest. |
| `C7` | High Seas naval - written proposal only | todo | ~54 files. Means extending BaseBoat. Do not start; Chase decides from the proposal. |

_Detail and acceptance criteria in `docs/tasks.md`. Status lives in `tools/progress-state.json`._

### Needs reconciling on a `MODERNUO_COMMIT` bump: 15 patches, 5 replacements

What a MODERNUO_COMMIT bump must reconcile. Patches fail LOUDLY - apply-patches.sh stops the build. Full-file replacements fail SILENTLY: they always apply, and quietly discard whatever upstream changed in that file.

| Upstream file | Patch | Diff | Risk | Breaks when |
|---|---|---|---|---|
| `Projects/Server/Mobiles/Mobile.cs` | Mobile-set-item-resistance-hook | +18/-5 | **high** | any upstream change to ComputeResistances or the resistance pipeline |
| `Projects/UOContent/Misc/AOS.cs` | AOS-damage-eater-hook | +15/-0 | **high** | any change to AOS.Damage's signature or damage ordering |
| `Projects/UOContent/Misc/AOS.cs` | AOS-set-attribute-aggregation | +11/-0 | **high** | changes to attribute aggregation; three patches share this file |
| `Projects/UOContent/Misc/AOS.cs` | AOS-pet-mimic-attribute-aggregation | +8/-0 | **high** | same file as the two above; upstream just changed OPL hashing nearby |
| `Projects/UOContent/Mobiles/PlayerMobile.cs` | PlayerMobile-fountain-luck-bonus | +1/-1 | **medium** | any change to how loot reads Mobile.Luck. Pinned by a test |
| `Projects/UOContent/Mobiles/PlayerMobile.cs` | PlayerMobile-individual-stat-cap | +3/-3 | **medium** | stat cap handling; second patch on this file |
| `Projects/UOContent/Items/Armor/BaseArmor.cs` | BaseArmor-set-self-repair | +4/-1 | **medium** | changes to self-repair or durability |
| `Projects/UOContent/Items/Weapons/BaseWeapon.cs` | BaseWeapon-talisman-durability | +5/-0 | **medium** | durability handling |
| `Projects/UOContent/Items/Skill Items/Misc/Bandage.cs` | Bandage-pet-mimic-targeting | +9/-0 | **low** | bandage targeting rewrite |
| `Projects/UOContent/Engines/Craft/Core/CraftGumpItem.cs` | CraftGumpItem-MakeX | +15/-1 | **low** | craft gump layout. Label still renders invisible (known) |
| `Projects/UOContent/Engines/Craft/Core/CraftGump.cs` | CraftGump-MakeXClear | +4/-0 | **low** | craft gump layout |
| `Projects/UOContent/Mobiles/Healers/Healer.cs` | Healer-resurrection-policy | +2/-2 | **low** | healer logic |
| `Projects/UOContent/Mobiles/Vendors/NPC/Guildmasters/HealerGuildmaster.cs` | HealerGuildmaster-resurrection | +27/-0 | **low** | guildmaster logic |
| `Projects/UOContent/Engines/Bulk Orders/SmallSmithBOD.cs` | SmallSmithBOD-PostValorite | +33/-0 | **low** | BOD generation |
| `Projects/UOContent.Tests/Fixtures/UOContentFixture.cs` | UOContentFixture-npc-speeds | +13/-0 | **low** | any upstream edit to UOContentFixture's constructor near SkillsInfo.Configure, or a change to what NPCSpeeds.Configure does; either way every creature test fails loudly in the constructor |

**5 full-file replacements fail silently on a bump** and must be diffed by hand: `BaseGuildmaster.cs`, `BulkMaterialType.cs`, `JacobsPickaxe.cs`, `LargeSmithBOD.cs`, `Mining.cs`.

**Deliberately declined:**

- **Eodon: the Valley of One quest line - REOPENED, and a poor first batch** — Declined by CC3 because ModernUO 'ships a different quest engine'. S3 found ModernUO already ships Engines/ML Quests: 109 files, 240 quests, 205 of ServUO's 408 present by name. S5 then translated one quest end to end and CONFIRMED the objective mapping holds, so this decline is reversed and these are content work. Q-023 answered. But S5 also read all seven: none uses two objective types and THREE of the seven (EmptyNest, TheGreatVolcano, PrideOfTheAmbush) use a hand-written InternalObjective with no counterpart on either side of the mapping, against 19% bespoke across the 203. Reopened, but do not start the quest work here - pick from the 164 single-standard-objective quests instead. See notes/s5-quest-spike.md sections 1 and 8.
- **Eodon: MoonstonePowerGenerator** — CC3. It is Myrmidex Invasion content, not Eodon. It lives inside Services/Expansions/Time Of Legends/Myrmidex Invasion/, spawns Zipactriotl (the Myrmidex boss) and IgnisFatalis, subclasses DamageableItem (absent from ModernUO), and is referenced only by Myrmidex Invasion/System.cs and the MyrmidexThreat quest. It reached the CC3 list because the keyword moonstone matched and nobody opened the file.
- **S3 costed menu - declines upheld with their ratios recorded** — Measured 2026-09-07, notes/s3-decline-costs.md. Skill Masteries (45 files/8,542 lines, unblocks 14, patches 35 upstream files - fails the layering test). Vice vs Virtue (57/9,613, unblocks 5, patches 21). Exploring the Deep (70/10,292, unblocks 2 - structurally the safest build here and the worst ratio). Shadowguard (14/11,222, unblocks 8). City Loyalty (28/8,177, unblocks 15 - decline on ratio, not structure; revisit with Town Cryer). Instanced Peerless (13/1,543, unblocks 2, and BasePeerless and PeerlessAltar are both absent from ModernUO, so there is no base to instance - cost Services/Peerless first). ServUO's ML quest framework (22 files/6,269 lines, not the 21/5,625 the brief stated) - declined because ModernUO already ships the same OSI system. NOT declined and recommended instead: SAAbsorptionAttributes, the TribeType transformation, and a one-quest spike onto ModernUO's ML quest engine. Vendor Searching (4/2,545) is a player feature, not content; the unblock ratio is the wrong test and it is Chase's call.
- **ServUO ML quest framework - decline REAFFIRMED by S5** — S5 translated one quest end to end and the objective mapping holds for 4 of 5 types, two of them pinned by tests. Porting ServUO's 22-file, 6,269-line framework would put a second engine in the tree to do a job the engine we already have does correctly. The decline was always on two-engines-for-one-job; it now rests on measurement rather than on principle alone. What is NOT declined: the 164 of 203 missing quests that use a single standard objective type. The 39 that hand-write a BaseObjective subclass (25 InternalObjective, 3 CollectionsObtain, 2 QuestionAndAnswer, ~9 one-offs) are per-quest work, not a framework port, and are the thing to cost before the next quest batch.

Counted from the trees: 198 customization files, 20 patch files.
Shard status: running on ModernUO.
<!-- PROGRESS:END -->

## Expansion coverage

<!-- EXPANSION:START -->
### Content by expansion

**3,103 of 6,144 ServUO files present** (51%), of which **64 ported by us**.

```
Pre-AoS (T2A/UOR/LBR)     ███████████░░░░░░░░░  2276/4294    53%   +53
Age of Shadows            █████████████░░░░░░░   201/309     65%
Samurai Empire            ███████████████░░░░░    88/115     76%   +1
Mondain's Legacy          ██████████░░░░░░░░░░   241/471     51%
Stygian Abyss (Ter Mur)   ██████░░░░░░░░░░░░░░   127/444     29%   +2
High Seas                 ██████░░░░░░░░░░░░░░    96/334     29%
Time of Legends (Eodon)   ████████░░░░░░░░░░░░    60/157     38%   +7
Endless Journey           ██████████████░░░░░░    14/20      70%   +1
TOTAL                     ██████████░░░░░░░░░░  3103/6144    51%   +64
```

_Filename-stem matching: a proxy for presence, not behaviour. Unclassified files fall into Pre-AoS, inflating it. Directional, not a completion percentage._
<!-- EXPANSION:END -->
