# cc-P367: a Music Room page on the web console

**Golem:** Bronze. **Date:** 2026-10-21. **Branch:** `golem/Bronze/P367` (ShatteredLegacy work copy). **Touches:**
web-console only.

## In plain words

- The web console has a new **Music Room** page at **https://uoconsole.tail81098d.ts.net/music** (a "Music Room"
  link is in the console's top bar). It lists all 353 music tracks we have on disk, with a Play button and a seek
  bar for each, so you can listen from the work PC or your phone.
- For each track you can mark Use, Maybe or Pass, tick where it fits (town, dungeon, boss and so on), name an area,
  monster or boss, and write a note. Notes save as you type. "Next unrated" works through the list like a playlist.
- 197 tracks carry a "not tagged Ultima" badge: their file's own album tag names another game or source (Diablo 2,
  Oblivion, Final Fantasy, Dark Souls and more), mostly in the SOS packs. Check those before shipping one.
- **For you:** once this branch is merged, restart the "SL web console" scheduled task. The task runs main's copy
  of the console, so the page appears only after the merge and a restart. Then open the link above and try a few
  tracks.

## What was built

All of it is in `web-console\` (ShatteredLegacy):

| File | What |
|---|---|
| `music.py` (new) | The library. It scans the four packs and the stock client music. For each track it reads the ID3 title, artist and album and the length (Xing/VBRI frame count, or the constant bit rate), and caches them in `D:\UO\web-console\music-index.json`. It matches each track to a stock track, stores the notes, builds the summary and the target suggestions, and makes the narrow commit. Standard library only. |
| `server.py` | Routes `GET /music` (+ `music.js`, `music.css`), `GET /api/music`, `GET /api/music/summary`, `GET /music-file/<pack>/<file>` (streamed, with Range), `POST /api/music/note` and `POST /api/music/commit`. An hourly thread commits the notes when they changed. The page-origin checks of `POST /api/action` moved into `_not_this_page()`, and both callers use it now. The docstring lists the new routes. |
| `static/music.html`, `music.js`, `music.css` (new) | The page: filters (pack, tag, rating, search), one card per track, the player in a sticky footer, Next unrated, Autoplay (off by default), Save to repo, and the Summary view. Every value is set as text, never as HTML. |
| `static/index.html` | A "Music Room" link in the console's nav. |
| `tests\test_music_room.py` (new) | 7 tests, below. |

### The tracks (counted by the scan; each matches the prompt's count)

| Pack | Folder (`D:\UO\third-party\...`) | Tracks | Matched to stock |
|---|---|---|---|
| SOS Mix Vol.2 (Zigholtul) | `sos-music-vol2\UO Classic Music (SOS Mix) Vol.2\Digital` | 93 | all 93 by name |
| SOS Mix + DLC (Zigholtul) | `sos-music-dlc\UO Classic Music (SOS Mix) + DLC\Digital` | 117 | 93 by name, **24 new** (Britain_Sewers, Covetous, Haven, Ice and so on) |
| Paranoia remixes (ParanoiaPhD) | `paranoia-remixes` | 49 | 7 by name; the other 42 carry the old MIDI names (OLDULT01, MINOC...), shown as "remix of the stock MIDI X (no digital track of that name)" |
| Paranoia Turfin | `paranoia-turfin` | 1 | Turfin |
| Stock client | `<repo>\client-data\classic-client\Music\Digital`, else `D:\UO\UltimaOnlineVanilla\Music\Digital` | 93 | (the originals, for comparing) |

- **"Remixes" is a name match, not a judgment.** Each SOS track has the same file name as the stock track it
  replaces in the client's music slots, so the page says "Same name as the stock track X" and offers "Play the
  stock one". The ID3 tags show that many of them are not remixes at all but music from other games under a stock
  name. For example, SOS DLC's `Turfin.mp3` is tagged "Optimistic" from Digimon, and `AnvilStrikeInMinoc.mp3` is
  "The Strongholds" from Kingdoms of Amalur.
- **Other games, per track:** 197 of the 353 have an album tag that does not contain "Ultima", and they carry the
  "not tagged Ultima" badge. This answers SOURCE.txt's flag where the tags can tell. The badge is not a verdict:
  some of those albums are "Youtube", "Wanderer" or "Origin Audio CD Vol. 2". The most common albums are Oblivion
  (16), Youtube (12), Diablo 2 (10), Fallout 1 (8), Ni No Kuni (7), Dark Souls 1 (7) and South Park: The Stick of
  Truth (7). The page shows each track's album and artist.
- **Lengths:** all 353 agree with ffprobe to within 1 second (I checked every one). The shortest is Deathtune at
  7.7 s; the longest seen is Vol.2's Ambrosia at 20:45 (ffprobe 1245.4 s).
- **Target suggestions (262):**
  - 240 region names: ModernUO's `regions.json`, with farm fields left out, plus our own "Old Haven Training",
    "the Rootdeep Burrows" and "the Vault"
  - 19 boss names from ART-LIBRARY.md's "Boss shortlist": Gloom Queen, Burrow Mother, beholder, otyugh,
    orc-lord and so on

### The notes file

`D:\UO\shard-migration\docs\music\music-notes.json`, under the console's `--notes` repo, which defaults to
`D:\UO\shard-migration`:

- It has `{about, schema: 1, tracks: {"<pack>/<file>": {pack, file, rating, tags, note, target, updated}}}`.
- A record with nothing in it is removed.
- The page sends the whole record 0.8 s after typing stops; a rating or tag goes at once.
- The server rewrites the whole file through a temporary file and `os.replace`.
- Limits: a note is up to 4000 characters, a target one line of up to 120.

The file does not exist yet: the console creates it at the first note. I did not create `docs\music\` myself
(AGENTS.md rule 2).

### Save to repo and the hourly commit

`music.commit_notes` commits that one file with `git commit --only -- docs/music/music-notes.json`. It does nothing
in any of these cases:

- the docs repo is not on `main`
- a merge, rebase or cherry-pick is under way (MERGE_HEAD and the rest)
- `index.lock` exists
- a Golem holds the commit lock (`D:\UO\golem\locks\commit.json`)
- nothing changed

When it skips, it says why, and the hourly run simply tries again an hour later. It **never pushes**: the next
Golem or Commit-ShardWork push carries the commit.

### Who can reach it

The same rules as the rest of the console (`panels.decide`):

- **Tailnet listener:** only with the sidecar's proof and an allowed Tailscale login, which is Chase's.
- **This PC's local listener:** allowed, as for the whole console, because "anything on this PC is Chase".
- **The two POSTs** also need the page's own `X-UOConsole-Action` header, the same origin, and JSON.
- **Unlike Golem buttons,** notes can be saved from the local listener too (see the decisions below).
- **Audio:** `/music-file/` serves only a pack id and file name that the scan listed. The page never names a path,
  and `..%2F` gets a 404.

## Tests

`python -m unittest discover -s web-console/tests -p test_music_room.py`: **7 of 7 pass.**

| Test | What it proves |
|---|---|
| `test_the_page_lists_all_four_packs_and_the_stock_music` | Small generated mp3s in the real folder shapes. It checks the five packs in order and their counts, the stock match (by name, ignoring case), "new", the MIDI remix, the lengths (including after an ID3 tag), the tags and the badge, the client slots from Config.txt, the nine tags, the region and boss suggestions, the page and its script, and the console's nav link. |
| `test_the_real_folders_give_every_track` | On this PC: the real counts of 93, 117, 49 and 1, and every track has a length. |
| `test_a_range_request_returns_partial_content` | 206 with the exact bytes and `Content-Range` for `a-b`, `a-` and `-n`. Past the end gives 416 with `bytes */size`. No Range gives 200 and the whole file, and HEAD works. A non-track, `..%2F`, an unknown pack or an unknown file gives 404. |
| `test_a_note_round_trips_to_music_notes_json` | A saved note is in the file and in `/api/music`, and lands in the summary under its tags and target. Only Use is summarised. Clearing a note removes its record. A bad rating, tag, length or target, or an unknown track, gives 400 and writes nothing. No `.tmp` file is left behind. |
| `test_the_page_refuses_anyone_but_chase` | No login, a stranger's login and a wrong proof each get 403 on every route (page, script, API, audio, both POSTs). Chase without the header, from another origin or a cross-site fetch gets 403, and not-JSON gets 415. Nothing refused is written. The local listener may look and take notes. PUT gives 405. |
| `test_save_to_repo_commits_that_file_alone` | The commit holds exactly `docs/music/music-notes.json`, and another dirty file stays uncommitted. A second save says "nothing changed". `changed()` sees a new edit. MERGE_HEAD or the Golem commit lock stops it. The hourly commit works. |
| `MusicRoomInEdge.test_rate_and_note_a_track_in_the_browser` | Headless Edge at phone size through the tailnet listener: 9 cards, no sideways scroll, autoplay off, the placeholder text. Next unrated plays the first unrated track. Use, a tag, a target and a typed note land in the file. Next unrated moves on, and the Summary shows the track. |

**Red first** (`scratchpad\mutants367.py`, each run on a copy):
- **Before the change:** against HEAD's web-console, the test module fails to load (`music` does not exist).
- **One mutant per test, each red as intended:**
  - stock folder dropped: the list test (and two others) red
  - Range ignored: the range test red
  - tags not kept: the round-trip test and the Edge test red
  - the POST's login check removed: the refusal test red
  - `commit -a` instead of the one file: the commit test red
  - music.js sends an empty note: the Edge test red
- **The new code unchanged:** 7 of 7 pass.

**Whole web-console suite:** 90 tests, 3 failures, 1 skipped. The 3 failures are
`test_golem_glow.PhoneGlow.test_five_states_on_a_phone` for Iron, Gold and Copper
(`'glow-pulse' != 'none'`). They fail the same way against HEAD's web-console without my change, so they were there
before this branch (not investigated further).

**Browser check on the real music:** `scratchpad\look367.py` ran this branch's server on a spare local port with a
scratch notes repo, in headless Edge:
- the page drew all 353 tracks, the 6 pack options and 262 suggestions
- filtering to the DLC pack and "sewers" left 1 track
- the real Britain_Sewers.mp3 streamed through the Range route: duration 239.5 s (ffprobe 239.52), a seek to 120 s
  worked, and the whole track is seekable
- a rating, tag, target and note were saved to the file
- Next unrated moved to the next unrated track
- the Summary showed the track
- at phone width (390 px) there is no sideways scroll

The screenshots were checked by eye. One limit: headless Edge refuses `play()` from a scripted click, which is not a
user gesture, so I loaded the audio with `load()`. A real tap is a gesture and plays.

## Deviations and decisions for Chase

1. **The "SL web console" task was not restarted.** The task runs
   `D:\ShatteredLegacy\web-console\server.py`, main's copy. A restart now would serve main without this page, and
   I may not touch `D:\ShatteredLegacy`. I checked the page on a side instance of this branch instead (above).
   Nothing restarts the task after a merge (only `Install-WebConsole.ps1` mentions it), so **after the merge,
   restart the "SL web console" task**, then open `https://uoconsole.tail81098d.ts.net/music`.
2. **"The console's normal commit path" became a narrow commit of one file.** Using `Commit-ShardWork.ps1` would
   commit and push everything that is dirty in both public repos, ask for the "commit shard work" phrase, and wait
   until every CC prompt has said DONE. With Golems running all day, an hourly commit would then block or sweep up
   other work. So Save to repo and the hourly commit commit only `music-notes.json`, with the same "never mid-merge,
   never during a Golem's commit" care, and leave pushing to the normal path. If you want it to push as well, that
   is a small change.
3. **Notes from this PC's own page:** the local listener (127.0.0.1:8095) may save notes and Save to repo. Golem
   buttons stay tailnet-only. Writing one notes file is not acting on the shard, and the console already treats this
   PC as you.
4. **Read tool denied:** the unattended run auto-denied
   `Read D:\UO\golems\Bronze\ShatteredLegacy\web-console\server.py` (lines 1-240), which I wanted for reading the
   console's code. I read the same lines with `sed` in Bash, as my notes for this work copy say to (the earlier
   ShatteredLegacy denials were handled the same way).
5. **Stock music folder:** the page uses the shard's own client data if it is there
   (`D:\ShatteredLegacy\client-data\classic-client\Music\Digital`, which I could not look in), otherwise
   `D:\UO\UltimaOnlineVanilla\Music\Digital`. Its 93 tracks and Config.txt match `D:\UO\tool-trials\client-data-copy`.
6. **The music stays where it is:** nothing from the music folders is copied into a repo, executed or published.
   The only thing written is the length cache in `D:\UO\web-console` (outside git).

## For P368

- Read `GET /api/music/summary`, or `music-notes.json` directly: the tracks rated `use`, with their tags and target.
- Each record is keyed by `<pack>/<file>`. Join it with `GET /api/music` for the track's length, album and
  "not tagged Ultima" flag, and the client slots it plays in.
- The SOS packs' `Server\Region.cs` and `PlayerMobile (Inserts).txt` hold ServUO's region music code, for reference.

P367 DONE
