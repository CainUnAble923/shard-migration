# ServUO content menu

What ServUO pub57 has that ModernUO does not, measured 2026-09-06 by comparing
ServUO's 6,144 scripts against ModernUO's 3,565 UOContent type names at pinned commit
`7c9215d97`. **3,091 candidate files, 548,912 lines.**

Nobody is going to port all of that, and nobody should try. This is a menu to choose from.

## How cost was measured

Each candidate was scanned for references to subsystems ModernUO ships **zero** files for:
Skill Masteries, Shadowguard, Myrmidex Invasion, Vendor Searching, Instanced Peerless,
Vice vs Virtue, City Loyalty, Khaldun, Exploring the Deep. The `dep%` column is the share of
files in that area touching one. High `dep%` means porting the content means building a
subsystem first.

| ServUO area | Files | Lines | dep% | Cost |
|---|---|---|---|---|
| Items/Artifacts | 318 | 33,618 | 2% | cheap |
| **Services/Revamped Dungeons** | 255 | 28,828 | 2% | **cheap** |
| Mobiles/NPCs | 222 | 40,053 | 0% | cheap |
| Services/Expansions (HS + TOL) | 176 | 47,220 | 12% | medium, **declined** |
| Items/Addons | 169 | 21,618 | 0% | cheap |
| Services/Seasonal Events | 154 | 22,106 | 25% | medium |
| Items/Equipment | 148 | 11,854 | 1% | cheap |
| Mobiles/Normal | 132 | 16,286 | 0% | cheap |
| **Services/XmlSpawner** | 97 | 63,630 | 1% | **cheap** |
| Items/Decorative | 88 | 6,486 | 0% | cheap |
| Items/Quest | 78 | 6,879 | 0% | cheap |
| Services/ExploringTheDeep | 70 | 10,341 | 29% | expensive |
| Items/Resource | 61 | 3,433 | 0% | cheap |
| Items/Consumables | 59 | 8,382 | 2% | cheap |
| Services/ViceVsVirtue | 55 | 9,445 | 100% | expensive |
| Services/CleanUpBritannia | 52 | 6,148 | 0% | cheap |
| Items/StoreBought | 51 | 6,799 | 0% | cheap |
| Items/Functional | 49 | 10,041 | 0% | cheap |
| Spells/Skill Masteries | 45 | 8,559 | 100% | expensive |
| Services/New Magincia | 40 | 10,963 | 0% | cheap |
| Quests | 34 | 7,824 | 0% | cheap |
| Items/Containers | 31 | 3,578 | 0% | cheap |
| Services/BulkOrders | 28 | 4,788 | 0% | cheap |

## Recommended first picks, for a family-and-classroom shard

**1. Revamped Dungeons — 255 files, 28,828 lines, 2% dependency.**
Despise, Shame, Wrong, Covetous Void Spawn, Blackthorn Dungeon, The Exodus Encounter.
This is the single best value on the list: a large amount of *places to go and things to
fight*, almost no subsystem dependencies. For kids, new dungeons are the most legible kind
of new content there is.

**2. XmlSpawner — 97 files, 63,630 lines, 1% dependency.**
This is the thing that started the whole conversation. Conditional and quest-driven
spawning, XmlAttachments, XmlQuests. ModernUO's spawner is good but has no equivalent for
this. Large in lines but self-contained, and it is a tool for building content rather than
content itself, so it pays off repeatedly.

**3. Creatures and NPCs — Mobiles/Normal (132) plus Mobiles/NPCs (222), 0% dependency.**
Pure additive content with no dependencies at all. Port them a handful at a time as needed
rather than in bulk; there is no reason to take all 354.

**4. Decoration and housing — Items/Addons (169) and Items/Decorative (88), 0% dependency.**
Cheap, visible, and the thing players actually spend time on. New Magincia (40 files,
housing lotto, plant system, bazaar) is also 0% dependency and community-flavored.

**5. Loot and equipment — Items/Artifacts (318), Items/Equipment (148), 1-2%.**
Best taken selectively. Port the pieces that anchor a dungeon or a quest rather than the
whole set.

## Declined, with the cost written down

- **High Seas naval combat.** `BaseGalleon` (1,848 lines) plus two cannon files (~3,000)
  extend and partly replace ModernUO's `BaseBoat`. Core surgery, not content.
- **Eodon / Time of Legends.** 18,828 lines resting on Myrmidex Invasion and Skill Masteries.
- **Vice vs Virtue** (100% dep), **Skill Masteries** (100%), **City Loyalty** (96%),
  **Exploring the Deep** (29%). Each is a subsystem build before any content appears.

Reversible. If the shard's users ask for one, the cost is here to re-read.

## The honest caveat

`dep%` measures dependencies on *missing subsystems only*. It does not measure how much a
file leans on ServUO base classes that differ from ModernUO's, and every port still needs
its serialization rewritten from ServUO's hand-written form to ModernUO's
`[SerializationGenerator]`. "Cheap" means cheap relative to the others here, not free.

The first port from any area should be treated as a probe: do one, build it, measure how long
it took, and use that to price the rest of that area.
