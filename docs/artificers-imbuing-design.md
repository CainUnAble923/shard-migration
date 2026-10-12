# Artificers' Order: Imbuing Rework (design)

Status: design settled 2026-10-11 in the Artificers/Imbuing design chat. Feature number assigned by the queue/overseer chat.
Related: recipe gating (cc-P-recipe-gating.md), F-33 mule modules, F-37 commissions, F-40 loot boxes, planned F-42 epic crafting, XmlLevelItems (crafted gear only).

## Core idea
Imbuing is gated by **property and intensity**, not by item. Learned properties are account-wide and kept through loops, like recipes. Formula books are sold by the Artificers' Order for guild currency only, granted by guild rank index (0 to 5). Past rank 5, unlocks come from the 140+ path (quest line, commissions, boxes, bosses).

## Intensity tiers
Every property has four tiers:

| Tier | Cap |
|---|---|
| Basic | about 1/3 of OSI max |
| Refined | about 2/3 of OSI max |
| Full | OSI max |
| Overcharged | past OSI max, scaled for the 200 cap (140+ path only) |

Rule: a property is learned at Basic, Refined comes one rank later, Full two ranks later. When that runs past rank 5, the remaining tier comes from the 140+ path.

| Learned at | Basic | Refined | Full | Overcharged |
|---|---|---|---|---|
| Free (rank 0) | 0 | 1 | 2 | 140+ |
| Rank 1 | 1 | 2 | 3 | 140+ |
| Rank 2 | 2 | 3 | 4 | 140+ |
| Rank 3 | 3 | 4 | 5 | 140+ |
| Rank 4 | 4 | 5 | 140+ | 140+ |

## Property ladder

**Free**
- Resists (all five), stat bonuses, HP/Stam/Mana Increase, the three regens
- Night Sight, Luck, Lower Requirements, Durability, Self Repair
- Lower Reagent Cost, Enhance Potions

**Rank 1: Apprentice Formulary**
- Life, Mana, Stamina Leech; Hit Lower Attack, Hit Lower Defense
- Elemental damage conversion, Balanced, Velocity, Spell Channeling, Mage Armor
- Jewelry +skill bonuses

**Rank 2**
- Hit Magic Arrow, Harm, Fireball, Lightning, Dispel
- Damage Increase, Mage Weapon, Reflect Physical Damage

**Rank 3**
- Hit Area (all five), single slayers
- Hit Chance, Defense Chance, Spell Damage Increase, Lower Mana Cost
- Custom: Bountiful, Mastercraft, Prospector, Butcher's Eye

**Rank 4: heavy-weight mods**
- Faster Casting, Faster Cast Recovery, Swing Speed Increase
- Super slayers, Casting Focus

**Rank 5: Master Formulary (needs guild trial)**
- No new properties. Raises the item budget (default: +1 property slot, so 6; config option for a higher intensity budget instead).

**140+ path (quest line, commissions, boxes, bosses)**
- Properties stock Imbuing cannot place (e.g. Splintering, Reactive Paralyze, Soul Charge)
- Remaining custom properties (below)
- Overcharged tiers

## +Skill properties
- Jewelry skill bonuses use the tiers: Basic +5, Refined +10, Full +15, Overcharged +20 to +25.
- Keep OSI's one-skill-per-group rule.
- New: crafting and gathering +skill on aprons, tool belts and guild gear. Combat skills stay on jewelry.
- Items may push skills past the cap (existing rule). Bonus points never count toward skill gain, so +skill cannot shortcut a loop.

## Custom properties
Limit: one custom property per item. Values below are starting points, all tunable in config.

| Property | Effect | Full value (start) | Unlock |
|---|---|---|---|
| Echo of the Loop | % XP gain for XmlLevelItems and player levels | 10% | 140+ |
| Time Slip | chance on hit to refund a special move's mana and cooldown | 5% | 140+ |
| Shatter | chance on hit to briefly lower target's highest resist | 10% chance, -10 for 5s | 140+ |
| Bond | % companion damage and companion XP | 10% | 140+ |
| Spell Leech | spell damage heals a small % | 5% | 140+ |
| Renowned | % Renown from League commissions and hunts | 10% | 140+ |
| Bountiful | % bonus gathering yield | 15% | Rank 3 |
| Mastercraft | % exceptional chance on crafter gear | 5% | Rank 3 |
| Prospector | % chance at rare finds while gathering (rare ores, woods, hides, gems, imbuing ingredients) | 10% | Rank 3 |
| Butcher's Eye | % bonus monster parts from kills and carving, small chance at a rare part | 20% | Rank 3 |
| Fortune's Favor | improves loot box roll quality tier only, never item count | low cap | 140+, from boxes/bosses only |

- Fortune's Favor: low cap, no Overcharged tier. Gear swapping before earning a box is allowed on purpose (see achievements).
- Custom properties use their own ingredients, proposed as monster parts from League hunts.

## Menu and hints
- Unknown properties and locked tiers are hidden in the imbue menu.
- One hint line per category that has locked properties, pointing to how to learn more (Artificers' rank, 140+ path).

## Unravel and Reinforce
Free for everyone, not gated.

## Mule soul forge (Artificers' mule socket)
- II: Imbue and Unravel with the owner's known list, capped at Refined, no forge success bonus.
- III: full known list up to Full, plus the standard soul forge success bonus.
- Never Overcharged. Overcharged needs a real forge (Queen's Soulforge or an Artificers' hall forge).

## XmlLevelItems
Imbuing does not make found gear levelable. Only crafted gear is levelable (existing rule).

## Achievements
- **Dressed for the Occasion** (hidden): earn a loot box while wearing Fortune's Favor gear equipped within the last 60 seconds. Flavor: "The System notes you changed into your lucky underwear seconds before achieving greatness. The System is not impressed. The System is taking notes." (Earned a loot box with luck gear equipped less than a minute earlier.) Reward: its own loot box.
- **Creature of Habit** (hidden): do it 25 times. Flavor roasts them for making it a routine. (Earned 25 loot boxes with luck gear equipped less than a minute earlier.)
