# Fidelity principle: port faithfully, so the existing wikis do our documentation

## The reasoning

The shard should run content players can look up **outside** a custom wiki. Twenty years of
UOGuide, Stratics, uo.com and forum knowledge already documents standard content. Every
system we run that matches OSI behaviour is a system nobody has to write documentation for.

This is the strongest argument for the "all newer content" scope. It is not about having more
things; it is about the shard being **legible to a new player without us explaining it**.

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
When we do deviate — and we will, this is our shard — it goes in a running list so a custom
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

## Four entries below are withdrawn, 2026-09-21

**D-55, D-56, D-62 and D-68 are not deviations and never were.** Each recorded
`SetSpecialAbility(DragonBreath)` as a Pet Training loss on `Slith`, `ToxicSlith`, `FireDaemon` and
`CrystalHydra`. Pinned ModernUO has the ability as `MonsterAbilities.FireBreath` from
`BaseCreature.GetMonsterAbilities()` (`:1131`), with `ColdBreath : FireBreath` for the cold variant,
and CC4 had already used it. The four creatures are on the shard fighting wrong until the follow-up
lands; **they are defects to fix, not deviations to accept**. Q-054 has the decision,
`docs/bug-list.md` §1b has the cause. Leave the rows in place until the fix ships, then strike them.

## Deliberate deviations

Every entry gets a date, the task that made it, what a player would notice, and what would
reverse it.

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
    Ter Mur `(1121, 957, -42)`, and it is a small follow-on task.
  - **ServUO's two unreachable reward cases are ported unchanged** rather than "fixed". Correct
    under "port unchanged": upstream dead code stays dead code, and quietly repairing it would be
    an undocumented divergence from every wiki that describes the fountain.

