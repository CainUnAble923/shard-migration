# P387: player guide to achievements, Achievement Points, and loot boxes

October 21, 2026. Codex lane, Verite-tower work copies. Docs-only draft.

## Deliverables

- [Player guide](wiki-drafts/achievements-and-loot-boxes.md).
- This evidence and verification note.

The page covers the achievement categories and records window, account sharing, AP, Renown, public titles, earned boxes, opening locations, binding, fanfare and mute, the League starter shop, its separate box pool, and Hall decor. It ends with Sources and Contradictions lists. Code file:line citations are kept here.

The task paused twice when the Golem's stop file appeared and resumed when authorized. Those pauses occurred during source review. No implementation was changed during any session.

## Sources reviewed

Read the two work-copy root AGENTS.md files, the direction decision, task list, and document-governance index. Used the League and Society of Smiths wiki drafts as models. Read the relevant feature-queue entries directly: F-13 and F-40 through F-42.

Primary topic notes and sections:

- P55 Parts F/G, P57 Part F, and P61 Part B: descriptions, retired achievements, layout, and progress.
- P75, P79, P78's reward-source section, P80's achievement/graduation material, and P82's box effects: reward proposals, the original earned-box implementation, placeholders, recipes, and quality.
- P147, P165, and P241: the client button, login-handshake repair, and category headings/icons. P241 changes headings, not category tabs.
- P229 and P243: starter shop, AP titles, cosmetic box pool, and Hall deeds.
- P231, P262's achievement material, P263, and P361: hidden definitions, hidden title handling, reward exceptions, and the boss-box finding.
- P366 and P371: merged flying-loot art and the new real graduation loop.
- P374 and P376: the League guide's earlier source disagreements and remaining documentation questions.

Searched the top-level cc-P*.md notes for achievement, loot-box, fanfare, and reward-shop references, then inspected topic passages. Peripheral references include P11/P15/P18/P20/P21/P25/P30/P47/P48/P49/P53/P54/P58/P64/P65/P69/P72/P73/P84/P89/P95, P100/P106/P117/P121/P127/P129/P135/P137/P138/P142/P145/P146/P150/P152/P164/P166/P173/P179/P189/P190/P191/P192/P194/P195/P196/P201/P209/P212/P217/P220/P224/P225/P227/P239/P240/P245/P260/P267/P278/P283/P286, and P364/P377/P378/P379/P381/P382/P383/P384/P386. Many concern unrelated build flakes or cite achievements incidentally. They do not establish current deployment or new reward behavior. Broad combined reads sometimes exceeded output limits; claims below use focused source reads, not unseen truncated output.

No historical AP ceiling, hidden-achievement total, or historical overall title count is published as current fact. No hidden achievement names, triggers, special rewards, or hidden title names are disclosed on the guide.

## Implementation evidence

C paths below are relative to the ShatteredLegacy work copy. M paths are relative to shard-migration. Pinned paths are relative to D:/UO/ModernUO-pinned, verified at d4531cd94b739613155225c234900de9f47d2c88.

| Guide topic | Evidence |
|---|---|
| Player access | C `server/customizations/ClusterFAchievements.cs:1695-1701` implements player `[achievements`. C `server/customizations/LeagueRegistrar.cs:41-42`, `:71-81` names Elara Voss and opens her menu. C `server/customizations/LeagueRegistrarGump.cs:134-140`, `:405-415` provides the records/shop/title routes. M P147 and P165 document the custom-client paperdoll and top-bar routes and the handshake fix. |
| Account earn and currencies | C `server/customizations/ClusterFAchievements.cs:1325-1352`: keys are added once by account username, AP and achievement Renown are added, titles sync, player notification and box hook follow. C `server/customizations/ClusterFAccountData.cs:10-21`, `:653-670`: account balances, qualifying lifetime earnings, and spending only from the balance. |
| Category inventory | C `server/customizations/ClusterFAchievements.cs:272-283` lists Combat, Skills, Exploration, Mining, Crafting, Legacy, Discovery, Collection, League, Mischief. `:1993-2006` gives their icons. `:2017-2027` gives All and the seven category tabs; Collection, League, and Mischief are available under All. |
| Public category examples | C `server/customizations/ClusterFAchievements.cs:436-472` first login and combat; `:658-697` facets; `:717-724`, `:738-754`, `:862-884` skills; `:889-904`, `:928-935` mining; `:968-1010` crafting; `:1015-1022`, `:1035-1050` collection; `:1054-1068` discovery; `:1072-1088`, `:1101-1108` Legacy; `:1112-1119` League. Hidden neighboring definitions were not used as examples. |
| Earned, unfinished, and retired rows | C `server/customizations/ClusterFAchievements.cs:2183-2200` filters hidden unearned rows and separates held retired entries. `:2285-2329` draws reward values, earned explanation, prerequisites, and unfinished progress. `:336-339` records the retained rewards policy, with retirement refusal at `:1329-1330`. `:2389-2409` is the separate trainer-quest checklist. |
| Shop and Titles from records | C `server/customizations/ClusterFAchievements.cs:2427-2436`. |
| Title thresholds and ownership | C `server/customizations/LeagueShop/LeagueShop.cs:332-339`: three bought public titles and the free thresholds 100/250/500/1,000/1,750. `:351-360` only adds owned AP titles. `:369-398` stores and displays the per-character choice. `:402-415` reapplies it on login. C `server/customizations/LeagueShop/LeagueShopGumps.cs:398-427` draws No League title and hides unheld secret titles. |
| Extra Renown source | C `server/customizations/Requisitions/RequisitionSystem.cs:248` grants requisition Renown as LeagueJob. The guide links to the League page instead of repeating requisition requirements. |
| First box and repeats | C `server/customizations/LootBoxes/ClusterFLootBoxes.cs:86-117`: a new source awards a rolled box; same-loop repetition does nothing, later-loop repetition gives a line without another box. `:132-159` finds the first online character on an earning account and applies ordinary or special box rules. The guide states no secret exceptions by name. |
| League promotions | C `server/customizations/ClusterFLeagueRanks.cs:424-425` calls the rank award after promotion. C `server/customizations/LootBoxes/ClusterFLootBoxes.cs:208-210` defines that source. |
| Graduation is live code | C `server/customizations/Tutorial/ClusterFTutorial.cs:216-251` calls Graduate and the separate Explorer tier-1 reward. C `server/customizations/Tutorial/ClusterFLoops.cs:25-34`, `:47-61` records a monotonic first loop and calls the reward. C `server/customizations/LootBoxes/ClusterFLootBoxes.cs:218-221` plays the capstone and awards a Loop box. `ClusterFLoops.cs:36-42` leaves level/skill reset integration empty. |
| Unbuilt sources | C `server/customizations/LootBoxes/ClusterFLootBoxes.cs:214-239` retains level, clear, trial, reaching-200, and fragment hooks. A search across canonical customization C# found only the method definitions for OnLevelUp, OnDungeonCleared, OnTrialChapter, OnReached200; OnLoopCompleted has its actual caller in Tutorial/ClusterFLoops.cs. The guide marks dungeon/floor-clear rewards and broader later loops as (planned). |
| Default tiers and currencies | C `server/customizations/LootBoxes/ClusterFLootTable.cs:53-58`, `:71-102`, `:146-167`: gold 250/750/2,000/5,000/12,000/30,000; base Renown 0/25/50/100/200/400; rarity names/colors and AP ceilings 10/25/50/100/250, then tier 6. These are source defaults, not verified running settings. |
| Material names and theme contents | C `server/customizations/LootBoxes/LootBoxRoller.cs:39-57` selects the ladder; `:145-183` rolls and fixes contents at award; `:239-288` implements theme rewards. Hunter uses hides/slayer gear; Explorer maps; Scholar reagents/scroll; Artisan supplies/recipe. League adds 50 times the quality tier in Renown, so the currency table is labeled base. The guide makes no material-content promise from the box name. |
| Slots are not item counts | C `server/customizations/LootBoxes/LootBoxRoller.cs:165-180`: a theme slot may create multiple items, one slot is currency, and general slots are additional rolls. Avoided presenting 2/3/3/4/5/6 slots as physical item counts. |
| Reward pools and scaling | C `server/customizations/LootBoxes/LootBoxRoller.cs:294-302`, `:307-375`, `:391-472` implements supplies, resources, magic gear, recipes, bound cosmetics, and rare rewards. `ClusterFLootBoxes.cs:54-67` uses total base skill divided by 10 as a level stand-in. No timing/equipment strategy or formula-based optimization is included in the page. |
| Placeholders and fragments | C `server/customizations/LootBoxes/LootBoxItems.cs:377-408`, `:411-436`, `:440-475`: five-fragment tooltip, epic component hint, and explicitly named placeholders. C `server/customizations/LootBoxes/ClusterFLootBoxes.cs:237-239` combines nothing and consumes nothing. The promises are marked (planned). |
| Opening locations and backpack | C `server/customizations/LootBoxes/LootBoxItems.cs:172-211`: guarded region with guards enabled, or house friendship which includes owner/co-owner; same account and the box in the opener's backpack are required. |
| Binding and ordinary contents | C `server/customizations/LootBoxes/LootBoxItems.cs:30-39`, `:144-168` rejects trade, ground, another account, and containers not carried by the account. `:352-373` applies the same restrictions to cosmetic sashes. Ordinary generated gear and supplies have no box-account restriction; see existing binding verification below. |
| Delivery, reveal, and deletion | C `server/customizations/LootBoxes/LootBoxItems.cs:218-282` pays gold/Renown, hands over item contents, clears the contents list, displays reveal, and deletes. C `server/customizations/ClusterFGuildPromotion.cs:233-247` tries the backpack and falls back to BankBox.DropItem. Thus the player does not manually empty the box as a container. |
| Flying loot | C `server/customizations/LootBoxes/ClusterFFlyingLoot.cs:85-129` maps supported item classes and selects the best; `:135-175` skips disabled/muted/unsupported cases and sends private or area effects. C `server/customizations/LootBoxes/LootBoxItems.cs:264-278` invokes it immediately, with tier 4+ major visibility. M P366 records merged art and says package publication remains a separate step. |
| Fanfare and mute | C `server/customizations/LootBoxes/ClusterFFanfare.cs:46-49`, `:73-84`, `:91-125`, `:148-196`, `:202-257`: per-character mute, merged celebrations, chat always sent, capstone broadcast unaffected, minor private and major public effects. Player command is `[FanfareMute`. VoiceHook is unassigned in canonical production customization source; spoken custom voice is (planned). |
| Shop gates and purchase | C `server/customizations/LeagueShop/LeagueShop.cs:126-148`, `:155-206`: account/AP/Renown checks, no registration/range gate, full item-set pack-capacity check, no charge on refusal, exact price after delivery. `LeagueShopGumps.cs:161-240` provides confirmation. Lifetime Renown is untouched. |
| Entire starter price table | C `server/customizations/LeagueShop/LeagueShop.cs:92-120`: each guide reward, AP gate, and price checked against these rows. `:228-237` marks and blesses the Registrar rune. C `server/customizations/LeagueShop/LeagueShopItems.cs:20-34` refuses tabard dye; `:99-134` captures the buyer's name/AP for the trophy. The items are cosmetic/convenience rewards, not stat/skill gear. |
| Shop boxes are separate | C `server/customizations/LeagueShop/LeagueShop.cs:254-305`: Bronze 1 draw/max 0 AP; Silver 2/max 250; Gold 3/max 1,000. Pool is eligible starter cosmetics, conveniences, decor plus bound League sash. Title rows have no item factory, boxes are excluded, and Fill explicitly pays 0 gold/0 Renown. Independent draws can duplicate. Hall rows are separate from Stock. |
| Hall decor | C `server/customizations/LeagueShop/LeagueHall.cs:94-132` defines pieces and bound deeds. `:253-271` gives wall/dye rules; `:310-314` preserves independent part hues and returns the bound deed. `:398-440` checks account/backpack and delegates house/wall placement to BaseAddon.CouldFit. M P243 and existing placement verification confirm owner-only placement. Hall prices were not repeated in this guide. |

## Boss reward finding and contradictions

P263's reported boss-box failure was cross-checked against the current canonical hook and pristine pinned source:

- C `server/customizations/LootBoxes/ClusterFLootBoxes.cs:163-190` subscribes to CreatureDeathEvent and rejects a creature that fails IsBoss.
- C `server/customizations/ClusterFRareSelfRepair.cs:57-60` requires Deleted false.
- Pinned `Projects/UOContent/Mobiles/BaseCreature.cs:3662-3669` calls base.OnDeath before CreatureDeathEvent.
- Pinned `Projects/Server/Mobiles/Mobile.cs:4899-4902` deletes non-player mobiles during that base call.
- A search of the shard's patch files found no replacement of that base/event ordering. The current hook still contains the reported blocker. This is static corroboration, not a fresh runtime reproduction.

The guide therefore describes first-boss boxes as intended but unreliable, and preserves the disagreement between F-40/P79 and P263 in Contradictions. No fix was attempted.

Other contradictions retained: fixed/uncalled loop assumptions versus P371 graduation; historical AP/title totals; no-Renown-spender descriptions versus built shops; empty-box lifecycle language versus immediate handover/deletion; the unverified exceptional-gear comparison; and fragment tooltips versus the unbuilt combination action. These are recorded without selecting a replacement design.

P241 and P231 do not disagree about tabs: category icons/headings were added while Mischief stayed under All. This was checked and was not manufactured into a contradiction.

## Existing test evidence inspected

Read existing verification methods and relevant assertions as source. No test was added or modified, no test suite was run, and no historical green run is claimed as this task's verification.

- C `server/tests/Misc/AchievementCategoryIconsVerification.cs:102-180`: mappings, headings, and no hidden category heading before an earn.
- C `server/tests/Misc/AchievementEarnedLineVerification.cs:97-111`, `:221-330`: descriptions, retired entries, and retained holder state.
- C `server/tests/Misc/AchievementProgressLineVerification.cs:110-183`: no earned progress line, unfinished counters still shown.
- C `server/tests/Misc/AchievementsLayoutVerification.cs:109-245`: layout, full tabs, prerequisite wording.
- C `server/tests/Misc/JokeAchievementsVerification.cs` and `NotedBySystemVerification.cs`: hidden before earning, secret-tagged after, one-time account rewards. Used only to check spoiler handling.
- C `server/tests/Misc/LootBoxFanfareVerification.cs:148-176`, `:187-231`, `:242-309`, `:316-378`: first/repeat, fixed contents, safety locations, binding, merge/mute/broadcast.
- C `server/tests/Misc/LootBoxFlyingLootVerification.cs:160-303`: item mappings/fallback, best item, successful versus refused opening.
- C `server/tests/Misc/LeagueShopVerification.cs:92-239` and its later stock/pool/window cases: exact spend, insufficient AP/Renown, unchanged lifetime/rank, retained AP titles, stock and box restrictions.
- C `server/tests/Misc/LeagueHallVerification.cs:127-240` and later dye/deed cases: gates, spend, bound deed, owner-only placement, independent dye.
- C `server/tests/Tutorial/GraduationLoopVerification.cs:71-99`, `:238-252`: first loop and box once, per-character treatment and skip/remedial behavior.

## Verification and limits

- Read the draft back against the ledger. Every displayed price and threshold comes from the cited tables. No AP ceiling, hidden reward totals, promised exceptional-gear superiority, or slot-as-item count.
- Local Markdown links resolve. The page has no em dashes, source file:line citations, or trailing whitespace. Player commands on it are only `[achievements` and `[FanfareMute`.
- The initial substring-based spoiler scan matched a short hidden title inside the ordinary word "books"; reviewed as a false positive. Final scan uses whole names with word boundaries, plus manual review of hidden titles/rewards and source-link labels.
- No new tests or durable validation gate were introduced, so there is no new red/green requirement. The task's lane-test requirement is none.
- Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE pointing at these work copies: exit 0. The tool still writes progress.json despite its dry-run description. Restored that generated file byte-for-byte to its pre-run contents; README was not rewritten. The docs-only deliverable remains limited to the requested Markdown files.
- No Haven connection, live configuration read, deployment, image build, account change, art generation, commit, merge, push, or branch switch. PowerShell is Windows PowerShell 5.1. No code changes.
- Unverified: deployed build/settings, NPC placement in a running world, player-package publication, client appearance and audio, runtime AP total, runtime reproduction of the existing boss defect, and the promised comparison between box gear and exceptional crafted gear. The page explicitly carries a draft/source-defaults notice.

Final editorial checks passed: all local links resolve in both files; no em dashes or trailing whitespace; no hidden achievement or hidden title names on the page; only the two documented player commands; no code file:line citations on the page. The complete starter-shop AP/price table, free-title names/thresholds, and earned-box base currencies were compared mechanically with current source and matched. Sources precedes the final Contradictions list.

Both repositories passed git diff --check. Final status showed exactly the requested new Markdown files, with the code repository clean. The guide is 13,709 bytes; this note is well below 5 MB. The stop file was absent at the final check. No runtime tests were required or run.

P387 DONE
