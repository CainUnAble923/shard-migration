# cc-P610: the urgent fix-up drafts from P533, built

## In plain words

- All ten urgent fixes from the October review are in; two only partly, because the rest of each is owned elsewhere. They cover:
  - companions that could be traded away or go wild;
  - unraveling that could destroy gear you never approved;
  - tutorial loaners that could be kept or cut up;
  - tutorial purchases and vet fees charged with no one there;
  - Exodus, Void Pool and Underworld state lost or broken by a restart;
  - the Rootdeep entrance sending players into the void when the map is missing;
  - extra jewelry stuck in a locked slot;
  - the play-test page attaching an answer to the wrong question or losing what you were typing.
- Each fix has a test that failed before the fix and passes after it. The full gated build `sl-modernuo:cc-P610` is green.
- Two parts were left out on purpose: the tutorial island gate (prompt P477 already owns it) and the unravel recovery formula (it waits on your decision C4).
- For you: when the play-test service is next deployed, update its server and the shard-migration tools together. The new page refuses a "Taken into" from an old server, and the old page's button errors against the new one. Nothing else to do.

## What was built

| Draft | Done or skipped | Why / what |
|---|---|---|
| U1 Companions | Done | Companions can no longer be transferred or traded. They never lose loyalty (new pinned hook `BaseCreature-companion-loyalty.patch`). A weapon's damage split is read after load. Companions come back at login even while the system is disabled, and ones left out at a restart are put away. |
| U2 Unravel | Done, except part 4 | Approval unravels only the items the preview counted. Blessed items and anything behind a locked container are refused, and the container's ancestors are checked too. **Part 4 (shard recovery formula) skipped:** it waits on Chase's decision C4 ("For Chase"). |
| U3 Tutorial loans | Done | New loaner cloth, log, bow and arrow types that cannot be cut, chopped or kept. Split remainders are adopted and swept. A saved ledger returns tithing points and the Hiding base after a restart. Hiding is rounded to tenths. |
| U4 Tutorial services | Done, except part 4 | Guildmaster sales need a guildmaster within 4 tiles, room in the pack, payment, then delivery, with a bank refund if delivery fails. The vet checks before charging. The play-through driver fails on a missing pick or graduation box. **Part 4 (an unavailable tutorial cannot trap players) skipped:** queued P477 T1 owns the island gate. |
| U5 Exodus | Done | The exit resumes after a restart, with no second boss. The Asclepius healing bonus works (one-line pinned patch `Bandage-asclepius-bonus.patch`). A revealed chest is removed on load. The six rewards are worth 5,000 cleanup points. |
| U6 Void Pool | Done | Cauldron charges are saved (save version 1 plus a migration). Every improving player's best single score is recorded. The record battle keeps its score table. A load clears the old spawn before the first battle. |
| U7 Rootdeep entry | Done (narrowed, as P533 itself narrowed it after P411) | At startup without the map overlay, the saved way-down teleporters are switched off and marked, then switched back on, marked ones only, once the map is there. The ladder out stays on. The log counts characters saved inside, and nobody is moved. Refusing to start was rejected: a test shard may start without the overlay (`Start-TestShard.ps1`), and a refusal would stop the whole shard. A Young warning test was added (P504 #2). C16 (client map policy) stays For Chase. |
| U8 Decisions inbox | Done | An answer joins its question by the saved question text, not its place. Answers that lose their question are kept as "question gone or changed" cards, which are counted and included in the copy. Take and undo carry the answer revision, and a stale one is refused. Drafts survive chips, other saves and refreshes, with a Discard button. A real headless-browser test covers drafts and hostile text. |
| W3 Extra jewelry | Done | A locked slot shows its jewel with Remove. Equip rules and the item's own rules run, and a rank change or settings change refreshes the slot. Level gear, imbue effects, Fortune's Favor and the achievements all count active jewels. |
| A1 Mini champions and Underworld | Done | Repeated wrong guesses work (pinned `PuzzleChest-repeat-wrong-guess.patch`). Mini champion restarts are saved (a new `MiniChampRestarts` store) and a switched-off controller stays off. The magic key cleans nested bags, and only its own boards. The gem's start timer is cancelled on delete. Note: P476 W5 is not issued yet; when it is numbered, it should drop P491 #1-#4, which are built here. |

None of the ten was already done by a merged prompt or queued in the prompts repo (`queue\`, `waiting\`, `completed\` and `held\` were checked), apart from the two parts named above. None was wrong against today's code.

## Tests (each seen failing first, then passing)

- `server/tests/Mobiles/Companions/CompanionLifecycleVerification.cs` (U1): 6 red on the old code, then green. Probe: 267 Companion, Pet and Loyalty facts passed; the 3 skips are pinned's own.
- `server/tests/Misc/UnravelApprovalVerification.cs` (U2): 5 red. The guards and the exact yield were proven by a deliberate break.
- `server/tests/Tutorial/TutorialLoanLifecycleVerification.cs` (U3): 13 of 14 red; the 14th is the control.
- `server/tests/Tutorial/TutorialServicesVerification.cs` (U4): 8 red, 2 more proven by a deliberate break. `notes/cc-P480-tools/test_graduation_rewards.py`: 3 of 4 red on the old driver.
- `ExodusEncounterVerification.cs` (U5): 5 red, plus a preventive fact proven by a deliberate break. The `CleanUpBritanniaPointsVerification` count is now 477.
- `CovetousVoidSpawnVerification.cs` (U6): 4 red, plus a coverage fact proven by a deliberate break.
- `server/tests/Regions/RootdeepMapSafetyVerification.cs` (U7): the saved way down sent the player to 5193,1138 on the old code. The Young fact was proven by a deliberate break. 15 of 15 Rootdeep facts pass.
- `tools/tests/test_decisions.py` Identity, Revisions and PageDom (U8): 11 red on the old code, and headless Chrome reproduced the lost draft. The hostile-text check fails when the box's escaping is removed. 29 of 30 pass. The remaining one, RealFiles P378-4, fails identically on the old code: it comes from real triage data, not this work.
- `server/tests/Misc/AccessoryIntegrationVerification.cs` (W3): 8 red, plus 1 proven by a deliberate break.
- `server/tests/Services/UnderworldStateVerification.cs` (A1): 6 red, plus the old-save guard.
- Gated build: `docker/uo/build.sh -t sl-modernuo:cc-P610`. The result is in the last section.

## Changed tests and existing behaviour

- `test_decisions.py`: the old take test and two page-source checks now use the new API. A take or undo without `expect` is refused, which is the point of P509 #3.
- `test_play_who.py` and `test_decisions.py` take `SL_SHARD`, as their neighbours do. Before this override, one run of `test_play_who.py` read the main shard copy's queue server and page (read-only, nothing written). Its 2 RealFiles failures are the same on the old code.
- `TutorialFirstPlayVerification`: the elixir fact now places a guildmaster, because the elixir is sold in person.

## Pinned patches and their alternatives

- `BaseCreature-companion-loyalty.patch` adds a virtual `KeepsLoyalty`, and the loyalty timer skips the drain when it is true. Alternatives rejected:
  - `Commandable = false` would also block commands.
  - Topping loyalty up in `OnThink` doesn't run while the AI sleeps.
  - `Loyalty` is a generated field that can't be overridden.
- `Bandage-asclepius-bonus.patch`: pinned `BandageContext` computes the heal inline and has no hook.
- `PuzzleChest-repeat-wrong-guess.patch`: `SubmitSolution` is not virtual and its guess table is private.

## Gaps and follow-ups found in passing (not built)

- Void Pool `CheckAddTop20` looks wrong too: it adds an existing table, never the battle. A controller switched off mid-battle and then deleted throws in `EndInvasion`. Both are inherited and outside U6.
- P609's rewording breaks other text matches in `notes/cc-P480-tools/playthrough.py`: TITLES, Rook's heading, and the "Done" line. Outside U4.
- W3 F09: no new test covers the combined caps at the HCI, DCI, mana-cost and casting-speed consumers. P486 found no bypass there.
- U8 deploy: the shard-migration `tools/` and the queue server and page ship together (see In plain words).
- Under narrow probe filters, the Mule and League-shop facts fail on the plain image too. That's run order, not this work; the full gated build runs them.

## Gated build

`docker/uo/build.sh -t sl-modernuo:cc-P610`: green. All patches applied and 2451 shard tests passed (EXIT=0). The image carries VERSION 2026.10.25.4 and its CHANGELOG section.

P610 DONE
