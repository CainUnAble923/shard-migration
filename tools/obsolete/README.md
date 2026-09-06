# Obsolete: built for a migrate-to-ServUO plan that was not taken

The shard **stays on ModernUO**. ServUO content is ported in. See `docs/direction-decision.md`.

Kept, not deleted: the research is sound and correct for what it was. Do not use any of it
without re-reading against the current direction.

- `spawner_json_to_xmlspawner.py` + tests + verification note — converts our spawner JSON to
  ServUO XML. Wrong direction; our spawners never leave ModernUO.
- `triage_ports.py` — ranks our 111 files by difficulty of porting *to* ServUO. We are not
  porting our files anywhere.
- `ExportServUOAccounts.cs`, `Account-modernuo-email.patch` + verification note — account
  migration. There is no cutover, so accounts never move and the SHA2 window is moot.
