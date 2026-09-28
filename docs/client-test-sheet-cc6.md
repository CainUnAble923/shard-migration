# Client test sheet: CC6 batches 1-8 and the breath/Incubator follow-up

**What this is.** Eight batches, roughly 70 creatures, the Stygian Abyss boss tier, the Incubator and
the restored dragon breath have all been proved headless and **none has been seen in a client**. The
two content areas that ever did get a client pass, CC9's artifacts and CC4 Despise, each turned up
real defects the build gate had happily passed: the gargoyle leggings missing their kilt section, the
invisible MAKE X label, the Despise teleporters. That is the base rate this sheet exists for.

**Ordered by risk, not by batch.** Tier 0 first: it is five minutes and it can invalidate everything
below it. Stop whenever you run out of time; anything unreached stays on the backlog.

**Recording it.** A tick is enough for a pass. For a failure, **name the item**, say what else was worn, and say
what you expected. What you did and what you saw beats a diagnosis every time, but a phrase without an item name is
not a defect report. "Gargoyle leggings only cover the shin" sat open for over a week and sent an agent hunting a
layer bug that did not exist: the legs were correct and the kilt is a separate garment (Q-061, closed
2026-09-27 as **not a defect**).

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

## The New Haven training board and its quest menu: passed in a client, 2026-09-26

Chase, on the test shard (`-Fresh` world, Owner character, `sl-modernuo:picker`). **Eight of nine
checks passed, none failed.** These were the only things the gate could not see, so this is the pass
that mattered.

| # | Check | Result |
|---|---|---|
| B.1 | `0xA0C5` draws as a free-standing bulletin board, not a wall fixture floating in the open | **pass.** The reason it was chosen over the three other candidates, unverified until now |
| B.2 | Double-click from the ground opens the menu | **pass** |
| B.3 | A row's button reaches the stock offer gump, and the quest can be accepted | **pass.** The whole pick path, previously proved only in bytes |
| B.4 | At ten held, the eleventh row reads "No room: 10 held" and the header counts | **pass.** One of the two states CC added beyond the five asked for; stock would have shown a bare 1080107 with no reason |
| B.5 | A skill past 50 shows "Past 50: gone" | **pass.** The lockout, which is the board's whole reason to exist |
| B.6 | **Label clipping** in the 125 px quest-title labels | **pass, 2026-09-27.** Screenshot of a full 13-row page: every title renders complete. Worst case is "Becoming One with the Shadows", which clears the "Past 50" column with roughly fifteen pixels to spare. "Bruises, Bandages and Blood" and "Channeling the Supernatural" have more room than that. The skill column is not close: "Blacksmithing" is the longest and fits easily. **No headroom left on the title column**, so any future quest title longer than "Becoming One with the Shadows" will clip |
| B.7 | **The five tooltip lines**, none truncated, line 4 exact | **pass on our five, with a finding.** Screenshot 2026-09-27: all five of our lines render in full and line 4 reads "Double-click For All 26 Quests. Take The Ones You Want.", exactly as specified. **But the tooltip carries seven property lines, not five.** "Quest Item" and "Quest Giver" are added ahead of ours by the base class, not by us. TazUO renders all seven without complaint, and the family package ships TazUO, so this is not a live problem. It does mean the five-line budget in the design note was two lines short of what the object actually emits, and **there is no room to add a sixth line of ours.** Anyone testing this on EA's own classic client should re-check it there. Separately, the Title Case in the tooltip is **the client's, not ours**: the same name renders "New Haven training board" in the gump and "New Haven Training Board" in the tooltip. Do not "fix" the capitalization in our source |
| B.8 | **Turn-in at the board**: finish a quest and double-click the board | **pass, partially.** Chase completed a quest and reported turning it in at the board on 2026-09-26, so the second half of the loop works through a client. **Not confirmed:** that the row then reads "Done" rather than "Past 50". Worth one glance the next time someone holds a finished quest, because that row state is CC's addition, not stock |

**Still unchecked on the board, and worth ten minutes when someone is next in game:**

| # | Check | Why it is still open |
|---|---|---|
| B.9 | **Reach from the arrival tile without walking.** Spawn a new character and double-click without stepping | The entire placement argument. Proved in a headless range check, not in a client |

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
