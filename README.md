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
**Direction: staying on ModernUO.** ServUO content is pulled in piece by piece.

Judgment reviewed 2026-10-13. Shard version 2026.10.14.13. Golem on, 5 queued, latest done P107. Play tests: 196 open, 2 failed, 18 passed.

## Port list: 1 of 16 systems in. 283 of 983 files (29%).

**Next to land: Bulk orders, all crafts.** A faithful port comes first, our feature customizations after it; work already started or already requested is still finished (Chase, 2026-10-13).

```
Port list ██████░░░░░░░░░░░░░░░░  283/983   28.8%
Setup     ██████████████████████  7/7     blocking defects resolved
```

| System | Done / files | | Feeds |
|---|---|---|---|
| Bulk orders, all crafts | 0 / 28 | `░░░░░░░░░░░░` | F-18, F-20, F-25, F-37 |
| Treasure maps revamp | 0 / 2 | `░░░░░░░░░░░░` | F-20; gate: train without a wall |
| Monster stealing | 0 / 14 | `░░░░░░░░░░░░` | gate: train without a wall |
| Despise and Shame (revamped) (in) | 15 / 15 | `████████████` | gate: somewhere to go |
| Blackthorn Dungeon (revamped) | 3 / 147 | `█░░░░░░░░░░░` | gate: somewhere to go; F-24, F-32 |
| Covetous Void Spawn | 2 / 29 | `█░░░░░░░░░░░` | gate: somewhere to go; F-24, F-32 |
| Wrong (revamped) | 2 / 26 | `█░░░░░░░░░░░` | gate: somewhere to go; F-24, F-32 |
| The Exodus Encounter | 1 / 38 | `█░░░░░░░░░░░` | gate: somewhere to go; F-40 boss boxes |
| Underworld (Stygian Abyss) + mini champions | 3 / 27 | `█░░░░░░░░░░░` | gate: somewhere to go; F-24 culling |
| Creatures: Mobiles/Normal remainder, bosses, Void creatures, AI | 80 / 193 | `█████░░░░░░░` | gate: things to fight; F-24, F-40, F-42 |
| Pet Training (OSI animal training) | 0 / 11 | `░░░░░░░░░░░░` | F-35 evo pets, companions, Animal Lore to 200 |
| Eodon (Time of Legends) remainder, no Myrmidex or Shadowguard | 6 / 19 | `████░░░░░░░░` | gate: somewhere to go, things to fight |
| High Seas, fishing half | 4 / 59 | `█░░░░░░░░░░░` | F-20 Fishing; Maritime Brotherhood |
| Crafting gaps: basket weaving, armor refinement, craft helpers, raised gardens | 0 / 33 | `░░░░░░░░░░░░` | F-43 recipe gating; Herbalism |
| Food, drink and potions | 0 / 44 | `░░░░░░░░░░░░` | F-43; Alembic, Cooking designs |
| Base items: resources, equipment, containers, tools, functional | 167 / 298 | `███████░░░░░` | everything above |

Not counted: ride 361 files (11 in); reward 717 files (288 in); source 178 files (3 in); later 307 files (12 in); drop 304 files (5 in). Every candidate belongs to a system. _Counted by filename stem (not behavior) against `server/customizations`; the list itself is `tools/port-list.json`, kept by hand._

### Playable? **Not yet: 2 of 11 gates met.** The next one to fall is *A new character can train without hitting a wall*.

'Playable' is a judgement, so it is written down as gates rather than felt. Each one is a thing a player would actually hit, and cites what it rests on. Update one with python tools/judge.py gate.

| | Gate | Where it stands |
|---|---|---|
| **yes** | The shard runs and holds a world | The test shard runs sl-modernuo:latest (built 2026-10-10, version 2026.10.10) and saves and reloads; 1,133 of 1,133 tests pass at P82. There is no live shard: the old live container stops at a deserialize error until the fresh-world wipe. _Sources: notes/cc-P82-artificers-imbuing.md section 7; notes/passdown-overseer-2026-10-05.md; docker ps and images, 2026-10-13._ _Confirmed 2026-10-13._ |
| **yes** | The player package installs on a clean PC | Passed on a clean Windows Sandbox (T-049), off the home network (T-020) and through the updater (T-021). The newer 2026.10.13.0118 zip passed gates 1 to 6 but is not uploaded; D61's sandbox graphics fallback was not rerun. _Sources: testing/play-tests.json T-049, T-020, T-021; notes/passdown-overseer-2026-10-05.md; notes/cc-P81-paperdoll-sos.md; docs/bug-list.md D61._ _Confirmed 2026-10-13._ |
| no | A new character can train without hitting a wall | Largely built, not seen in a client. The old 5x wall moved: the guilds are now the starter path, and P66 (hook G, 17 skills), P67 (craft ceilings) and P71 (effects scaled to 200) gave the 41 stalled skills a path to 200. Still open: casting schools above about 120, and the content skills (Alchemy, Cooking, Tailoring, Fishing, Inscription) need designs. ClusterFSkillGain still runs 3 attempts and a 5x gain amount. _Sources: notes/cc-P54-f12-xp-and-gain-paths.md; notes/cc-P66-clamps-and-hook-g.md; notes/cc-P67-craft-ceilings.md; notes/cc-P71-high-skill-effect-scaling.md; notes/f12-decisions-2026-10-05.md items 8b and 11; ClusterFSkillGain.cs:36-37._ _Confirmed 2026-10-13._ |
| no | A new character's first hour | P80 built the New Haven tutorial framework (37 stations), but every trial but the loop vision is a TODO and 8 decisions wait on Chase. P79 loot boxes and fanfare are built. Neither is deployed. T-040 failed: nothing points a player to the League. _Sources: notes/cc-P80-new-player-tutorial.md; notes/cc-P79-loot-boxes-fanfare.md; testing/play-tests.json T-040 (D41)._ _Confirmed 2026-10-13._ |
| no | Levels and loops work end to end | F-12 is not built: ClusterFLoops.CompleteLoop is only a hook. The research is done (P54 XP curve and gain paths, P72 level items) and Chase answered its questions; no F-12 play tests exist. _Sources: ShatteredLegacy server/customizations/Tutorial/ClusterFLoops.cs:1; notes/cc-P54-f12-xp-and-gain-paths.md; notes/cc-P72-level-items-research.md; notes/f12-decisions-2026-10-05.md._ _Confirmed 2026-10-13._ |
| no | What is built is seen in a client, not only compiled | Chase passed in-game checks for P46 to P57 on 10-04/05. P65 to P84 are committed but not on the deployed image, so none of them has been in a client; their play tests are open. _Sources: notes/passdown-overseer-2026-10-05.md; testing/play-tests.json; notes/cc-P78 to cc-P80: latest unchanged 8863156884f8._ _Confirmed 2026-10-13._ |
| no | Somewhere to go | Despise is client-verified (09-20, fixes D52 to D54 passed 10-03). Shame is ported but never seen in a client (T-007 open). The Burrows (P36) checks T-055 and T-056 are open. Extra facets (P76) are research only. _Sources: docs/client-check-backlog.md; notes/cc4-shame.md; notes/cc-P36-dungeon-build-1.md; notes/cc-P76-extra-facets.md; docs/bug-list.md D52-D54._ _Confirmed 2026-10-13._ |
| no | Things to fight | No creature batch since CC6 batch 8 (2026-09-21); 19 names the spawn data places still spawn nothing. Only P50 (chest mimic) and P65 (evo pets) added creatures since. The old 27 of 137 figure was not recounted. _Sources: tools/spawn-orphans.txt (2026-09-21); notes/cc-P50-chest-mimic-monster.md; notes/cc-P65-evo-pets-framework.md._ _Confirmed 2026-10-13._ |
| no | Set mechanics actually fire | Unchanged since 09-19: armor sets and absorption work; Bestial rage, Epiphany burst, the sculpture's luck and set self-repair are ported but inert until the set-mechanic hooks row is built. _Sources: docs/gap-register.md section A; docs/patch-backlog.md P3; a grep of server/customizations, 2026-10-13._ _Confirmed 2026-10-13._ |
| no | No live gap a player would call a bug | docs/bug-list.md section 1 has 60 rows, but 34 say fixed or built and at least 5 more were fixed later: the list itself needs a pass. Open ones a player would hit: D83-D85 (built in P61, awaiting a client), D88 (shard woods have no resource info), D32/D33 (recipes and items no player can reach), D14 (Fountain of Fortune, until Chase walks it). _Sources: docs/bug-list.md; docs/gap-register.md section A._ _Confirmed 2026-10-13._ |
| no | The fresh-world wipe is ready | There is no single fresh-world plan; the items are scattered: D34 must be fixed first, D50 (live stop timeout) takes on recreate, T-006 and T-010 run on the new world, the tutorial would greet old characters until then, F-4 (one character per account) starts with it. P73's test-account wipe is built and proven on a copy, not deployed, and refuses live. _Sources: docs/bug-list.md D34, D50; docs/client-test-queue.md T-006, T-010; notes/cc-P80-new-player-tutorial.md; docs/feature-queue.md F-4; notes/cc-P73-test-account-wipe.md._ _Confirmed 2026-10-13._ |

| Setup defect | Resolved |
|---|---|
| CraftContext members (RepeatCount, RepeatItem, RepeatTypeRes) recovered | yes |
| ResourceInfo extended wood enum members (8) recovered | yes |
| OutridersGuildmaster recovered | yes |
| server/customizations compiles standalone | yes |
| apply-patches.sh fails on failed patch | yes |
| stale server/customizations/migrations removed | yes |
| RegenRates routing made explicit | yes |

**Patches:** 16 total, **0 currently failing to apply**, 8 triaged, 3 found obsolete. `apply-patches.sh` fails the build on a failed patch, so a green build means every patch applied.

### Every ServUO file ModernUO lacks, by area (not a target): 551 of 2,045 (26.9%)

```
TOTAL                          █████░░░░░░░░░░░░░  551/2045   26.9%

Items/Artifacts                ████████████████░░  283/325    87.1%
Items/Equipment                ███████████████░░░  124/148    83.8%
Mobiles/Normal                 ████████░░░░░░░░░░   58/138    42.0%
Items/Resource                 ███████████░░░░░░░   36/61     59.0%
Services/Revamped Dungeons     ██░░░░░░░░░░░░░░░░   15/150    10.0%
Services/Expansions            █░░░░░░░░░░░░░░░░░   12/175     6.9%
Items/Quest                    ██░░░░░░░░░░░░░░░░    7/78      9.0%
Items/Containers               ██░░░░░░░░░░░░░░░░    4/31     12.9%
Items/Functional               █░░░░░░░░░░░░░░░░░    3/49      6.1%
Items/Decorative               █░░░░░░░░░░░░░░░░░    2/88      2.3%
Quests                         █░░░░░░░░░░░░░░░░░    2/84      2.4%
Services/CleanUpBritannia      █░░░░░░░░░░░░░░░░░    2/52      3.8%
Services/New Magincia          █░░░░░░░░░░░░░░░░░    2/40      5.0%
Items/Addons                   █░░░░░░░░░░░░░░░░░    1/169     0.6%
Mobiles/NPCs                   ░░░░░░░░░░░░░░░░░░    0/222     0.0%
Services/XmlSpawner            ░░░░░░░░░░░░░░░░░░    0/97      0.0%
Items/Consumables              ░░░░░░░░░░░░░░░░░░    0/59      0.0%
Items/StoreBought              ░░░░░░░░░░░░░░░░░░    0/51      0.0%
Services/BulkOrders            ░░░░░░░░░░░░░░░░░░    0/28      0.0%
```

_Counted by matching ServUO file stems (excluding those stock ModernUO already has) against `server/customizations`. Auto-counted, never hand-edited._

**Ported systems logged: 48**

| Content | Task | Notes |
|---|---|---|
| CC9 batch 5: Swiftflight, the in-row remainder, the whole plain bucket (136 files, 240 types) | CC9 | Closes the 320 and 81 buckets. Swiftflight is Bow, ISetItem with BaseSetWeapon's fields inlined and no carrier (Q-041), proven by the first content-level set test (real Feathernock + Swiftflight complete the Marksman set through the interface alone; round-trip of the set fields on a Bow subclass). 116 files generated from ServUO values by a refusing generator, 19 hand-written; every override and constructor value re-diffed (1,085 + 821, 0 findings, diff proved red). One base needs a carrier (LeatherTalons -> BaseSetClothing, for UnicornManeWovenTalons' absorption). Three more mechanics ported whole and inert pending engine hooks, the D-14 shape: Epiphany burst (12 Villainous pieces), TenthAnniversarySculpture luck, FirstAidBelt healing bonus (Q-043). Three files found already in ModernUO under other names and not ported (gargish cloth arms, HMS Cape model, mystic book). Three build cycles (two single-error failures: a Container.CheckStack that ModernUO gates through CheckHold, a third SoulCharge, a missing using), then green in 4.5 min, 44 tests. 237/237 reflected; headless fresh save and reload clean. The brief's 120/29 were 107/30 when counted from the trees. Nothing seen in a client; spot check now 381 files. |
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
| Gargoyle wearables, row share (9 files, 11 types) | CC9 | GargishGlasses, GargishPlateChest, GargishPlateLegs, GargishEarrings, GargishNecklace (+GargishAmulet, GargishStoneAmulet), GargishGnarledStaff, GargishKatana, GargishDagger, LargeStoneShield. ServUO's 'Race RequiredRace => Race.Gargoyle' is ModernUO's 'int RequiredRaces => Race.AllowGargoylesOnly' on armour/weapons/shields (Item.cs:2110); CanBeWornByGargoyles has zero readers and is dropped. S9's other three gargoyle files in this row (GargishClothArmor.cs, GargishLeatherArms, GargishStoneChest) were NOT ported: ModernUO already ships them as Gargish<Material><Slot>Type1/Type2 with the same item IDs, found by an item-ID cross-check, not by name. |
| Greymist (Acolyte) armour set (4 files) | CC9 | ServUO derives these from stock Leather* and reads set state off BaseArmor; here they derive from S1's BaseSetArmor and reproduce the stock parent's members, the TigerPelt/Aloron shape. This is the transformation every one of the row's 83 set-armour files needs and S9's name scan could not see. Set bonus firing is NOT verified headlessly; batched for the client spot check. |
| BaseCostume | CC9 | Shield-slot mask that body-mods the wearer; carrier for the 34 costumes in the in-row bucket, all now plain ports. Two persisted ints (CostumeBody, CostumeHue) at version 0; ServUO's three save versions collapse. Deviation D-5: ServUO knocks the costume off from AOS.Damage (AOS.cs:417); ModernUO has no call site, so a masked player keeps the mask through combat. One line added to the existing AOS-damage-eater-hook.patch would restore it. |
| CC9 batch 2: 33 costumes + 7 unblocked artifacts (40 files, 41 types) | CC9 | The 33 costumes are one template on BaseCostume (body, one hue, creature name, cliloc or default name) and were generated from the ServUO values by a script that refuses any file whose constructor or overrides differ from the template; it refused none. CastOffZombieSkin, CuffsOfTheArchmage (2 types), PillarOfStrength, BreastplateOfTheBerserker, GiantSteps, Glasses, NightEyes hand-written; three of them derive from ModernUO's own Gargish*Type1/Type2 classes rather than a ported parent. Green first cycle (95 s), 41/41 reflected, headless save/reload clean. Reading the 19 in-row artifacts batch 1 supposedly unblocked found 6 more absorption users and 5 set pieces on gargish jewellery, so only 8 were plain - S9's in-row bucket checked one member per file. |
| CC9 batch 1: artifacts and equipment (31 files, 34 types) | CC9 | 2,604 ServUO lines in, 1,324 out. Category-spread sample chosen to test S9's 'drops straight in' claim: 20 of 34 types needed only the standard conversion, 8 would not have compiled mechanically (four set pieces re-parented, fishing-pole attributes, BattleLust, two non-virtual overrides on earrings/necklace, IRepairable), 3 must not be ported at all (already in ModernUO). Real persisted state exercised on GobletOfCelebration (SerializableProperty + DeltaDateTime + AfterDeserialization timer rebuild), AmuletOfRighteousness (IUsesRemaining) and BaseCostume. Deviations D-3 AxeOfAbandon BattleLust, D-4 XenrrFishingPole SpellChanneling/CastSpeed (ModernUO's FishingPole has no attribute block and AosAttributes.GetValue aggregates only the seven equipment bases), D-5 costume damage hook. Gated build 86 s; 33/33 types reflected; headless save and reload clean. |
| The carrier family: BaseSetWeapon, BaseSetJewel, BaseSetClothing, BaseSetQuiver, BaseSetShield (5 files) | S10 | Subsystem, not content: the set state ServUO puts on each base class, on an additive intermediate class of ours instead (the S1 decision, applied four more times). 1,426 lines, zero patches, zero migrations, 15 tests, every gate watched fail. Field layout identical to BaseSetArmor on every carrier (0-9, then SetSelfRepair 10 and absorption 11 where the ServUO base has them; jewel has absorption at 10; quiver has neither). SetSelfRepair inert on weapon/clothing/shield (Q-038). The four ported gargish armour-class bases were re-parented onto BaseSetArmor in the same commit, before any instance reached a save. Unblocks CC9 batch 4 (13 set pieces + 9 non-armour absorption users + 5 gargish-jewellery set pieces) and CC4's ReforgedSuffix route C. |
| CC9 batch 3: the plain remainder (49 files, 49 types) | CC9 | 21 weapons, 11 jewellery, 17 armour and shields; 4,636 ServUO lines in, 1,740 out. Pre-flighted with the section-3 method before any build: every override checked against a pinned ModernUO virtual, every attribute member against the Aos* enums, item IDs cross-checked, and every ServUO descendant of all 49 walked transitively for set or absorption state. Nine bases got a carrier parent at port time because a descendant needs it (GargishPlateArms, GargishPlateKilt, the five DragonTurtleHide pieces on BaseSetArmor; GargishKiteShield on BaseSetShield; GargishBattleAxe on BaseSetWeapon, the ninth, found because GargishPincer assigns SetSkillBonuses, a token the AGENTS.md grep does not list - Q-040). The other 40 are on stock bases per docs/tasks.md. RandomWand is a static helper, not an item. Every override value re-diffed mechanically against ServUO after writing: 524 compared, 0 mismatches. Deviations D-10 (GargishWarHammer flip typo 0x481 -> 0x48C1), D-11 (EvilOrcHelm's two zero-reader virtuals), D-12 (OrcishBow one durability line, not two), D-13 (StaffRing IsPlayer; not OSI content). Gated build green first cycle, 101 s, 42 tests; 49/49 reflected; headless fresh save and reload clean. |
| CC9 batch 4: the one re-parent, the 41 carrier-blocked, the set-armour bucket (125 files, 127 types; 3 edited) | CC9 | GargishDagger moved from BaseKnife to BaseSetWeapon (Q-040: StoneDragonsTooth needs AbsorptionAttributes), after re-verifying no instance in any save by reading the type tables of the live save (2026-07-06, 1,468 types, no Gargish* at all), the three Backups snapshots and the newest daily and hourly Archives (decompressed), not by date alone. The 41 carrier-blocked: 40 ported, Swiftflight declined (Bow sits on BaseRanged, no carrier can sit above it; Q-041). Two talismans ported on stock BaseTalisman with the eater dropped, which is behaviour-identical: ServUO never aggregates a talisman's absorption (RunicReforging.GetSAAbsorptionAttributes). The set-armour bucket counts 85, not 79: 79 set pieces plus the 6 Phoenix suit files that sit under Sets/ with no SetID and stay on stock parents. All 85 generated from ServUO values plus a dump of the pinned stock parent's members ([Flippable] copied because ModernUO reads it inherit:false; IArcaneEquip dropped on 6 gloves per D-7). Two corrections found by reading the parents: batch 3's GargishBattleAxe had lost BaseAxe (Slash1H, sword sounds, no harvesting) and S10's BaseSetWeapon skipped BaseMeleeWeapon's AbsorbDamage; both fixed, both save-neutral today. Bestial pieces ported with the berserk helper inert (its AOS.Damage/heal hooks do not exist here; Q-042). Deviations D-14..D-19. Value diff over 126 files: 0 findings, proved red with three injected faults. One failed build cycle (28 s, one inlined member), then green in 99 s with 42 tests; 130/130 reflected; headless fresh save and reload clean. 10,062 ServUO lines in, 6,363 out. See notes/cc9-artifacts.md section 14. |
| CC4 Despise: the Revamped Despise dungeon (12 ServUO files + XmlSpawner XML -> 14 files, 4,684 lines) | CC4 | Regions are ServUO dynamic BaseRegions re-created by the controller; ModernUO's Region maps member for member except CheckTravel (now on BaseRegion with an out message), the absent EventSink.OnEnterRegion (DespiseRegion.OnExit instead), and priority: every pinned region is Dynamic so the tie with regions.json's Despise dungeon went to list order - priority 51. XmlSpawner XML became a 47-row table plus DespiseSpawner (PowerMin/PowerMax) applied in OnAfterSpawn, because ModernUO entries take fixed parameters. Headless on the real map: 227 creatures generated in bounds (capacity 227 of 229 requested: two XML rows exceed their entries), power 1-5 upper / 4-8 lower, 15+15 army spawners found, save/reload identical. 48 tests green, auto-stable gate proved red. Deviations (note-local D-29..D-36 in notes/cc4-despise.md): PutridHeart inert, MysteriousWisp not placed, Town Cryer hooks dropped, Silenii/Phantom Discordance dropped, ForceNotoriety absent, Container orb hook absent, lower level 4-8 vs a broken 2-arg XML, FightMode.Good/Evil -> Closest (behaviour-identical on pub57). |
| CC6 batch 1: twenty creatures the stock spawn data places and could not spawn (20 files + GoblinOppositionGroup, 1 test) | CC6 | Selection rule: pinned ModernUO's Distribution/Data/Spawns names 109 types no loaded assembly declares (BaseSpawner marks them InvalidType and spawns nothing); the twenty are the low-to-mid-level Mobiles/Normal part that is clean to port (Underworld goblins, Abyss enslaved goblins, Ter Mur spiders/skree/undead guardians, Old Haven spellbinders). Headless on the real map: the probe imported the four stock files (168 spawners, 0 failures), all twenty spawned by their stock spawners (127 live), save and reload identical; 60 tests green incl. 6 new (values, every stock entry now resolves and 89 names remain, gray/green goblin enmity, trapdoor stealth walk, tangling roots entangle+acid, the rest's shape). TribeType -> a fourth OppositionGroup, additive; CanStealth -> ServUO's BaseCreature.OnMove branch inlined in TrapdoorSpider. Deviations D-44 GreenGoblinScout on AI_Melee (no OrcScout AI), D-45 Spellbinder on AI_Mage (no Spellbinder AI), Skree on AI_Mage (D-41's shape), D-46 ShameWall constructor sets Visible (Q-046). Route extended: the test fixture never wired the skill-check handlers, so every CheckSkill failed in the test host; SkillCheck.Initialize added to the S8 fixture patch, proved red first. Nothing seen in a client; Q-048 asks whether the live world's Ter Mur spawners exist so these start on deploy. |
| CC4 Shame: the Revamped Shame dungeon on both facets (19 ServUO files + XmlSpawner XML -> 20 files, 3,772 lines) | CC4 | The brief's 11 files are 19 plus the XML: 116 of the XML's 194 rows spawn TreasureLevel1-4 (Nerun's chest pack, not in ModernUO, ported levels 1-4; Q-047), and the cave troll's four High Seas powder ingredients and the vortex's VoidCore are leaf items ported at ServUO's paths. No region layer: Shame constructs none, the creatures test regions.json's static Shame DungeonRegion by name on both facets, so Despise's priority trap does not arise. XmlSpawner XML became a 194-row table on plain Spawners (no constructor arguments in this file; Q-044's shape does not occur), 97 per facet and identical. Headless on the real map: 384 of 386 requested (two rows exceed their entries) all inside their rectangles and inside the Shame region on both facets, 58 locked chests with loot per facet, 6 altars / 6 walls / 6 trolls / 22 wall teleporters, save/reload identical, 54 tests green, ClayGolem gate proved red, no patch. Deviations (note-local D-37..D-43 in notes/cc4-shame.md): crystal points inert behind a seam for S7 so the altars answer 'not yet worthy' and the guardians are GM-only until then; chest loot unreforged and no refinement roll; StickySkin/ColossalRage/SearingWounds dropped; LifeLeech is DrainLifeAttack; CrazedMage on AI_Mage; TreasureMapChance absent; a timed-out challenge now frees the altar (ServUO leaves it stuck). ServUO's wall teleporters reproduced as read - inert until the first troll dies, then active whenever the wall stands (Q-046). |

### Task list (1 of 13 done)

```
Tasks          ██░░░░░░░░░░░░░░░░░░░░  1/13   Open work the overseer tracks
```

| | Task | Status | Notes | Confirmed |
|---|---|---|---|---|
| `DEPLOY` | Deploy P65-P84 to the test shard and check them in a client | todo | The deployed image is 2026.10.10 (8863156884f8); VERSION is 2026.10.13.6. Console: Test shard > Deploy built image, then the play-test page. | 2026-10-13 |
| `TUTORIAL` | New Haven tutorial trials | todo | P80 framework built; every trial but the loop vision is a TODO; 8 decisions for Chase (cc-P80 notes). | 2026-10-13 |
| `WIPE` | Fresh-world wipe plan | todo | No single plan document; gather D34, D50, T-006, T-010, F-4 and the tutorial's greeting into one. | 2026-10-13 |
| `BUGS` | Bug list pass | todo | 60 rows in section 1, 34 of them say fixed or built; at least D49, D56-D58 and D66 were fixed later. Close or move them. | 2026-10-13 |
| `P83-DEPLOY` | Deploy sl-play-tests (P83) on port 8093 | done | Deployed by Chase 2026-10-13; 8093 answers sl-play-tests, page and /status load. | 2026-10-13 |
| `C2` | Revamped Dungeons | todo | Despise and Shame landed 09-19; no Revamped Dungeons work since. Dungeon work moved to P36 (the Burrows) and F-32 (dungeon chests, P49/P50). | 2026-10-13 |
| `C4` | Creatures and NPCs | todo | Last batch CC6 batch 8 (09-21); 19 spawn names still place nothing (tools/spawn-orphans.txt). | 2026-10-13 |
| `C3` | High Seas, cheap half | todo | Unchanged: costed, no prompt has taken it. | 2026-10-13 |
| `C5` | Decoration, housing, crafting | todo | Unchanged: costed, no prompt has taken it. | 2026-10-13 |
| `C7` | High Seas naval - written proposal only | todo | Do not start; Chase decides from the proposal. | 2026-10-13 |
| `S7` | Services/PointsSystems | todo | Partly superseded: P33 built our own PointsSystem.cs for Clean Up Britannia. ServUO's still blocks Vice vs Virtue and City Loyalty. | 2026-10-13 |
| `F-12` | Levels and loops | todo | After the port (Chase 2026-10-13: faithful port first, customizations after). Research done (P54, P72), decisions in notes/f12-decisions-2026-10-05.md; nothing built beyond the CompleteLoop hook. | 2026-10-13 |
| `F-37` | Commissions move to the League | todo | After the port (Chase 2026-10-13: faithful port first, customizations after). Planned (docs/feature-queue.md F-37), with F-13 (League reward shop); nothing spends Renown yet (cc-P75 A.1). | 2026-10-13 |

_Status lives in `tools/progress-state.json`; `python tools/judge.py` updates one row and its date._

### Queue (Golem on; 58 prompts finished, 1 of them stopped early)

| Prompt | State | When |
|---|---|---|
| P108 retire-live | queued |  |
| P109 haven-print-queue | queued |  |
| P110 haven-mega-dashboard | queued |  |
| P111 tazuo-paperdoll-option | queued |  |
| P112 playtest-bot-icon | queued |  |
| P107 haven-ops-move | done | 2026-10-14 |
| P106 shard-questions | done | 2026-10-14 |
| P105 haven-h1-host-agnostic | done | 2026-10-14 |
| P104 uorespawn-read | done | 2026-10-14 |
| P103 tazuo-client-command | done | 2026-10-14 |
| P102 bot-nightly-archive | done | 2026-10-14 |
| P101 console-websites | done | 2026-10-14 |
| P100 visual-builder | done | 2026-10-14 |
| P99 golem | done | 2026-10-14 |
| P98 building-duplicator | stopped: work complete and verified, but every build is blocked by NuGet audit errors NU1902/NU1903 on System.Security.Cryptography.Pkcs 10.0.0 (needs Chase to choose a fix before the queue goes on) | 2026-10-14 |

### Needs reconciling on a `MODERNUO_COMMIT` bump: 67 patches, 10 replacements

_Counted from `server/patches/` and `apply-patches.sh`. The table below is hand-kept in `progress-state.json` and lists 17 rows; it is a partial risk register, not the count._

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
| `Projects/UOContent/Mobiles/BaseCreature.cs` | BaseCreature-PlayerMobile-can-auto-stable | +4/-0 | **low** | nothing likely; an added virtual next to IsBondable |
| `Projects/UOContent/Mobiles/PlayerMobile.cs` | BaseCreature-PlayerMobile-can-auto-stable | +6/-0 | **low** | a rewrite of AutoStablePets; three patches now share PlayerMobile.cs |

**10 full-file replacements fail silently on a bump** and must be diffed by hand: `BaseGuildmaster.cs`, `BulkMaterialType.cs`, `CharacterCreation.cs`, `HammerOfHephaestus.cs`, `JacobsPickaxe.cs`, `LargeSmithBOD.cs`, `Meditation.cs`, `Mining.cs`, `RegenRates.cs`, `ResourceInfo.cs`.

**Deliberately declined:**

- **Eodon: the Valley of One quest line - REOPENED, and a poor first batch** — Declined by CC3 because ModernUO 'ships a different quest engine'. S3 found ModernUO already ships Engines/ML Quests: 109 files, 240 quests, 205 of ServUO's 408 present by name. S5 then translated one quest end to end and CONFIRMED the objective mapping holds, so this decline is reversed and these are content work. Q-023 answered. But S5 also read all seven: none uses two objective types and THREE of the seven (EmptyNest, TheGreatVolcano, PrideOfTheAmbush) use a hand-written InternalObjective with no counterpart on either side of the mapping, against 19% bespoke across the 203. Reopened, but do not start the quest work here - pick from the 164 single-standard-objective quests instead. See notes/s5-quest-spike.md sections 1 and 8.
- **Eodon: MoonstonePowerGenerator** — CC3. It is Myrmidex Invasion content, not Eodon. It lives inside Services/Expansions/Time Of Legends/Myrmidex Invasion/, spawns Zipactriotl (the Myrmidex boss) and IgnisFatalis, subclasses DamageableItem (absent from ModernUO), and is referenced only by Myrmidex Invasion/System.cs and the MyrmidexThreat quest. It reached the CC3 list because the keyword moonstone matched and nobody opened the file.
- **S3 costed menu - declines upheld with their ratios recorded** — Measured 2026-09-07, notes/s3-decline-costs.md. Skill Masteries (45 files/8,542 lines, unblocks 14, patches 35 upstream files - fails the layering test). Vice vs Virtue (57/9,613, unblocks 5, patches 21). Exploring the Deep (70/10,292, unblocks 2 - structurally the safest build here and the worst ratio). Shadowguard (14/11,222, unblocks 8). City Loyalty (28/8,177, unblocks 15 - decline on ratio, not structure; revisit with Town Cryer). Instanced Peerless (13/1,543, unblocks 2, and BasePeerless and PeerlessAltar are both absent from ModernUO, so there is no base to instance - cost Services/Peerless first). ServUO's ML quest framework (22 files/6,269 lines, not the 21/5,625 the brief stated) - declined because ModernUO already ships the same OSI system. NOT declined and recommended instead: SAAbsorptionAttributes, the TribeType transformation, and a one-quest spike onto ModernUO's ML quest engine. Vendor Searching (4/2,545) is a player feature, not content; the unblock ratio is the wrong test and it is Chase's call.
- **ServUO ML quest framework - decline REAFFIRMED by S5** — S5 translated one quest end to end and the objective mapping holds for 4 of 5 types, two of them pinned by tests. Porting ServUO's 22-file, 6,269-line framework would put a second engine in the tree to do a job the engine we already have does correctly. The decline was always on two-engines-for-one-job; it now rests on measurement rather than on principle alone. What is NOT declined: the 164 of 203 missing quests that use a single standard objective type. The 39 that hand-write a BaseObjective subclass (25 InternalObjective, 3 CollectionsObtain, 2 QuestionAndAnswer, ~9 one-offs) are per-quest work, not a framework port, and are the thing to cost before the next quest batch.

Counted from the trees: 867 customization files, 72 patch files, 773 tests in 145 files.
Shard status: the test shard is the only one running (sl-modernuo:latest, 2026.10.10); there is no live shard until the fresh-world wipe; players get the 2026-10-05 package and TazUO; P65-P84 are committed, not deployed (confirmed 2026-10-13).
<!-- PROGRESS:END -->

## Expansion coverage

<!-- EXPANSION:START -->
### Content by expansion

**3,647 of 6,144 ServUO files present** (59%), of which **608 ported by us**.

```
Pre-AoS (T2A/UOR/LBR)     ████████████░░░░░░░░  2671/4294    62%   +448
Age of Shadows            ███████████████░░░░░   232/309     75%   +31
Samurai Empire            ████████████████░░░░    93/115     81%   +6
Mondain's Legacy          ███████████░░░░░░░░░   250/471     53%   +9
Stygian Abyss (Ter Mur)   █████████░░░░░░░░░░░   205/444     46%   +80
High Seas                 ███████░░░░░░░░░░░░░   110/334     33%   +14
Time of Legends (Eodon)   █████████░░░░░░░░░░░    70/157     45%   +17
Endless Journey           ████████████████░░░░    16/20      80%   +3
TOTAL                     ████████████░░░░░░░░  3647/6144    59%   +608
```

_Filename-stem matching: a proxy for presence, not behaviour. Unclassified files fall into Pre-AoS, inflating it. Directional, not a completion percentage._
<!-- EXPANSION:END -->
