# P14: what the New Haven quests hand out, and which guild could hand it out instead

Date: 2026-09-30. Agent: Claude Code. Pinned ModernUO `7c9215d97`. **Read-only task.** Nothing written outside
`notes/`; nothing built, run, committed or ported. `D:\ShatteredLegacy` and `D:\UO\ModernUO-pinned` were only read.

**This note reports facts. It does not design the guild route or pick guilds.** Where the code cannot decide a
question, it says so.

> **Headlines**
>
> 1. **26 quests, 26 skills, one item each, handed over on completion.** Nothing goes in the pack at the start.
>    Besides the item, each quest does exactly one other thing: a **15-minute skill-gain acceleration buff** on
>    accept (section 1.3). No title, no bag, no deed. The "Apprentice X" rank in the completion text is words only.
> 2. **The brief's premise is out of date: there are 15 guilds, not 4.** `ClusterFGuildSystem.RegisterAll` registers
>    15 `GuildDef`s. Four have the bespoke NPCs the brief names; the other eleven are bound to stock guildmaster types.
> 3. **Guilds can already hand items to a member, but only in code, hand-written per guild.** There is no data-driven
>    "reward table". Adding a guild's *definition* is one `Register(new GuildDef(...))` call (still code, C#, not
>    config). Making a guild *give something* is an `if (def.Key == ...)` block in `Join` or a button in a gump.
>    **So the proposal is a build, not configuration.** Section 2.2.
> 4. **The gap: 19 of the 26 quest skills have no guild keyed to that skill.** 7 do. Against the four guildmasters
>    the brief names, the gap is 24. Section 3.
> 5. **Membership is per account; quest rewards are per character.** This is the one structural mismatch a
>    replacement has to answer (section 2.4).

---

## 1. What the quests hand out

### 1.1 Where the list lives

The board holds **types, not skills**: `NewHavenQuestBoard.QuestTypes` (`NewHavenQuestBoard.cs:52-62`), 26 `typeof`s.
The skill is on each quest's objective, which is why a grep for `SkillName.` in the board finds nothing. The quest
definitions are **pinned's**, not ours:

- `D:\UO\ModernUO-pinned\Projects\UOContent\Engines\ML Quests\Definitions\NewHavenSkillTraining.cs`, lines 10-642.
- Our tree has **no override** of that file. `server/customizations/Engines/ML Quests/Definitions/` holds only
  `AthenaeumIsle.cs`; nothing in `docker/uo/apply-patches.sh` replaces `NewHavenSkillTraining.cs`.

**Counted:** 26 `class ... : MLQuest` in lines 10-642 of that file, the same 26 as the board's table, same order.

### 1.2 The 26

Every quest is built identically: `Activated = true`, `OneTimeOnly = true`, title and text clilocs,
**one** `GainSkillObjective(skill, 500, true, true)` and **one** reward. Every reward is an `ItemReward`, which the
stock ML path creates when the player accepts the reward gump **after reporting back**. Nothing is given on accept.

| # | Quest (class) | Skill | Reward item (type) | Line | Our tree changes the item? |
|---|---|---|---|---|---|
| 1 | CleansingOldHaven | Chivalry | Bulwark Leggings (`BulwarkLeggings`) | 27-29 | no |
| 2 | TheRudimentsOfSelfDefense | Wrestling | Gloves of Safeguarding (`GlovesOfSafeguarding`) | 51-53 | no |
| 3 | CrushingBonesAndTakingNames | Macing | Churchill's War Mace (`ChurchillsWarMace`) | 75-77 | no |
| 4 | SwiftAsAnArrow | Archery | Heartseeker (`Heartseeker`) | 98-100 | no |
| 5 | EnGuarde | Fencing | Recaro's Riposte (`RecarosRiposte`) | 122-124 | no |
| 6 | TheArtOfWar | Tactics | Arms of Armstrong (`ArmsOfArmstrong`) | 146-148 | no |
| 7 | TheWayOfTheBlade | Swords | Jockles' Quicksword (`JocklesQuicksword`) | 170-172 | no |
| 8 | ThouAndThineShield | Parry | Escutcheon de Ariadne (`EscutcheonDeAriadne`) | 194-196 | no |
| 9 | DefyingTheArcane | MagicResist | Bracelet of Resilience (`BraceletOfResilience`) | 218-220 | no |
| 10 | StoppingTheWorld | Meditation | Philosopher's Hat (`PhilosophersHat`) | 241-243 | no |
| 11 | ScribingArcaneKnowledge | Inscribe | Hallowed Spellbook (`HallowedSpellbook`) | 265-267 | no |
| 12 | TheMagesApprentice | Magery | Ember Staff (`EmberStaff`) | 289-291 | no |
| 13 | ScholarlyTask | EvalInt | Ring of the Savant (`RingOfTheSavant`) | 312-314 | no |
| 14 | TheRightToolForTheJob | Tinkering | Amelia's Toolbox (`AmeliasToolbox`) | 336-338 | no |
| 15 | KnowThineEnemy | Anatomy | Tunic of Guarding (`TunicOfGuarding`) | 360-362 | no |
| 16 | BruisesBandagesAndBlood | Healing | Healer's Touch (`HealersTouch`) | 384-386 | no |
| 17 | TheInnerWarrior | Focus | Clasp of Concentration (`ClaspOfConcentration`) | 408-410 | no |
| 18 | TheArtOfStealth | Ninjitsu | Silver Serpent Blade (`SilverSerpentBlade`) | 431-433 | no |
| 19 | BecomingOneWithTheShadows | Hiding | Bag of Smoke Bombs (`BagOfSmokeBombs`) | 454-456 | no |
| 20 | WalkingSilently | Stealth | Twilight Jacket (`TwilightJacket`) | 477-479 | no |
| 21 | EyesOfARanger | Tracking | Walker's Leggings (`WalkersLeggings`) | 501-503 | no |
| 22 | TheWayOfTheSamurai | Bushido | The Dragon's Tail (`TheDragonsTail`) | 524-526 | no |
| 23 | TheAllureOfDarkMagic | Necromancy | **Complete** Necromancer Spellbook (`NecromancerSpellbook`, all spells) | 547-570 | no |
| 24 | ChannelingTheSupernatural | SpiritSpeak | Bag of Necromancer Reagents (`BagOfNecromancerReagents`) | 591-593 | no |
| 25 | TheDeluciansLostMine | Mining | Jacob's Pickaxe (`JacobsPickaxe`) | 615-617 | **yes, replaced** |
| 26 | ItsHammerTime | Blacksmith | Hammer of Hephaestus (`HammerOfHephaestus`) | 639-641 | **yes, replaced** |

26 distinct skills, 26 distinct items. Item classes are all in pinned `Items/New Haven Quest Rewards/`, except the
spellbook (`Items/Skill Items/Magical/NecromancerSpellbook.cs`), which is a stock spellbook the quest fills in its own
`InternalReward.CreateItem` (`Content = (1ul << BookCount) - 1`). **That is the only reward with custom creation
logic;** anything else handing it out has to reproduce the "full book" step or it hands out an empty one.

**Two rewards are already ours, and already tied to a guild.** Both are replaced at build time
(`docker/uo/apply-patches.sh:241-249`):

- **Jacob's Pickaxe** (`server/patches/JacobsPickaxe.cs`): a Miners' Compact legacy tool. On first acquisition
  (`OnAdded`) it unlocks the restoration-registry key `legacy.jacobs_pickaxe` for the account. When exhausted, the
  **Miners' Compact Liaison** will issue a fresh one (`MinersCompactLiaisonGump.cs:1142-1211`), but only to a
  Compact member who **has already unlocked it**: `HasUnlocked(acct, "legacy.jacobs_pickaxe")`. The first copy still
  comes from the quest (or from an admin `Unlock`, `ClusterFCompactAdminTools.cs:133`).
- **Hammer of Hephaestus** (`server/customizations/HammerOfHephaestus.cs`): a Society of Smiths legacy tool with tiers
  and metal familiarity. The smiths' `HammerRestoreGump` **recharges a hammer already in the pack**
  (`HammerOfHephaestus.cs:1193-1236`); it does not issue one. The first copy comes only from the quest.

So for these two, the quest is today the **only** source of the first copy, and a guild handles everything after.

### 1.3 What the quests do besides give an item

Read off the quest classes and the stock objective; nothing else is overridden in any of the 26.

| Effect | Where | Notes |
|---|---|---|
| **Skill-gain acceleration buff** | all 26 pass `accelerate: true` (4th argument). `GainSkillObjective.cs:122-147` | On **accept**: `AcceleratedSkill = skill`, `AcceleratedStart = now + 15 min`. While it runs, each stock gain on that skill is multiplied by `Utility.RandomMinMax(2, 5)` (`SkillCheck.cs:245-248`). Ended on completion or cancel. Shares one slot with Scrolls of Alacrity (`ScrollofAlacrity.cs:62-100`). |
| Rank words | `CompletionNotice`, e.g. 1077725 "You have achieved the rank of Apprentice Paladin" | **Text only.** No title, no property, no flag is set. |
| One-time lockout | `OneTimeOnly = true`, per character's `MLQuestContext` | The done-record is what stops a second reward. |
| 50-point offer lockout | `GainSkillObjective.CanOffer`, line 58 | Not a reward; the reason D-90 exists. |

**Nothing else:** no bag, no deed, no gold, no title, no karma or fame, no stat, no follow-on quest (the board's own
fact pins that none is chain-triggered or has a `NextQuest`, `notes/new-haven-quest-picker.md` section 6).

**The buff under our gain rates, unverified.** `ClusterFSkillGain` wraps the stock skill-check handlers and repeats
the stock gain call (`ClusterFSkillGain.cs:105, 128`); the acceleration multiplier sits inside stock `Gain`, so by
reading it would apply on top of our multiplier. Not measured. Whether it matters at all when 50 arrives in minutes
is a design question, not a code one.

**Out of scope, noted so it is not assumed covered:** `ClusterFNewHavenSeeder` also seeds 13 NPCs that are not
skill trainers (Sir Helper, Andric, Kashiel, Asandos, Clairesse, Gervis, Mugg, Lowel, Lyle, Nibbet, Norton, Sadrah,
Hargrove; `ClusterFNewHavenSeeder.cs:13-25`). Their quests are not on the board and were **not examined**.

---

## 2. What a guild can currently do

### 2.1 The guilds and their keys

**15 guilds**, `ClusterFGuildSystem.cs:89-241`, counted as `Register(new GuildDef` = 15. (The class's own doc
comment says "all 12 guilds"; it is stale.) Each is **one skill** (or none) plus an optional tribute item:

| Key | Name | Bound NPC type (exact type) | Join task | Skill keyed |
|---|---|---|---|---|
| smithing | Smiths' Fellowship | `BlacksmithGuildmaster` (stock) | Blacksmith 50 **or** 10 iron ingots | Blacksmith |
| arcane | Arcane Society | `MageGuildmaster` (stock) | Magery 50 or 5 blank scrolls | Magery |
| tailoring | Tailors' Circle | `TailorGuildmaster` (stock) | Tailoring 50 or 10 cloth | Tailoring |
| tinkers | Tinkers' Union | `TinkerGuildmaster` (stock) | Tinkering 50 or 5 gears | Tinkering |
| healers | Healers' Covenant | `HealerGuildmaster` (stock) | Healing 50 or 25 bandages | Healing |
| bards | Bards' Consortium | `BardGuildmaster` (stock) | Musicianship 30 | Musicianship |
| thieves | Thieves' Den | `ThiefGuildmaster` (stock) | Stealing 20 | Stealing |
| warriors | Warriors' Brotherhood | `WarriorGuildmaster` (stock) | Tactics 30 | Tactics |
| mining | Miners' Compact | `MinerGuildmaster` (stock) | Mining 50 or 20 iron ore | Mining |
| rangers | Rangers' League | `OutridersGuildmaster` (ours) | Archery 30 or 25 arrows | Archery |
| maritime | Maritime Brotherhood | `FisherGuildmaster` (stock) | Fishing 30 or 5 fish | Fishing |
| merchants | Merchants' Exchange | `MerchantGuildmaster` (stock) | 500 gold, no skill | (none; `ItemID` dummy) |
| foresters | Foresters' Union | `ForestersGuildmaster` (ours) | Lumberjacking 50 or 20 boards | Lumberjacking |
| artificers | Artificers' Order | `ArtificersGuildmaster` (ours) | Imbuing 20 or 3 diamonds | Imbuing |
| custodians | The Custodians | `SanitationWarden` (ours) | always eligible | (none; `ItemID` 0.0) |

The brief's "Outriders" guildmaster is the **rangers** key; its "Smiths" is **smithing** on the stock
`BlacksmithGuildmaster`. The Miners' Compact Liaison is a separate `BaseCreature` that opens the mining gump; the
`GuildDef` itself is bound to stock `MinerGuildmaster`.

**Is adding a guild data or code?** Code. A `GuildDef` is a C# constructor call in `RegisterAll`; there is no JSON or
config source. The definition carries **one** `SkillName`, so a guild is keyed by exactly one skill. The NPC link is
by **exact type** (`_byNpc[def.GuildmasterType]`, lookup `GetDefForGuildmaster(GetType())`), so one type maps to one
guild and a subclass maps to none. (Side observation, not investigated: the five `Gargoyle*Guildmaster` subclasses
in `ClusterFGargoyleVendors.cs:309-345` therefore get no guild entry.)

### 2.2 Can a guild give a member an item? Yes, but only as hand-written code

**This is the load-bearing answer: every existing item hand-over is bespoke C#.** There is no generic
"guild gives item X" mechanism and no reward table. What exists:

| Mechanism | Where | Which guilds | Shape |
|---|---|---|---|
| **Join bonus**, dropped in the pack by `Join` | `ClusterFGuildSystem.cs:315-394` (`Join`) | mining (satchel, logbook, ledger), smithing (`SmithGuildBook`, `SmithGuildSalvageBag`), rangers (crook, satchel), foresters (logbook, satchel), custodians (trash bag, via `SanitationWarden.OnCustodiansJoined`), artificers (satchel, toolkit) | an `if (def.Key.Equals("..."))` block per guild. **6 of 15** have one; 9 give nothing but rep and scrip. |
| **Re-issue a lost starter item** | `OutridersGuildmasterGump.cs:352,389`; `ForestersGuildmasterGump.cs:378,413`; `MinersCompactLiaisonGump.cs:766-776` | rangers, foresters, mining | a button per item in that guild's own gump |
| **Tiered tool upgrade / restoration** | `MinersCompactLiaisonGump.cs:883-962, 1142-1290`; `HammerOfHephaestus.cs:1193-1283` | mining (pickaxes, satchels), smithing (hammer) | costs scrip + materials + gold; uses the restoration registry (below) |
| **Scrip shop** | `SanitationWardenGump.cs:162-290` | custodians (bandages, refresh and heal potions, trash bag) | fixed list of buttons, each a lambda |
| **Cross-guild exchange** | `CrossGuildExchangeGump.cs:128-198` | four currencies, including 25 Smithing Seals | one item: a `PackMuleDeed` |
| **Contract rewards** | `GuildContractLedgerGump.cs:521` | per guild | **gold only** |
| **Smithing Seals** | earned from BODs, work orders and salvage (`SmithGuildSalvageBag.cs:260-271`) | smithing | a currency (`ClusterFAccountData.GuildCurrency["smithing"]`). The info gump says Seals "may be spent on guild rewards as your rank grows" (`SmithGuildmasterGump.cs:390`); **the only things I found them buying are the hammer restore/upgrade and the Pack Mule deed.** |

**One reusable piece does exist: `ClusterFRestorationRegistry`** (`ClusterFRestorationRegistry.cs:115-200`). Per
account, arbitrary string keys (`legacy.*`), with `Unlock(acct, key, source)`, `HasUnlocked`, `HasActiveCopy`,
`TryRestore` and a one-active-copy rule. Its `Source` field already anticipates `"quest"`, `"admin"`,
`"guild_contract"`, `"legacy_migration"`. It is **bookkeeping, not delivery**: it records entitlement and whether a
copy exists; every caller still writes its own `new Item()` and `DropItem`. Today only the pickaxe and hammer
families use it.

**What that means for the design conversation, stated as fact rather than recommendation:** delivering 26 quest items
through guilds means writing code in `ClusterFGuildSystem.Join` and/or guild gumps, and for most of the 26 also
writing new `GuildDef`s. Nothing is a config change. The single choke point for every join is
`ClusterFGuildSystem.Join` (called from `GuildTaskDetailGump.cs:813-814`, `SmithGuildmasterGump.cs:323`,
`SanitationWardenGump.cs:337`; no other code adds to `JoinedGuilds`).

### 2.3 What joining requires, and whether a new character can meet it

`CanJoin` (`ClusterFGuildSystem.cs:261-313`): **skill `Base` >= threshold, or the tribute stack in the backpack**
(consumed on join if the skill check failed), or both for `SkillOrItem`. Note it reads `Skills[..].Base`; the quests
read `Skills[..].Fixed` when `useReal` is set, which includes item bonuses.

For a brand new character with no skill:

- **Always:** custodians (no requirement).
- **Yes, with starting gold:** merchants (500 gold; a new character is packed 1,000, `CharacterCreation.cs:154`).
- **Yes if they can buy or gather the tribute:** the ten `SkillOrItem` guilds (ingots, scrolls, cloth, gears,
  bandages, ore, arrows, fish, boards, diamonds). **Which New Haven vendors sell each tribute was not checked.**
- **No, until trained:** bards (Musicianship 30), thieves (Stealing 20), warriors (Tactics 30). At our gain rates
  that is minutes of play, not a wall; not measured.

**Where you can join from.** Not only the NPC. `[guild` is `AccessLevel.Player` (`ClusterFGuildSystem.cs:88`) and
opens `GuildProgressGump`, which lists all 15 with a View button on every row, member or not
(`ClusterFGuildSystem.cs:596-637`). View opens the guild's join screen through `OpenMemberServices`, and its Join
button calls `Join`. **By reading, a player can join any of the 15 from anywhere without meeting a guildmaster.**
Not exercised in a client or a test.

### 2.4 Per account, not per character

`JoinedGuilds`, reputation, scrip and the restoration registry all live on `ClusterFAccountData`, keyed by account.
The quests are per **character**: `OneTimeOnly` is checked against each `PlayerMobile`'s `MLQuestContext`, so each
character on an account can earn each of the 26 once. The join bonuses fire in `Join`, which a second character on
an already-joined account never reaches (`CanJoin` returns "Already a member."). **So today a join bonus is once per
account, a quest reward is once per character.** Which of those the replacement should be is Chase's call; the code
does not decide it.

---

## 3. The gap

Matching rule used: **a guild covers a quest if the guild's `TaskSkill` is the quest's skill.** That is the only
link the code has; whether, say, the warriors cover Swords is a design decision, not a fact.

**Covered: 7 of 26.**

| Quest skill | Guild key |
|---|---|
| Archery | rangers |
| Tactics | warriors |
| Magery | arcane |
| Tinkering | tinkers |
| Healing | healers |
| Mining | mining |
| Blacksmith | smithing |

**No guild keyed to the skill: 19 of 26.**

Chivalry, Wrestling, Macing, Fencing, Swords, Parry, MagicResist, Meditation, Inscribe, EvalInt, Anatomy, Focus,
Ninjitsu, Hiding, Stealth, Tracking, Bushido, Necromancy, SpiritSpeak.

(Counted: 7 + 19 = 26, each skill once.)

**Against only the four guildmasters the brief names** (rangers, foresters, artificers, smithing): 2 covered
(Archery, Blacksmith), **24 uncovered**. Foresters (Lumberjacking) and artificers (Imbuing) match no quest.

**Guilds with no quest:** tailoring, bards, thieves, maritime, merchants, foresters, artificers, custodians (8 of 15).

**Of the 7 covered, 3 already give items on join** (smithing, mining, rangers).
Arcane, tinkers, healers and warriors give nothing but rep and scrip today.

---

## 4. How visible the guildmasters are

Measured from the arrival tile, **(3503, 2574, 14) Trammel** (`CharacterCreation.cs:114`), in tiles (Chebyshev, which
is how update range is measured). The default update range is **18** (`Main.cs:150`), so within 18 is on a new
character's screen when they arrive; beyond it they must walk. The training board stands at (3502, 2573), 1 tile.

| NPC | Guild | Location (Trammel) | Distance | Source |
|---|---|---|---|---|
| Sanitation Warden | custodians | 3506, 2560, 21 | **14** (on screen, but at z 21, the civic hall) | `ClusterFInstitutionSeeder.cs:61-68` |
| Outriders' Guildmaster | rangers | 3524, 2574, 7 | 21 | `ClusterFInstitutionSeeder.cs:71-78` |
| TailorGuildmaster | tailoring | 3494, 2551, 20 | 23 | stock spawner |
| BlacksmithGuildmaster | smithing | 3526, 2536, 20 | 38 | stock spawner |
| BlacksmithGuildmaster | smithing | 3469, 2536, 41 | 38 | stock spawner |
| HealerGuildmaster | healers | 3463, 2558, 36 | 40 | stock spawner |
| MageGuildmaster | arcane | 3495, 2527, 27 | 47 | stock spawner |
| TinkerGuildmaster | tinkers | 3458, 2524, 53 | 50 | stock spawner |
| Artificers' Guildmaster | artificers | 3490, 2627, 0 | 53 | `ClusterFInstitutionSeeder.cs:101-108` |
| Foresters' Guildmaster | foresters | 3441, 2637, 28 | 63 | `ClusterFInstitutionSeeder.cs:81-88` |
| Miners' Compact Liaison | mining (gump only) | 3510, 2748, 0 | 174 (south mine) | `ClusterFInstitutionSeeder.cs:40-47` |
| Artificers' Guildmaster | artificers | Ter Mur 797, 3431, -10 | other facet | `ClusterFInstitutionSeeder.cs:91-98` |

"Stock spawner" = pinned `Distribution/Data/Spawns/post-uoml/trammel/Vendors.json`, filtered to New Haven's box
(`IsNewHavenArea`, x 3400-3560, y 2400-2760). **Unverified that this spawn set is the one generated on live**, and
unverified that the spawners have produced their NPCs; a live `[where` or a world query would settle it.

**Not found in New Haven's box:** the stock guildmasters for warriors, thieves, bards, maritime, merchants and
mining (`WarriorGuildmaster`, `ThiefGuildmaster`, `BardGuildmaster`, `FisherGuildmaster`, `MerchantGuildmaster`,
`MinerGuildmaster`). **Warriors is one of the 7 covered guilds and has no guildmaster in New Haven.** Neither does
mining's bound type; only the Liaison, 174 tiles south.

**Does a new character meet one unprompted?** Only the Sanitation Warden is within update range of the arrival tile,
and it is upstairs. None of the custom guildmasters shouts or reacts to movement (no `CanShout` or `OnMovement` in
`OutridersGuildmaster.cs`, `ForestersGuildmaster.cs`, `ArtificersGuildmaster.cs`, `MinersCompactLiaison.cs`,
`SanitationWarden.cs`); stock guildmasters were not checked. The trainers, by contrast, do shout
(`CanShout => true` on each, e.g. `NewHavenSkillTraining.cs:672`). The `[guild` command reaches all 15 from anywhere,
but a player has to know it exists. **Whether any in-game text points new players at `[guild` was not checked.**

---

## 5. Proposed register entry (text only; `docs/` not edited)

For `docs/fidelity-principle.md`, same columns as the existing rows. **D-92 is the next free number at time of
writing** (the register ends at D-91; `notes/index-blindspots.md:493` leaves D-92 open). Whoever promotes it confirms
the number then. The entry is written against the *proposal*, not a design, so the bracketed parts are for Chase's
design to fill.

| # | What | Player-visible effect | Class | Source |
|---|---|---|---|---|
| D-92 | **The New Haven training quests' item rewards are obtained through NPC guild membership instead of (or as well as) completing the quest.** The 26 quests are stock ML (`NewHavenSkillTraining.cs`, pinned), each a `GainSkillObjective` to 50 with one `ItemReward` on completion and a 15-minute skill-gain acceleration on accept. On this shard gain runs at roughly 15x stock (`clusterf.skillGain.chanceAttempts` 3, `amountMultiplier` 5, live `modernuo.json`), so the skill half is overshot before it registers and the quest reduces to an item hand-out; the change moves the hand-out. [Which guilds, which items, once per account or per character, and whether the quests stay offered: per the design.] | a player gets Recaro's Riposte, Jacob's Pickaxe and the other 24 [by joining the matching guild] rather than by reporting to the trainer. A wiki says "complete the trainer's quest"; here it is [guild route]. The items themselves are unchanged. | `ours` | `cc-P14-newhaven-guild-mapping` + the design note |

**Relation to D-90:** D-90 (the board) rests on the same premise, our gain rate. If the quests stop being the way
items are obtained, D-90's "reverses when" (stock gain rates) applies to this entry too, and D-90 itself may become
unnecessary. That is a consequence to record, not a decision made here.

---

## 6. Premises in the brief that did not hold

- **"Four guildmasters exist."** Four *bespoke* guildmaster NPCs exist; the guild system has **15** guilds, eleven on
  stock guildmaster types. Section 2.1.
- **"Membership is keyed by skill string."** It is keyed by a **guild key** (`"smithing"` is the key, not a skill
  name; `"arcane"`, `"rangers"` and `"custodians"` show the key and skill are separate). Each key carries one
  `SkillName`.
- **"A grep for `SkillName.` in the board returns nothing"**: correct; the skills are in pinned's quest
  definitions. Section 1.1.

## 7. Not verified

- Which stock guildmasters are actually standing on live (spawn set and generation), section 4.
- Which New Haven vendors sell each tribute item, section 2.3.
- The acceleration buff's interaction with `ClusterFSkillGain`, section 1.3: by reading only.
- `[guild` join from a distance, section 2.3: by reading only, not exercised.
- The 13 non-trainer New Haven quest NPCs: not examined.
- Whether any in-game text directs players to `[guild` or to a guildmaster.

## 8. Questions opened

None. The two things the code cannot decide (what "covers" means across skills, and per-account versus
per-character entitlement) are named in sections 3 and 2.4 for the design conversation.
