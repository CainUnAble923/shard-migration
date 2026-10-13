# cc-P82: Artificers' Order Imbuing rework

Builder prompt: `D:\UO\cc-prompts\cc-P82-artificers-imbuing.md`. Source of truth: `docs\artificers-imbuing-design.md`
(read, not copied or edited). Code in `D:\ShatteredLegacy`; image `sl-modernuo:cc-p82`. Not committed (autopilot).

## 1. What already existed (research, before any code)

- **Imbuing is entirely ours.** ServUO's imbuing (weights, soul forge checks, unravel, reinforce) was never ported.
  Ours is `server\customizations\ArtificersImbueGump.cs`: a property catalogue (`ImbueCatalogue`, 62 rows before this
  task), and a gump with imbue, disenchant (unravel), extract and craft-essence stages. Before cc-P82 its strength came
  from the character's Artificers' standing: an intensity cap of 100% to 200% and 5 to 8 property slots
  (`GetIntensityCap`, `GetMaxPropertySlots`), a Master Artificer gate on Self Repair (cc-P42) and a Journeyman gate on
  imbuing an already enchanted item. Essence "discovery" (mastery after N essence uses, account-wide
  `ImbuingDiscoveries`) is separate and kept as is.
- **Recipe gating (cc-P78)** is what the prompt says to reuse: the account-wide `ClusterFAccountData.LearnedRecipes`
  set (`ClusterFRecipeStore`), the rank index 0 to 5 (`ClusterFGuildSystem.GuildRankIndex`), guild currency through
  `GuildResources.TryPay`, the trial (`ClusterFGuildPromotion.TrialDone`) and the hint style. All reused; nothing
  parallel was built.
- **ServUO** (`D:\UO\ServUO-pub57`, read only): `Imbuing.cs` `m_SkillGroups` (OSI's five +skill groups, slot j = group
  j) and `CheckSoulForge` (soul forge art IDs 0x4263 to 0x4272, 0x4277 to 0x4286, 17607 to 17610; Queen's Palace bonus
  0.06, Royal City 0.02, any other forge 0).
- **Reinforce does not exist** anywhere here (no reinforcing powder, no reinforce step). Nothing to keep free; reported
  in section 6.

## 2. What was built

New folder `server\customizations\Imbuing\`:

| File | What |
|---|---|
| `ImbuingTable.cs` | The config table, `Configuration/imbuing.json` (written with the defaults when missing; a bad file is refused whole; `[ImbueKnowledge reload`). |
| `ClusterFImbueKnowledge.cs` | Account knowledge, tiers, the grant API, the ladder, books read, slots and budget, hint lines, `[ImbueKnowledge`. |
| `ImbueSites.cs` | Where an imbue happens (soul forge, mule socket II and III, anywhere) and the `ArtificersSoulForge` hall forge item. |
| `ImbueFormulaBooks.cs` | `ImbueFormulaBook` (one item class, contents from config), the shop and its gump, and the staff gump. |
| `ClusterFImbueEffects.cs` | The custom property store (`ImbueCustomStore`, its own save file) and every custom effect. |

Changed: `ArtificersImbueGump.cs` (catalogue and gump), `ArtificersGuildmasterGump.cs` (text, dashboard, Formula
Books button), `CompactOreSatchelRoutingHook.cs` and `ClusterFLumberjackingExtension.cs` (gathering hook),
`ClusterFHuntersSatchelHooks.cs` (carving hook), `Mobiles\Evo\EvoPet.cs` (Bond XP), `LootBoxes\LootBoxRoller.cs` and
`LootBoxes\ClusterFLootBoxes.cs` (Fortune's Favor and the box hook), `ClusterFAchievements.cs` (two achievements),
`Engines\Craft\ClusterFRecipeStore.cs` (names imbue keys in its lists), `Mobiles\Mule\MuleModuleData.cs` (the socket's
tier lines). New patch `server\patches\Imbue-custom-property-hooks.patch`, registered last in
`docker\uo\apply-patches.sh`. `CHANGELOG.md` and `VERSION` (2026.10.13.5).

By the prompt's numbered build list:

1. **Known imbue properties, account-wide.** Keys in `LearnedRecipes`: `imbue:<property>:<tier>`, `imbue:book:<id>`,
   `imbue:formulary:master`. Known tier = the highest key; a free property is Basic with no key. `LearnedRecipes` is
   already saved (ClusterFAccountData v17) and kept through loops and resets, so no version bump. A "property" is a
   knowledge key: a catalogue row's name or a family several rows share (`ImbueFamilies`: Elemental Damage, Jewelry
   Skill Bonus, Crafter Skill Bonus, Slayer, Super Slayer).
2. **Tiers.** Basic = OSI max x 0.333, Refined = x 0.667, Full = the OSI max (the catalogue's `MaxVanilla`),
   Overcharged = `overchargedMax` (default: the catalogue's old guild maximum, `MaxGuild`). All in the one config file.
   Imbuing is clamped to the known tier and the place's cap (`HandleApplyImbue`). Costs and difficulty are now by value
   over Full (no standing): difficulty 40 to 100 at Full, up to 120 at the top of Overcharged.
3. **Ladder and tier table.** `ImbuingTable.DefaultLadder()` is the design's property ladder by key;
   `BooksFromLadder` is the design's table as books (a property learned at rank L gets tier t from the rank L + t - 1
   book, never past Full; rank 5 is the Master Formulary). A test checks every (property, tier) against the table.
4. **Formula books.** Sold at the Artificers' guildmaster (Member Dashboard, "Formula Books") from their rank, for
   Essence Shards only (`GuildResources.TryPay`, gold 0). Contents are config (`books`), one item class. Reading
   teaches the account and consumes the book; a read book is not sold again and a second copy is refused.
5. **Master Formulary.** Rank 5, needs the trial (`TrialDone`) to be sold and to be read. Default: +1 slot (6).
   `masterMode: "budget"` keeps 5 slots and raises the item's intensity budget (sum of value over Full) from 500% by
   `masterBudgetPercent` (100).
6. **The 140+ grant API.** `ClusterFImbueKnowledge.Grant(ClusterFAccountData, key, ImbueTier)` (and a `PlayerMobile`
   overload that tells the player). Takes any catalogue key or family, and the grant-only keys Splintering, Reactive
   Paralyze, Soul Charge and Casting Focus. Never lowers; refuses Overcharged where a property has none.
7. **Hidden menu.** The view lists only known rows; one hint line per category with anything locked ("Weapon: 5 more
   properties and 2 higher tiers locked. Learn more: formula books from Artificers' rank Journeyman, the 140+ path.").
   The tier stage offers only known tiers; a known tier the place does not allow shows greyed with where it can be had.
8. **Unravel and Reinforce.** Disenchant and extract were already ungated; they still are (a test proves a non-member
   with nothing learned extracts). Reinforce does not exist (section 6).
9. **+Skill.** 30 jewelry rows (OSI's five groups, each its own AosSkillBonuses slot, so one skill per group) and 12
   crafter rows (crafting in slot 0, gathering in slot 1) on crafter gear (`crafterGearTypes`: HalfApron, FullApron by
   default; tool belts and guild gear do not exist, add their type names when they do). Combat skills only on jewelry.
   Tiers 5, 10, 15, 25. **Skill gain:** verified, nothing to fix: `Skills.Total` is the sum of Base, `SkillCheck.Gain`
   adds to Base and checks `Base < Cap` and `Total < Cap` (pinned `SkillCheck.cs:236-276`), and `ClusterFSkillGain`
   only widens a window that ends at the cap by the worn bonus so the bonus cannot stop a gain early
   (`ClusterFSkillGain.cs:205-212`). A test pins it.
10. **Custom properties.** All 11, values and ingredients in `custom`, one per item (`BlockedBy`). Wiring in section 4.
11. **Mule soul forge.** `ImbueSites`: socket II caps at Refined, no bonus; III at Full with the forge bonus; never
    Overcharged; Overcharged only within 2 tiles of a soul forge (OSI art or the new `ArtificersSoulForge`).
12. **XmlLevelItems.** Nothing here makes an item levelable: no XmlLevelItems exist in this build (searched), and the
    imbue code sets only attributes and the custom store. Nothing to change.
13. **Achievements.** Hidden "Dressed for the Occasion" (1 box) and "Creature of Habit" (25), with the design's text;
    Fortune's Favor equip time per item (the patched `PlayerMobile.OnItemAdded`), a 60 second window (config).
14. **Staff.** `[ImbueKnowledge` (GameMaster): target a player, a gump of every key with + (next tier) and - (revoke the
    top tier) and a Master Formulary toggle; every change is logged. `[ImbueKnowledge reload` rereads the config.

## 3. Config file

`Configuration/imbuing.json` (server Configuration folder; written with the defaults on first start). Fields:
`basicFraction`, `refinedFraction`, `overchargedMax` (per property), `ladder`, `books` (id, name, rank, price,
masterFormulary, grants), `baseSlots`, `masterMode`, `masterExtraSlots`, `masterBudgetPercent`, `siteCaps` (Anywhere,
MuleII, MuleIII, Forge), `forgeBonusPercent` (2), `queensForgeBonusPercent` (6), `forgeRange`, `muleRange`,
`crafterGearTypes`, `custom` (per property: effect, full, overcharged, applies, ingredient, ingredientAmount, shards,
gold), `effects` (Shatter drop and seconds, Butcher's Eye rare chance and parts, Prospector finds, Fortune's Favor cap
and window). Proposed ingredient mapping (existing imbuing ingredients, which are monster parts):

| Property | Full | Overcharged | Goes on | Ingredient |
|---|---|---|---|---|
| Echo of the Loop | 10% | 15% | anything | 5 Undying Flesh |
| Time Slip | 5% | 8% | weapons | 5 Vial of Vitriol |
| Shatter | 10% (-10 for 5 s) | 15% | weapons | 5 Crushed Glass |
| Bond | 10% | 15% | armor, jewelry, clothing | 5 Reflective Wolf Eye |
| Spell Leech | 5% | 8% | weapons, jewelry | 5 Daemon Claw |
| Renowned | 10% | 15% | anything | 5 Goblin Blood |
| Bountiful | 15% | 22% | armor, jewelry, clothing | 5 Spider Carapace |
| Mastercraft | 5% | 8% | armor, jewelry, clothing | 5 Lava Serpent Crust |
| Prospector | 10% | 15% | armor, jewelry, clothing | 5 Slith Tongue |
| Butcher's Eye | 20% | 30% | anything | 5 Raptor Teeth |
| Fortune's Favor | 5% (cap 10% worn) | none | anything | 5 Faery Dust |

## 4. Custom properties: where each runs

| Property | Wired to | How |
|---|---|---|
| Bountiful | `CompactOreSatchelRoutingHook.Give`, `ClusterFLumberjackingExtension.Give` | the gathered stack grows by the percent (remainder by chance) |
| Prospector | same two | a percent chance of a rare find (`effects.prospectorMining` / `prospectorLumber`) |
| Butcher's Eye | `Corpse.OnItemAdded` partial (carving) and the creature death event (kills) | carved stacks and a kill's monster parts grow; a small chance at a rare part |
| Mastercraft | patch: `CraftItem.GetExceptionalChance` | adds the percent to the exceptional bonus |
| Time Slip | patch: `BaseWeapon.OnHit` + `WeaponAbility.ClearCooldown` | a hit whose special move ran: chance to refund its mana and end the 3 s double-cost window |
| Shatter | patch: `BaseWeapon.OnHit` | chance to drop the target's highest resist by 10 for 5 s |
| Bond | patch: `BaseWeapon.OnHit`; `EvoPet.OnCreatureDeath` | a companion's melee damage and an evo pet's XP, by its master's worn Bond |
| Spell Leech | patch: `SpellHelper.Damage` | the caster heals the percent of spell damage dealt (immediate and delayed spells both pass here) |
| Fortune's Favor | `LootBoxRoller.Roll` | a percent chance the contents roll one quality tier higher; slots and gold stay the box's tier |
| Echo of the Loop | **hook only** `ClusterFImbueEffects.EchoOfTheLoopPercent` | no XmlLevelItems, no player levels (F-12) |
| Renowned | **hook only** `ClusterFImbueEffects.RenownedAmount` | nothing pays League commission or hunt Renown (`RenownSource.LeagueJob` and `.Commission` have no callers) |

The custom value shows as a tooltip line ("[Bountiful 15%]") through the patched `Item.GetProperties`.

## 5. The patch (argued, --fuzz=0)

`server\patches\Imbue-custom-property-hooks.patch`, applied last. Six files, one call each, all into
`ClusterFImbueEffects`; no override reaches any of them:
- `BaseWeapon.OnHit` (2 hunks): Bond after `AlterMeleeDamageFrom` (a creature's `AlterMeleeDamageTo` is per class;
  tamed creatures are pinned classes); Time Slip and Shatter right after `a?.OnHit` (the only point where the special
  move has run and its mana is known).
- `WeaponAbility`: a public `ClearCooldown` (the double-cost window is private).
- `SpellHelper.Damage`: Spell Leech after `AOS.Damage` (the one place both immediate and delayed spell damage pass;
  `SpellDamageTimerAOS.OnTick` calls it with no delay).
- `CraftItem.GetExceptionalChance`: Mastercraft (non-virtual).
- `Item.GetProperties` (Server project): one static delegate for an extra tooltip line (the custom store lives outside
  the item; every item's GetProperties reaches the base).
- `PlayerMobile.OnItemAdded`: when Fortune's Favor gear went on (the 60 second achievements need the equip moment).

Made against the tree with every earlier patch applied (BaseWeapon has three, CraftItem two, PlayerMobile four), dry
run clean at `--fuzz=0`, and the build applies it (section 7).

## 6. Hooks, TODOs and mismatches with the design

- **Rank 4 does not exist on the Artificers' ladder.** Its five rungs (0, 1,000, 5,000, 15,000, 40,000) map to rank
  index 0, 1, 2, 3 and 5 (`ClusterFGuildSystem.GuildRankIndex`: a five-rank ladder has no 4). So the rank 4 book (Faster
  Casting, Faster Cast Recovery, Swing Speed Increase, super slayers, Casting Focus) and the rank 5 Master Formulary
  both open at Arcane Artisan (40,000). For Chase: add a rung, or accept it.
- **Reinforce** does not exist (no ServUO port). Unravel (disenchant and extract) is free and ungated.
- **Grant-only properties with no effect yet:** Splintering, Reactive Paralyze, Soul Charge (no attribute storage in
  pinned or here; dropped earlier as D-74, D-21, D-49) and Casting Focus (no AosAttribute in pinned). The grant API
  records them; no catalogue row until an effect exists.
- **Echo of the Loop** and **Renowned**: hooks only (section 4). TODOs at the two methods.
- **Tool belts and guild gear** do not exist; crafter +skill goes on aprons until their type names are added to
  `crafterGearTypes`.
- **"Monster parts from League hunts"** do not exist; the ingredients are the existing imbuing ingredients (monster
  parts), proposed in section 3. Butcher's Eye's "monster parts from kills" are those same ingredient types on a
  corpse.
- **F-37 commissions, quest line, Renown commissions/hunts, player levels, XmlLevelItems:** none exist. The grant API is
  the hook for the 140+ path; loot boxes and bosses can call it when their tables name imbue unlocks (nothing does yet).
- **Mule socket II vs anywhere.** Today anyone with the Artificers' Toolkit (members) or at the guildmaster imbues
  anywhere up to Full, so socket II (Refined) adds nothing for them; III adds the forge bonus. The design does not say
  what "anywhere" allows. Kept the old behavior (Full) as `siteCaps.Anywhere`; set it lower in the config to make the
  mule matter. A decision for Chase.
- **"Standard soul forge bonus"**: ServUO gives an ordinary forge 0 (only the Queen's 6% and the Royal City's 2%). Used
  2 percentage points as the standard bonus (`forgeBonusPercent`) and 6 for the Queen's; tune in config.
- **The mule's own property sockets** are still never added in game (`MuleModule.AddSocket` has no caller); unchanged.
- **Creature of Habit's flavor** is not in the design (it says only that it roasts them); written here: "Twenty-five
  times. The System has stopped taking notes and opened a file. It is labeled 'Superstitions, Ongoing,' and it is
  getting thick." The two descriptions use the design's parenthetical text; Dressed for the Occasion's flavor is the
  design's exact text (shown without an item icon so it fits the popup).
- **Removed** with the standing model: the Master Artificer gate on Self Repair (cc-P42; the design makes it free; its
  price floor stays), the Journeyman gate on imbuing an enchanted item ("gated by property and intensity, not by item"),
  and the standing-based caps and slots. Standing still ranks the player and gates the books.
- **Crafter +skill rank:** the design names "Jewelry +skill bonuses" at rank 1 and crafter +skill as new without a
  rank; put at rank 1 beside it.

## 7. Tests, red then green, build

New `server\tests\Misc\ImbuingReworkVerification.cs`: 17 facts, numbered in its header.

Rewritten: `ImbueSelfRepairGateVerification.cs`. Its cc-P42 facts tested the standing gate this task removes. It now has 5 facts:
- Self Repair is free at Basic with no rank.
- Its Full tier works only once the account knows Full.
- The cc-P46 price floor is kept.
- The table charges that floor.
- Another property keeps its price scaling.

Also changed:
- `ImbueEssenceSourcesVerification.cs` grants Swing Speed Increase, now a rank 4 formula.
- `AchievementEarnedLineVerification.cs` expects 78 registered achievements.

| Run | What | Result |
|---|---|---|
| tests-only, first | compile | 2 errors (a namespace, a missing using); fixed |
| tests-only | first test run | 2 failures, both fixed. `[ImbueKnowledge` lacked `[ShardCommand]`. Dressed for the Occasion's design flavor did not fit the earn popup (6 lines in a 5-line block); fixed by dropping its icon, which widens the text, and by phrasing the Earned line as the design's parenthetical |
| tests-only | new test file | 2 failures, both in the tests, not the code. One test asked for Overcharged on the super slayer family, but on/off rows have only Basic; it now uses Swing Speed Increase. The test's `EquipItem` call refused the sword; `AddItem` now puts it on its layer |
| tests-only green | | **1133 / 1133** (1116 before: the old Self Repair file had 6 cases and the new one 5, plus 17 new) |
| **red** | 21 deliberate breaks across the six P82 files (listed below) | **18 failed**: 15 of the 17 new facts and 3 of the 5 Self Repair facts. The two new facts that stayed green pin behavior that already existed: fact 10 (pinned SkillCheck already reads Base; it cannot break without editing pinned) and fact 16 (row counts). Restored from backups; each file is `cmp`-identical |
| full build | `sl-modernuo:cc-p82` | First run 1132 / 1133. The failure was `WispOrbPossessionVerification(Silenii, Phantom)`, the known flaky test (D56; P50 and P52 notes), unrelated to imbuing; it passed in all three earlier runs. Re-run unchanged: **1133 / 1133, image built** (58d7fbd168c7) |

The red-phase breaks:
- free properties unknown
- Basic using Refined's fraction
- books teaching Overcharged
- books free
- the Master Formulary sold and read without the trial
- Overcharged Fortune's Favor granted, and accepted by the parser
- hints never drawn
- revoke doing nothing
- Bountiful and Fortune's Favor doing nothing
- the loot box hook off
- no soul forge and no mule III
- the +skill one-per-group check off
- extraction gated on membership

The `Item.Amount <= 0` lines in the test log are pre-existing corpse noise (see the P10, P17 and P73 notes).

The patch is in the build. The code calls `WeaponAbility.ClearCooldown` and `Item.ExtraProperties`, which exist only with the patch, and `apply-patches.sh` fails the build on any patch that does not apply at `--fuzz=0`.

Not done here: an in-game check, left for Chase.
- Imbue a few rows at the table.
- Read a formula book.
- Place an `ArtificersSoulForge` and try Overcharged.
- Look at the custom property's tooltip line.

Nothing was deployed, and `latest` is untouched.

## 8. Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

No file is over 5 MB. Every new file is source, config or notes.

P82 DONE
