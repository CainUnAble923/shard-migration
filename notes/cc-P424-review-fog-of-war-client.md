# P424: Review of the world map fog of war client patch

Reviewed October 22, 2026. Notes only; no code changes.

Read the P240, P352, and P357 notes. No earlier P352 Codex review was found beside them or by searching the review notes for P352, the patch name, and ShardFogOfWar. The duplicate server hooks and the pending visual alignment check were already reported, so they are not new findings here.

## Findings

1. **bug** - `client/patches/0004-world-map-fog-of-war.patch:135` (`ShardFogOfWar.Apply`): A full sync that decompresses to fewer bytes than the facet needs still replaces its explored bitset with a partially filled or empty array, hiding areas already explored in this session; a diagnostic against the P352 client confirmed that both a valid gzip containing one zero byte and an empty payload return true and clear a previously explored chunk. Require exactly the expected decoded length before replacing the old bitset, reject excess decoded data too, and add regression cases that preserve existing bits and Version when a full sync is rejected.

2. **risk** - `server/customizations/ClusterFAccountData.cs:98`: The server retains exploration under every character serial without removing deleted characters, so repeated character deletion and creation can grow an account's map records and save payload indefinitely; each login allocates all six facet bitsets, totaling 130,080 payload bytes per character from the current map table, even before that character explores anything. Remove only the deleted character's entry through the player deletion lifecycle, with a regression check that another character's explored areas survive; this is an existing server dependency, not growth introduced in the client patch.

3. **risk** - `client/patches/0004-world-map-fog-of-war.patch:217` (`ShardFogOfWar.Texture`): Every exploration update observed by an open world map rebuilds and uploads the entire facet texture, including scanning 393,216 chunks and allocating a 1,577,988-byte pixel array on Felucca, while the global Version also invalidates it for other facets and repeated deltas that change no bits. Keep reusable pixel storage and a revision per facet, skip unchanged deltas, and consider uploading only changed regions after measuring walking with the map open; actual frame time and GPU cost remain unverified.

4. **risk** - `client/patches/0004-world-map-fog-of-war.patch:509` (`A_new_login_starts_empty`): The login test calls Reset directly, so it would still pass if the EnterWorld reset hook were removed and exploration leaked into the next character or shard. Exercise the actual login handler or packet dispatch with populated state, then a replacement full sync and walking delta, and check that a subsequent shard that sends no exploration packets starts without fog.

## Scope checks

- **Client map data growth:** No unbounded retained map collection found. `ShardFogOfWar` has six fixed-size byte arrays and one cached texture; deltas set bits rather than append entries, and texture resizing disposes the old texture. The allocation churn in finding 3 is separate from retained growth.
- **Lost saves of explored areas:** No normal server serialization omission found in the inspected code. `ClusterFAccountData.cs:484` reads exploration and `:535` writes it; `ClusterFAccountPersistence` saves those records at `:1135`. `server/tests/Misc/AccountDataSerializerVerification.cs:512` already compares every exploration bit across serialization for two characters. Finding 1 loses the client's displayed copy, not the server's saved bits; a later valid full sync can restore it. A server save and restart was not run.
- **Other clients:** The pinned stock TazUO has a variable-length entry for 0xF4 in `Network/PacketsTable.cs:256` and no handler in its original registry; `Network/PacketHandlers/PacketParser.cs:181` checks for a handler before dispatch, so stock TazUO continues to show its normal map. The patched client also allows the fog to be turned off, so this feature does not enforce hidden geography. Official-client and other ClassicUO fork behavior was not verified.
- **Missing tests:** Besides finding 4, the existing fog suite does not cover short or empty full syncs overwriting populated state, excess decoded bytes, duplicate deltas leaving Version unchanged, or texture work after an unrelated facet changes. The server serializer test covers a record round trip, not deletion cleanup or a complete server-save-to-client-login cycle. Add those cases with the corresponding fixes, observing each new regression fail first.

## Evidence and verification

Reviewed all six patch targets: `Configuration/Profile.cs`, `Game/Managers/ShardFogOfWar.cs`, `Game/UI/Gumps/WorldMapGump.cs`, `Network/PacketHandlers/EnterWorld.cs`, `Network/PacketHandlers/HandlerRegistry.cs`, and `tests/ClassicUO.UnitTests/Game/ShardFogOfWarTests.cs`, plus `client/README.md`. Also traced `server/customizations/ClusterFExplorationManager.cs`, `ClusterFExplorationSync.cs`, and `ClusterFAccountData.cs`, the account serializer test, and the pinned ModernUO player deletion and serialization paths.

Patch citations above are physical line numbers in the canonical patch, not line numbers in its generated client files. Existing source at `D:\UO\cc-p352-work\tazuo\src` is at the configured TazUO pin `3212623f63436be1c0f4e3b308b202b29597c026`; reverse application checking of patch 0004 passed, and its SHA-256 matches the P352 client's build manifest: `118507f7f588379745da2992e5be6c07bbbb035d70d6be9a0d977e9399a9af37`.

Ran the existing `ShardFogOfWarTests` from that build with `dotnet vstest` under Windows PowerShell 5.1: 10 passed, 0 failed, 0 skipped. A temporary diagnostic outside both repositories called the existing client assembly and confirmed the overwrite in finding 1, the pixel-array size, and Version changes on other-facet and duplicate deltas. No regression tests were added and no fixes were made. No client window, graphics device, server, Docker daemon, or Haven connection was used.

The diagnostic is in `C:\Users\ckfle\AppData\Local\Temp\p424-fog-review-f5c5d687bb65411cb37bd301e41f5233\Probe.cs`, with its small compiled runner beside it; it uses the existing P352 assemblies without copying them. The filtered test run used `FullyQualifiedName~ShardFogOfWarTests`. The progress reporter completed with `--dry-run` and paths set to these work copies; it still rewrote `tools/progress.json`, so that generated file was restored to its original content. Only this review note remains changed.

P424 DONE
