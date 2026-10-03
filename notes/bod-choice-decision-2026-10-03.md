# Smith BOD request: player picks small or large (Chase, 2026-10-03)

From the P39 step 7 BOD check (bug-list D51).

- Large BODs are gated by **skill only**: Blacksmithy 70.1+. The Journeyman rank (5,000 standing) requirement is dropped.
- The guild page's Bulk Order button lets the player **choose Small or Large** (Large only when the skill is met), and
  the deed lands in the backpack through the normal accept gump, same as asking the Guildmaster.
- Works with or without the NPC (fixes D51's dead end).
- Caps stay: 3 small, 1 large active.
- NPC talk/context-menu path: overseer default is to keep the stock random roll; CC confirms in P42.
- Not OSI (large on demand): register a deviation from P42's text.
- Built in cc-P42 Part F.

## Same day, added (cc-P42 Part G)

- Small BODs, large BODs and Smith guild requests (commissions) ask only for items that can still raise the player's
  Blacksmithy. If none can: the hardest items the player can make (Chase picked the fallback).
- Rewards: about 3x Seals and 2x standing across the board, still no gold (Chase picked over gold or OSI reward items).
  Prompted by 20 exceptional ringmail tunics paying 60 standing and 1 Seal.
- Large-deed turn-in rank gate (cc-P32 PT-11) follows the skill-only rule too (Part F).
- Large Smith BODs accept crafted items directly (small deeds still combine too), because matching small deeds is near impossible (Chase, 2026-10-03; cc-P42 Part H).
