# cc-P111: An in-game "Paperdoll bodies" option in our TazUO build: SFW, Topless, Nude

2026-10-14. Prompt: `D:\UO\cc-prompts\cc-P111-tazuo-paperdoll-option.md`. Client patch plus launcher and packaging.
Nothing deployed or published. **No Topless or Nude art entered any repo, package or build output** (checked below).

## Headlines

- **The option:** in TazUO's Options window (the new one, TazUO's default), the existing **Paperdoll** tab gains a
  **Shattered Legacy** section with **Paperdoll bodies: SFW / Topless / Nude**. The Paperdoll tab is the most fitting
  existing section, so no new tab.
  - **SFW** is always there and is the default.
  - **Topless** and **Nude** are listed only when the add-on folder holds that set's six bodies (12, 13, 14, 15, 665,
    666; verified against `player-package\vendor\paperdoll-sos\bodies-sfw` and the two add-on folders). Without the
    add-on the list holds SFW alone and names nothing else.
- **Applies live.** Picking a set swaps the six body gumps' source and drops just those six from the gump atlas, so an
  open paperdoll redraws with the new bodies on the next frame. It is saved at once.
- **The add-on is read where it is, at run time** (`ExternalImageLoader.SetGumpOverrides`). Nothing is copied into
  `ExternalImages`, the client folder or a build, so packages stay clean without depending on a file swap.
- **Where it looks:**
  - `sl_paperdoll_folder` in the client's settings if set;
  - else `<client>\..\client-addons\paperdoll-nsfw`;
  - else `<client>\..\..\client-addons\paperdoll-nsfw`, the player install's own folder beside `app\`, where cc-P81's
    launcher looks.
- **Stored globally** (`settings.json`: `sl_paperdoll_bodies`, `sl_paperdoll_folder`), not per profile: the add-on is
  per machine. Client-side only: no packet, no server flag.
- **One rebasable patch:** `client\patches\0002-paperdoll-bodies-option.patch` (20,634 bytes, ASCII), on `3212623f`
  plus 0001. It is a new `PaperdollBodies.cs` (121 lines), small hooks in five upstream files, and 8 unit tests.
  `client\Build-Client.ps1` built it from a clean worktree: **1,282 client tests passed** (P103's 1,274 plus 8), and it
  published `D:\UO\tazuo-sl-build\client\TazUO.exe`. Its `sl-build.txt` lists patch 0002.
- **The launcher stands down** for a client that has the option (seen from that `sl-build.txt` line). It puts the
  shipped SFW six back, leaves the choice to the client, and carries a custom add-on folder into the launch settings
  once. Older clients keep cc-P81's swap.
- **The NSFW gate** still passes on the latest package and still stops a build with planted Topless art (re-proved).
- **Desktop shortcut** `SL - TazUO TEST (our build)` starts our build on the test shard with `D:\UO\UltimaOnlineVanilla`.
- **Tests:**
  - client: 8 new;
  - launcher: 3 new;
  - every new one seen failing first.
  - A smoke start of the built client passed the new start-up code.
  - **Not seen in a running game:** nobody has opened the Options or switched bodies on screen (For Chase).

## What changed, with file:line

### Client patch (`client\patches\0002-paperdoll-bodies-option.patch`; TazUO paths under `src\`)

Made on branch `sl/p111-paperdoll-option` in `D:\UO\cc-p40-work\tazuo-3212623f`: one commit, `df84b202a`, on top of
P103's `761d2456d`, exported with `git format-patch`. As in P103, I first reverted the build-generated `LegionAPI.md`.

| File:line | Change |
|---|---|
| `ClassicUO.Client/Game/Managers/PaperdollBodies.cs` (new, 121 lines) | `BodyIds`. `ResolveFolder(configured, clientDir)`: the configured folder if it exists, else `<client>\..` then `<client>\..\..` `client-addons\paperdoll-nsfw`. `SetFiles(folder, set)`: the six files, or null unless all six exist. `Available`: SFW plus each complete set. `Effective`: the choice if available, else SFW. `Overrides`. `Apply()`: sets the overrides and invalidates exactly the changed bodies. `Choose(set)`: saves the settings file at once, then applies |
| `ClassicUO.Assets/ExternalImageLoader.cs:84` | `LoadGumpTexture` looks in the override map first |
| `ClassicUO.Assets/ExternalImageLoader.cs:590` | `SetGumpOverrides` replaces the set and returns every id whose source changed, with its cached pixels dropped; `GetGumpOverride` |
| `ClassicUO.Renderer/Gumps/Gump.cs:62` | `Invalidate(idx)`: forgets one sprite, so the next draw loads it again |
| `ClassicUO.Client/Configuration/Settings.cs:102` | `sl_paperdoll_bodies` (default `sfw`), `sl_paperdoll_folder` |
| `ClassicUO.Client/Client.cs:217` | `PaperdollBodies.Apply()` after the client's files load, before anything is drawn |
| `ClassicUO.Client/Game/UI/MyraWindows/Options/Tabs/PaperdollTab.cs:24` | the Shattered Legacy section: a combo box of the available sets, with a tooltip saying it changes at once |
| `tests/ClassicUO.UnitTests/Game/PaperdollBodiesTests.cs` (new, 130 lines) | 8 facts, below |

**Live reload, how:** the renderer keeps each gump in a `SpriteInfo` slot and draws open gumps from it every frame. So
dropping the six slots (`Invalidate`) and the loader's pixel cache (`SetGumpOverrides`) makes the next draw load the
new file. The old atlas space for those six is not reclaimed, which is a few small textures per switch.

### Shard repo (`D:\ShatteredLegacy`)

| File:line | Change |
|---|---|
| `client/patches/0002-paperdoll-bodies-option.patch` (new) | the patch |
| `client/README.md` | the patch row |
| `design/client_patching.md` | the patch row in "Client code patches" |
| `player-package/payload/app/Paperdoll-Bodies.ps1:66` | `Test-ClientPaperdollOption`: true only when `app\tazuo\sl-build.txt` has a `patch NNNN-paperdoll-bodies-option.patch` line |
| `player-package/payload/app/Paperdoll-Bodies.ps1:78` | `Sync-PaperdollBodies -SettingsPath`; when the client has the option it stands down (below) |
| `player-package/payload/app/Play.ps1:311` | passes the settings file being launched |
| `player-package/tests/Paperdoll-Bodies.Tests.ps1:108` | 3 new facts |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.17, one `### Staff` line, which says nothing about Topless or Nude |

**The stand-down, exactly:** with the option in the client, `Sync-PaperdollBodies`:
1. copies the shipped SFW six back over `app\tazuo\ExternalImages\gumps` (undoing any older swap);
2. if `paperdoll-bodies.txt` names a non-default `folder=` and the launch settings file has no `sl_paperdoll_folder`,
   writes it there (other keys kept);
3. does not carry the mode: the client's own choice starts at SFW;
4. says "chosen in the game now (Options, Paperdoll tab)" when the old file still asks for Topless or Nude.

Without the option (a stock TazUO, or our build before 0002) nothing changed: cc-P81's swap runs as before.

### Outside both repos (Chase's PC only)

- `D:\UO\tazuo-sl-build\client\` holds the build. I gave it the **SFW** `ExternalImages` (1,856 files) from the latest
  package zip (`ShatteredLegacy-2026.10.13.0118.zip`, which the gate passes), so the test client looks like the
  shipped one; the six bodies hash-match `bodies-sfw`. **A rebuild may clear that folder** (see Deviations).
- `D:\UO\tazuo-sl-build\settings.sl-test.json`: test shard (`shatteredlegacyuo.com:2594`, as the package's test
  profile), client 7.0.117.0, UO data `D:\UO\UltimaOnlineVanilla` (from the 10.02 install's `uo-path.txt`),
  `sl_paperdoll_folder` `D:\ShatteredLegacy\client-addons\paperdoll-nsfw`, no username or password.
- `Desktop\SL - TazUO TEST (our build).lnk`:
  - target `D:\UO\tazuo-sl-build\client\TazUO.exe -settings "D:\UO\tazuo-sl-build\settings.sl-test.json"`;
  - working folder the client folder.
  - The overseer's two repointed shortcuts and their `.bak-20261014` copies are untouched.

## Tests

**Client** (`tests\ClassicUO.UnitTests`, xUnit), 8 new. The add-on folders in them hold empty stand-in files named like
the bodies, never art:
1. the bodies are cc-P81's six;
2. without the add-on only SFW is offered (no folder, a missing folder, nothing beside the client);
3. a set with all six is offered;
4. a set missing one body is not offered, and choosing it falls back to SFW with no overrides;
5. the chosen set's files are read from the add-on folder where they are (and SFW, or an unknown name, has none);
6. folder resolution: the configured folder, else beside the client, else the install's; a named folder that is gone
   is no add-on;
7. the choice persists in the settings JSON (`sl_paperdoll_bodies`, `sl_paperdoll_folder`), the default is SFW, and a
   settings file from before the option reads as SFW;
8. overrides win, and exactly the changed bodies are reported (back to SFW reports both).

**Seen failing first** (stubs in the clone, restored, `cmp` identical):
- **Stub 1:** every set always offered, no fallback, no changed ids reported, default `nude`. 4 of 8 failed (2, 4, 7,
  8).
- **Stub 2:** the configured folder trusted blindly, missing files not checked, one body id dropped. 4 of 8 failed
  (1, 2, 4, 6).
- **Together 6 of 8.** Facts 3 and 5 are the positive cases (a full set is offered; its files are read where they
  are), which a do-everything stub also passes. They guard against the option losing a set, not gaining one.
- **Real code:** 8 of 8, and the whole suite **1,282 of 1,282** inside `Build-Client.ps1`'s clean worktree.

**Launcher** (`player-package\tests\Paperdoll-Bodies.Tests.ps1`), 3 new:
- only a client whose stamp lists the option patch counts (no stamp, and a 0001-only stamp, do not);
- with the option the launcher stands down: a Nude swap made by the old path is put back to SFW, with a line saying
  where the choice is now, and an SFW install says nothing;
- a named add-on folder is carried into the launch settings once (other keys kept, the mode not carried, a folder
  already there not overwritten).

Against the launcher before P111 (`git show HEAD:`), the 3 new facts failed and the old 5 passed. Restored: **8 of 8**.

**Other player-package suites, unchanged by this task:**
- `Build-UoOverrides` 10/12, `Cliloc-Overrides` 9/10, `Launch-Settings` 15/20.
- Exactly the same counts at HEAD in a clean worktree, so the failures predate P111. Launch-Settings' failures are its
  end-to-end facts, whose sandboxed `Play.ps1` stops with "Press any key" or "The term ... is not recognized".
- **For the overseer**, not investigated here.

**The NSFW gate, re-proved once:**
- **Green:** `Build-PlayerPackage.ps1 -CheckZip dist\ShatteredLegacy-2026.10.13.0118.zip` passed gates 4, 5 and 6, exit 0.
- **Red:** with the add-on's Topless `12.png` planted over `vendor\paperdoll-sos\ExternalImages\gumps\12.png`, a build
  stopped before staging, exit 1: "NSFW GATE: vendor\paperdoll-sos holds Topless or Nude art".
- **Restored** from a copy in my scratchpad; the hash is the same as before. `git status` shows nothing under `vendor`,
  and no new zip in `dist`.

**No add-on art in the build:** all 6,907 files under `D:\UO\tazuo-sl-build\client` and `...\src` were checked against
the 12 add-on files' SHA-256, and for names containing `paperdoll-nsfw`, `topless` or `nude`: none.

**Smoke start:**
- The built `TazUO.exe` with the test settings file ran for 25 s and was then closed.
- It wrote `Data\Client\chair.txt` and the other files that `ChairTable.Load` and its neighbors write, which run right
  after `PaperdollBodies.Apply()` in `Client.cs`, so start-up passes the new code without a crash.
- Logging is off by default, so there is no log line. It did not log in.

## Deviations and decisions for Chase

1. **Only the new Options window has the option.** TazUO's legacy options gump (used only if a profile turns
   `UseNewOptionsWindow` off) does not; the setting still applies there, it just cannot be changed from it.
2. **The mode is not carried over** from `paperdoll-bodies.txt`. The first start of a client with the option shows SFW
   until the body set is picked in Options. Only a custom add-on folder is carried, so that the client can find it.
3. **The test client's `ExternalImages`** came from the package zip, not from a build step. `Build-Client.ps1`
   publishes into the same folder and may clear it. If the paperdoll ever looks stock after a rebuild, copy
   `app\tazuo\ExternalImages` from an installed package of 2026.10.13 or later (or from that zip) into
   `D:\UO\tazuo-sl-build\client\`. Folding that into `Build-Client.ps1` is a small follow-up if you want it.
4. **Players see no change yet:** the package still ships the stock TazUO (cc-P40's P-a), so this reaches players only
   when our build ships. When it does, the option shows SFW only, because players have no add-on.
5. **The test shortcut does not pass the shard's cliloc and UO overrides** (`-uofilesoverride`) the launcher builds, so
   a few of our custom texts may read stock in that client. The paperdoll does not depend on them.

## For Chase

1. Double-click **SL - TazUO TEST (our build)** on the desktop and log in to the test shard.
2. Open your paperdoll. Then Options > **Paperdoll** tab > **Shattered Legacy** > **Paperdoll bodies**: switch SFW,
   Topless, Nude. The open paperdoll should change each time without closing it.
3. Log out and back in (or restart): the last choice should still be shown.
4. To check the hidden case: rename `D:\ShatteredLegacy\client-addons\paperdoll-nsfw` for a moment. The list should
   then hold SFW only, and the paperdoll should be SFW. Rename it back.
5. Nothing to deploy. The Shard Console's commit pushes the patch and launcher change; the client build stays on this
   PC.

## Repo size

No pending file over 5 MB: the largest is the patch, 20,634 bytes. The build, the test settings and the copied
`ExternalImages` are under `D:\UO\tazuo-sl-build`, outside both repos.

## Commit preflight

`D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: `CHANGELOG.md`, `VERSION`, `client/README.md`, `design/client_patching.md`, the launcher's
`Paperdoll-Bodies.ps1` and `Play.ps1`, its tests, and the new `client/patches/0002-paperdoll-bodies-option.patch`.
docs: this note and the play-test importer's `testing/SUMMARY.md` and `testing/play-tests.json` (machine output).
Nothing under `client-addons\` or `design\paperdoll-sos\kit\` is pending; both stay git-ignored (cc-P81).

P111 DONE
