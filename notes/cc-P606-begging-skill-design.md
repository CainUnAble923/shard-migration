# P606: Begging becomes Persuasion

Design proposal, October 25, 2026. No code changes. Chase's direction is to make Begging a fuller social skill, including haggling and diplomacy. Recommended package: **Persuasion**, with asking for help at the bottom, trading and finding useful information in the middle, and negotiating difficult work at the top. Keep the existing skill slot and earned value.

Recommend option B below, delivered in six focused Golem prompts. Guard encounters depend on P608 and follow separately. Town standing integration also waits for an actual town standing system. This note proposes behavior, not a claim that it exists or approval to deploy it.

## Existing decisions and what this design changes

[Skills design](skills-design.md), lines 1396-1399 and 1430-1433, already records Chase's approval of the Persuasion name, temporary vendor discounts while training, a permanent discount at 200, and guild store coverage. The recorded working numbers are skill / 10 percent for ten minutes, then 30 percent permanently at 200. Preserve that purchase curve as the starting point. P606 adds a bounded selling benefit, information gathering, nonlethal encounters, and negotiation. It does not ask Chase to approve the name or concept again.

The following are **new proposals requiring review before implementation**: karma affecting the size of a concession; per-account charity limits; replacing the repeatable stock begging gain route with meaningful social work; exclusions and price floors that can narrow the earlier blanket discount; and choosing standing rather than extra gold or Renown for negotiated requisitions. The earlier design mentioned better League rewards without settling this complete package. These details are not silently treated as earlier approvals.

This is intentionally shard-specific content authorized by P606. After approval, the overseer should register the departures from stock Begging in the fidelity register. Agents have not edited `docs/`.

## What the source does today

Evidence checked in the supplied work copies. Code HEAD: `fcc658b853cc81684fb0d9d5268c91b6ba99ae49`. Notes HEAD before this file: `298768a18dd20b991cde4146a753615d2e21c30f`. The read-only ModernUO checkout is `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`.

In the references below, `C/` means `ShatteredLegacy/server/customizations/`, `P/` means `ShatteredLegacy/server/patches/`, and `U/` means `D:/UO/ModernUO-pinned/Projects/UOContent/`. Server core paths are identified separately. These are source observations, not live-server observations.

| Evidence | Current behavior and design consequence |
| --- | --- |
| `U/Skills/Begging.cs:10-24,28-82` | Registers the existing skill callback, reveals the user, and targets a human-bodied NPC within two tiles. Players are refused. A valid attempt bows and waits two seconds. Keep the skill button, but give it contextual social choices. |
| `U/Skills/Begging.cs:96-161` | Negative karma can cause refusal before the skill check. A successful 0..100 check takes one tenth of backpack gold, capped at 10..14 by Fame, not skill. Receiving coins can lower karma by up to 40, stopping at -3000. It does not give food or rumors. This proposal replaces that automatic karma loss with neutral charity. |
| `U/Skills/Begging.cs:163-171` | The valid attempt recalculates a ten-second skill cooldown measured from opening the targeter; opening initially reserves thirty seconds. Cancellation and invalid targets release it. Do not describe stock Begging as a thirty-second repeat timer. |
| `C/ClusterFSkillGain.cs:39-40,87-112,354-356,448-480` | P191 defaults are two chance attempts and one amount multiplier. Hook G extends the qualifying Begging check beyond its stock ceiling toward the character's cap. Begging can already gain past 100; its missing feature is a useful social job. |
| `C/ClusterFSkillCaps.cs:11,151-196`; `C/ClusterFSkillBonusAboveCap.cs:20-36` | Default individual Base cap is 200; worn bonuses can exceed Cap. The future loop ladder is not today's complete cap system. Separate learned unlocks from effective skill and bound social effects at 200. |
| `P/Begging-untrustworthy-achievement.patch:1-10`; `docker/uo/apply-patches.sh:805`; `C/ClusterFJokeAchievements.cs:93-101` | An existing hidden achievement is wired into the refusal branch. Preserve its identity and hidden status. This note does not reproduce its player-facing discovery instructions. |
| `C/Items/Consumables/Stew.cs:1-22`; `C/Items/Consumables/Cheese.cs:1-22`; `C/Items/Tools/BegFishingPole.cs:1-24` | Begging-marked items have been ported, but the inspected Begging handler never selects them. A constructible reward item is not a connected reward system. Use ordinary modest food for the new charity action; do not promise the ServUO reward lottery. |
| `C/ClusterFGuildStarterPath.cs:41-64,219-227`; `C/ClusterFGuildSystem.cs:215-224` | Begging and Appraisal belong to the Merchants' Exchange. The New Haven contact is listed at the bank. The Den has its own thief skills. Merchant initiation text still describes a 500-gold task; do not conflate this with the separately free guild join. |
| `U/Mobiles/Vendors/BaseVendor.cs:144-245,408-543,880-957,1353-1362`; `U/Mobiles/Vendors/GenericBuy.cs:50-83`; `U/Mobiles/Vendors/GenericSell.cs:12-88` | Listings and settlement use different paths, including stock and player-sold goods. Price scalar and item quality already affect prices. Resale asking price is normally 1.90 times the vendor's offer for that item. There is no inspected per-player Persuasion adjustment. A shared stock price object must not become one player's discount. |
| `C/Requisitions/RequisitionSystem.cs:220-273`; `C/Requisitions/RequisitionData.cs:31-66` | A request has a unique ID, item conditions, Renown, and guild reputation. Turn-in checks the item, pays Appraiser gold plus standing and Renown, removes the request, and deletes the item. Add negotiated terms to that transaction, not a second reward callback. |
| `C/Requisitions/RequisitionLeads.cs:35-45,49-91,165-204` | Leads already attach an area and creature group to a personal requisition, with rank eligibility and expiry. They affect qualifying kills and drops. Persuasion should help find an eligible Lead, not create a parallel loot engine. |
| `U/Skills/Peacemaking.cs:133-202`; `U/Mobiles/Guards/BaseGuard.cs:13-65,72-93` | Peacemaking has real creature pacification. Guards can be created at the target, and teleport support exists. A social pause must have narrower rules than Peacemaking. Walking posts, patrols, and guard challenges belong to P608. |
| `C/Tutorial/TutorialStations.cs:139-143`; `C/Tutorial/TutorialTradeTrials.cs:150-165,440-464`; `C/CharacterCreation.cs:1018-1028` | Begging is currently inside the thief trial, receives a temporary training bonus there, and selected Begging equips a staff at creation. A rename alone would leave misleading lessons and starter flavor. |

Read alongside the source: [P191](cc-P191-cont-earned-skill-gain.md), [P283](cc-P283-skill-gain-paths-research.md), [P535](cc-P535-skills-design-vs-build.md), the utility decisions in [skills design](skills-design.md), [guild index](wiki-drafts/guilds.md), and [Thieves' Den guide](wiki-drafts/thieves-den.md). P535 correctly separates built gain machinery from unbuilt Persuasion rewards. P283's existing gain path is not evidence that haggling exists.

The guild index and canonical guild table support the Merchants' Exchange as the home. No separate beggars' guild or street-folk membership was established by the inspected sources. No town-standing adapter was established either: exact-name searches are only leads, so these are unverified integration points, not claims that every possible reputation system is absent. No P608 note was present among this checkout's top-level notes; its dependency here comes from the task brief.

## Name, player action, and progression

**Persuasion** is the recommended display name and already approved. **Diplomacy** fits civic work but undersells bargaining and street contacts. **Silver Tongue** works better as a title than a skill name. Keep `SkillName.Begging`, its numeric slot 6, saved Base, Cap, lock, and skill modifiers. Do not add another skill or reset learned points. The updater and server display should agree, as with Appraisal. Client labels, macros, creation text, and tutorial text need a compatibility pass; their runtime behavior remains unverified here.

Use the skill and target an NPC, or choose its **Persuasion** context entry. Show only supported choices: **Ask for help**, **Haggle**, **Ask about work**, **Negotiate terms**, or **Appeal for calm**. State the offered result, refusal reason, and meaningful cooldown in ordinary language. Keep normal Buy, Sell, and Talk available. No typed keyword puzzle, reaction timer, or repeated click bonus.

Learned Base unlocks actions and titles. Let `S = clamp(effective Value, 0, 200)` for outcome calculations within an unlocked action. Gear helps an action you know, but cannot unlock the permanent Base-200 privilege or turn a novice into a negotiator. Above-200 Value does not increase discounts, sale bonuses, durations, or standing bonuses.

| Learned Base | Social work and reward |
| --- | --- |
| 0..19.9, novice | Ask a civilian for a small meal or coins. Ask where ordinary work can be found. Take a free Exchange introduction and beginner delivery job. Charity is a foothold, not the main income or training route. |
| 20..49.9, apprentice | Haggle with ordinary vendors. Find named public contacts and descriptions of local jobs. Carry messages or settle simple supply misunderstandings. A successful temporary purchase discount is about 2..5 percent at neutral karma. |
| 50..79.9, journeyman | Ask for a useful requisition Lead. Negotiate a small standing concession on eligible work. Request a brief pause from an eligible hostile person. Purchase discounts reach about 5..8 percent. |
| 80..99.9, adept | Use the difficult local negotiation jobs. Appeal to selected wild animals, with Animal Lore as an optional help. Unlock the future P608 routine guard challenge. Purchase discounts approach 10 percent. |
| 100..149.9, GM and beyond | GM earns a visible social title. Take regional mediation and supply negotiations with harder checks; learn more precise information about eligible Leads. Purchase discount rises from 10 to about 15 percent. Sale bonus and standing bonus keep growing slowly. |
| 150..199.9, master | Resolve multi-contact disputes and difficult regional jobs. A rumor can identify the relevant creature family and public destination without revealing a live spawn. Purchase discount approaches its temporary 20 percent ceiling. Social effects remain short and conditional. |
| 200, legendary | The approved purchase discount becomes permanent, up to 30 percent subject to the economy rules below. Highest precision for eligible Leads, maximum 5 percent better sale offers, and maximum 10 percent extra earned standing. Continue social jobs for ordinary rewards and roleplay, without gain at cap. |

GM means 100 Base here. Titles and guild rank are different. All bands obey the character's actual cap. Future F-12 loop caps can restrict the available bands, but this skill must not pretend that loop gating is already live. No growth beyond the configured Base cap is proposed.

## Haggling and economy limits

For player purchases, use the already recorded curve: before Base 200, a successful haggle grants `min(20, S / 10)` percent off for ten minutes at that vendor. At Base 200, grant 30 percent automatically while the character still has that learned Base. A future skill reset must remove the privilege until relearned; do not persist a forever-discount flag across resets. Haggling is not required on every shopping visit at 200 and passive shopping awards no training.

Proposed vendor selling bonus after the same successful haggle: `min(5, S / 40)` percent added to what the NPC normally pays. At Base 200 it is passive too. This benefits loot sellers without turning vendor stock into a gold printer. It never improves player-vendor trades or prices negotiated between players.

Karma is a small modifier, not a morality lock. At lawful shops use `M = 1 - 0.2 * clamp(-Karma / 10000, 0, 1)`. At explicitly designated underworld contacts reverse the karma sign. Neutral or favorable karma gives the full concession; strongly mismatched karma reduces it to 80 percent. Multiply both percentage benefits by M. Positive lawful karma never exceeds the stated caps, and an evil character retains a useful lawful shopping benefit. Guild membership/rank and legal vendor access still apply. Alignment does not secretly reverse on every shop in Buccaneer's Den; underworld status must be authored and visible.

Examples before integer rounding, neutral karma, for a vendor asking 100 gold and normally paying 40:

| Skill | Player buys for | Player sells for |
| --- | --- | --- |
| 50 | 95 | 40.50 |
| 100 | 90 | 41 |
| 150 | 85 | 41.50 |
| 200 | 70 | 42 |

At Base 200 and -10000 karma, a lawful shop instead asks 76 and offers 41.60. These are proposed formulas, not measured economy outcomes.

Apply the concession once after ordinary taxes and existing item adjustments. Competing social discounts use the larger benefit, rather than multiplying. Round purchase costs up and sale payouts down to whole currency units. A paid line costs at least one unit. Stack splitting must never improve an aggregate quote; keep the same per-unit rounding in display and settlement. Normal stock quantities, vendor cash, access, and resale eligibility remain in force.

Purchase coverage includes guildmasters' existing currency stores, as Chase requested. Apply the discount independently to each actual cost component; never discount a skill, membership, reputation, recipe-knowledge, or other access requirement. Standing is not a spendable currency. Guild currencies are not interchangeable. Renown stores require an explicit adapter and an audited catalog rather than assuming they use a vendor packet. There is no improved guild buyback rate and no discount on exchanging currencies.

**Proposed safety boundary for review:** ordinary equipment and consumables can participate after a catalog audit. Currency conversion, deeds with redemption value, refundable purchases, raw commodity loops, services, contract submission inputs, and uncataloged custom stores start excluded until audited. An authored exception must say "Fixed price". This narrows the earlier "every vendor" wording and must be accepted explicitly before implementation. Do not quietly ship a 30 percent discount into every independent custom gump.

The audit must cover the least expensive discounted acquisition and highest NPC payout across vendors, towns, alternate currencies, and deterministic conversions. Include buy/sell, buy/melt/sell, buy/craft/requisition, salvage, empty beverage containers, recipe rewards, and refund loops. A fixed percentage cap alone is insufficient. The normal 1.90 resale markup, for example, does not prove that another vendor or the Appraiser cannot pay more.

For a freely repeatable interchangeable item, require the maximum NPC cash-out to remain at most 90 percent of its minimum discounted NPC acquisition cost. Cap the social sale uplift at that boundary; if the ordinary payout already violates it, withhold the purchase discount for that catalog entry and record the preexisting issue separately. Include reversible transformations in the equivalence group. Where a safe comparison is unavailable, leave that entry fixed-price. Newly generated social job tokens must never qualify as vendor goods or requisition inputs.

This audit rule is a proposed release requirement, not a proven property of current catalogs. Purchase and settlement must share a per-player quote and revalidate skill, price, quantity, currency, and eligibility. A changed quote requires confirmation of the new amount. Never write a personal discount into shared `GenericBuyInfo.Price` or `PriceScalar`. Do not use repeated tiny transactions, restocks, or alts to manufacture gain.

## Diplomacy, terms, and information

### A short appeal for calm

At 50 Base, appeal to a selected hostile humanoid that the content author has marked as able to listen. At 80 Base, selected ordinary wild animals can also listen. Animal Lore can improve the animal attempt by at most ten percentage points; it never bypasses an immunity or teaches Persuasion by itself. Start with an explicit target list, not `Body.IsHuman` as a guarantee that a monster understands speech.

Stand within three tiles and line of sight, visible, and spend two uninterrupted seconds speaking. Success pauses that NPC's pursuit and attacks against the speaker for `2 + S / 50` seconds, capped at six. It does not pacify the encounter for the party, erase aggression, heal anyone, tame an animal, reset loot credit, or allow a free theft. The speaker can retreat. An ally already under attack remains under attack.

An offensive action by the speaker or their controlled creatures, or damage to the appealed NPC, ends the pause immediately. Do not let pet attacks and area damage preserve it. No effect on players, player pets, summons, bosses, champions, event encounters, uncalmable creatures, or NPCs currently engaged with another player. Standard guards are excluded and use the separate P608 contract. No repeated stop effect through parties: an attempted appeal gives the target a two-minute shared social immunity, and the speaker a thirty-second appeal cooldown, regardless of outcome. Losing the target or being interrupted consumes that encounter's attempt.

This deliberately has less combat control than Peacemaking and no area mode. Ordinary farmable animals give no repeated social gain. A real authored encounter can teach once under the work rules below. Ignore damage/heal macros and repeated release/retame cycles as training sources. Animal calming is the first feature to cut if it competes with the approved Drover's Handbook or bards.

### Talking past a guard: interface for P608

P608 owns guard perception, posts, patrols, pursuit, combat, and law. P606 supplies a social response only when P608 exposes a **routine challenge**, before an arrest or active pursuit. Recommended use: an innocent traveler explains their business at a watched checkpoint and, on success, gets a passage acknowledgment for that checkpoint for five minutes. It prevents another routine challenge there; it is not immunity from new crimes or other posts.

One attempt per account, checkpoint, and challenge opportunity. Failure leaves the ordinary P608 challenge in place. Criminal flags, murder status, outstanding lawful arrest, hot pursuit, combat, recent theft, restricted quest gates, and denied faction access cannot be talked away. No warning or dialogue delay may postpone a guard's response to witnessed harm. Recheck these facts when a pending conversation resolves. More skill can improve the explanation, never remove a crime or prevent reporting.

The challenge must have range and line-of-sight requirements supplied by P608 and remain interruptible. Successful routine challenges can give one eligible gain event, with a thirty-minute checkpoint/account training cooldown. Guards must not offer repeatable skill rolls while stationary. No change to current teleporting guards is included in this design. This interaction remains disabled until the P608 state transition exists and is tested.

### Negotiating completed work

At 50 Base, an eligible guild requisition or authored civic job offers one terms discussion before commitment. On success it records a prospective standing bonus of `min(10, S / 20)` percent. The benefit is at least a small improvement at early skill and tops at 10 percent. Karma affects the chance through the contact's attitude, not the final standing payout. Never multiply both the reward size and its payout again.

Recommended launch concession is **extra guild standing only**. Keep item quality, required properties, access, gold, Renown, guild scrip, Lead drop chances, and deadlines unchanged. Completing the same work better rewarded is the useful first negotiation. Alternative requirements, larger cash rewards, and changes to Renown would create more balancing paths and are deferred.

One immutable terms result per request ID, accepted before its item is submitted. A failed discussion still leaves the normal request available; retries, reopening its page, transferring items, or rerolling the board cannot retry that same terms roll. No standing or training is awarded simply for asking. At turn-in, award the extra only with the genuine consumed item and remove the request and its terms together. The first three eligible negotiated completions per account per UTC day can receive the bonus, across all guilds. Reserve an available bonus slot when displaying the final turn-in quote so another character cannot consume it concurrently.

Round the total extra standing down, carrying a fractional remainder per character and guild so small novice jobs are not permanently rounded to zero. No minimum +1 that can be farmed with tiny jobs. Only eligible work contributes to that remainder. Example: a base 25-standing job at GM earns 1.25 extra, paying one extra now and carrying 0.25. Do not apply this to joining, Apprentice rewards, donations, bought reputation, achievements, or the Custodians' lifetime-cleanup rank.

Future town work can use the same capped bonus for a town's earned standing, charged against the same account daily allowance. First identify its canonical owner and payout transaction. No new global town reputation ledger is part of option B. Reputation never increases for greetings, rumors, or repeatedly apologizing to guards.

### Rumors with a useful destination

Public directions and ordinary work listings are free to everyone, including zero skill. Persuasion adds specificity. At 20 Base, an NPC can name a relevant public contact or place. At 50, a useful rumor may attach one eligible Lead to an existing open requisition without a live Lead, using the current area, creature-family, rank, expiry, and drop rules. At 100, state the public route and relevant family clearly. At 150 and 200, prefer a Lead compatible with the character's chosen request and travel access, and offer a clearer explanation of what to seek. Do not increase drop rates or promise a rare spawn is alive.

One attempt per account and contact per UTC day; at most three newly attached Leads per account per UTC day. Failures consume that contact's attempt, not a successful-Lead slot. Reopening shows the saved answer. Rerolling does not reset a Lead's expiry, kill pity, or family. Never replace a live Lead to reroll it. Invalid, expired, or inaccessible destinations are refused without spending a success slot. Normal board-generated Leads remain independent.

Content authors can later write hints toward a survey, treasure story, or spawn region using the same validated clue format. Launch uses requisition Leads because they already have a destination and a completion loop. Exclude exact treasure coordinates, live spawn timers, hidden achievements, hidden players, and unreleased content. A shared rumor does not make its personal Lead transferable.

## Charity stays at the bottom

Keep **Ask for help** as a recognizable Begging action. A willing ordinary civilian can give either coins from existing backpack gold or one plain food serving. At most one charity result per account and NPC contact per UTC day, shared between food and coins. Use a stable contact identity across respawn or replacement; freshly created or player-controlled NPCs cannot supply charity.

Proposed coin ceiling per attempt is `floor((2 + 0.3 * min(S, 40)) * M)`, capped at 14, then limited by one tenth of the NPC's actual backpack gold and the account's remaining daily allowance. Maximum charity is 50 gold and two food servings per account per UTC day, shared across characters and towns. Keep a ten-second action cooldown. Invalid targets do not spend an allowance; a valid refusal spends that contact's attempt. No gold is minted to fill a civilian's empty pack.

A meal needs no NPC coin balance and uses a modest approved food list. Charity food has no NPC resale, salvage, requisition, or gifting value; the receiver can eat it. A new food may need an appropriate item wrapper or source tag during implementation. Neither food nor coins become richer after 40 skill. All karma paths retain access to basic food through at least one public relief contact; this avoids a beginner's refusal spiral. Asking does not lower karma. Genuine crimes still do.

Training from charity is introductory only, once for each distinct successful contact until Base 20. No gain for refusals, an empty pack, standing beside the same NPC, or charity after that band. Tutorial food and training props never pay real coins or refill these allowances. A player at 20 has an unlimited-in-principle paid-work training route, so waiting for the daily alms reset is never the next training step.

## Training that feels earned

P191 changes gain frequency, not whether a use deserves to train. Keep the shard's existing rate settings and 0.1 base gain size. Do not create a Persuasion-specific amount multiplier, free skill award on job turn-in, or a new Test Crystal rule. P283 already proves an existing route above the old ceiling; the design intentionally replaces its easy repeat target with better work. That behavioral replacement needs its own acceptance coverage.

Separate the action's outcome calculation from the right to train. A shop quote, greeting, repeated question, and passive Base-200 discount must never call an unrestricted `CheckTargetSkill(Begging, npc, 0, 100)`. That call currently reaches hook G and would restore cap training from a trivial target. Retire or narrowly guard the old Begging row when the new work route ships, covering both below-100 and above-100 gain. Do not ship haggling first with every attempt teaching to cap.

| Source of eligible practice | What makes it earned |
| --- | --- |
| Introductory aid, below 20 | A distinct successful, accounted charity result. The per-account contact budget also limits alts. |
| Ordinary vendor trade, below 75 | A successful new haggle followed by an actual eligible trade of at least 100 gold at the undiscounted quote. At most one practice event per account/contact/day; buying and selling share it. Splitting transactions or buying back the same goods gives nothing extra. This is optional incidental training, not the required leveling path. |
| Exchange social jobs, all bands | Finish distinct authored objectives: deliver an assigned sealed message to a different location, obtain a field witness report, reconcile a supplied invoice against a delivered shipment, or mediate an authored dispute after fulfilling its requested work. Inventory or world objectives validate completion; simply cycling dialogue cannot. |
| A rumor that leads somewhere | No gain on merely generating the hint. One eligible practice event when the character follows the personal Lead and completes the associated actual requisition. Its negotiated-turn-in event, if any, is the same event, not an additional roll. |
| Terms discussion | One event on the completed work that fulfills the recorded negotiation. A valid failed negotiation can still teach on eventual completion, since the work was done. No gain for repeated failed conversation clicks. |
| Authored calm or future guard encounter | One event when the encounter reaches its defined terminal resolution after its real prerequisites. Ordinary respawning animals, manufactured crimes, and repeated patrol greetings do not qualify. |

Every qualifying objective carries a server-generated job/request ID, difficulty, participant, consumed-or-resolved state, and a single credited practice key. Commit the objective and consume that key before issuing its gain event. Disconnects, daily refresh, NPC replacement, restart, and replayed responses must not replay practice. Replacing a contact keeps its stable ID; staff-created NPCs do not create new practice budgets.

The Exchange supplies a repeatable job pool from novice through 200 without requiring existing high guild rank, combat, rare treasure, or any successful charity attempt. Introductory jobs are free. Upper jobs require real deliveries, collected evidence, or completed requisitions, not purchased blank tokens. Rotate contact pairs and regions, avoid immediate repeats, and give a local low-risk job alternative. A citizen with negative karma has equivalent authored underworld or relief work with the same gain windows, without requiring a crime. No new beggars' guild is required.

Proposed job difficulties are 10, 35, 60, 85, 110, 135, 160, 185, and 195. Offer a tier from Base `max(0, difficulty - 25)`. Each eligible objective uses a gain window from difficulty - 25 to difficulty + 25, adding positive worn bonus to **both edges for this gain-only check**, so bonus gear cannot exhaust the challenge before Base does. Mark the window as already compensated through the existing gain helper; if its top happens to equal Cap, the wrapper must not add that bonus a second time. These overlapping tiers cover 0 through 200; the difficulty-195 window is 170..220 and therefore supports 199.9 -> 200. Outcome checks use S separately. No harder job must require Base 200 just to start the final gain.

A job can contain several distinct practical objectives, each teaching once. Repeatedly choosing a dialogue response is one objective, regardless of its number of messages. A failed negotiated outcome is allowed to teach only when the associated real work completes; an abandoned job or spammed failed appeal is not. Supply enough genuinely different repeatable work to avoid a daily training wall. Daily caps govern extra rewards and trivial incidental practice, not access to the main job pool.

Use the normal gain pipeline once per credited objective, retaining its configured extra chance attempts internally, locks, cap, and one logical SkillUsed event. Deduplicate tutorial observation and progression tracking against that same objective; do not run stock outcome gain and another completion gain. Outcome chance can start at `clamp((S - difficulty + 50) / 100, 0.05, 0.95)` for authored uncertain encounters, with at most a ten-percentage-point attitude/help adjustment and the same outer clamp. Simple public directions need no roll. Exact encounter odds are tuning proposals.

This prevents consequence-free NPC macro farming. It does not claim software can distinguish a person doing a real delivery from automation completing that same delivery. Time, objective variation, consumption, and completion evidence are the defenses. Do not promise a training duration from P191's combat simulation. Measure checks and gains per ordinary social session before tuning content density; do not raise the shared gain rate to compensate for too few jobs.

## Guild, titles, achievements, and tutorial

**Home:** the Merchants' Exchange remains the skill's owner, alongside Appraisal. Its public job identity is courier, broker, and mediator. The bank chapter is the verified listed introduction, not a newly promised hall. Let a street contact or relief worker offer its beginner work without creating a new faction, currency, building, or art request. Existing free membership remains free. The proposed social lesson should not charge the current 500-gold Apprentice task as an entry fee to practicing the skill; replacing that task with a completed beginner negotiation is an explicit option for Chase.

The Den can offer flavored contacts or jobs to members while ownership stays with the Exchange. It does not receive Begging as a second primary skill. Keep the same capability and gain budget for lawful and underworld work. Musicianship and begging disguises are deliberately deferred: music already has a guild and three combat skills, while disguises touch detection and P608 law. A later performance job could use Musicianship for presentation without multiplying tips or becoming a second gain roll. This package adds neither a tip farm nor a disguise that bypasses guards.

Suggested optional display titles, tied to Base rather than guild rank: **Streetwise** at 50, **Silver Tongue** at GM 100, **Mediator** at 150, and **Master Negotiator** at 200. Pick titles from earned records, rather than automatically overwriting the player's chosen title. Keeping the legacy beggar flavor as an optional title is reasonable. No title grants another price bonus.

Propose two visible achievements: **A Fair Deal**, for completing a first real negotiated transaction, and **Common Ground**, for finishing ten distinct authored mediation jobs across three towns. Cosmetic/title recognition only; no repeating currency, gold, or standing rewards. Count committed job IDs rather than conversation attempts. Preserve existing hidden achievements and their visibility metadata; keep any future hidden criteria in staff implementation notes and out of tutorial, rumors, and public guides. No additional hidden achievement is specified here.

The tutorial introduces a harmless social lesson near the trade/League route: ask a relief contact for a meal, ask where work is, and negotiate a practice invoice, then deliver it to the Exchange contact. Practice money and goods stay in the lesson and cannot be sold or submitted. Give a guaranteed demonstration outcome and ordinary explanation, not repeated failure until a novice wins a roll. Do not grant permanent skill points for replaying the lesson.

Remove Begging as a required thief-trial step and update the temporary skill-loan list and progress accounting with it. Preserve completed tutorial progress when moving that requirement; no forced replay or lost graduation. Keep the existing saved skill enum and tutorial compatibility mapping. Creation and all Skills UI surfaces say Persuasion; a retained starter staff is flavor, not a required instrument. An optional Exchange letter is a better new starter item, with no monetary value. Tell beginners: charity stops teaching early; delivery and negotiation jobs continue training; guards still enforce crimes. Teach the P608 routine challenge only after that feature ships.

## Three implementation options

Estimates below are Golem implementation prompts, each including source checks, failing-first behavioral tests where code changes, and its build gate. They are planning estimates, not measured durations. Options are cumulative totals, not additions to one another. P608's guard rework and any new town reputation system are external work and excluded from these totals.

| Option | Scope | Estimated prompts | Tradeoff |
| --- | --- | --- | --- |
| A: useful foundation | Retain the approved name and purchase curve; bounded selling; beginner charity; contextual actions; validated existing requisition Leads; a basic but continuous Exchange job ladder to 200; tutorial and economy safeguards. | 3: social identity/charity/jobs; price quotes/catalog audit; Leads/tutorial/integration proof. A large custom-store catalog could require a fourth. | Smallest useful shopping and street-contact skill. Deliberately defers the requested calm encounters and negotiated standing, so it is a first release rather than the full answer to Chase's direction. |
| **B: social profession, recommended** | A plus authored diplomacy, the capped standing concession, richer repeatable mediation work, and titles/achievements. Publish the P608 guard interface, but do not enable it against current guards. | **6 total:** (1) identity, charity, and novice work; (2) quote service and economy audit; (3) rumors/Lead completion; (4) requisition terms and standing payout; (5) eligible calm encounters and upper work ladder; (6) tutorial, compatibility, rewards, and end-to-end proof. | Delivers the core social skill with reusable existing systems. If custom-store audits do not fit prompt 2, split them and budget 7 rather than weakening the economy check. |
| C: wider civic play | B plus the P608 routine-challenge adapter, a verified town-standing adapter and authored civic negotiations, and a deeper regional contact/job set. No automatic performance or disguise subsystem. | 9..11 total: B's 6, one guard adapter, one town adapter, one regional content prompt, and up to two for catalog/content spillover. | More reasons to play a diplomat, but dependent on external guard and town work. Count those external systems separately; this is not a promise that P608 costs one prompt. |

Choose B and release only complete slices. Prompt 1 needs an actual repeatable training route, not a renamed button waiting for prompt 5. Prompt 5 extends the route's encounter variety and authored upper jobs; it must not be the first path to 200. Prompt 2 must ship display and settlement together. Prompt 4 must ship terms persistence and payout together. Each slice remains useful if the next one is delayed. Art is not required; reuse current NPCs, gumps, item art, and effects.

## Questions for Chase, with recommended answers

These are review choices for future builder prompts, not blockers for finishing this design. No live action or deployment is requested.

| Question | Recommended answer and reason |
| --- | --- |
| Which size should enter the queue? | B, six prompts with a seventh reserved if store audits expand. It supplies a profession, not just a vendor percentage. |
| Keep the already approved name and purchase curve? | Yes: Persuasion, temporary skill / 10 percent for ten minutes, permanent 30 percent at Base 200. Diplomacy is an activity and Silver Tongue a title. No need to reopen the settled name decision. |
| Accept karma scaling and explicit fixed-price exceptions to the blanket discount? | Yes, with the 80..100 percent attitude factor and audited catalog rules above. This is the one deliberate narrowing of the earlier purchase promise. If rejected, retain the promise in design and hold unsafe entries for a separate economy decision; do not implement an unverified blanket rate. |
| Add better vendor sale offers too? | Yes, at most 5 percent, subject to cross-vendor and conversion safety. It makes negotiating useful to adventurers without another large gold faucet. |
| Extra gold/Renown, easier item requirements, or standing as the first negotiated reward? | Standing, at most 10 percent on the first three eligible account completions per day. Preserve gold, Renown, requested items, and access; broader quest terms wait for a separate economy/content pass. |
| Merchants, thieves, or a new street guild? | Merchants' Exchange, with street and Den contacts as optional content. Replace the Exchange's Apprentice 500-gold task with one beginner mediation/delivery task, preserving its once-only reward, rather than creating another membership. |
| May diplomacy clear a crime or stop guards responding to harm? | No. Only P608 routine challenges for otherwise eligible travelers, with no legal immunity. Never enable that interaction on today's guard spawn path. |
| Keep animal calming, performance, and disguise? | Keep narrow authored animal appeals if they remain distinct from bard and Herding control. Defer performance and disguise. They add overlapping systems without helping the core release. |
| May the existing endless begging gain route change? | Yes, only when the replacement job pool demonstrably trains every band through 200. Keep P191's rate; beginner charity and meaningful work supply the practice. Existing skill points are retained. |
| Build town reputation for this task? | No. Specify the future adapter and use guild standing now. An invented town ledger would enlarge the task without a verified integration owner. |

## Future builder acceptance and task verification

Future implementation needs failing-first tests for quote/settlement equality, player isolation of prices, rounding and stack splitting, guild currency components, excluded/refundable goods, cross-vendor and conversion loops, and two characters using one account's allowances. Test trade and quest replays, expiry, restart, stable contact replacement, crime changes while speaking, pet/party attempts to chain calm, and the P608 adapter's refusal during active enforcement.

Training coverage must demonstrate a continuous reachable job ladder, representative lower caps, gain at Base 199.9 with and without positive skill bonuses, no gain at cap or locked Down/Locked, one logical skill-use event per objective, no double credit for rumor plus terms, and no teaching from repeated empty dialogue or disabled content. Confirm the Test Crystal remains a test-only rate lever. Preserve completed tutorial records, hidden achievement metadata, the stock saved skill identity, and normal vendor access.

These are acceptance criteria for later code, not new tests added by P606. This lane has no tests to run and changes only this note. No build, container operation, deployment, Haven connection, account/save operation, commit, merge, push, or branch switch was performed. No `server/uo/` files were read and no `docs/` files were edited.

Unverified: running configuration and deployment; client rename/macro compatibility; live NPC placement; every custom store's cost and refund paths; economy cycles across the entire catalog; actual social training time; town-standing ownership; and P608's final guard states. None is presented as an implemented feature. Source searches established the inspected behavior, not an aggregate content-completion count.

Ran `tools/progress.py --dry-run` with both work-copy path overrides: exit 0 and a report produced. This tool writes `tools/progress.json` even in dry-run mode; its prior bytes were preserved in memory, restored afterward, and confirmed byte-identical. No generated progress artifact is part of this task.

Editorial review checked local evidence references, note links, table structure, arithmetic examples, plain American English, and the absence of em dashes and trailing whitespace. No new executable tests or gates were added. Both repository statuses are checked again immediately before the completion marker; the intended final change is this note alone. Stop requests were checked between research, drafting, and review.

Final review passed: evidence paths and line bounds, local links, Markdown tables, whitespace, size, and both repository scopes checked. Code status is clean; notes status contains this file alone. Final stop-request check: absent.

P606 DONE
