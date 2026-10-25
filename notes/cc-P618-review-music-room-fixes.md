# P618: Review of the P456 Music Room fixes

Reviewed 2026-10-25 against ShatteredLegacy `57924e6` and shard-migration `0777d8f`. P456 is code commit `e0251a7`, merged by `f15bec8`. Review only. No tracked code or tests changed.

Read both work copies' AGENTS.md, the direction decision and task list, both `cc-P456-*.md` notes, and the earlier P368 and P403 reviews plus P429's Music Room follow-up. The findings below exclude issues already reported there or in P456's immediate Codex review. The registry and server assignment table still have no tracks, so the fallback finding affects future assignments.

## Findings

### 1. Medium (P2): Save to repo can accept a notes file the reader rejects

**Location:** `web-console/music.py:497`, with `web-console/static/music.js:211` and `web-console/server.py:1859`.

Open the page with an existing, modified notes file containing `{"tracks": []}`. GET reports `notesError` and supplies no records. Without editing a track, click Save to repo. `flush()` has no timers, failures or requests to await, so it resolves. `MusicRoom.commit()` calls `commit_notes()` without checking `load_notes()`. The helper can commit those damaged bytes and the page reports "Saved to the repo". The hourly path uses the same unchecked method. The refusal added to `save_note()` does not protect either commit path.

**Evidence:** A scratch file with that content produced a schema error from the real `load_notes()`. Calling the real `MusicRoom.commit()` and `commit_notes()` with only `_git` stubbed reached the commit command and returned `(True, 'committed fake123 ...')`. No real Git mutation was performed. The browser's empty `flush()` path was checked in source, not run in Edge.

**Fix:** Validate the current file before either kind of commit and return a failure containing the notes error. Hold the notes lock across validation and the commit snapshot so another Music Room save cannot change what was validated. Add a regression for loading a damaged file and clicking Save to repo without making an edit, and cover the hourly caller. `web-console/tests/test_music_room.py:585` currently makes an edit first, which exercises a failed `save_note()` instead of this path.

### 2. Medium (P2): A fallback filename does not preserve the player's stock slot mapping

**Location:** `player-package/payload/app/Build-UoOverrides.ps1:857`, with `player-package/vendor/shattered-legacy-music/Add-Track.ps1:78` and `player-package/Build-PlayerPackage.ps1:285`.

The new fallback is an MP3 basename. The launcher checks that the file exists, then uses it directly under the shard ID. It does not resolve the original stock music ID through the player's Config.txt. File names and server music names are not interchangeable across client installations.

For a concrete case, pinned ModernUO's `Projects/Server/Regions/Region.cs:25` defines `MusicName.Britain1` as stock ID 9. The installed client at `D:\UO\UltimaOnlineVanilla\Music\Digital\Config.txt:10` maps ID 9 to `britainpos,loop`; line 11 maps ID 10 to `britain1`. A row replacing stock ID 9 with `fallback=britain1`, a name advertised by the registry comment, passes validation. If its shard MP3 is missing and both stock files exist, the launcher plays the song from stock slot 10 instead of the player's song for slot 9. This is a different failure from P403's missing Config.txt entry: the new entry exists and points to the wrong stock selection.

**Evidence:** Ran the real override builder under Windows PowerShell 5.1 with tiny fixtures matching those installed Config.txt lines. Input `105 sl-probe.mp3,loop britain1`, with the shard MP3 absent, produced:

```text
9 britainpos,loop
10 britain1
105 britain1,loop
```

The pinned TazUO reader uses the line's filename and loop flag directly (`3212623f`, `src/ClassicUO.Assets/SoundsLoader.cs:307`). It cannot recover the original stock slot from this output. Audible playback was not tested.

**Fix:** Record the intended fallback stock ID and resolve its filename and loop setting from the player's Config.txt when building the copy. Validate that it names a stock ID. Add a regression where the stock slot uses a different filename from the server enum's name. The current fallback test at `player-package/tests/Music-Overrides.Tests.ps1:209` assumes the chosen basename already matches the stock mapping.

### 3. Low (P3): The watch's new handoff path has no regression test

**Location:** `server/tests/Misc/ShardMusicVerification.cs:326`, covering `server/customizations/Music/ClusterFShardMusic.cs:595`.

P456 also changes the watch to carry `fight.Before` through `Drop()` and `Engage()` when another live combatant takes over. The new town-to-wilderness test covers a boss taking over through a direct `Engage()` call. It does not enter the separate handoff branch inside `Check()`. Removing the `fight.Before` argument at line 596 would lose the remembered town track on that branch while the new tests still pass.

**Fix:** Start in a mapped town, keep a second mapped creature as the player's live combatant, make a boss the watched fight, then delete the boss without its death event marking `EndedAt`. Move to the default region and call `Check()` so the watch selects the other creature. End that fight and assert that the original town track returns after the delay. Observe this regression fail with the handoff argument removed, then pass with it restored. This is a coverage gap, not a confirmed failure in the current implementation.

## Verification and limits

- Traced the save queue, retries, revisions, malformed-file handling, commit routes and hourly caller. No additional save race was confirmed beyond the earlier reviews' findings.
- Read the P456 changes and the current versions of all files listed below. Checked the relevant pinned ModernUO enum and TazUO filename parser against source.
- Ran only the scratch probes described above. No new tracked tests were added; the existing suites and server build were not rerun. Server runtime behavior, browser interaction and audible playback remain unverified in this review.
- Scratch fixtures are under `ShatteredLegacy/downloads/P618/`, confirmed ignored with `git check-ignore downloads/P618/probe.txt`. Initial Python `TemporaryDirectory` attempts failed with access denied; the successful probes used directories created by PowerShell inside that ignored folder.
- Ran the progress reporter with `--dry-run` and work-copy path overrides. It exited successfully. Its incidental `tools/progress.json` write was restored byte for byte so the deliverable stays this note alone.
- No connection to Haven, deployment, commit, merge, push or branch switch was performed.

## Files reviewed

In ShatteredLegacy:

- `web-console/music.py`
- `web-console/server.py` (Music Room routes, construction and hourly commit caller)
- `web-console/static/music.js`
- `web-console/static/music.css`
- `web-console/static/music.html` (supporting page)
- `web-console/tests/test_music_room.py`
- `server/customizations/Music/ClusterFShardMusic.cs`
- `server/customizations/Music/ShardMusicTracks.cs` and `ShardMusicTable.cs` (supporting declarations)
- `server/tests/Misc/ShardMusicVerification.cs`
- `player-package/payload/app/Build-UoOverrides.ps1` (music builder and its caller)
- `player-package/Build-PlayerPackage.ps1` (music registry, list, staging and package gates)
- `player-package/vendor/shattered-legacy-music/registry.csv`
- `player-package/vendor/shattered-legacy-music/Add-Track.ps1`
- `player-package/tests/Music-Overrides.Tests.ps1`

P618 DONE
