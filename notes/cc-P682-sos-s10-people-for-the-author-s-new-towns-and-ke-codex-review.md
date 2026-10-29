# Codex review: P682

CC task P682: People for the author's new towns and keeps (SoS swap S10). Reviewed by Codex (`codex exec review`, read-only) after P682 DONE and before the Golem's commit, 2026-10-29 00:31.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.95). The spawn files, build integration and fresh-world command substantially implement the task. However, wild spawn ranges bypass the intended town and unfinished-land exclusions. Build results were inspected in the task notes, not independently rerun.

- **medium** [P2] Keep the full wild spawn range outside closed areas (`server\data\Spawns\sos\wild\Islands.json:410`)
  This spawner's home is outside the unfinished land east of Haven, but its radius of 30 reaches x=3197???3199 inside that closure, including walkable tiles. `BaseSpawner.GetSpawnPosition` samples the entire home range and checks spawnability, not the generator's exclusion mask, so alligators, lizardmen and snakes can spawn inside the land meant to remain fenced off. The same boundary issue lets `NujelmContinent sand 40` spawn inside Magincia. Shrink or constrain the spawn bounds against excluded areas, and verify those bounds rather than only the home tile.

(2.1 minutes, 991,241 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The work substantially implements the requested town populations and density reporting, but generated wild spawn ranges cross town and closure boundaries despite the claimed exclusions. The new checks validate homes and therefore miss this defect.

- **medium** [P2] Keep the entire wild spawn range outside excluded areas (`notes\cc-P682-tools\build_spawns.py:669`)
  The mask constrains spawner homes, but accepting a range with only 25% allowed tiles lets creatures spawn inside excluded areas. For example, the generated Trammel `NujelmContinent sand 40` at (3768,2015), range 30, overlaps walkable Magincia town tiles, and `island 107 jungle 1` at (3227,2396), range 30, overlaps the east-of-Haven closure. Pinned `BaseSpawner.GetSpawnPosition` samples the whole range without consulting this mask. Shrink or constrain spawn bounds to exclude forbidden tiles, and test the bounds rather than only each home.

(1.7 minutes, 695,827 tokens)
