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

`modernuo/ExportServUOAccounts.cs` is a temporary owner-only ModernUO command that walks
the live account collection and atomically emits a ServUO-shaped
`Export/ServUO/accounts.xml`:

1. Copy it into `Projects/UOContent/Commands/` in the pinned ModernUO build tree.
2. Rebuild and restart ModernUO.
3. Run `[ExportServUOAccounts` as an Owner.

The command refuses to write anything unless every account has a valid SHA2 hash. The
output contains password hashes, login IPs, comments, tags, email addresses, and character
serials; handle it as a secret and never commit it.

Key detail: the SHA512 digests are byte-identical between the engines, but ServUO stores
`BitConverter.ToString` output (hyphenated hex, `A1-B2-C3`) and ModernUO stores unseparated
hex (`A1B2C3`). Insert a hyphen every two characters on the way out.

The exporter writes stock ServUO's `totalCurrency` value and also preserves ModernUO's
exact gold, platinum, and email values in `modernUO*` extension elements. Stock ServUO
ignores those extension elements. `servuo/Account-modernuo-email.patch` loads the email
extension and makes subsequent ServUO saves retain it. Exact high-balance currency
preservation remains unresolved because ServUO's in-memory account model uses `double`.

Compilation was verified against ModernUO `7c9215d97` (the pin until cc-P38) and is not re-verified against `d4531cd94`; executing it against live accounts
and loading the result in ServUO remain unverified.

## `content_index.py` (D20, 2026-09-27)

The S3/S9 content index, kept as a tool instead of rebuilt and thrown away. Read-only against all three trees.
`--legacy` is S9's method and reproduces S9's artifacts row file for file; the default adds the D20 fixes (alias strings
count as declarations, every secondary type of a discarded file is reported) and splits S9's `upstream` bucket into
`upstream` (a patch), `extract` (a type inside a discarded file) and `unknown` (read it). See `notes/index-blindspots.md`.

```console
python tools/content_index.py row artifacts             # candidates bucketed; also cc4, cc7, cc7extra, cc5
python tools/content_index.py hidden artifacts          # secondary types of discarded files, classified. NOT a backlog
python tools/content_index.py filter                    # step 1 alone
python tools/content_index.py compare-s9 artifacts --ours <tree>   # legacy vs S9's appendix, then S9 -> fixed
python -m unittest tools/test_content_index.py          # regression, ~8 s
```

`hidden` output is classified mechanically; `unresolved` means read it. Never quote its total as content.

## `save_instance_check.py`

The re-parenting window check (`docs/gap-register.md`) as a script: does any save artefact on this machine hold
an instance of the named types? Reads every `SerializedTypes.db` under the live save, `Saves-test`, each
`Backups/Automatic` snapshot and the two newest archives of each kind (needs `pip install --user zstandard`), with
`Server.Items.Dagger` as a positive control on each. Read-only.

```console
python tools/save_instance_check.py SpiritualityHelm ValorGauntlets
```
