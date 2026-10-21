# cc-P280: the League Register, consolidation items, backpack upgrades and repair deeds

2026-10-21, the Copper Golem (Opus), branch golem/Copper/P280 of both repos. Prompt: `cc-P280-league-register-build.md`
(built from P179's design, `notes/cc-P179-league-design-pass.md`, with Chase's answers of 2026-10-21). Not committed (the
Golem commits). Both repos were clean at the start. Paused at Chase's request at a clean point: everything below is
built and green; see "Continuation".

## In plain words

- The League Registrar now hands out a **League Register** from Dull Copper: one book that holds your guilds (2 at Dull
  Copper up to all 18 at Celestial). Binding the Smith Guild Book or the Dispatch Ledger takes the book; you can take it
  back out free. Leave a guild and the Register shows it greyed out once, then drops it.
- The Register's **League actions** open with League rank: Bronze opens a bound guild's contracts from anywhere, Verite
  turns in every ready order at once, Blaze repairs everything you wear, carry and bank in one go.
- **League goods** for Renown and a little gold: a bigger backpack (150 / 175 / 200 / 250 items), the League Field Satchel
  (your four guild satchels in one slot) and the Combined Logbook. Smiths with Arms Lore can craft **repair deeds, repair
  kits and remote repair deeds** (Repair Items in the smithing menu).
- **For you:** look over the repair items' proposed numbers (below) and say if any should change; then play-test on the
  test shard (image `sl-modernuo:cc-P280`, steps under "For Chase"). The bank (answer 7) is still yours to decide.

## Headlines

- **Built:** the Register item and its window (Guilds, Ledger, League, Bank, Goods pages), issue and re-issue at the
  Registrar, bind and unbind with capacity by rank, live membership, the four League actions by rank, the backpack
  upgrades, C1 to C3, the three repair items and their crafting, Renown-plus-gold pricing. Every number is a setting.
- **Built on what exists, because P178 is still held:** only two guilds have a guild book today (smithing, mining). Those
  bind by giving the book up; every other guild binds by membership alone until P178 gives it a book. The Register shows
  each guild's status and contracts; P178's per-guild action lists slot into the Guilds page when P178 lands.
- **Answer 3 (F-34's ledger as the Bank page):** the page is F-34's base, which shows what the bank holds by kind. F-34's
  per-guild upgrades and range tiers (crafting from the bank) are unchanged and not built here; they are F-34's own build.
- **Answer 7 (bank):** nothing built, as asked.
- **Tests:** 17 new cases in `LeagueRegisterVerification`, every one seen failing under a deliberate break; the gated
  build is green at **2,069 of 2,069** and the runtime image `sl-modernuo:cc-P280` is built.

## What changed (ShatteredLegacy)

| File | What |
|---|---|
| `server/customizations/LeagueRegister/LeagueRegisterSettings.cs` (new) | every number as `clusterf.leagueRegister.*`; ranks written as metal keys, resolved on the generated ladder; `CapacityAt` |
| `server/customizations/LeagueRegister/LeagueRegister.cs` (new) | `LeagueRegisterSystem`: the bindable books (`Books`), `Issue` (re-issue deletes the old copy), `IsCurrent`, `DropLeft` (answer 9), `RefuseBind`/`Bind`/`Unbind`, `ActionRank`/`RefuseAction`, `OpenContracts`, `TurnInAll`, `RepairAll`; the `LeagueRegister` item (blessed, bound to its owner, a replaced copy crumbles) |
| `server/customizations/LeagueRegister/LeagueRegisterGump.cs` (new) | the window's five pages; `LeagueBank.Summary` (the Bank page) |
| `server/customizations/LeagueRegister/LeagueBackpack.cs` (new) | the backpack tiers, written to the pack's saved `MaxItems` at world load, login and purchase (as `ClusterFBankLimit` does the bank); `LeaguePrice` (Renown then gold, all or nothing) |
| `server/customizations/LeagueRegister/LeagueConsolidation.cs` (new) | C2 `LeagueFieldSatchel` (one item toward the pack whatever it holds; one satchel per kind; merge fee in that guild's currency), C3 `CombinedLogbook` and its gump, and their purchases |
| `server/customizations/LeagueRegister/LeagueRepair.cs` (new) | the repair pass, `FieldRepairDeed`, `FieldRepairKit`, `RemoteRepairDeed`, and their Blacksmithy entries (group "Repair Items") with Arms Lore as a second required skill |
| `server/customizations/ClusterFAccountData.cs` | `CharacterLeagueData` v2: `RegisterGuilds`, `RegisterSerial`, `PackTier`; v1 read branch |
| `server/customizations/GuildContractLedgerGump.cs` | the work-order turn-in moved into a public static `TurnIn` (behavior unchanged) so the Verite action uses the ledger's own code |
| `server/customizations/LeagueRegistrarGump.cs` | "League Register" on the Citizen Status row (button 29) |
| `server/tests/Misc/LeagueRegisterVerification.cs` (new) | 17 cases |
| `server/tests/Mobiles/Mule/MuleVerification.cs` | its `CharacterLeagueData.CurrentVersion` assertion 1 -> 2 |
| `CHANGELOG.md`, `VERSION` | 2026.10.21.18 (the .17 section was already committed) |

No pinned patch: everything is customizations.

## Every number, as a setting (`modernuo.json`, `clusterf.leagueRegister.`)

| Setting | Default | From |
|---|---|---|
| `issueRank` | DullCopper | answer 2 |
| `capacity` | `DullCopper:2,Bronze:4,Verite:6,Blaze:9,Mythril:12,Celestial:18` | answer 2 |
| `action.status` / `action.contracts` / `action.turnIn` / `action.repair` | DullCopper / Bronze / Verite / Blaze | answer 4 (Mythril and up reserved) |
| `satchel.rank`, `satchel.renown`, `satchel.gold`, `satchel.mergeFee` | Bronze, 5,000, 500, 50 | answer 5 (gold: answer 8, proposed) |
| `logbook.rank`, `logbook.renown`, `logbook.gold` | DullCopper, 500, 50 | answer 5 (gold proposed) |
| `backpack.tiers` (`Metal:items:renown:gold`) | `Bronze:150:2000:200,Verite:175:6000:600,Blaze:200:15000:1500,Mythril:250:30000:3000` | answer 6 (gold proposed: a tenth of the Renown) |
| `repair.deed.armsLore`, `repair.deed.ingots` | 90, 5 | proposal |
| `repair.kit.armsLore`, `repair.kit.charges`, `repair.kit.ingots` | 110, 10, 30 | proposal |
| `repair.remote.armsLore`, `repair.remote.ingots`, `repair.remote.gems` | 120, 20, 1 star sapphire | proposal |
| `repair.points` | 0 (repairs to full) | proposal |

The craft thresholds and materials are read when the craft table is built (server start); the rest on each use.

## The repair item proposal (for Chase)

| Item | Crafted with | Does |
|---|---|---|
| Field repair deed | Blacksmithy 60, **Arms Lore 90**, 5 iron ingots | one use: repairs one damaged item worn or in the pack, to full |
| Field repair kit | Blacksmithy 80, **Arms Lore 110**, 30 iron ingots | **10 charges**, each repairs one item; an item already whole costs nothing |
| Remote repair deed | Blacksmithy 90, **Arms Lore 120**, 20 iron ingots, 1 star sapphire | one use: the Blaze League repair, for a player below Blaze: everything worn, carried and in the bank box |

Why these: Arms Lore 90 / 110 / 120 sit on cc-P226's ladder (Arms Lore now trains to 200 and carries repair), so the deed
is a Grandmaster-ish smith's product and the remote deed needs real Arms Lore past 100. Repairs go to full with no loss of
maximum, like a smith's repair: the crafter's ingots and skill paid for it. "Tools" are covered where they wear: harvest
tools are weapons in pinned and repair like gear. Guild tools that count uses instead of durability (the Hammer of
Hephaestus) are not touched; their guilds restore them as before, and P178 is to price that cheaply.

## Choices made where the answers left room

1. **Binding without a book.** Only smithing and mining have a guild book today. Other guilds bind by membership, so the
   capacity ladder means something now; when P178 gives them books, binding can ask for the book.
2. **A book holding deeds is refused** ("Empty the book first"), so binding never destroys a player's deeds.
3. **Live membership (answer 9):** the open that finds a guild you have left shows it greyed "(dropped)" and frees its
   slot at once; the next open does not list it. No book comes back (you are not a member), nothing is refunded.
4. **Verite turn-in:** every bound guild's ready work orders (the ledger's own turn-in), and with the Society bound, every
   complete smith deed in the pack, paid the Society's way by the member's setting ("ask" banks).
5. **Blaze repair** covers the bank as well as worn and carried gear: "remote" repair.
6. **League Field Satchel:** the guild satchels keep their own code inside it, because the code that fills them searches
   the whole backpack. Taking one out is free, putting one in costs the merge fee (50 of that guild's currency).
7. **The Combined Logbook** deletes the two old logbooks on purchase; both only read the account's records, so nothing is
   lost.
8. **Gold as the small second cost** (answer 8): a tenth of the Renown for the backpack steps, 500 for the satchel, 50 for
   the logbook. All settings.

## Tests

`server/tests/Misc/LeagueRegisterVerification.cs`, 17 cases:

| Fact | Red (break) |
|---|---|
| Issued from Dull Copper, not below; a re-issue deletes the older copy | R1 (issue gate open) |
| Binding takes the book, unbinding gives a fresh one; refusals (not a member, no book, deeds in the book) | R2 (book kept) |
| Capacity 0/2/2/4/4/6/6/9/9/12/12/18 across the ladder; a full Register refuses, a promotion makes room | R3 (flat 18) |
| Each League action's rank gate (four) | R4 (gates open) |
| Bronze opens a bound guild's contract ledger, not at Dull Copper | R4 |
| Verite turns in two complete smith deeds at once and pays Seals; not at Bronze | R4, R5 (deeds skipped) |
| Blaze repairs worn, carried and banked gear; not at Toxic | R4, R6 (bank skipped) |
| Backpack: 150 at Bronze for 2,000 Renown and 200 gold; weight and lifetime Renown unchanged; Verite's step refused at Bronze; 250 at Mythril; restored at login | R7 (tier not written) |
| Repair deed (one item, consumed), kit (10 charges, one item each, a whole item costs nothing), remote deed (pack and bank) | R8 (no charge spent), R6 |
| Crafting each repair item needs its Arms Lore (three cases: 89.9 refused, at threshold allowed) | R9 (no Arms Lore requirement) |
| A guild left is shown once and dropped, its slot freed | R10 (never dropped) |
| League data v2 round trip, non-empty; a v1 record loads with none | R11 (tier not written) |
| The Field Satchel counts as one item and charges the merge fee; one per kind, satchels only | R12 (counts passed up) |
| The Combined Logbook takes both logbooks, at Dull Copper, for 500 Renown | R13 (old logbooks kept) |
| The Bank page counts ingots, gold (bank checks too), boards | R14 (checks not counted) |

**Build record** (the gated build script, `-t sl-modernuo:cc-P280`, under the docker-build lock, released after; logs
`p280-*.log` in the session scratchpad):

| Run | Result |
|---|---|
| 1 | patch gate: `AOS-set-attribute-aggregation.patch - present ... but never applied` although the log shows it applied: a flake in `apply-patches.sh`'s bookkeeping (see below), not this branch's change; next run passed it |
| 2-4 | compile fixes (two `using Server.Gumps`; P168's `BulkOrderGuildPay` is not on this branch, so the smithing key is written out) |
| 5 | 2,068 of 2,069: the Blaze fact's `EquipItem` refused the sword in the test host; the fact now places it with `AddItem` (the equip checks are not what it tests) |
| 6 | **2,069 of 2,069** |
| red | breaks R1-R14 (`breaks280.py` in the scratchpad): all 17 new cases failed. Two unrelated tests also failed once (`CovetousVoidSpawnVerification`, a gargoyle assassin placed at 5500,1807; `HighSeasFishingVerification`, an award roll), both random-spawn tests outside this code, green in every other run |
| green + image | breaks reverted (no `BREAK` left, checked): **2,069 of 2,069**, "Built sl-modernuo:cc-P280" |

**The patch-gate flake, for whoever owns `docker/uo/apply-patches.sh`:** the "every patch accounted for" loop runs
`printf '%s' "$HANDLED_PATCHES" | grep -Fxq "$name"` under `set -o pipefail`. When `grep -q` exits on an early match while
`printf` is still writing the (now long) list, `printf` gets SIGPIPE and the pipeline fails, so an applied patch is
reported as never applied. `grep -Fxq "$name" <<< "$HANDLED_PATCHES"` has no pipe. Not changed here (outside P280).

## Deviations and decisions for Chase

- **P178 is held**, so the Register cannot show each guild's own action list yet; it shows status and contracts per guild,
  and the cross-guild League actions. Binding without a book (above) is a stand-in until P178.
- **F-34's crafting from the bank is not built**: the Bank page is its base (what the bank holds). Its per-guild upgrades and
  range tiers stay as designed.
- **The bank (answer 7):** nothing built.
- **The window is not on P177's template** (not approved yet); it uses the League Shop's frame, one method per page.
- **The repair items' numbers** are a proposal (table above).

## For Chase

Start the test shard from `sl-modernuo:cc-P280` (it has no client art or text changes, so no package is needed).

- **P280-1, the Register.** A League citizen at Dull Copper (`[props` LeagueRank 2): League Registrar, "League Register".
  Pass: a blessed "League Register" in the pack. Press it again: the first copy is gone.
- **P280-2, binding.** In the Society of Smiths with an empty Smith Guild Book: Register, Guilds, bind the Society. Pass:
  the book is gone, the guild is listed "1 / 2". Unbind: a fresh book returns.
- **P280-3, capacity.** Join three guilds at Dull Copper: the third cannot bind ("holds 2"). LeagueRank 5 (Bronze): it can.
- **P280-4, League actions.** League page at Dull Copper, Bronze, Verite, Blaze: each action turns from red to available
  at its rank. At Bronze press Contracts on a bound guild; at Verite with two finished smith deeds press "Turn in every
  ready order"; at Blaze with damaged gear worn, in the pack and in the bank press "League repair".
- **P280-5, goods.** Give Renown (`[props` on the account data) and gold: buy the backpack steps at their ranks and check
  you can now carry 150 items; buy the Field Satchel and drop your ore satchel into it (needs 50 Compact currency); buy
  the Combined Logbook.
- **P280-6, repair items.** A smith with Arms Lore 90 / 110 / 120: Repair Items in the smithing menu; use a deed, the kit
  (count its charges) and a remote deed.
- **P280-7, leaving.** Bind a guild, `[ResetGuild <key>` on the character, open the Register: the guild shows greyed once.

## Continuation

Paused at Chase's request (Golem nudge during the red run). The step in hand was finished: breaks reverted, the gate
green, the image built.
- **Done:** every part of the prompt and its "Done means" (tests, CHANGELOG, these notes with every number as a setting and
  the repair proposal).
- **Left:** nothing of P280's own scope. Follow-ups, in the continuation prompt `cc-P372-cont-league-register.md`: Chase's
  answers on the repair numbers and the bank, the play tests above, and wiring P178's per-guild books and actions into the
  Register's Guilds page once P178 is built.
- **Mid-flight:** nothing.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`. Code: 13 files pending (6 changed,
the `LeagueRegister\` folder's 6 new files, the new test). Docs: this note. Neither BLOCKED; no file over 5 MB; scratch
(logs, `breaks280.py`, the pinned source copy) is in the session scratchpad, outside both repos. The continuation prompt
is in `D:\UO\cc-prompts\queue`, outside both repos.

```
Repo Result
---- ------
code dry run
docs dry run
```

P280 PAUSED
