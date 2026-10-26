# Tracking Ping

Draft checked against merged source on October 26, 2026. This describes the first server stage built in P625. Availability on the running shard and the display in a real client have not been checked.

Tracking Ping gives you a brief count and list of nearby creatures. It unlocks at **90.0 trained Tracking**. Gear bonuses do not count toward the unlock, range, duration, or player-sensing threshold. Any character who meets the skill requirement can use it; Rangers' League membership, rank, and a teaching purchase are not required.

The current version sends a chat summary and offers a results window. Mini map dots, world map overlays, and choosing a quarry from Ping results for a tracking arrow are still unbuilt. The usual Tracking categories remain available for ordinary tracking.

## How to use it

1. Be alive, have at least 15 stamina, and finish any spell you are casting. Use a location outside a dungeon region.
2. Use the Tracking skill and press **Ping: sense creatures near you** on the extra menu beside the usual Tracking menu. You can also type `[TrackingPing` or use that command in a macro.
3. Stand still for one second while you read the trail. Moving or taking damage breaks your focus. Death, a facet change, or disconnect also cancels it.
4. When the pulse fires, read the count in chat. Open **Ping results** from the extra menu or type `[TrackingPing results` while the pulse is active.
5. Press **Refresh** to see the latest list. There are ten contacts per page, with previous and next buttons when needed. The window does not update itself.

Opening or refreshing results does not start another Ping or charge another cost. After a pulse ends, opening or refreshing results reports that no Ping is active. An already open window can retain old text until you refresh it.

## Cost and range

A completed focus reveals you if you were hidden, spends **15 stamina**, and starts a **30 second Ping cooldown** measured from when the pulse fires. It uses no mana. An empty completed scan still pays the full cost. A refused or interrupted focus spends no Ping stamina and starts no Ping cooldown, although using the Tracking skill itself still has its normal skill delay.

Firing a Ping also imposes at least ten seconds before another skill use. The command respects an existing skill delay. The menu button currently skips that starting delay check, including on an old menu; both routes still enforce the Ping cooldown. Cost and cooldown do not improve with skill.

| Trained Tracking | Creature radius | Pulse duration | Player contacts |
| --- | --- | --- | --- |
| Below 90.0 | Unavailable | None | None |
| 90.0 | 18 tiles | 6 seconds | None |
| 95.0 | 21 tiles | 6 seconds | None |
| 100.0 | 24 tiles | 6 seconds | None |
| 120.0 | 28 tiles | 6 seconds | Within 12 tiles and line of sight |
| 125.0 | 29 tiles | 7 seconds | Same restriction |
| 150.0 | 34 tiles | 8 seconds | Same restriction |
| 175.0 | 39 tiles | 9 seconds | Same restriction |
| 200.0 and above | 44 tiles | 10 seconds | Same restriction |

The radius is a square: it extends the listed distance north, south, east, and west, including the corners. Between 90 and 100, it is 18 plus the whole-number part of `0.6 x (Tracking - 90)`. Above 100, it gains one tile per full five points. Duration gains one second per full 25 points above 100. Both stop improving at 200.

The scan stays centered on the tile where the pulse fired. You may walk inside that square afterward, but the square does not move with you. The server checks contacts once per second, adding arrivals and removing contacts that die, hide, or leave its limits. Chat gives the initial summary rather than a new count every second; use Refresh for the latest results.

The pulse ends after its listed duration, normally with **"Ping ended."** It can fade early if you leave the square, change facets, move more than 16 height units above or below its origin, enter a dungeon region, die, or drop below the trained Tracking value captured when it fired. Logging out or disconnecting ends it silently. Ending a fired pulse early does not refund its cost or clear its cooldown.

Ping itself grants no Tracking gain or XP. Use ordinary Tracking to train the skill.

## What the results mean

An example opening summary is:

> Ping: 2 hostiles, 1 neutral animal, 1 friendly. Hostiles: 1 fair/even, 1 tough. 6 seconds.

Counts depend on the creatures actually found. Groups with no contacts are left out. Each contact belongs to one group:

| Group | Meaning |
| --- | --- |
| Hostile | A creature attacking you or your party, or a wild creature whose enemy rules say it would attack you. |
| Neutral animal | An animal that does not meet the hostile or friendly rules. |
| Neutral NPC | Another creature or NPC that does not meet those rules, including ordinary vendors. |
| Friendly | Your pets and summons, and those of party members. |
| Player | A player who meets the separate sensing limits below, including a party member. |

Results use that group order and sort nearer contacts first within each group. A monster's appearance alone does not make it hostile. Another player's pet can be hostile if it or its owner is attacking you or your party; otherwise it is neutral unless it belongs to your party.

Creature rows show a kind such as **orc** or **giant spider**, rather than the creature's personal name. Player-owned pets read **your pet** or **a pet**. Hostile and neutral creatures also get a relative difficulty word: **easy or below**, **fair/even**, **tough**, or **dangerous/deadly**. Friendly pets have no difficulty word. A row might read `orc - hostile, tough`.

Difficulty uses the shard's creature comparison system. Its default comparison for you uses your best trained combat-related skill, rather than Tracking or an earned XP level. Treat it as a rough estimate. Ping provides no exact health, resistance, loot, or player combat-strength readout.

Player rows show a name and a notoriety word such as innocent, ally, gray, criminal, enemy, murderer, or invulnerable. Appearing in Ping does not grant permission to attack someone.

## Who and where Ping can find

Ping can find living, nonhidden monsters, animals, NPCs, pets, and summons on your facet within its square and within **16 height units** of the firing tile. Ordinary creatures can be sensed through walls. A result does not provide a route to reach it.

It excludes you, dead creatures, ghosts, dead bonded pets, hidden or invisible contacts, and staff characters. A ridden mount is not a second contact. Controlled pets or summons with no valid owner are excluded.

All dungeon regions are currently unavailable. Starting there gives **"Ping unavailable here: dungeon floor not mapped."** and costs nothing. Creatures inside a dungeon region are also excluded from an outside scan. No dungeon floor has been enabled for Ping in this stage.

House interiors are excluded unless you are inside the same house as the contact. This is a location check; owning a house does not let you scan its interior from outside. Outside dungeons, the height check does not distinguish separate stories of a building. Dedicated floor maps and private-instance or staff-area protections from the design are still unfinished.

### Players and other players' pets

At **120.0 trained Tracking**, a living, nonhidden player can appear if they are within **12 tiles of where you currently stand** and in line of sight. They must also remain inside the original scan square and satisfy its height and location limits. The 12 tile limit stays the same at higher skill and applies to party members too.

A player first detected receives:

> You feel watched. Someone nearby is reading the trail.

The warning gives no tracker name or direction. It is sent once per pulse, with at most one warning per ten seconds across multiple trackers.

A pet or summon owned by someone outside your party follows the same 120 skill, 12 tile, and line-of-sight restrictions, measured to the pet. It is excluded if its owner is hidden or staff. Your own and party-owned pets use the ordinary creature limits instead; hiding a party owner does not by itself hide that owner's pet. A pet appearing alone does not trigger a warning to its owner.

Hiding and invisibility keep a contact out at every Ping skill, including 200. Ping never reveals a target. Newly hidden contacts are removed from the server list at the next refresh; refresh the window to clear its old text. An empty scan says **"Ping: no eligible contacts on this floor."** It does not prove the area contains no hidden creatures or players.

## Current limits

- Players pass a line-of-sight check, but Ping does not yet honor every special visibility rule. In particular, it can list a nearby participant or pet that tournament rules would normally hide. Do not rely on Ping to preserve tournament separation.
- Very crowded scans can report **"Too many trails to read here."** If the initial scan is refused, it costs nothing. If crowding ends an already active pulse, its stamina and cooldown are currently kept. Ping otherwise keeps all eligible contacts rather than ordinary Tracking's nearest twelve.
- During a server stall, refresh callbacks can run after the nominal pulse deadline. The listed duration describes normal operation.

The moving map display, quarry selection, dungeon floor maps, and Rangers' League explanation are planned follow-up work. This draft describes the count and list available in the merged first stage.

## Sources

- [P625 build notes](../cc-P625-build-tracking-ping.md) and the [P563 design](../cc-P563-tracking-ping-design.md).
- [Current Ping source](../../../ShatteredLegacy/server/customizations/ClusterFTrackingPing.cs), [Tracking menu patch](../../../ShatteredLegacy/server/patches/Tracking-ping-offer.patch), and [creature comparison source](../../../ShatteredLegacy/server/customizations/ClusterFCreatureLevels.cs).
- [P625 review](../cc-P625-build-tracking-ping-codex-review.md) and [P637 review](../cc-P637-review-build-tracking-ping.md) for current defects and verification limits.
- [P648 work notes](../cc-P648-guide-tracking-ping.md) for source locations, design differences, and checks.
