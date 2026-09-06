# Obsolete: built for the migrate-to-ServUO plan

Everything here was correct work for a direction we no longer take. The shard **stays on
ModernUO**; ServUO content is pulled in selectively. See `docs/direction-decision.md`.

Kept rather than deleted because the research is sound and the direction could change again.
**Do not use any of it without re-reading it against the current direction.**

| File | What it was for | Why obsolete |
|---|---|---|
| `spawner_json_to_xmlspawner.py` | convert ModernUO spawner JSON to ServUO XmlSpawner XML | wrong direction; our spawners stay in ModernUO and never need converting |
| `test_spawner_json_to_xmlspawner.py` | its 10 unit tests | same |
| `spawner-converter-source-verification.md` | source verification for the above | same |
| `triage_ports.py` | rank our 111 files by difficulty of porting **to** ServUO | we are not porting our files anywhere |
| `ExportServUOAccounts.cs` | export ModernUO accounts to ServUO `accounts.xml` | no migration, so no account export |
| `Account-modernuo-email.patch` | ServUO-side account patch | same |
| `account-export-source-verification.md` | source verification for the above | same |

The SHA2 password work these supported is also moot: there is no cutover, so player password
hashes never need to be readable by another engine.

**Still valid and still in `docs/`:** `client-analysis.md` (the client diff and the custom
facet finding), `shard-inventory.md` (the measured custom surface), and the three setup
defects, which are problems with the shard as it runs today regardless of direction.
