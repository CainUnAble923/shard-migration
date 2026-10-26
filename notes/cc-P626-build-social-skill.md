# P626: Persuasion (Begging reworked), stage 1: identity, charity, and courier work

Written 2026-10-25 by the Iron Golem (Claude Code). Builds stage 1 of [cc-P606-begging-skill-design.md](cc-P606-begging-skill-design.md), Chase's option B (10-25 evening: haggling with audited price floors and exclusions, modest sale bonuses, diplomacy for standing rather than extra gold or Renown, earned skill gain; begging stays as the lowest use). Option B's six prompts begin with "(1) identity, charity, and novice work", and the design says prompt 1 "needs an actual repeatable training route, not a renamed button". This is that prompt. The other five are drafted as prompts at the end of this note.

## In plain words

- Begging is now called **Persuasion** on the server: the same skill, the same points, the same slot. Using it on a person opens a small menu with two choices for now: **Ask for help** and **Ask about work**. The client's skill list still says "Begging" until the player package's skill names are updated (a later stage).
- **Ask for help** is the old begging, kinder and capped. A townsperson gives a few coins from their own purse (up to 14 at a time) or, when they have none to spare, a loaf of bread. That is once per townsperson per day, and at most 50 gold and 2 loaves a day per account, shared by its characters. It no longer lowers karma. It only trains the skill up to 20, once per person who helps.
- **Ask about work** at any banker (or the Merchants' Exchange guildmaster) gives a sealed letter to hand in person (drag it onto them) to, for example, "a banker in Minoc". Beginners get an errand across their own town; higher skill sends letters farther. Each delivery is one training roll, and the ladder of letters reaches 200. This replaces endlessly begging from the same person as the way to train.
- For Chase: the image `sl-modernuo:cc-P626` is built and all 2,502 shard tests pass. Nothing is deployed. Two choices are noted below, neither blocking: courier letters pay no gold yet, and the Exchange's 500-gold joining task is unchanged. To try it, use Persuasion on a New Haven banker on the test shard.

## What changed (ShatteredLegacy, branch golem/Iron/P626)

| File | Change |
|---|---|
| `server/customizations/ClusterFPersuasion.cs` (new) | The skill's new handler, charity, the courier job board and the gain events, below. |
| `server/customizations/ClusterFExchangeLetter.cs` (new) | `ExchangeLetter`, the courier's sealed letter: a saved item (version 0). |
| `server/tests/Skills/PersuasionVerification.cs` (new) | 8 facts (16 cases), below. |
| `CHANGELOG.md`, `VERSION` | 2026.10.25.12: two Added and two Changed lines. I skipped .11 because P625 (not yet merged into this branch's base) uses it. |

No patch and no change to a pinned file. The skill button reaches the new handler because `ClusterFPersuasion.Initialize` carries `[CallPriority(100)]`. Pinned's `AssemblyHandler.Invoke` sorts every `Initialize` by that attribute (`Server/AssemblyHandler.cs:143`, default 50, higher runs later), so ours runs after pinned's `Begging.Initialize` and replaces the same callback. The first fact pins the attribute. (Correction to P625's notes: there I called the order between two `Initialize` methods unreliable. With `CallPriority` it is reliable. P625's patch is still a fine choice there, because it adds a menu beside a stock one rather than replacing a callback.)

### The rules as built

- **Name:** `SkillInfo.Table[Begging].Name = "Persuasion"`, as P239 did for Appraisal. `SkillName.Begging` (slot 6), saved Base, Cap, lock and modifiers are untouched. The client's own skill names come from the package's `skills.mul` copy (`Build-UoOverrides.ps1`, Build-Skills); that is client-package work for stage 6.
- **Use:** reveal; "Whom do you wish to persuade?"; target a living, human-bodied, uncontrolled, unsummoned non-player within 3 tiles and in sight. A valid target opens the Persuasion menu and sets a 10 s skill delay. A cancel or an invalid target releases the delay, as pinned's Begging does (`Begging.cs:163-171`).
- **Who can give charity:** a townsperson a spawner keeps (`Spawner` is an item), not controlled or summoned, human-bodied, and either a vendor or a creature that does not start fights (`FightMode` None or Aggressor). Their identity is the spawner plus their kind, so a respawned or replaced townsperson is the same contact, and a staff-made NPC gives nothing.
- **Charity amounts:** coins `floor((2 + 0.3 x min(S, 40)) x M)`, at most 14. S is effective skill clamped 0..200, and M is the design's karma factor (1 at neutral or good karma, 0.8 at -10000). That is further limited to a tenth of the giver's own gold and the account's remaining 50 for the UTC day; no gold is created. With no coins (empty purse, daily coins spent, or refused), one loaf of `BegFrenchBread` (one of the begging-marked foods P128 ported), up to 2 a day. One result per account, contact and UTC day, food and coins shared. A valid refusal or "nothing to spare" spends that contact's attempt; an invalid target spends nothing. The daily counts are account tags (`Persuasion.Charity*`), the way Fountain of Youth keeps its clock, so they survive a restart and are shared by an account's characters.
- **Karma:** asking never changes karma. Pinned's untrustworthy refusal (`Begging.cs:100-106`, the same chance formula) is kept for negative karma. It refuses coins only, and still calls `ClusterFJokeAchievements.BeggedUntrustworthy`, so the hidden "Not Trustworthy" achievement keeps working. The refused asker is still given bread when the day's bread allows (the design's "no refusal spiral").
- **Charity training:** one gain event per distinct contact that actually gave, below 20 Base only, on the window (-20, 20). Credited contacts are kept per account (account tag `Persuasion.CharityTaught`, the newest 200).
- **The courier ladder:** job difficulties 10, 35, 60, 85, 110, 135, 160, 185, 195 (the design's). The board offers the hardest one unlocked at `max(0, d - 25)`. Every delivery is one gain event on the window `d - 25 .. d + 25`, so every Base from 0 to 199.9 has a job whose window holds it (a fact checks all 2,000 values), and the 195 letter takes 199.9 to 200. The gain goes through the shard's normal pipeline (`ClusterFSkillGain.CheckSkillWornBonusIncluded`: its extra attempts, the lock, the cap, one `SkillUsed`). A positive worn bonus is added to both edges for this check only, as the design asks, so gear cannot end the window before Base does.
- **Where letters go:** at difficulty 10, a different kind of shopkeeper in the issuing town (`TownRegion`). From 35 up, a banker in another town on the same facet. From 110 up, a banker more than 1,000 tiles away where one exists. Never straight back to the previous destination. The board finds destinations from the world's vendors at the moment of asking, so it fits whatever towns a shard has. One letter at a time, 3 hours to deliver.
- **Delivering:** drag the letter onto the recipient (`Item.OnDroppedToMobile`), within 3 tiles. Only the courier it was issued to can deliver it; the wrong person, another player, a stale letter (torn up) or a replay gives nothing. The letter is deleted before its gain event, so nothing can teach twice. It is blessed, worth nothing to vendors, and staff can read and set its fields with `[props`.
- **Directions are free:** "Ask about work" anywhere else says "The Merchants' Exchange hires couriers. Ask any banker." There is no roll and no gain.
- **The thief trial:** "Ask for help" on your own tutorial practice person raises a successful Begging `SkillUsed` (the trial's step), with no coins, no bread and no skill. Stage 6 moves this lesson out of the thief trial as the design asks.
- **The old training route** is no longer reached from the skill button: pinned's `Begging.OnUse` (and its endless `CheckTargetSkill(Begging, 0, 100)`) stays in the build but only tests call it now. `ClusterFSkillGain`'s hook G row for that call (`ClusterFSkillGain.cs:354-356`) is left in place, dead for the game. Removing it means changing `SkillGainPastStockCeilingVerification` and `SkillGainRowKeysVerification`, which pin it. That cleanup is in the stage 6 draft.

## Tests: red first, then green

How I ran them: builder image `sl-uo-builder:cc-P625` (my previous gated build, same base `9cc69ca` plus P625's untouched files), with the two new customization files and the fact file bind-mounted, `dotnet test` filtered to `PersuasionVerification`. The script (`probe626.sh`), the stub, the mutants and every log are in the session scratchpad.

| Fact | What it pins |
|---|---|
| `TheSkillIsPersuasionAndItsButtonOpensPersuasion` | `Initialize` carries a CallPriority above 50. After pinned's `Begging.Initialize` and ours: the name is Persuasion, the slot is 6, and `UseSkill(Begging)` opens the Persuasion target with its line. |
| `CharityGivesCoinsOrAMealWithinTheDailyLimits` | 14 a time at 40 from a 500-gold purse (the purse loses exactly 14); the same contact once a day; 14, 14, 14, then 8 (the rest of 50); then two loaves, then "nothing to spare". A second character on the account gets nothing. A new day gives again. An empty purse gives bread. An unspawned NPC gives nothing and has no contact key. Karma unchanged. |
| `TheCoinCeilingFollowsSkillAndKarma` (7 cases) | 2 at 0; 5 at 10; 14 at 40 and 200; 14 at good karma; 11 at 40 and -10000 karma; 7 at 20 and -5000 karma. |
| `BadKarmaIsRefusedCoinsButStillFed` | At -15000: no coins, the untrustworthy line, one loaf, karma unchanged. |
| `CharityTeachesOncePerContactAndOnlyBelow20` | With every roll passing: 10.0 to 10.1; the same contact on a later day gives but does not teach; a new contact 10.2; 19.9 to 20.0; at 20 nothing more. |
| `TheCourierLadderCoversEveryBandTo200` | Spot values (0 gives 10, 10 gives 35, 100 gives 110, 199.9 gives 195), and every Base 0.0..199.9 lies inside its job's window. |
| `ACourierLetterGoesToTheRightPersonOnceAndTeaches` | Three test towns (Home, Near at 400 tiles, Far at 1,500). At 50: a difficulty 60 letter for "a banker in" another town; one at a time; refused at the wrong shopkeeper and from another player; delivered (deleted, 50.0 to 50.1); a replay does nothing; the next letter goes elsewhere. At 100: difficulty 110 and the far town. At 0: difficulty 10, "a provisioner in P626 Home", delivered for 0.1. A stale letter is refused and torn up with no gain. |
| `TheTopLetterTrainsTo200AndNothingPastTheCapOrWhenLocked` | Difficulty 195 at 199.9: 200.0. At 200 (cap 200): stays 200. Locked at 180: stays 180. |
| `OnlyTheExchangeHiresAndOnlyPeopleCanBePersuaded` | A provisioner gives directions and no letter. A player, a pet and an NPC 10 tiles off are refused; a shopkeeper beside you opens the menu. |
| `TheThiefTrialsPracticePersonStillCountsAndPaysNothing` | Through the real tutorial (enter, run the thieving trial station): "Ask for help" on the trial's mark marks the Begging step done, with no gold, no bread and no skill change. |

**Red on the old code:** a stub `ClusterFPersuasion` and `ExchangeLetter` with the same public names and no behaviour (the pinned Begging callback stays). 16 of 16 failed.

**Green:** 16 of 16, run three times as the facts grew (15 of 15 before the tutorial fact was added).

**Mutations of the finished code**, each run alone:

| Mutant | Result |
|---|---|
| m3: the letter is not deleted before its gain | red in the courier fact (a replay taught again) |
| m4: "never straight back" removed | red in the courier fact |
| m5: `[CallPriority(100)]` removed | red in the first fact |
| m6: a contact can teach again (the `Taught` check dropped) | red in the charity-teaching fact |
| m7: the once-a-day contact check dropped | red in the daily-limits fact |
| m1: the explicit "below 20" check dropped | stayed green: the gain window's top (20) already stops it. An equivalent mutant, so the check is belt and braces. |
| m2: the "50 gold left today" check dropped | stayed green: the coin amount is already limited by `50 - given today`, which is then 0, and bread follows. An equivalent mutant again. |

Two things the first runs found. Vendors come with a random purse (one banker had 623 gold where the fact expected 486), so the facts now empty a test townsperson's purse before giving them a known amount. Pinned's `Animate(AnimationType...)` overload does not exist in this pin, so the bow uses pinned Begging's own `Animate(32, 5, 1, true, false, 0)`.

**Gated build:** before launching I dropped the Docker VM's page cache (Windows had 4.2 GB available, 10 GB of it was VM cache; 11.3 GB after). I took the `docker-build` lock, ran `docker\uo\build.sh -t sl-modernuo:cc-P626` detached with its log on disk, and released the lock afterwards. It finished with EXIT=0: "Built sl-modernuo:cc-P626 with patches applied and 2502 shard test(s) passing". Of 2,506 tests, 2,502 passed and 4 were skipped (the real-map-data facts); none failed. All 16 Persuasion cases passed in it, and so did the existing Begging, tutorial and skill-gain facts. The images are `sl-modernuo:cc-P626` = `353c521d38b0` and `sl-uo-builder:cc-P626` = `fcec3bd8f53c`. The log is `build-P626.log` in the session scratchpad.

## Deviations and decisions for Chase

- **Shard-specific content** (an invented rework, not an OSI port): the design asks the overseer to register the departures from stock Begging in `docs/fidelity-principle.md` once approved. They are: the name; charity limits and no karma loss; the training route moved to courier work; and the untrustworthy refusal now refusing coins only.
- **Courier letters pay no gold.** The design says introductory jobs are free and names no fee. Paying gold for an unlimited, repeatable job would be a new faucet, and the design's economy audit (stage 2) is where any fee belongs. Recommendation: leave unpaid until stage 2 or 5 decides, or give a fixed small fee from the Exchange's own budget. Not blocking.
- **The Exchange's 500-gold initiation task** is unchanged. The design offers replacing it with a beginner courier job as an option; that is in the stage 6 draft.
- **Charity food** is `BegFrenchBread`, "Acquired by begging" on its properties. I did not audit every vendor's buy list for `FrenchBread` subclasses. If some vendor buys French bread by base type, charity bread could sell for a coin or two. That is in stage 2's audit list.
- **Who counts as a townsperson** is my reading of "willing ordinary civilian": a spawned vendor, or a spawned human that does not start fights. Escorts and townsfolk that a spawner keeps qualify. Guards (`BaseGuard` is not a `BaseCreature`) do not.
- **Two stray Docker volumes:** one probe run was started with relative file paths by mistake, and Docker created two empty named volumes, `ClusterFPersuasion.cs` and `ClusterFExchangeLetter.cs` (created 03:55:58Z). I inspected them and removed them at once; nothing else used them.
- **A finishing line written early in P625** (recorded in its own notes). Here the notes were written without it until everything was done.

## Unverified

- The menu, the letter's look (a hued blank scroll, 0x0E34) and drag-onto-NPC delivery in a real client. All standard, but nobody has seen them in a client yet.
- How many towns' bankers a real world gives the board (it reads the world's vendors when you ask). On a live map it should find every town bank on the facet; the facts use three test towns.
- Real training time per band. The design warns against promising one; the ladder is continuous, but how fast it feels is a playtest question.
- That every civilian spawner on the shard sets `Spawner` on what it spawns. Pinned's spawners do; hand-placed NPCs (some of our seeders) would not, and so give no charity, as the design intends for staff-made NPCs.

## Checks before handing over

`git diff --check` is clean in ShatteredLegacy, and the new files (both customizations, the facts, this note) are plain ASCII with no trailing whitespace. Nothing was committed, nothing was deployed, Haven was not touched, and no world or test shard was started. The Read tool worked this time; no step was skipped.

## Remaining stages, as prompt drafts for the overseer to number

These follow the design's option B order: (2) quote service and economy audit; (3) rumors and Lead completion; (4) requisition terms and standing payout; (5) calm encounters and the upper work ladder; (6) tutorial, compatibility, rewards, end-to-end proof. A seventh is reserved by the design if the store audits overflow prompt 2. `P<nn>` is for the overseer to fill in.

---

### Draft: Persuasion stage 2: haggling, with one quote for display and settlement, and the catalog audit

```
# CC task P<nn>: Persuasion stage 2: haggle at vendors (a per-player quote shared by display and settlement) and audit the catalogs

**Model:** Opus

**Touches:** server

**Summary:** Stage 2 of `notes\cc-P606-begging-skill-design.md` (option B, Chase 10-25), after P626's stage 1 (`notes\cc-P626-build-social-skill.md`). Adds Haggle to the Persuasion menu: from 20 Base, a successful haggle gives `min(20, S / 10)` percent off purchases and `min(5, S / 40)` percent on sales at that vendor for ten minutes, times the karma factor; at 200 Base, 30 percent off and 5 percent on sales are passive. Chase chose audited price floors and exclusions.

## The work

1. Read the design's "Haggling and economy limits" section and P626's notes. Build a per-player quote service: never write a personal discount into shared `GenericBuyInfo.Price` or `PriceScalar`. Buy display (the vendor buy list) and settlement must read the same quote; a changed quote at settlement needs confirmation. Apply once after existing adjustments; round costs up and payouts down; a paid line costs at least 1; stack splitting never improves a total. The larger of competing social discounts, never multiplied.
2. The catalog audit: classify every NPC vendor's buy and sell entries (pinned SB lists plus our custom stores) into participating and "Fixed price". Start excluded until audited: currency conversion, deeds with redemption value, refundable purchases, raw commodity loops, services, contract inputs, uncataloged custom stores. For each repeatable interchangeable item, the maximum NPC cash-out must stay at most 90 percent of the minimum discounted NPC acquisition cost across vendors, towns and reversible transformations (buy/sell, buy/melt/sell, buy/craft/requisition, salvage, empty containers). Withhold the discount where it fails. Write the audit table into the notes. Include P626's charity bread (`BegFrenchBread`) in the resale check.
3. Guild currency stores: discount each actual cost component independently, never a skill, membership, reputation or recipe requirement. If the audit is too big for this prompt, stop after the vendor half and say so; the design budgets a seventh prompt for that rather than weakening the check.
4. Training from trade: below 75 Base, at most one practice event per account, contact and day, after a successful haggle and an eligible trade of at least 100 gold at the undiscounted quote; buying and selling share it. Passive 200 shopping never trains. No call to `CheckTargetSkill(Begging, npc, 0, 100)`.
5. Red-then-green tests: quote and settlement equality, isolation between two players at one vendor, rounding and stack splitting, an excluded entry, a guild currency component, the 90 percent loop rule on a buy/sell and a buy/melt/sell, two characters on one account sharing the practice event, and the 200 passive discount ending when Base drops. Seen failing first; mutation evidence where a guard already passes.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG player lines.
7. Notes `notes\cc-P<nn>-persuasion-stage-2.md` with the audit table. Last line `P<nn> DONE`.
```

---

### Draft: Persuasion stage 3: rumors that attach a requisition Lead

```
# CC task P<nn>: Persuasion stage 3: Ask for rumors (a useful contact or place, and from 50 a requisition Lead)

**Model:** Opus

**Touches:** server

**Summary:** Stage 3 of `notes\cc-P606-begging-skill-design.md`. Persuasion adds specificity to directions: from 20 Base a named public contact or place, from 50 a rumor may attach one eligible Lead to an open requisition without one, using the existing Lead rules.

## The work

1. Read the design's "Rumors with a useful destination" and "Training that feels earned" sections, P626's notes, and `server/customizations/Requisitions/RequisitionLeads.cs` (35-45, 49-91, 165-204). Add "Ask for rumors" to the Persuasion menu at eligible contacts.
2. At 50+, attach one Lead to an existing open requisition with no live Lead, through the existing Lead creation (area, creature family, rank, expiry, drop rules unchanged). At 100 state the public route and family clearly; at 150 and 200 prefer a Lead fitting the chosen request and travel access. Never increase drop rates or promise a live spawn.
3. Limits: one attempt per account and contact per UTC day; at most three new Leads per account per UTC day; failures spend the contact's attempt, not a Lead slot; reopening shows the saved answer; never replace a live Lead; invalid or inaccessible destinations refused without spending. Account tags like P626's charity.
4. Training: no gain for the rumor itself; one practice event when the character completes the requisition that Lead served, through `ClusterFPersuasion.Practice` at a job-like difficulty. Not a second event if stage 4's terms also apply to that requisition (stage 4 must honour this).
5. Red-then-green tests: Lead attached through the real Lead code; limits per account across two characters; no replacement of a live Lead; no gain on asking; one gain on completion and none on a replay. Seen failing first.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG player lines.
7. Notes `notes\cc-P<nn>-persuasion-stage-3.md`. Last line `P<nn> DONE`.
```

---

### Draft: Persuasion stage 4: negotiated terms on requisitions, paid in standing

```
# CC task P<nn>: Persuasion stage 4: negotiate terms before a requisition, paid as extra guild standing

**Model:** Opus

**Touches:** server

**Summary:** Stage 4 of `notes\cc-P606-begging-skill-design.md`. Chase chose diplomacy for standing, not extra gold or Renown: from 50 Base, one terms discussion per requisition before turn-in records a prospective standing bonus of `min(10, S / 20)` percent, paid at turn-in in the same transaction.

## The work

1. Read the design's "Negotiating completed work" section, P626's notes and `server/customizations/Requisitions/RequisitionSystem.cs:220-273`, `RequisitionData.cs:31-66`. Add "Negotiate terms" to the Persuasion menu at a requisition's guild contact (or the requisition gump), from 50 Base.
2. One immutable terms result per request ID, saved with the request, decided before the item is submitted; a failure keeps the normal request; reopening, transferring or rerolling the board cannot retry it. Outcome chance `clamp((S - difficulty + 50) / 100, 0.05, 0.95)`, karma only through the contact's attitude (at most 10 points).
3. Payout inside the existing turn-in transaction: extra standing only (gold, Renown, items, access, deadlines unchanged), only with the genuine consumed item, at most the first three eligible negotiated completions per account per UTC day across guilds (reserve the slot when the quote shows), fractional remainder carried per character and guild, no minimum +1. Never for joining, apprentice rewards, donations, bought reputation, achievements or Custodians' cleanup rank.
4. Training: one practice event on the completed work that fulfils the recorded terms (also after a failed discussion, since the work was done), shared with stage 3's rumor event so one requisition never teaches twice.
5. Red-then-green tests: persistence across a save and load, no retry, payout and removal together, the daily three across two characters, the remainder carry (25 base at GM: 1 now, 0.25 carried), no payout without the item, one gain with rumor plus terms. Seen failing first.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG player lines.
7. Notes `notes\cc-P<nn>-persuasion-stage-4.md`. Last line `P<nn> DONE`.
```

---

### Draft: Persuasion stage 5: appeals for calm and the upper work ladder

```
# CC task P<nn>: Persuasion stage 5: a short appeal for calm, and authored upper-tier Exchange work

**Model:** Opus

**Touches:** server

**Summary:** Stage 5 of `notes\cc-P606-begging-skill-design.md`. Adds "Appeal for calm" against an explicit list of humanoids (50+) and wild animals (80+), and richer upper work (witness reports, invoice reconciliation, mediation) beside P626's courier letters, which already train to 200.

## The work

1. Read the design's "A short appeal for calm" and "Training that feels earned" sections and P626's notes. Appeal for calm: an explicit content list (not `Body.IsHuman`); 3 tiles, sight, visible, two uninterrupted seconds; on success the target stops pursuing and attacking the speaker for `2 + S / 50` seconds (at most 6); any offensive act by the speaker or their pets, or damage to the target, ends it; never on players, player pets, summons, bosses, champions, event creatures, uncalmable creatures or NPCs engaged with another player; guards excluded (P608). Two-minute shared immunity on the target and a 30 s speaker cooldown whatever the outcome. Animal Lore adds at most 10 points for animals. No gain from ordinary farmable animals.
2. Upper Exchange work: at least two new authored job kinds for the 110..195 tiers (for example a witness report collected from a named NPC, an invoice reconciled against a delivered shipment), using P626's letter and practice key pattern (one consumed job, one gain per distinct objective). Rotate contact pairs, avoid immediate repeats, and give a local low-risk alternative. Lawful and underworld variants with the same gain windows.
3. Red-then-green tests: the calm duration and every end condition, the exclusions, the immunity against a party chaining it, no gain from farm animals, each new job kind teaching once and never on a replay. Seen failing first.
4. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG player lines.
5. Notes `notes\cc-P<nn>-persuasion-stage-5.md`. Last line `P<nn> DONE`.

Animal calming is the first thing to cut if it competes with the Drover's Handbook or the bards; say so in the notes if it does.
```

---

### Draft: Persuasion stage 6: tutorial, client name, titles, achievements, and the end-to-end proof

```
# CC task P<nn>: Persuasion stage 6: the tutorial lesson, the client's skill name, titles and achievements, retire the old gain row

**Model:** Opus

**Touches:** server, client-package

**Summary:** Stage 6 of `notes\cc-P606-begging-skill-design.md`, the last of option B: everything players read says Persuasion, the lesson moves out of the thief trial, and the skill gets its titles and two cosmetic achievements.

## The work

1. Read the design's "Guild, titles, achievements, and tutorial" section and P626's notes. Client name: the player package's skill names (`Build-UoOverrides.ps1`, Build-Skills, as Appraisal was done) say Persuasion; package lock for any package build. Creation text (`CharacterCreation.cs:1018-1028`) and every Skills surface say Persuasion; the starter staff stays as flavor.
2. Tutorial: remove Begging from the thief trial's steps and skill loan (`TutorialTradeTrials.cs:150-165, 440-464`, `TutorialStations.cs:139-143`) without losing anyone's saved progress or graduation, and add a social lesson near the trade route: ask a relief contact for a meal, ask where work is, carry a practice letter to the Exchange contact, with a guaranteed demonstration and no real coins or permanent skill.
3. Retire the dead stock gain row: remove the Begging case from `ClusterFSkillGain` hook G and update `SkillGainPastStockCeilingVerification` and `SkillGainRowKeysVerification` accordingly (P626 left it in place, unreachable from the skill button).
4. Titles from Base, chosen rather than forced: Streetwise 50, Silver Tongue 100, Mediator 150, Master Negotiator 200. Achievements A Fair Deal (first real negotiated transaction) and Common Ground (ten distinct mediation jobs across three towns), cosmetic only, counting committed job IDs. Keep the hidden Not Trustworthy achievement as it is.
5. Optional for Chase: replace the Merchants' Exchange 500-gold initiation task with one beginner courier job, keeping its once-only reward. Ask Chase first (Ask-Chase.ps1) if it is not already decided.
6. End-to-end proof on a scratch shard under the test-shard lock (never Haven): a fresh character trains through charity to 20, then courier letters across two bands, haggles, takes a rumor Lead and a negotiated requisition; frames from the patched client.
7. Builds green: `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` and the client package if it changed. CHANGELOG player lines.
8. Notes `notes\cc-P<nn>-persuasion-stage-6.md`. Last line `P<nn> DONE`.
```

P626 DONE
