# P41 companions research: review (2026-10-03)

Review by the companions design chat of `D:\UO\shard-migration\notes\cc-P41-companions-research.md` (638 lines,
written 2026-10-02 22:34 against pinned **d4531cd94**, post P38 upgrade). Design source:
`claude/companions-squire-evo-research.md` and `claude/companions-combo-lines.md`.

## Verdict

**Engine research: sound. Design side: blind.** CC could not read the two design docs (they live only in the
claude.ai project, not on disk), so every design-shaped proposal in P41 (section 7.3 tables, section 10 build order,
section 9 questions) is written against guesses. The engine findings stand; the plan needs a correction pass before
any build prompt.

**Spot-checked 8 claims against pinned d4531cd94, all hold:** `PetOrders.cs:37-39` (follow, come, stay are stand-down
orders), `AITimer.cs:149` (controlled runs `Obey()`, not `Think()`), `SamuraiSpell.cs:28-29` (Bushido needs a
`PlayerMobile`), `SkillCheck.cs:140-143` (controlled pet gain x2), `AIType.cs` (10 values, no `AI_Paladin`),
`Spell.cs:260-263` (non-players skip reagents), `BaseWeapon.cs:2430-2437` (`SetDamage` overrides the weapon),
`HealerAI.cs:138` (heals only same-`Team` creatures).

**Process fix for next time:** put the design docs on disk where CC can read them (for example
`D:\UO\shard-migration\docs\companions\`), and say so in the prompt.

## Findings that change or confirm the design

| # | Finding (P41 section) | Effect on design |
|---|---|---|
| 1 | No pinned AI for healer, bard or stealth rogue; controlled pets on follow never fight back (3) | Every class needs our own `ForcedAI` (pattern exists: ours `DespiseMeleeAI`). **Support, Troubadour and Rogue are the risky paths**; P41 B7 may "decline" bard or rogue if probes fail. That would gut 1.5 of 5 paths, so probes should run early, not in B7. |
| 2 | Bushido is player-only (2.4) | **Blademaster** (and Sharpshooter if it uses Bushido) needs a pinned patch. Required, not optional. |
| 3 | Creatures cast with no reagents and cannot be disturbed (2.4) | Breaks "same math as a player" for Arcane and Support. Chase's call: patch, or accept as a deviation. |
| 4 | Parity needs about 4 pinned patches: pet gain x2, pet stat delay 5 min, Bushido, resurrection loss (2) | Chase decided full parity (16:49), so these are build items, not options. Add #3 above as a fifth. |
| 5 | A companion past 700 total skill falls to the gain floor unless it gets the player `Skills.Cap` (2.1) | B1 must set it. Matches F-12 (58 x max level). |
| 6 | Companion record on the creature itself (2.5) | **Matches the decision**: companion keeps its rank and loops on its own when the owner resets. |
| 7 | Rooms: our own registry, not stabling (6) | **Matches** "Room attendant kept, stabling inhumane". Reusing stabling would expose companions at Animal Trainers. |
| 8 | Logout behavior undecided (6, 9.1) | **Open, for Chase.** Proposal: companions log out with their owner (vanish and return at login), never auto-stabled. |
| 9 | Ethereal and real mounts work by code; nothing dismounts a pet rider (5) | Mount-follows-owner is ours to write; small (B8). |
| 10 | `ShrunkPet` cannot shrink a companion-mastered mount, and has 2 defects of its own (5.3) | The defects (follow order lost on restore, follower count drift after restart) also hit Beastcraft's Shrink Potion. **Route to the overseer as defects now.** |
| 11 | Lore gump `OnResponse` never re-checks ownership (1.2) | Security bug in the source; B4 must add the owner check. Good catch. |
| 12 | Steal, peace on players, loot ignoring notoriety (1.5) | Consistent with the design: Rogue has no Stealing; Troubadour should target monsters only; auto-loot "keep with care" means **respect notoriety and looting rights**. |
| 13 | Lineage needs a never-reused `LineageId`, not a serial (8) | Adopt. Add to the breeding-readiness fields. |
| 14 | Source does not compile on stock ServUO either (1.1) | Confirms "rewrite that borrows behavior". |

## Corrections P41 needs (it could not see the design)

1. **Section 7.3 `personality.json`:** rolls by "contract tier" with placeholder personalities (Steady, Gruff,
   Zealous, Cunning). Design: nine personalities (7 common, Gloomy rare 5%, Isekai'd extra rare 1%); **the buyer picks
   a path contract and the personality rolls from those allowed on that path**. Per-path odds are in the design doc.
2. **`classes.json`:** design has 5 paths x 2 branches + Penitent (Gloomy) + Otherworlder (Isekai'd), gendered titles,
   and a personality-to-path map (each common opens 2 paths; rares open all 5). Path is chosen at purchase; branch at
   loop 3.
3. **`speech.json`:** needs a **class/branch dimension** too, for the 50 personality x branch epithets and lines in
   `companions-combo-lines.md`. Epithets show in the lore window or as a title, not in the name.
4. **`party.json`:** design is party of 6 incl. player, per-companion slot cost 1/1/2/2/3/3 by loop, companions and
   pets **share** `FollowersMax`. Design's draft `FollowersMax` at max level 50 is 2, **below stock 5**; reconcile
   (likely raise the floor so a new player keeps a pet or mount).
5. **B4 hiring:** two sources, a **League vendor** (path contract) and a **board of candidates** (name, gender, path
   shown; personality hidden).
6. **B10:** P41 ports the 26 training contracts as-is. Design **reworks** them into **Drill Orders** (faster gain up to
   previous peak or cap, never past). Instructors become **5 League class trainers** (one per path), not 4 instructors
   plus a representative.
7. **Pigeon:** design reworks it as courier letters with a travel delay; P41's required checks (owner, travel, combat,
   cooldown) fit that.
8. **Penitent and Otherworlder mechanics** (damage share, cheat death, cheat skills) were not researched; they need a
   probe pass of their own, plus the shared cheat-death cooldown.

## Decisions (Chase, 2026-10-03 07:25)

1. **Logout:** companions log out with their owner.
2. **Spell parity:** free casting for now (recorded deviation).
3. **Probe early:** yes, the risky classes are probed before any build.

## Suggested next steps

1. Overseer: log the two `ShrunkPet` defects now (they affect Beastcraft too).
2. ~~Copy both design docs to disk for CC.~~ Done 2026-10-03: `D:\UO\shard-migration\docs\companions\`.
3. A short probe prompt (notes plus throwaway test code only): the unverified items in P41's list, especially healer,
   bard and stealth on a creature, and the abandoned-pet versus registry load order.
4. Then a B1 build prompt with the corrections above folded in.
