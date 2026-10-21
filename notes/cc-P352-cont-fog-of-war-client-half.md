# CC task P352: Fog of war, the TazUO half (F-6), continued

Iron, 2026-10-21. Both repos were clean on `golem/Iron/P352` when I started. Continues P240
(`notes\cc-P240-fog-of-war-client-half.md`). **Paused at Chase's request** after part 5 (the package build); the
continuation is `cc-P357-cont-fog-of-war-client-half.md` in the queue (patch notes, notes, preflight).

## Headlines

- **Patch 0004 is written and builds:** `client\patches\0004-world-map-fog-of-war.patch` (P240's manager plus the
  wiring in four upstream files) and its row in `client\README.md`.
- **`Build-Client.ps1` with tests is green:** the pin plus 0001-0004 applied, **1,302 of 1,302** client unit tests
  passed, `TazUO.exe` published to `D:\UO\cc-p352-work\tazuo\client`.
- **Two new tests, each seen failing first:** the "Fog of war" toggle defaults on (a `Profile` needs no
  GraphicsDevice, so it is testable), and 0xF4 is registered to the manager.
- **The package builds from that client to scratch** with every gate passed (`ShatteredLegacy-2026.10.21.0814.zip`,
  99 MB, 741 files, "TazUO 3212623f + 4 patches"), and `-CheckZip` passes gates 4, 6 and 5. Not published.
- **Left for P357:** the CHANGELOG/VERSION entry, its notes and preflight.

## What changed

Code repo (`D:\UO\golems\Iron\ShatteredLegacy`):
- `client\patches\0004-world-map-fog-of-war.patch` (new, 24 KB): `git diff` of the dev tree over 0001-0003, headed like
  0001-0003 (a format-patch mailbox header; the `From` hash is zeros because the dev tree's change was never
  committed; `git apply` and `git am` ignore it). LF only, like the others (0 CR lines in all four).
- `client\README.md`: the 0004 row in the patch table.

What the patch changes, with lines as built in `D:\UO\cc-p352-work\tazuo\src\src\ClassicUO.Client\`:
- `Game\Managers\ShardFogOfWar.cs` (new): P240's manager, unchanged from `notes\cc-P240-files\`.
- `Network\PacketHandlers\HandlerRegistry.cs:125`: `(ShardFogOfWar.PacketId, ShardFogOfWar.Receive)`, plus its `using`.
- `Network\PacketHandlers\EnterWorld.cs:18`: `ShardFogOfWar.Reset()` right after the player is created, so each login
  starts empty and a shard that sends no 0xF4 shows no fog.
- `Configuration\Profile.cs:443`: `WorldMapShowFog`, default true, beside `WorldMapFlipMap`.
- `Game\UI\Gumps\WorldMapGump.cs`:
  - `:75` `_showFog`; loaded `:247`, saved `:294` with the other world-map settings;
  - `:370` the "Fog of war" menu entry (`TazLang` key `map_show_fog`, English fallback), added after "Flip map" `:707`;
  - `:2366-2403` `DrawFog`, called `:2515` right after the map texture and before markers and mobiles. It returns at
    once unless the setting is on and `ShardFogOfWar.HasData(_map.Index)`. It draws with the float overload
    (`Batcher2D.cs:1044`), with the math from P240's route: source rect in chunks from
    `floor((centerX - size_zoom_half) / 8) - 1`, `size_zoom / 8 + 3` square; position the map's centre; the map's
    rotation; origin `(worldCenter - chunk0 * 8) / 8`; scale `8 * size / size_zoom`.
- `tests\ClassicUO.UnitTests\Game\ShardFogOfWarTests.cs`: P240's 8 tests plus 2 (below).

Not checked by a test: the drawn alignment itself (it needs a GraphicsDevice and a running client). It rests on the
batcher's arithmetic as read in P240, and is item 1 of For Chase.

## Tests

| Test | What it checks |
|---|---|
| `The_fog_toggle_defaults_on` | `new Profile().WorldMapShowFog` is true |
| `The_packet_is_registered_to_the_manager` | `PacketHandlerRegistry.GetHandlers()` has exactly one 0xF4 entry, and it is `ShardFogOfWar.Receive` |

| Run | Tree | Result |
|---|---|---|
| red | the dev tree with the default set to false and the registry line commented out (both marked P352-RED) | `--filter ShardFogOfWarTests`: **2 failed, 8 passed of 10**, the two new ones |
| green | markers removed (grep finds none), wiring restored | all client tests: **1,302 of 1,302 passed** |
| build | `Build-Client.ps1 -Out D:\UO\cc-p352-work\tazuo` (fresh worktree at the pin, 0001-0004 `git apply`, tests, publish) | 0004 applied; **1,302 of 1,302 passed**; `TazUO.exe` built |

Package (P124's checks), under the `package` lock (taken, released):
`Build-PlayerPackage.ps1 -TazUO D:\UO\cc-p352-work\tazuo\client -Out D:\UO\cc-p352-work\package -UoData D:\UO\UltimaOnlineVanilla -Notes "P352 scratch build: fog of war (patch 0004)"`
- exit 0; paperdoll fit gate 0 failures; animation encode gate matches; gate 6 123 native files checked;
- `built D:\UO\cc-p352-work\package\ShatteredLegacy-2026.10.21.0814.zip`, `99 MB, 741 files, TazUO 3212623f + 4 patches`;
- `-CheckZip` (with `-UoData`): GATE 4 passed, GATE 6 passed, GATE 5 passed. (Without `-UoData` it stops, asking for
  the EA data, as designed.)
- Not published.

Server suite untouched (no server change).

## Deviations and decisions for Chase

1. **The patch header's commit hash is zeros.** The dev tree is a scratch worktree of the shared TazUO clone, so I did
   not commit in it; the header is otherwise format-patch's. The README's rebase recipe (`git am`) still takes it.
2. **The scratch folder is `D:\UO\cc-p352-work`** (client build, package zip, both logs), outside both repos. It and
   `D:\UO\cc-p240-work` can be deleted once P357 is done.
3. P240's decisions stand (toggle in the world map's menu, fog strength 216/255, the server's duplicate exploration
   code, depletion ignored).

## For Chase

Once a package with this client is published (not done here):
- a fresh character's world map is dark;
- walking clears 8x8 chunks around them;
- relogging keeps what was walked;
- "Fog of war" in the world map's right-click menu hides the fog;
- another shard shows no fog.

To try it now without publishing: run `D:\UO\cc-p352-work\tazuo\client\TazUO.exe` against the test shard. Check that
the fog edges sit on the map's tiles at a few zoom levels, with "Flip map" on and off.

## Continuation

- **Done:** parts 1-5: dev tree, the wiring, the two tests (red then green), patch 0004 and its README row,
  `Build-Client.ps1` with tests, the package to scratch with its gates.
- **Left:** part 6: CHANGELOG.md and VERSION, notes, preflight. That is `D:\UO\cc-prompts\queue\cc-P357-cont-fog-of-war-client-half.md`.
- **Mid-flight:** nothing. No lock held. The code repo holds only the finished patch and README row. It builds, and
  its client tests are green.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P352 -NoRefresh`
(the work copies in place of the real folders). It commits nothing; neither repo is BLOCKED:

```
Repo Result
---- ------
code dry run
docs dry run
```

- code: `client/README.md`, `client/patches/0004-world-map-fog-of-war.patch`.
- docs: this note.

P352 PAUSED
