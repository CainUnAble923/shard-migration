# Requisitions and Leads

Player guide draft, checked against source on October 24, 2026. The running shard and its settings have not been checked. Numbers below are built-in defaults. P452 fixes are queued and marked **changing soon**.

Requisitions let you trade unwanted magic equipment for Renown, guild standing, and gold. Some requests come with a personal Lead that helps you find an item for that request.

## Open your board

Visit the League field office in New Haven. Double-click the requisitions board on its north wall, or choose **Requisitions board** from the League Registrar's menu. The League board has **Previous guild** and **Next guild** buttons.

You can also open a guild's requests with **Requisitions** on its guild hall page, or open the full board through a League Appraiser. The Custodians do not post requisitions under the default rules.

Your requests belong to **your character**. Another character on the same account has a separate set. You do not need to join a guild to fill its requests, but non-members receive that guild's lowest-tier requests.

To check your open requests while traveling, type `[requisitions`. It prints the list in your journal; use the board to turn items in.

## Fill a request

1. Read the item type, property or slayer requirement, and reward on the board.
2. Put a matching item in your backpack. Found or crafted equipment can qualify.
3. Stay near a requisitions board, the League Registrar, an Appraiser, or the guildmaster of the guild posting the request.
4. Click **Turn in** beside that request, then target your item.

The counter ranges are 3 tiles for a board covering that guild, 4 for the Registrar or an Appraiser, and 8 for that guild's guildmaster. Stay nearby until you finish targeting.

**Turning in consumes the item.** You receive the listed Renown and guild standing, plus the gold the Appraiser would pay for that item. The Renown counts toward League rank. Standing pays immediately even if you have not joined that guild; it is not held until you complete an Apprentice task.

One item fills one request. It cannot also earn Clean Up Britannia points after being consumed, and a requisition does not award Clean Up points.

## Read the requirements

| Request | What the item needs |
| --- | --- |
| A named property | The right item type, that property at the required intensity, and enough properties in total. |
| A slayer | The right item type and the named slayer family. The family's super slayer also counts. For example, Repond can fill an orc-slaying request. |
| Anything magic | The requested item type with at least the listed number of magic properties. |

Intensity is the property's strength compared with its Full value in the Artificers' catalogue. A request for a property at 30% means at least 30% of that Full value. It does not necessarily mean a tooltip value of 30. On/off properties count as 100% when present. The board tells you why an item fails a turn-in.

Guilds favor different equipment. The Warriors' Brotherhood asks for swords, maces, and shields; the Rangers' League includes bows; the Bards' Consortium includes slayer instruments. The Thieves' Den and Artificers' Order can ask for any magic item with enough properties. Check the actual row before saving an item for a guild.

Blessed items are currently refused. **Changing soon, P452:** ordinary spellbooks, including necromancy books, are blessed by default and are wrongly refused even when they match a book request. This also affects books created by Leads. Spellbook turn-ins are queued for repair. Do not assume a book request can be completed before that fix arrives.

**Changing soon, P452:** the current property check can count ordinary exceptional crafting bonuses as magic. The queued fix will remove those bonuses from magic counting and Appraiser pricing. Do not rely on a plain exceptional craft qualifying as a magic item. The final board eligibility details need checking after P452 lands.

## Tiers and rewards

New requests use your rank in the requesting guild, capped by your League rank. You need both ranks to reach a higher tier. Raising either rank does not upgrade a request already on your board.

These are request tier labels. Individual guilds may use different names for their own ranks.

| Request tier | League rank needed to allow it | Minimum property intensity | Minimum properties | Renown | Guild standing |
| --- | --- | --- | --- | --- | --- |
| Initiate | Available without League registration | 20% | 1 | 10 | 40 |
| Apprentice | Iron | 30% | 1 | 20 | 60 |
| Journeyman | Bronze | 40% | 2 | 35 | 90 |
| Master | Verite | 55% | 2 | 55 | 130 |
| Grandmaster | Toxic | 70% | 3 | 80 | 180 |
| Top rank | Obsidian | 85% | 3 | 110 | 250 |

The intensity column applies to named-property requests. Anything-magic requests use the property count. Slayer requests use the slayer match rather than the tier's intensity or property count. Every tier also pays gold based on the item you hand in.

## Daily refresh

Each guild that posts requisitions gives your character **3 open requests**. A completed slot stays empty until the next daily refresh. Pressing **Refresh** on the board updates the display; it does not give you another set early.

The default refresh is **05:00 UTC**. The new set appears when you next read or use the system after that time. Open requests without an active Lead are replaced. Requests with an active Lead stay, and other slots fill around them.

Leaving a request unfinished or letting a Lead expire costs no Renown or standing. There is no Infamy penalty for requisitions.

**Changing soon, P452:** clock corrections or changes to the server's refresh setting can currently cause extra sets to appear. The queued fix protects the last-issued day. Treat 3 requests per guild per refresh day as the intended allowance.

## Follow a Lead

A Lead appears below its request. It names an area and a creature group, shows time remaining, and tracks qualifying kills since its last special drop. You do not need to accept it separately.

By default, a Lead lasts **3 real days from when the request is created**. Its request survives daily refreshes while the Lead remains active. You can still fill the request with any other matching item; following the Lead is optional.

When the Lead expires, its extra rolls stop and the request loses its protection from daily refresh.

To count for a Lead, a kill must meet all of these rules:

- The Lead is still active on your open request.
- The creature dies in the named area and belongs to the named creature group. If a Lead says creatures generally, there is no narrower family restriction.
- The creature has at least **1,000 Fame**. Some weaker creatures in the right area will not count.
- The creature killed is not a controlled pet or a summon.
- Your character receives the kill credit used by this system. A kill credited to your pet can count for you through its master.

Each qualifying kill gets a separate chance to produce an item for the request. This is **an extra item roll**, not a literal doubling of the monster's normal loot odds.

| Creature Fame | Extra drop chance on the first qualifying kill |
| --- | --- |
| 1,000 to 4,999 | 5% |
| 5,000 to 14,999 | 10% |
| 15,000 or more | 20% |

The chance rises after unsuccessful qualifying kills. With the default rules, the **40th qualifying kill since the Lead began or last dropped an item is guaranteed to trigger a Lead drop**. Forty is the maximum wait under these rules, not the average. The spellbook refusal described above currently prevents those book drops from fulfilling their requests.

Look in the creature's corpse and watch for **The rumor held** in your journal. If there is no usable corpse, the item goes to your backpack. The item is ordinary equipment without a special Lead tag. A personal Lead does not make its dropped item a bound quest item.

A drop resets that Lead's kill count. It leaves the Lead active on the open request, so more qualifying kills can produce more drops until the Lead expires or you fill the request. You receive the request's Renown and standing only when you turn an item in. One qualifying kill can advance more than one of your active Leads if it fits each one.

Higher League rank increases the chance that a new request has a Lead: 10% before Iron, then 15% at Iron, 20% at Bronze, 25% at Verite, 30% at Toxic, and 35% at Obsidian. It also opens more possible areas. Follow the area and group named on your own board.

## Use the Appraiser

The source places League Appraisers at the New Haven field office and near banks in Britain, Trinsic, Minoc, Vesper, Moonglow, Skara Brae, Luna, and Royal City. The New Haven post and the listed bank posts through Skara Brae are in Trammel; Luna is in Malas and Royal City is in Ter Mur. Placement on the running shard has not been checked.

Double-click an Appraiser or choose **Talk**, then use:

| Menu option | What it does |
| --- | --- |
| **Appraise an item** | Gives a quote without selling. |
| **Sell an item** | Opens a quote with a sale confirmation. |
| **Which requisition wants this?** | Names the first open request of yours that accepts the item. |
| **The requisitions board** | Opens your full board. |

Dragging an item onto an Appraiser also opens a quote. The item stays with you until you confirm **Sell**. **Keep** closes the quote.

The default price uses the item type, number of properties, and their combined intensity, capped at **500 gold per item**. Ordinary items without counted magic properties are refused. The exceptional-craft exception is **changing soon under P452**, as described above.

Selling consumes the item and pays gold only. If a request wants it, turning it in pays the same gold plus Renown and standing. Blessed items are currently refused by the Appraiser too. P452's spellbook turn-in fix does not establish that blessed spellbooks will become sellable, so do not plan on selling those books.

**Changing soon, P452:** safer checks for server settings are also queued to prevent a bad requisitions settings reload from leaving the board or Leads unusable. No player action is needed for that fix.

For related systems, see [the League](league.md), [guilds](guilds.md), and the [Artificers' Order](artificers-order.md). Source references and verification limits are in the [P558 work notes](../cc-P558-guide-requisitions.md).
