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

## Deliberate deviations

Every entry gets a date, the task that made it, what a player would notice, and what would
reverse it.

- **2026-09-06, F3.** `SmithBOD-PostValorite.patch` split into
  `SmallSmithBOD-PostValorite.patch`. Content unchanged; the `LargeSmithBOD` half was dead
  because that file is replaced wholesale. Renamed because the old name implied both files.
  No behaviour change.

- **2026-09-06, P2.** `LuckyCoin` ported without its `OnDoubleClick`. ServUO's coin is
  double-clicked at a `FountainOfFortune` to trade for Stygian Abyss rewards. ModernUO has no
  Fountain, and porting it pulls in `EnchantedEssence`, `GemologistsSatchel`, `RelicFragment`
  and `SolesOfProvidence`. That is a subsystem, which we decline.
  **What a player notices:** the coin drops correctly and stacks, and double-clicking it does
  nothing rather than saying "That is not sacred waters."
  **Why here and not in the creature:** twelve `Mobiles/Normal` creatures drop this coin. Putting
  the deviation in the item keeps all twelve creatures' loot tables faithful, which is what a
  player checks against UOGuide. Dropping the `OnDeath` override instead would have put the
  deviation in the loot table, where it is visible and wrong.
  **Reversal:** one file. If the Fountain is ever built, restore the `OnDoubleClick`.
