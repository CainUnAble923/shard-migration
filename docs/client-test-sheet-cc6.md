# Client test sheet: CC6 batches 1-8 and the breath/Incubator follow-up

**What this is.** Eight batches, roughly 70 creatures, the Stygian Abyss boss tier, the Incubator and
the restored dragon breath have all been proved headless and **none has been seen in a client**. The
two content areas that ever did get a client pass, CC9's artifacts and CC4 Despise, each turned up
real defects the build gate had happily passed: the gargoyle leggings missing their kilt section, the
invisible MAKE X label, the Despise teleporters. That is the base rate this sheet exists for.

**Ordered by risk, not by batch.** Tier 0 first: it is five minutes and it can invalidate everything
below it. Stop whenever you run out of time; anything unreached stays on the backlog.

**Recording it.** A tick is enough for a pass. For a failure, what you did and what you saw beats a
diagnosis, every time. "Gargoyle leggings only cover the shin" was worth more than any theory.

---

## Tier 0 — Is any of this reachable at all? (5 min, do this first)

Every batch note ends with the same open question, Q-048: the live world generated its spawners
months ago, and nothing has confirmed the regions these creatures live in are among them. **If a
region's spawners are absent, nothing from that batch appears no matter how correct the port is.**

| # | Check | How | Pass |
|---|---|---|---|
| 0.1 | Ter Mur is populated | Gate to Ter Mur, walk the open ground | Sliths, bouras, kepetch visible. These are the most-placed creatures on the shard (Slith alone caps at 184) |
| 0.2 | The Abyss is populated | Travel into the Stygian Abyss | Fire daemons, lava elementals, goblins |
| 0.3 | The Underworld is populated | Travel to the Underworld | Rotworms, wolf spiders |
| 0.4 | Malas: Citadel and Labyrinth | Both | Citadel: assassins, mages, thieves. Labyrinth: the four named elementals |
| 0.5 | Heartwood and the Twisted Weald | Ilshenar | The seven elders, dryads |

**If any of these is empty**, stop the appearance testing and tell me which. That is a spawner
generation question, not a content question, and it changes what the rest of the sheet is worth.

---

## Tier 1 — The two live defects (10 min)

These affect play today and are not new content.

| # | Check | How | Pass |
|---|---|---|---|
| 1.1 | **MAKE X label** | Open any craft menu, look at the MAKE X entry | The text is visible. Fixed 2026-09-19, **never verified after a rebuild** |
| 1.2 | **New character training** | Make a fresh character, take a New Haven training quest, gain skill | The gap register says this is **blocked by our own change**: ClusterFSkillGain runs 5x and the 26 New Haven quests interact badly. This is the first thing a new family member hits |

---

## Tier 2 — Appearance sweep (15 min, the highest-volume risk)

A wrong body id shows as an invisible creature or a blob. Spawn one of each family rather than all 70.

    [add Slith            [add RuddyBoura        [add Kepetch
    [add LavaElemental    [add SkeletalLich      [add PitFiend
    [add GargoyleShade    [add ClanRibbonPlagueRat
    [add Rotworm          [add WolfSpider        [add ClockworkScorpion
    [add FireAnt          [add AcidSlug          [add MaddeningHorror
    [add ChickenLizard    [add CrystalHydra      [add FairyDragon
    [add WyvernRenowned   [add PixieRenowned     [add Flurry
    [add Medusa           [add SlasherOfVeils    [add StygianDragon
    [add NavreyNightEyes  [add ClanChitterTinkerer

**Look for:** a creature that renders, at a sane size, in a colour that is not default grey. Name
above it reads as a name, not a class. Then kill one or two and confirm the corpse looks right.

**One specific thing worth a hard look:** the Renowned creatures should show **"[Renowned]" as a
title after the name**. Nothing has confirmed that renders.

---

## Tier 3 — New mechanics, the ones with no precedent in this tree (20 min)

Each of these is the first of its kind ported, which is where the defects live.

| # | Check | How | Pass |
|---|---|---|---|
| 3.1 | **Shearing a live boura** | Spawn a `RuddyBoura`, use a bladed item on it while alive | The target cursor **accepts** it, you get one Fur, the message appears, a second attempt is refused. This is the first `ICarvable` port and the signature was adapted from bool to void |
| 3.2 | **Shearing a dead one** | Kill a boura, carve the corpse | **Expect no fur.** That is D-48, a known accepted gap, not a bug. Confirming it looks deliberate rather than broken |
| 3.3 | **The crystal hydra's breath** | Fight one, ideally with a second character nearby | Cold breath, roughly every 5 to 7 seconds, and it should hit **up to five targets at once**. It is the only one of the four with its own definition |
| 3.4 | **The other three breathe** | Slith, toxic slith, fire daemon | Fire breath. These were shipped without it by mistake and restored last week |
| 3.5 | **The Renowned artifact hand-out** | Kill a Renowned creature, having done most of the damage | The artifact lands **in your pack**, not on the corpse. Roughly 15% of kills, so try several |
| 3.6 | **The Incubator, full cycle** | Craft one (carpentry, Other, 100 boards), place and **secure** it in a house, drop a chicken lizard egg in, pour water from a pitcher, wait | The egg advances. Unsecured, it should refuse the egg. This is the longest chain in the batch |
| 3.7 | **Gargoyle cloth artifacts** | On a **gargoyle** character, equip `MantleOfTheFallen` and `SummonersKilt` | Mantle in the inner-torso slot, kilt in the **glove** slot. That glove layer looks like a typo and is not. Check a female gargoyle too: the graphic will **not** swap, which is a known difference |

---

## Tier 4 — The long tail, if there is time

- Kepetch ambusher and trapdoor spider **hide effects**, and whether they reveal on a run.
- An orc scout at range 7 with a bow: does it actually shoot under MeleeAI? Batch 1's goblin scout
  has the same open question.
- The bloodworm's corpse-to-bones swap.
- Medusa: does a knife on a **living** Medusa reach her carve path from a client? And what does the
  paperdoll of a frozen (petrified) clone look like?
- The hybrid treasure chest's crate graphic, lock and trap.
- Sound ids across all batches. Low value: a wrong sound is cosmetic and nobody has a reference.

---

## What a failure is worth

Three of the four defects the earlier client passes found were **invisible to the build gate and to
the headless runs**. The gate proves a thing compiles, constructs, serializes and spawns. It cannot
see a graphic, a layer, a colour, or a target cursor that refuses. That is the entire job of this
sheet, and it is why one afternoon here is worth more than another batch.
