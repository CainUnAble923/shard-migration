# cc-P376: the League's contradictions, as a decision sheet

2026-10-21, the Crystal Golem (Claude Code cloud session, GitHub only). Branch `golem/Crystal/P376` of shard-migration.
Sources: P374's guide draft `notes/wiki-drafts/league.md` (its "Differences and contradictions found" list, lines
157-165) and `notes/cc-P374-league-player-guide-draft.md`, both on `main` (merge 341e651). Code read at
shattered-legacy-infrastructure `origin/main` 47b3eae. Nothing in code or `docs/` was changed. All code paths below
are under `server/customizations/` unless they say otherwise.

P374 lists **9** contradictions (counted: 9 bullets, `league.md:157-165`), so there are 9 questions. Each one keeps
what is built unless the design clearly says otherwise. Answering a question changes no code; most answers only
say which line of `docs/feature-queue.md` (or `docs/league-storyline.md`) is history.

## The questions for Chase

**Q1. Which ranks hold story chapters 4 and 5: Blaze and Mythril (ranks 12 and 15), or "every third rank" (Toxic 11
and Obsidian 14)?**
- A. Blaze and Mythril, by name, as built. "Every third rank" is old wording.
- B. Toxic and Obsidian, so the chapters fall every third rank. It is a settings change (the ladder file), but the
  storyline names Blaze and Mythril.
- C. Blaze and Mythril, and also move the other things that step every third rank (requisition tiers, guild-rank
  bands) to match them.
- **Recommend A.** Your decision named the metals, the code and the storyline table use them, and the ranks that step
  every third rank today only gate other things, so they can stay.

**Q2. How many story chapters: six or five?**
- A. Six, Dull Copper to Celestial (as built: five blade pieces plus the ring).
- B. Five.
- **Recommend A.** "Five trials" is left over from before you said the story runs to Celestial. The code has six
  chapter waivers.

**Q3. Do League bonuses step at every rank or only at the six milestones?**
- A. Only at milestones, as built for the bank (+100 items per milestone, 1,000 to 1,600). The "per rank" lines in
  F-19 and F-25 are history.
- B. Every rank.
- **Recommend A.** You decided this on 2026-10-03 and the bank is built that way. The BOD and job-cap bonuses are not
  built yet. When they are, they use the same milestone count.

**Q4. Citizen Commissions: the design's "Steel" and "Silver" ranks are not on the ladder. Which ranks get the posting
permissions?**
- A. P47's mapping, with the milestones as now numbered: accept at Iron, small posts at Bronze, larger posts at Verite
  ("Steel"), public and high-value posts at Blaze ("Silver"; rank 12, not P47's 11).
- B. Leave it open until the Citizen Commissions build prompt is written.
- C. Another mapping.
- **Recommend A** as the default for the build prompt. Nothing about commissions is built, so nothing changes now.

**Q5. Is the Renown shop delivered? The notes still say "nothing spends Renown".**
- A. Yes: the League Shop (P229), the Hall page (P243) and the backpack upgrades (P280) all spend it. F-13's "nothing
  spends it yet" and the same line in P47, P75 and P179 are history.
- B. No, something is still missing (say what).
- **Recommend A.** Three spenders are built.

**Q6. What should players be told about the AP total and the number of titles?**
- A. Neither, as P374's draft does. List the eight titles anyone can see by name, keep the four hidden ones secret,
  and drop F-13's "2,505 AP".
- B. Publish an AP ceiling and a title count.
- **Recommend A.** Both numbers have changed twice and will change again. The code now has 12 titles (8 visible, 4
  hidden) and 2,575 AP, by my own count. The 2,505 and the 1,955 are each out of date. One point for you: the visible
  achievements give only 1,110 AP, so the 1,000 and 1,750 AP tiers need hidden achievements.

**Q7. Requisitions and Leads were built with three changes from F-47 and F-48. Do you accept them as the design?**
1. A request with a live Lead stays through the daily refresh.
2. "Double drop chance" became an extra roll, with a guarantee by the 40th qualifying kill.
3. A qualifying kill is decided by area, creature group and at least 1,000 Fame, not by "its loot table can roll the
   item".

- A. Accept all three. F-47 and F-48 become "built (P150), as changed".
- B. Accept some (say which).
- **Recommend A.** All three are built and tested. P150 explains why the loot-table test cannot work here.

**Q8. A non-member who fills a requisition gets that guild's standing at once. F-24 says League jobs bank it until the
Apprentice task. Which rule do requisitions follow?**
- A. Pay at once, as built. Banking stays a rule for the job board only, which is not built.
- B. Bank requisition standing too, until the Apprentice task.
- **Recommend A.** Your 2026-10-03 answer kept existing non-member payouts and limited banking to League jobs.
  Non-members only get the lowest tier (40 standing). One side effect to know about: in a guild without a promotion cap,
  that standing counts toward rank as soon as they join.

**Q9. P75's utility rewards: the League Warehouse (more bank), Featherweight satchels (less weight) and dropping the
Clockwork Scavenger. Which survive?**
- A. Drop the Warehouse and Featherweight. The bank grows only by milestone, and weight belongs to the guild satchels.
  The Scavenger stays the League's auto-loot reward, as F-33 Option A says.
- B. Drop all three, as P75 proposed for the Scavenger.
- C. Keep all of them for later.
- **Recommend A.** Neither the Warehouse nor Featherweight is built. You said "weight is not sold" for P280, and P179
  showed the bank would be sold twice. Your bank answer (P179 question 7) is still open, and this answers it. The
  Scavenger is your 10-05 decision and only P75 argued against it, so it stays until you drop it.

---

## Evidence

Line numbers are for shattered-legacy-infrastructure 47b3eae and shard-migration 341e651.

### Q1: milestone rank numbers

- The ladder is generated from the metal enum, numbered from 1: `ClusterFLeagueRanks.cs:146-157` (`Generate`,
  `ladder.Count + 1`). The enum order is `ResourceInfo.cs:9-27`: Iron 1, Dull Copper 2, Shadow Iron 3, Copper 4,
  Bronze 5, Gold 6, Agapite 7, Verite 8, Valorite 9, Platinum 10, Toxic 11, Blaze 12, Frost 13, Obsidian 14,
  Mythril 15, Adamantium 16, Celestial 17. Dawnstone comes next (`:31`) and is excluded (`ClusterFLeagueRanks.cs:121`).
  Counted from the enum: **Blaze is 12 and Mythril is 15.**
- Chapters by name in the default table: `ClusterFLeagueRanks.cs:485-504`. Dull Copper ch1 (`:488`), Bronze ch2
  (`:491`), Verite ch3 (`:494`), Blaze ch4 (`:498`), Mythril ch5 (`:501`), Celestial ch6 (`:503`). The header says so
  too: `:25-27`.
- The table can be overridden by `Configuration/league-ladder.json` (`ClusterFLeagueRanks.cs:21-23`, `:477-479`).
  Whether Haven's copy differs from the defaults cannot be checked from GitHub (needs the game PC or Haven).
- Sources that disagree: `docs/feature-queue.md:1986-1988` ("every third rank from Dull Copper", then names Blaze and
  Mythril). `docs/league-storyline.md:32` and `:49` still say "every third rank", but its table says Blaze (12) and
  Mythril (15) (`:57-58`). P47 says Blaze 11 and Mythril 14 (`notes/cc-P47-league-research.md:157`). P48 built by name
  and asked this question (`notes/cc-P48-league-batch-1.md:28-34`, `:296-298`). I found no answer to it.
- Things in code that step every third rank (rank 2, 5, 8, 11, 14, 17), not at the named milestones:
  - Requisition League gate: Bronze 5, Verite 8, **Toxic 11**, **Obsidian 14** (`Requisitions/RequisitionTable.cs:230-235`).
  - Loot-box tier on promotion: bands of three ranks (`LootBoxes/ClusterFLootTable.cs:130`).
  - Guild requirements in the ladder: Journeyman from Verite 8, four guilds from Toxic 11, Master from Obsidian 14
    (`ClusterFLeagueRanks.cs:494-501`; P48 `:296-298` notes the misalignment).
  
  Option C would move these. Option A leaves them, because nothing requires them to match the chapters.

### Q2: chapter count

- Built: `ChapterCount = 6` (`ClusterFLeagueRanks.cs:123`), with six waiver settings
  `league.trialsWaivedUntilBuilt.chapter1..6`, all `true` by default (`:184`, `:198`, `:206-208`).
- Sources: `docs/feature-queue.md:1987-1988` says six chapters; `:1989` says "the five trials". The storyline
  (`docs/league-storyline.md:32-33`) has six chapters, "the five pieces of the blade, then the ring", which is
  probably where "five" came from.

### Q3: per-rank or per-milestone bonuses

- Built: bank `BaseItems = 1000` (`ClusterFBankLimit.cs:26`), `ItemsPerLeagueMilestone = 100` (`:32`), bonus = 100 x
  milestones reached (`:46-47`). Milestones counted in `ClusterFLeagueRanks.cs:256-268`. Six milestones, so 1,600 at
  Celestial.
- Not built: no BOD cap or League job cap reads League rank. The only places that read it outside the ladder and
  bank are requisitions and loot boxes (grep of `GetRank(` / `LeagueMilestones` / `LeagueRank` across
  `server/customizations`: `Requisitions/*`, `LootBoxes/*`). The smith commission caps are fixed at 3 small and 1
  large (`ClusterFSmithCommissions.cs:454-456`).
- Sources: per rank in `docs/feature-queue.md:1660`, `:1674` (F-19), `:1951` (F-24 job cap) and `:2063-2064` (F-25).
  Your 2026-10-03 decision replaces them: `:2002-2005` ("Replaces F-24's '+1 per League rank' job cap and F-25's '+2
  small, +1 large per League rank'"). F-19 was never marked as changed.

### Q4: commission posting permissions

- Nothing about Citizen Commissions is built. `RenownSource.Commission` exists (`ClusterFAccountData.cs:678-679`) and
  never counts toward rank (`:663`), but nothing calls it (`Imbuing/ClusterFImbueEffects.cs:23`, `:450`: "nothing pays
  RenownSource.LeagueJob or .Commission yet"; requisitions now pay `LeagueJob`, below).
- Sources: `docs/feature-queue.md:2016-2017` ("map them to ladder ranks when specified"). P47's mapping:
  `notes/cc-P47-league-research.md:611-619` (Steel to Verite 8, Silver+ to "Blaze (11)", which is Toxic by the enum;
  Blaze is 12). Posting limits use the same names, `:608`.

### Q5: Renown spenders

- Built spenders of `SpendRenown` (`ClusterFAccountData.cs:666-671`, balance only; lifetime never drops):
  - `LeagueShop/LeagueShop.cs:173` and `:198` (shop rows, including the Hall page; `LeagueShop/LeagueHall.cs:5` says it
    pays through `LeagueShop.Purchase`);
  - `LeagueRegister/LeagueBackpack.cs:177` (P280 backpack upgrades; tiers in `LeagueRegister/LeagueRegisterSettings.cs:55`).
- Stale lines: `docs/feature-queue.md:1300-1301` (F-13, "nothing spends it yet"). F-13 has no "delivered" note
  (`:1288-1385`). P47, P75 and P179 also say there is no spender; those notes are dated and predate P229.

### Q6: AP total and titles

- **AP, counted:** every `Reg(` call in the four files that define achievements (`ClusterFAchievements.cs:427-1219`
  calls `RegisterJokes`, `RegisterAccessories`, `RegisterNoted` at `:1216-1218`). I parsed each call for `ap:`,
  `hidden: true` and `retired: true`. Not run in a game; the build's own fact prints the runtime figure
  (`server/tests/Misc/LeagueShopVerification.cs:388-390`).

  | File | Live | AP | Visible (AP) | Hidden (AP) | Retired |
  |---|---|---|---|---|---|
  | `ClusterFAchievements.cs` | 73 | 1,955 | 56 (1,110) | 17 (845) | 6 |
  | `ClusterFJokeAchievements.cs` | 16 | 130 | 0 | 16 (130) | 0 |
  | `Accessories/AccessoryAchievements.cs` | 5 | 65 | 0 | 5 (65) | 0 |
  | `ClusterFNotedBySystem.cs` | 45 | 425 | 0 | 45 (425) | 0 |
  | **All** | **139** | **2,575** | **56 (1,110)** | **83 (1,465)** | **6** |

  Retired (not counted): `skills.grandmaster` `:532`, `skills.paragon` `:726`, `skills.triple_grandmaster` `:766`,
  `skills.mining_legend` `:788`, `skills.smith_legend` `:810`, `skills.magery_legend` `:832` (in `ClusterFAchievements.cs`).
  P229's 1,955 (`LeagueShop/LeagueShop.cs:328`, P229 notes `:175`) is exactly the first file. P231, P262 and P263
  added the other three files later. F-13's 2,505 (`docs/feature-queue.md:1334`) came from 74 achievements before
  cc-P55 retired six.
- AP is per account (`ClusterFAccountData.cs:38`) and the shop tiers go up to 1,750 (`LeagueShop/LeagueShop.cs:118`).
  Visible achievements total 1,110 AP, so the 1,000 and 1,750 tiers need hidden ones.
- **Titles, counted:** `LeagueShop/LeagueShop.cs:330-345`, 12 entries: 3 bought (`:332-334`), 5 free by AP at
  100/250/500/1,000/1,750 (`:335-339`), 4 `HiddenUntilHeld` (the Unshod `:340`; Larry, the Supervisor, the Brave
  (citation needed) `:342-344`). P229's "nine" (`notes/cc-P229-league-reward-shop.md:30`) and "eight" were both
  written before the hidden four. Today the picker shows 8 until a hidden one is held.
- By the way: P229 removed a 2,500 AP title because nobody could reach it. With 2,575 AP now, it could be reached,
  but only by earning nearly every hidden achievement. Not a question, just something to know before raising a tier.

### Q7: requisitions and Leads as built

- Refresh keeps live-Lead requests: `Requisitions/RequisitionSystem.cs:3-6`, `:134`
  (`RemoveAll(e => force || !e.LeadLive(now))`).
- Extra roll plus pity: `Requisitions/RequisitionLeads.cs:11-15`, `:210-218` (100 percent at `PityKills`). Defaults
  are 3 days, 40 kills, Fame 1,000 (`Requisitions/RequisitionTable.cs:71-73`). Extra-roll chance by Fame band is 2 /
  5 / 10 / 20 percent (`:75-80`).
- Qualifying kill by area, group and Fame: `Requisitions/RequisitionLeads.cs:5-10` (with the reason the loot-table
  test cannot work: pinned generates loot at spawn) and `:182`.
- Sources: `docs/feature-queue.md:3348` (daily refresh), `:3378` (2x plus pity), `:3387` (loot-table test). Neither
  F-47 nor F-48 is marked built (`:3332-3393`). P150 and P203 notes record the build.

### Q8: non-member standing

- Turn-in pays Renown as `LeagueJob` (counts toward rank) and standing through `AddReputation` straight away
  (`Requisitions/RequisitionSystem.cs:248-249`; header `:9-12`: "paid to a non-member too: nothing banks for
  non-members yet"). `AddReputation` has no membership check (`ClusterFAccountData.cs:973-974`). No banking code exists
  (no `Banked`/`Pending` reputation anywhere in `server/customizations`).
- Non-members roll tier 0 (`RequisitionSystem.cs:7`, `:108`), and tier 0 pays 10 Renown and 40 standing
  (`Requisitions/RequisitionTable.cs:239`).
- Rank comes from standing, plus the Apprentice bump, without the Apprentice task being required to count the standing
  (`ClusterFGuildSystem.cs:662-673`). The promotion cap applies only to tracked craft guilds (`ClusterFGuildPromotion`,
  cc-P78). So standing earned before joining counts toward rank at once in other guilds. F-24 wanted it held until the
  Apprentice task (`docs/feature-queue.md:1963-1966`).
- Your scope ruling: `docs/feature-queue.md:2008-2009` ("Existing payouts to non-members stay as they are ...
  Banking applies to League jobs only."). Requisitions were designed after this (F-47, 10-16), so the ruling does not
  name them. That is why this is a question.

### Q9: utility rewards

- Warehouse: not built. The only bank growth is the milestone bonus (`ClusterFBankLimit.cs:40-47`). P179 recommends
  no purchase (`notes/cc-P179-league-design-pass.md:71-72`, `:232`, `:244`). Your answers for P280 left the bank
  open: "7. Bank: not answered yet. Build nothing for it" (prompts repo
  `completed/cc-P280-league-register-build.md:28`; `notes/cc-P280-league-register-build.md:31`, `:147`).
- Featherweight: not built (no match for `Featherweight` in the code). Your P280 answer 6 says "Weight is not sold"
  (prompts repo `completed/cc-P280-league-register-build.md:27`). Built as item count only:
  `LeagueRegister/LeagueBackpack.cs:3`, tiers `LeagueRegister/LeagueRegisterSettings.cs:55`. P179 drops Featherweight
  in favour of the guild satchels (`notes/cc-P179-league-design-pass.md:243`).
- Scavenger: not built. The mule's Load Harness III is marked partial: "the Clockwork Scavenger (the League's auto-loot
  reward) is not built; the redirect hook is" (`Mobiles/Mule/MuleModuleData.cs:71-72`). Design: F-33 Option A
  (`docs/feature-queue.md:2628-2630`). Proposal to drop it: `notes/cc-P75-league-rewards-rethink.md:170`, `:178-185`,
  `:198`, which rests on TazUO's client autoloot (`GM\ScavengerManager.cs` and others in the TazUO source). I could not
  check that from GitHub. The TazUO source is not in these repos.

## What I could not check

- **Haven's live settings.** `Configuration/league-ladder.json`, the requisition table file and
  `league.trialsWaivedUntilBuilt.*` may differ from the defaults cited here. This needs the game PC or Haven.
- **The runtime AP total.** 2,575 comes from parsing source, not a running server. A `docker/uo/build.sh` run prints
  it (`LeagueShopVerification.cs:389`), which needs the game PC.
- **TazUO's client autoloot** (Q9), which P75 relies on. The client source is in `D:\UO\third-party`, which this
  session cannot reach.
- Whether you answered P48's milestone question (Q1) or P75's Scavenger question (Q9) somewhere outside these repos.
  I searched `docs/`, `notes/` and the prompts repo and found no answer.

P376 DONE
