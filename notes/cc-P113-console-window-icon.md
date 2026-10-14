# cc-P113: The Shard Console uses its desktop-shortcut icon inside the app

2026-10-14. Prompt: `D:\UO\cc-prompts\cc-P113-console-window-icon.md`. `scripts\Shard-Console.ps1` and its tests only.
No deploy.

## Headlines

- **The console's window now shows the desktop shortcut's icon** in the title bar, the taskbar and Alt+Tab. It is the
  exact file the shortcut uses: `docker\website\html\favicon.ico` (11,476 bytes). That file is resolved from the repo
  root, not copied and not an absolute path.
- **Every form the console makes gets it:** the main window and its three dialogs (the typed confirmation, the list
  picker, the wipe-admin picker), through one helper, `Set-ConsoleIcon`. The icon is loaded once per file and shared.
- **Missing or unreadable file:** the form keeps Windows' default icon, one line goes to the action log (`icon not
  loaded: <reason>`, once per file however many forms open), and there is no popup and no failure.
- **Seen in the real console, started through `D:\UO\tools\Run-ShardConsoleLogged.ps1`** (not edited):
  - the live window's icons, read back from the window itself, are the sword-in-ring logo of `favicon.ico`;
  - the startup log shows `START` and `EXIT closed normally, errors logged this session: 0`, with no ERROR lines (three
    runs).
- **Tests:** 3 new facts, each seen failing first. Full suite under Windows PowerShell 5.1: **309 facts, 307 passed**.
  The 2 failures are not this change (below).

## What changed, with file:line (`D:\ShatteredLegacy`)

| File:line | Change |
|---|---|
| `scripts/Shard-Console.ps1:306` | `Get-ConsoleConfig`: `WindowIconFile`, `Join-Path $RepoRoot 'docker\website\html\favicon.ico'` |
| `scripts/Shard-Console.ps1:4585` | `Get-ConsoleIcon`: loads `New-Object Drawing.Icon <path>` once per path and keeps it (`$script:ConsoleIcons`); a missing or unreadable file gives `$null` and one `Write-ConsoleLog` line |
| `scripts/Shard-Console.ps1:4603` | `Set-ConsoleIcon $Form $Config`: sets `.Icon` when there is one, else leaves the default |
| `scripts/Shard-Console.ps1:6776`, `:6833`, `:6983` | the three dialogs: `Show-TypedConfirm`, `Show-ListPicker`, `Show-WipeAdminPicker` |
| `scripts/Shard-Console.ps1:7242` | the main form, in `New-ConsoleForm` |
| `scripts/tests/Shard-Console.Tests.ps1:5176-5250` | 3 facts |
| `CHANGELOG.md`, `VERSION` | 2026.10.14.19, one `### Staff` line |

**The forms, counted:** `New-Object Windows.Forms.Form` appears four times (the main form and the three dialogs); a
fact checks every one is followed by `Set-ConsoleIcon`. The **`-Action` child windows** are plain PowerShell console
windows (conhost), not forms of the console's, so there is nothing to set there.

## Tests

`scripts\tests\Shard-Console.Tests.ps1`:
1. `P113_TheIconIsTheShortcutsFileResolvedFromTheRepoRoot`: `WindowIconFile` is `<repo>\docker\website\html\favicon.ico`;
   the file exists; it is the file `Desktop\Shard Console.lnk` names (`...\docker\website\html\favicon.ico,0`).
2. `P113_TheMainFormAndEveryDialogGetTheIcon`:
   - a built main form (`New-ConsoleForm`, dry run) holds the very Icon object `Get-ConsoleIcon` loaded, and it was
     loaded once;
   - the three dialogs block on `ShowDialog`, so their wiring is read from the source: every
     `$x = New-Object Windows.Forms.Form` (four) is followed by `Set-ConsoleIcon $x`.
3. `P113_AMissingIconKeepsTheDefaultAndLogsOneLine`:
   - a missing file keeps the form's default icon, and two forms make exactly one `icon not loaded: no file at ...`
     line;
   - an unreadable file (text named `.ico`) also keeps the default and logs its own line.

**Seen failing first:**
- **Against the console before this change** (`git show HEAD:`): 3 of 3 failed. Two of them only because the helpers did
  not exist, which proves little, so also:
- **A mutant with the helpers** (one dialog's call removed, the cache removed, the main form's call removed): fact 2
  failed ("the main form shows it") and fact 3 failed (two log lines, not one). Fact 1 passed; the config line was
  untouched.
- **A mutant with only the dialog's call removed:** fact 2 failed ("line 6832 makes a form without the icon").
- Each mutant was restored from a copy and checked byte-identical; then 3 of 3 passed.
- **A test bug of mine, caught on the first run:** fact 2 read the form's variable from `$Matches` after a `-notmatch`
  had overwritten it, so it failed on the real code. It now saves the name first.

**Full suite (Windows PowerShell 5.1): 309 facts, 307 passed, 2 failed.** Neither is this change:
- `P107_TheSnapshotSendsNothingBeforeTheCutoverAndDryRunPrintsItsJson`: fails in every run since the `SL game PC
  snapshot` task was installed (P108 notes).
- `P84_TheUOLookAddsUnderASecondToTheStart`: a timing fact, 1,050 ms against a 1,000 ms limit. Rerun in its own group 3
  times: **passed, failed (1,893 ms), passed**. It also failed in P110's full run before this change. The icon is set
  the same way in both looks, so it adds nothing to the difference this fact measures. A flaky fact, for the overseer.

**The real console:**
- Started three times through `Run-ShardConsoleLogged.ps1`: the window appears about 44 s after start (it reads Docker
  first). It was then closed with `CloseMainWindow`, and each run logged `EXIT closed normally, errors logged this
  session: 0` and no ERROR lines.
- The live window's icons, read with `WM_GETICON`, are 32x32 (taskbar, Alt+Tab) and 16x16 (title bar). Drawn out, both
  are the sword-in-ring logo. That is the art of `favicon.ico`'s own frames: its 4 frames (16, 32, 48 and 64 px) are
  PNG-compressed, and the 64 px PNG, extracted with a direct parse of the file, shows the same logo. The Windows Forms
  default icon is a different picture.
- **A wrong turn, for the record:** my first check compared pixels with `favicon.ico`'s own `Icon.ToBitmap()` and read
  "100% different". .NET Framework's `ToBitmap` cannot decode PNG-compressed icon frames and returns noise; Windows
  draws them correctly. The images and the direct parse settled it. Nothing in the console uses `ToBitmap`.

## Deviations and decisions for Chase

1. **Loaded on first use, not inside `Get-ConsoleConfig`.** The config carries the path; `Get-ConsoleIcon` loads it the
   first time a form needs it and keeps it. The prompt said "load once where the config is built". The config builder
   runs dozens of times in the tests and before WinForms is loaded, so loading there would load it many times. It is
   still loaded once per run.
2. **No copy under `scripts\`.** The prompt asked me to say whether a copy would be safer. It would protect the console
   if the website ever changes its favicon, but then the shortcut and the window could differ. Using the same file
   keeps them matched, and the shortcut already depends on it. **Your call; I did not copy it.**
3. **The `-Action` windows** are console windows, so they keep PowerShell's icon.

## For Chase

Close the console and reopen it from the desktop shortcut: the title bar and taskbar show the shortcut's icon. No deploy.

## Repo size

4 files changed, 102 lines added; no new files.

## Commit preflight

`D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: `CHANGELOG.md`, `VERSION`, `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`. docs: this note.
The proof images (`p113-icons*.png`, `p113-fav-*.png`) are in the session scratchpad, outside both repos.

P113 DONE
