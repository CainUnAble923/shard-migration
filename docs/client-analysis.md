# Client data analysis: UOAlive and Immortal Realms vs vanilla

Measured 2026-09-06. Three installs walked and indexed in place; 1,539 files, 9.6 GB.
Comparison is by relative path and byte size. Nothing was uploaded or modified.

Data roots differ per install and must be resolved separately:

- vanilla: `D:\UO\UltimaOnlineVanilla` (files at root)
- UOAlive: `D:\UO\UOAlive\UOAlive 7.0.116.0`
- Immortal Realms: `D:\UO\ImmortalRealms\ClassicUOLauncher-win-x64-release\ClassicUO\ClientFiles`

## Method caveat, read first

The vanilla baseline is a **different client build** than UOAlive's 7.0.116.0. A family of
unrelated files comes out uniformly slightly smaller in UOAlive: art, gumpart, animations,
`tileart.uop`, `string_dictionary.uop` and every `cliloc.*`. Uniform small shrinkage across
unrelated files is version drift, not customization.

Rule applied throughout: **small negative deltas are version noise; positive deltas and new
files are real customization.**

Also note these clients had not been launched when measured, so anything a shard patcher
fetches on first run may not be on disk. Both clearly shipped their customization in the
download, so this does not change the conclusions.

## UOAlive: lightly customized

487 of 524 files match vanilla exactly in size. 28 differ, 9 are new (logs and config).

- Map edits to Felucca and Trammel: `map0LegacyMUL.uop` +1.6 MB, `map1LegacyMUL.uop` +803 KB,
  `map1xLegacyMUL.uop` +1.6 MB
- Static edits: `statics1.mul` +122 KB, `statics0.mul` -38 KB
- Custom multis: `MultiCollection.uop` differs
- Facet data touched: `facet00.mul` and `facet01.mul` both differ
- Config only: `uo.cfg` +1.9 KB, `client.cuo`, `macros2d.txt`, `metrics.txt`, patcher logs

**Absent:** no custom art, no custom gumps, no extra facets, unmodified `client.exe`,
no `verdata.mul`.

Consistent with its reputation as the more active community. Almost nothing to download,
almost nothing to break.

## Immortal Realms: heavily customized

1.8 GB larger than vanilla across the same file set. 383 of 499 files match; 50 differ,
66 are new.

- **Custom art at scale:** `artLegacyMUL.uop` +53 MB, `gumpartLegacyMUL.uop` +61.9 MB
- **Statics rebuilt on every standard facet:** Felucca 20.4 to 68.7 MB (3.4x), Trammel
  20.4 to 74.3 MB (3.6x), Ilshenar/Malas/Tokuno 3.7x to 4.2x
- **Sixteen additional facets** (see below)
- **Rewritten strings:** `cliloc.enu` -1.3 MB, every other language file about -16 KB
- **Patched client:** `client.exe` differs by 53 KB
- **Both formats shipped:** `art.mul` alongside `artLegacyMUL.uop`, `map0.mul` through
  `map5.mul` alongside the `LegacyMUL.uop` equivalents
- **No `verdata.mul`:** patching by outright file replacement

Consistent with a heavily customized, one-character-does-everything design.

## The custom facet table

Standard UO ships facets 0-5. Immortal Realms ships `map0.mul` through `map21.mul` with
matching `staidx` for all, and real statics on 13 of the 16 extras. Dimensions derived from
map size at 196 bytes per block.

| Facet | map.mul | Dimensions | statics | Read |
|---|---|---|---|---|
| 0 | 89,915,588 | 7168x4096 | 68,698,574 | Felucca, statics 3.4x vanilla |
| 1 | 89,915,588 | 7168x4096 | 74,329,556 | Trammel, statics 3.6x vanilla |
| 2 | 11,289,796 | 2304x1600 | 8,918,133 | Ilshenar |
| 3 | 16,056,516 | 2560x2048 | 9,852,605 | Malas |
| 4 | 6,421,352 | 1448x1448 | 4,376,610 | Tokuno |
| 5 | 16,056,516 | 2560x2048 | 3,781,925 | Ter Mur |
| 6 | 89,915,392 | 7168x4096 | 0 | allocated, terrain only |
| 7 | 77,070,336 | 6144x4096 | 6,280,099 | custom, populated |
| 8 | 77,070,336 | 6144x4096 | 11,407,361 | custom, populated |
| 9 | 77,070,336 | 6144x4096 | 6,014,666 | custom, populated |
| 10 | 77,070,336 | 6144x4096 | 3,632,727 | custom, populated |
| 11 | 77,070,336 | 6144x4096 | 11,488,603 | custom, populated |
| 12 | 77,070,336 | 6144x4096 | 6,374,179 | custom, populated |
| 13 | 77,070,336 | 6144x4096 | 7,109,263 | custom, populated |
| 14 | 77,070,336 | 6144x4096 | 7,505,491 | custom, populated |
| 15 | 77,070,336 | 6144x4096 | 7,073,689 | custom, populated |
| 16 | 89,915,392 | 7168x4096 | 21,497,525 | custom, heavily built |
| 17 | 77,070,336 | 6144x4096 | 28,844,669 | custom, most built of all |
| 18 | 77,070,336 | 6144x4096 | 7,497,301 | custom, populated |
| 19 | 77,070,336 | 6144x4096 | 2,991,611 | custom, lightly populated |
| 20 | 89,915,392 | 7168x4096 | 0 | allocated, terrain only |
| 21 | 89,915,392 | 7168x4096 | 0 | allocated, terrain only |

## Why this matters to us

**The six-facet ceiling is an official-client limit, not a ClassicUO one.** Immortal Realms
runs sixteen extra facets and ships ClassicUO as its launcher. ServUO's `Server/Map.cs`
already allocates 256 map slots and `MapDefinitions.cs` carries a commented
`RegisterMap(32, ...)` example.

If we standardize on ClassicUO, custom facets are a real design option rather than a
workaround that reuses slots 0-5. This corrects an earlier claim in `migration-plan.md`.

## Available on request

Entry-level diffing inside the `.uop` and `.mul` containers, which would name the specific
art indices, tile IDs and cliloc strings that changed rather than reporting at file
granularity.
