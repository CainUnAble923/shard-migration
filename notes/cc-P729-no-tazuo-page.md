# cc-P729: the player package no longer opens TazUO's own page at a new character's start

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P729`. Not committed, nothing deployed, Haven not touched, no package built or published.

## In plain words

- **The page was TazUO's own "TazUO Version History" window.** It has a changelog note, the TazUO Wiki and TazUO
  Discord links, and it opened on top of the isle's first scene. A new character's first login no longer opens it.
- **Characters that already exist are unchanged.** The window opens once per client version, so they have already seen
  it. A default the player saved themselves is never touched. Anyone can still open the window by typing `-version`.
- **For you:** nothing to rebuild. This is a launcher change only, not a client patch, so the next package build
  carries it. To see it, make a new character after updating.

## What it was, exactly

Not a browser page, a welcome gump, or the wiki or Discord link on its own. It is TazUO's `VersionHistory` gump
(TazUO `3212623f`, `src/ClassicUO.Client/Game/UI/Gumps/VersionHistory.cs`). Its parts:
- the title "TazUO Version History";
- "Version history can now be found on our GitHub repo CHANGELOG.md file.";
- links to the main and dev changelogs, the TazUO Wiki and the TazUO Discord.

I saw this same window myself in P679's first-login TazUO shots (`notes\art\sos-s4-gates\first-try\`, the "Version
History ... TazUO Wiki / TazUO Discord" panel behind the patch notes).

**What opens it** (`Game/UI/Gumps/WorldViewportGump.cs:108-114`), when the world view is built at login:

```
if (ProfileManager.CurrentProfile.LastVersionHistoryShown != CUOEnviroment.Version.ToString())
{
    UIManager.Add(new VersionHistory(world));
    ProfileManager.CurrentProfile.LastVersionHistoryShown = CUOEnviroment.Version.ToString();
    LegionScripting.LegionScripting.DownloadApiPy();
}
```

`CUOEnviroment.Version` is the client assembly's version. That is `TazUO.dll`'s `AssemblyVersion`: 5.31.2 in
`ClassicUO.Client.csproj`, read as **"5.31.2.0"** from the package's `TazUO.dll` and stored as such in real profiles.
A new character's profile has no stored version, so the window always opened at its first login.

## The setting

**`last_version_history_shown`** in the character's `profile.json` (`Profile.LastVersionHistoryShown`,
`Configuration/Profile.cs:719`, snake_case by `SnakeCaseNamingPolicy`). TazUO has no on/off switch for this window;
this per-profile "already shown for version X" key is the only control. So no client patch was needed (the prompt's
rule: patch TazUO only if no setting exists).

**How new profiles get it** (P719's route): TazUO builds a new character's `profile.json` from
`Data\Profiles\default.json` (`ProfileManager.NewFromDefault`). The launcher now also writes the version of the client
it is about to start into that file:
- `player-package\payload\app\Launch-Settings.ps1`:
  - `Get-TazUOClientVersion -ClientDir` reads `TazUO.dll`'s AssemblyVersion (`[Reflection.AssemblyName]::GetAssemblyName`;
    PowerShell 5.1 reads the .NET 10 assembly's metadata fine). It returns `$null` when there is no readable dll.
  - `Initialize-NewProfileDefaults -ProfilesDir -ClientDir` writes `always_run`, `sl_open_paperdoll_at_login` (P719)
    and `last_version_history_shown`.
- `Play.ps1` passes the folder of the client it starts: the package's `app\tazuo`, or a `-ClientDir` client.

**Who gets what:**
- **New characters:** no window.
- **Existing characters:** their own `profile.json` is never read for this, so nothing changes. They saw the window once
  at their first login and stored 5.31.2.0, so it does not come back on this client.
- **A default the player saved** (Options > Profile, "Set as default"; a whole profile, with keys the launcher never
  writes): left byte for byte. Characters made from it then follow whatever that saved default says.
- **Our own default from P719** (only the launcher's keys): updated in place. The version key is added at the first
  launch after this update, and moved to a newer client's version after a TazUO upgrade, so a future upgrade does not
  bring the window back for new characters. This is the one change from P719's "write only when there is none". A file
  holding only our own keys is ours, not a player choice.
- **No readable `TazUO.dll`:** the other defaults are still written, without the version, and the window opens as
  before. Nothing breaks.

**What a new character skips with it:** the same branch calls `LegionScripting.DownloadApiPy()`. It downloads TazUO's
dev-branch `API.py` from GitHub into the client's `LegionScripts\` folder and makes `__builtins__.py` there if missing.
- `API.py` is a stub for script editors. The script list skips it (`LegionScripting.cs:229, 271`), and the package
  treats both files as the client's own (`LegionScripts.ps1:32`).
- The folder is per install, not per character, so an install whose older characters already saw the window has it.
- On a brand-new install it is now fetched only when someone types TazUO's own **`-updateapi`** command
  (`CommandManager.cs:36-39`), which does exactly this.

I left it so rather than patch the client: it pulls an unpinned file from the internet, which a new player does not
need.

## Tests

`player-package\tests\No-TazUO-Page.Tests.ps1` (new, 7 facts):
- Each client folder holds a stand-in `TazUO.dll` compiled with a known `AssemblyVersion`, so the test needs no client.
- `Test-OpensVersionPage` mirrors TazUO's rule above: a new profile is `default.json`, and the window opens unless its
  key equals the client's version.

The facts:
1. **A fresh profile opens no TazUO page at start.** The control: with no `default.json` it would.
2. P719's two-key file gets the version too.
3. After a client update (5.31.2.0 to 5.40.0.0) a new character still opens no page, and an up-to-date file is not
   rewritten.
4. A default the player saved is never changed.
5. A character's own `profile.json` is left alone.
6. A client folder with no readable `TazUO.dll` still gets P719's defaults.
7. `Play.ps1` passes the started client's folder.

Results:
- **Red** on the launcher before the change (`notes\cc-P729-tools\red-no-tazuo-page.txt`): facts 1, 2, 3 and 7 fail.
  Facts 4, 5 and 6 are guards, already true.
- **Green**: 7 of 7 (`green-no-tazuo-page.txt`).
- P719's `New-Profile-Defaults.Tests.ps1` stays 5 of 5 (`green-new-profile-defaults.txt`).
- `Launch-Settings.Tests.ps1` 27 of 27 and `Launch-Overrides.Tests.ps1` 19 of 19.
- `Package-Client.Tests.ps1`: 6 of 9 fail **here only for want of EA client data**. "No EA client data in
  ...\client-data\classic-client (-UoData): gate 4 needs its file": this work copy has no `client-data\`, which is
  git-ignored. Its real builds never reach the launcher code.

Not tried in a real client: the rule is TazUO's own three lines above, and P679's shots on this exact client showed
the window and the stored "5.31.2.0" (`D:\UO\golem\legion-test\Iron\client\Data\Profiles\...\profile.json:478`).

## Files

- Code copy:
  - `player-package\payload\app\Launch-Settings.ps1`, `Play.ps1`;
  - `player-package\tests\No-TazUO-Page.Tests.ps1`;
  - `CHANGELOG.md` (2026.10.28.8, Changed) and `VERSION`.
- Docs copy: this note, `notes\cc-P729-tools\` (the red and green outputs).

P729 DONE
