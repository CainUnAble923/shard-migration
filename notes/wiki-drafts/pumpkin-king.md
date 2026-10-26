# Pumpkin King Halloween event

Player guide draft, checked against the merged source on October 26, 2026. Live availability, settings, and the entrance route have not been checked in a game client.

Treasures of Sorcerer's Dungeon is a shared Halloween dungeon event on Ilshenar. Fight through a rotation of nine bosses ending with Jack the Pumpkin King, collect equipment of Enchanted Origin, and trade unwanted pieces to the Researcher for rewards.

## Where and when

The default annual season runs **October 24 through November 2, inclusive**, using the server's local date. The checked deployment files default to US Central time. Automatic checks run on world load and hourly, so opening and closing need not happen exactly at midnight. Under these defaults, closing happens on the first check on November 3. Staff can change the schedule or switch the event on or off.

The entrance to **Sorcerer's Dungeon on Ilshenar** is listed at **546, 455**. The Researcher stands nearby at **536, 456**, among pumpkins and flaming scarecrows. His personal name varies; look for **Artifacts of Enchanted Origin Trader**.

Bring healing supplies, cures, a carving tool, backpack space, and allies. There is no separate event quest or entry fee in this implementation. No tested party size or completion time is available.

## Work through the rooms

1. Find the room where event creatures are appearing. The regular enemies are zombies, skeletons, gargoyles, liches, and lich lords.
2. Defeat **80 of the current room's event creatures** to bring out its boss. This is one shared count for everyone, not 80 kills per character.
3. Defeat the boss. After a pause of **one to three minutes**, spawning begins in the next room.
4. After Jack, the rotation returns to the first room. You can join a rotation already underway.

| Order | Boss | Hit points |
| --- | --- | ---: |
| 1 | Nightmare Fairy | 8,000 |
| 2 | Jack in the Box | 8,000 |
| 3 | Headless Elf | 8,000 |
| 4 | Abominable Snowman | 8,000 |
| 5 | Twisted Holiday Tree | 8,000 |
| 6 | Rabid Reindeer | 8,000 |
| 7 | Garish Gingerman | 8,000 |
| 8 | Stocking Serpent | 8,000 |
| 9 | Jack the Pumpkin King | 26,000 |

The event maintains up to **15 regular creatures in the current room**. More can appear during the boss fight, and survivors can remain in earlier rooms. Fifteen is not a limit on all enemies in the dungeon. Earlier rooms' survivors and undead hatched from Jack's pumpkins do not advance the current room's count. Ordinary dungeon creatures can qualify for artifact awards without advancing that count.

## Fighting Jack

Jack casts Magery and Necromancy spells. His base melee damage is **22-26 physical damage**. His resistances are physical, fire, and cold **70-80%**, poison **60-70%**, and energy **40-50%**. He is immune to poison through Deadly. Energy is his lowest resistance, though that alone does not establish the best strategy for every character.

When you damage Jack, he retaliates against the attacker with a pumpkin effect and a separate **8-20 physical damage roll**, before mitigation. This is not a percentage of the damage you dealt. Keep healing available even when attacking from range.

Each retaliation has a **5% chance** to attempt to place **one to three unholy pumpkins** around the attacker one second later. Blocked tiles can prevent placement. Event pumpkins land only inside Sorcerer's Dungeon on Ilshenar, while Jack is still the living event boss and the attacker is alive inside the dungeon.

Unholy pumpkins hatch into undead after **five to ten seconds**. Use a carving tool on a pumpkin before it hatches. Each attempt has a **30% chance** to destroy it and leave **25-100 gold on its tile**. A failed attempt only gives a message and does not stop the hatch. The resulting undead include liches and lich lords, so deal with pumpkins promptly.

## Earning equipment of Enchanted Origin

While the event is enabled, a qualifying creature killed **inside the Sorcerer's Dungeon region** can award equipment of Enchanted Origin. You must be alive and have earned looting rights. Each eligible character gets a separate roll. Merely standing nearby does not qualify, and killing a tamed or summoned creature does not earn this currency.

There is **no guaranteed artifact per boss or per rotation**. Your personal hidden tally grows with qualifying kills. Higher creature Fame and your Luck increase the amount added. The chance is evaluated after adding the kill, and the tally resets when you receive an artifact.

For reference, the formula gives about **0.0863% at a tally of zero**, **1% at 250,000**, and **11.5832% at 500,000**. These are examples of the hidden tally, not reward points or fixed chances for particular monsters. They do not promise a number of kills to the next award.

Awards go directly to your **backpack**, with a message and sound. If the backpack cannot hold the item, the game tries your **bank**, then places it **at your feet** if neither can hold it. Keep space free and watch the award message.

You can keep and use the equipment or redeem it. The current pool produces weapons, armor, shields, jewelry, and hats; the planned expansion to Stygian Abyss equipment is still pending. Renaming or dyeing unrelated equipment does not make it redeemable.

## Turn artifacts into points

Reward points belong to the **character** who turns in the artifact. They are separate from the hidden kill tally.

1. Put the artifact directly in your backpack, outside any inner bag. The turn-in menu only lists items at the top level.
2. Stand within **two tiles** of the Researcher and open his context menu. Choose **Turn In Artifacts of Enchanted Origin**.
3. Select the piece to surrender. **Selecting it consumes the equipment for one point**, regardless of its strength or properties. There is no additional turn-in confirmation.
4. Choose **Claim Rewards**, or double-click the Researcher from within **five tiles**, to see the reward list. Select an affordable reward and confirm the purchase nearby.

The turn-in message may mention artifacts of the Kotl. That reused wording still refers to your Sorcerer's Dungeon points. Purchased rewards require backpack space; if delivery fails for lack of space, the purchase gives no item and takes no points.

## Rewards

| Reward | Points | Use and limits |
| --- | ---: | --- |
| Jack's Bag of Tricks | 75 | Double-click for a random treat or holiday oddity. October only, with a 24-hour cooldown per bag. |
| Serpent's Jawbone | 50 | House teleporter to Ilshenar destinations. Lock it down or secure it, then double-click from within two tiles. Travel restrictions apply. |
| Jack in the Box | 20 | Toy opens nine seconds after use and closes five seconds later. Wait 20 seconds between uses. |
| Shackled Heart of the Pumpkin King | 20 | Double-click for five blood effects at two-second intervals. The effect causes no hit-point damage. |
| Sterling Silver Ring | 50 | Hit Point Regeneration 3, Mana Regeneration 5, Damage Increase 75%, and a selectable +20 combat skill bonus. Initial durability is 255. |
| Talons of Escaping | 50 | Gargoyle footwear with Dexterity Bonus 4 and Stamina Regeneration 1. |
| Boots of Escaping | 50 | Thigh boots with Dexterity Bonus 4 and Stamina Regeneration 1. |

To set the ring's skill, put it in your backpack and double-click it. Choose **Archery, Fencing, Mace Fighting, Swordsmanship, Throwing, or Wrestling**, then confirm. Plan on keeping the choice; there is no normal reset option. The client may spell the name **Stirling Silver Ring**. Complete one purchase or ring choice before opening another confirmation. Safeguards for overlapping confirmations remain unfinished in the checked build.

**The Bag of Tricks works throughout calendar October, including outside the dungeon season. It does not work in November**, even on November 1-2 while the event may still be active. The cooldown is a full 24 hours after an item is produced, not a midnight reset. Each use has a **10% chance** of a Halloween treat; otherwise it gives rancid reindeer meat, a glass candy cane, named elf ears, a suspicious gift box, an insulting doll, or spiked eggnog. If your backpack cannot hold the result, it drops at your feet.

The Jawbone refuses travel while you are a murderer, criminal, carrying a faction sigil, in combat, or casting a spell. It also refuses if you are already at the destination.

**Hero of the Unloved, Savior of the Demented, and Slayer of the Pumpkin King title deeds are not offered.** Killing Jack does not grant one of these titles.

## When the season ends

New artifact awards stop, and the event removes its tracked creatures, bosses, unholy pumpkins, and hatched undead. Normal dungeon spawning resumes. **Do not assume the dungeon is safe when the event ends.** Existing cleanup does not cover every spell summon, such as a boss's Revenant, and ordinary dungeon enemies remain a danger.

The Researcher and entrance decorations normally stay. You can still turn in saved artifacts and spend points after the season, unless staff separately removes the Researcher. Equipment, unspent points, the hidden kill tally, and purchased rewards have no seasonal expiration in the checked source. The bag retains its October-only restriction.

Source record and implementation limits: [P654 guide notes](../cc-P654-guide-pumpkin-king.md). This is an unpublished draft, not confirmation of the build currently running on the shard.
