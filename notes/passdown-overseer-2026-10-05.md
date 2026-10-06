# Overseer pass-down, 2026-10-05 (08:20)

Supersedes `passdown-overseer-2026-10-03.md` for queue state and numbers. That file's long running log (2026-10-03 to
10-05 08:18) is the detail; its "Lessons" and the 10-03 role paragraph still hold. Read `passdown-overseer-2026-10-01.md`
"how this chat works" too.

## Role, in one paragraph

Track the CC prompt queue (one builder at a time in `D:\ShatteredLegacy`; notes-only prompts run alongside), read CC
results from `D:\UO\shard-migration\notes\` when Chase says a prompt is done, write or number prompts in
`D:\UO\cc-prompts\`, record Chase's decisions, keep `docs\bug-list.md` and `docs\fidelity-principle.md` current, give
Chase short in-game checklists. Never commit (Chase runs `D:\UO\Commit-ShardWork.ps1`). Git only with
`--no-optional-locks`. ASCII only, no em dashes, American spelling. Verify in code before asserting; cite file:line.
Engine authority: `D:\UO\ModernUO-pinned` at `d4531cd94`. Only the TEST shard is in use until the fresh-world wipe.
Other chats (features, companions, dungeon, bugs) write prompts too and leave them unnumbered (`cc-P-*.md`): number them,
fix title/notes path/build tag, move the draft to `cc-prompts\_renders\`.

## Rules added 2026-10-04/05 (Chase)

- **Every prompt ends with a "Finishing" section**: CC's notes end with a last line `Pnn DONE` (or `Pnn STOPPED: reason`)
  and its chat ends with **Pnn DONE**. Chase commits only after that.
- **Every prompt from P57 on has a "Patch notes" section**: CC adds player-facing lines to `CHANGELOG.md` and bumps
  `VERSION` (F-15 rules in the file's header). Wiki publish waits for the fresh-world launch.
- Build from Git Bash: `& "C:\Program Files\Git\bin\bash.exe" docker/uo/build.sh -t sl-modernuo:cc-pNN` (plain `bash` is
  WSL with no distro). If Docker hangs mid-build, CC stops; a poisoned cache needs `docker images sl-uo-builder ...|rmi`
  then `docker builder prune -af`.
- Chase's remote PowerShell runs as SYSTEM: git refuses (dubious ownership) and there is no push credential. Commit only
  from his own login. `Commit-ShardWork.ps1` now reports FAILED on a git error (D66 fixed by overseer; backups `.bak-*`).
- The 200 skill cap stands for the foreseeable future; only items go above 200 (D-113).

## Numbers (re-derive before trusting)

- Bugs: next free **D87**. Deviations: next free **D-121**. Prompts: next free **P61**. Features: see feature-queue.md
  (features chat owns it; next free F-36 at last read).

## Queue (2026-10-05 08:20)

| Prompt | Kind | State |
|---|---|---|
| P56 smith economy and labels | builder | done, committed `b8e525d` 08:15; **tested in game 08:41, all passed** |
| P58 changelog catch-up 10.02-10.05 | CHANGELOG/VERSION only | **DONE 08:46**, uncommitted (shares the tree with running P57; commit both together after P57 DONE). Was: runs beside P57 (Chase started P57 first, 08:29); P57 may or may not have read its Patch notes section (appended ~08:20) |
| P57 batch 6 | builder | **running since ~08:20**: A catalog prices x3 decoupled, B post-Valorite item part half-step, C harvest tiers like OSI, D own cliloc pipeline (Breed, Smelt Ore, Metal Familiarity), E D81 guildmaster Small/Large + layout, F D80 achievements gump, G D82 Stealing stack exploit |
| P34 winter decor, P36 dungeon build 1, P45 companion probes, P50 chest mimic monster | builders | queued, after P57 |
| P59 evo pet body sheet | notes | numbered 08:35 from the features chat draft (F-35); ready, may run beside P57 |
| P54 F-12 research | notes | done; its "Decisions for Chase" belong to the features chat (F-12) |

## Tested in game 2026-10-04/05 (all passed)

P46 (except D58 Despise fight and commissions, dropped pending a commissions rework in another chat), P48 League, P51
Staff Hub (grant-to-other-player not yet) and Raptor pack, P52, P53 (not all items rechecked in game), P55 fully, P35
clean-machine (sandbox; graphics fallback proven), 1919 package published, T-021 updater passed.

## Open for Chase

- Unanswered: should greyed context entries say why (guild, tool)? Proposal in D80, not yet in a prompt.
- Remote control of CC from the overseer (Chase: look at it later).

## Log

- 08:35: numbered features-chat draft as P59 (added Patch notes = none, Finishing). Draft moved to `_renders\`. A 0-byte
  `cc-P-f12-xp-curve-and-gain-paths.md` stub sits in `cc-prompts\` (real draft already in `_renders\`, became P54); left in place.
- 08:39: P56 in game (Chase): bank passed (iron 10 exceptional ringmail legs: +303 Seals = 300 gloves +3 rung + 3 gold, +120 standing), Platinum smelt refused at 112.4 and works at 112.5, satchel passed. Left: non-member town smith, Ask mode, labels. Possible D83: Mining 112.5 to 114.0 (~15 gains) around one visible smelt success; asked Chase whether it was one smelt or several.
- 08:41: P56 rest passed (non-member town smith, Ask mode, labels). P56 fully tested. D83 smelt-gain question still open.
- 08:46: P58 DONE. Four sections 10.02-10.05, 77 player + 7 Staff lines, VERSION 2026.10.05. Staff lists not shown in game or wiki (ShardVersion.cs:111-121). Do not commit until P57 DONE. After P57: check its lines merged into the same 2026.10.05 section. P46 commission line stays unless the commissions rework lands first.
- 08:52: Smelt skill-gain jump is not a bug (test char, super fast gain enabled). No D83. Next free bug stays D83.
- 10:09: P57 tested (all passed; Platinum vein shelved, menu words wait for package). P60 DONE (console Commit tab, blocks on not-DONE). P59 DONE (not yet read). Commit-ShardWork.ps1 fixed per P60 s7 items 1-2 (archive only on DONE/STOPPED; exit 1 on add/commit/push failure), backup .bak-20261005-0956. Logged D83 (Blacksmithy no gain above 140, awaiting pick), D84 (earned achievement shows 9/1), D85 (post-Val deeds unnamed; Chase: own clilocs). D86 hammer +5 stuck in pack once, not reproduced (not yet in bug-list). P60 did not do P57 changelog lines or the 2 stale lines (40, 59): goes in P61.
- 16:15: Features chat (commissions): F-37 Client Commissions to the League, F-20 skill list decided, F-38 Mining/Lumber contract rework added (needs numbers pass). Infamy is new (not in code). Mule goes to its own chat. Next free F-39. Not committed.

## State at 16:25

- Done and committed: P56-P64 (P62 kitsune walk test, P63 console package/deploy, P64 patch history). P54 research done; Chase's 17 answers in notes\f12-decisions-2026-10-05.md.
- Running: P68 (console Check package, cancelled publish = exit 3, commit wait 60 s + countdown). Chase added a Force checkbox in the kickoff: Force skips only the recent-change wait, never the not-DONE check, SYSTEM refusal or typed phrase.
- Builder queue after P68: P65 evo pets framework, P66 clamps + hook G, P67 craft ceilings + P61 follow-ups (orders roll teaching metals; harder items teach better; band speed stock), then P34, P36, P45, P50. Next free P69.
- Overseer edits today: Commit-ShardWork.ps1 (archive only on DONE/STOPPED; exit 1 on git failure), Publish-PlayerPackage.ps1 (decline exits 3). Bug list D77-D82 closed (2b); D83-D85 built in P61 awaiting test; D86 hammer not reproduced; D87 bulletin wrap (P64). Fidelity D-121, D-122 + amendments. Next free bug D88, deviation D-123 (re-check after P62-P68).
- Kitsune: updated walk frames re-encoded into vendor sl-anim7 (committed 16:2x); package publish waits until the rest of the art is drawn (Chase).
- To features chat: commissions to the League (Renown, Infamy, orders for all skills, training bonus), Imbuing rework. Offered: XmlLevelItems port research (notes only), not yet accepted.
