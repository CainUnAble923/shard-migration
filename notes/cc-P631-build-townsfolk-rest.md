# P631: New Haven townsfolk and inn rest, stage 1

Written 2026-10-26 by the Iron Golem (Claude Code). Builds stage 1 (the design's prompt 1, "Townsfolk table, speech and topic menus") of [cc-P566-design-townsfolk-features.md](cc-P566-design-townsfolk-features.md). Chase's decision (10-25 evening) took the design's defaults: the first roster is Mara, Ellis and the existing innkeeper; rest costs 25 gold after 120 seconds without harm, with a 60-second reuse. Stage 1 is the talk only. The inn rest and the innkeeper's part are stage 2, placement is stage 3, as the design orders them.

## In plain words

- Players will not notice anything yet. Talk is switched off and nobody is placed in New Haven.
- On the test shard, staff can try it: `[ClusterFTownsfolk on`, then `[add ClusterFTownsfolk plaza` (Mara, the town steward) or `[add ClusterFTownsfolk trades` (Ellis, the workshop runner) inside New Haven. Within 3 tiles, saying hello, name, job, help, inn, rumors or goodbye gets a short answer that only you see. So does double-clicking them, or choosing Talk.
- A character still doing the tutorial's first lessons is pointed back to Rook. Everyone else gets directions to the bank, the inn and the League office.
- Nothing for you to do. The inn rest (25 gold, out of combat for 2 minutes) is the next stage, drafted at the end.

## Status

Done. The Iron Golem (Opus), branch `golem/Iron/P631` of both repos, not committed (the Golem commits). The gated build is green (section 3). No shard was started, no world command run, no package built, nothing deployed, no Haven contact.

## 1. What was built

| File | What it holds |
|---|---|
| `server/data/townsfolk-talk.json` (new) | The dialogue: schema 1, profiles `plaza` and `trades` (region `New Haven`) and `innkeeper` (region `the New Haven Inn`). Each has hello, name, job, help, inn, rumors and goodbye. Plaza has 3 rumors; trades and innkeeper have 2 each. `help` has a `core` line pointing to Rook and an `any` line. Names come from `{name}`. Written for us; nothing copied from the download. Two of the design's suggested lines are left out because they promise rest, which does not exist until stage 2 (the design forbids advertising unfinished features): the inn line "offers a paid rest" and the innkeeper's "Say rest". The help line says the League office is to the **south-west**, not south. Checked against the seeded anchors: Rook 3500,2572 at the plaza; the bank, Sarsmea Smythe at 3492,2577, beside it; the inn, Asandos at 3504,2519, north of it; the Registrar at 3459,2601, south-west of it. |
| `docker/uo/Dockerfile` | One `COPY` of that file to `/build/modernuo/Distribution/Data/ShatteredLegacy/townsfolk-talk.json` before publish. The tests read the shipped bytes there. The runtime stage already copies that whole Data folder to `/modernuo/Data`, so the server reads the same file at `/modernuo/Data/ShatteredLegacy/`. No separate runtime line is needed. |
| `Townsfolk/ClusterFTalkRules.cs` (new) | The strict loader. A whole table is checked before use. Refused: an unknown field anywhere, a wrong schema, a missing or unknown profile tag, a missing launch topic, duplicate profiles, topics or aliases, an alias that is reserved (rest, buy, sell, vendor buy/sell, train, teach, bank, guards, pet orders, join, resign, skip, tutorial) or contains the word "rest", an alias not written in its matched form, markup or control characters, a template other than `{name}`, a topic without an `any` response, fewer than 2 rumors, an unknown phase, and the parser's size limits (256 KiB, 8 profiles, 16 topics, 12 aliases, 8 responses, 80 and 240 characters). Loaded at startup (`Configure`) and on `[ClusterFTownsfolk reload`. A failed reload keeps the old table; a failed first load leaves talk off; nothing is made up. Matching is exact: case-folded, punctuation as spaces, whitespace collapsed, at most 160 characters. The words must equal an alias, optionally after the NPC's name. |
| `Townsfolk/ClusterFTownsfolkService.cs` (new) | Settings `clusterf.townsfolk.enabled` (false), `talkRange` (3), `talkCooldownSeconds` (3), `repeatCooldownSeconds` (15), refused outside range 1-3 or below 1 second. The test shard's `EnabledOverride` lasts until restart. Talk is on only with the switch, sound settings and a valid table. `CanTalk`: both alive and there, same facet, in range, seen, in line of sight, and the NPC inside its profile's region (or a child of it). `Select`: of the residents whose profile matches the words, the nearest, else the lowest serial (a name-first phrase matches only the NPC it names). Only it replies; the speech is marked handled, never blocked. Only regular or whisper speech from a living player counts. The reply is `PrivateOverheadMessage` to the speaker's own client, in the NPC's voice. Random lines avoid repeating the last one. Per-player cooldowns live in a `ConditionalWeakTable`, never saved and gone with the mobile. `PhaseOf` reads `ClusterFAccountPersistence.Get` only: Core for this character's own unfinished core, AfterCore once it is done, Any otherwise. `[ClusterFTownsfolk [status|reload|on|off]`: Administrator, `[ShardCommand(DevTool, TestOnly)]`. |
| `Townsfolk/ClusterFTownsfolk.cs` (new) | `ClusterFTownsfolk`: generated serialization v0, a saved tag (`plaza` or `trades`; any other value is treated as `plaza`). Fixed identity and outfit by tag. Stationary (`CantWalk`, `AI_Animal`, `FightMode.None`, as `TutorialRecruiter`), blessed and invulnerable, no loot, no teaching, no auto-stable, refuses drops. Speech, double-click and the stock Talk entry (6146, cliloc 3006146, as `GuildMembershipEntry`) go to the service; other speech goes on to the base creature unchanged. `[add` needs Administrator. `TownsfolkTalkGump`: one button per topic in `TutorialStyle`. Every press checks it came from the same player's client, then answers through the service, which rechecks everything and shares the cooldowns. A topic removed by a reload says nothing. Opening the menu says and grants nothing. |

Stage 1 places nobody. There is no seeder, no innkeeper partial, no rest and no cliloc change; those are stages 2 and 3. The `innkeeper` profile is in the table so stage 2's `InnKeeper` partial can use it. Until then nothing speaks it.

## 2. Tests: red first, then green

`server/tests/Townsfolk/TownsfolkTalkVerification.cs`, 8 facts:

| Fact | What it shows |
|---|---|
| `TheShippedTableLoadsFromTheBuildersDataFolder` | The shipped file is found (its path ends `Data/ShatteredLegacy/townsfolk-talk.json`) and loads: exactly innkeeper, plaza and trades, every launch topic, 2 or more rumors each, the two region names. Defaults: off, 3, 3, 15. Bad settings refused. |
| `TheParserRefusesABadTableOutright` | The shipped table parses clean. Each of 16 mutations of it is refused with its own message: an unknown "action" field, schema 2, trades removed, an unknown tag, inn topic removed, "hello" claimed twice, "rest", "take a rest", "vendor buy", "Your Job?", markup, a bell character, `{type}`, phase "night", no `any` response, one rumor. Also an oversized file and not-JSON. |
| `AFailedReloadKeepsTheTableInUse` | The good table loads. A reload of an empty-profiles file fails and the same table instance stays, with errors kept; a missing file does the same. With nothing loaded, a bad load leaves no table and talk is off even when switched on. |
| `MatchingIsExactWords` | "  Hello,   THERE! " normalises to "hello there". "What is your job?" and "MARA, hello" match. "forest", "rest", "i need a job today" and "vendor buy" do not. Speech over 160 characters is ignored. |
| `SpeechGetsOneReplyFromTheRightResidentOnlyToTheSpeaker` | Through `DoSpeech` (the engine's real dispatch): one reply, from Mara (1 tile) not Ellis (2 tiles), to the speaker's own test client and not to a bystander. A second topic inside 3 s is silent. "Ellis, hello" makes Ellis answer. The same topic from Mara is silent until 15 s, then answered. A whispered name question starts "Mara.". A yell, "forest", "buy", the switch off and a dead player get nothing. Of two equally close residents, the lower serial answers. |
| `TheTutorialPhaseIsReadOnly` | An account with no data gets the visitor line and still has no data afterwards. An InCore record for this character gets the Rook line. Another character on the account reads Any. With every core station done it reads AfterCore and gets the general line. The record's state and stations are unchanged. |
| `TheTopicMenuSharesTheRulesAndGrantsNothing` | Double-click opens the menu with no reply. A press from another player's client does nothing. A press answers and reopens. A second press inside the cooldown is silent. After Mara moves 8 tiles away, nothing. With the switch off the menu will not open and a stale press does nothing. |
| `AResidentsIdentityComesFromItsSavedTag` | Trades is Ellis, the workshop runner, invulnerable and not walking. An unknown tag becomes Mara. The tag and name survive a save and load. |

How I ran them: builder image `sl-uo-builder:cc-P635` (main plus P628, the same as this branch for everything townsfolk touches), with the `Townsfolk` folder, the fact file and the data file bind-mounted to the paths the Dockerfile uses. `dotnet test` was filtered to `TownsfolkTalkVerification`, with the gate's flags. Scripts and logs are in the session scratchpad.

**Red.**
- Stub 1: the same public names and no behaviour (no loading, `Normalize` returns its input, no match, service off, residents with no identity). 8 of 8 failed. Facts 1, 5, 7 and 8 failed on assertions ("Value is null", "collection was empty", "Strings differ"). Fact 3 failed on "Expected: True". Facts 2, 4 and 6 failed on exceptions, because without a table there was nothing to assert on.
- Stub 2, run to get assertion failures: the real loader, stubbed service and resident. Facts 1, 5, 6, 7 and 8 failed on assertions (fact 6 on "Expected: Core, Actual: Any"). Facts 2, 3 and 4 passed, since their subject is the real loader. The loader's own guards are shown by the mutants below.
- The real code **without** the data file mounted (as if the Dockerfile line were missing): 7 of 8 failed. The shipped-file fact failed on "Value is null".

**Green.** The real code with the data file: 8 of 8 on the first run, with no compiler warnings from the new files.

**Mutations of the finished code**, each run alone:

| Mutant | Red facts |
|---|---|
| t1: the reserved-alias check removed | `TheParserRefusesABadTableOutright` |
| t2: substring matching instead of exact aliases | `MatchingIsExactWords` |
| t3: a failed reload drops the table in use | `AFailedReloadKeepsTheTableInUse` |
| t5: the phase read with `GetOrCreate` | `TheTutorialPhaseIsReadOnly` (account data appears) |
| t4: nearest only, the named-first rule removed | **survived** |

Each caught mutant turned exactly its one fact red, 7 of 8 passing. t4 survived for a real reason: `Match` already accepts a name-first phrase ("ellis hello") only for the NPC it names, so the named-first rule in `Select` could never change the outcome. That rule was dead code. I removed it, along with the `Addresses` helper it used, and documented in the service header that naming works through `Match`. The matching fact now checks that another NPC's name does not match (`"Ellis, hello"` against Mara). Re-run: 8 of 8.

## 3. Build gate

`docker\uo\build.sh -t sl-modernuo:cc-P631`, under the Golem's `docker-build` lock (taken, then released after the second run). The Docker VM's page cache was dropped before each run, and each was started detached.

- **Run 1: red.** The builder log shows the new step, `COPY server/data/townsfolk-talk.json /build/modernuo/Distribution/Data/ShatteredLegacy/townsfolk-talk.json`. 2,549 tests: 2,544 passed, 4 skipped, 1 failed: `TheShippedTableLoadsFromTheBuildersDataFolder`, "Sub-string not found". In the real build the file is found first **beside the test host** (`/build/modernuo/Projects/UOContent.Tests/.../Data/ShatteredLegacy/`), because the build also copies `Distribution/Data` there. That copy comes from the same Dockerfile line. The fact now asserts the path ends `Data/ShatteredLegacy/townsfolk-talk.json`, which covers all three places the copy lands (Distribution, beside the test host, `/modernuo/Data`).
- **Run 2: green**, exit 0: "Built sl-modernuo:cc-P631 with patches applied and 2545 shard test(s) passing". 2,549 tests, 2,545 passed, 4 skipped (the real-map facts), 0 failed. Image `9f0cd95bf665`. All 8 townsfolk facts passed, and so did the 5 `CommandDeclarationVerification` facts (so `[ClusterFTownsfolk`'s declaration is accepted).
- **Shipped bytes:** `/modernuo/Data/ShatteredLegacy/townsfolk-talk.json` in the finished image has SHA-256 `7457c730...203a4`, identical to `server/data/townsfolk-talk.json`. It sits beside `CHANGELOG.md` and `VERSION`.

## 4. CHANGELOG

A `## 2026.10.26.3` section with one **Staff** line (the switch, the two `[add` commands, the topics, the cooldown, the tutorial pointer, reload). `VERSION` `2026.10.26.3`, above P629's `2026.10.26` already in this branch and P630's `2026.10.26.2` still on its own branch. There are no player lines: players see nothing in stage 1.

## 5. Deviations and decisions for Chase

- **Rest lines held back** (section 1): the inn line and the innkeeper's job line leave out rest until stage 2 adds it. Stage 2's draft puts them back.
- **"South-west", not "south"** for the League office, from the seeded anchors. Nobody has checked yet that the view from the plaza matches (stage 3 is the client walk).
- **Residents outside the seeder:** staff can `[add` a resident by hand on the test shard. The design's seeder (all-or-nothing placement, dry run, removal) is stage 3. Until then, a hand-placed resident outside New Haven simply never answers, because of the region check.
- **Cooldown storage:** the design suggests per-player timestamps on the player. I used a `ConditionalWeakTable` keyed by the mobile: it is never saved, needs no `PlayerMobile` partial, and is collected with the mobile. Stage 2's combat history will need the `PlayerMobile` partial anyway (`OnHitsChange`).
- The Read tool stayed off for the work-copy files in this unattended run, as in P630. Edits to existing files went through the same exact-replacement helper, and new files were written whole.

## 6. Proposed invented-feature register text (for the overseer, not `docs/`)

> New Haven townsfolk and inn rest (P566 design, P631 onward). Native shard content inspired by David's conversational townsperson (uploaded by Zavreyon) and Zigholtul's specialized innkeeper (P405 notes; no code or dialogue copied). Two New Haven residents (Mara, the town steward, and Ellis, the workshop runner) and the existing innkeeper answer a small set of spoken or menu topics, privately, in their own voices. The innkeeper sells a self-only, out-of-combat restore for 25 backpack gold. Both are independently off by default. Stock NPC services, account progression and OSI quests are unchanged.

## 7. Remaining stages, ready to number

Each prompt writes its own notes, keeps files under 5 MB, checks its stop-request file, lets the Golem commit, starts from current canonical source, rereads the agreements, P566 and this note, and never deploys or contacts Haven.

### Draft A: New Haven inn rest and the existing innkeeper (stage 2)

**Touches:** server, client-package

Depends on P631. Chase's choices (10-25): 25 gold, after 120 seconds without harm, 60-second reuse; Mara, Ellis and the existing innkeeper.

1. `Townsfolk/ClusterFInnKeeperExtension.cs`: a partial `Server.Mobiles.InnKeeper` implementing `ITalkResident` with profile `innkeeper`. It answers topics only while inside `the New Haven Inn` (or a child) on Trammel. Exact `rest` (and "<name> rest") opens the quote. The stock speech type and vendor AI keep every other command. Add no serializable member or serialization attribute to the stock class. Check `GargoyleInnKeeper` too.
2. Put the held-back rest lines back into `server/data/townsfolk-talk.json`: the inn line, and the innkeeper's job line with "Say rest".
3. `Townsfolk/ClusterFInnRestCombat.cs`: subscribe once to `EventSink.AggressiveAction`, recording attacker and defender and their player masters (`GetMaster`). Add a partial `PlayerMobile.OnHitsChange` that records decreases only. Keep nonserialized timestamps on the player. Apply a 120-second hold after world load.
4. `Townsfolk/ClusterFInnRest.cs`: settings `clusterf.townsfolk.rest.enabled` (false), `rest.fee` 25, `rest.quietSeconds` 120, `rest.cooldownSeconds` 60, `rest.quoteSeconds` 30, all validated. A quote gump with the design's text; one outstanding quote bound to player, NetState, innkeeper, fee and settings generation; a one-use token. Confirm rechecks everything: region, range 3, LOS, visibility, criminal, 5+ kills, combatant, aggression, quiet period, poison, bleed, mortal wound, hidden, owned pets' combat via `AllFollowers`, and all-full. Then call `Backpack.ConsumeTotal(typeof(Gold), fee)` once and, only if it succeeds, fill the three pools and start the 60-second cooldown. Use the design's refusal messages, rounding waits up.
5. One Rest context cliloc: reserve the next free number (recheck 1900014) in `ShardClilocs.cs`, `player-package/vendor/shattered-legacy-cliloc/entries.json` and the append-only `registry.csv`. Run the PS 5.1 Pester cliloc checks, including an intentional missing-entry failure first.
6. Red-then-green facts for every rest and callback case in P566's table (money across nested stacks, bank-only funds, each one-pool deficit, duplicate confirm, replaced or expired quote, moved vendor, foreign session, all combat and effect cases through the real aggression event and Hits setter, and the time boundaries with `ShardTestClock`). Buy and sell speech to the innkeeper must still work. Show each red first.
7. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green. Both switches off. Do not publish the package. CHANGELOG Staff line only. Notes; `P<nn> DONE`.

### Draft B: New Haven townsfolk placement and isolated acceptance (stage 3)

**Touches:** server

Depends on Drafts A and P631.

1. `Townsfolk/ClusterFTownsfolkSeeder.cs`: `[ClusterFSeedTownsfolk [dryrun]` and `[ClusterFRemoveTownsfolk [dryrun]`, Administrator and test shard only (`ClusterFStaffHub.IsTestShard`), each with a `[ShardCommand]` declaration. All-or-nothing: compute ground Z, `CanFit`, New Haven region membership, no door, stairs, tutorial mark or NPC collision, and a reachable neighbour tile. Otherwise refuse both and report the point. Identify residents by type and tag; report duplicates and moved residents; never create or delete an innkeeper, spawner or unrecognised resident.
2. Check the candidates against the map (Mara 3508,2582; Ellis 3474,2544; ground Z) using hash-verified client files, and record the final points with evidence. Keep them clear of Rook's arrival tile and the core lesson marks.
3. Red-then-green facts: seed refusal, dry run with no change, idempotent rerun, save round-trip, removal only of owned tags.
4. Under the `test-shard` lock, on a private loopback scratch shard with a current client: journal and overhead text, menu contrast, the innkeeper's buy and sell, the Rest label with the updated package and the fallbacks without it, payment, walking out before confirming, combat and pet-combat refusal, restart and save/reload with no duplicates. Record the client and package used and what stays unverified.
5. Build gate green. Write the exact activation and rollback steps for Chase using the existing settings. Do not switch anything on. Notes; `P<nn> DONE`.

### Draft C: New Haven townsfolk player guide and handoff (stage 4)

**Touches:** docs-only

Depends on Draft B's verified behaviour. Write `notes/wiki-drafts/new-haven-townsfolk-and-rest.md` and a handoff note: the actual names, places, phrases, price, timers, backpack-only payment, refusal rules, the package label requirement and the activation status. Cross-check the tutorial guide's directions to Rook and the inn. Mark both features planned until Chase switches them on. Include the register text above. Do not edit `docs/` or publish. Notes; `P<nn> DONE`.

P631 DONE
