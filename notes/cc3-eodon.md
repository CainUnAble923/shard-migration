# CC3 — Eodon core content: the verified list, the port, the timings

Date: 2026-09-06. Agent: Claude Code, headless. Pinned ModernUO `7c9215d97`.
Source: `D:\UO\ServUO-pub57` (read-only). Dependency oracle: `D:\UO\ModernUO-pinned` (read-only).

**The count was wrong a third time.** `docs/tasks.md` CC3 and `docs/eodon-separability.md` both
say "about 22 files, roughly 4,000 lines". The verified figure is **17 files, ~1,130 source lines
in**. The quest line — half the stated task by line count — is declined, and it is not a content
port.

`docs/eodon-separability.md` predicted this failure mode in its own methodology note and then
committed it twice more in the same table. Both new errors are the same shape: a keyword
("moonstone") or a directory name matched a large shared system, and nobody opened the file.

---

## Phase 1 verification: how each candidate was checked

Three gates, run per file, all against source, none against documentation:

1. **Genuinely Eodon content, not a shared system that mentions Eodon.** Read the file.
2. **Stem absent from stock ModernUO.** Checked against a 6,773-type universe extracted from
   `D:\UO\ModernUO-pinned\Projects\{Server,UOContent}`, *plus* the 117 stems already under
   `server/customizations`. Not against `tools/modernuo-stems.txt`, which is a filename-stem list
   and wrong for this (see AGENTS.md).
3. **References no Myrmidex or Shadowguard**, and no other subsystem ModernUO lacks. Every
   `new X(`, base class, `typeof(X)` and static access in the file was checked against the same
   6,773-type universe.

All 17 keepers passed the collision check against all three lists with zero hits.

---

## The verified list — 17 files

### Batch A — resources and leaf items (4 files)

| # | Ported to `server/customizations/` | ServUO source |
|---|---|---|
| 1 | `Items/Resource/RaptorTeeth.cs` | `Items/Resource/RaptorTeeth.cs` |
| 2 | `Items/Quest/AncientPotteryFragments.cs` | extracted from `Items/Quest/SAQuestItems.cs:122` |
| 3 | `Items/Consumables/PerfectBanana.cs` | extracted from `Items/Consumables/EodonPotions.cs:726` |
| 4 | `Items/Artifacts/Equipment/Weapons/RaptorClaw.cs` | same path |

2 and 3 are **forced dependency ports to the leaf**, per Q-010 / the `LuckyCoin` precedent:
`Raptor` drops `AncientPotteryFragments`, `SilverbackGorilla` drops `PerfectBanana`, and neither
exists in ModernUO. Both are trivial `Item` subclasses that drag in nothing. One extracted type
per file, per the recipe.

### Batch B — TOL decoration artifacts (6 files)

All six come out of the single ServUO file `Items/Artifacts/Decorative/TOLDecorationArtifacts.cs`,
split one type per file into `Items/Artifacts/Decorative/`:

`StretchedDinosaurHide`, `CarvedMyrmydexGlyph`, `WakuOnASpit`, `SacredLavaRock`,
`WhiteTigerFigurine`, `DragonTurtleHatchlingNet` — the six tribal reward decorations
(Barrab, Barako, Jukari, Kurak, Urali). Each is ~25 lines of `BaseDecorationArtifact`, no
behaviour.

`CarvedMyrmydexGlyph` is a **name**, not a coupling. It is the Barrab tribe's decorative reward;
it references no Myrmidex type and no Myrmidex system. Note the spelling — ServUO writes the item
"Myrmydex" with a **y**, so a `Myrmidex` grep does not find it. Flagged here so the next person
does not "discover" it and pull the Invasion in behind it.

### Batch C/D — creatures (7 files)

| # | Ported to `server/customizations/` | ServUO source |
|---|---|---|
| 11 | `Mobiles/Normal/Allosaurus.cs` | `Services/Expansions/Time Of Legends/Mobiles/Allosaurus.cs` |
| 12 | `Mobiles/Normal/Archaeosaurus.cs` | same directory |
| 13 | `Mobiles/Normal/Dimetrosaur.cs` | same directory |
| 14 | `Mobiles/Normal/Najasaurus.cs` | same directory |
| 15 | `Mobiles/Normal/Saurosaurus.cs` | same directory |
| 16 | `Mobiles/Normal/SilverbackGorilla.cs` | same directory |
| 17 | `Mobiles/Normal/Raptor.cs` | `Mobiles/Normal/Raptor.cs` |

**Path deviation, stated deliberately:** the six dinosaurs live in ServUO under
`Services/Expansions/Time Of Legends/Mobiles/`. They are ported to `Mobiles/Normal/` instead.
Reason: a space in a directory name is a liability in the `apply-patches.sh` mirror and in every
shell command that touches it, and these are ordinary creatures, not an expansion service. The
recipe's rule is "mirror ServUO's layout so *where did this come from* stays answerable" — that
question is answered by the table above instead. Applied consistently to all six.

---

## What was dropped, and why

### 1. The eight Aloron armour pieces — DECLINED (missing subsystem)

`Items/Artifacts/Equipment/Armor/Sets/Alorons Set/Alorons{Bustier,Gorget,Helm,Legs,LongSkirt,Shorts,Skirt,Tunic}.cs`

They rest on the **armour set-bonus subsystem**, which ModernUO ships **zero** files for.
Verified absent from `D:\UO\ModernUO-pinned`: `SetItem` (0 definitions), `SetAttributes` (0),
`AbsorptionAttributes` (0), and no `SetID` / `Pieces` / `SetPhysicalBonus` / `SetSelfRepair` on
`BaseArmor`. ModernUO's only `SetBonus` is `UOContent/Misc/AOS.cs:1212`, an unrelated
`SkillBonuses` method — a false positive if you grep for the word alone.

This is not a near miss. Read `AloronsTunic.cs`: after five resistance overrides, the entire item
**is** set data — `SetID`, `Pieces`, `SetAttributes.BonusMana`, `SetAttributes.LowerManaCost`,
`SetSelfRepair`, and five `Set*Bonus` values. Port it without the subsystem and what lands is a
re-hued `TigerPeltChest` with a label. That is porting halfway, which the rules forbid.

They also inherit from the **TigerPelt armour set** (`Items/Equipment/Armor/TigerPeltChest.cs`
and seven siblings), a further eight files on nobody's list, itself set-bonus content.

Carrying `SetItem.cs` (388 lines) across would not fix it — that file is the enum and the bonus
tables, not the `BaseArmor` plumbing that reads them.

**Cost to do it properly: the set-bonus subsystem, then TigerPelt (8 files), then Aloron (8).**
That is its own task, not CC3.

### 2. The quest line — DECLINED (subsystem port, not a content port)

`Quests/Eodon/Valley of One Quest/{Creatures,Items,TigerCubEnclosure}.cs`

Two independent reasons, either one sufficient.

**a. It is 3 of 8 files, not 3 of 3.** `Quests/Eodon/Valley of One Quest/` holds eight files and
3,870 lines: `Creatures.cs` (840), `DragonTurtleNest.cs` (256), `Items.cs` (759),
`MyrmidexSpawner.cs` (250), `Questers.cs` (414), `Quests.cs` (670), `TigerCubEnclosure.cs` (456),
`Volcano.cs` (225). The three named files reference `PrideOfTheAmbushQuest` and
`TimeIsOfTheEssenceQuest`, both defined in `Quests.cs`, and `TigerCub`, defined in `Creatures.cs`
alongside quest-only types. The three do not compile alone. The "2,058 lines" figure in
`docs/eodon-separability.md` is the sum of exactly those three files and is the sum of a set that
does not stand up. (There is also a second tree, `Quests/Eodon/MyrmidexThreat/`, 3,530 lines,
which is Myrmidex Invasion and out of scope by name.)

**b. It rests on a quest framework ModernUO does not have, and ModernUO has a different one.**
Every file is `namespace Server.Engines.Quests` over ServUO's Mondain's Legacy quest framework:
`BaseQuest`, `BaseQuestItem`, `BaseObjective`, `QuestChain`, `QuestHelper`, `MondainQuester`,
`BaseRewardTitleDeed`. Verified absent from `D:\UO\ModernUO-pinned`: `BaseQuest` (0),
`BaseQuestItem` (0), `QuestHelper` (0), `BaseRewardTitleDeed` (0).

That framework is **6,269 lines** in ServUO (`Services/MondainsLegacyQuests/` 5,625 +
`Quests/BaseQuest.cs` 644), before gumps and persistence.

ModernUO does ship a quest engine — `Engines/ML Quests` (`MLQuest`, `MLQuestSystem`,
`MLQuestInstance`, `MLQuestContext`) — but it is a **different shape**: static quest definitions
registered at load and referenced through a per-player context, against ServUO's per-player
instantiated `BaseQuest` objects carrying a `QuestChain`. Porting Eodon's quests means either
standing ServUO's framework up alongside ModernUO's (two serialized quest engines in one world)
or rewriting the quest line against `MLQuest`. The first is a subsystem port; the second is not a
port at all, it is a reimplementation, and it would be a fidelity deviation of exactly the kind
`docs/fidelity-principle.md` exists to prevent.

**Declined. This is a subsystem port, not a content port, as the brief anticipated.**

### 3. `MoonstonePowerGenerator.cs` — DECLINED (it is Myrmidex Invasion)

`Services/Expansions/Time Of Legends/Myrmidex Invasion/MoonstonePowerGenerator.cs`

It is **literally inside the `Myrmidex Invasion` directory**. It spawns `Zipactriotl`, the
Myrmidex boss (`:300`, `:319`), and `IgnisFatalis` (`:504`); it subclasses `DamageableItem`
(absent from ModernUO); and it is referenced only by `Myrmidex Invasion/System.cs` and the
MyrmidexThreat quest.

This is the third instance of the exact error `docs/eodon-separability.md` documents: a keyword
("moonstone") matched a shared system and it went on the list unread. The gate that catches it
is free — the file's own directory name says Myrmidex.

### Also considered and left off

- **`SetItem.cs`** (388 lines) — the set-bonus enum and tables. Inert without the `BaseArmor`
  plumbing ModernUO lacks. Also mentions Myrmidex.
- **The other TOL creatures** — `Gallusaurus`, `Anchisaur`, `DragonTurtle`,
  `DragonTurtleHatchling`, `GreaterPhoenix`, `DesertScorpion`, `Infernus`, `BritannianInfantry`,
  `EodonTribesman` (752 lines). Genuinely Eodon and genuinely absent from ModernUO, but **not on
  the CC3 list**, so left for a follow-up rather than silently widening scope. `EodonTribesman`
  in particular is a tribe-faction system, not a creature. `MyrmidexLarvae` / `MyrmidexDrone` /
  `MyrmidexWarrior` are Myrmidex and excluded.
- **`AuctionSafe/`** (2,108 lines, 5 files) — sits in the TOL folder, is not Eodon content, and
  is a vendor/auction subsystem.

## A correction to `notes/port-recipe.md` and `AGENTS.md`

**`SetWeaponAbility` DOES have a faithful ModernUO equivalent. The recipe says it does not.**

`notes/port-recipe.md` ("Enum and API renames that bite") and `AGENTS.md` (CC6 notes) both say:

> `SetWeaponAbility(...)` / `SetSpecialAbility(...)` do not exist on ModernUO's `BaseCreature`.
> Any ServUO creature that calls them needs a decision, not a translation.

The method names do not exist. The **capability** does:

- `UOContent/Mobiles/BaseCreature.cs:1312` — `public virtual WeaponAbility GetWeaponAbility() => null;`
- `UOContent/Mobiles/BaseCreature.cs:439` — `public virtual double WeaponAbilityChance => 0.4;`
- **49 stock ModernUO creatures override it**, including the multi-ability form
  (`AbysmalHorror.cs:57` uses `Utility.RandomBool()`, `DemonKnight.cs:202` a `Utility.Random(3)`
  switch) — which is exactly the shape ServUO expresses as several `SetWeaponAbility` calls.

All eight `WeaponAbility` names the CC3 creatures use exist in ModernUO under the same names:
`ArmorPierce`, `CrushingBlow`, `Disarm`, `BleedAttack`, `TalonStrike`, `MortalStrike`,
`Dismount`, `ConcussionBlow` (`UOContent/Items/Weapons/Abilities/WeaponAbility.cs:53-75`).

So the translation is mechanical and faithful:

```csharp
// ServUO
SetWeaponAbility(WeaponAbility.MortalStrike);
SetWeaponAbility(WeaponAbility.Dismount);

// ModernUO
public override WeaponAbility GetWeaponAbility() =>
    Utility.RandomBool() ? WeaponAbility.MortalStrike : WeaponAbility.Dismount;
```

**The other three do not translate.** `SetSpecialAbility`, `SetMagicalAbility` and
`SetAreaEffect` have no ModernUO counterpart — `SpecialAbility`, `MagicalAbility` and
`AreaEffect` are all absent from the pinned tree — and remain a decision, not a translation.

**Why this matters well beyond CC3.** The recipe's own measurement puts 132 of 462
`Mobiles/Normal` files (29%) in the "calls a Pet Training method" cohort and treats the whole
group as blocked. In CC3, **6 of 7 candidate creatures were in that cohort and 6 of 7 ported
anyway**, because `SetWeaponAbility` was the only one of the four they called. The 29% figure is
real but it is not a decline rate — it needs splitting by *which* of the four methods is called
before CC6 sizes its batches off it. That re-count is not done here.

This is AGENTS.md ground rule 4: source evidence beat a stated rule. Raised as Q-013.

---

## Deviations, for `docs/fidelity-principle.md`

Every one of these is a ServUO behaviour with no ModernUO equivalent, dropped rather than
approximated. None is a choice between two working options.

| Where | Dropped | Effect in game |
|---|---|---|
| all six dinosaurs | `AttacksFocus` | ModernUO has no such flag; creatures use normal `FightMode` targeting |
| Allosaurus, Dimetrosaur | `IsChampionSpawn` branch, `SetToChampionSpawn()` | no stat downgrade in a champ spawn. Inert: ModernUO's `ChampionSpawn` never calls back into the creature, and neither dinosaur is in a spawn table. The non-champion loot arm is kept |
| Dimetrosaur | `SetAreaEffect(AreaEffect.PoisonBreath)` | loses its poison breath area attack |
| Dimetrosaur | `OnAfterTame` (Hits/4 on first tame) | ModernUO has no `OnAfterTame` hook. `StatLossAfterTame` gives `AnimalTaming`'s `ScaleStats(0.50)` instead, so a tamed Dimetrosaur ends up stronger than on ServUO |
| Saurosaurus | `SpecialAbility.TailSwipe`, `SpecialAbility.LifeLeech` | loses both signature abilities. ServUO's own source carries the comment `// Missing: Life Leech, Tail Swipe ability` |
| Archaeosaurus, Saurosaurus | `DragonBlood => 6 / 8` | no dragon blood when carved; ModernUO has neither the property nor the item |
| RaptorClaw | `IsArtifact` | none. A ServUO-only `Server.Item` virtual whose every consumer (pigments, NaturalDye, AlterItem, RunicReforging) is also ServUO-only — zero readers in ModernUO |
| 6 TOL decorations | derive from `Item`, not `BaseDecorationArtifact` | none, and this one *prevents* a deviation: ModernUO's base adds an artifact-rarity property line that ServUO suppresses via `ShowArtifactRarity => false`. `DefaultWeight`, `ForceShowProperties` and `DisplayWeight` are reproduced so the rendered properties match ServUO exactly. Rarity retained as inert data |
| all 17 | no `SpeedClass` override | Medium (0.25 / 0.5), per the standing Q-008 answer |
| all 17 | range perception argument dropped | 16, which is what ServUO's constructor rewrites 10 to |
| six dinosaurs | ported to `Mobiles/Normal/`, not the ServUO path | none. Path choice, reasoned above |

**Saurosaurus is the closest call.** It loses two of its three abilities. It is still ported
rather than declined, following the `LuckyCoin` precedent (Q-010): its stats, loot, taming and one
weapon ability are all faithful, and a player checking UOGuide finds a saurosaurus that exists
with the right numbers rather than no saurosaurus at all. The alternative — declining it — was
considered and rejected. Flagged explicitly because it is a judgement call, not a rule.

---

## The clock

All times UTC, 2026-09-06. Agent wall-clock including model inference, the same unit as CC2.
Warm Docker build cache. No client. Excludes writing this file.

| # | Phase | From | To | Elapsed |
|---|---|---|---|---|
| 0 | Orientation — `AGENTS.md`, CC3 in `docs/tasks.md`, `docs/eodon-separability.md`, `notes/port-recipe.md`, `notes/cc2-timed-port.md`, standing answers | — | 21:39:30 | **~3:30** |
| 1 | **Verifying the file list** — read every candidate, build the 6,773-type ModernUO universe, screen 23 candidates, collision-check 17 keepers | 21:39:30 | 21:48:18 | **8:48** |
| 2 | Writing the verified list and the declines to `notes/` | 21:48:18 | 21:50:15 | **1:57** |
| 3 | Batch A — 4 resource / leaf items + **build (1:09), clean** | 21:50:15 | 21:52:02 | **1:47** |
| 4 | Batch B — 6 decoration artifacts + **build (1:06), clean** | 21:52:02 | 21:54:05 | **2:03** |
| 5 | Batch C — 4 creatures + **build (0:49), clean** | 21:54:05 | 21:56:34 | **2:29** |
| 6 | Batch D — 3 hard creatures + **build (1:01), clean** | 21:56:34 | 21:58:49 | **2:15** |
| 7 | Headless verification (breakdown below) | 21:58:49 | 22:05:11 | **6:22** |
| 8 | `expansion_coverage.py`, `progress-state.json`, `progress.py` | 22:05:11 | 22:08:04 | **2:53** |
| | **Total from end of orientation** | 21:39:30 | 22:08:04 | **28:34** |
| | **Total including orientation** | — | 22:08:04 | **~32:00** |

### Phase 7 broken down

| Step | Elapsed | Note |
|---|---|---|
| Harness setup — scratch dirs, config copy, loopback rewrite | 1:00 | CC2's three traps all avoided: Windows-style bind paths, `n` before `save`, `save` before `shutdown` |
| Run 1 — **wasted** | 1:47 | my fault, not the port's. I changed five config settings where CC2 changed three; `pingServer.enabled=False` makes stock `PingServer.Shutdown()` null-deref, because it never started. The save itself completed clean before the crash |
| Run 1 redo — start / save / shutdown | 1:42 | clean. Loopback-only on `127.0.0.1:2593` and `127.0.0.1:12000`, `Saving world done (0.02 seconds)`, clean shutdown, zero errors or warnings |
| Run 2 — reload the saved world | 1:08 | `Loading world done (622 items, 91 mobiles)`, zero errors |
| Assembly reflection over all 17 types | 0:45 | **17 ok, 0 bad** |

**Lesson from the wasted run, worth the same status as CC2's three traps: change exactly the
three settings CC2 changed** (`listeners`, `serverListing.address`, `autosave.enabled`) and
nothing else. The scratch config is not a place to tidy.

**Zero failed build cycles.** All four batches compiled first time. That is the direct payoff of
the pre-flight dependency check against `D:\UO\ModernUO-pinned`: every `new X(`, base class and
static access was resolved against the real tree before a single file was written, and it caught
`PerfectBanana`, `AncientPotteryFragments`, `DragonBlood`, `AttacksFocus`, `OnAfterTame`,
`IsChampionSpawn`, `ShowArtifactRarity` and `IsArtifact` before the compiler could. P2 lost a
whole cycle to one missing type; CC3 checked 23 files and lost none.

---

## Did the "batch of 20 is about an hour" estimate hold?

**Yes on throughput, by a wide margin. No on where the time goes.**

| | P2 estimate | CC3 measured |
|---|---|---|
| Per-file transformation | ~1:10 | **~0:30** (8:34 for 17 files, builds included) |
| Warm build cycle | 0:44 | 0:49–1:09, mean **1:01** |
| A batch of ~20 | ~1:00:00 | **~10:00** of actual porting |

Seventeen files took **8:34** to write and build, against the 23:20 the P2 rate predicts. That
estimate came from a sample of one creature ported by an agent meeting the recipe for the first
time, so it priced in learning that does not repeat.

**What the estimate missed, and it is the whole story:**

1. **Verification, not transformation, is the cost.** Phase 1 — deciding *which* files to port —
   took **8:48**, slightly longer than writing and building all 17 put together. P2's model has
   no line item for it, because P2 was handed its one file. Any batch drawn from a list someone
   else wrote pays this, and CC3's brief was right that paying it was worth more than the port.
2. **Batch size barely moves per-file cost but moves build cost a lot.** Four builds for 17 files
   is 4:05 of build time; seventeen builds would have been about 17:00. Builds are cheap per
   cycle and expensive per file. Batches of five are the right size, as instructed.
3. **Extraction inflates the file count without inflating the work.** 8 of the 17 files came out
   of 3 ServUO files. Counting ported *files* overstates the work; counting ported *ServUO source
   files* (12) understates the diff. Neither number is the effort.
4. **The declines cost real time and produce no files.** Roughly four minutes of phase 1 went to
   proving the quest line and the Aloron set are subsystems. That work moves no counter, and it
   is the most valuable output of this task.

**Revised estimate for CC6-style batches: ~0:30 per file, plus ~1:00 per build cycle of five,
plus a verification pass that scales with how much you trust the list.** A pre-verified batch of
20 done in fives: about **15 minutes**. Twenty files off an unverified keyword list: budget the
verification separately and expect it to be the larger half.

**One caveat on the throughput number.** CC3's 17 files are unusually homogeneous — six near-
identical dinosaurs and six near-identical decorations. `Raptor` alone (persisted state, an inner
timer, an `[AfterDeserialization]` hook) took longer than the six decorations together. A batch of
20 genuinely varied creatures will not hit 0:30 per file.

---

## What is verified and what is not

**Verified headlessly:** all 17 compile; the server starts; the world loads, saves and reloads
clean with zero errors; and all 17 types are registered in the shipped `UOContent.dll` with
generator-written `Serialize(IGenericWriter)` / `Deserialize(IGenericReader)` and a `(Serial)`
constructor — none of which appears in the source, so it is direct evidence the generator ran.
`Raptor` additionally reports the collapsed `(Boolean)` constructor, confirming the
optional-parameter form.

**Not verified, and deliberately not worked around:** an *instance* of any of these in a saved
world. The container console registers only `save`, `shutdown`, `restart`; there is no headless
spawn. Per the standing rule, this is batched for a later client spot check rather than
scaffolded around. **`Raptor` is the one to prioritise there** — it is the only ported type with a
`[SerializableField]`, so it is the only one whose round-trip is not already covered by what
`BaseCreature` does. Its `[AfterDeserialization]` delete-on-load is untested for the same reason.

**Nothing was deployed.** The live `sl-modernuo` container was never started. All testing ran in
throwaway `--rm` containers with no published ports, a scratch `Saves/` under a session temp
directory, and a scratch `Configuration` listening on `127.0.0.1` only.
`docker/uo/docker-compose.yml` was read and not touched (Q-009 is Chase's).

## Loose end

`python tools/expansion_coverage.py` crashes on a stock Windows console
(`UnicodeEncodeError: 'charmap' codec can't encode`) because it prints block-drawing characters
to cp1252. `PYTHONIOENCODING=utf-8 python tools\expansion_coverage.py` works, and that is what was
run here. Not fixed: it is a change to a tool I was not asked to touch, and it may not reproduce
in Chase's shell.
