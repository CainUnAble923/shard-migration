# High Seas fishing and ships

Draft checked against project notes and source code through October 25, 2026, including P269 and its P587 fix-up as merged. Features still to come are marked (planned). Some built features still lack a normal player access route, as explained below. Availability, fish-monger placement, and settings on the running shard have not been checked.

## Your first fishing trip

Start with a fishing pole and nearby water. Fishermen sell poles. Double-click the pole, then target water within reach. Leave room in your backpack for the catch. If the fish stop biting, try another spot.

The Maritime Brotherhood is the guild for Fishing, Cartography, and Cooking. Open the Guild Directory with `[guild`, choose the Brotherhood, and use **Show me the way** to find its New Haven docks chapter. Joining is free and gives your character trade tools, including a fishing pole.

The Brotherhood's Apprentice task asks for **30.0 Fishing or 5 ordinary Fish**. That is a task after joining, not an admission fee. Membership and guild standing belong to your character.

## Where to fish

Shore fishing is a good start. A classic boat lets you reach open water and pursue ocean catches. Dungeon water has a separate High Seas fish pool.

| Water or catch | Fishing requirement | Examples or notes |
|---|---|---|
| Ordinary water fishing | No minimum to start | Ordinary fish, small magic fish, and occasional discarded footwear. |
| Named High Seas shore fish | 50.0 | Yellow perch, brook trout, walleye. |
| Named High Seas deep-water fish | 80.0 | Mahi mahi, amberjack, yellowfin tuna. |
| Named High Seas dungeon fish | 106.0 | Demon trout, orc bass, dungeon chub. |
| Deep-water special finds | 80.0 base for big fish and special nets; 90.0 for treasure maps; 100.0 for bottles | Meeting the requirement allows a chance at the find. |

Deep water means open sea with deep water around the fishing spot. Being aboard a boat close to shore is not enough. Dungeon water is treated separately for named High Seas fish.

These thresholds open a catch pool. They do not guarantee that every cast produces that kind of fish. Some rare species have their own location and skill requirements.

## Rare and legendary catches

Rare and legendary fish are tied to particular seas or dungeon regions. Use the right water as well as enough Fishing. These examples show how the requirements differ; access to the named fishing spots has not been checked on the running shard.

| Catch | Where | Minimum Fishing |
|---|---|---|
| Yellowtail barracuda | Trammel, deep water | 81.9 |
| Giant koi | Tokuno, deep water | 95.8 |
| Blue marlin | Trammel, deep water | 105.0 |
| Black marlin | Felucca, deep water | 110.1 |
| Autumn dragonfish | Ilshenar | 105.4 |
| Abyssal dragonfish | Destard | 120.0 |

Rare catches record the fisher, date, and weight. Keep a specimen whole if you want a trophy. Common High Seas fish can be cut into raw fish steaks; some special fish have their own carved meats or steaks.

A taxidermist needs **90.0 base Carpentry, a taxidermy kit, and 10 boards** to turn a supported rare fish, crab, or lobster into a trophy deed. The process consumes the catch, boards, and kit. Use the deed beside a suitable wall in a house where you are an owner or co-owner. The trophy preserves the catch details and can be chopped back into its deed.

## Crab and lobster traps

Lobster traps and lava lobster traps have been ported. Fish-monger delivery orders can now reward a **lava lobster trap**, if staff have placed the mongers. A normal purchase or crafting source for an ordinary lobster trap remains unverified.

If you have a trap, double-click it in your backpack and target suitable water within **6 tiles**. It becomes a buoy and bobs once a minute. Double-click the buoy to recover the trap, then double-click the recovered trap to empty its catch into your pack.

Traps catch crabs and lobsters, including rare varieties when the location and Fishing requirements match. A pole does not catch those varieties. A lava lobster trap targets lava instead of water. Pole fishing in lava is also built, but requires a lava hook that current delivery orders cannot award.

Recover traps regularly. Their chance of being lost rises with time, and a lost trap takes its contents with it. Your party and player guild members can recover your trap too. Felucca allows others to take it as a criminal act. A player guild here means your player-run guild, not shared Maritime Brotherhood membership.

## Bait, hooks, and lava fishing

Bait and enhanced bait now work on poles and traps. Double-click a bait cup in your backpack, enter the amount when asked, then target your pole or trap. Fish bait goes on poles; crab and lobster bait goes on traps. You can also target another cup of the same bait to combine it.

Matching bait doubles that species' rare-catch roll; enhanced bait triples it. You still need the right water and Fishing skill, and a catch is not guaranteed. A successful pole catch spends one bait use. Check the pole's tooltip for its bait and remaining amount.

The Fisherman's Tall Straw Hat, Vest, Eelskin Gloves, and Trousers are built as Charybdis rewards. Their bonus adds to the matching-bait roll. Wearing the set does not improve an unbaited cast, and normal access to Charybdis remains blocked below. The gargoyle Fisherman's set is still (planned).

If you have a magic hook, double-click it in your backpack and target a pole. Replacing an attached hook returns the old one with its remaining uses. Hooks wear out through use, and some failed casts can wear them too.

| Hook | Effect |
|---|---|
| Lava hook | Lets a pole fish in lava. Targeting water still fishes water. |
| Junk-proof hook | Gives an 80% chance to skip the discarded-footwear row of the catch table. It does not guarantee a valuable catch. |
| Dredging hook | Makes supported shipwreck salvage barnacle-covered during SOS recovery. |

Lava-pole catches include stone footwear, cracked lava rocks, stone pavers, and an occasional weapon. Some rare catches also depend on the lava's region. An axe can split a cracked lava rock into decorative pieces. Access to suitable lava on the running shard is unverified.

**Current access limit:** these hooks are implemented, but current classic-boat orders cannot reach their reward tier. Ordinary delivery rewards provide some bait, including a rare chance of enhanced bait, but no hooks or Charybdis bait. Lava-pole fishing therefore still needs staff-supplied equipment.

## Bottles, SOS messages, and sea monsters

Go to sea prepared to fight. A treasure map, message in a bottle, or special fishing net found by pole fishing can be carried by a hostile sea serpent instead of going into your pack. Defeat and loot the serpent to collect it.

| Find | What to do |
|---|---|
| Message in a bottle | Double-click it in your backpack to extract an SOS. Read the SOS for the wreck's coordinates. |
| Waterstained SOS | Carry it in your own backpack, sail near the coordinates in Trammel or Felucca, and fish. You may recover wreckage before the treasure chest. Recovering the chest consumes the SOS. |
| Ancient SOS | Follow the same process. Its chest contains a fabled fishing net instead of the ordinary special net. |
| Special fishing net | Double-click it in your pack and target open deep water. It brings up hostile sea creatures, which can include serpents, water elementals, and krakens. The net is consumed. |
| Fabled fishing net | Expect a Leviathan as well as the net's other sea creatures. This is a combat encounter. |

Keep the SOS on your character. A message stored on a pack mule is not available to the fishing recovery check. Recovered chests are unlocked and untrapped, but sailing and nearby monsters still make the trip dangerous.

SOS recovery now includes fish heads, oars, unfinished furniture parts, and a rare yellow polka dot bikini among the salvage before a chest. A recovered chest also has a small chance to be a ship's strongbox. The bikini is a salvage find, not a promised item inside every chest.

Charybdis and Osiredon the Scalis Enforcer are also ported. Charybdis uses tentacles, lightning, and waves; Osiredon uses water attacks and parasitic eels. Their rewards include artifacts. They can push boats, but the current port has no hull-damage system.

The **Oracle of the Sea and Charybdis summoning are now built**. If you have the equipment, double-click a charged Oracle in your backpack to seek a spot at sea in Trammel or Felucca. A successful search spends a charge; a new Oracle has five. Keep it in your backpack and cast a pole baited for Charybdis into the indicated area with **100.0 Fishing**. The encounter has a cooldown, so the Oracle cannot always provide a new spot.

**This is not yet a normal player route:** current orders cannot award the Oracle or Charybdis bait. Building the summoning mechanism did not make its equipment obtainable. The current fabled net still summons a Leviathan; it is not a verified way to summon Osiredon.

Corgul the Soulbinder, his crew, and some of his rewards are also built. His altar and the boat warp to his island remain (planned), so his encounter currently requires staff placement. It waits on boat travel work, not a completed cannon-combat system. This guide cannot direct players to a working Corgul encounter.

## Fish-monger delivery orders

Profession fishing deliveries are now built separately from the Maritime Brotherhood's Cooking orders. Staff must place the fish mongers before players can use them. The setup covers Britain, Moonglow, Trinsic, Vesper, Jhelom, Skara Brae, Papua, and the Sea Market in Trammel and Felucca; actual placement is unverified.

1. Bring a boat you own within **100 tiles** of a fish monger on the same facet. Stand within **3 tiles** of the monger and double-click him.
2. Read the offered fish, quantity, and delivery port. Accepting places a shipping crate in your boat's hold.
3. Put the requested whole fish or crustaceans in that crate. Its tooltip shows progress and destination. Credited catches cannot normally be lifted back out, so keep trophy specimens elsewhere and leave delivery catches whole.
4. Sail the loaded boat to the destination and double-click its monger with the boat nearby. Confirm the completed order to collect the reward and fish-monger standing.

Classic boats receive an order for one kind of catch, with a quantity between **5 and 20**. Higher Fishing opens more kinds of requests. These orders live on their crates rather than in the general quest log. Use `[FishMongerStatus` to check your standing.

**Current rewards are limited to the first tier:** bait, lava lobster traps, Fishing Guide volumes 1 or 2, Fishing power scrolls, or plain fishing poles. The tier depends on the points from that delivery, not your accumulated standing. Even the largest current order falls below the next tier, so repeating deliveries does not unlock hooks, the Oracle, or Charybdis bait. These rewards are possible rolls, not a bundle paid for every delivery.

**Choose an order carefully:** there is currently no usable player cancellation action for an accepted order. An unfinished crate left in the hold can block dry docking. Ask staff for help with an order you cannot finish.

## Fish pies

Fish pies and their timed effects are built. Learn their oven recipes with the **Cooking band II book**; minimum Cooking is **55.0 or 61.0**, depending on the pie. Each uses its specified fish steak or meat, dough, and other ingredients.

**Players cannot currently bake them through normal ingredient sources.** Mento Seasoning, Samuel's Secret Sauce, and Dark Truffle have no implemented supplier here; Unicorn Fish Pie also needs unavailable Fresh Ginger. Learning the book does not supply those ingredients. Charybdis drops two to five pies, but normal access to that encounter remains blocked as described above.

If you obtain a pie, double-click it in your backpack. Its effect lasts **five minutes**; eating another with the same effect does not stack it. Examples include Bull Fish Pie's **+5 damage increase**, Great Barracuda Pie's **+8 hit chance**, and Autumn Dragonfish Pie's **+10 Meditation**, which obeys your skill cap. Other pies give spell damage, defense chance, regeneration, or protection against a damage type. Damage-protection pies remove up to five points of the matching damage per hit and do not reduce player-versus-player damage under Endless Journey rules.

Fairy Salmon Pie's casting focus and Lava Fish Pie's soul charge have no working gameplay bonus in this port. Their buff display does not establish an active benefit.

## Choosing and using a boat

| Ship | Status |
|---|---|
| Small, medium, and large classic boats, with dragon versions of each | Existing classic designs, sold by shipwrights. |
| Tokuno, Gargish, and Orcish galleons; Britannian ship; rowboat (planned) | Assessed for a future port. No completed ship port is recorded in the checked source. |
| Hull damage and repairs, ship paint, ship recall runes, cannons, crews, and bounty voyages (planned) | Part of the proposed High Seas ship work. |

For a classic boat, buy a deed from a shipwright and use it to target a clear stretch of water. Keep the boat key safe. Use the plank to board, and give the tiller man spoken sailing orders from aboard: **forward**, **stop**, **turn left**, **turn right**, **raise anchor**, and **lower anchor**.

To pack the boat away, lower its anchor, empty its hold, clear loose items and passengers from the deck, and step ashore. Keep its key in your backpack. Double-click the tiller man from outside the boat to begin dry docking, then confirm. The boat becomes a docked boat item you can carry and place again.

The ship assessment proposes sailing galleons first, then damage and repair, cannons, and finally crews and bounty work (planned). It does not establish a release date or final player acquisition rules.

## Fishing, training, and the League

Catches check **Fishing skill**, not a character level. The default individual skill cap is **200**, but ordinary pole fishing keeps its training ceiling at **100**. Unlocking a rare catch above 100 does not itself add a higher pole-training range.

Trap bobs can give Fishing gains toward your cap. Deep-water trap training requires **75.0 base Fishing**. This training behavior is built; the new lava-trap reward does not verify fish-monger placement or accessible lava on the running shard.

Fishing can satisfy the general skill achievements. Open `[achievements` to see the public requirements and earned rewards. Achievement Points and Renown connect those accomplishments to the [League](league.md). A separate character-level and XP system is (planned); this port does not establish XP payments per catch.

The Maritime Brotherhood already offers **Cooking bulk order deeds** to qualifying members and teaches Cooking patterns. Its proposed guild Fishing deeds remain (planned); the fish mongers' delivery crates are a separate system. Its Ocllo headquarters is (planned); the New Haven docks remain its chapter. See the [crafting guide](crafting-changes.md) for Cooking orders and patterns.

## Sources

Paths below are relative to the shard-migration repository. File and line evidence for the original guide is in the [P393 work notes](../cc-P393-guide-high-seas-fishing.md); the [P599 refresh notes](../cc-P599-guide-high-seas-refresh.md) record the merged second-half source checks and verification limits.

- [P193 fishing port](../cc-P193-port-high-seas-fishing.md) and [P209 integration](../cc-P209-cont-fixup-port-high-seas-fishing.md): fish, traps, trophies, champions, rewards, deferred content, and recorded verification.
- [P269 second half](../cc-P269-high-seas-fishing-second-half.md) and [P587 integration](../cc-P587-cont-fixup-high-seas-fishing-second-half.md): bait, hooks, lava poles, SOS salvage, the Oracle, delivery orders, pies, Corgul, and reported build verification.
- [P598 source review](../cc-P598-review-high-seas-second-half.md): reward-tier access, missing ingredients, missing order cancellation, and unresolved item-handling defects. These findings are not reported as fixed by the merge.
- [P268 ship assessment](../cc-P268-high-seas-ships-assessment.md): classic boats, proposed galleon phases, ship combat, and open access questions.
- [P67 craft ceilings](../cc-P67-craft-ceilings.md) and [P283 skill-gain survey](../cc-P283-skill-gain-paths-research.md): fishing find limits and pole versus trap training.
- [P54 XP and gain-path research](../cc-P54-f12-xp-and-gain-paths.md) and [levels and loops design](../f12-levels-loops-caps.md): earlier training gaps and planned character progression.
- [P15 guild starter path](../cc-P15-guild-starter-path.md), [P123 bulk orders](../cc-P123-port-bulk-orders-crafts.md), and [P78 recipe gating](../cc-P78-recipe-gating.md): guild tools, Cooking orders, and learned patterns.
- [P175 Clean Up Britannia](../cc-P175-cont-clean-up-britannia-finish.md): deferred fishing-set rewards.
- [Feature queue](../../docs/feature-queue.md), F-9, F-12, F-20, F-49, and F-51: guild scope, levels, Fishing deeds, halls, and reagent gathering design.
- [Content menu](../../docs/content-menu.md): recorded naval-combat decision.
- [League](league.md) and [crafting](crafting-changes.md): companion drafts.

## Contradictions

These differences remain on record. The instructions above follow the checked implementation.

- **Ship direction:** the content menu declines High Seas naval combat as core surgery. P268 recommends a phased port and says the recorded decision needs a reversal.
- **Player access:** P269 describes the full delivery reward table, and says orders pay tier 1 or 2. P598 and the current source show that classic-boat orders only reach tier 1. Lava lobster traps and some bait now have a delivery source, conditional on monger placement; hooks, the Oracle, Charybdis bait, and normal champion access remain blocked. Pie ingredients have no normal source either. Staff-created test items do not establish player access.
- **Order handling:** P269 describes destroying a crate as resignation. P598 finds no usable player action to do so. It also records unresolved bait, hook, and crate-handling defects; P587 preserved the implementation rather than repairing those behaviors.
- **Training above 100:** the earlier P54 survey lists Fishing among skills needing a new gain path. P283 and the trap implementation provide cap-based trap checks; the ordinary pole gain window remains 0 to 100.
- **Pearls:** F-51 places Black Pearl among shoreline and fishing reagent sources. The checked fishing bonus awards White Pearl, and a Black Pearl fishing route is not implemented there.
- **Fisherman's set rewards:** P175's Clean Up Britannia notes defer the fishing set. P193 ports the human pieces as Charybdis rewards; the current Clean Up catalog does not list them as purchasable rewards.
