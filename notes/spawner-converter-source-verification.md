# Spawner converter source verification

Verified 2026-09-06 against:

- ModernUO `7c9215d97cb25c56b0b5cb35034944ccdaa0a485`
- ServUO pub57 `d76bf4443cf76d081ddaf8f57c87ff33749256af`

ModernUO sources inspected:

- `Projects/UOContent/Engines/Spawners/Commands/ExportSpawnersCommand.cs`
- `Projects/UOContent/Engines/Spawners/BaseSpawner.cs`
- `Projects/UOContent/Engines/Spawners/Spawner.cs`
- `Projects/UOContent/Engines/Spawners/SpawnerEntry.cs`
- `Projects/UOContent/Engines/Spawners/RegionSpawner.cs`
- `Projects/UOContent/Engines/Spawners/ProximitySpawner.cs`
- `Projects/Server/Geometry/Rectangle3D.cs`
- `Projects/Server/Json/Converters/Rectangle3DConverter.cs`

ServUO sources inspected:

- `Scripts/Services/XmlSpawner/XmlSpawner Core/XmlSpawner2.cs`
- `Scripts/Misc/MapDefinitions.cs`

Verified mappings implemented by `tools/spawner_json_to_xmlspawner.py`:

- The native ServUO DataSet shape is `Spawns` containing `Points` rows.
- ModernUO `count` maps to XmlSpawner `MaxCount`.
- Entry `maxCount` maps to the `MX` value in native `Objects2`; the remaining native
  object fields use the values emitted by ServUO's own save routine.
- Delays map to integer minutes when both are whole minutes, otherwise integer seconds
  with `DelayInSec=True`. Sub-second delays are rejected because the ServUO loader uses
  integer parsing.
- ModernUO XY bounds are end-exclusive. XmlSpawner's random selection includes
  `X + Width` and `Y + Height`, so converted width and height are each reduced by one.
- Legacy ModernUO `homeRange` creates a `2r+1` half-open square; the equivalent native
  XmlSpawner rectangle has width and height `2r`.
- ModernUO `spawnLocationIsHome` maps directly to XmlSpawner `IsHomeRangeRelative`:
  both choose the spawned location rather than the spawner location as `BaseCreature.Home`.
- ServUO pub57 registers Felucca, Trammel, Ilshenar, Malas, Tokuno, and TerMur. Other map
  names are rejected.

Explicitly unverified or unrepresentable:

- XmlSpawner has no direct per-entry probability field. Values other than 100 are rejected.
- ModernUO entry `properties` and constructor `parameters` may overlap XmlSpawner's type
  string language, but a safe encoding has not been verified. They are rejected.
- ProximitySpawner behavior has not been shown equivalent and is rejected.
- Spawn-position optimization fields have no verified mapping.
- XmlSpawner does not directly carry ModernUO's explicit Z bounds. Bounds and region
  conversions therefore require `--allow-z-loss`.

Verification performed:

- Ten unit tests cover counts, delay units, inclusive/exclusive geometry, legacy home
  range, region names, XML escaping/round-trip, strict rejection, and selective skipping.
- A strict smoke conversion of ModernUO stock
  `Distribution/Data/Spawns/post-uoml/felucca/Vendors.json` produced 34 XmlSpawner rows.
- A smoke conversion of ModernUO stock
  `Distribution/Data/Spawns/shared/felucca/FelCropsLS.json` produced 24 region-spawner
  rows with the required explicit Z-loss opt-in.
- Loading the generated XML inside a running ServUO server remains unverified.
