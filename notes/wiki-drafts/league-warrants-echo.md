# League Investigation Warrants and the friendly Echo

Draft checked against merged source on October 26, 2026, through P629 and P630. Both features are still being built and default to off. Warrants are not sold, and there is no Tome of Echoes or Registrar claim page yet. This guide describes the current code. Availability and settings on the running shard have not been checked.

## What each feature does

An **Investigation Warrant** names a hostile mini boss and a fixed investigation site. The current item gives directions and explains why it cannot be used. It cannot start a fight yet.

An **Echo of the Stygian Dragon** is a temporary friendly melee helper. It has the dragon's appearance in League blue, with much weaker combat stats and none of the real boss's special attacks. Staff can exercise the summon service; players do not yet have a way to call it.

## Investigation Warrants

### Getting and reading a warrant

There is currently no warrant purchase in the League shop. The catalog reserves **500 Achievement Points (AP)** as the unlock and **300 Renown** as the price for either warrant, but no purchase or payment happens in this version.

If staff supplies a valid warrant for a test, keep it in your backpack and double-click it. A bag inside your backpack also passes the use check. The warrant is blessed, weighs 0.1 stone, and is bound to an account. Characters on that account can pass its ownership check. Another account cannot use it. Direct trades and ground drops are refused; nested bags have a known transfer defect, so do not treat the item as safely transferable inside a bag.

To reach the site's final availability check, you must be a registered League member on the owning account, carry the warrant, and stand on the correct facet within **4 tiles** of its site. Using it from your bank fails. Earlier refusals can appear before the closed-feature message.

### The sites

| Warrant | Site | Facet | Coordinates, X/Y |
|---|---|---|---|
| Investigation Warrant: The Siegebreaker | Covetous, the harpy hall | Trammel | 5472, 1877 |
| Investigation Warrant: The Hollow Oak | The Yew woods | Trammel | 1059, 1166 |

The Siegebreaker site is in the harpy hall. The earlier lake shore proposal was dropped because it overlaps the Void Pool event area.

Away from the site, double-clicking gives its name, facet, and coordinates. On the correct facet it also gives your distance and the four-tile requirement. It does not teleport you. At the correct site, with the default switch off, it says: "League investigations are not open yet. Your warrant is kept."

A League investigation marker, if staff has placed one, identifies the investigation at that site. Double-clicking the marker gives information only. It cannot call a boss. Source entries for the sites do not establish that markers exist on the running shard.

A closed site keeps your warrant. A warrant for a withdrawn encounter tells you to take it to staff. A warrant marked as already in use is refused. Double-clicking never consumes the item in the current implementation.

### Rules that are not active yet

The tooltip describes one use, solo or consenting party play, a **24-hour account investigation cooldown**, one corpse's loot for the group, spending the warrant on failure, and restoration after a server interruption. Those are intended rules printed on the item. The current code has no encounter runner, party ready check, investigation cooldown tracking, protected group corpse, consumption, or interruption refund.

The catalog also reserves a **60-second ready check**, up to **10 participants**, and a **15-minute fight limit**. These values do not run a timer or create a party encounter yet. There is no current warrant reward or completion flow to use.

## The friendly Echo

### Access and requirements

The current player interface is unfinished. You cannot claim, buy, replace, or double-click a Tome of Echoes, and there is no player Call or Dismiss page. Those belong to later work.

For a staff-supervised test, the summon service requires **Mythril Citizen or higher on the character making the call**. A lower-rank alt does not inherit another character's eligibility. You must be alive, able to act, outside a duel, and have **2 free follower slots**. Existing pets and companions still use their normal slots. There must be a clear tile beside you that you can see and the Echo can occupy.

### Numbers and behavior

These are built-in defaults. Staff settings can change the required rank, duration, and cooldown.

| Rule or stat | Current default |
|---|---|
| Lifetime | 20 seconds from a successful summon |
| Cooldown | 30 minutes from success, shared by every character on the account |
| Active limit | One Echo per account |
| Follower cost | 2 slots; your follower cap does not increase |
| Maximum distance from its caller | 12 tiles |
| Health / stamina / mana | 300 / 100 / 0 |
| Strength / Dexterity / Intelligence | 200 / 100 / 50 |
| Base melee damage | 12-16, split 75% physical and 25% fire |
| Resistances | 35 in each damage type |
| Wrestling / Tactics / Magic Resist | 80 / 80 / 80 |

It starts by following its caller. It uses melee AI, has no spells or boss attacks, cannot bond or carry dropped items, and can be dispelled. Its base damage is not a promise of damage per hit against every enemy.

A successful call reveals a hidden caller and starts the cooldown. A refused call or failed summon leaves the cooldown unchanged. Once a call succeeds, early death, release, dispel, or dismissal does not refund the wait. Changing characters does not bypass it. The cooldown deadline is saved with account data; an active Echo does not resume after loading a save.

### Where it works and what it fights

The allowed facets are **Trammel, Ilshenar, Malas, Tokuno, and Ter Mur**. Felucca and custom facets are refused. Houses, staff jail regions, duel safe zones, the tutorial yard, Apprentice training grounds, and guarded regions with active guards are refused. An ordinary dungeon can be allowed. New Haven's wilderness is not automatically excluded just because it is on the island.

Its target checks allow living wild creatures that ordinary combat rules let its owner attack. They reject players, owned pets, summons, bonded or protected creatures, vendors, escorts, tutorial creatures, and other Echoes.

The Echo dissolves when its time runs out or lethal damage or release ends it. Owner death and logout also end it. A check once per second ends it for excessive distance, a facet change, entering a forbidden place, joining a duel, losing the required rank, or staff disabling the feature. Ending releases its follower slots without shortening the cooldown.

It leaves no corpse, loot, meat, hides, scales, or trophy. It is not the real Stygian Dragon and cannot provide that boss's drops.

### Current limits of this draft

Disconnecting is not the same as completing logout: the current Echo may remain during the logout delay until its short lifetime ends. Some owner restrictions are enforced by the periodic check, allowing a brief gap before dissolution. A review also found a pet-loss achievement reward path when an Echo takes lethal damage, so this draft does not promise that destroying it can never grant rewards.

Player access, full save/reload behavior, appearance in the installed client, and real fight balance still need verification. This is a preview of disabled foundations, not an announcement that either reward is ready to use.
