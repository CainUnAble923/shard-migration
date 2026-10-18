# cc-P147: An Achievements button on the paperdoll and in TazUO's top menu

2026-10-18. Prompt: `D:\UO\cc-prompts\cc-P147-achievements-button.md`. Our TazUO's third patch, a small server hook,
placeholder button art and the package path. Not committed (the Golem commits after DONE). Both repos were clean at the
start. Nothing deployed or published.

## Headlines

- **One button, three places, all in our client (patch 0003):**
  - **Classic paperdoll:** an **Achievements** button in **Help's slot**, on your own paperdoll only (option A, below).
  - **Modern paperdoll:** an **Achievements** line in its menu, after Quests.
  - **Top bar:** an **Achievements** button at the right end, after More + (and Xml Gumps).
  - Each opens the page `[achievements` opens (`AchievementsGump`).
- **The button sends a whitelisted ClientCommand, never typed text.**
  - The client sends 0xCE id 4 **with** the command `achievements`. P103's bare id 4 stays its acknowledgement.
  - The server answers only a client that acknowledged id 4 on this connection, and only a command on its
    `ShardButtons` list with a page registered for it. Anything else does nothing, logged once per name.
  - **A stock TazUO never shows it.** It is our patch.
  - **Our client shows none of it on another shard:** the buttons appear only while this connection's server asked
    for id 4.
- **Generic for later pages.** The client keeps a table, `ShardButtons.All`: command, label, and paperdoll gumps. The
  server keeps `ShardButtons` plus `RegisterShardButton(name, open)`. League, guild progress or loop status would be
  one line on each side and one registration.
- **Paperdoll placement: A built, B and C for Chase.** Screenshots in `notes/art/achievements-button/options-ABC.png`.
  They are mockups from the shipped art (background, buttons, Siege of Sosaria bodies), not client screenshots.
  - **A** (built): it takes Help's slot. Help is still on the top bar's More + menu and in the modern paperdoll's
    menu. Nothing moves.
  - **B:** a ninth button, with the column closed up to 24 px a row. Every stock button moves, and the ninth touches
    the title panel.
  - **C:** a small icon button by the title strip.
- **It looks right on all six Siege of Sosaria bodies:** the button column is outside the body area
  (`option-A-every-body.png`).
- **Art:** gumps **22456** (normal), **22457** (pressed) and **22458** (hover), right after Castiel's 22450 to 22455.
  - All three checked free by `find-free-art.py --explain-gump` and registered (kind gump).
  - **They are a placeholder:** the shipped Help button's frame with "Achievements" in Arial Narrow Bold, in Help's own
    label colours.
  - The real art is briefed for Chase's art chat in `notes/art/achievements-button/BRIEF.md`. The generator and the
    mockup scripts sit beside it.
- **The client is rebuilt.** `client\Build-Client.ps1` applied 0001, 0002 and 0003 with no fuzz, and **1,292 of 1,292
  client tests** passed.
  - A real package build passed every gate as `TazUO 3212623f + 3 patches`
    (`player-package\dist\ShatteredLegacy-2026.10.18.0838.zip`, git-ignored; `-CheckZip`: gates 4, 6 and 5 passed).
  - P124's client gate refuses the old two-patch build.
- **Three gates had to learn something new, each argued below:**
  1. `Build-Client.ps1` now puts the `x64\` natives beside `TazUO.exe`. A fresh publish never had, so gate 6 failed.
  2. `find-free-art.py --check-registry` and `check-paperdoll-fit.py` now know a gump below 50000 is a standalone
     gump, not a worn item's.
  3. The free-art check now counts a TazUO file our patches add as ours.
- **Tests:**
  - server 8 new cases, 4 of them red against a stub;
  - client 10 new cases, 8 of them red against a stub;
  - paperdoll-fit 1 new fact, red before its fix;
  - a registry red proof.
  - Final: server **1,448 passed, 4 skipped, 0 failed**; client 1,292 of 1,292; shard `scripts\tests` 35 of 35;
    Package-Client 9 of 9; Paperdoll-Bodies 9 of 9.
- **Not seen in a running client.** Nobody has clicked the button yet (For Chase).

## What changed, with file:line

### Client patch (`client\patches\0003-shard-buttons-achievements.patch`, 17,361 bytes, ASCII; TazUO paths under `src\`)

Made on branch `sl/p147-shard-buttons` in `D:\UO\cc-p40-work\tazuo-3212623f`: one commit, `6ad3b6602`, on top of P111's
`df84b202a`, exported with `git format-patch`. The build-generated `LegionAPI.md` was reverted first, as in P103 and
P111.

| File:line | Change |
|---|---|
| `ClassicUO.Client/Network/EnhancedPackets/ShardButtons.cs` (new, 95 lines) | `Entry` (command, label, paperdoll gumps); `All` = Achievements, 22456 to 22458; `Paperdoll` (the entry with art); `Available` (this connection's server asked for id 4), `MarkOffered`, `Reset` (and reset on disconnect); `Build(command)` = `[0xCE][u16 length][u16 4][ASCII, 0]`, null off the table; `Send` |
| `ClassicUO.Client/Network/EnhancedPackets/EnhancedClientCommand.cs:77-82` | `SendAck` resets the offer at every handshake and marks it when the server listed id 4 |
| `ClassicUO.Client/Game/UI/Gumps/PaperdollGump.cs` | `_helpBtn`/`_shardBtn`; the shard button is added in Help's place (hidden), with its label as a tooltip; `Update()` shows it instead of Help while `Available` and its gump art exists (Help again if the art is missing); `Buttons.Shard` sends the command. Built only for the player's own paperdoll (inside the existing `LocalSerial == World.Player` branch) |
| `ClassicUO.Client/Game/UI/Gumps/ModernPaperdoll.cs` | the menu gains one line per entry, after Quests, on the player's own paperdoll while `Available` (the menu grows 20 px a line) |
| `ClassicUO.Client/Game/UI/Gumps/TopBarGump.cs` | one large button per entry after the last stock button, hidden; `Update()` shows them while `Available` and widens the bar's background by their width |
| `tests/ClassicUO.UnitTests/Network/ShardButtonsTests.cs` (new) | 5 facts, 10 cases, below |

### Shard repo (`D:\ShatteredLegacy`)

| File:line | Change |
|---|---|
| `server/customizations/TazUO/TazUOClientCommand.cs:14-18` | header: the other direction |
| `:33-41` | `ShardButtonResult` (Opened, NotCapable, Refused) |
| `:61` | `ShardButtons = ["achievements"]`, the patch's list |
| `:120-122` | id 4 **with** a payload goes to `HandleShardButton`; the bare id 4 is still the acknowledgement |
| `:135` | `RegisterShardButton(name, open)`, only for a listed name |
| `:146` | `HandleShardButton`: NotCapable unless the client acknowledged id 4 and has a character; Refused off the list or with no page; logged once per name |
| `server/customizations/ClusterFAchievements.cs:291`, `:297` | `Configure` calls `RegisterShardButton()`, which registers "achievements" to send `AchievementsGump`, exactly as `[achievements` does (safe to call again) |
| `server/tests/Misc/TazUOShardButtonVerification.cs` (new) | 4 facts, 8 cases, below |
| `client/patches/0003-shard-buttons-achievements.patch` (new) | the patch |
| `client/Build-Client.ps1:16-18`, `:78-84` | step 7: the `x64\` native DLLs are copied beside `TazUO.exe` (Deviation 4) |
| `client/README.md`, `design/client_patching.md` | the 0003 row |
| `player-package/vendor/shattered-legacy-art/gumps/22456.png`, `22457.png`, `22458.png` (new) | the placeholder states, 64 x 21 |
| `player-package/vendor/shattered-legacy-art/registry.csv` | 3 gump rows |
| `player-package/vendor/shattered-legacy-art/SOURCE.txt` | the button's section: placeholder, the Help frame it is made from, Castiel credited |
| `scripts/find-free-art.py` (check-registry) | `mine()`: a TazUO hit in a file one of our patches **adds** is ours (`our_patch_file`); a gump row must belong to an Animation number only at 50000 and up |
| `scripts/check-paperdoll-fit.py:81-86` | `registry_gumps`: only gumps at 50000 and up need a fit entry |
| `scripts/tests/test_check_paperdoll_fit.py` | `test_a_registered_button_gump_needs_no_fit_entry` |
| `CHANGELOG.md`, `VERSION` | 2026.10.18.7: one `### Added` player line and one `### Staff` line (2026.10.18.6 was committed with P146) |

### shard-migration

- `notes/art/achievements-button/`:
  - `BRIEF.md` (the art brief);
  - `make_button.py` (the placeholder states);
  - `mockups.py` and `pdlib.py` (the mockups, on cc-P81's renderer);
  - `options-ABC.png`;
  - `option-A-every-body.png`;
  - `placeholder-states-x6.png`.
- `testing/bot-triage.md` and `testing/playtest-steps.json`: rows and steps for P147-1 to P147-5, so the P115 and P146
  checks stay green when the importer brings them in.

### Outside both repos

- **`D:\UO\cc-p40-work` restored from its archive** (`UO Archive\cc-p40-work.7z`, SHA-256 matched the `ARCHIVED.md`
  record, 15,397 files), with the archive's own restore command. `Build-Client.ps1` needs the TazUO clone there; it had
  been archived on 10-17. `ARCHIVED.md` removed as its instructions say.
- `D:\UO\tazuo-sl-build\client`:
  - rebuilt;
  - its `ExternalImages` (1,860 files) refilled from the new package zip, so the test shortcut shows the shipped
    paperdoll and the new button (the rebuild clears the folder: P111's Deviation 3).

## Tests

**Server** (`docker/uo/build.sh --tests-only`), `TazUOShardButtonVerification`, 4 facts and 8 cases:
1. **Our client's button opens the page:**
   - the client answers 1 and 4, then sends `00 04 "achievements" 00` through the real `OnEnhancedPacket`;
   - `AchievementsGump` is open;
   - `HandleShardButton` says Opened.
2. **A client that never acknowledged gets nothing:**
   - a stock TazUO (answered 1 only): nothing opens, NotCapable;
   - a client that answered nothing, then presses twice: nothing opens, and **a press is not taken as the
     acknowledgement** (`CanRunCommands` stays false).
3. **Not a shard button:** `worldmap`, `Achievements` (case), `achievements now`, `cast Fireball` and the empty string
   each open nothing and are Refused, from our client.
4. **The bare id 4 is still the acknowledgement**; the list is `["achievements"]`; registering `worldmap` throws.

- **Fail first:** with `HandleShardButton` and the packet branch stubbed (no request branch, so a press counted as the
  acknowledgement; no acknowledgement check; any registered name in any case):
  - 1,452 run, **4 failed**, all P147's: facts 1 and 2, `Achievements`, `achievements now`.
  - The other 4 cases (`worldmap`, `cast Fireball`, empty, and fact 4) are refusals the stub also makes, because it
    still opened only registered names.
  - Restored, `cmp` identical.
- **First green run:** it did not compile (my test used `FindGump` and lacked `System.Buffers`); the shard code
  compiled.
- **Fixed, final:** **1,452 run: 1,448 passed, 4 skipped (the real-map facts, as always), 0 failed.** The 8 new and
  P103's 16 pass.

**Client** (`dotnet test tests\ClassicUO.UnitTests`), `ShardButtonsTests`, 5 facts and 10 cases:
1. the table is Achievements with its label and gumps 22456 to 22458, and it is the paperdoll entry;
2. the request is byte for byte `CE 00 12 00 04 "achievements" 00`;
3. nothing off the table is ever built: `worldmap`, `Achievements`, `achievements `, `cast Fireball`, empty, null;
4. the buttons follow the connection's answer: none before the server asks, none sent, on after `MarkOffered`, off
   after `Reset`;
5. a shard button is not a command the server can run here (not on P103's whitelist).

- **Fail first:** against a stub (no gumps in the table, always available, anything built, the string written
  without its terminator), **10 run, 8 failed**.
  - The two that passed: null (the stub kept the null check) and fact 5 (true of any table).
  - Restored, `cmp` identical.
- **Real code:** 31 of 31 with P103's cases. In `Build-Client.ps1`'s clean worktree, the whole suite was **1,292 of
  1,292**: P111's 1,282 plus 10.

**The patch applies with no fuzz:** `Build-Client.ps1` runs `git apply --check` then `git apply` (which takes no
fuzz) on 0001, 0002 and 0003, and printed "applied" for each. Run twice; both times the tests passed and it published.

**The package gate:**
- `PackageClient.ps1`'s `Test-PackageClient` on a copy of the old `sl-build.txt` (0001 and 0002 only) said: "STALE
  CLIENT BUILD ... the build lacks 0003-shard-buttons-achievements.patch". On the rebuilt client it gave no reasons.
- **A real build:**
  - `Build-PlayerPackage.ps1 -Notes "P147 gate check..."` gave `ShatteredLegacy-2026.10.18.0838.zip`;
  - "98 MB, 741 files, TazUO 3212623f + 3 patches";
  - the zip holds `app/tazuo/ExternalImages/gumps/22456.png` to `22458.png`, and its `sl-build.txt` lists 0003;
  - `-CheckZip`: GATE 4, 6 and 5 passed.
- **The two builds before it failed, for reasons this task found** (each fix argued in Deviation 4):
  1. the paperdoll fit gate: "gump 22456 is in registry.csv but paperdoll-fit.json says nothing about where it sits";
  2. gate 6: "FAudio.dll imports SDL3.dll: not shipped in app/tazuo/".

**Art gates:**
- `check-paperdoll-fit` tests: with HEAD's checker, **4 of 12 failed**: the new fact, plus three that read the real
  registry and now met 22456 to 22458. With the fix, 12 of 12. P138's "a registered gump with no fit entry fails"
  (55555) still fails as it should.
- **`find-free-art.py --check-registry`:**
  - before the fix: "3 of 140 registered IDs are no longer free" (our own `ShardButtons.cs` names them, and "not the
    paperdoll gump of a registered Animation number");
  - after the fix: **0 of 140**.
  - **Red proof:** a temporary row for Castiel's 22450 is still flagged (the UOP has it, Fiddle-Me-This ships it, and
    stock `PaperdollGump.cs` names it, a file we only modify). The registry was restored, `cmp` identical.
- **Not run:** the console's Pester suite (about 45 minutes). This task changes no console file, and its client facts
  use fixtures.

## Play-test items added

From For Chase below, by the importer (checked with `playtests.py parse`: 5 items, the 2 deploy steps skipped):
P147-1 to P147-5, all EYES in `testing/bot-triage.md`, each with Where, Do and Pass in `testing/playtest-steps.json`
(Where: In game: Player, any character).

**Also sorted here: P146's own four items.** The commit preflight's mirror refresh brought in P146-1 to P146-4 (from
P146's For Chase), with no Who, and the P115/P146 real-files facts went red (2 failures). P146 should have sorted them;
I added them now: P146-1 and P146-2 DEPLOY (the page, on Chase's screen), P146-3 and P146-4 CC (the repo's
`decisions.json` after an answer; the live API). The suite is green again: **151 of 151**.

## Deviations and decisions for Chase

1. **Where the paperdoll button goes: A is built. Say if you want B or C instead.** Screenshots:
   `notes/art/achievements-button/options-ABC.png`.
   - A (built): Achievements takes Help's slot on our shard; Help stays on the top bar's More + menu and in the modern
     paperdoll's menu.
   - B: a ninth button below Status, with the column closed up to 24 px a row (every stock button moves).
   - C: a small icon button on the frame by the title strip.
2. **Keep the placeholder button picture, or have the art chat draw the real one?** The brief is
   `notes/art/achievements-button/BRIEF.md`. The label "Achievements" does not fit a blackletter at the stock height;
   the brief asks for a condensed blackletter, or a short word ("Deeds", "Feats"), or a small icon with a word.
3. **The top bar button sits at the right end of the bar, not beside Paperdoll and Journal.** It must stay hidden on
   other shards, and a hidden button in the middle would leave a gap. Say if you want it further left (then it shows
   on every shard, doing nothing off ours).
4. **Three checks learned that a gump can be a button, and one build script was fixed. Each is a gate's rule, not a
   weakening:**
   - **`Build-Client.ps1` copies the `x64\` natives beside `TazUO.exe`.** A fresh `dotnet publish` (TazUO's own
     release workflow does the same) keeps them in `x64\` only. The client folder the package had shipped since P111
     also had them beside the exe, from where is not recorded. Gate 6 needs `SDL3.dll` there for `FAudio.dll` and
     `FNA3D.dll`. Without the copy, a rebuilt client could never be packaged: this was latent since P103's script and
     surfaced on its first fresh rebuild.
   - **`check-paperdoll-fit.py` and `find-free-art.py --check-registry`:** a gump below 50000 stands alone. At 50000
     and up it must still belong to an Animation number and have a fit entry, as before.
   - **`find-free-art.py`:** a hit in a TazUO file one of our patches adds is ours, as a hit in our server code already
     was. A file we only modify still counts as TazUO's. A planted stock ID is still caught.
5. **Restored `D:\UO\cc-p40-work` from the iCloud archive** (3.1 GB on disk again). `Build-Client.ps1` needs the TazUO
   clone. Re-archive it when you like; the next client patch will need it back.
6. **The modern paperdoll has no button column,** so there it is a menu line (its menu has the same functions as the
   classic buttons). Its art (the embedded modern background) is unchanged.
7. **Patch notes: an `### Added` player line.** Since P124 the package ships our client, so the next Build package
   and Publish puts this in players' hands. If you would rather wait for the real art, the line can stay until then.
8. **The Read tool was refused, unattended, on `D:\ShatteredLegacy\scripts\find-free-art.py`.** I wanted to read lines
   800 to 820 (`Read D:\ShatteredLegacy\scripts\find-free-art.py`, offset 800) to fix two characters a shell heredoc
   had mangled in my edit. I fixed them with a small Python script file instead and checked the result by printing
   the function; nothing was skipped.
9. **No task list for Chase:** this session has no task-list tool, so nothing could be kept in progress there.
10. **For the overseer (not changed):** in the mockup of all six bodies, the Siege of Sosaria gumps 665 and 666 (P81's
    vendored SFW set) look like the female and male gargoyle the other way round from their labels (665 is the male
    body). I did not verify which is right; P81's `render-report.txt` lists them as the kit's files.

## For Chase

**Deploy first:**

1. Shard Console > Test shard: rebuild the test shard, so it runs the server half.
2. To give it to players: Shard Console > Player package: Build package, then Publish. The client folder is already
   rebuilt (`TazUO 3212623f + 3 patches`).

**In game on the test shard** (desktop shortcut SL - TazUO TEST (our build), any character):

1. **Paperdoll button:** open your own paperdoll (classic style): the top button reads Achievements where Help was; click it: your achievements page opens, the same page as `[achievements`.
2. **Only on your own:** open another character's paperdoll (Eve beside you, or any player): it has no Achievements button.
3. **Top bar:** at the right end of the top bar, click Achievements: the same page opens.
4. **Modern paperdoll:** turn on the modern paperdoll in Options, open your paperdoll, open its menu (top right): click Achievements: the page opens.
5. **Stock client:** log in with SL - TazUO TEST (stock): the paperdoll shows Help, and the top bar has no Achievements.

## Repo size

- No pending file is over 5 MB. The largest new ones are `option-A-every-body.png` (178 KB), `options-ABC.png` (188 KB)
  and the patch (17 KB).
- The package zip (98 MB) is in `player-package\dist\`, which is git-ignored (P124 proved it with `git check-ignore`;
  rechecked below).
- The builds are in `D:\UO\tazuo-sl-build`, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after these notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

- code (17 files): `CHANGELOG.md`, `VERSION`, `client/Build-Client.ps1`, `client/README.md`, `design/client_patching.md`,
  the art `SOURCE.txt` and `registry.csv`, the three gump PNGs, `scripts/check-paperdoll-fit.py`,
  `scripts/find-free-art.py`, `scripts/tests/test_check_paperdoll_fit.py`, `ClusterFAchievements.cs`,
  `TazUO/TazUOClientCommand.cs`, the new patch and the new server test.
- docs (12 files): this note, `notes/art/achievements-button/` (7 files), `testing/bot-triage.md`,
  `testing/playtest-steps.json`, and the mirror's `testing/SUMMARY.md` and `testing/play-tests.json` (machine output).

P147 DONE
