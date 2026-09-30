# cc-P18: reset stone and per-character guild data (F-7), Young by time played (F-5), craft X (F-1)

Date: 2026-09-30. Agent: Claude Code. Pinned ModernUO `7c9215d97`. Brief: `D:\UO\cc-prompts\cc-P18-reset-stone-young-craftx.md`.
Specs: `docs/feature-queue.md` F-7, F-5, F-1. Built in `D:\ShatteredLegacy`, **not committed** (Chase runs `Commit-ShardWork.ps1`).
No world was changed: nothing placed, moved or removed, no shard deployed, restarted or recreated. `sl-modernuo:latest`
was not moved (`16b0f49e6828` before and after). Image: `sl-modernuo:cc-p18` = `dbc1036aa991`.

**Gate before starting.** `git --no-optional-locks status` in `D:\ShatteredLegacy` was clean at `bb51fad`. P15's
`GuildStarterRecord` (ClusterFAccountData v14) is in `99d5273`; P17's files (for example
`server/tests/Engines/Craft/MakeXRepeatVerification.cs`) are in `bb51fad`. Both notes read; nothing in them changes this plan
except P17 section 7 (PT-04), which F-1 builds on.

> **Headlines**
>
> 1. **F-7 built, all green, every new fact watched red first.** Guild data (membership, Apprentice marks, reputation,
>    scrip, work orders, smith commissions, the Artificer order) is per character: `CharacterGuildData`, keyed by
>    character serial like exploration, in `ClusterFAccountData` **v15**. Old saves: the account-level guild data is
>    **cleared**, not guessed onto a character, and the server says so once in the console at load (section 1.6).
>    The reset is rebuilt by scope (this character / every character / the account) and now clears everything the
>    brief lists. `[ResetMyAccount` and a **Reset Stone** open the same gump through the same code as `[ClusterFReset`.
> 2. **F-5 built, all green, every brief fact watched red first.** 336 hours of account game time; no skill rule; the
>    murder rule kept; "I want to grow up!" opens OSI's confirm; countdown in days and hours. **Two small patches** to
>    pinned (`Account.cs`, `PlayerMobile.cs`): no hook reaches either rule (section 2.2).
> 3. **F-1 stopped at Part A, as the brief allows.** It is clearly more than a moderate change: make-X is **ours, not
>    pinned's**, woven into our 1,486-line `CraftItem.cs` replacement; "gump closed" has no gump to close today; and the
>    salvage bag's own code salvages **the whole bag**, which collides with "nothing else is touched". Findings, a plan
>    and three decisions for Chase are in section 3.
> 4. **One file outside the brief's list was changed:** `docker/uo/apply-patches.sh` gained the two `apply_patch` lines
>    for F-5's patches. The gate fails any patch it does not name, so a patch cannot exist without its line (section 2.3).
> 5. **ASCII.** Every file touched is ASCII now. Most of the 33 guild files carried box-drawing rules and em dashes
>    before; they were converted, which changes some **player-visible text** slightly (section 4.3).
> 6. **304 shard tests pass** (293 before; 11 new). Two red runs, each break aimed at one fact, every file restored
>    byte-identical by SHA-256 (section 5).

---

## 1. F-7: reset stone, and guild data per character

### 1.1 A1: every call site of the account guild API

Counted at `bb51fad` (before this task) with `notes/cc-P18-tools/callsite_table.py` (the regex is the eight names the
brief lists; comments and `[Description]` strings excluded): **35 files, 203 code lines**: 33 in `server/customizations`,
2 in `server/tests`. The brief's "about 33 files" is right for customizations alone. Every site had a `PlayerMobile` in
reach, found by reading the line that defines each site's account variable (`cc-P18-tools/find_acct.py`); the three
exceptions are marked.

| File | Reads (line) | Writes (line) | Character in reach |
|---|---|---|---|
| `ArtificerWorkOrderSystem.cs` | 557, 855 | 1009, 1010, 1015, 1016 | pm or _pm |
| `ArtificersGuildmasterGump.cs` | 81, 218, 219 | - | pm or _pm |
| `ArtificersImbueGump.cs` | 566, 567, 568, 905, 1146, 1201, 1202, 1385, 1553 | 1413, 1433, 1457, 1523, 1569 | pm or _pm |
| `ArtificersToolkit.cs` | 51 | - | pm or _pm |
| `ClusterFCompactAdminTools.cs` | 69, 99, 116 | 64, 94, 246, 247, 248 | the targeted PlayerMobile |
| `ClusterFCustodianSystem.cs` | - | 222, 223 | pm |
| `ClusterFDevTools.cs` | - | 98, 99, 104 | **account only** (a character if one is online or named); the reset clears every character, so none is needed |
| `ClusterFGuildStarterPath.cs` | 455, 457 | 486 | pm or _pm |
| `ClusterFGuildSystem.cs` | 297, 587, 737, 763, 883, 1059, 1069, 1073 | 395, 396, 413, 1084, 1085, 1086 | pm or _pm; **`IsJoined(IAccount)` at :296 took only the account**, and all 20 of its callers had a PlayerMobile |
| `ClusterFLeagueSystem.cs` | 63, 152 | - | pm at :151; **`GetStatus(data)` at :63 took only the account record**; its caller (`LeagueRegistrarGump`) has `_pm`, now passed in |
| `ClusterFSmithBODSystem.cs` | 89, 143 | 231, 232, 418, 419 | pm / pmComm |
| `ClusterFSmithCommissions.cs` | - | 608, 609, 678, 679 | pm |
| `ClusterFWorkOrderSystem.cs` | 149, 175 | - | pm (parameter) |
| `CompactDispatchLedger.cs` | 54 | - | pm |
| `CompactOreSatchelRoutingHook.cs` | - | 250 | pm (Mobile m cast) |
| `CrossGuildExchangeGump.cs` | 74-77, 143-146 | 189-192 | pm or _pm |
| `ForestersGuildmasterGump.cs` | 83, 208, 209, 349, 364, 384, 399 | 376, 411 | _pm |
| `ForestersLogbookGump.cs` | - | 352, 353 | pm |
| `GuildContractLedgerGump.cs` | 231, 436 | 517, 518 | _pm |
| `HammerOfHephaestus.cs` | 1047, 1048, 1202, 1247, 1248 | 1225, 1271 | pm or _pm |
| `JacobsDeepdelverPickaxe.cs` | 214, 215, 298, 299 | 319 | pm or _pm |
| `JacobsProspectorPickaxe.cs` | 213, 214, 296, 297 | 317 | pm or _pm |
| `JacobsReinforcedPickaxe.cs` | 242, 243, 334, 335 | 357 | pm or _pm |
| `JacobsWorldbreakerPickaxe.cs` | 217, 218, 305, 306 | 327 | pm or _pm |
| `MinersCompactLiaisonGump.cs` | 155, 280, 281, 411, 412, 567, 812, 836, 933, 948, 972, 993, 994, 1092, 1110, 1146, 1166, 1218, 1238 | 870, 960, 1020, 1026, 1032, 1038, 1122, 1195, 1273 | pm or _pm |
| `OutridersGuildmasterGump.cs` | 82, 207, 208, 226, 325, 344, 365, 384 | 350, 387 | pm or _pm |
| `SanitationWardenGump.cs` | 95, 96, 165, 303 | 310 | pm |
| `SmithGuildBook.cs` | 170, 171 | - | pm |
| `SmithGuildSalvageBag.cs` | - | 270 | pm |
| `SmithGuildmasterGump.cs` | 86, 87 | - | pm |
| `SmithSealCatalogGump.cs` | 133, 227 | 225, 235 | pm or _pm |
| `SurveyArchivistGump.cs` | - | 338, 339 | pm |
| `TrashBag.cs` | 100, 101 | - | pm |
| `tests/Misc/AccountDataSerializerVerification.cs` | 89-93, 175-185, 287-289, 425, 426 (reads and writes) | | test code |
| `tests/Misc/GuildStarterPathVerification.cs` | 630, 635, 671, 672, 680, 681, 686 | | test code |

Also `IsJoined(acct, ...)`, the account-level membership check, at 20 call sites in 9 files (for example
`ClusterFSmithBODSystem.cs:57,80,134,182,207,406`, `SanitationWardenGump.cs:66`, `HammerOfHephaestus.cs:1323`); each had
`pm` in scope and now passes it.

### 1.2 A2: other account data tied to a guild

| Data | Tied how | Done |
|---|---|---|
| `ActiveWorkOrders` / `CompletedWorkOrders` | each entry has a `GuildKey`; eligibility reads the guild's standing (`ClusterFWorkOrderSystem.cs:149`); turn-in pays rep and vouchers (`GuildContractLedgerGump.cs:517`). Per account, character B could turn in A's order and be paid. | **moved** |
| `SmithCommissions` / `SmithLargeCommissions` | Smiths' commissions, paid in Smiths' rep and seals (`ClusterFSmithCommissions.cs:608`). | **moved** |
| `ActiveArtificerOrderKey` / `ItemSerial` | one Artificers' order at a time, paid in Artificers' and Smiths' rep and scrip (`ArtificerWorkOrderSystem.cs:1009-1016`). | **moved** |
| Apprentice marks (account flags `guild.apprentice.<key>`, cc-P15) | a guild rank. | **moved** (to `CharacterGuildData.ApprenticeGuilds`) |
| `OreDiscoveries`, `WoodDiscoveries` | knowledge, **but reporting a vein pays Mining rep and vouchers** (`SurveyArchivistGump.cs:338`) and marks it `Reported` per account. A second character cannot be paid again for a vein the first reported. Ore discoveries also gate mining work orders (`ClusterFWorkOrderSystem.cs:154`). | **left per account; for Chase** |
| `ImbuingDiscoveries` | Artificers' mastery count per property; gates Artificer orders (`ArtificerWorkOrderSystem.cs:175`). | **left; for Chase** |
| `EncounteredCreatures` | bestiary; gates hunting work orders (`ClusterFWorkOrderSystem.cs:158`). | **left; for Chase** |
| League flags (`league.joined` etc.) | League registration is an account flag; "Recognized Citizen" now means this character is in a guild (`ClusterFLeagueSystem.cs:60-66`). | left per account |
| Renown, AP, achievements, restoration registry | account-wide by their own design (Renown "is account-wide and permanent", `LeagueRegistrarGump.cs:143`). | left |

**Recommendation:** keep discoveries per account until F-4 settles it. They are knowledge and belong to the player; the
one wrinkle is that report rewards are paid once per account. Moving them would mean a v16 and another cleared block.

### 1.3 A3: how exploration is stored

`ClusterFAccountData._exploredChunks`, `Dictionary<uint, BitArray?[]>`: character serial to six facet bit arrays
(`ClusterFAccountData.cs:92-100` at `bb51fad`). Serialized as count, then per character the serial and six (bool,
BitArray) pairs (`:359-373`). Written since v8, reordered in v10. `CharacterGuildData` follows the same pattern: a
dictionary keyed by `(uint)serial`, written as count then (serial, record) pairs, with the record carrying its own
version like P15's `GuildStarterRecord`.

### 1.4 A4: what the reset did not clear

`ClusterFDevTools.ExecuteReset`, **as of `bb51fad`**: "Account Data" (`:94-107`) cleared Renown, guild reputation, guild
currency, the restoration registry and, since P15, `JoinedGuilds`, the `guild.apprentice.*` flags and every character's
starter record. The overseer's "clears only Renown, guild reputation, guild currency and the restoration registry" was true
at `d0a1782` and stale after P15. It still left:

| Field | Now cleared by |
|---|---|
| `ActiveWorkOrders`, `CompletedWorkOrders` | Guilds (per character now) |
| `SmithCommissions`, `SmithLargeCommissions` | Guilds (per character now) |
| `ActiveArtificerOrderKey`, `ActiveArtificerItemSerial` | Guilds (per character now) |
| `OreDiscoveries`, `WoodDiscoveries`, `ImbuingDiscoveries` | Discoveries |
| `EncounteredCreatures` | Discoveries |
| `_exploredChunks` (every character) | Exploration |
| `Flags` other than `guild.apprentice.*`, `FlagValues` | League, flags |
| `AchievementPoints` | Achievements (already, separate box) |
| `LastSeenBulletinId` | Bulletins (already, separate box) |

### 1.5 A5: P15's layout

P15 kept membership per account and made only the starter record per character (`GuildStarterRecord`, v14): tools and
starter items taken, and the welcome, per serial. F-7's layout agrees: a **separate** per-serial record for guild data,
beside P15's, so P15's record and its tests are untouched. The Guilds reset clears both. P15's fact 2 encoded the old
behavior ("Already a member." for a second character, PT-06) and was changed to the new one: the second character is not
a member, joins on its own, and gets its own tools (`GuildStarterPathVerification.cs:243`).

### 1.6 B: what was built

**Per-character guild data.** `CharacterGuildData` (`ClusterFAccountData.cs`, own version 0; an unknown version throws,
the D40 rule) holds `JoinedGuilds`, `ApprenticeGuilds`, `GuildReputation`, `GuildCurrency`, `ActiveWorkOrders`,
`CompletedWorkOrders`, `SmithCommissions`, `SmithLargeCommissions` and the Artificer order, **with the member names the
account record had** (`GetReputation`, `AddCurrency`, `SpendCurrency`, ...). So each call site changed from `data.X` to
`guild.X` and nothing else, with `guild` from `ClusterFAccountPersistence.GetOrCreateGuild(pm)` or
`data.GetOrCreateGuildData(pm.Serial)`. `IsJoined` and `GetRankName` take the character's record. **To fold back to
account-wide when F-4 lands**, key every character of an account to one record in `GetOrCreateGuildData` (comment there);
no call site changes.

**Serialization, v15.** The account record no longer writes the eight guild blocks. The reader still reads them for
`version < 15`, into a throwaway record, and **drops them**, along with any `guild.apprentice.*` flag.
`DroppedAccountGuildData` is set when anything was dropped; `ClusterFAccountPersistence.Deserialize` then prints once:
`[ClusterFAccountPersistence] Cleared account-level guild data on N account(s): guild membership, reputation and scrip
are per character from this build (cc-P18).` **On the test world, after this build, every account's guild membership,
rank, reputation, scrip, work orders, commissions and Artificer order are gone.** That is Chase's decision
("clear, do not guess"). An Artificer work-order item already handed out stays in its owner's pack, orphaned; it can no
longer be turned in.

**The reset.** Options by scope, in three labeled sections of the gump:

| Scope | Options |
|---|---|
| This character only | Skills, Stats, Quest History |
| Every character on the account | **Guilds** (membership, rank, rep, scrip, work orders, commissions, tools and starter items), **Exploration** |
| The account | Achievements, Renown (with the restoration registry), **Discoveries** (ore, wood, imbuing, creatures encountered), **League and flags**, Bulletins |

The confirm lists exactly what the options' `Describe` returns: one line per box ticked, each ending with whom it clears
for ("this character (Name)", "EVERY character", "the account"). Above the list it says in red that lines marked EVERY
character affect every character on the account and that the reset cannot be undone. Exploration clears every
character's chunks and re-sends the (empty) map to any character online, through `ClusterFExplorationManager.OnPlayerLogin`.

**Player access, one code path.** `ClusterFDevTools.OpenReset` builds and sends the gump; `ExecuteReset` applies it. Three
entries call it: `[ClusterFReset [username]` (Administrator, unchanged behavior), `[ResetMyAccount` (Player) and the
stone. The last two go through `OpenSelfReset(from)`: the caller's own account and current character. **There is no
argument and no target**; a name typed after the command is ignored (fact 5). The gump's account is fixed when it is
built, and a gump response carries only buttons and switches, so a client cannot redirect it.

**The stone.** `ResetStone` (`ClusterFResetStone.cs`): graphic `0xED4`, pinned's gift-stone art (`IngotStone`,
`RegStone`, ...), in **one constant** `StoneGraphic` for F-8. Hue `0x2B`, name "a Reset Stone (test shard)". Not movable,
`Decays` false, use range 2.

**Where it stands: 3501,2575,14 Trammel.** Two tiles south-west of the New Haven arrival tile (3503,2574,14,
`CharacterCreation.cs:114`, where Sir Helper stands), across that tile from the Guild Board (3502,2573,14,
`NewHavenQuestBoard.HomeLocation`). Checked with cc-P15's `fit.py` (port of pinned `Map.CanFit` over the client map, statics
and pinned's New Haven decoration): standable at z 14 only, **no static on the tile**. The tiles east of the arrival tile
are the inn's stone steps (z 16 to 18), which a stone would block. **Not checked:** what items the test or live world
already has on that tile (no save was read for this); the dry run reports what it would do, and the seeder places nothing
if any Reset Stone is already anywhere in New Haven.

**Seeder.** `ClusterFResetStoneSeeder`: `[ClusterFSeedResetStone [dryrun]` (Administrator). A fresh world gets it at world
load only if `clusterf.resetStone.seedOnWorldLoad` is true (default false, like P17's services seeder; the server writes the
default into `modernuo.json` on first start). Otherwise Chase runs the command. It moves and deletes nothing.

**Go-live.** The stone, its seeder, `[ClusterFSeedResetStone` and `[ResetMyAccount` are marked `TEST-SHARD TOOL` in the
code (`ClusterFResetStone.cs` header and class, `ClusterFDevTools.cs` Configure). **At the live rebirth:** delete
`ClusterFResetStone.cs`, remove the `ResetMyAccount` registration and `OpenSelfReset` from `ClusterFDevTools.cs`, delete
`ResetStoneVerification.cs` facts 5 and 6 with them, and remove any placed stone (`[Global delete where ResetStone` or by
hand). The admin `[ClusterFReset` stays.

### 1.7 Tests (F-7)

`server/tests/Misc/ResetStoneVerification.cs` (new, 4 facts) and `AccountDataSerializerVerification.cs` (2 new, 2 changed):

| Brief | Fact | Shows |
|---|---|---|
| 1 | `TwoCharactersOnOneAccountHaveTheirOwnGuildsReputationAndScrip` | first joins, second not a member and can join; the Apprentice task pays only the first; the second cannot do it; ranks differ; scrip spent by one is not spent by the other |
| 2 | `AVersion14SaveWithAccountLevelGuildDataLoadsAndTheGuildDataIsCleared` | v14 bytes from a **frozen copy of the `bb51fad` writer** (`ClusterFAccountData.cs:316-398` there) with every guild field and an Apprentice flag: read to the last byte; no character has guild data; no Apprentice flag left; everything else kept, starter records too; re-saved as v15; a v14 save with no guild data is not reported as dropping any |
| 2 | `AVersion13SaveFromTheBuildBeforeGuildStarterRecordsLoads` (changed) | P15's v13 load, now also dropping the account guild data and re-saving as v15 |
| 3 | `AnAccountWithEveryCollectionNonEmptySurvivesAWriteAndARead` (changed) | two characters' guild data (every field, every collection non-empty on the first) and two characters' exploration, round trip to the byte |
| - | `AnAccountRecordOrStarterRecordOfAnUnknownVersionFailsLoudly` (one assert added) | an unknown `CharacterGuildData` version throws |
| 4 | `TheResetWithEverythingSelectedEmptiesEveryCharacter` | two characters with guilds, rank, rep, scrip, both kinds of work order, both kinds of commission, an Artificer order and exploration; account discoveries, flags, renown, AP, bulletins: all empty after; the confirm's 10 lines, 2 of them "EVERY character" |
| 5 | `ResetMyAccountAndTheStoneReachOnlyTheCallersOwnAccount` | through `CommandSystem.Handle`: `[ResetMyAccount <other account>` by a Player opens the gump for **their own** account and character; `[ClusterFReset <other>` gives a Player nothing; the stone gives each user their own; out of range, nothing; not movable, no decay |
| 6 | `TheSeederRunTwicePlacesOneStone` | dry run places none; two runs place one, at 3501,2575,14 Trammel, graphic `0xED4` |

P15's facts changed with the behavior: fact 2 (above), fact 9 (Guilds option instead of Account Data), the Apprentice fact
and the join fact (the character's record instead of the account's).

---

## 2. F-5: Young status by time played, 2 weeks

### 2.1 A1: pinned's rules, confirmed

| Rule | Where (pinned `Projects/UOContent`) |
|---|---|
| `YoungDuration` 40 hours | `Accounting/Account.cs:21` |
| checked | `CheckYoung` declared at `:833`, the comparison at `:835` (the brief's `:835`); run each minute by `YoungTimer` (`:1095-1109`), started on connect (`:759-763`), and at load (`:208`, `:328`) |
| counter | `Account.TotalGameTime`, account-wide, deleted characters included (`:90-110`) |
| login countdown, hours | `OnLogin` `:788-806` |
| skill total 450.0 | `Mobiles/PlayerMobile.cs:4149-4153` (`SkillsTotal >= 4500`, message 1019036) |
| murder | `PlayerMobile.cs:4119-4125` (`OnKillsChange`) |
| renounce keyword | `Misc/Keywords.cs:40`, keyword `0x35`, opens `RenounceYoungGump` (`Gumps/YoungGumps.cs:61`), whose OKAY calls `RemoveYoungStatus(502085)` |

### 2.2 A2: patch or hook, per change

Patches apply through `docker/uo/apply-patches.sh` (`apply_patch`, `patch -p1 --fuzz=0`, dry run first; a patch file
not named there fails the build, `:329-345`). Policy (`docs/subsystem-policy.md:94-112`): a patch where no `UOContent` hook
exists; a failing patch beats copied upstream logic. Both patches here are in `UOContent`, not core.

| Change | Route | Why |
|---|---|---|
| duration 336 h | **patch** `Account-young-duration.patch`: `YoungDuration = ClusterFYoungPlayer.Duration` | a `static readonly` in pinned, read by `CheckYoung` and `OnLogin`; no hook. Writing it by reflection was not tried: .NET refuses to set an initonly static after type initialization, and it would route around the gate. |
| countdown in days and hours | **patch**, same file: `OnLogin` sends `ClusterFYoungPlayer.LoginMessage(ts)` | the text is inside pinned's `[OnEvent]` handler |
| skill rule removed | **patch** `PlayerMobile-young-time-only.patch`: the five lines become a comment | inside `PlayerMobile.OnSkillChange`; PlayerMobile cannot be replaced for every player |
| murder rule | untouched | kept |
| "I want to grow up!" | **hook**: `EventSink.Speech` in `ClusterFYoungPlayer.Configure` | speech is an event; no patch |

The single constant is `ClusterFYoungPlayer.Duration` (`TimeSpan.FromHours(336.0)`). Both patches keep pinned's lines
beside a comment naming this file, as `PlayerMobile-individual-stat-cap.patch` does.

### 2.3 A3: custom code that sets or checks Young

`CharacterCreation.cs:218-220` copies the account's Young onto a new character (as pinned's does); `DrelgorTheImpaler.cs:64`
and `Mobiles/Bosses/Medusa.cs:122` set `IgnoreYoungProtection`. Nothing else. None changes.

**Outside the brief's list:** `docker/uo/apply-patches.sh` gained the two `apply_patch` lines, with a comment in the
style of P8's and P9's. Without them the gate fails: the first F-5 build stopped with "Account-young-duration.patch
present in /patches but never applied or skipped by name".

### 2.4 B: what was built

`ClusterFYoungPlayer.cs`: the constant, the phrase handler (loose match: case, spacing, and trailing "!" or "." ignored;
the whole line must be the phrase), and the countdown: "You will enjoy the benefits and relatively safe status of a young
player for another 13 days and 23 hours of play time. Say "I want to grow up!" to give it up sooner." Young stays per
account, as pinned has it. OSI's phrase is untouched and still works.

### 2.5 Tests (F-5)

`server/tests/Misc/YoungPlayerVerification.cs` (new, 6 facts): the duration reached pinned (`Account.YoungDuration` is
336 h); **1** 335 h played, skill total 490.0, still Young after `CheckYoung`; **2** still Young at 40 h and at 336 h minus a
minute, not Young at 336 h, on both characters; **3** OSI's phrase (keyword 0x35) and six spellings of ours open the
confirm, seven other lines do not, OKAY ends Young, and after that the phrase opens nothing; a murder count still ends
Young; the countdown reads "14 days", "13 days and 23 hours", "1 day and 1 hour", "5 hours", "less than an hour".

---

## 3. F-1: craft X, keep going on failure (stopped after Part A)

### 3.1 A1: is there a make-X already?

**Pinned: no.** Pinned's craft gump has MAKE LAST (`Engines/Craft/Core/CraftGump.cs:72`, `:635`) and MAKE NOW; no count
and no repeat (`RepeatCount` does not occur in pinned). **Ours: yes.** `CraftGumpItem-MakeX.patch` adds a MAKE X button that
opens our `CraftCountGump.cs` (presets 5 to 100, custom up to 200, clamped at `:103`). It arms
`CraftContext.RepeatCount` / `RepeatItem` / `RepeatTypeRes` (our `CraftContext.cs` replacement, `:34-40`), and our
`CraftItem.cs` replacement continues on success (`:1281-1287`) and **stops on the first failure** (`:1357-1361`). P17 found
it also stays armed after a pre-check failure and never says it stopped (P17 section 7). F-1 builds on this.

### 3.2 A2: exceptional chance, and "cannot be exceptional"

`CraftItem.GetExceptionalChance` (`CraftItem.cs:807`, ours, as pinned) from the success chance and the system's `ECA`,
plus a talisman bonus. It is 0 when `ForceNonExceptional` is set, which recipes set through
`CraftSystem.ForceNonExceptional(index)` (pinned `CraftSystem.cs:290`; 54 calls across pinned's `Def*.cs`). The same flag
already hides the maker's-mark option (`CraftItem.cs:326`). Hide "exceptional only" when `ForceNonExceptional` is set or
the item type has no quality (not `BaseWeapon`, `BaseArmor`, `BaseClothing` or another quality-bearing `ICraftable`).

### 3.3 A3: what can be recycled, and how

| Craft | Path in pinned | Public? |
|---|---|---|
| Blacksmithy | resmelt (`CraftSystem.Resmelt`, set only by `DefBlacksmithy.cs:694`); `Core/Resmelt.cs` target, per item | per-item smelt is **private** (`Resmelt.InternalTarget.Resmelt`, `Resmelt.cs:43`) |
| Tailoring (cloth, leather) | scissors: `IScissorable.Scissor` on `BaseClothing` (`Items/Clothing/BaseClothing.cs:255`) and `BaseArmor` (`Items/Armor/BaseArmor.cs:659`), which cut back to half the resource; `Scissors.CanScissor` | **public** |
| Salvage bag | Salvage Ingots (anvil and forge within 2, a smithing tool), Salvage Cloth (scissors) | **private** (`SalvageBag.cs:45,172,241,289`), and each works on **everything in the bag** |
| Tinkering, Carpentry, Bowcraft, Inscription, Alchemy, Cooking, Glassblowing, Masonry | none in pinned (`Resmelt` is set only for Blacksmithy) | - |

### 3.4 A4: the salvage bag hook

Two problems, not one. The methods are private; and the bag's own salvage **salvages every item in the bag**
(`SalvageIngots` enumerates the whole bag at `:204`, `SalvageCloth` at `:254`). "Put rejects in the bag and run its salvage" would also salvage whatever
else the player keeps there, breaking "nothing else is touched". **Cleaner: a small documented patch** adding a public
`SalvageOne(Mobile from, Item item)` to `SalvageBag` that calls its own `Resmelt` or `IScissorable.Scissor` for one item.
That keeps the bag's own code, with no copy, and touches one item. A customizations hook cannot call a private method
without reflection, which the policy's "a failing patch beats a silent route" argues against.

### 3.5 A5: remembering toggles per player

`CraftContext` is per player per craft system, in memory (`CraftSystem.cs:16`, `m_ContextTable`), and not saved. **Yes,
cheaply:** keep the count mode and exceptional-only as `CraftContext` fields. They last until the server restarts. Saving
them across restarts is not cheap (new persistence) and not recommended.

### 3.6 A6: size, and why F-1 stops here

| Piece | Estimate |
|---|---|
| `CraftCountGump` rewrite: mode toggle, exceptional-only (hidden when impossible), caps 100/500, rejects-bag target | ~200 lines |
| run engine (counters, caps, stops, summary), separate from rejects | ~250 lines |
| hooks in our `CraftItem.cs` replacement: success, skill failure, and the three pre-check exits (skills, materials, `CanCraft`) | ~60 lines in 5 places of a 1,486-line replacement |
| rejects: smelt, scissor, salvage bag, plain bag; Custodian trash-bag hook left marked | ~150 lines |
| `SalvageBag-salvage-one.patch` (new pinned patch) | ~15 lines |
| tests through the real timer chain (P17's `MakeXRepeatVerification` harness) | ~400 lines |

**About 1,100 lines, one new pinned patch, and three decisions only Chase can make:**

1. **Salvage bag:** salvage only this run's rejects (needs the patch above; recommended), or accept that the bag's own
   salvage takes the whole bag?
2. **"Gump closed":** during a make-X run no gump is open today (`CraftItem.cs:1283-1287` goes straight to the next
   attempt), so there is nothing to close. Proposed: a small progress gump ("Made 12 of 20, 3 failed ... [Stop]"),
   closing it stops the run. Or drop that stop.
3. **Caps, clamp or refuse:** the custom field today clamps to 200 and says "1-200". Proposed: clamp to the cap and say so
   in the summary line.

### 3.7 Proposed plan (for a later prompt)

1. `CraftContext`: `MakeXRun` state (target, mode, exceptional-only, counts, start location, rejects container), plus the
   two remembered toggles.
2. `ClusterFCraftRun.cs`: `Begin`, `OnAttemptEnded(success, item, quality)`, `ShouldContinue(out stopMessage)`, `End`
   (summary line "Made 20 (7 failed, 1 exceptional)."), caps `ItemsCap = 100`, `AttemptsCap = 500`. Stops: out of materials,
   tool worn out, pack full or overweight, moved (location differs from the start), dead, progress gump closed.
3. `ClusterFCraftRejects.cs`: per skill, smelt (`DefBlacksmithy`), scissor (`IScissorable`), salvage bag (`SalvageOne`),
   else the chosen bag. A marked `// F-3 hook: Custodian trash bag` left unrouted (Custodian scoring would make crafting a
   token farm).
4. `CraftItem.cs`: replace the two repeat blocks with calls into the run engine, and route the three pre-check exits
   through `End`, which also fixes P17's "stays armed".
5. Tests: the five from the brief, with P17's harness (`ShardTestClock`, `BuiltInRng`).

---

## 4. What changed, file by file

All in `D:\ShatteredLegacy`. 40 files modified, 6 new.

### 4.1 New

| File | What |
|---|---|
| `server/customizations/ClusterFResetStone.cs` | F-7: `ResetStone`, `ClusterFResetStoneSeeder`, `[ClusterFSeedResetStone [dryrun]`, setting `clusterf.resetStone.seedOnWorldLoad` (default False). TEST-SHARD TOOL |
| `server/customizations/ClusterFYoungPlayer.cs` | F-5: `Duration`, the phrase handler, the countdown text |
| `server/patches/Account-young-duration.patch` | F-5: pinned `Account.cs:21` and `OnLogin` |
| `server/patches/PlayerMobile-young-time-only.patch` | F-5: pinned `PlayerMobile.cs:4149-4153` |
| `server/tests/Misc/ResetStoneVerification.cs` | F-7: 4 facts |
| `server/tests/Misc/YoungPlayerVerification.cs` | F-5: 6 facts |

### 4.2 Changed

| File | What |
|---|---|
| `server/customizations/ClusterFAccountData.cs` | v15; `CharacterGuildData`; old guild blocks read and dropped; `DroppedAccountGuildData` and the load-time line; `ClearExploration`, `ExploredCharacterCount`, `GetOrCreateGuildData`, `GetGuildData`, `ClearGuildData`; `GetOrCreateGuild(m)`, `GetGuild(m)`, `GetGuildStarter(m)` |
| `server/customizations/ClusterFDevTools.cs` | the reset by scope; `OpenReset`, `OpenSelfReset`, `[ResetMyAccount`; `ResetOptions.Describe`; the confirm's warning; the admin command's slot loop uses `account.Length` (was `Count`, which is the number of characters: a character behind an empty slot was missed) |
| `server/customizations/ClusterFGuildSystem.cs` | `IsJoined(Mobile, key)`, `IsApprentice(CharacterGuildData, key)`, `GetRankName(key, CharacterGuildData)`; join, Apprentice task and `[ResetGuild` per character; `ApprenticeFlag` removed |
| `server/customizations/ClusterFLeagueSystem.cs`, `LeagueRegistrarGump.cs` | "Recognized Citizen" reads the character's guilds |
| 30 more guild files (section 1.1 list, less `ClusterFDevTools`, `ClusterFGuildSystem`, `ClusterFLeagueSystem`) | `data.X` to `guild.X` from the character's record; `IsJoined(acct, ...)` to `IsJoined(pm, ...)`; `ClusterFWorkOrderSystem.HasActive` and `CanAccept` take the record; comments that said "per account" |
| `docker/uo/apply-patches.sh` | the two F-5 `apply_patch` lines (section 2.3) |
| `server/tests/Misc/AccountDataSerializerVerification.cs` | v15 facts; frozen v13 and v14 writers take the old account-level guild data explicitly |
| `server/tests/Misc/GuildStarterPathVerification.cs` | four facts follow per-character membership (section 1.7) |

### 4.3 ASCII

Every file touched is ASCII and LF (checked by script). 33 of them carried non-ASCII before this task: 21,194 box-drawing
characters in comment rules, 384 em dashes, 81 arrows, and a few others. They were mapped, not deleted: rules to `-`, em
and en dashes to `-`, arrows to `->`, bullets to `*`, `>=` for the sign. **Player-visible text changed in small ways:** 151
em dashes inside strings became `-`; the Hammer of Hephaestus charge bar (`HammerOfHephaestus.cs:956-957`) draws `#` and `.`
instead of block characters; the Smiths' guild book's done marker is `[x]` instead of a check mark
(`SmithGuildBook.cs:297,436`); an Artificer requirement reads `>= 3` instead of the sign. Not checked in a client.

---

## 5. Red and green runs

Green: 293 before this task (P17's count; not rerun on `bb51fad`); **304** after, the final full build that made the image.

| Run | Breaks (each aimed at one fact) | Result |
|---|---|---|
| red A | a: guild data keyed per account (`GetOrCreateGuild` and `GetGuild` use serial 0); b: the seeder never sees an existing stone; c: `Duration` 337 h; d: the phrase matched exactly | **296 passed, 8 failed**: F-7 fact 1 ("Assert.False" at `IsJoined(second, "thieves")`, line 136), fact 6 (`second.Placed` true, line 355), F-5 fact 2 (still Young at 336 h, line 166), the duration fact (14.01:00:00), F-5 fact 3 (message "I want to grow up", the spelling without "!", line 207). a also failed F-7 fact 4 (2 records expected, 1) and P15 facts 2 and 9, all expected with one shared record |
| red B | e: an old save's guild data given to a character (serial 0); f: Apprentice marks neither written nor read; g: the reset leaves exploration; h: `[ResetMyAccount` honours an account name; i: pinned's skill rule back (patch skipped by name); j: countdown in hours only | **297 passed, 7 failed**, exactly the targets: F-7 fact 2 (v14 and v13 loads: `GuildDataCount` 0 expected, 1), fact 3 (round trip: Apprentice `["mining"]` expected, `[]`), fact 4 (exploration 0 expected, 2), fact 5 (the other account's gump: expected p180e..., actual p1861...), F-5 fact 1 (not Young at 335 h with 490.0), countdown ("14 days" expected, "336 hours") |

After each run every broken file was restored from its backup and matched its first SHA-256
(`ClusterFAccountData.cs f555d396...`, `ClusterFResetStone.cs f908082c...`, `ClusterFYoungPlayer.cs d75cfc9b...`,
`ClusterFDevTools.cs 42a5a49a...`, `apply-patches.sh aeb6f06e...`). The final build ran after both restorations.

**Not watched red:** `AMurderCountStillEndsYoung` (pinned's rule is untouched; a red would mean patching it away);
the unknown-`CharacterGuildData`-version assert.

---

## 6. Deviations for the register (one line each)

| ID | What OSI does | What we do | Why |
|---|---|---|---|
| F-5a | Young ends after 40 hours of account play time | after 336 hours (2 weeks) | Chase, 2026-09-30: a longer safe start on a small shard |
| F-5b | Young ends at a skill total of 450.0 | no skill rule; time and murder only | Chase: time only; skill gain here runs about 15x stock (P15 D-92), so 450 would come in hours |
| F-5c | only "I renounce my young player status" | that, and "I want to grow up!" (any case, "!" optional), same confirm | Chase: an easier phrase; OSI's kept so the wikis stay right |
| F-5d | login countdown in hours | days and hours, plus how to end it sooner | 336 hours reads badly as a number |
| F-7a | (ours) guild membership, rank, rep, scrip, work orders, commissions per account | per character | Chase: characters on one account are separate play tests until F-4 |
| F-7b | no player reset | Reset Stone in New Haven and `[ResetMyAccount`, own account only | test-shard tool; removed at the live rebirth |

---

## 7. Found in passing

1. **The admin reset's slot loop** used `account.Count` (the number of characters) as the bound over slots
   (`ClusterFDevTools.cs:43` at `bb51fad`); pinned `Account.Count` is `:417`, `Length` `:444`. A character behind an empty
   slot was never found. Fixed (`Length`).
2. **Per-serial records outlive deleted characters** (exploration, starter records, now guild data). Harmless, small; a
   cleanup on deletion would be a later task.
3. **`ArtificersGuildmaster.cs` holds mojibake**: UTF-8 box-drawing characters decoded as cp1252 and saved again (for
   example line 41). Not touched here.
4. **AGENTS.md repo facts are stale:** "15 .patch + 5 replacements" in `server/patches`; counted now: **25 `.patch` and 5
   `.cs`** (23 at `bb51fad`).
5. **`[ResetGuild`** (GameMaster, `ClusterFGuildSystem.cs`) now resets the caller's character only; its description says so.

## 8. Not verified

- Nothing was run in a client: the gump layout, the stone's look and tooltip, the login line.
- What the test and live worlds already have on 3501,2575,14.
- That .NET refuses to set an initonly static by reflection was not tried here (section 2.2); not relied on.

## 9. For Chase to decide

1. F-1: the three decisions in section 3.6, then a prompt for the build.
2. Discoveries and encountered creatures: stay per account (recommended) or move per character (section 1.2).
3. Whether to add `[ClusterFSeedResetStone` to the console's World setup list, or set
   `clusterf.resetStone.seedOnWorldLoad` true on the test shard.

---

## 10. Checklist for Chase

1. **Commit** with `D:\UO\Commit-ShardWork.ps1`. This task's files are the 46 in section 4, including
   `docker/uo/apply-patches.sh`.
2. **Rebuild the test shard** from the console ("Rebuild through the gates"). The gate should say **304 passed**. At
   the first start the console prints "Cleared account-level guild data on N account(s)": every account's guild data on
   the test world is gone, as decided.
3. **On the test shard, as Administrator:** `[ClusterFSeedResetStone dryrun`, then `[ClusterFSeedResetStone`. The stone
   stands two tiles south-west of where new characters arrive. Then on an account with two characters:
   1. Character A joins a guild (for example the Warriors). Log in as B: B is not a member; the Guild Directory says
      "Member of 0".
   2. A says `[ResetMyAccount`; the gump shows three sections. Tick Guilds and Exploration; the confirm says "EVERY
      character". Confirm. A is no longer in the guild; B neither.
   3. Double-click the stone from 2 tiles: the same gump. From 3 tiles: "That is too far away."
4. **Young:** log in with a Young character. The login line reads "... for another N days and H hours of play time. Say
   "I want to grow up!" ...". Say `i want to grow up`: the renounce confirm opens; Cancel keeps Young.
5. **Craft X:** not built (section 3). The make-X that exists today is unchanged.
