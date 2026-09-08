# ServUO content menu

> **REWRITTEN 2026-09-07 after S9. Read this box before any number below it.**
>
> **The old counts here were not raw ServUO counts, and every later document read them as if
> they were.** They were filtered once, on 2026-09-06, against ModernUO's **3,565 `UOContent`
> type names** — not against the **7,093 tree-wide types** S3 later indexed. So they sat between
> the raw number and the real one, and nothing on the page said which. `Items/Artifacts` is 583
> raw and 318 here; `Mobiles/Normal` is 462 raw and 132 here, against S3's 137.
>
> **The `dep%` column is deleted, not corrected.** It was "share of files touching one of nine
> named subsystems", which is the *touches* measure `AGENTS.md` says is an upper bound and not
> the work. It also claimed `Items/Addons` at 0% while 41 of its files need `DirectionType`. A
> corrected version would preserve a number in the shape that keeps misleading us.

## The four rows that have been measured properly

Filtered with S3's definition (a primary type ModernUO already declares, tree-wide), then
**resolved**, because a reference count is an upper bound on work and not the work. Full method,
file lists and four-bucket breakdown in `notes/s9-backlog-remeasure.md`.

| Area | Raw | Candidates | What resolving found |
|---|---|---|---|
| **Items/Artifacts + equipment** | 1,022 | **455** | **320 drop straight in, 81 need one more file from the same two directories. 88% needs nothing built.** Cheapest row on the backlog |
| Services/Revamped Dungeons | 255 | **255** | the only row where the filter removes nothing. `docs/tasks.md` also said 150 elsewhere; **255 is the answer** |
| Decoration / housing / crafting | 745 | **303** | plus 57 more from two directories the old 297 never covered. `DirectionType` + `AddonOptionGump` is ~71 additive lines and frees 34 |
| High Seas, cheap half | 78 | **77** | the one published figure that survived |

**Everything else on this page is unverified.** Treat any other row as an upper bound of unknown
tightness until someone applies the same two steps to it.


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
