# Overseer pass-down, 2026-10-03 (11:35)

Supersedes `passdown-overseer-2026-10-02.md` for queue state and numbers (its "Lessons" still hold; read them).
The "how this chat works" section of `passdown-overseer-2026-10-01.md` still holds.

## Role, in one paragraph

Track the CC prompt queue (one builder at a time in `D:\ShatteredLegacy`; notes-only prompts run alongside), read CC
results from `D:\UO\shard-migration\notes\` when Chase says a prompt is done, write or number prompts in
`D:\UO\cc-prompts\`, record Chase's decisions in notes, keep `docs\bug-list.md` and `docs\fidelity-principle.md`
current, give Chase short in-game checklists. Never commit (Chase runs `D:\UO\Commit-ShardWork.ps1`). Git only with
`--no-optional-locks`. ASCII only, no em dashes, American spelling. Verify in code before asserting; cite file:line.
Engine authority: `D:\UO\ModernUO-pinned` at upstream `d4531cd94`. **Ignore anything "live" until the fresh-world
wipe (Chase 2026-10-03); only the TEST shard is in use.** Other chats (features, companions, dungeon) write prompts
too: they often leave them unnumbered (`cc-P-*.md`); number them, rename, fill the number into the file's title,
notes path and build tag, and move the draft to `cc-prompts\_renders\`.

## Numbers (re-derive before trusting)

- Bugs: **next free D69** (D68 Society of Smiths; D67 Staff Hub readability; D66 commit script false clean; D65 catalog back button; D64 metals to 200 cap; D59 HoH +5, D60 familiarity reach, D61 force_driver, D62 material name case, D63 category overflow). D50-D58 logged 2026-10-02/03; D51-D54 fixed in P42 and passed in game; D55-D58 fixed in
  P46 (in-game check pending).
- Deviations: **next free D-113** (D-107 to D-112 from P42). P46 adds text to update (D-109 teaching toggle, Seal
  numbers, Self Repair floor): read P46's notes and register.
- Features: **features chat owns `docs\feature-queue.md`**; next free there was F-33 (check the file).
- Prompts: **next free P51.** Re-check `cc-prompts\` and `completed\` right before saving.

## State of the shards

- TEST: new engine `d4531cd94` since the P43 cutover (2026-10-02 18:18). Running image `a4525e03b317` (P42).
  P46's image `sl-modernuo:cc-p46` (`8d7505c739f6`) is built and committed (`1f2b899`) but **not yet on the test
  shard**: deploy with `docker tag sl-modernuo:cc-p46 sl-modernuo:latest` then
  `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild` (stop first with `-Down`; call by full path).
- Stops now wait 60 s (D50, P43). The console "Rebuild" can still hit D56-type flakes; P46 fixed the known one.

## Queue (2026-10-03 11:35)

| Prompt | Kind | State |
|---|---|---|
| P44 one-step install (wait for EA patch) | builder, player package | **done 13:12**, uncommitted; notes read; prompt moved to `completed\` |
| P45 companion probes | builder (worktree) | after P44 |
| P48 League batch 1 (ladder, signposts) | builder | after P46 (done); account data bumps from whatever version P46 left |
| P50 chest mimic monster | Part A notes; Part B builder | Part B after P44 (player package). Art placed 2026-10-03 at `D:\UO\third-party\animated-mimic\` with `SOURCE.txt` |
| P35 clean-machine test | builder | **next builder** (P44 says so: it is the real-EA proof). B4 step 2 now asks P44's open questions |
| P36 dungeon build 1 | builder | after P44; map edits are patches per the client policy. Step 5 updated for P44 (older client now waits) |
| P34 winter decor | builder | never beside P48 (both touch the registrar office seeder) |
| P47 League research | notes | done (`notes\cc-P47-league-research.md`) |
| P49 dungeon chests and mimic research | notes | may run any time |

## Owed to Chase

1. **P46 in-game checklist** (end of `notes\cc-P46-smith-orders-2.md`) once its image is on the test shard:
   Celestial deed refuses iron; teaching toggle (choice gump and guild book, relog keeps it); Self Repair floor;
   commission rewards x3; runic prices; Hephaestus familiarity on default iron; Wisp Orb pet fight (no master swing,
   no karma loss on death); hammer regen 10/5 min with a "next use" timer.
2. Register P46 deviations; mark D55-D58 passed after the checklist.
3. Old items still open: F-12 numbers (reserve cap, step size above 100, League metal ranks may now be settled by
   P47/P48), P33 test list, P23/P27 old client checks.

## Results files from today

`notes\p39-step7-checks-2026-10-03.md` (new-engine cutover checks), `notes\p42-checks-2026-10-03.md` (P42 checks),
`notes\bod-choice-decision-2026-10-03.md` (all Smith BOD decisions).

## Lessons added 2026-10-03

- Before telling Chase what a CC result needs, read the CC notes' "For Chase" and checklist sections; CC chips
  ("suggested task") can duplicate a queued prompt: tell Chase to close them.
- `Start-TestShard.ps1 -Down` leaves PowerShell in the repo root, so call the script by full path afterwards.
- A fact that passes in CC's build can fail in the console's rebuild (order-dependent statics): deploy CC's tested
  image with `docker tag` + `-SkipBuild` instead of rebuilding.

## Update 13:12 (P44 done)

- P44 notes: `notes\cc-P44-wait-for-ea-patch.md`. All probes green, 4 watched red first. Changed
  `Setup.ps1`, `README.txt`, `Build-PlayerPackage.ps1` (new gate 4 check). Nothing proven against EA's real
  patcher (UAC, UIPI close, window behavior): P35 is the proof. Do not publish until P35 passes.
- Overseer edits: P35 B4 step 2 asks UAC count, window close, installer auto-start, copy EA's log; "2.5 GB" fixed.
  P36 step 5 points at P44 probe 6. P44 prompt moved to `completed\`.
- Scratch `D:\UO\cc-p44-work\` (about 1.5 GB) safe to delete.

## Update 19:15 (P35 done, commit blocked)

- P35 finished (`notes\cc-P35-clean-machine-test.md`). Commit refused `player-package/vendor/vc-runtime/vcruntime140.dll`
  (`Commit-ShardWork.ps1` blocks `.dll`; both repos public). Overseer fix: `.gitignore` ignores
  `player-package/vendor/vc-runtime/*.dll` (kept on the build PC; SOURCE.txt tracked; build checks hash and signature),
  and `Commit-ShardWork.ps1` now uses `status --porcelain --untracked-files=all`, because it expanded new folders with
  Get-ChildItem and swept in ignored files. Backup: `D:\UO\Commit-ShardWork.ps1.bak-2026-10-03`.
- Lesson: a CC prompt that vendors a binary must say "gitignored, build-PC only" up front.

## Update 2026-10-04 07:15 (P35 sandbox run)

- Sandbox (vGPU off): extract, permission prompt, EA installer (plus DirectX), EA's patcher started on its own,
  our progress bar, patch finished: **install path passed.** TazUO then crashed: OpenGL 2.1 required (GDI Generic 1.1),
  logged D61. `FNA3D_FORCE_DRIVER` is ignored (TazUO sets it from its own `force_driver` setting: 1 OpenGL,
  2 Vulkan, 3 auto). `-force_driver 3` test offered to Chase.
- Chase decision: graphics in the sandbox is not a player blocker; **publish 1919 and test on a fresh real PC.**

## Update 2026-10-04 07:20: P35 / T-049 passed

- `D:\UO\clean-test-results\20261003-192012\results\evidence-5.txt` (07:20:07): TazUO running from the package,
  window "Test - [TazUO ...]", `zlib.DLL` and `VCRUNTIME140.dll` both from `app\tazuo\`, D3D11 through WARP
  (`d3d10warp.dll`), 0 Zone.Identifier left, no new app errors after 07:15. EA patch 19:24:38 to 19:33:50 (1.77 GB),
  headless patcher started by EA's installer. Chase logged in to TEST with a test account.
- Only with `-force_driver 3` (D61). The sandbox reached TEST via a hosts entry `192.168.1.58` because public DNS was on
  a VPN exit `159.26.100.68` (D47 again, Chase's VPN). Test shard 2594 is LAN only by design.
- Next: P51 = D59, D60, D61, sandbox LogonCommand error (`inside-start-error.txt`); D47 if Chase says yes. Publish 1919
  only after VPN off and DNS back on the home IP.
- 07:22: VPN off, public DNS back on 216.247.206.76 (dns.google). **1919 published** (`publish-output.txt`: OK,
  sha256 ab152c66...). Fresh-PC test must be on the home LAN with `Play TEST Shard.bat` (2594 is LAN only; live is down).
- D47: Chase wants a Shard-Console VPN warning, not a ddns redesign. Goes in P51.
- 07:45 Chase decisions: (a) metals rescale to the 200 cap for now (D64, even 12.5 steps proposed); (b) post-Valorite
  Seal multipliers (x1.5..x5) stay as they are; (c) **items and temporary effects may raise skills and stats above
  the cap.** Stats already do (StatCap limits raw stats only). Skills do not: pinned `Skills.cs:317-325` clamps
  ObeyCap mods at Cap, and item skill bonuses set `ObeyCap = true` (`Misc/AOS.cs:1357-1358`), as OSI does. So (c) is a
  deviation to register (next D-113) and a P51/P52 item: item bonuses and our mods (hammers, spells, potions,
  talismans) ObeyCap=false; audit every SkillMod source.

## Update 2026-10-04 17:08

- **P48 done** (notes 13:36): 41/41 patches, 606/606 facts, image `sl-modernuo:cc-p48` (`beb5677d7a5d`, build 3).
  Build 4 hung when Docker stopped answering; Chase re-runs `build.sh -t sl-modernuo:cc-p48` before committing.
  ClusterFAccountData v15 -> v16. Open for Chase: chapters 4/5 at Blaze/Mythril (built, by name) or Toxic/Obsidian.
  Untracked `design\tutorial-farm\` appeared mid-P48 (another chat), not P48's.
- **P51 is taken** by the features chat: `cc-P51-staff-hub-and-raptor-pack.md` (F-30 Staff Hub, F-31 Raptor pack).
  The overseer's bug batch (D59-D65, D47 console VPN warning, sandbox LogonCommand, skill mods over cap) is **P52**.
- Queue: P49 (notes) may run now. Builder after P48 is committed: P51, then P52 (or P52 first if Chase wants fixes
  first). P50 Part B, P36, P34, P45 after.

## Update 2026-10-04 20:05

- P48 committed (`aa61227`, 18:54) after a clean rebuild (Docker's build cache held a truncated NuGet file from the
  hung build 4; fixed by removing all `sl-uo-builder:*` images and `docker builder prune -af`). Lesson: a Docker hang
  mid-build can poison cached layers; prune alone will not drop layers an image still references.
- **P51 done** (00:51 UTC): 42/42 patches, 637/637 facts, image `sl-modernuo:cc-p51` (`aead9f7f5e2e`). Uncommitted.
  Checklist in its notes "For Chase" (Staff Hub `[SL`, Raptor pack).
- **P49 done** (notes only). Section 9 has 17 decisions for Chase (F-32); belongs with the features chat.
- Next builder: **P52** (overseer bug batch), to be written.
- 20:15 Chase, Staff Hub (P51) results: Travel worked; Player tab works offline; Grant-to-other-player check deferred.
  **Requests for P52 (Staff Hub Travel tab):** (1) a "change facet" control: same x/y/z on another facet
  (Felucca/Trammel/Ilshenar/Malas/Tokuno/TerMur), refusing cleanly where the spot is invalid; (2) **Green Acres** as a
  shard place (staff area; CC to verify coordinates and facet in pinned data, do not guess).
- 20:21 P51 Raptor pack **passed in game** (Chase): attack calls 2 friends, friends not tamable (no Tame entry),
  friends vanish after the leader dies. Staff Hub: tabs, Dry run, Player offline, Travel passed; Grant-to-other-player
  deferred; readability = D67.
- 20:27 P48 League **passed in game** (Chase): office already placed (status 0 of 3), League row first in [guild,
  [LeagueLadder table matches, Elara speaks and names the player, promotion to Dull Copper Citizen, bank 1,100.
  Ranks match the metals (Chase misread a question). **Chase 20:28: keep chapters 4/5 at Blaze and Mythril.**
  D68 Society of Smiths decided.
- 20:31 P46: hammer familiarity on default iron likely passed (admin account; recheck on a player). Valorite small exc
  BOD x20 paid 96 Seals / 360 standing (in range). **Commission check dropped: Chase may rework the commissions table
  in another chat.** Left: D58 Despise fight, P51 grant to another player.
- 20:35 **P52 written** (`cc-prompts\cc-P52-bug-batch-4.md`): Parts A D59 hammer bonus held-only, B D60 familiarity
  context entry, C D61 force_driver, D sandbox start script, E D65 catalog Back/footer, F D67 hub readability +
  change facet + Green Acres, G D68 Society of Smiths, H D47 console VPN warning. Handed for overnight.
  **P53 still to write**: D62 material names Title Case, D63 craft category overflow, D64 metals to the 200 cap
  (and the 300 skill cap setting), skill bonuses above the cap (deviation D-113).
- 20:37 Chase wants to look at a remote-control setup for Claude Code tomorrow (so the overseer can hand prompts to CC directly).

## Update 2026-10-05 05:30

- **P52 done**: 42/42 patches, 671/671 facts, image `sl-modernuo:cc-p52` (`88b7983f2d29`), package gates 1-6 green,
  Launch-Settings 20/20, Shard-Console 94/95 (pre-existing red-list fact, now P53 Part F). D61 chose: keep OpenGL,
  fall back to force_driver 3 only after the OpenGL 2.1 crash. D60 cliloc 1112530 "Knowledge". Green Acres Felucca
  5445,1153. P35 kit cause: Sandbox has no notepad.exe. Uncommitted. Checklist in its "For Chase".
- **P53 written** (`cc-prompts\cc-P53-two-hundred-cap.md`): A skill cap 200, B metal tiers + all 300-era numbers,
  C bonuses above cap (deviation), D Title Case materials, E category overflow, F Shard-Console red-list fact.
- 05:40 P52 in-game: D59 hammer +/-5 **passed**; D60 "Knowledge" entry **passed**; D65 catalog footer + Back
  **passed** (screenshot); D67 hub solid and "Skips. Shard: Any." **passed** (screenshot); D68 Society of Smiths
  **passed**; D47 console VPN tile **passed**. Chase: familiarity rises too fast. Code: +1 per successful craft
  (`HammerOfHephaestus.cs:280-282`, `:661-663`), FamCap 100 (T1, `:116`) / 250 per metal (T2, `:495`). Asked Chase
  for the target.
- 05:42 Chase: familiarity = all three (caps x10, chance to gain, exceptional counts more): logged D69, for P54. P53 with CC.
- 05:55 PT-12/PT-13 (bugs chat) registered as D70 satchel smelt ratio, D71 T3-T5 lose Smelt Metal; both for P54 with D69. Decision pending: guaranteed smelt vs forge skill check.
- 05:59 Chase D70: satchel smelts exactly like the forge (ratio + skill check), forge still required.
- 06:01 D72 satchel hues along ore ladder (proposal pending OK; T2 0x8A5C flag-bit suspect), D73 achievements get a plain (Earned: ...) parenthetical. Both P54.
