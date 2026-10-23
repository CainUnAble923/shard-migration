# cc-P277: the rideable red dragon (P139-D6), built from TheArt's file

2026-10-22. The Iron Golem (Opus). Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P277-rideable-red-dragon.md`. Work copies
`D:\UO\golems\Iron\ShatteredLegacy` and `D:\UO\golems\Iron\shard-migration`, branch `golem/Iron/P277`, both clean at the
start. Not committed: the Golem commits after the DONE line.

## In plain words

- There is now a rideable red dragon, and a second dragon that takes any colour, for staff only. In game, as staff:
  `[add RideableRedDragon` (or `[add RideableColorableDragon`), double-click it, and you ride it. Screenshots of
  mounting, riding and dismounting in TazUO are in `notes\art\p277-dragon\proof\`.
- Players cannot get one yet. Their stats are a horse's for now, and nothing tames, sells or rewards them. **How
  players get one is your call** (the question is at the end of these notes).
- The dragon art reaches players in the normal package update, which grows by about 5 MB (to about 124 MB). The big
  red dragon file stays out of git as you decided on 10-18. The package build copies it in from
  `D:\UO\third-party` by itself.
- To try it: build and publish the player package, rebuild the test shard on this branch's image, then ride one.
  One thing to look at: the rider sits low, inside the dragon's back (see the screenshots). That is the client's
  default seat height for a mount it doesn't know. Fixing it needs a small TazUO patch, so tell me if it bothers you.

## What was asked, what was done

| Part | Done | Where |
|---|---|---|
| 1. The body, P139's checklist, the `.vd` outside git, the built output in the package | Body 2086 (anim7 slot 207, ANIMAL), its `.vd` git-ignored and copied in by the encoder from `D:\UO\third-party` against a committed SHA-256; built into `build\sl-anim7.bin`, shipped in the package | ShatteredLegacy `player-package\vendor\shattered-legacy-art\` (registry, records, SOURCE.txt, `.gitignore`), `scripts\build-equip-anims.py` |
| 2. The mount (ModernUO's pattern), staff-only placeholders; the colorable dragon if cheap | `RideableRedDragon` and `RideableColorableDragon : BaseMount`; mount items 0x6E87 and 0x6E88, our tiledata records on the Mount layer naming the bodies; the colorable body 2087 (it was cheap: 3.2 MB, under the rule) | `server\customizations\Mobiles\Mounts\RideableDragons.cs`, `ShardBodyTypes.cs` |
| 3. Proof in TazUO: mount, ride, dismount, a screenshot of each; the package size and the updater | Done in our TazUO build, with this branch's art, on a scratch shard of my own (section 4); package +5.0 MB, the updater handles it (section 5) | `notes\art\p277-dragon\proof\` |
| Done means: CHANGELOG (staff), these notes, the question | `CHANGELOG.md` 2026.10.22 `### Staff` | below |

## 1. The body (P139's seven steps)

1. **Terms.** `D:\UO\third-party\theart-critters\SOURCE.txt`: "TERMS: none stated. Treat as community work: credit
   TheArt, ship only inside the player package or the private repo, do not repost", and the OSI Classic Rips are
   EA-derived, "ship as patch records only". Both hold: the frames ship only as blocks inside our own anim7 file. No
   "Needs Chase's call" flag line, so no edit under `third-party\`.
2. **Slot.** `python -P scripts\validate-art.py --data D:\UO\UltimaOnlineVanilla propose` on both files:

   ```
   L-Ridable Red Dragon.vd         low  0-12  2086 (0x826)  207  none needed (ANIMAL is the default for slot 207 of anim7)
   L-Colorable Rideable Dragon.vd  low  0-12  2087 (0x827)  208  none needed (ANIMAL is the default for slot 208 of anim7)
   ```

   then `check-vd ... 2086 --file 7 --slot 207 --type animal --flags 0`: "low layout, 65 records, 65 with frames,
   actions 0-12 ... verdict: free and matching" (and the same for 2087 at slot 208). (`--data` because this work copy
   has no `client-data\` folder; `D:\UO\UltimaOnlineVanilla` is the classic client the Legion harness uses too.)
3. **Register.** `registry.csv` rows 2086 and 2087 (`body`) and 28295 and 28296 (`art`, the mount items);
   `records.json` `bodyAnims` (2086 with `"outsideGit": { "from", "sha256" }`, 2087 plain) and two `tiledata` records;
   `SOURCE.txt` the credit and both SHA-256s:

   | File | Bytes | SHA-256 | In git |
   |---|---|---|---|
   | `L-Ridable Red Dragon.vd` as `anim-src\bodies\2086.vd` | 5,751,247 | `a4f50372ecd9f25190bb6cd50ae3ae0b982c07487b0c800d9abad531841d9482` | **no**: `.gitignore:104`, `git check-ignore -v` proves it |
   | `L-Colorable Rideable Dragon.vd` as `anim-src\bodies\2087.vd` | 3,240,155 | `59afd3abfa6192b625c16c1d4717d3f64d93802c1864372344c388f3e5e1a54e` | yes (under 5 MB) |

4. **Encode.** `build-equip-anims.py` printed "body 2086: copied anim-src/bodies/2086.vd from D:/UO/third-party/
   theart-critters/OSI Classic Rips converted/L-Ridable Red Dragon.vd (kept outside git, sha256 checked)" and wrote
   `build\sl-anim7.bin` (51,891,270 bytes) and `sl-anim7-idx.bin` (422,100 bytes). `--check`: "body 2086 slot 207
   (low): 65 blocks, 374 frames, every block the .vd's bytes and every pixel identical", the same for 2087 (65 blocks,
   355 frames), "anim7 matches".
5. **Server.** `ShardBodyTypes.Entries`: `(2086, BodyType.Animal, ...)`, `(2087, BodyType.Animal, ...)`. The .vd's
   13 actions are the animal set (walk, run as a flight cycle, stand, eat, alert, two attacks, hit, die, two idles, lie
   down, a second death), so nothing the server plays on an Animal falls back to the stand frame.
6. **Gates.** `find-free-art.py --check-registry`: 0 of 627 registered IDs are no longer free. `validate-art.py
   check-registry`: 0 of 627 rows have problems (2086 and 2087 "ok [anim7 slot 207/208 low; mobtypes ANIMAL 0 from
   records.json]", 28295 and 28296 "ok"). The scripts' tests: 58 OK. Launcher facts 22 of 22. The package build: every
   gate (section 5).
7. **Ship.** As P139 says: the Golem commits; Chase builds and publishes the package from the console and rebuilds
   the test shard.

**How "outside git" works** (P139 left it open; the prompt said "copy the .vd to the art source folder P139 uses
for files outside git", but no such folder existed, so this is the route P139 section 7 item 6 named, done the way
P368's music tracks are): the file sits where every other body's `.vd` sits (`anim-src\bodies\2086.vd`), so nothing
in the gates, the launcher or `validate-art.py` changed; only that one path is git-ignored. `records.json` carries
its source and SHA-256, and `build-equip-anims.py` (`fetch_outside_git`) copies it in from that source when it is
missing and checks the SHA-256 either way. A copy or a source with other bytes is refused, and so is a missing file
when the source is not on the PC (the message says where to copy it from). The package build already runs the encoder
first (P140's ANIMATION ENCODE GATE), so a package built on the game PC picks it up by itself. A PC without
`D:\UO\third-party` can't build the package until the file is copied there, and the message says so.

**The mount items.** TazUO draws a ridden mount from the mount item's tiledata Animation
(`ClassicUO.Client/Game/GameObjects/Item.cs:474-500`, `GetGraphicForAnimation`: its own table of OSI mount items
first, then `ItemData.AnimID` when it is not 0). So each dragon has a mount item of ours, 0x6E87 and 0x6E88 (both
"FREE; art empty" by `find-free-art.py --explain`, the two IDs after our last), with a tiledata record: layer 25 (Mount),
Animation = the body, flags Wearable (0x00400000), weight 255, named "red dragon mount" and "dragon mount". Their art
IDs need a PNG under the package's art rule, so each icon is the dragon's own stand frame (action 2, direction 1)
scaled to 44 px (`scratchpad p277_icons.py`; the same script made the render sheets). OSI's mount item range
(0x3E90 up) is no help here: in this client's tiledata those IDs are High Seas ship parts (0x3EA0 "ship", Animation
846), and TazUO's own table answers them.

Render sheets (the first frame of each action, direction 1, 1x): `notes\art\p277-dragon\p277-red-dragon-sheet-dir1.png`
(stand frame 187 x 173 px) and `p277-colorable-dragon-sheet-dir1.png` (140 x 129 px).

## 2. The mounts (server)

`server\customizations\Mobiles\Mounts\RideableDragons.cs` (new):

- `RideableDragonArt`: the four numbers (bodies 2086 and 2087, mount items 0x6E87 and 0x6E88), records.json's values. A
  launcher fact compares the two files (below). `SetPlaceholderStats`: **a stock horse's numbers** (pinned `Horse.cs`:
  Str 22-98, Dex 56-75, Int 6-10, Hits 28-45, damage 3-4, Physical 15-20, MagicResist 25.1-30, Tactics and Wrestling
  29.3-44, Fame and Karma 300), **Tamable false**, ControlSlots 1. They are placeholders so a dragon is no stronger than
  any mount until Chase decides.
- `RideableRedDragon : BaseMount` and `RideableColorableDragon : BaseMount`: `base(body, mountItem, AIType.AI_Animal,
  FightMode.Aggressor)`, the stock dragon's sound (362), "a red riding dragon" and "a riding dragon", eats meat.
  `[Constructible(AccessLevel.GameMaster)]`: only staff can `[add` them. Nothing places, spawns, sells or rewards them.
  A GameMaster rides any mount (pinned `BaseMount.OnDoubleClick`: `from.AccessLevel >= AccessLevel.GameMaster ||
  GetMaster() == from`); a player gets "That mount does not look broken! You would have to tame it to ride it."
- The colorable one: the staff sets `Hue`, and pinned's `BaseMount.Hue` passes it to the mount item, so the ridden
  dragon shows the same colour (proved below with hue 1157).

## 3. Tests, each seen failing first

**Shard** (`server\tests\Mobiles\Mounts\RideableDragonVerification.cs`, new, 4 facts, 6 cases): each dragon stands on
its body typed Animal with the package's mount item and is a staff placeholder (not tamable, a horse's numbers); each
round-trips the generated serializer; a GameMaster rides the red one (the mount item goes on the Mount layer, the
dragon leaves the map), dismounts (the dragon is back where the rider stands), and a player can't ride an untamed one;
the colorable dragon's hue goes onto its mount item.

| Run | Break | Result |
|---|---|---|
| red, `--tests-only` (image tag `sl-modernuo:cc-P277`) | the bodies not yet in `ShardBodyTypes`, and `RedMountItem = 0x3EA0` (the stock horse item) | **5 failed** of 2176: both "stands on its body" cases (body not typed Animal; `Expected: 28295 / Actual: 16032`), the ride fact (`Expected: 28295 / Actual: 16032`), and both round-trip cases. The round trips failed for a reason of the test's own: it built the copy from `typeof(T)` (`BaseMount`, abstract), fixed to `original.GetType()`. The hue fact passed (it does not depend on the break). "No image was built" |
| green, the full build | none (the file restored from the pristine copy; `RED BREAK` no longer in it) | 2176 tests, **2172 passed, 0 failed**, 4 skipped; image `sl-modernuo:cc-P277` built; `sl-modernuo:latest` not touched |

**Scripts:** `scripts\tests\test_build_equip_anims.py` (new, 3 tests: a missing copy is fetched and checked, then
left; a copy or a source with other bytes is refused; no copy and no source says where to get it): 3 errors on the old
script (no `fetch_outside_git`), 3 OK after. All 58 script tests OK.

**Launcher** (`player-package\tests\Build-UoOverrides.Tests.ps1`): new fact
`TheRideableDragonMountItemsAreTheServersAndNameTheirBodiesOnTheMountLayer` (reads `RideableDragons.cs`' constants:
each mount item has one tiledata record, on layer 25, naming its body; registered art with its PNG; each body
registered with one ANIMAL `bodyAnims` entry in an animal slot; the red one with its `outsideGit` source and SHA-256).
Red under the break: "expected [1] but got [0]. one tiledata record for mount item 16032". The registry counts went to
627 rows, 40 bodies and 570 art, and the "one record besides the stones" filter leaves out 28295-28296 (checked by the
new fact). **22 facts, 22 passed.**

## 4. The proof in TazUO

Screenshots, our TazUO build (5.31.2.0) with this branch's art overrides, 1280 x 800 window, New Haven
(3503, 2580). A GameMaster character adds each dragon beside it, rides it, walks, and dismounts:

| Step | Screenshot |
|---|---|
| The red dragon added beside the rider (it stands; the grey dragon behind it is OSI's stock dragon, body 12, a resident of the copied test world, a fair size comparison) | [1-red-spawned](art/p277-dragon/proof/1-red-spawned.jpg) |
| **Mounted**: the rider on the red dragon | [2-red-mounted](art/p277-dragon/proof/2-red-mounted.jpg), [2b-red-walking](art/p277-dragon/proof/2b-red-walking.jpg) |
| **Riding**: three steps east, then two south | [3-red-riding](art/p277-dragon/proof/3-red-riding.jpg), [3b-red-riding](art/p277-dragon/proof/3b-red-riding.jpg) |
| **Dismounted**: the dragon stands again where the rider got off | [4-red-dismounted](art/p277-dragon/proof/4-red-dismounted.jpg) |
| The colorable dragon, added with hue 1157 (a deep red), ridden two steps, dismounted | [5-colorable-spawned](art/p277-dragon/proof/5-colorable-spawned.jpg), [6-colorable-riding](art/p277-dragon/proof/6-colorable-riding.jpg), [7-colorable-dismounted](art/p277-dragon/proof/7-colorable-dismounted.jpg) |

What they show: the body draws whole in TazUO from our anim7, stands and walks; the mount item's tiledata Animation
makes the client draw the dragon under the rider; the rider goes with it and dismounting puts the dragon back. **The
rider sits low**: the human is drawn down inside the dragon's back, not on top. That is TazUO's seat height for a
mount outside its own table (`MountInfo.OffsetY` 0, `Mounts.cs`); OSI's own big mounts carry offsets there (the
unicorn -9, the tiger 18). `Mounts.def`, which could set ours, is read only for the Eventine server
(`Mounts.cs:89-90`), so a fix is a client patch (our `client\patches\`). See the question below. The dragon is OSI
dragon sized (its stand frame is 187 x 173 px), far bigger than a horse.

**How the proof ran, and why not on the real test shard.** P219's harness (`D:\UO\golem\Test-LegionScript.ps1`)
logs a Golem's Player into the real test shard (`sl-modernuo-test`, `sl-modernuo:latest`), which has neither the
dragon classes nor this branch's art. Swapping that shard to this branch's image would have risked saves that
`:latest` can't load once it is put back. So:

- **A scratch shard of my own**: `sl-modernuo:cc-P277` as container `sl-modernuo-p277`, loopback only on
  127.0.0.1:2596 (inside the harness guard's 2594-2599; never 2593 or 2594, and the bot's 2595 untouched), on a
  **copy** of the bot's last scratch world (`D:\UO\bot-shard\world`, itself a copy of the test world's backup) in
  `D:\UO\cc-p277-work\`, outside both repos. In that copy the Golems' accounts were players with no characters, so I
  ran the test shard's own account wipe on the copy (TestAccountWipe, as the bot does): "deleted 23 accounts, 41
  characters, 7357 items ... admin 'p277-admin' made (Owner); world saved". Its random password lived in
  `D:\UO\cc-p277-work\admin.local.json` and was deleted after the run; the client's saved password was cleared. The bot
  made its character "Rider" through the real 0xF8 packet. The container is stopped and removed (its log is in
  `D:\UO\cc-p277-work\shard.log`). No test-shard lock was taken: neither the test shard nor the bot's shard was
  touched.
- **The client**: a copy of `D:\UO\tazuo-sl-build\client` with this branch's overrides, built by the launcher's own
  `Build-UoOverrides.ps1` against `D:\UO\UltimaOnlineVanilla` (`tiledata.mul`, `animdata.mul`, `Bodyconv.def`,
  `mobtypes.txt`, `anim7.mul` and `.idx` from `build\`), started with `-uofilesoverride` as `Play.ps1` does, and a
  Legion script (`p277_proof.py`) driving the steps, with a screenshot (`Save-LegionShot`) at each step it marked. Four
  runs to get there: the first two found no staff access (the account wipe fixed that) and that `CloseGumps` only
  closes a script's own gumps; the third showed the dragon walking away before the mount ("That is too far away to
  ride": it is an AI_Animal), so the proof adds it with `set CantWalk true`. Scripts in the session scratchpad
  (`p277-shard.ps1`, `p277-admin.ps1`, `p277_mkchar.py`, `p277-client.ps1`, `p277_proof.py`).

## 5. The package size and the updater

A scratch package from this branch (`Build-PlayerPackage.ps1 -TazUO D:\UO\tazuo-sl-build\client -Out
D:\UO\cc-p277-work\pkg -UoData D:\UO\UltimaOnlineVanilla`, under the `package` lock; not for publishing): **every
gate passed** (the animation encode gate "anim7 matches", paperdoll fit 0 failures, gate 6 123 native files), built
`ShatteredLegacy-2026.10.22.2309.zip`, **123,757,809 bytes** (118 MiB).

| | Unpacked | In the zip (deflated) |
|---|---|---|
| `app/sl-anim7.bin`, whole | 51,891,270 | 33,771,804 |
| the red dragon's blocks | 5,750,463 | about 3,516,622 |
| the colorable dragon's blocks | 3,239,371 | about 1,518,189 |
| **the two dragons** | **8,989,834** | **about 5,034,811 (5.0 MB)** |
| the two mount item icons | 5,072 | 5,068 |

(The dragons' share in the zip is their blocks deflated alone with zlib level 6, so it is an estimate within a few
KB; the zip's whole `sl-anim7.bin` entry is measured.) Without the colorable dragon the package would grow by about
3.5 MB.

**The updater handles it.** `Play.ps1` downloads the whole package whenever `version.json` names a new one
(`Save-Download`, `payload\app\Play.ps1:138-170`): a streamed download with a progress bar, no size limit, a 10-minute
connect timeout and the 5-minute stall timeout, then the size and SHA-256 checked against `version.json`; `Update.ps1`
copies it over the install. A larger `sl-anim7.bin` is just a bigger file in the zip. `app\uo-overrides\` is rebuilt by
the launcher because `art-records.json` changed (the stamp includes the records' hash). Every player downloads about
5 MB more with the next update, 124 MB instead of about 119.

## Deviations and decisions for Chase

1. **The "art source folder P139 uses for files outside git" did not exist.** P139 only named the idea ("a
   git-ignored path with a stamp"). I made it the one git-ignored file `anim-src\bodies\2086.vd`, with its source and
   SHA-256 in `records.json`, copied in by the encoder (section 1). The package build on the game PC needs nothing new;
   a PC without `D:\UO\third-party` gets a clear refusal.
2. **The colorable dragon is committed** (3.2 MB, under the 5 MB rule, like every other body's `.vd`).
3. **Staff only:** `[Constructible(AccessLevel.GameMaster)]`, not tamable, a horse's numbers, placed nowhere.
4. **The rider sits low** on both dragons (section 4). Not fixed: it needs a TazUO patch (a `Mounts` entry or
   `Mounts.def` for our server), so it waits for your word.
5. **The proof ran on a scratch shard of my own,** a copy of the bot's last scratch world with its accounts wiped to one
   owner, not on the real test shard (section 4, and why). The `docker-build` lock was held for the two builds and the
   `package` lock for the package; no test-shard lock (the test shard and the bot's shard were not touched).
6. **The red round-trip fact failed first for a reason of its own** (`Activator.CreateInstance(typeof(T))` on an
   abstract `BaseMount`), not only the break; fixed in the test, and green in the full build.
7. **No play-test steps or bot check were added** (P139 added a bot check for its body; the prompt asked for
   screenshots, which are here). If you want the nightly bot to spawn and ride one, that is a short follow-up.
8. **The guard hook blocks any command naming the shard build script or the bot's compose file, even to read them**
   (as my memory notes say), so I read both through small script files.
9. **Memory:** 5 GB free before the red build, 2 GB before the green (the build script drops the Docker VM's page
   cache first, and the build was not killed), 6.7 GB after dropping it again for the proof.

## The question for Chase: how players get a dragon

Today only staff can `[add` one. Pick a route, and say whether the colorable one ships too:

- **A League reward**: the top tier of the League reward shop (like P229's shop items), bought with League points.
- **An achievement reward**: for example for a set of dragon kills or a whole achievement category.
- **A tame**: a wild red dragon to tame (with what Animal Taming skill, and where it lives).
- **Something else** (an event prize, a quest, the evo-pet line), or keep them staff only.

And the numbers: today they are a horse's. Should a dragon mount be stronger (OSI's swamp dragon or Hiryu as a
model), fly (P212's flying-mount question, U92 in P392), or stay a looks-only mount? The colorable one takes any hue;
should players choose it (a dye tub?) or get set colours?

## Files

**`D:\ShatteredLegacy`** (branch `golem/Iron/P277`):

| File | Change |
|---|---|
| `.gitignore` | `player-package/vendor/shattered-legacy-art/anim-src/bodies/2086.vd`, with why |
| `player-package/vendor/shattered-legacy-art/records.json` | `bodyAnims` 2086 (with `outsideGit`) and 2087; `tiledata` 28295 and 28296; the `about` line |
| `player-package/vendor/shattered-legacy-art/registry.csv` | rows 28295, 28296 (art) and 2086, 2087 (body): 627 rows |
| `player-package/vendor/shattered-legacy-art/SOURCE.txt` | the dragons' section |
| `player-package/vendor/shattered-legacy-art/anim-src/bodies/2087.vd` (new) | the colorable dragon, byte for byte (2086.vd is git-ignored) |
| `player-package/vendor/shattered-legacy-art/art/28295.png`, `28296.png` (new) | the mount items' icons |
| `scripts/build-equip-anims.py` | `sha256_of`, `fetch_outside_git`, called by `build()`; the docstring |
| `scripts/tests/test_build_equip_anims.py` (new) | 3 tests |
| `player-package/tests/Build-UoOverrides.Tests.ps1` | the dragon fact; the counts; the filter |
| `server/customizations/Mobiles/Mounts/RideableDragons.cs` (new) | the two mounts and `RideableDragonArt` |
| `server/customizations/Mobiles/Evo/ShardBodyTypes.cs` | 2086 and 2087 Animal |
| `server/tests/Mobiles/Mounts/RideableDragonVerification.cs` (new) | 4 facts |
| `CHANGELOG.md` | 2026.10.22 `### Staff`: the dragons |

**`D:\UO\shard-migration`**: these notes; `notes\art\p277-dragon\` (the two render sheets, 293 KB, and `proof\`, 11
screenshots, 1.5 MB, the largest 163 KB).

**Outside both repos:** `D:\UO\cc-p277-work\` (the scratch world, the client copy, the overrides, the scratch package
`pkg\ShatteredLegacy-2026.10.22.2309.zip` 124 MB, logs). Nothing in `D:\UO\third-party\` was changed.

## Commit preflight

Run with these notes written, before the last line (`git status --short --untracked-files=all` in both work copies):

- **ShatteredLegacy** (`golem/Iron/P277`): 8 changed (`.gitignore`, `CHANGELOG.md`, `Build-UoOverrides.Tests.ps1`,
  `SOURCE.txt`, `records.json`, `registry.csv`, `build-equip-anims.py`, `ShardBodyTypes.cs`) and 6 new (`2087.vd`,
  `28295.png`, `28296.png`, `test_build_equip_anims.py`, `RideableDragons.cs`, `RideableDragonVerification.cs`).
  `anim-src/bodies/2086.vd` is not listed: `git check-ignore -v` names `.gitignore:104`.
- **shard-migration** (`golem/Iron/P277`): 14 new (these notes, the 2 render sheets, the 11 proof screenshots).
- No file over 5 MB (the largest is `2087.vd`, 3,240,155 bytes); every changed text file ASCII; nothing under `docs\`.

P277 DONE
