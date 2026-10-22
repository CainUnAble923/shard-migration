# P403: Music Room and area music review

Reviewed 2026-10-22 against ShatteredLegacy `1ecd9f3` and shard-migration `c99448b`. This is a review only. The findings from `notes/cc-P368-added-music-areas-monsters-bosses-codex-review.md` are excluded.

The server track list, assignment table, and package registry are still empty. The server and package findings below affect the paths used once tracks are assigned; the Music Room save findings affect the page now.

## Findings

1. **bug**, `web-console/static/music.js:176`: A failed autosave decrements `pending` just like a successful save, so the header says "all saved" and the refresh warning at line 193 no longer protects the unsaved text. Keep failed records dirty, retain a recoverable browser draft or retry them, and add a failed-request-then-refresh test.

2. **bug**, `web-console/static/music.js:172`: Editing a track while its earlier POST is pending can send another whole-record POST, and an older request arriving last overwrites the newer note while both requests report success. Serialize saves per track or reject stale revisions on the server, including edits from another tab, and test reversed request arrival.

3. **bug**, `web-console/static/music.js:179`: `flush()` waits only for debounce timers, so clicking Save to repo after an autosave has already started can commit the previous file and report success before the latest edit reaches disk. Track and await outstanding requests as well as timers, require successful saves before committing, and test Save to repo during a delayed autosave.

4. **risk**, `web-console/music.py:401`: An existing notes file that cannot be read or parsed is treated as an empty collection, so the next successful save can replace every prior note with one new record. Treat only a missing file as empty, refuse writes after read or schema errors while preserving the original, and add malformed-file and read-error tests.

5. **bug**, `player-package/payload/app/Build-UoOverrides.ps1:727`: A missing MP3 causes the launcher to omit its Config.txt entry, but the server still sends the assigned new ID, and the pinned client stops current music for an unknown ID instead of choosing the classic track. Add an availability-aware fallback to the area's remembered classic track and test a missing track and a player using an older package.

6. **bug**, `server/customizations/Music/ClusterFShardMusic.cs:590`: When a fight ends in a region whose music is `MusicName.Invalid`, including the default wilderness region, the watch drops the fight and sends `0x6D FF FF`, which the pinned client ignores, leaving a looping boss or monster track playing after combat. Explicitly stop music or restore the previous classic track for this return case, and test fight cleanup in a region without a music assignment.

7. **bug**, `player-package/payload/app/Build-UoOverrides.ps1:734`: If a launch builds Config.txt while one track is missing and another is present, restoring the missing MP3 later adds its file override but reuses a cached Config.txt that still lacks its ID. Include the accepted tracks in the cache stamp or validate the cached entries before reuse, and add a missing-then-restored-track test.

## Classic files

No finding for overwriting classic music files. `Build-UoOverrides.ps1:742` reads the player's Config.txt and writes the appended copy under the override directory at line 745; tracks use separate `sl-` names, and the package registry gate reserves IDs 105 through 149 (`Build-PlayerPackage.ps1:278`).

## Verification and missing coverage

- Ran `powershell.exe -NoProfile -ExecutionPolicy Bypass -File player-package/tests/Music-Overrides.Tests.ps1` in Windows PowerShell 5.1: **7 facts passed, 0 failed**. The tests cover additive overrides, skipped files, and cache changes to Config.txt or the shipped list, but do not cover restoring a missing MP3.
- Confirmed finding 7 with the real override builder and tiny scratch files: a list named 105 and 106, only 106 existed on the first run, then 105 was restored without changing the list or stock Config.txt. The second override list included `sl-one.mp3`, but the cached Config.txt still contained only stock 9 and new 106.
- Confirmed finding 4 with the real `MusicRoom.save_note`: after saving a note, a scratch notes file was made invalid JSON; `notes()` returned `{}`, and saving a different track replaced the file with only that track. No real Music Room notes file was written.
- Findings 1 through 3 were traced through `edit`, `send`, `flush`, `saveRepo`, `beforeunload`, and `status`, plus the threaded POST handler and `save_note`'s whole-record replacement. Browser reproduction is **unverified**: headless Edge failed to create its DevToolsActivePort file, so the planned browser probe could not run.
- For finding 5, read TazUO at the actual pin `3212623f63436be1c0f4e3b308b202b29597c026` with `git show`, since the reference checkout's working HEAD has later local commits: `src/ClassicUO.Renderer/Sounds/Sound.cs:50` returns no music for an unknown Config.txt ID, and `src/ClassicUO.Client/Game/Managers/AudioManager.cs:281` stops the current track. The server sends the new IDs at `ClusterFShardMusic.cs:245` and `:541` without checking the player's installed music.
- For finding 6, pinned ModernUO `d4531cd94b739613155225c234900de9f47d2c88` creates the default region at `Projects/Server/Maps/Map.cs:119`; `Projects/Server/Regions/Region.cs:166` and `:229` give it `Invalid` (-1). `Projects/Server/Network/Packets/OutgoingPlayerPackets.cs:278` writes that value into the packet; the pinned TazUO handler at `src/ClassicUO.Client/Network/PacketHandlers/PlayMusic.cs:15` recognizes `1F FF` as stop, while its audio manager at line 238 rejects the out-of-range value from `FF FF`.
- `web-console/tests/test_music_room.py:220` checks successful note round trips, and `:321` waits for a successful browser save; neither exercises failed requests, overlapping saves, refresh recovery, a pending save at commit time, or an unreadable existing file. `server/tests/Misc/ShardMusicVerification.cs:223` tests fight return into a region with a valid track, and `:354` checks ID ownership; neither tests missing client audio or return into an unscored region.
- Server behavior and audible playback are **unverified in a running shard/client**. No server build was run and no new tests were added in this review.
- Ran the working agreement's progress command with `--dry-run` and work-copy path overrides; it completed successfully but still rewrote `tools/progress.json`, so that generated change was restored. The deliverable remains this note alone.

## Files reviewed

ShatteredLegacy:

- `web-console/music.py`, the Music Room routes and hourly commit hook in `web-console/server.py`, `web-console/static/music.html`, `music.js`, `music.css`, and the nav link in `web-console/static/index.html`.
- `web-console/tests/test_music_room.py` and its local browser helper `web-console/tests/cdp.py`.
- `server/customizations/Music/ClusterFShardMusic.cs`, `ShardMusicTracks.cs`, `ShardMusicTable.cs`, and `server/tests/Misc/ShardMusicVerification.cs`.
- `player-package/vendor/shattered-legacy-music/registry.csv`, `SOURCE.txt`, `Add-Track.ps1`, the music sections of `player-package/Build-PlayerPackage.ps1` and `player-package/payload/app/Build-UoOverrides.ps1`, and `player-package/tests/Music-Overrides.Tests.ps1`.
- `.gitignore`, `client/TAZUO_COMMIT`, and the client patch list checked for changes to the audio paths.

Read the P367 and P368 implementation notes and the P368 Codex review before reviewing these files. Scratch probes are under the git-ignored `ShatteredLegacy/downloads/P403/`, proven with `git check-ignore`; no tracked code, tests, or `docs/` files were changed.

P403 DONE
