# Decision: migrate to ServUO, do not port content into ModernUO

Status: **decided**, 2026-09-06. Measured by reading both source trees, not documentation.

## Scope that drove it

Full post-ML world **including naval combat and Eodon**. That scope is what settles this.

## The content gap

Both emulators declare the same expansion ladder
(`None T2A UOR UOTD LBR AOS SE ML SA HS TOL EJ`). ModernUO's enum reaches EJ but the content
behind those flags was never written.

| Content | ServUO pub57 | ModernUO main |
|---|---|---|
| High Seas | 134 files / 31,080 lines | 0 |
| Time of Legends / Eodon / Myrmidex | 74 files / 18,828 lines | 0 |
| Ter Mur / Stygian | 18 | 5 (all spawn data JSON, no systems) |

High Seas by subsystem (lines): Items 13,750 | Quests 5,139 | Multis 5,135 | Mobiles 3,174 |
Spawners 1,346 | Gumps 1,048 | Regions 827 | Network 84

## Why the reverse port was rejected

The two directions are not symmetrical.

| | Forward (shard to ServUO) | Reverse (content to ModernUO) |
|---|---|---|
| What gets rewritten | our own custom scripts | 184 files / 49,908 lines we did not write |
| World data | lost, fresh start + compensation | untouched, shard keeps running |
| Accounts | bridgeable but time-boxed | not a question |
| Runtime | .NET 10 down to net48/Mono | stays on .NET 10 |
| Shape of work | all-or-nothing cutover | incremental, reversible |
| Missing substrate | none | MUO has **zero** files for SkillMasteries, Shadowguard, Myrmidex, VendorSearching, InstancedPeerless |
| Maintenance after | ServUO project maintains it | we maintain it forever, conflicts on every upstream pull |
| Precedent | hundreds of shards | nobody has done it |

The reverse direction has real merit and was not dismissed lightly. It keeps the better
engine and skips the migration event entirely. It fails on scope:

**High Seas is not leaf content.** Its center is `BaseGalleon.cs` (1,848 lines) plus
`Cannon.cs` (1,491) and `ShipCannon.cs` (1,512). That subsystem extends and partly replaces
`BaseBoat`. Porting it means core surgery on the engine we would be keeping precisely to
avoid core surgery. **Eodon** is Time of Legends, 18,828 lines, sitting on Myrmidex Invasion
and Skill Masteries, both of which ModernUO ships zero files for.

The cheap half of the reverse port was always leaf content: fishing (`Fish.cs`,
`RareFish.cs`, `CrabsAndLobsters.cs`, `FishPies.cs`, ~3,300 lines, few dependencies) and
spawn data (JSON on MUO, XML on ServUO, converts both ways). None of that is what we want.

## What ModernUO does have

Worth recording so nobody re-discovers it: Quests, Party (`Engines/Party/`),
CannedEvil/champions, and Multis with the classic RunUO boats (`BaseBoat`, `SmallBoat`,
`LargeBoat`, `Plank`, `Hold`). Its spawner system is genuinely good: `Spawner`,
`RegionSpawner`, `ProximitySpawner`, JSON-backed with `[ExportSpawners]` / `[ImportSpawners]`,
and 109 era-tiered spawn files across `shared`, `uoml` and `post-uoml`.

The premise "ServUO has better spawn options" is right about **reach**, not about
**plumbing**. What ServUO adds is XmlSpawner2's conditional and quest-driven logic
(99 files, with XmlAttachments and XmlQuests) plus a post-ML world worth spawning into.

## Third option, considered and not taken

Stay on ModernUO, port only leaf content and data, accept an ML-era world with extras.
Cheapest path by a wide margin. Rejected because post-ML content is the point of the shard.

## Footnote

ServUO is GPL-2.0, ModernUO is GPL-3.0. Only matters if we distribute source. Not legal
advice, but worth checking before publishing a repo that combines both.
