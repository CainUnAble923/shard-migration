# Can we have High Seas and Eodon without migrating?

Measured 2026-09-06 against ServUO pub57. Chase asked for both. This prices them properly
instead of treating each as one indivisible block.

Two different cost drivers are measured separately:

- **missing-dep%** — share of files referencing a subsystem ModernUO ships **zero** files for
  (Skill Masteries, Shadowguard, Myrmidex, Vendor Searching, Instanced Peerless, VvV,
  City Loyalty, Khaldun). High means *build a subsystem first*.
- **naval%** — share referencing `BaseGalleon`, `ShipCannon`, `Cannon`, `BaseBoat`, `Multis`.
  High means *coupled to the boat system*, which ModernUO has but in a much simpler form.

## High Seas: portable. No missing subsystems at all.

| Subarea | Files | Lines | missing-dep | naval | Verdict |
|---|---|---|---|---|---|
| Items | 57 | 13,807 | 0% | 21% | mostly separable |
| Quests | 24 | 5,163 | 0% | 58% | naval-coupled |
| Multis | 15 | 5,150 | 0% | 100% | the boat system itself |
| Mobiles | 21 | 3,195 | 0% | 24% | mostly separable |
| Spawners | 2 | 1,348 | 0% | 100% | naval-coupled |
| Gumps | 7 | 1,055 | 14% | 86% | naval-coupled |
| Regions | 4 | 831 | 0% | 75% | naval-coupled |
| Network | 2 | 86 | 0% | 100% | naval-coupled |

**The headline: 0% missing-subsystem dependency across every subarea.** Nothing in High Seas
requires building a subsystem ModernUO lacks. It is not blocked, only expensive in one place.

It splits into two halves:

- **Cheap half, ~78 files / ~17,000 lines.** Items and Mobiles: the fishing overhaul, rare
  fish, crabs and lobsters, fish pies, sea creatures, nets, charts, decorations. Almost no
  boat coupling. This is most of what a player actually *sees* of High Seas.
- **Naval half, ~54 files / ~14,000 lines.** Multis, Spawners, Network, Gumps, Regions,
  Quests. Centered on `BaseGalleon` (1,848 lines) plus the two cannon files. Porting it means
  extending ModernUO's `BaseBoat` rather than dropping files in. Real work, but bounded and
  not blocked.

**Conclusion: we can have all of High Seas on ModernUO.** Do the cheap half first, and treat
the naval half as its own project when the fishing and sea content is already landing.

## Eodon / Time of Legends: genuinely entangled

| Subarea | Files | Lines | missing-dep | Verdict |
|---|---|---|---|---|
| Shadowguard | 14 | 11,230 | 71% | expensive |
| Mobiles | 18 | 2,721 | 33% | expensive |
| Myrmidex Invasion | 6 | 2,198 | 83% | expensive |
| AuctionSafe | 6 | 2,114 | 0% | cheap |
| Items | 4 | 613 | 25% | expensive |

This is the opposite shape. The dependencies are on subsystems ModernUO does not have, so
porting means **building Shadowguard and Myrmidex Invasion from scratch** before any Eodon
content runs. That is a subsystem project, not a content port.

Note Shadowguard is a separate dungeon from the Valley of Eodon; they ship in the same
expansion folder. The Eodon *place* (map, tribes, creatures) is partly separable from the
Myrmidex battle system, and that separation has not been measured yet. Worth doing before
committing either way.

## Where this leaves the direction

Nothing here overturns staying on ModernUO. It changes the sequencing:

1. **High Seas cheap half** — fishing and sea content. Straightforward, high visible value.
2. **High Seas naval half** — a bounded project against `BaseBoat`. Decide after 1 lands.
3. **Eodon** — do not start until someone measures how much of the Valley separates from
   Myrmidex. If the answer is "not much", the honest options are building the subsystem or
   revisiting the migration, and the cost of each is written down.

The migration question stays legitimately open for Eodon specifically. It is closed for High
Seas: that one we can simply do.
