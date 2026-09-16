# Client test sheet — run this at the keyboard

Companion to `client-check-backlog.md`, which says *why*. This says *what to type*.
Tick as you go. Anything that fails, write the line under **Findings** at the bottom;
that is what comes back to me.

**Covers 381 ported files.** Tier 1 is about ten minutes and settles the only two
things where we overrode the source on our own judgment. Everything after that is
sampling, so stop whenever you have had enough and the sheet still has value.

---

## 0. Setup

- [ ] Bring up the **throwaway test container**, not `sl-modernuo`. `build.sh` makes the image.
- [ ] `Play-SL-Admin-TEST.bat` (points at 127.0.0.1).
- [ ] Make a **gargoyle** character. Most of CC9 is gargish equipment with a race gate;
      on a human it reads "you cannot wear that", which is correct and looks like a bug.
- [ ] `[add` needs GM. Confirm you can spawn: `[add dagger`

---

## 1. Tier 1 — the two calls that were ours, not ServUO's

ServUO's values here looked like typos and we overrode them. A client is the only proof.

- [ ] `[add GargishWarHammer` — equip, flip it (drag to paperdoll / use the flip).
      **Pass:** it still looks like a war hammer.
      **Fail:** it turns into a stone pillar. Then D-10 is wrong and ServUO's `0x481` was right.
- [ ] `[add DarkwoodCrown` — equip, flip it.
      **Pass:** still a crown.
      **Fail:** it turns into a vulture helm. Then D-16 is wrong.

---

## 2. Tier 2 — the types whose parent we changed

Re-parenting onto a set carrier means the stock parent's members were rewritten by hand.
Batch 3 got exactly this wrong once and batch 4 caught it, which is why this tier exists.

- [ ] `[add GargishBattleAxe` — **the one that actually broke.**
      **Pass:** two-handed, axe swing sound, and it will **chop a tree**.
      **Fail:** one-handed, sword sounds, or no harvest option.
- [ ] `[add GargishDagger` — double-click should give a carving target.
- [ ] `[add LeatherTalons` — goes on the footwear layer, correct art.
- [ ] `[add BearMask` — headwear, wearable.
- [ ] `[add HumilityCloak` — cloak layer.
- [ ] `[add SorcererHat` / `[add VirtuososCap` — hat layer, not a generic item.
- [ ] `[add GargishKiteShield` — shield, blocks, correct art.
- [ ] `[add GargishPlateArms` / `[add GargishPlateKilt` — correct layers on a gargoyle.
- [ ] `[add DragonTurtleHideChest` (and `Arms`, `Bustier`, `Helm`, `Legs`) — armor, correct art.
- [ ] `[add Feathernock` — quiver, equips to the correct slot.

---

## 3. Tier 3 — sets completing

The newest mechanism on the shard. Equip every piece, watch for the set bonus and the
"part of a set" lines.

- [ ] **Marksman (2)** — `Feathernock`, `Swiftflight`.
      **Priority: this is a brand new shape.** Swiftflight is a Bow implementing the set
      interface directly rather than deriving from a carrier. Nothing else on the shard
      works this way.
- [ ] **Darkwood (6)** — `DarkwoodChest DarkwoodCrown DarkwoodGauntlets DarkwoodGorget DarkwoodLeggings DarkwoodPauldrons`
      (also re-checks the tier 1 crown flip in context)
- [ ] **Darden (5)** — `DardensBustier DardensHelm DardensLegs DardensSleeves DardensTunic`
      **Expect NO "Myrmidex Slayer" line.** That is D-26 and it is deliberate.
- [ ] **Virtuoso (7)** — `VirtuososArmbands VirtuososCap VirtuososCollar VirtuososEarpieces VirtuososKidGloves VirtuososNecklace VirtuososTunic`
- [ ] **Bestial (7)** — `BestialArms BestialEarrings BestialGloves BestialGorget BestialHelm BestialLegs BestialNecklace`
      **The set bonus should apply. The set should NEVER rage, hue-shift or block heals.**
      That is D-14 and it is expected until the hooks row lands.
- [ ] **Aloron (8)** — still unverified since S1/S6.
      Completed set eats cold damage as a **capped delayed heal about three seconds after
      the hit**. Watch health recover; do not watch for a smaller damage number.

Other sets exist and are lower value: Knights (10), Scout (9), Sorcerer (8), Virtue (6),
Paladin (6), Myrmidon (6), Initiation (6), Necromancer (5), Grizzle (5), Mage (4),
Hunter (4), Assassin (4), Acolyte (4), Juggernaut (2), Luck (2), Luck2 (2).

---

## 4. Tier 4 — the wide sample

Fifteen or twenty, spread out. Looking only at art, hue, and whether the property list
reads sanely.

- [ ] Weapons: `[add OrcishBow` `[add PaladinSword` `[add StoneWarSword` `[add GargishScythe`
- [ ] Jewelry: `[add BlueDiamondRing` `[add FireRubyBracelet` `[add WhitePearlBracelet`
- [ ] Armor/shields: `[add LargePlateShield` `[add AssassinsCowl` `[add EvilOrcHelm` `[add MagesHood`
- [ ] Artifacts: `[add VoidInfusedKilt` `[add DragonHideShield` `[add StoneDragonsTooth` `[add Pincer`
- [ ] Costumes: `[add ZombieCostume` `[add DrakeCostume` — then **take damage while wearing one**.
      **It should stay on.** ServUO knocks it into your backpack; we do not (D-5).

---

## 5. The oldest item on the list

- [ ] **MAKE X button label is invisible.** Open a craft gump, find the MAKE X button.
      The button works and sits in the right place; the label is invisible because the
      patch passes an RGB555 color where `AddLabel` wants a hue index.
      **This affects the live shard today**, not ported content. Confirm it and it is a
      one-line fix.

---

## Known missing — do NOT report these

All deliberate, all logged, most already costed:

| What you will not see | Why |
|---|---|
| Soul charge on `GargishSignOfChaos`, `HumanSignOfChaos`, `MysticsGuard` | D-21, member absent from ModernUO's enum |
| Hit-lower-defend on the three mace-and-shield head pieces | D-22 |
| `DespicableQuiver`'s resistance and Archery +5 | D-23 |
| Epiphany burst and its "Set Ability" lines (12 Villainous pieces) | D-24, hooks row |
| Bestial rage, hue shift, heal block | D-14, hooks row |
| Anything after "Your luck just improved!" from the Tenth Anniversary Sculpture | D-28, hooks row |
| `FirstAidBelt` speeding up bandages | D-27 |
| Self-repair on any completed **weapon, clothing or shield** set (armor sets do work) | Q-038, hooks row |
| "Myrmidex Slayer" on the Darden set | D-26 |
| Fountain of Fortune anywhere in the world | nothing places one; Q-021 has the coordinates |

---

## Findings

Write anything that failed here, one line each. Item, what you expected, what you saw.

