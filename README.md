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

**Patches:** 9 total, **0 currently failing to apply**, 8 triaged, 3 found obsolete. `apply-patches.sh` fails the build on a failed patch, so a green build means every patch applied.

### Content moved over: 11 of 2,045 candidate files (0.5%)

```
TOTAL                          █░░░░░░░░░░░░░░░░░   11/2045    0.5%

Services/Expansions            █░░░░░░░░░░░░░░░░░    6/175     3.4%
Mobiles/Normal                 █░░░░░░░░░░░░░░░░░    3/138     2.2%
Items/Artifacts                █░░░░░░░░░░░░░░░░░    1/325     0.3%
Items/Resource                 █░░░░░░░░░░░░░░░░░    1/61      1.6%
Mobiles/NPCs                   ░░░░░░░░░░░░░░░░░░    0/222     0.0%
Items/Addons                   ░░░░░░░░░░░░░░░░░░    0/169     0.0%
Services/Revamped Dungeons     ░░░░░░░░░░░░░░░░░░    0/150     0.0%
Items/Equipment                ░░░░░░░░░░░░░░░░░░    0/148     0.0%
Services/XmlSpawner            ░░░░░░░░░░░░░░░░░░    0/97      0.0%
Items/Decorative               ░░░░░░░░░░░░░░░░░░    0/88      0.0%
Quests                         ░░░░░░░░░░░░░░░░░░    0/84      0.0%
Items/Quest                    ░░░░░░░░░░░░░░░░░░    0/78      0.0%
Items/Consumables              ░░░░░░░░░░░░░░░░░░    0/59      0.0%
Services/CleanUpBritannia      ░░░░░░░░░░░░░░░░░░    0/52      0.0%
Items/StoreBought              ░░░░░░░░░░░░░░░░░░    0/51      0.0%
Items/Functional               ░░░░░░░░░░░░░░░░░░    0/49      0.0%
Services/New Magincia          ░░░░░░░░░░░░░░░░░░    0/40      0.0%
Items/Containers               ░░░░░░░░░░░░░░░░░░    0/31      0.0%
Services/BulkOrders            ░░░░░░░░░░░░░░░░░░    0/28      0.0%
```

_Counted by matching ServUO file stems (excluding those stock ModernUO already has) against `server/customizations`. Auto-counted, never hand-edited._

**Ported systems logged: 20**

| Content | Task | Notes |
|---|---|---|
| PlagueRat | P1 | P1 reference port. 88 lines to 55. Builds, spawns, survives save/reload. No speed override: SpeedClass Medium, per the Q-008 answer (ModernUO's npc-speeds.json fallback is the standing rule for all ported creatures). |
| GreaterPoisonElemental | P2 | P2 timed port, headless. 123 lines to 80. Compiles clean, server starts, world saves and reloads; type registration proven by reflection over the shipped assembly. Adds PackItem, multi-AddLoot, an OnDeath override, AI_Mage and the two-argument stat overloads over what PlagueRat covered. No speed override, per Q-008. An instance in a saved world is NOT verified: headless has no spawn - batched for a later client spot check. |
| LuckyCoin | P2 | Forced dependency of GreaterPoisonElemental; ModernUO has no LuckyCoin. Ported complete except its OnDoubleClick, which needs FountainOfFortune (an SA addon ModernUO lacks that drags in four more items). Deviation is in the item, not the creature. Q-010. Reused by 12 Mobiles/Normal creatures. |
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

### Task list (8 of 14 done)

```
Tasks          █████████████░░░░░░░░░  8/14   Foundation and the port pipeline
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
| `C1` | Eodon core content (CC3) | done | 17 files ported, built and verified headless; 12 declined. The 22-files/4,000-lines figure was wrong for the third time: the quest line (half the stated line count) is a subsystem port and is declined, the Aloron set rests on a subsystem ModernUO lacks, and MoonstonePowerGenerator is Myrmidex Invasion content. Delivered: 6 dinosaurs, Raptor, RaptorClaw, RaptorTeeth, 6 TOL decoration artifacts, and 2 forced leaf dependencies. Four build cycles, zero failures - the pre-flight dependency check against D:\UO\ModernUO-pinned worked. Time of Legends coverage moved 53/157 to 59/157. Recipe correction: SetWeaponAbility DOES have a faithful ModernUO equivalent, BaseCreature.GetWeaponAbility(), used by 49 stock creatures. See notes/cc3-eodon.md. |
| `C2` | Revamped Dungeons | todo | 255 files. Unblocked: F2 added subdirectory mirroring. One chat per dungeon: Despise 4, Shame 11, Wrong 26, Covetous 29, Exodus 38, Blackthorn 147. |
| `C3` | High Seas, cheap half | todo | ~78 files. Fishing, rare fish, sea creatures, food. Skip anything touching BaseGalleon or cannons. |
| `C4` | Creatures and NPCs | todo | ~360 files. Only 275 (60%) are clean on both dependency checks: 89 (19%) reference a type ModernUO lacks, 132 (29%) call a BaseCreature method it does not have. Batches of ~20, drawn from the clean 60%, about an hour each per the P2 measurement. See notes/cc2-timed-port.md. |
| `C5` | Decoration, housing, crafting | todo | Addons, Decorative, New Magincia, Items/Resource, BulkOrders. 0% dependency. |
| `C6` | Artifacts and equipment | todo | ~473 files, 1-2%. Selectively: pieces anchoring a dungeon or quest. |
| `C7` | High Seas naval - written proposal only | todo | ~54 files. Means extending BaseBoat. Do not start; Chase decides from the proposal. |

_Detail and acceptance criteria in `docs/tasks.md`. Status lives in `tools/progress-state.json`._

**Deliberately declined:**

- **Vice vs Virtue, City Loyalty, Skill Masteries, Exploring the Deep** — 29-100% dependent on subsystems ModernUO lacks entirely. Deferred to workstream 4.
- **Eodon: the eight Aloron armour pieces** — CC3. Rest on the armour set-bonus subsystem, which ModernUO ships zero files for - SetItem, SetAttributes and AbsorptionAttributes are all absent, and BaseArmor has no SetID/Pieces/Set*Bonus/SetSelfRepair. After the resistances the entire item IS set data, so porting without the subsystem leaves a re-hued TigerPeltChest with a label. They also inherit from the TigerPelt set, a further 8 files. Cost to do properly: the set-bonus subsystem, then TigerPelt (8), then Aloron (8).
- **Eodon: the Valley of One quest line** — CC3. Two reasons, either sufficient. (1) It is 3 of 8 files, not 3 of 3: the directory is 3,870 lines and the three named files reference PrideOfTheAmbushQuest and TimeIsOfTheEssenceQuest from Quests.cs, so they do not compile alone. The 2,058-line figure sums a set that does not stand up. (2) It rests on ServUO's Mondain's Legacy quest framework - BaseQuest, BaseQuestItem, QuestHelper, QuestChain, MondainQuester, BaseRewardTitleDeed, all absent from ModernUO - which is 6,269 lines before gumps and persistence. ModernUO ships a DIFFERENT quest engine (MLQuest/MLQuestSystem: static definitions plus per-player context, versus ServUO's per-player instantiated BaseQuest objects). Porting means either two serialized quest engines in one world or a reimplementation. Subsystem port, not a content port.
- **Eodon: MoonstonePowerGenerator** — CC3. It is Myrmidex Invasion content, not Eodon. It lives inside Services/Expansions/Time Of Legends/Myrmidex Invasion/, spawns Zipactriotl (the Myrmidex boss) and IgnisFatalis, subclasses DamageableItem (absent from ModernUO), and is referenced only by Myrmidex Invasion/System.cs and the MyrmidexThreat quest. It reached the CC3 list because the keyword moonstone matched and nobody opened the file.

Counted from the trees: 134 customization files, 14 patch files.
Shard status: running on ModernUO.
<!-- PROGRESS:END -->

## Expansion coverage

<!-- EXPANSION:START -->
### Content by expansion

**3,050 of 6,144 ServUO files present** (50%), of which **11 ported by us**.

```
Pre-AoS (T2A/UOR/LBR)     ██████████░░░░░░░░░░  2228/4294    52%   +5
Age of Shadows            █████████████░░░░░░░   201/309     65%
Samurai Empire            ███████████████░░░░░    87/115     76%
Mondain's Legacy          ██████████░░░░░░░░░░   241/471     51%
Stygian Abyss (Ter Mur)   ██████░░░░░░░░░░░░░░   125/444     28%
High Seas                 ██████░░░░░░░░░░░░░░    96/334     29%
Time of Legends (Eodon)   ████████░░░░░░░░░░░░    59/157     38%   +6
Endless Journey           █████████████░░░░░░░    13/20      65%
TOTAL                     ██████████░░░░░░░░░░  3050/6144    50%   +11
```

_Filename-stem matching: a proxy for presence, not behaviour. Unclassified files fall into Pre-AoS, inflating it. Directional, not a completion percentage._
<!-- EXPANSION:END -->
