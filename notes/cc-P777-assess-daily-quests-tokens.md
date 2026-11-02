# cc-P777: assess daily quests and token rewards

## In plain words

- **Two downloads checked: a daily quest system and a token currency.** Neither goes onto the shard as it is. Their
  rewards break the shard's rules (armour sets stacked with bonuses, 1-million-gold jackpots), and most of what they do
  we already have (the reward stores, the requisitions board, the trash bag that pays points).
- **One good idea to keep: a daily "hunt" board.** Each day, give a player a few kill goals ("cull 10 ettins") on the
  board they already use, paying League Renown and guild points, plus one bigger weekly hunt. That is the League hunts
  piece we planned (F-24) and never built. It would give players a reason to log in and fight every day.
- **For you:** say yes or no to the hunt board prompt sketch below (about one Golem task). Nothing to deploy.

Iron Golem, 2026-11-02. Assessment only, no code. Read the code in `D:\UO\third-party\code\daily-quests` and
`D:\UO\third-party\code\token-system` (nothing built or run) and compared it with our code copy
`D:\UO\golems\Iron\ShatteredLegacy`. Both rows are added to `D:\UO\third-party\CODE-INTAKE.md` as `assess (P777)`.

A naming note: the prompt says "League commissions" and "Legacy Gems". Neither name is in the code or the docs. I read
"League commissions" as the requisitions board (daily refresh, pays Renown) plus the smith commissions, and found no
Legacy Gems currency; the closest currencies are Renown, guild points, Festival Tokens and spendable AP (all P760).

## 1. Each item

### daily-quests (DragnMaw, DailyQuests 1.02, servuo.dev #1539)

**What it does.**

- Three quest-giver NPCs (Combat Master, Craft Master, Boss Master), placed by an XmlSpawner file in every bank.
  Talking to one offers a random quest from its list through the stock Mondain quest gump.
- Combat quests: kill 10 of one creature (titans, ettins, blood elementals, balrons, succubi, two custom ServUO-server
  mobs). Craft quests: hand in 100 iron ingots, leather or boards, or kill 10 of some custom server mobs. The one boss
  quest: kill a Barracoon. Each quest also costs one **Online Ticket**.
- Repeat: 24 hours after the quest (`RestartDelay` 1440 minutes; boss 10,000 minutes, about a week). The delay is
  only applied on refuse in the code shown, so the cooldown as written is shaky.
- **Online Ticket:** a timer drops one ticket in every online player's bank each hour. Opened, it pays 1,000 gold, a 10%
  chance of 5 Sovereigns, a 4% chance of a Combat or Craft ticket, and 1-in-1,000 chances of 1,000,000 gold or 1,000
  Sovereigns.
- **Combat Ticket / Craft Ticket** (quest rewards, loot boxes): 10,000 gold each, a 10% chance of 50 Sovereigns, a 10%
  chance of a set piece (combat) or a 15-use valorite / barbed / heartwood runic tool (craft), and 1% each for 1,000,000
  gold and 1,000 Sovereigns, with a world broadcast.
- **Four 6-piece armour sets** (Wisdom, Archmage, Berserker, Warrior, plus gargoyle versions): artifacts with per-piece
  bonuses and a full-set bonus (Warrior chest: 15 in every resist, HP regen 2, +5 HP, 8 DCI; full set +10 Str/Dex/Int,
  +12 HP, regen 5. Archmage full set: 100 spell damage, FC 2, FCR 6).
- A one-page guide book.

**Size.** 54 .cs, about 4,100 lines; 44 of the files (about 2,400 lines) are set pieces. 68 hand-written Serialize
overrides. Core edit: new values in the `SetItem` enum. Needs XmlSpawner (we have none), ServUO's Mondain quest classes
(`BaseQuest`, `SlayObjective`, `ObtainObjective`, `QuestHelper`) and the Sovereigns wallet. The author says it is
deliberately left not compiling. Saved types: 3 NPCs, 3 ticket items, a guide book, 44 armour pieces, and quest state
on `PlayerMobile.Quests`.

**Terms.** None stated. Credit DragnMaw; private repo and player package only; no repost.

**Fit and overlap.**

| Ours | What it already does | daily-quests adds |
|---|---|---|
| Requisitions board (P150, `Requisitions/RequisitionSystem.cs`) | a personal set of requests that rerolls once a day at a fixed hour, pays Renown, guild standing and gold; slayer rows; Leads | **kill-count goals** ("slay 10 X") and a **weekly** goal; today a slayer row asks for an item, not a count |
| Smith commissions (`ClusterFSmithCommissions.cs`) | repeatable craft orders with an abandon cooldown | nothing (turn in 100 ingots is a thinner version) |
| Achievements and AP store (P760) | one-time goals; AP buys titles and decor | nothing |
| Loot boxes (P759/P763, `LootBoxes/`) | tiered loot boxes with tables, fanfare and counters | nothing better; their tickets are cruder loot boxes |
| Festival Tokens (P760) | first login of the day in season pays 1 | the hourly Online Ticket is a play-time reward, which we chose to keep small and seasonal |
| F-24 League hunts and culls | **not built**: `RequisitionSystem.HuntFamily` is the empty seam, and `ClusterFLeagueBestiary.cs` names the creatures | the shape of a daily hunt: count kills of a family, hand in, cooldown |

So the only new thing is the **daily and weekly kill goal**. Everything else overlaps or breaks the rules.

### token-system (Karmageddon, Karma Tokens, servuo.dev #1303)

**What it does.**

- Every kill pays the killer tokens by a formula on the creature's gold, fame, karma and hit points (`TokenAward.cs`),
  straight into an owner-bound, blessed **Token Box** in the backpack (cap 200 million).
- The box gump takes tokens out as a stack (up to 60,000) or as a **Token Check** (up to 1,000,000) that only a token
  box will cash.
- **Trash 4 Tokens backpack** (Daat99's, modified): non-stackable items dropped in it are deleted after 3 minutes and
  pay 5 to 10 tokens each.
- **Vendor Stone** (Raelis's, modified): a staff-stocked shop that sells any item for tokens or another currency, with
  an optional "(B)" option that sells the item **blessed** (or a pet **bonded**) for an extra price.

**Size.** 6 .cs, about 2,200 lines (the vendor stone is 1,500 of them, ArrayList-era RunUO code). 6 hand-written
Serialize overrides. Core edits: a line in `BaseCreature` where fame and karma are awarded, and a line in character
creation for the box. Saved types: Tokens, TokenBox, TokenCheck, TrashBackpack, VendorStone, VendorBall.

**Terms.** None stated; reworked from Dupre's token system. Credit Karmageddon (and Dupre); private repo only; no repost.

**Fit and overlap.** Almost all covered already.

| Token system part | Ours |
|---|---|
| a per-kill currency | Festival Tokens drop from strong creatures (in season), guild points, Renown from requisitions; we chose earned-on-purpose currencies, not a drip on every kill |
| token box and checks | not needed: P760 currencies are counters on the account or character, nothing to carry or lose |
| Trash 4 Tokens | the trash bag, trash barrel (Guild Store row), `[cleanup` and the mule's Salvage Bin all pay Clean Up Britannia points (`ClusterFCustodianSystem.cs`) |
| vendor stone | the P760 reward stores (`RewardStores/`) with a shared price file, `Configuration/reward-stores.json` |

Nothing new worth taking.

## 2. Rules check

Rule: nothing that grants skill or stat points, power scrolls, bless deeds or property artifacts; items usable now and
mostly helpful.

| Item | Breaks a rule? |
|---|---|
| daily-quests armour sets | **Yes.** They are property artifacts (`IsArtifact => true`), with full-set bonuses far above our loot (75 resists on the Warrior set, 100 spell damage on the Archmage set). |
| daily-quests jackpots | Not a named rule, but 1,000,000 gold from a ticket wrecks the economy. Sovereigns do not exist on our shard. |
| daily-quests runic tools | Allowed on its own (our Guild Stores sell runic tools), but a 10% chance on a daily ticket is far more than our stores' pace. |
| daily-quests hourly Online Ticket | Not a named rule, but it pays for being logged in, which rewards idle play; we kept login rewards to 1 Festival Token a day. |
| daily-quests quest shape (kill 10, hand in 100) | **No.** Safe. |
| token-system vendor stone "(B)" option | **Yes, in effect.** Buying any item blessed for tokens is a bless deed by another name. |
| token-system tokens, box, trash | No rule broken, but a per-kill drip with a 200-million cap is uncontrolled inflation. |

So nothing from either download should ship as written. The safe part is the daily kill-goal mechanic, rebuilt with
our own rewards.

## 3. Recommendation per item

| Item | Call | Reason |
|---|---|---|
| daily-quests | **idea only** (rebuild small) | The daily/weekly kill goal is the one new thing and it fills the empty F-24 hunts seam. The code itself is ServUO quest API, XmlSpawner, Sovereigns and rule-breaking rewards; nothing is worth porting line by line. |
| token-system | **skip** | Every part is already covered (P760 stores and currencies, Clean Up points); the vendor stone's bless option breaks the rules and a per-kill token drip inflates. |

### Ranked ports for Chase

1. **Daily League hunts on the requisitions board** (rebuild from the daily-quests idea; medium, about 500 to 700 lines
   with facts, no new NPC).
   Prompt sketch: "F-24 hunts: fill `RequisitionSystem.HuntFamily` and add kill-count rows to the daily requisitions
   roll (cull N of a League Bestiary family, counted on kill by the player with the most damage), paying Renown, guild
   standing and gold at the row's tier, plus one weekly 'great hunt' row with a bigger payout and a loot box; no new
   currency, no NPC, the board shows progress; facts for counting, refresh and the weekly reset."
   Open choice for Chase in that prompt: whether a hunt row counts party kills, and whether the weekly row pays a
   Silver or Gold loot box.

There is no second port: nothing in token-system is new, and its Trash 4 Tokens backpack is already our trash bag and
Salvage Bin.

## Files

- `notes/cc-P777-assess-daily-quests-tokens.md` (this file).
- `D:\UO\third-party\CODE-INTAKE.md`: two new rows (11-02, `code/daily-quests` and `code/token-system`), Overseer
  `assess (P777)`. Backup of the file before the edit in the session scratchpad.

No code, no build, no docs changes. Nothing run from `D:\UO\third-party`.

P777 DONE
