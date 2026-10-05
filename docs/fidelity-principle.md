# Fidelity principle: port faithfully, so the existing wikis do our documentation

> **Reset, Chase, 2026-09-30 (recorded by the overseer 2026-10-02):** "We will TRY and be as faithful to OSI as
> possible but we will have a lot of systems that build on OSI so in the end we may just have one amazing and detailed
> wiki." This replaces the premise in the title below: the external wikis no longer do our documentation; the
> shard's own wiki does. Port faithfully still wins wherever OSI has an answer, and this register is still the list
> of where we differ, because it is the wiki's table of contents. Rows for systems that are entirely ours (the
> League, levels, guild costs) are registered so the wiki covers them, not because they are debt.

## The reasoning

The shard should run content players can look up **outside** a custom wiki. Twenty years of
UOGuide, Stratics, uo.com and forum knowledge already documents standard content. Every
system we run that matches OSI behaviour is a system nobody has to write documentation for.

This is the strongest argument for the "all newer content" scope. It is not about having more
things; it is about the shard being **legible to a new player without us explaining it**.

## The rule, as settled 2026-09-26

Chase: *"Look, I'm ok with customizing our stuff and eventually porting over what is needed into
a custom wiki to be honest."*

That settles a question this document had been carrying awkwardly, so the operative rule is now
stated once, in two halves:

**Content we port stays faithful to its source, so the existing wikis document it.** A ported
creature, item, quest or system should behave the way a player who read UOGuide expects. When it
cannot, that is a deviation and it goes in the register below.

**Content we invent is ours to design, and it goes on our own wiki.** Nothing is owed to fidelity
by a thing that exists nowhere else. It is owed a wiki entry instead.

The test between them is not who wrote the file. It is **whether a player could be misled by a
difference they had no way to know about.** A ported rotworm that quietly stops making stew is a
fidelity problem, because a wiki told the player it would. A board in the New Haven square that no
wiki mentions cannot mislead anyone about anything; a player either finds it or does not.

Two consequences worth naming, because they change how the register should be read:

1. **Invented content still gets a D-number.** Not because it is a failure, but because the wiki
   scope has to stay finite and known, which is the whole point of principle 5 below. D-90 is the
   first entry of this kind.
2. **A deviation on ported content is still a debt, and the rule above does not forgive it.** The
   reframing widens what we are allowed to build. It does not license changing a ported drop rate
   because we would prefer a different one.

## What it means in practice

**1. Port unchanged. Deviation is a documentation debt.**
Bring content across with its OSI behaviour intact: drop rates, spawn rates, damage, skill
gates, quest steps, timers. Every value we "improve" creates a page only we can write, and a
player who reads the wiki and finds it wrong trusts the wiki less everywhere else.

**2. Keep ServUO's defaults unless there is a reason.**
ServUO's config values encode OSI behaviour. Changing one is a decision that needs recording
in `docs/`, not a preference applied in passing.

**3. Prefer well-documented content when ordering the backlog.**
As a tiebreaker between two candidates of similar cost, take the one a player is more likely
to find written up. Named dungeons, known creatures, standard crafting, published quest lines
score high. Obscure systems score low.

**4. Tune configuration, not code.**
Deciding a system is *off* costs nothing documentation-wise: the player never meets it.
Deciding it is on but *different* costs a wiki page. Prefer on-or-off over on-but-changed.

**5. Record every deliberate deviation in one place.**
When we do deviate, and we will, this is our shard, it goes in a running list so a custom
wiki, if it ever exists, has a finite and known scope rather than being needed everywhere.

## The tension, stated honestly

The shard already runs a hundred-odd custom scripts with no external documentation anywhere: extended
ore and lumber tiers (Platinum through Celestial), the Artificer and Forester guild systems,
PetMimic, the pack mule breeding system, satchels, the league and achievement systems. None
of that is on any wiki and never will be.

So the goal is not zero custom documentation. It is **keeping the custom surface small and
bounded** while the large standard surface documents itself. Our custom systems are the
things a shard wiki would cover; everything ported should not need to be.

That is also a reason to be careful about "improving" ported content: it silently grows the
set of things that need explaining, and it grows it in the places players are least expecting
surprises.

## Withdrawn: six entries that were never deviations, and one overstated

These were recorded as losses and are not. Every one has the same cause, which
`docs/bug-list.md` §1b carries as a standing entry: **reasoning from ServUO's vocabulary to
ModernUO's capability.** ServUO names a thing, pinned ModernUO has no class or method by that
name, and the absence of the name is read as the absence of the behaviour. A missing name is
evidence about the name.

- **D-55 (`Slith`), D-56 (`ToxicSlith`), D-62 (`FireDaemon`), D-68 (`CrystalHydra`): retired
  2026-09-21.** Each recorded `SetSpecialAbility(DragonBreath)` as a Pet Training loss. Pinned has
  the ability as `MonsterAbilities.FireBreath` from `BaseCreature.GetMonsterAbilities()` (`:1131`),
  with `ColdBreath : FireBreath` for the cold variant, and CC4 had already used it. The breath is
  restored on all four (`notes/cc6-followup-breath-incubator.md`), so these are retired rather than
  reversed: they were never true, and the creatures now fight correctly.
- **D-47 (`SkeletalLich`): withdrawn, Q-050.** It recorded the lich running `AI_Mage` instead of
  ServUO's `AI_NecroMage` as "casts Magery only; its 100-120 Necromancy is set and unused." Pinned
  `MageAI` carries the necromancer branch itself and gates it on **skill, not AI type**:
  `IsNecromancer => Core.AOS && Mobile.Skills.Necromancy.Value > 50` (`MageAI.cs:70`), with
  `UseNecromancy()` weighting the choice by magery against necromancy (`:252`) and ServUO's own
  spell sets in `GetRandomDamageSpellNecro` (`:262`) and `GetRandomCurseSpellNecro` (`:301`). A lich
  with 100-120 Necromancy casts Necromancy on the stock AI.
- **D-45 (`Spellbinder`): withdrawn 2026-09-26, found while building this register.** It recorded
  three losses against ServUO's `AI_Spellbinder`: no spirit-speak heal, no teleport, no dispel.
  Pinned `MageAI` has all three as its own constants: `HealChance = 0.10` with
  `Mobile.UseSkill(SkillName.SpiritSpeak)` in the heal path (`:18`, `:135-160`),
  `TeleportChance = 0.05` (`:19`, `:215`), `DispelChance = 0.75` (`:20`, `:337-367`). ServUO's
  figures are 5%, 5% and 75%. **The whole deviation is a 5 point difference in heal chance**, not
  the loss of three behaviours, and it should be restated at that size or dropped. This is the
  `HealChance` trap already named in `AGENTS.md`, which means the trap was documented and the
  entry it had already produced was never revisited.

- **D-44 (`GreenGoblinScout`): one of its three claims withdrawn, 2026-09-26.** It recorded the loss
  of hiding while wandering, a 4% combat teleport, and fleeing below 20% hits, against ServUO's
  `AI_OrcScout`. **The flee is stock.** The scout runs `AI_Melee`, and pinned `MeleeAI` overrides
  `BaseAI`'s `FleeHealthThreshold => 0.0` to **`0.2` with `FleeChance => 0.1`** (`MeleeAI.cs:9-10`),
  then flees in `DoActionFlee` (`:142`). So it does flee below 20% hits, at a 10% chance per check.
  **The other two claims stand:** pinned has no self-hiding for a wandering creature and no combat
  teleport outside `MageAI`, so D-44 is real at two thirds of its recorded size and should be
  restated at that size.

  **How I got this wrong the first time, because the method matters more than the entry.** I wrote
  in this document earlier today that pinned's AI base class "is not in the checkout under any
  `*AI.cs` name". It is, at `Projects/UOContent/Mobiles/AI/BaseAI/BaseAI.cs`. I had searched the
  cloud container, where only the files I had staged exist, and read the empty result as a fact
  about the pinned tree. That is the same error this section is about, one level up: an absence in
  the place I happened to look, taken as an absence in the thing itself. The check that settles it
  is to list the directory on the machine that holds the tree.

## Deliberate deviations, before D-numbering

These predate the D-number scheme and stay in prose, which is how they were written and where the
reasoning lives.

- **2026-09-06, F3.** `SmithBOD-PostValorite.patch` split into
  `SmallSmithBOD-PostValorite.patch`. Content unchanged; the `LargeSmithBOD` half was dead
  because that file is replaced wholesale. Renamed because the old name implied both files.
  No behaviour change.

- ~~**2026-09-06, P2.** `LuckyCoin` ported without its `OnDoubleClick`.~~ **CLOSED 2026-09-07 by
  S2.** The Fountain of Fortune cluster is ported and `OnDoubleClick` is restored, covering all
  twelve coin droppers at once, pinned by a regression test. The original decline rested on a
  factual error of mine: `EnchantedEssence` and `RelicFragment` do not pull in Imbuing, they are
  leaf items in `SAQuestItems.cs` that Imbuing merely consumes. Kept struck through rather than
  deleted, because a deviation that got closed is the most useful kind of entry this log has.

- **2026-09-06, CC3.** Eleven deviations across the 17 Eodon files, every one a ServUO behaviour
  with no ModernUO equivalent, dropped rather than approximated. Full table with reasoning in
  `notes/cc3-eodon.md`. The ones a player could notice:
  - **`Dimetrosaur` loses its poison breath area attack** (`SetAreaEffect`). ModernUO has no
    `AreaEffect` at all.
  - **`Saurosaurus` loses Tail Swipe and Life Leech** (`SetSpecialAbility`). ServUO's own source
    carries the comment "Missing: Life Leech, Tail Swipe ability", so OSI parity was already
    imperfect upstream. **This is the closest call in the set.** It keeps correct stats, loot,
    taming and one weapon ability, and was ported rather than declined on the `LuckyCoin`
    precedent: a saurosaurus with the right numbers beats no saurosaurus.
  - **`Archaeosaurus` and `Saurosaurus` give no dragon blood when carved.** ModernUO has neither
    the property nor the item.
  - **A tamed `Dimetrosaur` ends up stronger than on ServUO.** ModernUO has no `OnAfterTame`
    hook, so `AnimalTaming`'s `ScaleStats(0.50)` applies instead of ServUO's Hits/4.
  - All six dinosaurs lose `AttacksFocus`; ModernUO uses normal `FightMode` targeting.

  **Reversal:** each is one file, and each becomes portable if the corresponding ModernUO
  subsystem is ever built.

  Three further entries in that table are deviations only on paper and change nothing a player
  sees: the champion-spawn branch (ModernUO's `ChampionSpawn` never calls back, and neither
  dinosaur is in a spawn table), `RaptorClaw.IsArtifact` (zero readers in ModernUO), and the six
  decorations deriving from `Item` rather than `BaseDecorationArtifact`, which **prevents** a
  deviation by suppressing a rarity line ServUO also suppresses.

- **2026-09-07, S1.** Four deviations in the armour set-bonus subsystem, all omissions rather
  than approximations, which is the right side of "prefer turning a system off over running it
  differently". Full reasoning and the cost to close each in `notes/s1-armour-sets.md` section 5.
  - **`AbsorptionAttributes.EaterCold = 2` omitted from all eight Aloron pieces.** That property
    is `SAAbsorptionAttributes`, the Stygian Abyss damage-eater system, which ModernUO lacks
    entirely and whose `GetValue` pulls in `Enhancement`, `RunicReforging` and
    `SkillMasterySpell`. **What a player notices:** a completed Aloron set gives no cold-damage
    eating. **Closes when** the absorption subsystem is built, which is now a costed row in S3.
  - **Aloron's Dinosaur Slayer omitted, effect and tooltip line both.** ModernUO's `SlayerName`
    enum has neither `Dinosaur` nor `Myrmidex`. Omitting the tooltip too is deliberate: a slayer
    line that does not slay is worse than no line.
  - **`SetSelfRepair` uses ModernUO's self-repair formula, not ServUO's.** The set contributes
    faithfully at the same point ServUO adds it; the two emulators' underlying formulas already
    differed, and this changes nothing about that.
  - **Property-list ordering differs slightly** from ServUO, because ModernUO splits
    `AddNameProperty` from `GetProperties`. Cosmetic; the same lines with the same values.

- **2026-09-07, S2.** Four live deviations in the Fountain of Fortune cluster. Full reasoning in
  `notes/s2-fountain.md`.
  - **The fountain's luck bonus shows in the status bar**, where ServUO hides it. ServUO routes
    the reward through `PlayerMobile.RealLuck`, which ModernUO does not have, and all three of
    ModernUO's luck consumers read `Mobile.Luck`. One patched line in `PlayerMobile.Luck` gets all
    three right, against three patches into three content files for the invisible version.
    Cosmetic, and the cheaper patch is the more robust one.
  - **`SolesOfProvidence` loses `IsArtifact`**, a ServUO-only virtual with zero readers in
    ModernUO. Inert.
  - **Nothing places a fountain yet**, so the coin's only reachable outcome is its failure
    message. Not a deviation we are keeping: Q-021 answers it with the OSI coordinates,
    Ter Mur `(1121, 957, -42)`, and it is a small follow-on task. **Still true as of 2026-09-26:**
    nothing in the tree places one. `docs/bug-list.md` §1 carries it as an open loose end. **2026-10-02:** cc-P27 built `[ClusterFSeedFountainOfFortune`, which places it at that point; D14 closes once Chase confirms the shore is reachable on foot.
  - **ServUO's two unreachable reward cases are ported unchanged** rather than "fixed". Correct
    under "port unchanged": upstream dead code stays dead code, and quietly repairing it would be
    an undocumented divergence from every wiki that describes the fountain.

## The numbered register, D-1 to D-120

Every numbered deviation, in one place, current to 2026-09-26. **Each row is a pointer, not the
entry**: the note named in the last column carries the full statement, the reasoning and what would
reverse it. Nothing here replaces reading that note before acting on a row.

Status, and how it was assigned:

- `visible` a player can notice it and we are living with it. **This is the wiki debt.**
- `paper` nothing a player can notice. Assigned where the note's own player-effect column says so.
- `fix` we differ from ServUO on purpose because ServUO was wrong. Closer to OSI, no debt.
- `closed` was true, has since been fixed.
- `retired` recorded in error, never true. See the withdrawn section above.
- `ours` content we invented. Owed a wiki entry, not a fix.

Counts: 91 numbers issued, 90 with a table row in a note (D-36 was issued and has no row, which
is itself a loose end). 6 retired, 3 closed, 1 ours, 6 fixes, and the rest split between `paper`
and `visible`.

| # | What changed | What a player notices | Status | Note |
|---|---|---|---|---|
| D-1 | `IsArtifact => true` dropped across 208 of 320 artifact files | nothing; zero readers in pinned | `paper` | `cc9-artifacts` |
| D-2 | `CanBeWornByGargoyles` dropped on 70 files; the race gate kept via `RequiredRaces` | nothing | `paper` | `cc9-artifacts` |
| D-3 | `AxeOfAbandon` loses `BattleLust` | no Battle Lust line and the effect never fires | `visible` | `cc9-artifacts` |
| D-4 | `XenrrFishingPole` loses `SpellChanneling`, `CastSpeed -1` | casting clears hands, as with a normal pole | `visible` | `cc9-artifacts` |
| D-5 | `BaseCostume` and all 34 costumes stay on when the wearer is damaged | a masked player keeps the mask through combat | `visible` | `cc9-artifacts` |
| D-6 | `GargishEarrings`/`GargishNecklace` drop two non-virtual overrides | nothing; the resource terms they suppressed are zero | `paper` | `cc9-artifacts` |
| D-7 | `GreymistGloves` is not `IArcaneEquip` | nothing; an artifact glove is never crafted arcane | `paper` | `cc9-artifacts` |
| D-8 | `GobletOfCelebration` clamps a negative refill delay; `DateTime.Now` to `Core.Now` | nothing | `paper` | `cc9-artifacts` |
| D-9 | `BaseCostume.OnRemoved` calls base once where ServUO calls twice | nothing | `paper` | `cc9-artifacts` |
| D-10 | `GargishWarHammer` flips to `0x48C1`, not ServUO's `0x481` | nothing wrong; `0x481` is a Prism of Light pillar, so ServUO's value is a typo | `fix` | `cc9-artifacts` |
| D-11 | `EvilOrcHelm` drops `UseIntOrDexProperty` | nothing; zero readers in ServUO either | `paper` | `cc9-artifacts` |
| D-12 | `OrcishBow` shows one durability line where ServUO shows two | one tooltip line | `visible` | `cc9-artifacts` |
| D-13 | `StaffRing` tests `AccessLevel == Player`, not `IsPlayer()` | nothing; cause corrected in Q-040 | `paper` | `cc9-artifacts` |
| D-14 | Bestial berserk inert: `BestialSetHelper.OnDamage`/`OnHeal` have no caller | a full Bestial set never rages: no damage shrug, no heal block, no hue shift | `visible` | `cc9-artifacts` |
| D-15 | `FrostguardTalisman`, `JadeSnakeHead` lose `EaterCold`/`EaterPoison 5` | one tooltip line; ServUO never aggregated a talisman's absorption either | `visible` | `cc9-artifacts` |
| D-16 | `DarkwoodCrown` flips to `0x3168`, not ServUO's `0x3169` | nothing wrong; `0x3169` is the flipped Vulture Helm | `fix` | `cc9-artifacts` |
| D-17 | `Swiftflight` not ported; Marksman set could not complete | closed by CC6 batch 5: ported as `Bow, ISetItem` | `closed` | `cc9-artifacts` |
| D-18 | `SorcererHat`, `VirtuososCap` drop `BaseHat`'s shipwreck and craft-bonus fields | nothing; artifact hats are neither fished up nor crafted | `paper` | `cc9-artifacts` |
| D-19 | `JadeWarAxe` drops `BaseAxe`'s `IUsesRemaining` fields | nothing; `WarAxe.HarvestSystem => null` | `paper` | `cc9-artifacts` |
| D-20 | `[Alterable]` dropped from 8 classes | nothing; pinned has no alter-item system | `paper` | `cc9-artifacts` |
| D-21 | `SoulCharge` dropped from three shields | the three shields lose the line and the effect | `visible` | `cc9-artifacts` |
| D-22 | `HitLowerDefend 30` dropped from three head pieces | no hit-lower-defence | `visible` | `cc9-artifacts` |
| D-23 | `DespicableQuiver` loses a random resistance and Archery +5 | the quiver shows neither line | `visible` | `cc9-artifacts` |
| D-24 | Epiphany burst inert: `EpiphanyHelper` hooks have no caller | the 12 Villainous pieces are plain armour; no burst, no Set Ability lines | `visible` | `cc9-artifacts` |
| D-25 | `RunedDriftwoodBow` loses `LowerAmmoCost 15` | one line; lower ammo cost still works on quivers | `visible` | `cc9-artifacts` |
| D-26 | The five Darden pieces do not emit "Myrmidex Slayer" | no line, and no set slayer to apply | `visible` | `cc9-artifacts` |
| D-27 | `FirstAidBelt.HealingBonus` stored but inert, line suppressed | no bandage bonus; the attribute lines were cosmetic on ServUO too | `visible` | `cc9-artifacts` |
| D-28 | `TenthAnniversarySculpture` luck inert: `GetLuckBonus` uncalled | an hour of nothing after "Your luck just improved!" | `visible` | `cc9-artifacts` |
| D-29 | `PutridHeart` inert: no Despise crystal points awarded | hearts pile up and cannot be redeemed | `visible` | `cc4-despise` |
| D-30 | `MysteriousWisp` not placed; two quest and town-crier hooks dropped | no vendor to spend crystal points with, no quest, no title deed | `visible` | `cc4-despise` |
| D-31 | `Container.DropToWorld` does not call `WispOrb.CheckDrop` | an orb inside a bag survives the bag being dropped; a dropped orb still vanishes | `visible` | `cc4-despise` |
| D-32 | `Silenii` and `Phantom` lose `MagicalAbility.Discordance` | neither creature discords | `visible` | `cc4-despise` |
| D-33 | `ForceNotoriety` absent; possessed notoriety comes from the master | a possessed creature's name shows in its possessor's colour | `visible` | `cc4-despise` |
| D-34 | No `SmartSpawning`: spawners do not idle when nobody is near | the dungeon is populated whether or not anyone is in it | `visible` | `cc4-despise` |
| D-35 | Lower level rolls power 4-8 where ServUO's XML builds nothing | on pub57 the battlefield is empty; here it has the army the design implies | `fix` | `cc4-despise` |
| D-36 | **No table row in any note.** Issued and never written up | unknown | `loose end` | none |
| D-37 | Crystals of Shame inert; altars cannot be paid (`Enabled => false` seam) | the level guardians can never be summoned by a player | `visible` | `cc4-shame` |
| D-38 | Chest loot not reforged; no SA refinement roll | chest loot has no magic properties and no armour refinements | `visible` | `cc4-shame` |
| D-39 | Pet Training abilities dropped: `StickySkin` (MudPie), `ColossalRage` (three elementals), `SearingWounds` (MoltenEarthElemental). **The note says "four" and names three**, which needs settling | those creatures hit without their rider effects | `visible` | `cc4-shame` |
| D-40 | `LifeLeech` mapped to ModernUO's `DrainLifeAttack` | the drain lands more often and costs the victim mana | `visible` | `cc4-shame` |
| D-41 | `CrazedMage` runs `AI_Mage`; ServUO's is `AI_Mystic` | it casts Magery, not Mysticism | `visible` | `cc4-shame` |
| D-42 | `TreasureMapChance => 1.0` has no counterpart; the stock roll applies | a level-5 map sometimes rather than always | `visible` | `cc4-shame` |
| D-43 | A timed-out challenge clears the altar; ServUO leaves it stuck until restart | the altar can be challenged again after a failed hour, as the design reads | `fix` | `cc4-shame` |
| D-44 | `GreenGoblinScout` runs `AI_Melee`, not `AI_OrcScout`: no hiding while wandering, no 4% combat teleport | **the flee claim is withdrawn**, `MeleeAI` flees below 20% at a 10% chance. Two thirds of the recorded size; restate it | `visible` | `cc6-creatures-batch1` |
| D-45 | `Spellbinder` runs `AI_Mage`, not `AI_Spellbinder` | withdrawn 2026-09-26: pinned `MageAI` heals, teleports and dispels. Real difference is 5 points of heal chance | `retired` | `cc6-creatures-batch1` |
| D-46 | `ShameWall` is `Visible = true` from the start; ServUO leaves it invisible until its troll dies | nothing; the wall now behaves the same before and after its first troll | `fix` | `cc6-creatures-batch1` |
| D-47 | `SkeletalLich` runs `AI_Mage`, not `AI_NecroMage` | withdrawn, Q-050: pinned `MageAI` gates Necromancy on skill, not AI type | `retired` | `cc6-creatures-batch2` |
| D-48 | A dead boura or kepetch yields no fur on carve | kill one without shearing it first and the fur is lost | `visible` | `cc6-creatures-batch2` |
| D-49 | `BouraTailShield` has no Reactive Paralyze | no line, and attackers are never frozen by it | `visible` | `cc6-creatures-batch2` |
| D-50 | No dragon's blood from carving a boura, kepetch or slith | a mystic cannot farm the reagent from these | `visible` | `cc6-creatures-batch2` |
| D-51 | `RuddyBoura` loses `ColossalBlow` | the boura never stuns | `visible` | `cc6-creatures-batch2` |
| D-52 | `HighPlainsBoura` loses `TailSwipe` and `ColossalBlow` | neither effect | `visible` | `cc6-creatures-batch2` |
| D-53 | `LowlandBoura` loses `ColossalBlow` | never stuns | `visible` | `cc6-creatures-batch2` |
| D-54 | `Kepetch` loses `ViciousBite` | no bleed over time | `visible` | `cc6-creatures-batch2` |
| D-55 | `Slith` recorded as losing `DragonBreath` | retired 2026-09-21; the breath is restored and it breathes fire | `retired` | `cc6-creatures-batch2` |
| D-56 | `ToxicSlith` recorded as losing `DragonBreath` | retired 2026-09-21; restored | `retired` | `cc6-creatures-batch2` |
| D-57 | `StoneSlith` loses `GraspingClaw` and `TailSwipe`; `BleedAttack` kept | no resist debuff, no stun | `visible` | `cc6-creatures-batch2` |
| D-58 | `Rotworm` loses `BloodDisease` | no sickness from a rotworm bite | `visible` | `cc6-creatures-batch3` |
| D-59 | `Rotworm` corpse yields ribs, not raw rotworm meat | a cook cannot make Bowl of Rotworm Stew | `visible` | `cc6-creatures-batch3` |
| D-60 | `Rotworm` never drops `ArielHavenWritofMembership` | nothing; the Missing quest is not here either | `paper` | `cc6-creatures-batch3` |
| D-61 | `Rotworm` does not flee a burning `CandlewoodTorch` | nothing until the torch exists; it is a Missing-quest reward | `paper` | `cc6-creatures-batch3` |
| D-62 | `FireDaemon` recorded as losing `DragonBreath` | retired 2026-09-21; restored | `retired` | `cc6-creatures-batch3` |
| D-63 | `BloodWorm` loses `Anemia` | no stat drain and no leech on hit; the corpse drain is ported | `visible` | `cc6-creatures-batch3` |
| D-64 | `ClockworkScorpion` cannot be repaired by a tinker | its hits regenerate normally; nothing else | `visible` | `cc6-creatures-batch3` |
| D-65 | `FireAnt` loses `ExplosiveGoo` | no goo burst; damage and resists are as ServUO's | `visible` | `cc6-creatures-batch3` |
| D-66 | `MaddeningHorror` loses `ManaDrain` | no mana drain; its casting is as ServUO's | `visible` | `cc6-creatures-batch3` |
| D-67 | `AcidSac` cannot burn the Underworld's vine walls | nothing; the walls are not here | `paper` | `cc6-creatures-batch3` |
| D-68 | `CrystalHydra` recorded as losing `DragonBreath` | retired 2026-09-21; restored as cold breath | `retired` | `cc6-creatures-batch4` |
| D-69 | `ChickenLizardEgg` never incubated | closed 2026-09-21 by the Incubator (P12) | `closed` | `cc6-creatures-batch4` |
| D-70 | `ChickenLizardEgg` could not be watered | closed 2026-09-21 by `Beverage-chicken-lizard-egg-pour.patch` | `closed` | `cc6-creatures-batch4` |
| D-71 | `BattleChickenLizard` loses `OnAfterTame` | one tamed mid-flight keeps fleeing for the rest of the 30 s | `visible` | `cc6-creatures-batch4` |
| D-72 | `CrystalHydra` loses `LootPack.Parrot` | no parrot from a crystal hydra | `visible` | `cc6-creatures-batch4` |
| D-73 | `LegacyOfDespair` loses `HitCurse 10` | one line; no 10% Curse on hit | `visible` | `cc6-creatures-batch5` |
| D-74 | `SwordOfShatteredHopes` loses `SplinteringWeapon 20` | one line; no splinter | `visible` | `cc6-creatures-batch5` |
| D-75 | `TheImpalersPick` loses `HitManaDrain 10` | one line; no mana drain on hit | `visible` | `cc6-creatures-batch5` |
| D-76 | `ClanChitterTinkerer` keeps the OSI name; ServUO's `ClanCT.cs` says "Clan Scratch Tinkerer" | the OSI name, which UOGuide has and ServUO's does not | `fix` | `cc6-batch7` |
| D-77 | Six ratmen are not Repond slayer targets | a Repond weapon does normal damage to them | `visible` | `cc6-batch7` |
| D-78 | Seven ratmen and three others are not Vermin talisman targets | a Vermin talisman gives no bonus against any of them | `visible` | `cc6-batch7` |
| D-79 | `BasePeerless` has no altar: no instance, no teleporter, no key consumption | a party walks to the boss instead of unlocking a private copy of the room | `visible` | `cc6-batch8` |
| D-80 | `BasePeerless` drops no `SkillMasteryPrimer` | nothing here; `BaseSABoss.DropPrimer => false` on ServUO too | `paper` | `cc6-batch8` |
| D-81 | `CanBeParagon => false` not carried | nothing reachable; paragon conversion is Ilshenar-only and all four spawn on Ter Mur | `paper` | `cc6-batch8` |
| D-82 | Five Pet Training abilities dropped across Navrey, the Slasher and Medusa | Navrey never webs; the Slasher never burns, drains or freezes; Medusa poisons one target at a time | `visible` | `cc6-batch8` |
| D-83 | Navrey has no lair: `NavreysController`, the pillars and the web tunnels are not ported | she stands on her spawner with no pillar mechanic | `visible` | `cc6-batch8` |
| D-84 | Nothing produces `EyeOfNavrey` for the Green With Envy quest | nothing; the quest is not here | `paper` | `cc6-batch8` |
| D-85 | Navrey teleports: pinned `MageAI` casts Teleport where ServUO's `TeleportChance => 0` forbade it | she blinks toward her target; on ServUO she never does | `visible` | `cc6-batch8` |
| D-86 | None of the four Abyss bosses is a slayer target | a demon, spider, reptile, dragon or repond slayer does normal damage | `visible` | `cc6-batch8` |
| D-87 | `LifeSyphon` and `VampiricEssence` lose `BloodDrinker 1` | the bleed is not doubled and does not heal the wielder | `visible` | `cc6-batch8` |
| D-88 | The Gorgon Lens does not exist, so nothing deflects Medusa's gaze | every gaze petrifies; on OSI a lens-wearer is deflected | `visible` | `cc6-batch8` |
| D-89 | A petrified `MedusaClone` does not animate as a statue | the copy stands still at hue 761 instead of the statue pose | `visible` | `cc6-batch8` |
| D-91 | Gargish cloth **clothing** artifacts do not swap to the female graphic. ServUO's four cloth bases set `ItemID` to the female art in `OnAdded`; the five of ours that sit on a set carrier instead do not (`SpinedBloodwormBracers`, `MantleOfTheFallen`, `SummonersKilt`, `BestialKilt`, `VirtuososKilt`) | a female gargoyle wearing one sees the male art (`0x408` rather than `0x407`) | `visible`, cosmetic | `armour-set-completion` |
| D-90 | **Our own content.** A New Haven training board at `(3502, 2573, 14)` Trammel offering the 26 stock skill-training quests through the stock ML quest path | a new player can take the training quests from the tile they arrive on. Quests, text, rewards and the 50-point lockout are unchanged; only the place is new. No wiki mentions the board | `ours` | `new-haven-quest-board` |
| D-92 | **Ours (F-19).** Banks hold 1,000 items, plus 100 per League rank once ranks exist (0 today); backpacks and house containers keep 125. The limit is reapplied at login, so a hand-set bank limit resets | a bank takes far more than OSI's 125 | `visible` | `cc-P22` 2, `p22-decisions-2026-10-01` |
| D-93 | **Ours (F-11).** Our guild systems take costs and turn-ins from the bank as well as the pack (pack loose, pack satchels, bank loose, bank satchels), never equipped, blessed or locked-up items. Since cc-P27 this includes the essence an Artificers' imbue takes, including from the Essence Satchel. OSI crafting and BODs stay pack-only | guild upgrades, restorations, turn-ins and imbues draw from the bank | `visible` | `cc-P22` 4 and 9, `cc-P27` 2 and 7 |
| D-94 | **Ours (F-16).** Jacob's Pickaxe restoration costs less at T1 (1 voucher, 25 iron, 100 gp) and T2 (4 vouchers, 100 iron, 15 dull copper, 1,000 gp). OSI has no such item | cheaper restoration | `visible` | `cc-P22` 1 |
| D-95 | **Ours (F-9 follow-up).** Wren, the Thieves' Den lookout, sits on the stool at Trammel 3440,2558,56 and points to the Thieves' guildmaster. Placed by `[ClusterFSeedGuildHalls` | an NPC OSI does not have | `visible` | `cc-P22` 3, `p22-decisions-2026-10-01` |
| D-96 | **Ported with two additions (F-17).** "Combine this deed with contained items": the container must be the backpack or inside it (OSI and ServUO accept any container), and it stops when the deed is full and says how many went in (ServUO repeats "maximum already combined" per leftover) | a bag elsewhere cannot be used; a clearer message | `visible` | `cc-P22` 5 and 9 |
| D-97 | **Ours (F-15).** A date version, patch notes shown in the login bulletin once per account per version, `[version`, and `shard.version` in status.json | patch notes at login | `visible` | `cc-P22` 6 |
| D-98 | **Ours (D42).** The Smith Guild salvage bag scales its return with Mining past 100 but never returns more than `cost - 1` (floor 2); OSI clamps Mining at 100 (pinned `SalvageBag.cs:94-98`). Vanilla `SalvageBag` is untouched | high Mining returns more, never a profit | `visible` | `cc-P23` 1 |
| D-99 | **Ours (D43).** The Smith Seal catalog sells no power scrolls (tab removed; F-12 will repoint scrolls at level) | nothing to buy there | `visible` | `cc-P23` 2 |
| D-100 | **Ours (F-8, a custom static).** A "shattered runestone" with four staff-chosen facings, art by Vrark (servuo.dev "Animated Runestone"; the download's "MMH7" names are a misnaming, art cleared by Chase 2026-10-02), shipped as TazUO PNG overrides in art slots 0x3C10-0x3C3B and animated through tiledata and animdata records the launcher writes into copies of the player's own files. The server's in-memory tiledata for those four IDs is ours, so the stone blocks. The Reset Stone wears design 1 (F-7b amended) | an item OSI does not have | `visible` | `cc-P26` 11, `p26-decisions-2026-10-02` |
| D-101 | **Ours (stats, Chase 2026-10-02).** Raw stats gain to `stats.statMax = 500` in both configs (OSI 125, set May 2026, `docker/uo/SERVER.md:642`), with **no** per-stat table, total cap or veteran +50. Today `patches/PlayerMobile-individual-stat-cap.patch` clamps effective stats at 500 (OSI 150); F-12 removes that clamp. Stats carry through a reset. Consequences kept on purpose: self-bandage reaches 1.0 s at Dex 200 and instant from effective Dex 220 (pinned `Bandage.cs:493`); pets gain to the same cap; stock bosses were balanced for OSI numbers | stats far above OSI's | `visible` | `cc-P25`, `p25-decisions-2026-10-02` |
| D-102 | **Ours.** Carry weight is `100 + 3.5 x Str` for humans with no cap (`customizations/ClusterFBackpack.cs:33-42`; 800 stones at Str 200, 1850 at effective 500, against OSI's 550 cap) | carry far more than OSI | `visible` | `p25-decisions-2026-10-02` 2 |
| D-103 | **Ours (D45).** Meditation's start chance: OSI uses the absolute mana deficit; above a 150-mana pool ours scales the deficit to a 150 pool, so a large pool is not penalized. At or below 150 it is OSI's formula exactly | high-Int characters can start meditating with a large pool partly empty | `visible` | `cc-P29` 2 and 7 |
| D-104 | **Ours (D14).** Twelve walkable pavers of existing art ("PaverStones Natural") over the decorative stepping rocks to the Fountain of Fortune, ending one tile from it, placed by `[ClusterFSeedFountainSteps`. In OSI's data the rocks are impassable and no walkable tile is within the coin range of 3. The fountain stays at OSI's point | a player can walk out to the fountain | `visible` | `cc-P29` 4 and 7 |
| D-105 | **Ours (PT-11).** Smith BODs run on two paths: any blacksmith gives and takes them for OSI's rewards (OSI's path); the Blacksmith Guildmaster and the Smithing Guild Book give and take them for Smithing Seals and standing, with no cooldown (at most 3 small and 1 large in the pack; large needs 70.1 Blacksmithy since cc-P42, D-108; guild turn-ins pay x3 Seals and x2 standing since cc-P42). Because the guild path has no cooldown and regular smiths pay OSI's rewards for its deeds, OSI's 1-to-6-hour per-deed throttle (`Blacksmith.cs:78-95`) does not limit deed hunting; accepted by Chase 2026-10-02 | guild members can request deeds as often as they like | `visible` | `cc-P32` B.4, B.5; `p32-decisions-2026-10-02` **Amended cc-P55 H (2026-10-05): a Society member is now paid the guild's way at every smith; regular smiths issue by a Small/Large choice (D-115, D-116).** |
| D-106 | **Ours (F-27).** Self Repair is out of the ordinary random property table for armor, shields and hats; a separate roll gives it to about 1 in 500 magic weapons and armor from high-end sources only (bosses, champions, paragons), intensity mostly 1 or 2; weapons included; never from runic crafting; named artifacts keep their fixed values. The Artificers' imbue sells it only at a high rank and a much higher price (Chase 2026-10-02; to be built) | Self Repair is extremely rare | `visible` | `cc-P32` C.4; `p32-decisions-2026-10-02` |
| D-107 | **Ours (cc-P42 A).** Imbuing offers Self Repair (weapons and armor, 5 to 7 by rank) at Master Artificer (15,000 standing) and above, priced well above every other property (40 Essence Shards and 40,000 gold at the vanilla maximum, scaling with value and rank). OSI's imbuing never adds Self Repair and removes it from any item it imbues. With D-106 it is the deliberate, expensive way to get it | Self Repair is buyable late and dear | `visible` | `cc-P42` A |
| D-108 | **Ours (cc-P42 F, Chase 2026-10-03).** The Society of Smiths' Bulk Order button (guild page, anywhere) and the Smithing Guild Book let the player choose a small or a large order; large needs 70.1 Blacksmithy and no rank (requesting and turning in). OSI picks small or large at random (talking to the Blacksmith Guildmaster still does). Regular smiths unchanged | large deeds on demand | `visible` | `cc-P42` F; `bod-choice-decision-2026-10-03` |
| D-109 | **Ours (cc-P42 G1, Chase 2026-10-03).** The Society's bulk orders and commissions ask only for items whose crafting can still raise the smith's Blacksmithy; past the top of every item they ask for the hardest the smith can make. OSI picks any item the smith can make. Regular smiths unchanged | guild orders always train | `visible` | `cc-P42` G1 |
| D-110 | **Ours (cc-P42 H, Chase 2026-10-03).** A large Smith deed takes crafted items directly, each filling its entry as a small deed of that entry would (type, ore, exceptional), as well as completed small deeds. OSI fills large deeds only by combining small deeds | large deeds are practical | `visible` | `cc-P42` H |
| D-111 | **Ours (cc-P42 J, Chase 2026-10-03).** Trammel Despise runs the revamp only: the pre-revamp creature spawners (ettins, lizardmen, elementals, trolls, ogres, cyclopes) are not placed; its treasure chests stay. Felucca Despise is classic. (Whether OSI's Trammel Despise kept any pre-revamp creatures: unverified) | no old monsters in Trammel Despise | `visible` | `cc-P42` J |
| D-112 | **Ours (cc-P42 K).** A Wisp Orb survives its owner logging out inside Despise (the possessed creature stays linked and returns with them); leaving by foot or magic still dissolves it. ServUO's code dissolves it on logout too, contradicting its own login handler | possession survives a relog | `visible` | `cc-P42` K |
| D-113 | **Ours (cc-P53 C, Chase 2026-10-04).** Item skill bonuses ("Skill +X" on equipment, talismans, set bonuses) and temporary skill effects count above the skill's cap: a +15 item on a capped skill reads cap + 15. Skill gain still stops at the cap, and material requirements still read the unmodified skill. OSI clamps item and Animal Form bonuses at the cap | gear matters at the cap | `visible` | `cc-P53` C |
| D-114 | **Ours (cc-P53 D, Chase 2026-10-04).** Craft menu material names read in Title Case ("Iron", "Dull Copper", "Red Scales", "Leather/Hides") instead of the client's upper-case labels ("IRON", "DULL COPPER"), so they match the shard's own metals and woods. Cosmetic; what each material does is unchanged | consistent craft menus | `visible` | `cc-P53` D |
| D-115 | **Ours (cc-P55 H, Chase 2026-10-05).** Any blacksmith or weaponsmith asked for a bulk order lets the player choose small or large (large at 70.1 Blacksmithy, stock's gate); OSI picks large by a (skill - 40) / 300 roll. The stock timer and the 20% offer on purchase are unchanged | players pick the deed size | `visible` | `cc-P55` H |
| D-116 | **Ours (cc-P55 H, Chase 2026-10-05).** Society of Smiths members' completed smith deeds, at any smith, the guildmaster or the guild book, are banked as Smithing Seals or cashed out for half OSI's gold, its fame and a 1 in 40 chance at OSI's item, by a per-character setting (always bank, default; always cash out; ask). Non-members get OSI's rewards. OSI banks points per craft at a turn-in choice (ServUO `BulkOrderSystem.cs:105-142`); the rates are ours | banking pays more than cash out | `visible` | `cc-P55` H **Amended cc-P56 A (2026-10-05): banking pays the deed's gold value x1.25 at the guild's rate plus the Seal catalog price of the best item OSI's ladder gives for the deed, so banking is worth at least OSI's non-member pay for every deed (918 shapes checked); cash out unchanged.** |
| D-117 | **Ours (cc-P55 B, Chase 2026-10-05).** Ore satchels tiers 2 to 5 smelt every pile near a forge exactly as the forge does, through the forge's own code (ratio, skill check, loss). OSI has no such satchel | convenience only | `visible` | `cc-P55` B |
| D-118 | **Ours (cc-P55 A, Chase 2026-10-05).** Hammer of Hephaestus Metal Familiarity: caps 1,000 (T1) and 2,500 (T2) per metal, each craft a rolled gain (max(0.05, 1 - current/cap)), +3 for exceptional, +1 otherwise | slower, steadier familiarity | `visible` | `cc-P55` A |
| D-119 | **Ours (cc-P56 B, Chase 2026-10-05).** Post-Valorite ores smelt at their metal's tier (Platinum 112.5 .. Celestial 200, `ClusterFMetalTiers`), with the forge's usual 25-point window; stock gives every ore it does not know 50. Harvest stays at 100, so a miner can dig an ore they cannot yet smelt | harder top metals | `visible` | `cc-P56` B |
| D-120 | **Ours (cc-P56 C).** Context-menu labels on stock clilocs that are not the words we would choose: pack mule breed "Use", trash bag "Clean Up Britannia". Reverses when a client cliloc pipeline ships | readable menus | `visible` | `cc-P56` C |

### What the register says about wiki scope

The `visible` rows are the shard wiki's actual table of contents, and they cluster, which is the
useful part. Most of them are not separate problems:

- **Pet Training special abilities** (D-32, D-39, D-51 to D-54, D-57, D-58, D-63, D-65, D-66, D-82)
  are one absent subsystem seen from a dozen angles. P6 in `docs/patch-backlog.md` is the row.
- **Weapon and armour attributes** (D-3, D-21, D-22, D-73, D-74, D-75, D-87) are members missing
  from `AosWeaponAttribute` and `AosArmorAttribute`. P4 is the row.
- **Set mechanics** (D-14, D-15, D-23, D-24, D-26, D-27, D-28) are the set-hook family, Q-038,
  Q-042 and Q-043.
- **Points systems** (D-29, D-30, D-37) are one missing service, S7.
- **Slayer groups** (D-77, D-78, D-86) are entries in two tables.

Which means the wiki debt is smaller than 90 rows suggests: roughly five subsystems plus a tail of
one-offs. That is the whole point of keeping this list.
