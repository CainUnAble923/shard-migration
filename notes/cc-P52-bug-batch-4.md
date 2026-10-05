# cc-P52: bug batch 4 (D59, D60, D61, P35 kit, D65, D67, D68, D47)

2026-10-04. Brief: `D:\UO\cc-prompts\cc-P52-bug-batch-4.md`. Engine: `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88` (`rev-parse HEAD` today). Shard HEAD `39a2da8`, tree clean when I started.
"C\" = `D:\ShatteredLegacy\server\customizations\`, "T\" = `D:\ShatteredLegacy\server\tests\`, "P\" =
`D:\UO\ModernUO-pinned\Projects\`. Scratch: `D:\UO\cc-p52-work\`. Nothing committed, nothing deployed, no shard touched.
No clash: no other builder ran in `D:\ShatteredLegacy` while I worked. P53's work (200 cap) not started.

## Headlines

1. **All eight parts done and green.** Final build `docker\uo\build.sh -t sl-modernuo:cc-p52`: **42/42 patches**,
   **671/671 shard facts** (637 before plus 34 new), image `sl-modernuo:cc-p52` = **`88b7983f2d29`**.
   `sl-modernuo:latest` not moved (`aead9f7f5e2e` before and after, P51's image). Package: a fresh build into
   `D:\UO\cc-p52-work\pkg\` passed gates 1 to 6 (build exit 0) and `-CheckZip` (gates 4, 5, 6). Package facts
   `Launch-Settings.Tests.ps1` **20/20** (13 before plus 7). Shard-Console facts **94/95** (87 before plus 8 new); the one
   failure is **pre-existing at HEAD** and not mine (headline 7).
2. **Every new fact watched red.** Server: three scratch trees (`D:\UO\cc-p52-work\make-red.py`, built with `build.sh
   --tests-only` under their own tags): red-a (all of P52 undone, APIs kept) fails **27 of the 34**; red-b (the hammer
   counting a container again, hooks kept) fails the **4** absence cases red-a cannot; red-c (restore no longer
   re-applies) fails the **2** restore-while-held cases. The one fact never red is the hammer restore gump's Back, which
   existed before P52 (Part E). PowerShell: every new fact fails against the HEAD scripts, and behaviour-level reds
   (fallback overrides a player's own driver; a failed DNS check shown red; an adapter alone deciding "VPN on") fail
   exactly the facts aimed at them. Table below.
3. **Part C decision: keep OpenGL, fall back to 3 only after TazUO logs the OpenGL 2.1 crash.** 0 is OpenGL in the
   shipped TazUO, and 3 on a real GPU would move every player to SDL_GPU (Vulkan or Direct3D 12), an untested renderer
   for us. The launcher now waits up to 20 s after starting the client; on that crash it writes `force_driver: 3` where
   the value is still 0 and starts the client again. A player's own 1, 2 or 3 is never changed.
4. **Part D cause proven in a real sandbox:** Windows Sandbox (Windows 11 24H2, build 26100) has **no notepad.exe**, and
   `Start-Process notepad.exe` was the kit's last step. The fixed kit, in one Build-mode smoke start, wrote "README opened
   with the .txt handler (notepad.exe is not on this computer)". I closed that sandbox with `wsb stop`.
5. **Part B cliloc: 1112530 "Knowledge"** (no cliloc says "familiarity"; read from the client's own compressed
   `Cliloc.enu`, decompressed with pinned's `BwtDecompress.cs`).
6. **Two premises in the brief were off, said here so nobody trusts them:** (a) Part H: the console's other checks do
   **not** run off the UI thread; they run on a `Windows.Forms.Timer` tick with short timeouts
   (`scripts\Shard-Console.ps1`, the 30 s timer and `Invoke-DockerRead`). The new DNS check really does run in a runspace
   of its own. (b) Part E: the contract ledger already drew a Back button, but it did nothing for the smith guild.
7. **Found, not mine:** `RedMeansTestOnlyUnclassifiedOrAPlainRunThatDeletesAndNothingElse` (Shard-Console facts) fails at
   HEAD `39a2da8` too (run from a `git archive HEAD` copy): its hard-coded red list predates `[SL` (P51) and
   `[ClusterFDespiseStockCleanup`. Not changed: whether `[SL` should be red is a judgment for whoever owns that list.
   Also `WispOrbPossessionVerification ... (Silenii, Phantom)` failed once in red-a and passed in builds 2, 3 and final:
   looks flaky, unverified. `docker ps` shows `sl-ddns` "unhealthy" (D23 territory), left alone.

## What changed (all uncommitted)

Shard (`D:\ShatteredLegacy`):

- `C\HammerOfHephaestus.cs` (a full-file replacement of pinned's, routed as before): Parts A, B, and the restore gump's
  Back (E).
- `C\SmithSealCatalogGump.cs`, `C\SmithGuildmasterGump.cs`, `C\SmithGuildBook.cs`, `C\SmithCommissionGump.cs`,
  `C\SmithBulkOrderChoiceGump.cs`, `C\CrossGuildExchangeGump.cs`, `C\GuildContractLedgerGump.cs`, and the Exchange's
  four other openers `C\MinersCompactLiaisonGump.cs`, `C\ForestersGuildmasterGump.cs`, `C\OutridersGuildmasterGump.cs`,
  `C\ArtificersGuildmasterGump.cs`: Part E.
- `C\StaffHub\StaffHubGump.cs`, `C\StaffHub\ClusterFStaffHub.cs`: Part F.
- `C\ClusterFGuildSystem.cs`, `C\ClusterFGuildStarterPath.cs`, `C\ArtificerWorkOrderSystem.cs`,
  `C\GuildContractLedgerGump.cs`: Part G.
- Facts (new): `T\Engines\Craft\HammerHeldBonusVerification.cs` (A, B: 17 cases),
  `T\Misc\SmithBackButtonsVerification.cs` (E: 10), `T\Misc\StaffHubReadabilityVerification.cs` (F: 5),
  `T\Misc\SmithGuildNameVerification.cs` (G: 2).
- `player-package\payload\app\Launch-Settings.ps1`, `...\Play.ps1`, `player-package\tests\Launch-Settings.Tests.ps1`: C.
- `player-package\clean-test\Inside-Start.ps1`: D.
- `scripts\Shard-Console.ps1`, `scripts\tests\Shard-Console.Tests.ps1`: H.
- No patch added or changed (`server\patches\`, `apply-patches.sh` untouched).

This repo: this note; `README.md`, `dashboard.html`, `tools\progress.json` from `tools\progress.py` ("Overall: 27%",
Content 551/2045, Setup 7/7; "808 customization files, 47 patch files, 502 tests in 99 files").
`docs\bug-list.md`, `docs\league-storyline.md` and `notes\passdown-overseer-2026-10-03.md` were already modified when
I started; not mine, not touched.

## Part A: the Hammer of Hephaestus bonus only while held (D59)

**Cause** (as the bug row read it, confirmed): `OnAdded` applied the base SkillMod for a parent that was the player or
any container rooted at the player; `GuildmasterRestore` used `RootParent`; the mods are not serialized and nothing
re-applied them after a load; passive regen out of exhaustion cleared `_exhausted` without re-applying. The Reinforced
hammer's `RecordFamiliarity` also applied the familiarity mod to the crafter wherever the hammer was
(`UpdateSkillMod(from)`), so crafting from the pack added it too.

**Change** (`C\HammerOfHephaestus.cs`, both tiers):
- `HeldBy => Parent as Mobile` (`:246`, `:622`); `ApplyHeldBonus()` (`:249`, `:628`) removes this hammer's own mod(s)
  first, then adds them only for a held, usable, undeleted hammer. Every path calls it: `OnAdded` (`:444`, `:846`),
  restore (`:481`, `:883`), regen out of exhaustion (`:224`, `:599`). T2's `UpdateSkillMod()` (`:699`) applies only to
  the holder. One mod of each kind per hammer at any time, because each apply removes its own first.
- **The load hook: `Timer.DelayCall(ApplyHeldBonus)` at the end of `Deserialize`** (`:199`, `:574`). Argued:
  - It is the shape pinned uses for exactly this: `BaseWeapon`'s `[AfterDeserialization]` re-adds its SkillMods from
    `Parent as Mobile` (`P\UOContent\Items\Weapons\BaseWeapon.cs:3551-3571`). Our hammer has a hand-written
    `Deserialize`, so the generator's attribute is not wired; the delayed call is the same thing by hand.
  - It runs after the whole world has loaded, when `Parent` (read in `Item.Deserialize`, `P\Server\Items\Item.cs`
    around `:2913-2930`) is the live mobile. `Mobile.AddSkillMod` (`P\Server\Mobiles\Mobile.cs:3500-3512`) does not
    care what map the owner is on, so a held hammer on an **offline** character (on Map.Internal) gets its bonus too.
  - **No login hook**: SkillMods live on the Mobile in memory and nothing in `P\Server` clears them on logout (the only
    removals are `RemoveSkillMod`, `Mobile.cs:3535-3579`, and `SkillMod.Remove`). So once applied after the load, a
    held hammer keeps its bonus across any number of logouts until the next restart, where the load hook applies it
    again. Chase's "logged in with the hammer equipped: 111" was the first login after a restart: the load case.
- The header comment's "display-only until Phase 4E" text is replaced with what the code now does.

**Facts** (`T\Engines\Craft\HammerHeldBonusVerification.cs`, every case for T1 and T2): in pack none, held one;
held then pack none; three round trips then held: one; a held hammer serialized and deserialized has none until the
load tick and one after (in the pack: none); restore and regen while held add it, in the pack do not (two restores in
a row still one mod); T2's familiarity mod (250 Iron = +0.1, total 10.1) follows the same rule including after a load.

## Part B: Metal Familiarity in the single-click menu (D60)

**Change:** `HammerFamiliarityEntry` (`C\HammerOfHephaestus.cs:896`), added by both hammers' `GetContextMenuEntries`
(`:383`, `:791`). Shown to the character carrying the hammer (in hand or in their pack: `RootParent == from`) while
alive; selecting it sends `HammerFamiliarityGump` anywhere. Double-click behaviour unchanged.

**The cliloc.** The client's `D:\UO\UltimaOnlineVanilla\Cliloc.enu` is BWT-compressed (its first int is not the
plain header). I decompressed it with pinned's own `P\Server\Client\BwtDecompress.cs`, called as
`Localization.cs:98-119` does (scratch project in my scratchpad), 124,000 entries. No entry mentions "familiar" except
the necromancer's Summon Familiar. Candidates read from it:
- **1112530 "Knowledge"** (chosen: the panel is the hammer's knowledge of each metal);
- 3000098 "Information", 3000484 "Info", 3002140 "Overview", 1165983 "Progress", 3000132 "Status".
Pinned sends any number above 0x7FFF as is (`P\Server\ContextMenus\ContextMenuEntry.cs:39-48`) and switches the menu to
the newer packet for numbers outside 3000000-3032767 (`ContextMenu.cs:51-54`), which every client we ship speaks. Easy
to swap: `HammerFamiliarityEntry.Cliloc`.

**A custom cliloc ("Metal Familiarity"), not done, what it would take** under `notes\client-policy-2026-10-02.md` (ship
our patches, applied to EA's files on the player's machine): Build-UoOverrides.ps1 would patch a copy of the player's
`Cliloc.enu` the way it patches `tiledata.mul` (P26): decompress BWT (the file is compressed now), add our number and
text, write it uncompressed, and the client must read it from the override folder. Unverified: whether TazUO's
`-uofilesoverride` covers `Cliloc.enu`, and whether the client accepts an uncompressed file there (pinned's reader
accepts both, `Localization.cs:105-124`). A number range of our own would also need picking so no EA patch collides.

**Fact:** for both hammers, held and in the pack, the owner's menu has exactly one `HammerFamiliarityEntry` (number
1112530) and another character's has none; `OnClick` sends the gump.

## Part C: client graphics fallback (D61)

**Evidence read:**
- Shipped client: `D:\UO\TazUO\client\TazUO.exe` is 26.0909.63+**3212623f**, source at
  `D:\UO\cc-p40-work\tazuo-3212623f`. In it, `src\ClassicUO.Client\Main.cs:211-227`: `switch (ForceDriver) { default:
  case 1: FNA3D_FORCE_DRIVER=OpenGL ...; case 2: Vulkan; case 3: /* SDL/FNA auto-select */ break; }`. So **0 is not
  "let FNA choose": 0 falls into `default:` and forces OpenGL**, same as 1. Today every player runs OpenGL. The
  command-line parser (`:450-480`) keeps 1, 2, 3 and turns anything else into 0. (There is no 4/D3D11 in this build;
  the newer `cc-p40-work\tazuo` HEAD has one, which we do not ship.)
- **3** sets no driver, so FNA3D tries its list in order: `SDLGPUDriver`, `D3D11Driver`, `OpenGLDriver`
  (`external\FNA\lib\FNA3D\src\FNA3D.c:42-53`, first whose `PrepareWindowAttributes` succeeds, `:188-203`). The shipped
  `FNA3D.dll` has the SDL_GPU driver compiled in (its strings include `SDLGPU` and "SDL_GPUSupportsProperties failed").
  In P35's sandbox, 3 got D3D11 through `d3d10warp.dll` (evidence-5), i.e. SDL_GPU refused and D3D11 (WARP) took it.
- **What 3 would pick on a normal gaming PC:** SDL_GPU, which on Windows means Vulkan or Direct3D 12 (whichever SDL3's
  own order picks; SDL3's source is not in the tree, so which of the two is unverified). Not OpenGL. Players might
  notice different frame pacing and vsync behaviour, different driver bugs, and possibly shader or filtering
  differences: a renderer change we have never tested.
- The crash is logged where the launcher can see it: `app\tazuo\Logs\<yyyy-MM-dd_hh-mm-ss>_crash.txt`
  (`Main.cs:88-96`, `ClassicUO.Utility\Logging\LogFile.cs:18`), containing "OpenGL 2.1 support is required!". The real
  one from P35's sandbox, `app\tazuo\Logs\2026-10-04_07-10-03_crash.txt` (evidence-2.txt:174), has exactly that name
  shape and text.

**Decision: the third option, fall back to 3 only after that crash.** Passing 3 always (option 1) or writing it into
every settings file (option 2) moves every working player off OpenGL to an untested renderer to fix a case (no OpenGL
2.1: VMs, RDP, Microsoft Basic Display) few real players have. Option 2 also cannot tell a player's own 0 from the
default, and option 1 overrides a player's choice outright (the command line wins over the file). The fallback keeps
every working PC exactly as today and fixes the broken one, at the cost of one crash on that PC.

**Change** (`player-package\payload\app\Launch-Settings.ps1`):
- `Get-ForceDriver` (`:105`): the file's value, 0 when missing or unreadable.
- `Find-OpenGlCrash` (`:117`): the newest `*crash.txt` in `Logs` at or after a time that contains the OpenGL 2.1 text.
- `Set-GraphicsFallback` (`:131`): writes `force_driver: 3` into every `settings*.json` whose value is 0, keeping
  everything else (login above all), no BOM. A player's 1, 2 or 3 is never touched.
- `Start-TazUO` (`:150`): before the start, a PC that already logged the crash gets the fallback first (covers a player
  who closed the window); then it starts the client, waits up to 20 s, and if the client exited having written that
  crash since this start, applies the fallback and starts it again once (one yellow line). If the player's own value
  was non-zero it says so in red and changes nothing. TazUO keeps `force_driver` in its own settings when it saves, so
  the 3 persists. Settings files created later (a first TEST profile) start at 0 and fix themselves the same way.
- `Play.ps1:305-308` calls it instead of `Start-Process`. **Visible change for every player:** the launcher window now
  stays up to 20 seconds ("Starting the game...") instead of closing at once.

**Facts** (`player-package\tests\Launch-Settings.Tests.ps1`, the repo's own Fact harness, not Pester: the existing
files say why, Windows ships Pester 3.4): reading 0/missing/3/unreadable; only an OpenGL crash since the launch
counts; the fallback writes 3 over 0 only, keeps the login, no BOM; end to end with a stub TazUO that crashes unless
its settings say 3: crash then fallback then a good start, and the next launch starts on 3 at once; a player's own 1
is not changed and not restarted; an earlier crash switches before the launch; a normal start is left alone. These
need no server. **One of them caught a real bug of mine first:** I had given the crash window 2 s of slack, and the
previous launch's crash log counted as this launch's.

Package: fresh `Build-PlayerPackage.ps1 -Out D:\UO\cc-p52-work\pkg` exit 0 (gates 1 to 6), zip
`ShatteredLegacy-2026.10.04.2114.zip`, 76 MB, 740 files; `-CheckZip` gates 4, 6 and 5 passed. The zip's
`app\Launch-Settings.ps1` and `app\Play.ps1` carry `Start-TazUO`; no clean-test file ships. Not published.

## Part D: the sandbox kit's start script (P35 follow-up)

**Cause:** `Inside-Start.ps1`'s last step was `Start-Process notepad.exe` (`:122` before). Windows Sandbox on Windows 11
24H2 has no `notepad.exe` (Notepad is a Store app there and the sandbox has none). The error text is exactly
Start-Process's for a missing program: `Start-Process sl-p52-no-such-program.exe` here gives "This command cannot be
run due to the error: The system cannot find the file specified." (`InvalidOperationException`). Everything before it
had run, which is why the zip still reached the desktop. The LogonCommand itself was fine.

**Change** (`player-package\clean-test\Inside-Start.ps1`): `Open-ReadMe` (`:39`) tries `notepad.exe` only if
`Get-Command` finds it, then the .txt file's own handler (`Invoke-Item`), and otherwise says the README is on the
desktop. It never fails the start. `results\inside-start.txt` records how it ended (`:142-144`). `-Notepad` (`:30`)
exists only so a dry run can name an editor that is not there.

**Proof:**
1. Dry run on the host, red: HEAD's script with the editor renamed to a missing one ends "INSIDE-START FAILED: This
   command cannot be run due to the error: The system cannot find the file specified." (the sandbox's line, word for
   word) with the desktop files already copied. Green: the new script with `-Notepad sl-p52-no-notepad.exe` writes
   `inside-start.txt` "README opened with the .txt handler (sl-p52-no-notepad.exe is not on this computer)".
   (`D:\UO\cc-p52-work\partD\`.)
2. **One Build-mode smoke start** (allowed by the brief): `Start-CleanTest.ps1 -Mode Build -Zip
   D:\UO\cc-p52-work\pkg\ShatteredLegacy-2026.10.04.2114.zip`, run folder `D:\UO\clean-test-results\20261004-212038`.
   `results\inside-start.txt`: "README opened with the .txt handler (notepad.exe is not on this computer)"; baseline
   CLEAN, Windows 11 Enterprise 24H2 build 26100.9457. Nothing installed or clicked; I stopped it with `wsb stop`.

## Part E: Seal catalog Back and footer (D65), and the other sub-gumps

**Change:** each smith sub-gump takes an optional `Action<PlayerMobile> back` from its opener, draws Back only when it
has one, and passes it through its own refreshes.
- Seal catalog (`C\SmithSealCatalogGump.cs`): `BtnBack = 99` (`:119`, outside the category range 1..N and the buy range
  100-199), drawn bottom left (`:197`), handled first in `OnResponse` (`:222`), carried through the category switch and
  all four buy refreshes. **Footer:** the note is now wrapped HTML in the right panel just under the rows (`:190`,
  `NoteY` `:205`), 36 high, so it no longer runs under Close and OK; on the longest category it still ends above the
  footer line (a fact checks it).
- Openers: the guildmaster gump passes `Reopen` (`C\SmithGuildmasterGump.cs:300`, same guild, account and NPC, so
  Commissions still reach the guildmaster) to all its sub-gumps (`:266-294`); the guild book passes a reopen of the
  page it was on (`C\SmithGuildBook.cs:517-523`).

**The other sub-gumps of those two menus, checked:**

| Menu button | Gump | Before | Now |
|---|---|---|---|
| Guildmaster 1 Bulk Orders | `SmithBulkOrderChoiceGump` | Close only | Back (`BtnBack = 4`), kept through the teaching toggle |
| Guildmaster 2 Guild Contracts | `GuildContractLedgerGump` | **Back drawn, did nothing for smiths** (`SendBackGump` knew only "mining") | Back reopens the Society of Smiths menu (`:394`) |
| Guildmaster 3 Seals info | `SmithSealsInfoGump` | nothing | Back (`BtnBack = 1`) |
| Guildmaster 4 Hammer upgrades | `HammerRestoreGump` | had Back (reopened the guildmaster gump without the NPC) | uses the opener's Back when given, so the NPC is kept; old behaviour otherwise |
| Guildmaster 5 Commissions | `SmithCommissionGump` | nothing | Back (`BtnBack = 99`), kept through request, turn-in, abandon |
| Guildmaster 6 / book 4 Seal catalog | `SmithSealCatalogGump` | Close only | Back, as above |
| Guildmaster 20 Mule exchange | `CrossGuildExchangeGump` | nothing | Back (`BtnBack = 1`); also given by the four other guild menus that open it (Miners, Foresters, Outriders, Artificers), each back to its member dashboard |

The guild book's other buttons are pages of the book itself (its own navigation).

**Found, not fixed (not smith menus):** the ledger's Back is still a no-op for **rangers and foresters**, and its
`GuildDisplayName` names the healers "Healers' Circle" (the guild definition says "Healers' Covenant") and has no
foresters entry, so their ledger header shows the raw key "foresters".

**Facts** (`T\Misc\SmithBackButtonsVerification.cs`): catalog from the guildmaster keeps Back through a category
switch and a buy and Back reopens the guildmaster gump; from the guild book's page 1, Back reopens the book on page 1;
each of the six guildmaster sub-gumps draws Back and Back reopens the guildmaster gump; the ledger's Back does; the
coming-soon note is HTML that ends above the footer line, on the longest category too, with no button in its rows.

## Part F: Staff Hub readability and two Travel requests (D67)

1. **Opaque, chosen: solid black tile 2624 with no alpha region** (`C\StaffHub\StaffHubGump.cs:150`, over the same
   (16,74) 528 x 324). 2624 is the dark tile pinned's own gumps lay under text (for example `AdminGump.cs:1347`),
   normally with an alpha region on top; without one it is solid, so nothing shows through. The 9270 stone frame is
   unchanged.
2. **Spacing:** `ClusterFStaffHub.CommandMeta` (`ClusterFStaffHub.cs:647`): "Re-run: Skips. Shard: Any." (was
   "Re-run: Skips . Shard: Any").
3. **Long values:** the nine rows are one wrapped HTML block (`StaffHubGump.cs:325`, `PlayerRowsHtml` `:654`), x 26,
   y 136, 300 x 234, label grey and value white, so a long value takes a second line. If the estimate (7 px a character)
   ever outgrows the block it gets a scrollbar instead of cropping. The Levels and Loops placeholder became one grey line
   at y 374 (`:329`) to give the rows the room. The skill cap row still shows the old 300 cap (17400 = 58 x 300, D64):
   that is P53's.
4. **Change facet** (`ClusterFStaffHub.ChangeFacet` `:508`, the row at `StaffHubGump.cs:432`, buttons 4500-4505):
   Felucca, Trammel, Ilshenar, Malas, Tokuno, TerMur, two rows of three under the shard places; the current facet is
   gold with no button. Same x and y; **z = the target's `GetAverageZ(x, y)`, which is what pinned's `[Go x y` does when
   no z is given (`P\UOContent\Commands\Handlers.cs:537`)**. Outside the target's bounds (0..Width-1, 0..Height-1) it
   refuses in one red line and nothing moves (for example "3000, 3000 is outside Ilshenar (0 to 2303, 0 to 1599).").
   The move goes in Recent as "Felucca 1500, 1610". The old note "Read from the seeders' own coordinates." gave its
   line up to this row.
5. **Green Acres: Felucca 5445, 1153, 0.** Sources: pinned's go-locations list
   (`D:\UO\ModernUO-pinned\Distribution\Data\Locations\felucca.json:221`, and `trammel.json:189` with the same point),
   the region's GoLocation (`Distribution\Data\regions.json:780-787`, GreenAcresRegion, Map Felucca), and staff
   character creation, which starts staff there on Felucca (`P\UOContent\Engines\Character
   Creation\CharacterCreation.cs:309-315`). ServUO agrees (`Data\Locations\felucca.xml:159`). Felucca, as the region and
   character creation use. Added to `ShardPlaces` (`ClusterFStaffHub.cs:483`).

**Facts** (`T\Misc\StaffHubReadabilityVerification.cs`): no alpha region and the 2624 panel on every tab; every
command row's meta matches `^Re-run: \w+\. Shard: \w+\.$` and no label has " ."; for a fixture in three guilds with
five unlocks, every row value appears whole in the block, none in a cropped label, the two values Chase saw cut off are
wider than the old 176 px, the scrollbar is on exactly when the estimate overflows, and the block clears the
placeholder and the Actions column; change facet keeps x and y with [Go's z, refuses off Ilshenar with no move, has no
button for the current facet, reaches all five others; Green Acres is a place and Go lands there.

## Part G: "Society of Smiths" everywhere (D68)

Every player-visible change (display text only; the key stays `smithing`, and no saved data holds the name):

| Where | Was | Now |
|---|---|---|
| `C\ClusterFGuildSystem.cs:106` guild definition `Name` | Smiths' Fellowship | Society of Smiths |
| ...which every `def.Name` shows: the guild directory row (`:901`), the hall page title (`:1034`), the join and rank messages (`:404-428`: "You have joined the ...", "Welcome back to the ...", "You are now X of the ...", "Awarded ... with the ..."), the Staff Hub's guild standing row and guild hall names | Smiths' Fellowship | Society of Smiths |
| `C\ClusterFGuildStarterPath.cs:124` the starter path's own rule for It's Hammer Time | The Smiths' Fellowship recharges it. | The Society of Smiths recharges it. |
| `C\ArtificerWorkOrderSystem.cs:741` artificer order label | (requires Smiths' Fellowship) | (requires Society of Smiths) |
| `C\GuildContractLedgerGump.cs` `GuildDisplayName` (the smith contract ledger's header) | Smiths' Brotherhood | Society of Smiths |
| `C\ArtificerWorkOrderSystem.cs:110` (a comment) | Smiths' Fellowship | Society of Smiths |

Already right, unchanged: the Seal catalog header, the BOD turn-in message, the guildmaster gump header, the guild
book's "This book is for members of the Society of Smiths.", the hammer tooltips. Searched with `grep -i
"fellowship\|smiths'"` over `server\customizations`, `server\patches`, `server\tests`, `server\migrations`, `docker`:
no other hit. **Not changed (outside my paths):** `docker\uo\SERVER.md:1586` (its guild table says Smiths' Fellowship)
and `design\systems\guild_framework.md`, `design\systems\league_of_extraordinary_citizens.md`. **A separate naming
question, not changed:** the artificer order text says "Smiths' Scrip" and "Smiths' Standing"
(`ArtificerWorkOrderSystem.cs:764`, `:1012`) where everything else calls the currency Smithing Seals.

**Facts** (`T\Misc\SmithGuildNameVerification.cs`): the definition's name and key; the directory (exact row text) and
the smith hall page say Society of Smiths and nothing there says Fellowship; the catalog, ledger header and starter
rule say it; and a scan of every `.cs` installed from `server\customizations` (`/customizations` in the builder, as
`CommandDeclarationVerification` reads it) finds no "Fellowship" and no "Smiths' Brotherhood".

## Part H: Shard-Console VPN warning (D47)

**What it shows:** a fourth tile, **PUBLIC DNS**, beside LIVE, TEST and STATUS PUBLISHER
(`scripts\Shard-Console.ps1:2416`). Red "VPN ON" with "VPN on: public DNS points at <ip>. Turn the VPN off." (and which
interface carries the traffic); red "WRONG IP" with "VPN on: public DNS points at <ip>, not this house (<ip>). Turn
the VPN off; ddns puts it back within 10 minutes."; green "OK" with "shatteredlegacyuo.com = <ip>, this house. No
VPN."; grey "UNKNOWN" with the reason when a check failed; grey "CHECKING" before the first answer.

**Signals, and why** (judged by `Get-DnsGlance` `:1229`, gathered by `Get-NetworkProbe` `:2076`):
- **Route (decides "VPN on"):** the interface Windows would use for 1.1.1.1 (`Find-NetRoute`). If its source address is
  not the house LAN address 192.168.1.58, a VPN carries this PC's traffic. VPN clients either replace the default route
  or add 0/1 and 128/1; this question is answered through either. Checked here today: Ethernet, 192.168.1.58.
- **Adapters:** up adapters of PPP or tunnel type, or with a VPN client's name (WireGuard, Wintun, TAP, OpenVPN,
  NordLynx, Proton, Mullvad, AnyConnect, Fortinet, GlobalProtect, ...: `Test-VpnAdapter` `:1204`). Shown in the text,
  **not decisive alone**: a split-tunnel VPN can be up while traffic still leaves through the LAN, and then DNS decides.
- **Public DNS over HTTPS:** Cloudflare's JSON API, then Google's, for the A record. Not `Resolve-DnsName`, because the
  UniFi router answers port-53 queries for the name with 192.168.1.58 inside the house.
- **This house's address:** Cloudflare's `cdn-cgi/trace` as seen from this PC, compared with DNS **only when no VPN
  route is seen** (with a VPN on it is the VPN's exit and says nothing about the house). The router's WAN address needs
  UniFi credentials the console does not have, and no fetch from this PC can be shown to bypass a full-tunnel VPN, so
  the house address is known only while the VPN is off. That is why the route is the deciding signal and both facts
  are shown.
- Today, live: route Ethernet 192.168.1.58, no VPN adapter, DNS 216.247.206.76, public 216.247.206.76: green OK (1.1 s).

**Never blocks the console:** the probe runs in a runspace of its own (`Start-NetworkProbe` `:2124`, the functions
handed over as text). A 1 s `Windows.Forms.Timer` (`:2667`) only collects a finished probe (`IsCompleted`, never a
wait) and starts the next one 30 s after the last answer (`Update-NetworkTile` `:2136`); a probe still running after
30 s is abandoned as UNKNOWN. Each HTTPS GET has a 4 s timeout; the probe never throws (each failure is recorded beside
its signal), and **a failed check is grey, never red**. As said in headline 6, the console's other checks run on the UI
thread; this one does not.

**Facts** (`scripts\tests\Shard-Console.Tests.ps1`, `P52_*`, with the route, adapters and both HTTPS answers handed
in, using D47's real addresses): VPN on (red, the brief's sentence, names ProtonVPN); VPN off at the house (green,
Hyper-V and loopback are not VPNs); DNS not the house with no VPN seen (red); a failed check (DNS, public IP, both,
route, no A record, and everything at once) is grey UNKNOWN and both DNS services were tried; a split-tunnel VPN is
judged by DNS; adapter shapes; the parsers on real shapes (and SERVFAIL is a failure); the form's fourth tile is built
without the network and draws VPN ON in red. `TheFormBuildsFromACaptureWithoutBeingShown` now also checks the tile
exists, with the probe switched off for the test.

## Facts, red then green

| Fact | Red in | Green |
|---|---|---|
| A held only, no stacking (T1, T2) | red-a, red-b | final |
| A held after a load (T1, T2) | red-a | final |
| A in the pack after a load: none (T1, T2) | red-b | final |
| A restore in the pack: none (T1, T2) | red-a, red-b | final |
| A restore while held: one (T1, T2) | red-c | final |
| A regen while held: one (T1, T2) | red-a | final |
| A regen in the pack: none (T1, T2) | red-b | final |
| A T2 familiarity mod held only and after a load | red-a, red-b | final |
| B menu entry for the owner, gump sent (T1, T2) | red-a | final |
| E catalog Back through switch and buy, to the guildmaster | red-a | final |
| E catalog Back to the guild book's page | red-a | final |
| E Back on Bulk order, Seals info, Commissions, Catalog, Mule exchange (5 cases) | red-a | final |
| E Back on Hammer upgrades | **never red: that Back existed before P52** | final |
| E ledger Back for smiths | red-a | final |
| E coming-soon note clears the footer | red-a | final |
| F solid panel on every tab | red-a | final |
| F command meta spacing | red-a | final |
| F player values whole and wrapped | red-a | final |
| F change facet | red-a | final |
| F Green Acres | red-a | final |
| G name everywhere; G no source names the old guild | red-a | final |
| C seven facts | HEAD scripts (all 7); behaviour red: "own driver" and "writes over 0 only" | 20/20 |
| H eight facts | HEAD script (all 8 and the updated form fact); behaviour red: "failed check grey" and "split tunnel" | 94/95 (headline 7) |
| D kit start | dry run of HEAD's script with no editor: the sandbox's exact line | dry run and a real sandbox |

## Build table

| Build | What | Result |
|---|---|---|
| 1 | A and B, tests-only | builder failed: missing `using Server.Gumps;` in the new fact |
| 2 | A, B, E, tests-only | 664/664 (637 + 27) |
| 3 | + F and G, tests-only | 671/671 |
| red-a | everything undone | 643/671, 28 fail: 27 new + `WispOrbPossession...(Silenii, Phantom)` (flaky, headline 7) |
| red-b | hammer rule only | 662/671, 9 fail (all hammer) |
| red-c | restore without re-apply | 669/671, 2 fail (restore while held, T1 and T2) |
| final | `build.sh -t sl-modernuo:cc-p52` | 42/42 patches, 671/671, image `88b7983f2d29` |

Builder tags made: `sl-uo-builder:cc-p52`, `sl-uo-builder:cc-p52-red-a`, `-red-b`, `-red-c` (no runtime images for the
reds). Docker answered throughout; no hang, no truncated layer.

## For Chase

Deploy the test shard first:

1. `docker tag sl-modernuo:cc-p52 sl-modernuo:latest`
2. `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -Down`
3. `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild`

In game on the test shard:

4. **Hammer (D59):** with the Hammer of Hephaestus in your pack, look at Blacksmithy: no +5. Equip it: +5. Unequip: back
   down. Equip it and restart the test shard (steps 2 and 3), log in: +5 is there without re-equipping. Same with the
   Reinforced hammer (+10, more with familiarity).
5. **Hammer menu (D60):** single-click the hammer (in hand or in the pack): the menu has **Knowledge**; pick it anywhere
   (also at a forge): the Metal Familiarity panel opens. If you want a different word, say which: Information, Info,
   Overview, Progress and Status also exist.
6. **Seal catalog (D65):** from the Society of Smiths guildmaster, open the Seal Catalog, switch to Post-Valorite: the
   "Not yet available" note sits under the rows, not under Close. Buy something, then press **Back**: the guildmaster
   menu. From the Smithing Guild Book's Commissions page, open the catalog and Back: the book, same page. Also press
   Back on Bulk Orders, Seals info, Commissions, Hammer upgrades, Guild Contracts and the Mule Exchange.
7. **Staff Hub (D67):** `[SL`: the content area is solid black. Commands rows read "Re-run: Skips. Shard: Any.".
   Player tab: select a character in several guilds: Guild standing and Skill / stat caps wrap to a second line, nothing
   ends in "...". Travel: **Green Acres** is in Shard places (Felucca 5445, 1153); "Same x, y on another facet": stand
   in Britain on Trammel and press Felucca (same spot), then Ilshenar from x above 2303 (one red line, no move).
8. **Guild name (D68):** `[guild` directory and the smith hall page say **Society of Smiths**; join a fresh character:
   "You have joined the Society of Smiths".

Package and console:

9. **Launcher (D61), on this PC:** build and publish as usual when ready. Starting the game, the launcher window now
   stays up to 20 seconds. Nothing else changes on a PC with a working OpenGL driver: check your settings file keeps no
   new `force_driver` value: `Select-String -Path D:\UO\TazUO\client\settings*.json -Pattern force_driver`.
10. **Launcher, the real no-OpenGL case** (the next full P35 run): `D:\ShatteredLegacy\player-package\clean-test\Start-CleanTest.ps1 -Mode Build`,
    install as the README says, then Play. Expected: TazUO's crash page may flash once, the launcher says "This
    computer has no OpenGL 2.1 driver. Starting the game again with its automatic graphics driver.", and the game
    starts. Unverified until then: that the crashed TazUO process exits within 20 s in the sandbox.
11. **Shard-Console (D47):** `D:\ShatteredLegacy\scripts\Shard-Console.ps1`: a fourth tile **PUBLIC DNS: OK** (green,
    216.247.206.76). Turn the VPN on and wait up to 30 s: **PUBLIC DNS: VPN ON** in red with "VPN on: public DNS points
    at ...". Turn it off: OK again (or WRONG IP until ddns catches up). Tell me the VPN client's adapter name if the
    tile names the interface but lists no VPN adapter, so the pattern can include it.
12. Facts, any time: `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1`
    (expect 94 of 95: the one failure predates P52) and
    `powershell -NoProfile -ExecutionPolicy Bypass -File D:\ShatteredLegacy\player-package\tests\Launch-Settings.Tests.ps1`
    (20 of 20; its end-to-end facts need the test shard up).
