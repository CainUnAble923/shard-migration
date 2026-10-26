# Item Identification: Appraisal and Arms Lore

Draft checked against merged source on October 26, 2026. P627 ships this feature **disabled**. The rules below describe its first stage when staff enables it for testing. They do not announce a live release. The running shard's setting and the display in a real client have not been checked.

Appraisal discovers an item's magic. Arms Lore discovers its resistances, damage types, and physical condition. Each skill reveals its own information, and discoveries belong to the item: everyone sees what has been learned, including a buyer or another character with lower skills.

## Which items need identification?

With the feature enabled, weapons and armor produced through the covered monster-loot generator start unknown. Shields qualify as armor. This does not cover every monster reward or every source of magic equipment.

Existing equipment keeps its ordinary tooltip. The separate crafting, vendor-stock, loot-box, and quest-reward routes do not mark their output unknown in this stage. This includes runic crafts. Staff can deliberately mark an eligible item unknown. Jewelry, clothing, hats, spellbooks, and slayer instruments do not have their own identification support in this stage.

An unknown item keeps its visible art and hue, but its tooltip uses a plain item name instead of its special name. It includes:

```text
Unidentified
Resistance and condition: uninspected
```

Basic details such as weight, handedness, and required weapon skill can still appear. The effective strength requirement is hidden if it would reveal an unknown Lower Requirements enchantment. The current version does not replace it with a base requirement.

## How to use the skills

1. Use **Appraisal** from your skills list or an ordinary skill macro, then target the item. Its target range is eight tiles. The skill may still be called **Item Identification** in a client without the shard's name override.
2. Read the message and hover over the item again. A successful discovery updates its tooltip.
3. Use **Arms Lore** and target the same gear to inspect the other side. Its target range is two tiles. Either skill can be used first.

Using the skill costs no gold or reagents. Appraisal allows one managed-item attempt per character per second, across all items. Retrying too soon says, "You must wait a moment before appraising another item."

### Appraisal: magic traits and values

These thresholds use your effective skill, including applicable bonuses.

| Appraisal | What an attempt can reveal |
| --- | --- |
| Below 30.0 | "You sense magic, but cannot identify it." No discovery. |
| 30.0 to below 60.0 | On success, the names of magic traits, with their values still hidden. |
| 60.0 and above | On success, exact magic properties. A partial success can reveal only the trait names. |

The named stage can show `Appraised traits: hit life leech, swing speed increase, slayer` followed by `Magic values unknown`. The word `slayer` at this stage does not identify its specific slayer title. If the item has no magic lines assigned to Appraisal, it instead says, "Appraised: its magic concerns resistance; Arms Lore can measure it."

Appraisal covers bonuses such as Damage Increase, Swing Speed Increase, hit spells, leeches, stat and skill bonuses, luck, slayers, Self Repair, magical durability bonuses, and Lower Requirements. It does not measure physical durability, armor resistances, weapon damage percentages, or ordinary weapon damage and speed.

Failures say, "You cannot determine more." They remove no previous discovery. That message can also mean your skill cannot reach the next stage. Once the magic values are known, another attempt says, "Its magic is already known."

### Arms Lore: resistances and condition

Arms Lore must first pass its ordinary inspection check. The new information then follows your effective skill:

| Arms Lore | What a successful inspection adds |
| --- | --- |
| Below 30.0 | Ordinary inspection messages, with no new tooltip discovery. |
| 30.0 to below 60.0 | An `Inspected:` list of resistance, damage, and condition traits, followed by `values not measured`. |
| 60.0 and above | Exact supported resistance and condition values. |

This side includes physical, fire, cold, poison, and energy resistances; weapon damage percentages; ordinary weapon damage, speed, and range; current and maximum durability; Reflect Physical Damage; and poison charges where present. Learning these does not reveal leeches, slayers, or other Appraisal traits.

**Inspecting your own damaged gear can also perform field maintenance.** This existing Arms Lore feature applies to gear in your backpack or worn by you. It restores `2 + floor(Arms Lore / 10)` durability, up to the maximum, using effective Arms Lore capped at 200. It can be used once every ten seconds. Before restoring durability, it can cost one maximum durability point: 25% chance at 100 skill, falling to zero at 200. That maintenance cooldown does not prevent the separate identification discovery after a successful inspection. Appraisal does not perform maintenance.

## Why a 60-skill appraiser can still fail

The thresholds unlock stages; item difficulty determines success. Each Appraisal attempt uses one random roll for all reachable stages, rather than a separate roll for every property. At 60 or higher, that roll can learn both names and values at once, learn only names, or learn nothing.

The current calculation is:

```text
D = round(15 x counted properties + 0.75 x strongest intensity percent)
```

D is limited to 10 through 175. It uses the current imbuing/requisition property readers, which do not count every supported enchantment. Do not assume the visible number of tooltip lines is the property count.

For names, the stage difficulty is D minus 60, with a minimum of zero. For values, it is D. Each stage has a 50-point success window:

| Effective Appraisal compared with the stage difficulty | Chance |
| --- | --- |
| 25 points below or lower | 0% |
| Equal | 50% |
| 25 points above or higher | 100% |

The stage's 30 or 60 skill floor still applies. Chances rise evenly between those points.

For example, the build's sample sword has Hit Life Leech 20, Swing Speed Increase 10, a Silver slayer, and 20% fire damage. Its calculated D is 135. At 59 Appraisal, its names have an 18% chance. At 100, its values have no chance. At 135, values have a 50% chance; at 160, they are certain. Arms Lore measures the fire damage separately. These are calculations for that sample, not a promise about every slayer weapon.

## Keeping and sharing discoveries

You can ask another player to appraise or inspect a difficult find. What they learn is public on that item and stays with it when it changes hands. A failed or lower-skill attempt never lowers its discovery stage. The server saves both stages.

When magic values and Arms Lore measurements are both known, the item returns to its ordinary full tooltip, including its normal name. If staff disables the feature, ordinary tooltips return while discovery records are retained.

## Training and current limits

Appraisal attempts on items managed by this feature grant **no Appraisal skill gain** in this stage. Ordinary identification on other items keeps its existing behavior. Arms Lore retains its existing inspection and training checks; the new discovery adds no extra gain roll.

Creature Appraisal remains available through the same skill. It gives a rough comparison below 30, adds creature level at 30, stats and resistances at 60, and a creature stat card at 90. Those reports follow skill thresholds rather than the item's difficulty roll. Creature Appraisal remains a training route, including its existing harder-creature progression above 100.

There is no item report card or advanced hazard stage at 90 yet. Identifying an item does not certify it free of curses or traps, and Appraisal does not open or disarm containers.

The League Appraiser still offers its existing price quotes and purchases. Paid magic identification and paid arms inspection have not been added. Identification wands still use their old identification flag; they do not advance these new discovery stages.

The test version also leaves other information routes unfinished, including some shop and trade displays, legacy labels, price breakdowns, requisition messages, and imbuing screens. Extra custom tooltip lines can appear when both tracks complete, and equipment changes do not yet reset the affected discovery stage. Treat this as a guide to the disabled first stage, pending the remaining work and client checks.
