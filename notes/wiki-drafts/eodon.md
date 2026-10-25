# Exploring the Valley of Eodon

Draft checked against the shard's source and port notes on October 25, 2026. The running shard's gate, creatures, and travel routes have not been checked in a game client. Locations below describe the implemented spawn areas, not guaranteed sightings.

Eodon is a wilderness on Ter Mur with dinosaurs, tribal villages, jungle wildlife, swamps, and lava fields. Bring healing supplies, a way to handle poison, and a way home. Leave follower space if you plan to tame an animal.

## Getting there and getting home

Open a public moongate's destination menu, choose **Ter Mur**, then **Valley of Eodon**. The arrival point is **719, 1863**, at height 40. The destination requires a client that supports Ter Mur and the newer expansion content. Murderers and characters carrying a faction sigil have restricted moongate menus.

The Eodon public moongate belongs at that same arrival point. Use it to choose your destination for the return trip. If the gate is missing, report it to staff. An arrival option in the menu does not prove that the return gate has been placed in that world.

## Where to explore

Coordinates here are map tile X and Y, not sextant readings. Creatures can wander away from these areas.

| Area | Places to look | What to expect |
|---|---|---|
| Northern dinosaur country | Around **425, 1404** and **319, 1501**, northwest of the gate | Allosaurus, anchisaur, archaeosaurus, dimetrosaur, gallusaurus, najasaurus, and saurosaurus. Some are tameable; others are hunting targets. |
| Northern swamps | Around **267, 1433** and **319, 1502** | Alligators, frogs, toads, corpsers, and acid elementals. These areas overlap dinosaur territory. |
| Tiger country | Around **347, 1911**, **398, 1896**, and **454, 1895**, southwest of the gate | Wild tigers, less common white and black tigers, panthers, forest ostards, and other wildlife. |
| Western desert | Around **122, 1805** and **117, 1740** | Giant black widows and desert scorpions. Desert scorpions inflict lethal poison. |
| Southern lava fields | Around **856, 2132** | Lava serpents, lava snakes, fire elementals, and lava lizards. Air elementals also appear farther east. |
| Northeastern gorilla country | Around **921, 1410** | Silverback gorillas. Their thrown bananas can hurt at range, so distance alone is not protection. |

An allosaurus is a substantial fight, with 18,000 starting hit points. An archaeosaurus can cause bleeding. A dimetrosaur can use Mortal Strike and Dismount. A najasaurus inflicts lethal poison. Do not judge a dinosaur's danger by its size or by whether it can be tamed.

The villages belong to the **Jukari, Kurak, Barrab, Barako, Urali, and Sakkhra** tribes. Tribesmen normally retaliate against attackers rather than treating every visitor as an enemy. Attacking one can bring nearby idle members of the same tribe into the fight. Tribe shamans are spellcasters.

A **wandering shaman** is a different NPC: a traveling healer in tribal clothing. The healer's resurrection rules still apply, including refusal of criminals and murderers.

## Climbing to the Barako village

Look for the vines at **678, 1759**, north and slightly west of the arrival gate. They lead to the raised Barako platform.

1. Stand within **2 tiles** of a vine, at its height or below it.
2. Finish any spell you are casting. You cannot climb while paralyzed, frozen, or casting, even if the refusal message only mentions paralysis.
3. Double-click the vine. It moves you to **679, 1757**, at height 100, on the platform.

The vines climb upward only. They do not offer a trip back down. A walking descent has not been confirmed in a game client for this draft, so bring a way home before climbing.

## Taming notes

Use **Animal Lore** to inspect a candidate and check your available follower capacity before starting. These are the base Animal Taming requirements for fresh, untrained creatures. Meeting a requirement does not guarantee success. Training can increase the skill and follower slots a pet needs.

The starting slot values below assume the implemented Time of Legends pet training rules. A najasaurus with a low enough roll can start at one slot instead of two.

| Creature | Base Animal Taming | Starting follower slots | Notes |
|---|---:|---:|---|
| Wild tiger, wild white tiger, wild black tiger | 95.1 | 2 | Look in tiger country. Ordinary wild tigers are not rideable by default, including after taming. |
| Najasaurus | 102.0 | 1-2 | Lethal poison; can become angry during taming. |
| Gallusaurus | 102.0 | 3 | Can become angry during taming. |
| Dimetrosaur | 102.0 | 3 | Can become angry during taming. Its first tame reduces its wild stats and maximum hit points. |
| Saurosaurus | 102.0 | 3 | Can become angry during taming. Its first tame also reduces its wild stats and maximum hit points. |

Allosaurus, anchisaur, archaeosaurus, and silverback gorillas in these spawn areas are not tameable. A white or black wild tiger is a color variant of the wild tiger, not a saber-toothed tiger.

### Dragon turtle hatchlings

A dragon turtle hatchling has a base taming requirement of **104.7**. With pet training enabled, it starts at **3-4 follower slots**, depending on its roll. However, the regular Eodon spawn list does not place hatchlings, so this draft has no verified wild-taming route for one.

If one becomes available, its first tame keeps its stats and maximum hit points. Each positive skill is capped at 100 and receives an additional 55% reduction after the ordinary taming reduction. Without paralysis during taming, that leaves roughly **40.5% of its wild skill values**, allowing for rounding. Releasing and re-taming it does not repeat the hatchling's extra first-tame reduction.

## Hunting materials and the port's limits

Carving a wild tiger's corpse leaves **4 pelts** on the corpse. Ordinary, white, and black tigers provide their corresponding pelts. Open the corpse to collect them. A wild dragon turtle hatchling's corpse similarly yields **4 scutes**, but its regular hunting source is unverified as described above. Tamed animals do not provide these special carving yields while controlled.

The valley's travel, wildlife, tribes, and vines do not establish access to every Eodon activity described on other Ultima Online wikis. This spawn list omits the Myrmidex invasion creatures, the Valley of One quest encounters, and the Dragon Turtle champion. It also provides no regular spawns for saber-toothed tigers, greater phoenixes, or infernus. Do not plan a quest, boss hunt, or taming trip around those encounters without a confirmed source on this shard.

Some creature abilities differ from standard guides. For example, the ported anchisaur does not use the Rampage mastery, and the ported saurosaurus does not receive natural Tail Swipe or Life Leech abilities. Use the creature's current Animal Lore information when planning a pet.
