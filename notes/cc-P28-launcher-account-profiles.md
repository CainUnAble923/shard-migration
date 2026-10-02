# cc-P28: launcher account profiles (one saved login per account)

Brief: `D:\UO\cc-prompts\cc-P28-launcher-account-profiles.md` (overseer, 2026-10-02). Launcher only; no server
change, no pinned file, nothing published, nothing committed. Numbering: no clash (P27's note is
`cc-P27-defect-batch-1.md`; no other P28 exists).

## Headlines

1. **`Play.ps1 -Test -Account <name>` works**: `app\tazuo\settings.test.<name>.json`, save and autologin on, the
   first line says `TEST SHARD (throwaway), profile: <name>`. No `-Account` is today's launch exactly.
   `-Account` without `-Test`, or a name outside `^[a-z0-9-]{1,24}$`, is one red line and exit 1, before anything
   is read, checked or written.
2. **The brief's premise was wrong in one place, and the fix adds one TazUO flag.** `autologin = true` does **not**
   log straight in on a cold start in the TazUO we ship. It only connects at startup with TazUO's own
   **`-skiploginscreen`** command-line flag (no value, not a password), so the launcher passes that flag for a
   profile. Proved in the source **and** in the real client (section 2). Without it, the shortcuts would have
   opened a login screen with the login already filled in, every time.
3. **An empty profile falls back to the login screen.** It does not loop or error: 0 connections in 25 s, and the
   client stays up. A saved login that fails connects **once** (at 2.4 s) and is not retried.
4. **It does pick the last character**, by the source (`LoginScene.cs:591-621`): autologin selects the server by
   `last_server_name` and then the character named in `Data\Profiles\lastcharacter.json` for that account. **Not
   seen in a logged-in client**: I cannot log in to the test shard (T-row in section 7).
5. **The updater now brings a profile back as itself** (`Update.ps1 -Account`). That is in `payload\app\`, the
   brief's directory, but it is not one of the files the brief named; it is a pass-through like the .bat case.
   The reason is in section 3.3.
6. Tests: **13 new facts, red 11 of 13 first, then 13 of 13 green; 7 deliberate breaks each went red.** The
   existing 8 P26 facts are still green. The package builds through its gates (scratch only).

## 1. Facts from the brief, checked before building on them (at HEAD `eccf5af`)

| Brief's fact | Checked | |
|---|---|---|
| settings file chosen at `Play.ps1:36-39` | yes, exactly | now `Launch-Settings.ps1:18-35` |
| `-Test` forces `saveaccount`/`autologin` false at `Play.ps1:287` | yes, that exact line | now `Launch-Settings.ps1:78-81`, only when there is no profile |
| keeps the saved login and rewrites only what it owns (`Play.ps1:264-285`) | yes (`:265-272` keep, `:273-286` force) | now `Launch-Settings.ps1:38-86`, moved unchanged |
| `D:\ShatteredLegacy` clean before starting | `git --no-optional-locks status`: clean, `main`, up to date | |

## 2. TazUO 26.0909.63 (3212623f): what autologin really does

Source: a clean clone at `3212623f63436be1c0f4e3b308b202b29597c026` (left by an earlier session's scratchpad,
`git rev-parse HEAD` and `status` checked, read only). The client binary I probed reports ProductVersion
`26.0909.63+3212623f...`.

| Question | Answer at 3212623f | Where |
|---|---|---|
| Does `autologin` connect at startup? | **No.** `Load()` connects only if `(CanAutologin && CurrentLoginStep != Main) \|\| (SkipLoginScreen && gump)`, and a cold start's step **is** `Main` | `Game/Scenes/LoginScene.cs:127`, `Network/LoginHandshake.cs:47` |
| What does connect at startup? | `-skiploginscreen` sets `CUOEnviroment.SkipLoginScreen` | `Main.cs:419-420`, `LoginScene.cs:127-134` |
| ...with no saved login? | It connects only `if (!string.IsNullOrEmpty(Username))`; otherwise it shows the normal login screen | `LoginScene.cs:129` |
| Does `-skiploginscreen` eat the next argument? | Only one that does not start with `-`. The launcher puts it between `-settings "<path>"` and `-uofilesoverride` | `Main.cs:259-264` |
| What `autologin` does after connecting | picks the server by `last_server_name` (else `lastservernum`), then the last character | `LoginScene.cs:169-183`, `:404-421`, `:591-621` |
| Server name match | the test shard advertises `Shattered Legacy TEST` and the launcher writes the same | `docker/uo/Start-TestShard.ps1:89`, `test-shard.sh:50` |
| Where the last character lives | `app\tazuo\Data\Profiles\lastcharacter.json`, one list keyed by account **and** server, so profiles do not collide | `Game/Managers/LastCharacterManager.cs:22-23`, `:54-78` |
| Loop on a failed login? | No. `HandleReconnect` needs `Reconnect`, which is set only after a live disconnect **and** only when the `reconnect` setting is on; the launcher never sets it (TazUO default false) | `LoginHandshake.cs:160-180`, `:437-439`, `Settings.cs:81` |
| Is the login kept? | `Connect` copies it into the settings when `SaveAccount`; saved on `LoginInToServer`; `Save()` blanks it only when `saveaccount` is false. The password is TazUO's own `Crypter` encoding, exactly as today | `LoginScene.cs:381-392`, `:185-188`, `Configuration/Settings.cs:151-168` |
| No account characters yet? | character creation opens | `LoginScene.cs:623-626` |
| Four clients at once? | nothing stops a second instance; the only `Mutex` is per JSON file save | `Configuration/JsonSave.cs:549` |

**Probe in the real client** (`notes\cc-P28-tools\probe-autologin.ps1`): a scratch copy of `D:\UO\TazUO\client`
without `Data\`/`Cache\`; a `TcpListener` on 127.0.0.1:27594 that counts connections and closes each; 25 s per
case; the UO folder `D:\ShatteredLegacy\client-data\classic-client`, read only.

| Case | Connections | Client up after 25 s |
|---|---|---|
| empty login, `-skiploginscreen` (a profile's first launch) | **0** | yes |
| saved username `probe`, `-skiploginscreen` | **1, at 2.4 s; no retry** | yes |
| saved username `probe`, autologin on, **no** `-skiploginscreen` | **0** | yes |

The third row is the one that matters: autologin alone would not have logged anyone in.

## 3. What changed (`D:\ShatteredLegacy\player-package`)

### 3.1 `payload\app\Launch-Settings.ps1` (new, 86 lines, dot-sourced)

The settings-path and settings-merge logic, pulled out of Play.ps1 so the tests can call it (the brief's
suggestion, as P26 did with `Build-UoOverrides.ps1`).
- `Get-LaunchTarget` (`:18-35`): `-Lan`/`-Test`/neither as before, plus `-Account`. Refusals at `:20`, `:22`
  (`-Account works only with -Test, so the live shard is never logged in automatically.`) and `:23`
  (`-Account '<x>' is not a profile name: use 1 to 24 of a-z, 0-9 and -.`). **`-cnotmatch`, case-sensitive**: `Admin`
  is refused, because Windows file names are not case-sensitive and `Elf`/`elf` would share a file. The brief's
  regex says lower case; PowerShell's `-match` would have let `Admin` through (mutation m3 proves the test sees it).
  "Bound" is `$PSBoundParameters.ContainsKey('Account')`, so `-Account ""` is refused too, not treated as absent.
- `Write-LaunchSettings` (`:38-86`): moved unchanged, then `:72-81`: a profile sets `saveaccount` and `autologin`
  true; plain `-Test` still forces both false; live and LAN untouched.

### 3.2 `payload\app\Play.ps1`

- Header `:9-16` and `:28-30`: the new switch.
- `:36` the `-Account` parameter; `:45-50` dot-source and `Get-LaunchTarget`, refusal as one red line and exit 1.
  This is the **first** thing the script does, before the update-backup restore, the client check, the update
  check and Setup, so a refusal writes nothing at all (the e2e facts check that `uo-path.txt` was not written).
- `:203-210` the updater hand-off (3.3).
- `:275-276` `Write-LaunchSettings` (replaces the old inline block).
- `:292-296` `-skiploginscreen` for a profile.
- The label line (`Write-Host "  $label"`, unchanged) now prints `TEST SHARD (throwaway), profile: gargoyle`. It is
  the console's first line, not a window title: the console closes once the game starts, and TazUO sets its own
  title in game.

### 3.3 `payload\app\Update.ps1`: why it changed

`Install-Package` hands over to the **new** package's `Update.ps1`, which relaunches `Play.ps1` with `-Test`/`-Lan`
only (`Update.ps1:315-319` before). An update taken from a profile shortcut would therefore come back as the plain
test login, once. Now:
- `Update.ps1:56` adds `[string]$Account` (the header says add, never rename or remove), `:320` passes it on, and
  `:10` and `:32-33` are the header.
- Play.ps1 passes `-Account` **only if the downloaded `Update.ps1` declares it** (`Play.ps1:206-209`, via
  `Get-Command ... .Parameters`, inside `try`). Passing it to an older updater (a rollback) would fail parameter
  binding, and the update would not run at all. Probed in 5.1: the new file gives True, HEAD's gives False, a file
  that does not parse gives False, and a missing file throws, which the `try` catches (the script runs under `Stop`).
- `settings*.json` was already never overwritten by an update (`Update.ps1:109`), so profile files survive updates.

### 3.4 Elsewhere

- `payload\README.txt:68-72`: the switch under "For the house".
- `tests\Build-UoOverrides.Tests.ps1:246`: its sandbox copies `Launch-Settings.ps1` (Play.ps1 now needs it).
- `.bat` files: **no change needed.** `Play-Test.bat` already passes `%*` after `-Test`.
- Every touched file: 0 bytes above 127, no CR, no em dash (python byte count).
- Not touched: `CHANGELOG.md` (outside the brief's files). A line for the next package's notes:
  "Test profiles: `Play-Test.bat -Account <name>` keeps one saved test login per name and logs straight in."

## 4. Tests: `player-package\tests\Launch-Settings.Tests.ps1` (new, 13 facts)

    powershell -NoProfile -ExecutionPolicy Bypass -File player-package\tests\Launch-Settings.Tests.ps1

Facts 1-8 call the functions and need nothing else. Facts 9-13 run the real `Play.ps1`, `Play-Test.bat` and
`Update.ps1` in a sandbox with P26's stub `TazUO.exe` (it writes its command line), each process started with a
raw command line (no PowerShell argument mangling). Refusals need no server; facts 9, 10 and 13 check the test
shard's port first, as Play.ps1 always does, so they need the test shard up.

| # | Fact | Brief's test |
|---|---|---|
| 1 | `AProfileGetsItsOwnTestSettingsFileAndALabelThatNamesIt` | 1 |
| 2 | `AProfileKeepsItsSavedLoginAcrossRelaunchesAndTurnsOnSaveAndAutologin` (two relaunches; an unowned setting kept) | 2 |
| 3 | `AFirstLaunchOfAProfileHasAnEmptyLoginWithSaveAndAutologinOn` | 2 |
| 4 | `WithoutAProfileTestStillForcesSaveAccountAndAutologinOff` | 3 |
| 5 | `LiveAndLanAreUnchanged` | 3 |
| 6 | `TwoProfilesDoNotShareAUsername` (and a new profile does not inherit `settings.test.json`'s login) | 5 |
| 7 | `AccountWithoutTestIsRefused` (alone, and with `-Lan`) | 2b |
| 8 | `ABadProfileNameIsRefused`: `''`, `../x`, `..\x`, `Admin!`, `Admin`, `GARGOYLE`, `a b`, `a.b`, `a_b`, 25 chars, `elf/x`, `c:` | 4 |
| 9 | `EndToEnd_AShortcutLaunch...`: **`Play-Test.bat -Account gargoyle`** exactly as a shortcut runs it; TazUO gets `-settings "<...settings.test.gargoyle.json>" -skiploginscreen`; `settings.test.json` byte-identical; no other file; then a saved login survives a relaunch and is **not** on TazUO's command line | 1, 2 |
| 10 | `EndToEnd_WithoutAProfileTestIsTodaysLaunch`: `settings.test.json`, no `-skiploginscreen`, both false, old label | 3 |
| 11 | `EndToEnd_AccountWithoutTestIsRefusedWithOneLineAndWritesNothing`: exit 1, exactly one line, no game, no settings file, Setup never ran | 2b |
| 12 | `EndToEnd_ABadProfileName...`: `../x`, `..\x`, `Admin!`, `Admin`, `"a b"`, `""`: same checks, and no `settings*.json` anywhere in the sandbox | 4 |
| 13 | `EndToEnd_AnUpdateRelaunchesTheSameProfile`: `Update.ps1 -Test -Account gargoyle` with nothing to change says "Already up to date" and starts the game on the gargoyle file with `-skiploginscreen` | (3.3) |

**Red, then green.**

| Run | Result |
|---|---|
| baseline, P26 suite, before any change | 8 / 8 |
| red: functions extracted, behaviour unchanged, no `-Account` | **11 failed, 2 passed** (5 and 10, the unchanged launches). Fact 4 was red only because `.Profile` did not exist yet, so m1 below is its real red |
| first green | 11 / 13: facts 11 and 12 failed on **a bug in the test** (a one-element array from a function unrolls to a string, so `$lines[0]` was a space). Fixed with `@()`, not by changing the launcher |
| green | **13 / 13**; P26 suite **8 / 8** |

**Deliberate breaks** (`notes\cc-P28-tools\mutate_launcher.py`, each restored and checked by SHA-256:
`Launch-Settings.ps1 92a42433eff0`, `Play.ps1 1dec2e40a227`, `Update.ps1 8a071a5e16a8`):

| Break | Facts that went red |
|---|---|
| m1 plain `-Test` no longer forces save/autologin off | 4, 10 |
| m2 a profile no longer turns them on | 2, 3, 9 |
| m3 `-cnotmatch` to `-notmatch` (case-insensitive) | 8, 12 |
| m4 `-Account` allowed without `-Test` | 7, 11 |
| m5 a profile shares `settings.test.json` | 1, 2, 6, 9, 13 |
| m6 Play.ps1 drops `-skiploginscreen` | 9, 13 |
| m7 Update.ps1's relaunch drops `-Account` | 13 |

**Package.** `Build-PlayerPackage.ps1 -Out <scratch>`: gates green, exit 0, `ShatteredLegacy-2026.10.02.0818.zip`,
80,074,411 bytes. **Counted in the zip: 977 files**, the 976 of `dist\...2026.10.02.0609.zip` plus
`app/Launch-Settings.ps1`, nothing else different. (The build prints "740 files"; that line does not count the
zip's entries, and P26 quoted the same 740. I did not chase what it counts.) Nothing went into `dist\`.

**Smoke of the built package**: extracted to scratch, `app\Play-Test.bat -Account gargoyle -NoUpdate` against the
real test shard. First line `TEST SHARD (throwaway), profile: gargoyle`; the real TazUO was running with
`-settings "...\settings.test.gargoyle.json" -skiploginscreen -uofilesoverride "...\files-override.txt"`;
`settings.test.gargoyle.json` was the only settings file, with save and autologin true, an empty username and port
2594. No login was typed; I stopped the client.

## 5. The desktop shortcuts (for the overseer's script)

One per profile. `<install>` is the folder Chase plays from, the one holding `Play Shattered Legacy.bat`.
`D:\UO\ShatteredLegacy-2026.10.02.0609` exists and has a `settings.test.json`, but **I have not confirmed it is the
install he uses**. Updates are in place, so the path does not change with versions.

| Shortcut | Target | Arguments | Start in |
|---|---|---|---|
| Admin (TEST) | `<install>\app\Play-Test.bat` | `-Account admin` | `<install>\app` |
| Human (TEST) | `<install>\app\Play-Test.bat` | `-Account human` | `<install>\app` |
| Gargoyle (TEST) | `<install>\app\Play-Test.bat` | `-Account gargoyle` | `<install>\app` |
| Elf (TEST) | `<install>\app\Play-Test.bat` | `-Account elf` | `<install>\app` |

So, for example, the full target line is `"<install>\app\Play-Test.bat" -Account gargoyle`. Use the .bat, not
`powershell.exe -File Play.ps1`: it adds `-Test` itself and **pauses on a failure**, so a refusal or "Cannot reach"
stays on screen. Run: Normal window (minimised would hide that pause). Icon: `<install>\app\tazuo\TazUO.exe`.
No password and no UO account name go in a shortcut.

## 6. Worth knowing

- **First launch of each profile:** the login screen, with Save Account and Autologin already ticked. Type the
  account once. If the box is unticked by hand, the next launch ticks it again (the launcher owns that value).
- **Four clients at once share one `Data\Profiles\lastcharacter.json`.** TazUO loads the list at start and rewrites
  it whole when a character is picked (`LastCharacterManager.cs:54-78`), so with several clients open, a later pick
  can overwrite another profile's entry with an old copy. Effect: that profile's next autologin picks the **first**
  character on the account (`LoginScene.cs:594-621`, `charToSelect` stays 0). Harmless for one character per test
  account. A known edge, not fixed: it is TazUO's file.
- A saved login with a wrong password: one attempt, TazUO's error popup, and the login screen. No loop (section 2).
- The password is stored the way TazUO stores it today (its `Crypter` encoding in the settings file). That is
  obfuscation, not encryption. It is TEST only, by design.
- `settings.test.json` (the plain TEST shortcut) is unchanged and still never saves a login.

## 7. Not verified

- **Anything after a real login**: server auto-pick, last-character auto-pick, and entering the world. I cannot log
  in to the test shard. Proposed T-row: "Gargoyle shortcut: first launch shows the login screen with Save Account
  ticked; log in and pick the character; close; the second launch reaches the world as that character with no
  clicks. Repeat for one more profile, then open two at once."
- The real `Install-Package` hand-off end to end (download, then a new window, then relaunch). Fact 13 covers the
  updater's relaunch, and the `Get-Command` check was probed on its own; the HTTP path was not run.
- HTTPS and publishing: unchanged, not run.

## 8. Files

```
D:\ShatteredLegacy\player-package\
  payload\app\Launch-Settings.ps1        NEW  target and settings merge, -Account
  payload\app\Play.ps1                   -Account, refusal first, -skiploginscreen, updater hand-off, header
  payload\app\Update.ps1                 -Account passed through to the relaunch, header
  payload\README.txt                     the switch under "For the house"
  tests\Launch-Settings.Tests.ps1        NEW  13 facts
  tests\Build-UoOverrides.Tests.ps1      sandbox copies Launch-Settings.ps1
D:\UO\shard-migration\notes\
  cc-P28-launcher-account-profiles.md    this note
  cc-P28-tools\mutate_launcher.py        the 7 breaks
  cc-P28-tools\probe-autologin.ps1       the TazUO startup probe
```

## Checklist for Chase

1. [ ] Commit: `D:\UO\Commit-ShardWork.ps1` (the files in section 8; nothing else of mine is in either tree).
2. [ ] Optional: run the tests with the test shard up:
       `powershell -NoProfile -ExecutionPolicy Bypass -File player-package\tests\Launch-Settings.Tests.ps1`
       (13 facts, exit 0).
3. [ ] Build the package: `.\player-package\Build-PlayerPackage.ps1` (add `-Notes` from section 3.4 if you like).
4. [ ] Get it into your install: publish and let Play update itself, or unzip over your install. Your
       `settings*.json` files are kept either way.
5. [ ] Run the overseer's shortcut script (section 5 has the target, arguments and start-in for each).
6. [ ] Double-click each shortcut once, log in with Save Account ticked, pick the character. From the second
       launch on it should go straight in: that is the T-row in section 7.
