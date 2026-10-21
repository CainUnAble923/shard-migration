# CC task P240: Fog of war, the TazUO half (F-6)

Iron, 2026-10-21. Both repos were clean on `golem/Iron/P240` when I started. **Paused at Chase's request** after the
client manager and its tests were written and green. The continuation is `cc-P352-cont-fog-of-war-client-half.md` in
the queue. Our TazUO source is `D:\UO\tazuo-sl-build\src` (TazUO `3212623f` plus patches 0001-0003); paths below are
relative to its `src\ClassicUO.Client\` unless they say otherwise.

## Headlines

- **TazUO has no fog of war** and no explored-area option. Its world map takes no overlays or plugins. So the fog is a
  change to our own build: one more client patch, the way 0001-0003 are carried.
- **The ClusterF client half is gone.** "FogOfWarManager" appears only in the server's own comment. No repo, folder or
  commit on this PC, its Google Drive or GitHub ever held the client file.
- **0xF4 is free from server to client.** Our TazUO already has it as a variable-length packet with no handler, so
  today it reads the length and skips it. Every live player has been receiving it unread.
- **The route is small, about one sitting:**
  - a manager that reads 0xF4 and keeps each facet's explored chunks;
  - a chunk-resolution fog texture, drawn over the world map with the map's own source rect, rotation and origin,
    scaled by 8;
  - a toggle in the world map's right-click menu;
  - a reset at login.
- **Built so far (outside the repos, saved in the notes):** the manager, `ShardFogOfWar.cs`, and 8 unit tests. 7 of
  them were seen failing against a stub, and all are green with the real file. All 1,300 client unit tests pass.
- **Left for P352:** wiring (handler, reset, profile setting, menu entry, the draw), patch 0004, building our TazUO and
  the package to scratch, and patch notes.
- **One server finding, not changed (no server work in this prompt):** the exploration code exists twice, in two
  files, so every login sends the full fog data twice.

## Part 1: check first

**(a) Fog or explored area in our TazUO: none.**
- `Game\UI\Gumps\WorldMapGump.cs` (4,253 lines) and the whole client source contain no "fog", "explor" or "reveal".
- The map is the facet's full art, drawn at once (`Draw`, `:2361`; the map texture `:2434-2470`).

**(b) Overlays or plugins without a fork: no.**
- The world map has no layer hook. It draws the map texture, then `DrawAll` (markers, mobiles, corpses, the
  path), all inside the gump.
- ClassicUO plugins get packets, not the world map's batcher.
- Legion scripting's world-map API places markers, not layers.
- So the fog needs a change to our build.

**(c) What our build changes, and how a change rides upstream updates.** `client\README.md` (cc-P103):
- upstream TazUO at `client\TAZUO_COMMIT` (`3212623f`, v26.0909.63) plus `client\patches\*.patch`, applied in order
  with `git apply`;
- built by `client\Build-Client.ps1` (worktree at the pin, submodules checked, patches, unit tests, `dotnet publish`);
- today's patches:
  - 0001: ClientCommand, enhanced packet 0xCE id 4;
  - 0002: the paperdoll bodies option;
  - 0003: the shard buttons (Achievements);
- the README's rebasing recipe carries each patch onto a newer upstream (`git am`, fix, `git format-patch`).

The fog becomes 0004, the same way. It touches four upstream files lightly (the handler list, EnterWorld, Profile,
WorldMapGump), plus one new file, so a rebase has little to resolve.

## Part 2: the lost client half

**Gone.** Searched:
- **`D:\UO`**, every folder except other Golems' desks and `shard-migration`, for `FogOfWarManager` in `.cs`, `.md` and
  `.txt`: only copies of `ClusterFExplorationManager.cs` (bot-shard, test-shard-src, the cc-pNN work trees,
  ops-proof) and the queue entry.
- **`C:\Users\ckfle`** and `D:\` to depth 4 for a ClusterF folder: only `C:\Users\ckfle\clusterf-infrastructure`.
  - That is the old homelab repo. Its `containers\uo\README.md` describes a stock ClassicUO connecting.
  - `git grep FogOfWarManager` over every commit finds only the server file (added in `4fbe6eb`, 2026-05-22, "Phase 4
    polish ..."). No client file was ever committed.
- **`G:\My Drive`** (Google Drive), `D:\Servers` and `D:\Server Backups`, by name (`*FogOfWar*`, `*ClassicUO*`,
  `*clusterf*`): nothing.
- **GitHub** (`gh repo list`): `clusterf-infrastructure` is the only ClusterF repo; no client fork.

**The server's layout, read either way.** `server\customizations\ClusterFExplorationManager.cs`:
- `:12-24` the header ("sends that state to the ClusterF custom client (ClassicUO fork) via packet 0xF4");
- `:30-38` the facet sizes (Felucca and Trammel 6144x4096, Ilshenar 2304x1600, Malas 2560x2048, Tokuno 1448x1448,
  TerMur 1280x4096);
- chunk 8x8, `ExploreRadius` 2 chunks (plus the mule's Survey Saddle Roll);
- `:134` the packet ID; the layout comment above it, and the send code `:187-199`:

  | Bytes | Field |
  |---|---|
  | 1 | `0xF4` |
  | 2 | total length, big-endian |
  | 1 | sub |
  | 1 | facet |
  | 4 | payload length, big-endian |
  | N | payload |

- the subs:
  - **0x01**: full explored, gzip of `BitArray.CopyTo` bytes; bit i is chunk `cy * width + cx`, least significant
    bit first;
  - **0x02**: delta, a big-endian u16 cx and u16 cy per newly walked chunk;
  - **0x03 / 0x04**: mining depletion, full and delta;
- login sends all six facets 2 s after `Connected`; walking sends deltas.

**The duplicate.** `ClusterFExplorationSync.cs` (namespace `Server`) defines the same three classes as
`ClusterFExplorationManager.cs` (namespace `Server.Custom`), and both have an `Initialize` that registers
`EventSink.Movement` and `EventSink.Connected` (Sync `:324-331`, Manager `:280-284`).
- Walking is harmless: the second handler finds the chunks already marked and sends nothing.
- Each login sends every facet's full explored set (and the depletion sets) twice. Sync also resends depletion to
  everyone every 5 minutes.
- A later server prompt should delete one of the two. Not touched here: no server change in this prompt.

## Part 3: packet 0xF4

Checked; it is free from server to client:
- **Our TazUO:**
  - `Network\PacketsTable.cs:256`: `-1, // f4`, so variable length, read from bytes 1-2, as the server writes it.
  - `Network\PacketHandlers\HandlerRegistry.cs:118-125`: handlers 0xF0, 0xF1, 0xF3, 0xF5, 0xF6, 0xF7; **none for
    0xF4**. So the parser skips the packet whole (`PacketParser.cs`, `AnalyzePacket` with no handler).
  - The one `0xF4` in its outgoing code (`Network\OutgoingPackets.cs`, `Send_InvokeVirtueRequest` `:3048`) is a payload
    byte inside packet 0x12, not a packet ID.
  - Our patches 0001-0003 use 0xCE only.
- **Pinned ModernUO:** 0xF4 is a client-to-server `CrashReport` (`Server\Network\Packets\IncomingPackets.cs:98`), the
  other direction. Nothing in pinned sends 0xF4.
- **Our server:** only `ClusterFExplorationPackets`. `TazUO\TazUOClientCommand.cs:18` notes it already goes to every
  client at login.

No new ID is needed.

## Part 4: the route, with effort

**One sitting.** It does not need a fork beyond one more patch:
1. **`Game\Managers\ShardFogOfWar.cs` (new, written):**
   - the server's facet table (the client's map files can be larger, Felucca 7168 wide, but the chunk index uses the
     server's widths);
   - one byte array per facet;
   - `Receive` (the 0xF4 handler), `Apply` (sub 0x01 gunzip, 0x02 deltas, depletion ignored), `IsExplored`, `Reset`;
   - `FogPixels`: one pixel per chunk, fog `0xD8000000` (black at 216/255), clear 0. It adds one extra column and row
     of fog, so the map beyond the server's edge stays dark under clamp sampling;
   - `Texture`: rebuilt only when the data or facet changed (Felucca is 769x513, under 1.6 MB).
2. **`HandlerRegistry.cs`:** `(ShardFogOfWar.PacketId, ShardFogOfWar.Receive)`.
3. **`EnterWorld.cs`:** `ShardFogOfWar.Reset()` at login, so a shard that sends nothing shows no fog. The shard
   resends everything on each login.
4. **`Profile.cs`:** `WorldMapShowFog`, default true (beside `WorldMapFlipMap`, `:442`).
5. **`WorldMapGump.cs`:**
   - a "Fog of war" entry in `BuildOptionDictionary` beside `flip_map` (`:358`), added to the menu beside it (`:702`),
     saved like the others;
   - in `Draw`, right after the map texture (`:2459-2470`), when the setting is on and
     `ShardFogOfWar.HasData(_map.Index)`:
     - source rect in chunks: from `floor((centerX - size_zoom_half) / 8) - 1`, `size_zoom / 8 + 3` wide and high;
     - drawn with the float overload `Draw(texture, position, source, hue, rotation, origin, scale, effects, depth)`
       (`ClassicUO.Renderer\Batcher2D.cs:1044`);
     - position: the map's (`gX + halfWidth`, `gY + halfHeight`);
     - rotation: the map's (45 degrees when flipped);
     - origin: `(worldCenter - chunk0 * 8) / 8` texels, where `worldCenter = (centerX - size_zoom_half) + size_zoom / 2f`
       is the point the map is drawn around;
     - scale: `8 * size / size_zoom`.
     
     The batcher reads origin as a fraction of the source rect and multiplies scale by the source width
     (`Batcher2D.cs:1056-1092`), as XNA does. So the fog lines up with the map tile for tile at every zoom, flipped or
     not, without rounding. It uses point-clamp sampling (`Batcher2D.cs:92`), so chunk edges stay crisp.

**Dungeons:** they are on the same maps east of x 5120 (Felucca and Trammel), inside the server's 6144 width, so they
are fogged and revealed like anywhere else (a test covers x 5300). **Every facet** the server tracks (0-5) is drawn;
a facet it has no table for gets none.

Only walked chunks reveal. Cartography reveals are later (F-6), and need only another sub or more deltas from the
server.

## Part 5: built so far

Outside both repos, in `D:\UO\cc-p240-work\tazuo` (`Build-Client.ps1 -Out D:\UO\cc-p240-work\tazuo -SkipTests`, the
pin plus 0001-0003; the scratchpad path was refused by the script's "inside a repo" guard because it contains
"shard-migration"). Saved for P352 in `notes\cc-P240-files\`:
- `ShardFogOfWar.cs`: the manager above (route step 1).
- `ShardFogOfWarTests.cs`: 8 tests:

| Test | What it checks |
|---|---|
| `The_chunk_table_is_the_servers` | 768x512 (Felucca), 288x200 (Ilshenar), 181 (Tokuno), 512 (TerMur) |
| `A_known_chunk_bit_reveals_exactly_that_chunk` | a full set built the server's way (BitArray, CopyTo, gzip) with chunk (400, 300) on Trammel: exactly one clear pixel, that one; the layer is 769x513 |
| `A_dungeon_chunk_east_of_5120_is_kept_like_any_other` | Felucca x 5300 |
| `A_delta_reveals_the_listed_chunks_and_only_on_its_facet` | (5, 7) and (256, 2) on Malas; Ilshenar untouched |
| `The_servers_packet_parses_through_the_handler` | a whole 0xF4 packet through `Receive`, the reader after id and length as the parser hands it |
| `No_data_means_no_fog` | no facet has data, no pixels, after a reset |
| `Mining_depletion_and_bad_data_draw_nothing` | subs 0x03 and 0x04, bad gzip, a facet out of range |
| `A_new_login_starts_empty` | `Reset` clears and bumps the version |

Runs (`dotnet test tests\ClassicUO.UnitTests\ClassicUO.UnitTests.csproj -c Release` in the dev tree):

| Run | Tree | Result |
|---|---|---|
| red | the tests plus a stub with the same API (no data, no table; marked P240-RED) | **7 failed, 1 passed of 8**. Every test that expects fog or a revealed chunk failed. `No_data_means_no_fog` passed, as it must against a stub that has no data |
| green | the real `ShardFogOfWar.cs` | **1,300 of 1,300 passed**, the 8 new among them |

**Not done (paused):** route steps 2-5 (the wiring and the draw), patch 0004, our TazUO built with tests through
`Build-Client.ps1`, the package build to scratch, and the patch notes.

## Deviations and decisions for Chase

1. **The toggle lives in the world map's right-click menu** ("Fog of war", beside "Flip map", saved in the profile like
   every other world-map setting), not the main Options window. TazUO keeps all world-map settings there. Say if you
   want it in Options too.
2. **Fog strength:** black at 216/255, so the land shows faintly under it. One constant (`FogAlpha`).
3. **The server's duplicate exploration code** (Part 2): a small server prompt should delete one copy. That halves
   the login burst and stops the double depletion resend.
4. **Mining depletion (subs 0x03 and 0x04)** arrives too. The client ignores it for now; it could become a "mined
   out" haze on the map later (F-6 tie-ins).
5. **The scratch build folder is `D:\UO\cc-p240-work`**, not the session scratchpad, whose path contains
   "shard-migration" and is refused by `Build-Client.ps1`'s guard. It is outside both repos and can be deleted after
   P352.

## For Chase

Nothing to check in the client yet: P352 builds and packages it. When it lands:
- a fresh character's world map is dark;
- walking clears 8x8 chunks around them (about two screens' radius);
- relogging keeps what was walked;
- "Fog of war" in the world map's right-click menu hides the fog;
- another shard shows no fog.

## Continuation

- **Done:** Parts 1-4 (check first, the lost half, the 0xF4 check, the route and effort); the manager and its 8
  tests, red then green; findings for the server.
- **Left:** everything in `D:\UO\cc-prompts\queue\cc-P352-cont-fog-of-war-client-half.md`: the wiring in four upstream
  files, patch 0004 and the README row, `Build-Client.ps1` with tests, P124's package build to scratch, patch notes,
  notes, preflight.
- **Mid-flight:** nothing in either repo. The dev tree `D:\UO\cc-p240-work\tazuo` holds the two files (with the
  pin's patches staged) and can be reused or rebuilt. No lock is held.
- No CHANGELOG entry yet: nothing a player sees has shipped. P352 writes it.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P240 -NoRefresh`
(the hand-off's work copies in place of the real folders). It commits nothing; neither repo is BLOCKED:

```
Repo Result
---- ------
code clean
docs dry run
```

- **docs: 3 files**: this note and `notes\cc-P240-files\` (`ShardFogOfWar.cs` 8 KB, `ShardFogOfWarTests.cs` 6 KB).
- **code: clean.** No code-repo change at the pause, so both repos build as they did, and their tests are unchanged.

P240 PAUSED
