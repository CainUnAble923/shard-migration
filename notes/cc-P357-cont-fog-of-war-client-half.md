# CC task P357: Fog of war, the TazUO half (F-6), continued again

Gold, 2026-10-21. Both repos were clean on `golem/Gold/P357` when I started. Continues P352
(`notes\cc-P352-cont-fog-of-war-client-half.md`), which continued P240 (`notes\cc-P240-fog-of-war-client-half.md`).
This finishes the task: the patch notes, these notes and the preflight.

## Headlines

- **Patch 0004 and its README row are as P352 left them**, committed in `7b1ecda` (merged in `5d29bfa`); nothing
  touched either file since. Nothing rebuilt.
- **Patch notes:** a new version `2026.10.21.11` in `CHANGELOG.md` (today's sections up to `.10` were already
  committed, so I started the next one rather than add to a released section), and `VERSION` bumped to match.
- No server change, no build, no world command, no lock taken. The wiki page was not published.

## What changed

Code repo (`D:\ShatteredLegacy`):
- `CHANGELOG.md`: section `## 2026.10.21.11`:
  - Added: "The world map now has a fog of war: it starts dark and clears where you have walked, and what you have
    explored is kept across logins. Choose "Fog of war" in the world map's right-click menu to turn the fog off.
    Update your game through the launcher to see it."
  - Staff: the fog is drawn by our TazUO build (client patch 0004), so players see it only once a player package
    built with that client is published; until then the server's exploration data is sent but not shown.
- `VERSION`: `2026.10.21.10` to `2026.10.21.11`.

The section follows the file's head comment (one line per item, plain words, no file names in the player line; the
patch number is only in the Staff line, which players never see). It was not run through the server's parser
(`ShardVersion.cs`), which needs a server build; its shape is the same as the sections below it.

## Tests

None run: this part changes only the patch notes. P352's client results stand (1,302 of 1,302 client tests, the
package gates passed).

## Deviations and decisions for Chase

1. **The package is not published**, so the line "update your game through the launcher" is true only after the next
   package publish with P352's client (`D:\UO\cc-p352-work\tazuo\client`, or a fresh `Build-Client.ps1` build). If
   this version deploys first, the Staff line says why the fog is not visible yet.
2. `D:\UO\cc-p352-work` and `D:\UO\cc-p240-work` can now be deleted. They are on the PC that ran P240 and P352,
   not on this one (neither exists here).

## For Chase

Once a package with our patched TazUO is published:
- a fresh character sees a dark world map;
- walking reveals the map around them, 8x8 tiles at a time;
- relogging keeps what was walked;
- "Fog of war" in the world map's right-click menu hides the fog (and choosing it again brings it back);
- another shard shows no fog.

Also worth a look while there: the fog's edges sit on the map's tiles at a few zoom levels, with "Flip map" on and off.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\ShatteredLegacy -DocsRepo D:\UO\shard-migration -Branch golem/Gold/P357 -NoRefresh`.
It commits nothing; neither repo is BLOCKED:

```
Repo Result
---- ------
code dry run
docs dry run
```

- code: `CHANGELOG.md`, `VERSION`.
- docs: this note.

P357 DONE
