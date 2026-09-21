# Draft upstream report: spawn entries in `Distribution/Data/Spawns` that name types the assembly does not declare

**Status: DRAFT, not filed.** Written for Q-055's condition 2 (CC6 batch 7, 2026-09-21). Chase decides whether it goes
to ModernUO and in what form (an issue, or a pull request renaming the entries). Everything below was measured at the
pinned commit `7c9215d97`; re-check the entry names against `main` before filing, since the spawn files may have moved.

---

## Summary

`Distribution/Data/Spawns` (the Nerun's Distro conversion, commit `0d1fffd9f`, 2021-09-03) carries **9 entry names,
23 spawner entries in all, that name types ModernUO ships under a different spelling.** `AssemblyHandler.FindTypeByName`
returns null for each, so `BaseSpawner.Spawn` sets `EntryFlags.InvalidType` (`BaseSpawner.cs:1130`) and the spawner
never fills. The visible result: the Citadel has no elite ninjas, the Twisted Weald has no dryads, and Heartwood has
seven of its named elders missing. Each is a one-word rename in the JSON.

Beyond those nine, 31 further names (44 entries) in the same files name types ModernUO does not ship under any spelling
(ServUO-era content such as the Clan ratmen, the Underworld quest NPCs, `Medusa`, `StygianDragon`, `Niporailem`); those
are not renames and are listed at the end only so the count is complete. Two names (`genericguard`, `bodysculptor`,
4 entries) exist in no tree we can find.

## The nine renames

| file(s) | entry name as written | entries | should name | evidence |
|---|---|---|---|---|
| `shared/malas/Citadel.json` | `eliteninjawarrior` | 7 (spawners at [82,1875], [81,1892], [181,1883], [139,1868] and three more) | `EliteNinja` (`Mobiles/Monsters/SE/EliteNinja.cs`) | ServUO's Premium Spawner XML of the same Nerun lineage (`Spawns/malas.xml`) names `EliteNinja`/`eliteninja` at the same coordinates with the same counts and the same sibling entries (`serpentsfangassassin`, `tigersclawthief`, `dragonsflamemage`). The JSON never names `eliteninja` anywhere in the Citadel |
| `shared/ilshenar/TwistedWeald.json` | `DryadA` ([2171,1181], maxCount 8) and `Dryada` ([2207,1180], maxCount 12) | 2 | `MLDryad` (`Mobiles/Monsters/ML/Humanoid/Magic/MLDryad.cs`) | `Spawns/twistedweald.xml` names `MLDryad`/`mldryad` at the same rooms with the same siblings (`CuSidhe`, `Changeling`, `Satyr`, `DireWolf`). The JSON names `mldryad` nowhere. The assembly's other `Dryad` (`Engines/Quests/Uzeraan Turmoil`) is the Haven quester "Anwin Brenna", not a Weald creature |
| `shared/trammel/TownsPeople.json`, `shared/felucca/TownsPeople.json` | `abbein` | 2 ([7048,382]) | `ElderAbbein` (`Engines/ML Quests/Definitions/Heartwood.cs`) | the type's `DefaultName` is "Elder Abbein"; `Spawns/trammel.xml` places `Abbein` at Heartwood (7046,390) |
| same | `alethanian` | 2 ([7048,382]) | `ElderAlethanian` | `DefaultName` "Elder Alethanian" |
| same | `aneen` | 2 ([7053,338]) | `LorekeeperAneen` | `DefaultName` "Lorekeeper Aneen"; `trammel.xml` places `Aneen` at (7054,340) |
| same | `jothan` | 2 ([7048,382]) | `ElderJothan` | `DefaultName` "Elder Jothan" |
| same | `mallew` | 2 ([7048,382]) | `ElderMallew` | `DefaultName` "Elder Mallew" |
| same | `taellia` | 2 ([7048,382]) | `ElderTaellia` | `DefaultName` "Elder Taellia" |
| same | `vicaie` | 2 ([7048,382]) | `ElderVicaie` | `DefaultName` "Elder Vicaie" |

The JSON names `elder*` and `lorekeeper*` nowhere except `eldergazer` and `elderdugan`, and `MLQuest.Generate()` places
nothing (`Engines/ML Quests/MLQuest.cs:103`), so the seven Heartwood quest-giver types exist in the assembly and never
appear in the world.

## How it was verified

1. **Every entry name in every `Distribution/Data/Spawns/**/*.json` was resolved the way the spawner does.** A test
   in our tree reads the same files at runtime and calls `AssemblyHandler.FindTypeByName(name)` with the defaults
   (`fullName: false`, `ignoreCase: true`, the call `BaseSpawner.Spawn` makes); an offline script does the same over
   the source (every `class`/`struct`/`enum` declaration plus every `[TypeAlias]` string, last dotted segment,
   case-folded, as `TypeCache` registers them). Both give the same list.
2. **The intended type was taken from a second export of the same rooms, not guessed.** ServUO ships Premium Spawner
   XML of the same Nerun's Distro lineage; at the same coordinates it names the type its own tree has, and for the
   Citadel and the Weald that is the type ModernUO also ships. For Heartwood, the type's own `DefaultName` string
   equals the entry name with its title prefixed, and the ServUO NPC files of the same names agree on name, title and
   sex.
3. **Renaming works.** On our shard the nine are reconciled additively with `[TypeAlias]` on a second partial part of
   each stock type (no data change); with that in place the same JSON entries resolve, and the stock spawners at
   those coordinates fill with the stock types in a headless run against real map data. The aliases are a local
   workaround pending this fix and will be deleted when the data is corrected.

## For completeness: names with no ModernUO type under any spelling (not renames)

31 names, 44 entries, all ServUO-era content ModernUO does not ship: `magedragonsflamemage`, `treasurelevel1h`,
`athialon`, `boatpainter`, `dockmaster`, `escortablewanderinghealer`, `Barreraak`, `ClanChitterAssistant`,
`ClanChitterTinkerer`, `ClanRibbonCourtier`, `ClanRibbonSupplicant`, `ClanScratchHenchrat`, `ClanScratchSavageWolf`,
`ClanScratchScrounger`, `ElderDugan`, `FiddlingTobin`, `Garamon`, `Gretchen`, `IronBeetle`, `Jaacar`, `Medusa`,
`NavreyNightEyes`, `NevilleBrightwhistle`, `Niporailem`, `QuartermasterFlint`, `SlasherOfVeils`, `sphynx`,
`StygianDragon`, `Vernix`, `Xenrr`, and the two with no source anywhere, `genericguard` (2, `post-uoml/termur/
Underworld.json`) and `bodysculptor` (2, `post-uoml/*/Vendors.json`, the Sea Market). Whether ModernUO wants those
entries at all is a separate question; they cost nothing at runtime beyond the `InvalidType` flag.

## Related, found while verifying the Heartwood seven (separate issue if wanted)

`Distribution/Data/MLQuests.cfg` binds 27 of the 48 NPC types declared in `Heartwood.cs` to quests and leaves 21
unbound, among them all seven above plus `ElderAcob`, `Athailon`, `Bolaevin`, `Cloorne`, `Daelas`, `Mielan`,
`Olaeni`, `Rebinil`, `Tillanil`, `Tyeelor` and four others, while 99 of the file's 100 quest types are registered.
So even once the spawn entries are corrected, those elders stand in Heartwood and offer nothing. Not a spawn-data
defect; noted because a reader fixing the names will otherwise expect quest givers.
