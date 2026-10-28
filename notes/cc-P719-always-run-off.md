# cc-P719: the player package starts TazUO with always-run off (and the paperdoll closed)

## In plain words

- A brand-new character now walks instead of running everywhere. Running is one tick away: click **Options** on your
  character window, then **Gameplay**, then **Movement**, and tick **Always run** (P718's isle tip already says this).
- A brand-new character no longer opens its character window (the paperdoll) by itself at login. Double-click
  yourself, click **Paperdoll** on the top bar, or press **Alt+P** to open it.
- Characters that already exist keep everything they had: their running, their windows, and a default profile a
  player saved themselves. Only characters made after this update start the new way.
- For you: after this merges, rebuild the shared client (`client\Build-Client.ps1`) before the next package build,
  because the package build checks the client has every patch, and this adds patch 0009. Then make a new character
  to see it. Nothing else for you to do.

## Where always-run came from

Not from our package and not from our patches: **TazUO's own default**. `Profile.AlwaysRun` starts as `true`
(TazUO `3212623f`, `src/ClassicUO.Client/Configuration/Profile.cs:275`), saved in each character's `profile.json` as
`always_run`. The package ships no profile and no settings json that set it (`app\tazuo\Data\` may hold only
`XmlGumps\*.xml`, a package gate), and patches 0001 to 0008 do not touch it.

**The setting:** `always_run` in `Data\Profiles\<account>\<server>\<character>\profile.json`.
**How a player turns it on (exact menu path, for P718's tip):** Options (the button on the character window, which
opens on a double-click of yourself) > **Gameplay** > **Movement** > **Always run**. The labels are TazUO's own:
`mog_gameplaytab_gameplaylabel=Gameplay`, `mog_movementtab_label=Movement`, `mog_movementtab_running_alwaysrun=Always
run` (`Configuration/language.ini:1413, 1946, 1950`); the Movement tab is inside Gameplay (`GameplayTab.cs:27`,
`MovementTab.cs:32`). The checkbox under it, "Run unless hidden", stays on (TazUO's default), so a hidden character
still walks when Always run is ticked. P718's tip text (`TutorialClientTips.cs`) already gives exactly this path, so
it needs no change.

## How new profiles get the default (and returning players do not)

TazUO builds a character's first `profile.json` from `<profiles>\default.json` when that file exists, else from its
own defaults (`ProfileManager.Load`: `File.Exists(profile.json) ? Profile.Load() : NewFromDefault()`, and
`NewFromDefault` reads `default.json`). Keys the file leaves out keep TazUO's own default. A character that already
has a `profile.json` never reads `default.json`.

So the launcher writes one:
- `player-package\payload\app\Launch-Settings.ps1`: new `$NewProfileDefaults` (`always_run` false,
  `sl_open_paperdoll_at_login` false) and `Initialize-NewProfileDefaults -ProfilesDir`, which writes
  `default.json` (no BOM) **only when there is none**.
- `Play.ps1` calls it on `app\tazuo\Data\Profiles` right after the settings file, on every launch (live, -Test, a
  test profile, -Lan). A `-ClientDir` client reads the same folder (`-profilespath`), so it gets it too.

What this keeps:
- **Existing characters:** untouched. Their `profile.json` holds their own `always_run`.
- **A default the player saved themselves** (Options > Profile, "Set as default", `ProfileManager.SetProfileAsDefault`):
  kept, because the launcher never writes over an existing `default.json`.
- **Updates:** `Update.ps1` keeps `Data\` (the player's), so the file survives updates and is never re-written.

Why not ship `default.json` in the package: the package gate refuses anything under `app\tazuo\Data\` but
`XmlGumps\*.xml`, and an update would then carry it over a player's own saved default.

## The paperdoll at login

TazUO asks the server for the player's paperdoll at **every** login, for every profile:
`LoginComplete.Receive` queues a double-click on the player with the paperdoll flag
(`world.Player | 0x8000_0000`), and the server's answer (packet 0x88) opens the gump. No profile setting controlled
it, so this needs a client patch.

**Client patch `client\patches\0009-new-character-defaults.patch`** (on 0001 to 0008):
- `Profile.SlOpenPaperdollAtLogin`, saved as `sl_open_paperdoll_at_login`, **default true**. Every profile saved before
  this patch lacks the key, so it reads as true and keeps opening the paperdoll as before: a returning player sees
  no change.
- `LoginComplete`: the paperdoll request is sent only when it is true.
- The launcher's `default.json` sets it false, so new characters start with the paperdoll closed.
- A paperdoll a player leaves open at logout still comes back, from the saved gumps (`Profile.ReadGumps`,
  `GumpType.PaperDoll`), which `LoginComplete` restores right after.
- No options checkbox: a new player who wants it at every login just leaves it open when logging out.
- `client\README.md` has the patch's row.

One small side effect: the login paperdoll request also told the client the character's title (packet 0x88 carries
it). With the request skipped, the title arrives the first time the paperdoll is opened. Nothing else on our shard
reads it before that, as far as I found (unverified beyond reading `OpenPaperdoll.Receive`, the only place it is set).

**How a player opens the paperdoll (for P718's lesson):**
- **Double-click yourself** (the classic way; `GameActions.OpenPaperdoll`).
- **Paperdoll** on the top bar (TazUO's `TopBarGump`, first button, cliloc 3000133).
- **Alt+P**, TazUO's default macro "Paperdoll" (`MacroManager.CreateDefaultMacros`: key 112 `p`, alt). This default
  exists only while the player has no own `macros.xml` default.
- The tutorial's own button: patch 0001's `paperdoll` client command, which the isle stations already use.

## Tests

Every new test was seen failing first.

**Package:** `player-package\tests\New-Profile-Defaults.Tests.ps1`, 5 facts:
1. a fresh install gets `default.json` with exactly `always_run` false and `sl_open_paperdoll_at_login` false, no BOM;
2. a `default.json` the player saved is left byte for byte;
3. a character's own `profile.json` is untouched (and the next new character still gets the default);
4. `Play.ps1` calls it on `app\tazuo\Data\Profiles`, the same folder a `-ClientDir` client gets as `-profilespath`;
5. patch 0009 adds a bool profile property, default true, whose snake_case key is the one `default.json` sets, and
   gates `LoginComplete` on it.

Red first: 0 of 5 passed before the change (no function, no call, no patch). After the launcher change 4 of 5, and
with patch 0009, 5 of 5. `Launch-Settings.Tests.ps1`: 27 of 27 pass with the change (its end-to-end facts ran the
real `Play.ps1` in a sandbox).

**Client:** `tests\ClassicUO.UnitTests\Configuration\SlNewCharacterDefaultsTests.cs` (in patch 0009), 4 facts, which
read the launcher's exact file text (PowerShell 5.1's `ConvertTo-Json` output) with TazUO's own `ProfileJsonContext`:
the launcher's default makes a character that walks and does not ask for its paperdoll; every other setting keeps
TazUO's default; a profile saved before the patch keeps running and opening the paperdoll; the switch saves under the
key the launcher sets.

- **Red first.** Without 0009 the test file does not compile (no `SlOpenPaperdollAtLogin`). With a stub property on
  TazUO's plain bool default (false) and no login gate (`notes\cc-P719-tools\red_client.py`), 1 of 4 failed: the
  returning-profile fact. The other three test reading the file, which a stub property already does. Restored after.
- **A fresh `Build-Client.ps1 -Out D:\UO\golems\Iron\tazuo-p719`:** applied 0001 to 0009, passed all **1,326** client
  tests and published; `sl-build.txt` names 0009 with SHA-256 `7b30bebb...`.
- **One flaky upstream test on the way.** My first build failed on my own fourth fact: reading a whole saved profile
  back runs `Profile.OptionsFont`'s setter, which needs the game's UI. That fact now checks the saved text only. The
  second build failed once on `JournalMessageClassifierTests.Classify_MatchingSystemLikeRegularMessage_ReturnsChatSystem`
  (upstream, untouched by 0009; it passed in the build before and the build after). It looks like a race in
  `JournalMessageClassifier`'s static regex cache (it sets the pattern before the regex) or its 100 ms match timeout
  under load. Upstream's to fix; not chased further.

## CHANGELOG

`2026.10.28.4`, Changed: "A new character walks until you turn on Always run (Options, then Gameplay, then Movement),
and starts with its character window closed: double-click yourself to open it. Characters you already have keep their
own settings." `VERSION` is `2026.10.28.4`.

## Deviations and decisions for Chase

- **No in-game proof.** I did not log a new character in on a shard. The evidence is TazUO's code path (read above),
  the client unit tests on the launcher's exact file, and the package tests. You will see it on the next package:
  make a new character.
- **No package build.** The package build would refuse until the shared client is rebuilt with 0009 (it checks the
  client's patch list); the package's own payload copying did not change. Rebuild the shared client after the merge.
- **A Read the run could not ask for:** the Read tool was denied (unattended) on
  `player-package\payload\app\Launch-Settings.ps1`; I made that edit with a script
  (`notes\cc-P719-tools\edit_launch_settings.py`) and checked the diff instead.
- `client\README.md` had a stray bell character from an earlier edit (0007's row read "ExternalImages<BEL>rt" for
  "ExternalImages\art"); fixed while adding 0009's row.
- Files outside both repos: `D:\UO\golems\Iron\tazuo-p719\` (this prompt's client build and worktree) and
  `D:\UO\golems\Iron\p719-work\` (the worktree I wrote the patch in). Both are registered worktrees of
  `D:\UO\cc-p40-work\tazuo-3212623f` and can be removed (`git worktree remove --force`). No locks were needed or taken;
  Haven was not touched; nothing was asked of Chase.

## Files

- `ShatteredLegacy\player-package\payload\app\Launch-Settings.ps1`, `Play.ps1`
- `ShatteredLegacy\player-package\tests\New-Profile-Defaults.Tests.ps1` (new)
- `ShatteredLegacy\client\patches\0009-new-character-defaults.patch` (new), `client\README.md`
- `ShatteredLegacy\CHANGELOG.md`, `VERSION`
- `shard-migration\notes\cc-P719-tools\` (the edit scripts)

P719 DONE
