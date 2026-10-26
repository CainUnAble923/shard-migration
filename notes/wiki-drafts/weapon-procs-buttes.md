# Weapon milestones and archery buttes

Player guide draft, October 26, 2026. Checked against merged code, including P647's fixes. This is not a release announcement or confirmation of what the running shard has installed.

Weapon milestones are available only for staff-enabled testing on a test world. The new butte hit pictures are in the source package, but the scoring butte that would use them, its crafting recipes, and its New Haven practice yard are not built yet. Existing ordinary archery buttes already keep scores.

## Weapon milestones at item level 100

A milestone binds one permanent combat effect to a levelable, player-crafted weapon. The threshold is the weapon's item level. Reaching level 100 does not buy the effect automatically.

These are the current defaults. The test settings can change, so read the purchase page before confirming.

| Requirement or effect | Current default |
| --- | --- |
| Eligible item | A crafted, non-artifact weapon already made levelable with a Smith's Seal |
| Unlock | Item level 100 or higher |
| Price | 100 unspent points belonging to that weapon |
| Property cost | One free property slot, with a base limit of five |
| Choices per weapon | One, with no second choice at higher levels |
| Chance | 5% per eligible damaging weapon strike |
| Cooldown after success | 10 seconds, shared with your companions and also kept on the weapon |
| Stormstrike | 12 raw energy damage |
| Emberstrike | 12 raw fire damage |
| Targets | Eligible wild creatures only |

The damage goes through normal resistance and damage rules. Twelve raw damage does not promise twelve lost hit points. The proc's raw damage and chance do not increase with weapon level, quality, material, Luck, or your damage increase bonuses. Stormstrike and Emberstrike have the same default strength and price; their damage types differ.

Armor, shields, jewelry, found weapons, artifacts, and bare hands do not qualify for a weapon milestone. Normal crafted melee weapons, bows, crossbows, and thrown weapons qualify by item type, although ranged and thrown combat still need the broader runtime checks described below.

Under the current progression defaults, a weapon earns 440 points by level 100 before spending anything, and needs 1,020,000 cumulative item XP to reach that level. Points already spent on other properties are unavailable for the milestone. Save 100 points and a property slot if you want one.

## How to buy and inspect an effect during testing

Staff must enable weapon milestones for the test session. They start disabled. A Smith's Seal has no normal player acquisition source in the current code, so obtaining a newly sealed test weapon requires staff help. If staff supply a seal, double-click it in your backpack and target an eligible crafted item you carry or wear. The seal is consumed only on success.

1. Carry or equip your levelable weapon. To buy for a companion, take the weapon back into your own possession first.
2. Type `[ItemLevel` and target the weapon.
3. Open **Weapon milestone**. The page is available before level 100 while testing is enabled and explains any missing requirement.
4. At item level 100 or higher, with 100 unspent points and a free slot, choose Stormstrike or Emberstrike.
5. Read the confirmation and press **Bind it** to pay. **Cancel** leaves the weapon unchanged.

There is no gold or extra consumable charge for binding the milestone. Ownership, eligibility, points, and slots are checked again when you confirm. If the price or unlock level changed while the confirmation was open, nothing is spent and you must confirm the new terms.

The choice stays with the weapon when traded. There is no current replacement, refund, or respec option. Buying at item level 150 still buys the same level-100 milestone. An ordinary Hit Lightning or Hit Fireball property can coexist with it, but remains a separate property with its own chance. It does not add to the milestone's 5% chance.

After purchase, the weapon tooltip names the bound effect and marks it PvE. Its milestone page shows the purchase and your shared cooldown, or an unavailable message when the feature or effect is switched off. The page's cooldown is your timer; a recently traded weapon can still have its own timer even when yours says ready.

## When the effect can fire

Equip the weapon and land a damaging strike on the living wild creature you are currently fighting. It must still be in weapon range, in line of sight, on your map, and legally damageable when the proc is checked. A target killed by the original strike or its ordinary hit effects cannot receive a milestone afterward.

Players, controlled pets, companions, summons, invulnerable creatures, and creatures excluded from normal kill awards are not eligible targets. Spell damage, poison ticks, reflected damage, and damage you receive do not independently roll this weapon effect. Butte practice does not trigger it.

Each eligible strike gets a fresh 5% roll while both cooldowns are clear. A failed roll starts no cooldown. Five percent does not guarantee a success within twenty hits. A successful roll starts both timers before applying its effect, even if later mitigation prevents the extra damage.

You and your controlled companions share one player cooldown. If any of you triggers a milestone, the others wait too, including when using different milestone weapons. A companion can trigger its equipped weapon only while its owner is alive, online, on the same map, and within 18 tiles. Ordinary pets and summons cannot trigger milestones.

Changing weapons does not clear your timer. Trading the triggering weapon does not clear its timer for the next wearer. Cooldown deadlines are saved as real times, so elapsed downtime counts toward the wait. Full world restart behavior still awaits a hands-on acceptance check.

## Current testing limits

The planned rule that makes a proc dormant when the wearer's acting level is too low is not implemented. Current testing checks item level when buying, without a wearer-level or Arms Lore activation requirement. Do not rely on the design's proposed loop-reset dormancy yet.

The item-level menu counts the milestone as a property slot, including while disabled. The imbuing menu does not yet share that accounting, and the planned intensity reservation is absent. This unfinished interaction is a reason the feature remains restricted to testing.

Ranged and thrown hits follow the shared combat path in source, but runtime coverage beyond the tested melee path, special-move interactions, client visuals, full world restart behavior, and combat balance still need acceptance work. The temporary staff enable switch is not saved across restarts; a saved purchase does not enable the feature by itself.

## Using an ordinary archery butte now

These are the existing butte rules. They do not require the new hit pictures.

Equip your own bow or crossbow and put matching arrows or bolts in your backpack. Stand exactly 5 or 6 tiles in front of the target, directly in line with it, then double-click it. For an east-facing target, stand east of it on the same row. For a south-facing target, stand south of it on the same column. Four tiles is too close; seven is too far.

The butte accepts at most one shot every 2 seconds, shared by everyone using that target. Each accepted shot consumes one piece of ammunition, including a miss or split. Refused clicks consume no ammunition and do not start the delay.

The default skill check runs from -25 to 25 using the equipped ranged weapon's skill. At effective Archery 25 or higher, an ordinary bow or crossbow passes this check without further training from that window. Buttes are basic practice, not a way to train high Archery.

After the skill check succeeds, the ring is selected separately:

| Result | Chance after passing the skill check | Ordinary score | Split score |
| --- | --- | --- | --- |
| Bullseye | 10% | 50 | 100 |
| Inner ring | 15% | 10 | 20 |
| Middle ring | 25% | 5 | 15 |
| Outer ring | 50% | 2 | 5 |

A failed skill check misses for zero points but still counts as a shot. The ring percentages are not your overall hit chance.

Each ordinary hit stores one arrow or bolt for recovery. A miss or split stores none. On a successful hit, the split chance is 2% for each arrow or bolt already stored in that butte, reaching certainty at 50 stored projectiles. A split does not remove a previously stored projectile.

Walk within one tile and double-click to collect stored arrows and bolts. Anyone nearby can gather the shared ammunition, which clears every shooter's score on that butte. Gathering does not clear the shot delay. Scores also reset when the server process restarts; saved ammunition counters persist. An ordinary butte with no stored ammo has no close-click score-reset feature. Scores award no prizes, gold, or item XP.

The existing Clean Up Britannia reward remains an ordinary archery butte deed costing 80,000 cleanup points. The new scoring deed is not available through that reward or Carpentry.

## What the new butte pictures do today

P632 prepared arrow and bolt pictures for the bullseye, inner, middle, and outer rings, plus misses, in east and south facings. Current gameplay does not switch a butte to those pictures.

The scoring component, east and south house deeds, crafting, New Haven placement, tutorial-loan protections, and empty-ammo close-click reset remain future work. There is no new public practice range or craft recipe to follow from this draft. Ordinary butte practice does not complete the tutorial bow lesson; that lesson still uses its echo target.

Source and verification details: [P655 working notes](../cc-P655-guide-weapon-procs-buttes.md).
