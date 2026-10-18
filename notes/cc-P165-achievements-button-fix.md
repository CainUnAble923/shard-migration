# cc-P165: Achievements button does not appear in game (P147 play test failed)

2026-10-18. Opus. Prompt: `D:\UO\cc-prompts\cc-P165-cont-achievements-button-fix.md`. Not committed (the Golem commits
after DONE). All three repos were clean at the start.

## Headlines

- **The cause, in one sentence:** the server sent the TazUO handshake (0xCE id 1, "please use id 4") from
  `EventSink.Connected`. ModernUO raises that inside `PlayCharacter` right after `state.BlockAllPackets = true`, so
  `NetState.Send` silently dropped it on every real login. No client ever learned that the shard offers id 4, so
  `ShardButtons.Available` stayed false and both buttons stayed hidden.
- **The fix is server only:** the handshake now goes from `PlayerMobile.PlayerLoginEvent`, which `DoLogin` raises
  last, after the login timer has unblocked packets. The client patch was right all along and is unchanged, so no
  client rebuild and no new package are needed for this fix.
- **It also explains P103.** The tutorial's "Open the World Map / Journal / Options" buttons have the same dependency
  (the server sends them only to a client that answered id 4), so they cannot have shown either. They should appear now
  too. That follows from the same fix but was not seen in game (Deviation 4).
- **Proved live on the test shard**, which now runs `sl-modernuo:cc-p165` (HEAD plus this fix, healthy, tagged
  `good-ab51d83-dirty`). A debug build of our client logged each step:
  - the handshake **arrives** (`recv 0xCE id=1`), and the client lists ClientCommand as enabled;
  - it **answers** id 4 (`SendAck: ClientCommand enabled=True`);
  - **`Available` goes true**;
  - the **top-bar Achievements button turns visible**;
  - the **paperdoll** sees `avail=True` with the button art present (`tex=True`), so it shows Achievements in Help's
    slot.
  - Then the button's own send function was called once. Before it: no server gumps. Three seconds after:
    **Eve's "Achievement Records" page is open** ("League of Extraordinary Citizens", AP 650, Renown 1535, the
    category tabs).
  - The server logged no refusal and no error.
  - **Before the fix**, the same build on the old server logged only "avail=False": not one 0xCE packet arrived.
- **A fact that would have caught it**, seen red first:
  - `TazUOHandshakeLoginVerification` logs in the way `PlayCharacter`, its login timer and `DoLogin` do: block
    packets, attach the NetState, unblock, then the login event.
  - **Old code:** expected 1 handshake, got 0. That was the only failure in 1,455.
  - **New code:** 1,451 passed, 0 failed, 4 skipped.
  - P103's and P147's facts never saw the bug, because they attached the NetState with nothing blocked.

## What changed

D:\ShatteredLegacy (uncommitted):

| File | Change |
|---|---|
| `server/customizations/TazUO/TazUOClientCommand.cs` | Header :7 ("at login") and the cc-P165 paragraph :21-27 (why and when); `using ModernUO.CodeGeneratedEvents;` and `Server.Mobiles` :33, :35; `Configure` no longer subscribes `EventSink.Connected` :86-90; new `OnLogin` :92-106, `[OnEvent(nameof(PlayerMobile.PlayerLoginEvent))]`, sends the handshake when `clusterf.tazuo.enhancedPackets` is on, and logs a warning instead of sending if packets were still blocked |
| `server/tests/Misc/TazUOHandshakeLoginVerification.cs` (new) | 3 facts: a real-order login gets the handshake exactly once; nothing is sent while packets are blocked; with the setting off, none is sent. The ModernUO lines it copies are cited in its header (`IncomingAccountPackets.cs` at d4531cd9: PlayCharacter :289-295, LoginTimer :637-638, the login event :341-344) |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.18.10`: one `### Fixed` player line (the button, and the tutorial's open buttons) and one `### Staff` line; VERSION 2026.10.18.9 -> 2026.10.18.10 (.9 was committed with P164) |

Not changed: `client/patches/0003-shard-buttons-achievements.patch` and every other client file.

Outside both repos:
- **The test shard** runs `sl-modernuo:cc-p165` (`Start-TestShard.ps1 -Image sl-modernuo:cc-p165`; `latest` not
  moved).
- **Docker images** `sl-uo-builder:cc-p165` and `sl-modernuo:cc-p165` / `good-ab51d83-dirty` exist.
- **`D:\UO\p165-debug\screenshots\`** holds the debug client's own screenshots, game only, nothing of the desktop:
  `p165-buttons_*.png` (buttons up) and `p165-page_*.png` (the page open), plus `debug-log.txt`. The debug client
  itself was deleted.
- **The debug lines** in the TazUO build tree (`D:\UO\tazuo-sl-build\src`) were put back from byte copies; no debug
  text is left there. The shipped `D:\UO\tazuo-sl-build\client` was never touched, apart from the empty
  `Logs\Network` folder my `-packetlog` tries made, which I removed.

## How it was found

1. **Launched the shipped test client exactly as "SL TEST - Admin" does** (`Play.ps1`'s own `Get-TazUOLaunch`), with
   TazUO's `-packetlog`.
   - The shard log showed the login and the character list, but the packet log stayed empty. TazUO's logger appears
     not to write in this build (not pursued).
2. **A debug build** (same source, five files with log lines, published to `D:\UO\p165-debug\client`) showed the
   client entering the world (Eve's paperdoll, serial 80272) with `avail=False`, and **no 0xCE packet ever
   arriving**. The art was fine (`tex=True`).
3. **The client drops nothing:** `PacketParser.AnalyzePacket` dispatches every packet in any scene, and 0xCE is
   registered.
4. **The server:** `TazUOClientCommand` sent on `EventSink.Connected`, which `Mobile.NetState`'s setter raises.
   - In `PlayCharacter` that setter runs right after `state.BlockAllPackets = true`.
   - `NetState.Send` returns early on `CannotSendPackets()`, which includes `BlockAllPackets`
     (`Server/Network/Packets/OutgoingPackets.cs:12`).
   - Character creation does the same (`:198`, `:207`).
5. The prompt's other suspects were cleared:
   - `-skiploginscreen` and the settings file: the client logs in normally;
   - "handshake before the paperdoll and top bar exist": with the fix it arrives after both, and both refresh in
     `Update()`;
   - gump ids and art: present;
   - admin or AccessLevel: no difference in the code path.
6. **The other `EventSink.Connected` users** are fine:
   - the exploration packet (`ClusterFExplorationManager`, `ClusterFExplorationSync`) waits 2 seconds, past the
     block;
   - `ClusterFWeightPatch` sends nothing.

## Tests

**New: `server/tests/Misc/TazUOHandshakeLoginVerification.cs`**, 3 facts:

| Fact | Red (old `TazUOClientCommand.cs`) | Green |
|---|---|---|
| `AClientThatLogsInTheRealWayGetsTheHandshakeOnce` | **FAILED**: expected 1, actual 0 | passed |
| `NothingIsSentWhilePacketsAreBlocked` | passed (it pins ModernUO's blocking, which the fix relies on) | passed |
| `WithTheHandshakeTurnedOffNoneIsSentAtLogin` | passed (the old code sent nothing at login either) | passed |

**Full shard route** (`docker/uo/build.sh`, its own builder tag):
- **Red:** with the old file swapped back in, 1,455 total, **1 failed** (the fact above), 1,450 passed, 4 skipped.
  The file was restored afterwards and SHA-256 checked.
- **Green:** `build.sh -t sl-modernuo:cc-p165`, **1,455 total: 1,451 passed, 0 failed, 4 skipped**, and the image
  built.

**Client tests:** not re-run, since no client file changed (P147 recorded 1,292 of 1,292 on this patch set).

**Live:** the test shard on `cc-p165`, the debug client, the log above. The debug log is at
`D:\UO\p165-debug\screenshots\debug-log.txt`.

## Deviations and decisions for Chase

1. **The red run was stopped by Claude Code for low memory**, while the session was idle (the PC had 1.4 GB of 32 GB
   free; WSL held 7.4 GB). It had already finished: its output has the full result, quoted above.
   - Its last step, putting the fixed `TazUOClientCommand.cs` back, never ran. I restored the file myself and checked
     its hash.
   - I freed the .NET build servers (about 1.6 GB back) and ran the green build in the foreground.
2. **Reading the debug client's screenshot with the Read tool was auto-denied** (unattended run):
   `Read D:\UO\p165-debug\client\Data\Client\Screenshots\p165-buttons_2026-10-18_04-48-58.png`, to look at the
   paperdoll and top bar myself. I did not retry it another way.
   - So **I have not seen the screenshots.** The evidence that the buttons show is the debug log (the visible states
     and art lookup), and that the page opens is the list of open server gumps.
   - The screenshots are in `D:\UO\p165-debug\screenshots\` for you to look at. They are the client's own back
     buffer (the game window only). They are not in either repo, since I have not seen them.
3. **Two desktop captures were taken and deleted.** Early on I captured the screen (Pillow `ImageGrab`) to find the
   game window. It showed your desktop and this terminal, not the game, so I deleted both and switched to the
   client's own screenshot function. Nothing from them was kept or published.
4. **The press was the button's own send function, not a mouse click.** The debug build called
   `ShardButtons.Send("achievements")` once, which is what the button's click handler calls. I did not move your
   mouse.
   - The click itself (TazUO's standard `ButtonAction.Activate` to `OnButtonClick`) was not exercised: **that is your
     P147-1 / P147-3 check**.
   - The tutorial's P103 buttons were not tried in game either.
5. **The test shard now runs `sl-modernuo:cc-p165`**: HEAD `ab51d83` plus this fix (the label says dirty). It is the
   same code the Golem's commit will hold. **Shard Console > Test shard: Rebuild** after the commit puts it on `latest`
   the usual way.
6. **No client rebuild or package**: the client patch had no bug. The prompt expected a client change; none was needed.

## For Chase

1. **The test shard already has the fix** (`cc-p165`). After the Golem commits, **Shard Console > Test shard:
   Rebuild** puts it on `latest`. Either way the fix is live now.
2. **No new player package is needed for this fix**: the client is unchanged. Your test client
   (`D:\UO\tazuo-sl-build\client`, the one P147 built) already has the button. If players have not had P147's package
   yet, **Player package: Build, then Publish** gives it to them, as P147 said.
3. **Log in with SL TEST - Admin (or any character) and look:**
   - **Paperdoll** (your own, classic style): **Achievements** where Help was;
   - **Top bar**: **Achievements** at the right end, after More + and Xml Gumps;
   - click either: your **Achievement Records** page opens;
   - another character's paperdoll still shows Help; stock TazUO shows nothing new.
4. **On the play-test page, set P147-1 and P147-3 back to open** (Reopen on each card, or `/api/result` with status
   `open`) and test them again. I did not change them, since the page is on Haven.
5. **Also worth a look:** the tutorial's "Open the World Map", "Open the Journal" and "Open Options" buttons (P103)
   should now appear at the core.travel, core.chat and core.movement stations for our client.
6. **The debug screenshots** are in `D:\UO\p165-debug\screenshots\` if you want to see them. Delete the folder when
   done.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

- No repo BLOCKED.
- `code`: this prompt's 4 files.
- `docs`: these notes, plus `testing/SUMMARY.md` and `testing/play-tests.json` (the mirror refresh, machine output).
- No file over 5 MB. Scratch and the debug folder are outside both repos.

P165 DONE
