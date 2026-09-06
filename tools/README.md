# Migration tools

## `spawner-json-to-xmlspawner`

`spawner_json_to_xmlspawner.py` converts the JSON produced by ModernUO's
`ExportSpawners` command into the native DataSet XML consumed by ServUO pub57's
XmlSpawner loader:

```console
python tools/spawner_json_to_xmlspawner.py modernuo-spawns.json servuo-spawns.xml
```

The default is deliberately strict. Unsupported spawner types or behavior stop the
conversion without writing output. `--skip-unsupported` writes only verified rows and
prints every skipped spawner. `--allow-z-loss` explicitly accepts that XmlSpawner cannot
preserve ModernUO's bounds/region Z-selection behavior; both options are intentionally
lossy.

Currently source-verified mappings: ordinary `Spawner`, `RegionSpawner`, legacy home
range, total and per-entry counts, whole-second delays, team, walking/home range,
map/location, XY bounds, and region name.
Not verified and therefore rejected: `ProximitySpawner`, per-entry probability other
than 100, entry constructor parameters/properties, non-default position optimization,
and non-default maximum spawn attempts. Exact Z-selection parity
remains unverified and cannot be represented directly by XmlSpawner.

Run its tests with:

```console
python -m unittest tools/test_spawner_json_to_xmlspawner.py
```

## `muo-accounts-to-servuo-xml`

A small exporter that runs inside ModernUO, walks accounts, and emits a ServUO-shaped
`Accounts/accounts.xml`.

Key detail: the SHA512 digests are byte-identical between the engines, but ServUO stores
`BitConverter.ToString` output (hyphenated hex, `A1-B2-C3`) and ModernUO stores unseparated
hex (`A1B2C3`). Insert a hyphen every two characters on the way out.

Only works for accounts hashed with SHA2. See the Phase 0 note in `../docs/migration-plan.md`.
