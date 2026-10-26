# Persuasion

Player guide draft, checked against merged source on October 26, 2026. Availability and settings on the running shard have not been checked.

Persuasion replaces Begging. Your learned points, skill cap, skill lock, and bonuses carry over. The current version lets you ask townspeople for help and carry letters for the Merchants' Exchange.

Your client's skill list may still call it **Begging**. Use that skill to open the **Persuasion** menu.

## Use the skill

1. Stand within **3 tiles** of a living human-shaped NPC, with a clear line of sight.
2. Use Persuasion, or Begging if that is the name in your client, and target the NPC.
3. Choose **Ask for help** or **Ask about work**.

Using the skill reveals you. Opening a valid conversation sets a **10-second skill delay**. Canceling the target or choosing an invalid target releases the delay. Players, controlled creatures, and summons cannot be persuaded.

## Ask for help

Ordinary spawned human townspeople can give coins or bread. Shopkeepers qualify, as do peaceful civilian creatures. Hand-placed NPCs without a spawner do not give charity, and opening the menu does not guarantee that an NPC qualifies.

The limits are shared by **every character on your account**, across towns:

| Limit | Allowance |
| --- | --- |
| Gold | Up to 50 per UTC day |
| Bread | Up to 2 loaves per UTC day |
| Each contact | One attempt per UTC day, including a refusal or nothing to spare |
| Reset | Midnight UTC |

A contact can give coins or one loaf, never both from the same request. If they give no coins, they offer bread while your account has bread left for the day. Asking never lowers karma. Negative karma can cause a refusal of coins, but does not prevent the bread fallback.

At neutral or positive karma, the maximum coins from one request are:

| Effective Persuasion | Maximum coins |
| --- | --- |
| 0 | 2 |
| 10 | 5 |
| 20 | 8 |
| 30 | 11 |
| 40 or higher | 14 |

The actual amount is also limited to one tenth of the NPC's backpack gold, rounded down, and your remaining daily gold allowance. Negative karma reduces the calculated ceiling as well as risking refusal. Bonuses help this calculation, but charity becomes no richer above 40 effective skill.

Charity can give a training opportunity only **below 20 base skill**, after you actually receive coins or bread. Contacts already credited for charity practice normally do not teach again, even on a later day or another character on the account. The current system remembers up to 200 credited contacts, so that history is not permanent after enough different contacts. A failed gain roll still spends the practice opportunity. Refusals and empty requests give no practice.

## Carry Exchange letters

Use Persuasion on a **banker** or the **Merchants' Exchange guildmaster**, then choose **Ask about work**. New Haven's bank is a starting point. No guild membership, rank, fee, or successful charity request is required. Other NPCs give directions to a banker instead.

The contact puts **a sealed Exchange letter** in your backpack. Its properties name the recipient's occupation and town, such as "a banker in Minoc." Double-click it to read the instructions and minutes remaining.

Travel to the named town on the **same facet as the issuer**. Stand within **3 tiles** of a matching recipient and **drag the letter onto the NPC**. Only the character assigned the letter can deliver it. A matching occupation in the wrong town or facet will not accept it.

You have **3 real hours from issue**. A successful delivery consumes the letter and gives one training opportunity. A wrong recipient leaves it undelivered. Trying to deliver an expired letter destroys it without practice; asking for work also removes an expired letter found in your backpack.

**Letters currently pay no gold, guild standing, scrip, or Renown.** Some dialogue mentions paid work, but the reward implemented here is a chance to train Persuasion.

An unexpired letter in your backpack blocks another assignment. Keep it there until delivery. This check currently covers the backpack rather than all outstanding letters. There is no daily courier quota.

## Train through courier work

Your **base skill**, before bonuses, chooses the hardest unlocked letter tier:

| Base Persuasion | Letter difficulty | Destination |
| --- | --- | --- |
| 0.0 to 9.9 | 10 | A different kind of shopkeeper in the issuing town |
| 10.0 to 34.9 | 35 | A banker in another town |
| 35.0 to 59.9 | 60 | A banker in another town |
| 60.0 to 84.9 | 85 | A banker in another town |
| 85.0 to 109.9 | 110 | A distant banker when available |
| 110.0 to 134.9 | 135 | A distant banker when available |
| 135.0 to 159.9 | 160 | A distant banker when available |
| 160.0 to 169.9 | 185 | A distant banker when available |
| 170.0 to 200.0 | 195 | A distant banker when available |

For the distant tiers, the board prefers a destination more than **1,000 tiles** from the issuer if one qualifies. Otherwise it uses another qualifying town on that facet. It avoids the previous issued destination while the server remains running; a restart forgets that rotation history.

Each delivery checks practice from **difficulty minus 25 to difficulty plus 25**. The ladder covers learned skill through 200, subject to your actual cap and available routes. Set the skill lock to **Up** to train. Bonuses do not unlock harder jobs early, and the practice check compensates for positive bonuses so wearing skill gear does not end its training window early.

A delivery is a training opportunity, not a guaranteed skill increase. The letter is consumed even when you gain nothing. Courier work can start at zero, so you do not need to wait for charity resets. At your cap, deliveries give no further learned skill. Training time has not been measured in play.

## Route problems and current scope

The board uses existing NPCs and recognized towns. If it says there are no outgoing letters, try another town's bank. From 10 base skill onward, a facet needs another recognized town with a banker. The supplied Tokuno content does not provide that route from Zento, so you may need to take work on another facet.

Some bank locations, including Luna's supplied bank location, can fail town recognition. Also, minters and gypsy bankers can be selected by the board but cannot accept letters addressed to "a banker." Try an ordinary banker in the named town; if none can accept it, report the route and let the letter expire. These are current code limitations, and actual saved-world routes have not been checked.

This version has no Persuasion haggling, sale-price bonus, rumor action, negotiated requisition rewards, calming action, or guard negotiation. Reaching 200 does not yet grant the proposed permanent shopping discount. The thief tutorial still uses its practice person for the Begging step; **Ask for help** there completes the demonstration without coins, bread, or skill gain.
