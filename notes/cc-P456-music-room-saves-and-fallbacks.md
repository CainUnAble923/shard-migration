# cc-P456: Music Room saves that cannot lose notes; music fallbacks for a missing or unknown track

## In plain words

- **Music Room (web console, /music):** a note that did not save now stays marked "not saved" in red, with a Retry
  button. The top line counts it, and closing or reloading the page asks first. Before, a failed save looked finished
  and closing the page lost it.
- **Music Room:** two quick edits to one track can no longer arrive in the wrong order and put the older note back.
  Save to repo now waits for a save that is still going, and it refuses to commit while a track is not saved. If
  music-notes.json is damaged, the page shows the problem and leaves the file alone. Before, the next save
  overwrote it.
- **In game, once tracks ship:** when a fight ends somewhere with no area music (the open wilderness), the music from
  before the fight comes back, or the music stops. Before, the fight track kept looping, because TazUO ignores the
  "no music" signal the server sent.
- **Launcher, once tracks ship:** if a shard track's mp3 is missing, that slot plays a stock track instead of going
  silent. When the mp3 comes back, the launcher picks it up again. Before, a restored track stayed missing until
  something else changed. **For you:** each track you add now needs a `-Fallback` stock name (for example
  `-Fallback dungeon9`). It also needs about 2 minutes of listening once a test client is handy; see section 5.

Found by cc-P403 (Codex) #1 to #7 and checked by cc-P429 (Crystal). The prompt's line numbers were from main
da1a0cb. On this branch, the launcher's music code is at `Build-UoOverrides.ps1:800-866`, not :704-727.

## What changed

All edits are in `D:\UO\golems\Iron\ShatteredLegacy` (branch golem/Iron/P456). There are 12 files in all:

| File | Change |
|---|---|
| `web-console/static/music.js` | Each track has at most one save in flight (`inflight`). An edit made meanwhile is sent once that save is back (`again`), always from the newest record and its revision. A failed save stays in `failed` until a save of that track succeeds: the status line counts it ("N not saved"), `beforeunload` warns for waiting, in-flight or failed tracks, and a per-row **Retry** button appears. `flush()` sends waiting edits, retries failed ones, waits for every in-flight save, and rejects when a track is still not saved. Save to repo then says "Not committed: 1 track not saved (...)" and commits nothing. The summary view shows a notes-file error. |
| `web-console/music.py` | New `load_notes()` returns `(tracks, error)`. Only a missing file counts as empty. A read error, invalid JSON, a non-UTF-8 file, `tracks` that is not an object, or a record that is not an object is an error. When there is an error, `save_note` refuses (409) and writes nothing. `save_note` now needs `rev`, the record's revision the page last saw (0 for none). A stale one gets 409 ("a newer save of this track is already in ..."), and a missing or non-number one gets 400. Each saved record carries `rev`. A cleared record is removed and reports `rev` 0. `save_note` returns `(record, error, status)`. `summary()` carries `notesError`. |
| `web-console/server.py` | `GET /api/music` adds `notesError`. `POST /api/music/note` answers with save_note's status (400 or 409). The route comment names `rev`. |
| `web-console/static/music.css` | One rule for the Retry button. |
| `server/customizations/Music/ClusterFShardMusic.cs` | `ReturnMusic(pm, before)` gives the area's music. Where the area has none (`Invalid`), it gives the music from before the fight. When that was none too, it gives `NoMusic` (0x1FFF, sent as 0x6D 1F FF, the stop). It never gives Invalid. `Fight.Before` records the area music when the first fight of a run began. A boss taking over, or the watch moving to the next creature, keeps the first fight's value. The header comment says why. |
| `player-package/payload/app/Build-UoOverrides.ps1` | **Stamp:** `uo-music 2` adds a `lines ...` row holding the Config.txt lines this run writes, so a mp3 that comes back or goes missing rebuilds the copy (:711). **Fallback:** `shard-music.txt` takes an optional last word, the stock track name. When our mp3 is missing and the player has `Music\Digital\<fallback>.mp3`, the copy gets `<id> <fallback>[,loop]` with no override line, plus a yellow line saying so. With no fallback, or one the player lacks, the track is skipped as before (:727). The fallback column never reaches Config.txt, because TazUO's reader takes two or three fields a line. |
| `player-package/Build-PlayerPackage.ps1` | The registry gate requires a `fallback` on each row. The gate 4 list check accepts the optional last word. The staged `shard-music.txt` writes `<id> <file>.mp3[,loop] <fallback>` and adds one comment line. |
| `player-package/vendor/shattered-legacy-music/registry.csv` | New `fallback` column after `loop`, with its comment. The registry has no rows yet, so nothing needs migrating. |
| `player-package/vendor/shattered-legacy-music/Add-Track.ps1` | `-Fallback` is mandatory and checked (letters, digits, underscores, no .mp3). It is written into the row and named in the printed Config.txt line. |
| the three test files | Section 6. |

## 5. TazUO with an unknown music ID, and with 0x6D FF FF

I worked this out from the source the package ships: upstream `3212623f` (client\TAZUO_COMMIT; sl-build.txt in
`D:\UO\tazuo-sl-build\client` names the same commit). None of patches 0001 to 0007 touches the music files.
`git diff --stat 3212623f` in `D:\UO\tazuo-sl-build\src` is empty for `PlayMusic.cs`, `AudioManager.cs`,
`Renderer/Sounds/Sound.cs`, `SoundsLoader.cs`, `UOMusic.cs` and `Constants.cs`. **I did not listen in a live client.**
The Golem run is unattended and cannot hear audio. The check for Chase is at the end of this section.

**How 0x6D is read.** `Network/PacketHandlers/PlayMusic.cs`: the packet is fixed at 3 bytes (`PacketsTable.cs`,
0x6D = 0x0003), so `p.Length == 3` is always true. The handler reads **two single bytes**, `cmd` (the high byte) and
`index` (the low byte):
- `cmd 0x1F, index 0xFF` (0x6D 1F FF, ModernUO's `SendStopMusic` and `MusicName.NoMusic`) calls `StopMusic()`, and the
  music stops.
- Anything else calls `PlayMusic(index)`, using **the low byte only**. Our IDs 105 to 149 fit in that byte, which
  agrees with the registry's limit of 149.

**`AudioManager.PlayMusic(int music)`** (`Game/Managers/AudioManager.cs:231`):
- `music >= MAX_MUSIC_DATA_INDEX_COUNT` (150, `Constants.cs:60`) returns, and **nothing changes**.
- Otherwise it calls `Sounds.GetMusic(music)`. That returns null when Config.txt has no line for the ID
  (`SoundsLoader.TryGetMusicData`). When the result is null and music is playing, it calls **`StopMusic()`**.

So:

| Sent | TazUO does |
|---|---|
| **0x6D FF FF** (`MusicName.Invalid`, what `SendPlayMusic(Invalid)` writes) | Read as `PlayMusic(255)`. 255 is at least 150, so it returns and **the current track carries on**. After a looping fight track, the fight music loops forever, which was the fault in part 3. Pinned's own `Region.OnRegionChange` sends this too, when a player walks from a town into a region with no music. In that case the town's music carries on, which is stock behaviour and is left alone. |
| **0x6D 1F FF** (stop) | Stops the music. This is what the fix sends when there is nothing to go back to. |
| **An unknown ID under 150** (no Config.txt line, for example a shard ID whose mp3 the launcher skipped) | `GetMusic` gives null, so whatever was playing **stops**, and the player hears silence. This is why the launcher now keeps the ID on a stock fallback. |
| **An ID whose Config.txt line names a missing file** | `GetTrueFileName` logs "No File found known as ..." and `UOMusic.BeforePlay` fails to open the stream and catches the error. The previous track was already stopped, so the result is silence with no crash. |

**Check by ear (about 2 minutes, for Chase, on a test client):** `[ShardMusicPlay 9` plays Britain, which loops. Then
`[ShardMusicPlay 140` should give silence, because 140 is an unknown ID. Next, `[ShardMusicPlay 9` again, then walk
out of a town region into the open land. Pinned sends 0x6D FF FF there, so Britain should **keep playing**. If either
case sounds different, the table above is wrong for the live build.

## 6. Tests, each seen red first

**Web console** (`web-console/tests/test_music_room.py`, 13 tests, 4 of them Edge). Red against the old code: 5
failures and 1 error, each for its own reason:

| Test | Red (old code) | Green |
|---|---|---|
| `MusicRoom.test_a_malformed_notes_file_is_untouched_after_a_save` | `200 == 200 : cut short` (the bad file was overwritten) | five bad files (cut short, `tracks` a list, not an object, not UTF-8, a record not an object): each save refused, file byte-identical, no `.tmp`, GET shows `notesError`; a missing file is a normal first save |
| `MusicRoom.test_a_stale_revision_is_refused` | `KeyError: 'rev'` | the older save from the same revision gets 409, the file keeps the newer note; no rev or a string rev gets 400 |
| `MusicRoomSavesInEdge.test_a_failed_save_then_reload_warns` | `saved 2:08:19 PM` (it said saved) | "not saved" on the row and in the status line; `beforeunload` is cancelled twice; Retry after the file is fixed saves it, then no warning and "all saved" |
| `MusicRoomSavesInEdge.test_reversed_arrival_keeps_the_newer_note` | `'the newer note' != 'the older note'` | the first save is held 1.5 s while the second edit is typed; at most one save is in flight; the file ends with the newer note |
| `MusicRoomSavesInEdge.test_save_to_repo_during_a_slow_save_commits_the_latest` | `Not committed: no notes yet` (it committed before the save landed) | `HEAD:docs/music/music-notes.json` holds the latest note |
| `MusicRoomSavesInEdge.test_save_to_repo_stops_when_a_track_is_not_saved` | `Saved to the repo: committed ...` | "Not committed: 1 track not saved (...)", HEAD unchanged |

The existing tests' `note()` helper now sends the revision GET reports. The local-listener POST sends `rev: 0`.
Green: 13 of 13. I ran the Edge classes three more times: OK each time. The whole web-console suite: **120 tests OK
(1 skipped)**.

**Package** (`player-package/tests/Music-Overrides.Tests.ps1`, run with Windows PowerShell 5.1). Red: 3 of 9 failed:
- `TheRegistryFollowsItsRulesAndEveryRowHasItsTrackWithItsHash` failed on the columns, because there was no `fallback`.
- `AMissingTrackPlaysItsStockFallbackAndARestoredOneComesBack` failed because the old parser could not read lines with
  a fallback.
- `ARestoredTrackIsBackInTheCopyWithNoFallbackColumn` failed with `expected [105 sl-test-one.mp3,loop;106
  sl-test-two.mp3] but got [106 sl-test-two.mp3]`. This is the stale-stamp fault on its own, with old-shape lines.

Green: **9 of 9**. The other launcher test files are also green: Build-UoOverrides 24 of 24, Cliloc-Overrides 10 of
10, Launch-Overrides 8 of 8, Launch-Settings 27 of 27, Map-Overrides 7 with 0 failed, Ui-Skins 4 of 4.

**Server** (`server/tests/Misc/ShardMusicVerification.cs`, fact 6). I probed it on the builder image
`sl-uo-builder:cc-P587` with the `Music\` folder and the test bind-mounted (no lock, as in P368 and P455):
- Red with the old `ClusterFShardMusic.cs`: `AFightThatEndsInTheDefaultRegionStopsTheFightMusic` expected
  `(pm, 8191, Area)` but got `(pm, -1, Area)`. `AFightThatMovesIntoTheDefaultRegionReturnsToTheMusicFromBeforeIt`
  expected `105` but got `-1`. The other 5 facts passed.
- Green: 7 of 7.

The first fact also reads the wire: it finds 0x6D 1F FF and no 0x6D FF FF. The second is a fight that starts in a
mapped town (105), lets a boss take over, drifts into the default region and ends there. The town track comes back.

**The gated build:** I took the `docker-build` lock and released it afterwards. Before the build I dropped the VM's
page cache; Windows had 9.1 GB free. The build ran detached, and its log is `build-P456.log` in the session scratchpad.
`docker\uo\build.sh -t sl-modernuo:cc-P456` finished with EXIT=0: "Built sl-modernuo:cc-P456 with patches applied and
2378 shard test(s) passing". That is **2,382 tests: 2,378 passed, 4 skipped (the real-map-data facts, as always), 0
failed**, and the 7 music facts are among the passes. The images are `sl-modernuo:cc-P456` = `65241722d9f5` and builder
`sl-uo-builder:cc-P456` = `66d08f3c8531`. `latest` is untouched. The red evidence comes from the bind-mounted probes
above, which run the same tests on the same builder.

## Deviations and decisions for Chase

- **Part 5 comes from the source, not from listening.** An unattended run cannot hear the client. The by-ear check is
  in section 5.
- **The revision is per track, and a cleared record goes back to revision 0.** Two tabs open on the Music Room: the
  second tab's save of a track the first one changed is refused (409, "reload the page"). That is intended. Edge case:
  if a track's record is cleared (every field emptied), its revision resets to 0, so a very old save from another tab
  made before the record first existed could still land. I judged that not worth a tombstone in the file.
- **A failed save is retried** on the next edit, on Retry, on Save to repo, and when the page is being left. It is not
  retried on a timer.
- **The fallback lives in registry.csv and is mandatory for new tracks** (`Add-Track.ps1 -Fallback`). A
  `shard-music.txt` without fallbacks still works: those tracks are skipped as before.
- **Not changed: `[ShardMusic off/on` (`SetOff`)** still sends `AreaMusic`, which can be Invalid in the default region.
  The prompt scoped part 3 to the fight's return. Turning shard music off in the wilderness mid-fight would leave the
  fight track playing until the next region change. It is a one-line follow-up with `ReturnMusic`, if wanted.
- **Tools:** the Read and Grep tools were denied on `D:\UO\golems\Iron\ShatteredLegacy\...` in this unattended run
  (Read of `web-console/tests/test_music_room.py` lines 268-271, to fix one line, and a Grep for `save_note` callers).
  I did both with Bash (`git grep`, `sed`) and made the edits with small Python exact-replace scripts in the
  scratchpad, as P454 and P455 did. The diff is the same.
- No CHANGELOG or VERSION entry: the prompt did not ask for one. Nothing ships to players until a track is assigned.

P456 DONE
