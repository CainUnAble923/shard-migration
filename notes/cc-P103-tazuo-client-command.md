# cc-P103: TazUO client patch: a whitelisted ClientCommand, so tutorial buttons open the World Map, Journal and options

2026-10-14. Client patch plus server side. Prompt: `D:\UO\cc-prompts\cc-P103-tazuo-client-command.md`. Not committed
(autopilot commits after DONE). Both repos were clean at the start, apart from the play-test importer's machine output.

## Headlines

- **The patched client builds here.** The TazUO source is P40's clone, `D:\UO\cc-p40-work\tazuo-3212623f`, at
  upstream `3212623f63436be1c0f4e3b308b202b29597c026` (v26.0909.63, the TazUO the package ships). The new
  `client\Build-Client.ps1` makes a clean worktree at that pin, applies our patch with no fuzz, runs the client's tests
  and publishes `D:\UO\tazuo-sl-build\client\TazUO.exe`. That build is outside both repos.
- **One rebasable patch:** `client\patches\0001-enhanced-packet-client-command.patch` (9,874 bytes), based on `3212623f`.
  It is one new file (`EnhancedClientCommand.cs`, 87 lines), **9 lines in three upstream files**, and a 68-line unit test.
- **The client side:**
  - What it does: enhanced packet 0xCE id 4 runs one command from the whitelist `optlink`, `paperdoll`, `marktile`,
    `radius`, `worldmap`, `journal`, `options`, through `CommandManager.Execute`.
  - The three new commands call `GameActions.OpenWorldMap`, `OpenJournal` and `OpenSettings`.
  - Guards: it sits behind the existing enhanced-packet opt-in. A command off the whitelist, a non-ASCII line or one over
    100 characters is ignored, and logged once per command name.
- **The server side:** `TazUOClientCommand.Send(mobile, command)`.
  - At connect the server sends the 0xCE id 1 handshake, asking for id 4.
  - It sends a command only to a client that answered id 4. Any other client gets nothing, and the gump's words stay.
  - A command off the whitelist is refused before anything is sent.
- **One step beyond the brief** (decision 1): a stock TazUO also answers the handshake but does not know id 4, so "TazUO"
  alone would show it a button that does nothing. Our patched client echoes id 4, and only that client gets buttons.
- **Tutorial:** core.travel and travel.wing (World Map), core.chat (Journal and filters) and core.movement (Options)
  show an "Open the ..." button, for our client only. The text stays the same for every client.
- **Tests:**
  - Server: 16 new cases. Against a wrong stub 15 failed (the 16th, "a station without those windows offers nothing", a
    do-nothing stub also passes). Full suite **1,163 of 1,163**.
  - Client: 21 new cases, **12 failed** against a stub. Full client suite **1,274 of 1,274**, also from the build
    script's clean worktree.
- **Not seen in a running client:** nobody has clicked a station button in the patched TazUO yet (For Chase, step 2).
  The player package still ships the stock TazUO, so **players see no change** until our build ships (cc-P40's P-a).

## Where the source is, and how it is built

- Source: `D:\UO\cc-p40-work\tazuo-3212623f` (a clone of `PlayTazUO/TazUO` with its six submodules), from cc-P40. I worked
  on a branch there, `sl/p103-client-command`, one commit `761d2456d` on top of `3212623f6`, and exported it with
  `git format-patch`. Before branching I reverted the two files P40's build had regenerated (`LegionScripting/docs/API.py`,
  `LegionAPI.md`; the build's `GenerateDocs` target writes them, P40 C.2). Nothing else of P40's was in that tree.
- `client\Build-Client.ps1`:
  1. a `git worktree` at the pin in `D:\UO\tazuo-sl-build\src`;
  2. the six submodules copied from the clone, each checked against the commit the pin records (nothing is fetched);
  3. our `nuget.config`;
  4. `git apply --check`, then `git apply`, per patch;
  5. `dotnet test` on the client's unit tests;
  6. `dotnet publish -c Release -r win-x64`, and `sl-build.txt` with the pin and each patch's SHA-256.

  Run on 2026-10-14: every submodule matched, the patch applied, 1,274 tests passed, and `TazUO.exe` built (240 MB folder).
  The string "not on the whitelist" is in the published `TazUO.dll`.
- Recorded where `design\client_patching.md` keeps client patches. It covered only `.mul` data patches, so I added a
  "Client code patches" section and a pointer near the top. `client\README.md` has the patch table and how to rebase.

## What changed

### Client patch (`client\patches\0001-enhanced-packet-client-command.patch`, paths under TazUO `src\ClassicUO.Client\`)

| File:line | Change |
|---|---|
| `Network/EnhancedPackets/EnhancedClientCommand.cs` (new) | `Whitelist`; `TryParse` (first word on the whitelist, printable ASCII, at most 100 characters, split on spaces); `ShouldLogRefusal` (once per name); `Handle` (reads the ASCII line, runs `world.CommandManager.Execute(parts[0], parts)` when a player is in the world); `SendAck` (id 4 back to the server, only if the server's enable list asked for id 4) |
| `Network/EnhancedPackets/EnhancedPacketTypeEnum.cs:9` | `ClientCommand = 4` |
| `Network/EnhancedPackets/EnhancedPacketHandler.cs:25` | registers id 4, inside the static constructor's existing `if (!Enabled) return;` opt-in |
| `Network/EnhancedPackets/EnhancedPacketHandler.cs:51` | `SendAck()` after the existing enable reply |
| `Game/Managers/CommandManager.cs:223-225` | `worldmap`, `journal`, `options` |
| `tests/ClassicUO.UnitTests/Network/EnhancedClientCommandTests.cs` (new) | 21 cases |

Wire format, server to client: `[0xCE][u16 length][u16 4][u16 version 0][ASCII command, 0]`. Client to server: `[0xCE][u16 5][u16 4]`.

### Shard repo (`D:\ShatteredLegacy`)

| File:line | Change |
|---|---|
| `server/customizations/TazUO/TazUOClientCommand.cs` (new) | `Configure` :57 registers incoming 0xCE (variable length) and the `EventSink.Connected` handshake; setting `clusterf.tazuo.enhancedPackets` :59 (default True) turns the handshake off; `SendHandshake` :73; `OnEnhancedPacket` :85 records id 1 (TazUO), id 4 (can run commands) and id 2 (version) per NetState in a `ConditionalWeakTable`; `IsAllowed` :115; `Send` :135 returns Sent, NotCapable or Refused |
| `server/customizations/Tutorial/TutorialGumps.cs:154-232` | `TutorialStationGump(station, canOpenWindows)`: `Windows` :157 maps a station's TazUO feature to its command and button words; `Offered` :167; a button per offered window; `OnResponse` :215 sends the command and shows the page again |
| `server/customizations/Tutorial/ClusterFTutorial.cs:124` | the stub station page passes `CanRunCommands(pm.NetState)` |
| `server/tests/Misc/TazUOClientCommandVerification.cs` (new) | 16 cases, below |
| `client/` (new) | `TAZUO_COMMIT`, `patches/`, `nuget.config`, `Build-Client.ps1`, `README.md` |
| `design/client_patching.md` | "Client code patches" section |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.10, one `### Staff` line (decision 3) |

## Tests

**Server** (`docker/uo/build.sh --tests-only`, the shard's test gate in a container):

- the handshake bytes (`CE 00 0B 00 01 00 00 00 01 00 04`);
- our patched client (answered 1 and 4) is sent exactly `CE len 00 04 00 00 "worldmap" 00`;
- a stock TazUO (answered 1 only), a client that answered nothing, and a null mobile get NotCapable and no bytes;
- six refusals: `cast Fireball`, `organizer`, `playlscript evil.py`, empty, a non-ASCII `e`, and `journal\n-cast Kill`.
  Each is refused even for our client, with no bytes;
- the whitelist is the patch's seven, and arguments and case are allowed (`radius 5 33`, `OptLink`);
- the four stations offer their window only when `canOpenWindows` is true; core.paperdoll and core.league offer none;
- the core.travel button sends `worldmap`.

Fail first:

- I replaced the helper with a stub that allows every command, knows no client and sends nothing, and forced the gump to
  offer nothing. **1,163 tests, 15 failed, all of them P103's**.
- I restored the real files (byte-identical copies kept in my scratchpad, then compared) and ran again: **1,163 passed, 0 failed**.

**Client** (`dotnet test tests/ClassicUO.UnitTests`): whitelisted lines parse, including arguments and case; nine lines
are refused (`cast Fireball`, `organizer`, `playlscript`, `sb`, empty, blank, `-worldmap`, a newline injection, non-ASCII);
too long is refused; the whitelist is the seven; a refusal logs once per name; `ClientCommand` is 4.

- Fail first: against a `TryParse` that accepts everything and a log that always fires, **21 run, 12 failed**.
- Real code: the whole suite **1,274 passed**, and again inside `Build-Client.ps1`'s clean worktree.

**Manual, not done (no one at the client):** the patched client logging in and a station button opening each window.
That is For Chase, step 2.

## Deviations and decisions for Chase

1. **Buttons go to clients that answered id 4, not every TazUO.** The brief says "answered the handshake as TazUO", but a
   stock TazUO answers that too (id 1). It has no id 4, so it would log "Received invalid enhanced packet 4" and the
   button would do nothing. So our patched client echoes id 4 when asked (`SendAck`, 6 lines). Stock TazUO, EA's
   client and ClassicUO keep the words only.
2. **The handshake goes to every client at connect.** No other way exists for the server to find out. The shard already
   sends a custom variable-length packet (0xF4) to every client at connect. 0xCE is variable length in ClassicUO's
   copy of the client's length table, so a client without a handler should skip it. **Not tested with EA's own client.**
   If one ever misbehaves, set `clusterf.tazuo.enhancedPackets` to False in modernuo.json: no handshake, and no buttons.
3. **Patch notes: a `### Staff` line, not a player line.** The brief asked for a `### Players` line. The changelog's own
   headings are Added, Changed, Fixed and Staff, and players cannot see this until our build ships. A player line now
   would announce buttons nobody has. When our build ships, add under `### Added`: "In the tutorial, the stations that
   teach the World Map, the Journal and the options window have a button that opens it."
4. **The patch is larger than "about 30 lines":** 9 lines in upstream files and an 87-line new file (whitelist, parsing,
   log-once, ack, and comments), plus the test. Upstream files are touched as little as possible, to make rebasing easy.
5. **Arguments are allowed** after a whitelisted name, as the existing commands take them (`radius 5`, `marktile -r`,
   `optlink <page>`), but only printable ASCII up to 100 characters. The tutorial sends names only.
6. **A minimal build script, not the full P-a pipeline:** no version stamp, no smoke start, no package gates. The package
   is unchanged.
7. **The scratch clone now carries a branch** (`sl/p103-client-command`, commit `761d2456d`) and a registered worktree,
   `D:\UO\tazuo-sl-build\src`. The build script replaces the worktree on its next run.

## For Chase

1. Nothing to deploy for players. The server change ships with the next test-shard deploy. It sends the handshake to
   every client and shows buttons only to the patched build.
2. **Manual check** (the brief's test), on the TEST shard after that deploy:
   - Run `D:\UO\tazuo-sl-build\client\TazUO.exe` (or rebuild it:
     `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\client\Build-Client.ps1`).
   - Point it at your UO data and the test shard.
   - Make a character still in the tutorial, and at the recruiter open "Core: Getting around", "Core: Speaking and the
     journal" and "Core: Walking, running and the camera".
   - Each page should show a button that opens the World Map, the Journal or the options window.
   - Your stock TazUO should show the same pages with no buttons.
3. To ship our build to players: cc-P40's P-a (or point `Build-PlayerPackage.ps1 -TazUO` at
   `D:\UO\tazuo-sl-build\client` after its own gates), then add the player line from decision 3.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

P103 DONE
