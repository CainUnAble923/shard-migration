# Does Eodon separate from Myrmidex and Shadowguard?

**Yes. 60% of it is clean.** Measured 2026-09-06 across all of ServUO pub57, not just the
Time of Legends folder.

## Method

Scanned every ServUO script for Eodon-family terms (Eodon, the five tribes — Barrab, Jukari,
Kurak, Sakkhra, Urali — Zipactriotl, the dinosaur types, Myrmidex, Valley of Eodon), then
classified each hit by whether it also references a subsystem ModernUO lacks.

**148 files, 71,830 lines** mention Eodon-family content.

| Bucket | Files | Lines | Share |
|---|---|---|---|
| **CLEAN — Valley, tribes, creatures only** | **89** | **25,354** | **60%** |
| Myrmidex-coupled | 45 | 22,791 | 30% |
| Shadowguard-coupled | 8 | 11,385 | 5% |
| SkillMasteries-coupled | 6 | 12,300 | 4% |

## The clean set, by area

| Area | Files | Lines |
|---|---|---|
| Mobiles/Normal | 52 | 6,607 |
| Services/Expansions | 6 | 1,101 |
| Services/Seasonal Events | 4 | 842 |
| Quests/StudyOfTheSolenHive | 4 | 648 |
| Mobiles/Bosses | 2 | 499 |
| Services/Pet Training | 2 | 2,376 |
| Quests/Eodon | 2 | 1,298 |
| Services/VeteranRewards | 2 | 918 |
| Mobiles/AI, Named, NPCs, Multis, Items/Consumables, Factions | 7 | ~6,000 |

The largest clean block is **52 creature files** — the dinosaurs and tribal mobs that are what
players actually meet in the Valley. Plus the Eodon quest line and two bosses.

## What this corrects

The earlier figure of "Myrmidex Invasion is 83% dependent" was true but misleading. It
measured the **Myrmidex Invasion folder**, not Eodon as a whole. Read as a verdict on Eodon
it was wrong, and it made Eodon look gated when most of it is not.

Shadowguard is a **separate dungeon** that merely ships in the same expansion folder. It has
almost nothing to do with the Valley and accounts for 5% of the Eodon-family files.

## What this means

**Eodon moves out of workstream 4 (subsystem builds) and into workstream 3 (content backlog)**
for its clean 60%.

Suggested order:

1. **Eodon creatures** — 52 files, 6,607 lines, zero subsystem coupling. Dinosaurs and tribal
   mobs. Straightforward additive content and the most visible part of the Valley.
2. **Eodon quests and bosses** — ~4 files, ~1,800 lines.
3. **The rest of the clean set** — pet training, veteran rewards, seasonal tie-ins.
4. **Myrmidex Invasion** — 45 files, 22,791 lines. Genuine subsystem build. Do it later, or
   never, and the Valley still works without it.
5. **Shadowguard** — separate dungeon, its own decision entirely.

The Valley of Eodon is reachable on ModernUO without building a single missing subsystem.
