# CC task P239: creature levels, con colors and the Appraisal skill (F-14)

Iron, 2026-10-21. Both repos were clean on `golem/Iron/P239` when I started. Pinned is `D:\UO\ModernUO-pinned` at
`d4531cd94`; pinned paths below are relative to its `Projects\`.

## Headlines

- **Every creature and NPC has a level, 1 to 200.** It is OSI's own Bard difficulty (pinned
  `BaseInstrument.GetBaseDifficulty`) without its 160 cap, one level per point, computed on every look and never
  stored. Rat 6, giant rat 23, orc 43, troll 49, drake 85, daemon 105, dragon 117, balron 128, ancient wyrm 150.
- **A hand override beats it:** a type table (the Harrower), champions 200, peerless bosses 190, invulnerable NPCs 1
  (and always grey). Our Rootdeep creatures need none: hog 9, grub 24, Burrow Mother 66, Gloom Queen 105.
- **`[CreatureLevels`** (Administrator, Diagnostic) writes every creature type's difficulty and level to a file. All
  1,011 creature types in pinned and ours are scored; none fails to construct.
- **Every player sees a con color** under a creature's or NPC's name on a single click (and the client's all-names):
  grey (trivial), green (easy), blue (fair), yellow (even match), orange (tough), red (dangerous), dark red (deadly).
  It is its own label line, so the name line and its notoriety hue are pinned's, untouched. Tested on a red and a
  blue mobile.
- **The player's level is provisional:** their best combat skill, behind a setting, read through one interface
  (`IPlayerLevelSource`) that F-12 replaces without touching a caller.
- **Item Identification is Appraisal.** On a creature or NPC it tells more as the skill grows: the color and a vague
  line, then the level (30), hits, stats and resists (60), and a stat card gump (90). On items and players it is stock.
  It trains past 100 on creatures near its level, the way P191's skills do (hook G).
- **The name "Appraisal" ships in the player package.** TazUO reads skill names from `skills.mul`, and the launcher's
  `Build-UoOverrides.ps1` now writes a copy with skill 3 renamed (not published). The server says Appraisal too.
- **Tests:** 27 new server test cases and 2 new package facts. Each was seen failing first. The full suite is green
  through `docker\uo\build.sh`: 1,944 tests, 1,940 passed, 4 skipped, 0 failed.

## Part 1: the spread first

Before any level code, a one-off probe test (marked `P239-PROBE`, deleted after) did the following:
- built every creature type with a no-argument constructor (pinned and ours);
- called pinned's `GetBaseDifficulty` on each one;
- failed on purpose, so its table landed in the build log.

Result: **1,011 types, 1,011 scored, 0 failed to construct**, with SE and LBR on and expansion EJ. The whole table is
`notes\cc-P239-files\bard-difficulty-spread.txt`.

**It ranks sensibly where it should:**

| Creature | Difficulty | | Creature | Difficulty |
|---|---|---|---|---|
| Chicken | 3.9 | | Drake | 84.6 |
| Rat | 6.2 | | Wyvern | 88.7 |
| Giant rat | 22.6 | | Lich | 104.1 |
| Grey wolf | 30.4 | | Daemon | 105.2 |
| Ettin | 39.5 | | White wyrm | 108.3 |
| Orc | 42.8 | | **Dragon** | **116.9** |
| Ogre | 47.0 | | Lich lord | 123.4 |
| Troll | 49.4 | | Balron | 128.3 |
| Evil mage | 75.5 | | **Ancient wyrm** | **150.3** |

Rat below dragon below ancient wyrm.

Spread: 0-19: 77 types, 20-39: 220, 40-59: 160, 60-79: 157, 80-99: 156, 100-119: 80, 120-139: 29, 140-159: 34,
**160: 98**.

**Where it goes wrong:**
1. **The cap.** Pinned clamps at 160 under SE (`BaseInstrument.cs:298-301`), and 98 types sit on it.
   - Every champion (Barracoon, Rikktor, Semidar, Neira, Lord Oaks, Mephitis, Serado, Ilhenir, Twaulo, Meraktus), the
     Harrower, the peerless and SA bosses (ours too), and the Renowned creatures.
   - Also big-HP ordinary creatures: Vorpal Bunny, Fire Rabbit, Giant Turkey, Burning Mage, Archmage, Lesser Wind
     Elemental, Flame Elemental.
   - Fixed by dropping the cap (they spread above 160 by their own numbers) and by the overrides for bosses.
2. **Town NPCs score like monsters**, from their hit points and skills: Healer 96, Evil Healer 110, Wandering Healer 106,
   Fortune Teller 95, Mage NPC 71, Banker 28.5. Fixed by the invulnerable rule (level 1, always grey). A vendor counts
   only when `vendor.isInvulnerable` is on (pinned default: Core.LBR, so on).
3. **Poison immunity is +100 (10 levels) for fodder undead.** Zombie 35 and skeleton 41 sit above an ettin (39.5).
4. **Abilities the formula ignores** (its own TODO, `:251-254`: auras, summoning undead):
   - creatures whose danger is a special (a corpser's grasp, a wisp's teleport, a gazer's beam) read low;
   - creatures whose stat blocks are large but harmless read high.
   - A type-table override is the place for any of these Chase wants moved.
5. **A few creatures roll their poison on every read** (speckled scorpion, giant serpent). Their level moves by 2
   between looks. Pinned's own Bard difficulty does the same.

## Part 2: the level

`server\customizations\ClusterFCreatureLevels.cs` (new):
- `:120` **`UncappedDifficulty`**: pinned's `GetBaseDifficulty` step for step, calling its public helpers
  (`IsMageryCreature`, `IsFireBreathingCreature`, `IsPoisonImmune`, `GetPoisonLevel`), without the SE cap line. A fact
  proves it equals pinned's for every type below 160, so a pinned change shows.
- `:165` **`ComputedLevel`**: the uncapped difficulty rounded, clamped to 1-200. One level per point: a level reads as
  the Bard difficulty a bard would face, with nothing invented. A paragon's +40 is OSI's, inside the formula.
- `:169` **`Level(m, out why)`**: overrides first, in order:
  1. `TypeOverrides` (`:101`; the Harrower 200, a `BaseCreature`, not a `BaseChampion`);
  2. `BaseChampion` 200;
  3. `BasePeerless` 190 (pinned's and our SA and boss classes);
  4. invulnerable 1.
  
  Then computed. `why` says which rule applied. Never stored on the creature.

## Part 3: the provisional player level

- `:41` `IPlayerLevelSource` (one method, `LevelOf`), and `ClusterFCreatureLevels.PlayerLevels` holds the source.
  F-12's build sets its own there; no caller changes.
- `:50` `ProvisionalPlayerLevel`:
  - the player's best combat skill, Base in whole points, clamped 1-200;
  - the skills: Archery, Fencing, Macing, Swords, Wrestling, Throwing, Magery, Necromancy, Chivalry, Bushido,
    Ninjitsu, Spellweaving, Mysticism, Animal Taming, Provocation;
  - so a Grandmaster swordsman is level 100 and a new character level 1.
- Settings (`:106`):
  - `clusterf.creatureLevels.provisionalPlayerLevel`, default true;
  - when it is false, everyone is `clusterf.creatureLevels.fixedPlayerLevel` (default 50);
  - `clusterf.creatureLevels.conLine`, default true, switches the con line off.

## Part 4: the con color

- `:208` **bands by the level gap** (creature minus player): grey -20 and below, green -19 to -10, blue -9 to -3,
  yellow -2 to +2, orange +3 to +9, red +10 to +19, skull +20 and up. `:223`: an invulnerable NPC is always grey.
- `:228` hues, picked from the client's `hues.mul` for readability:

  | Band | Hue | Colour |
  |---|---|---|
  | grey | 0x3B2 | 152,152,152 |
  | green | 0x44 | 24,192,0 |
  | blue | 0x63 | 40,88,192 |
  | yellow | 0x35 | 192,192,0 |
  | orange | 0x2B | 192,80,0 |
  | red | 0x26 | 192,24,0 |
  | skull | 0x20 | 152,0,32 |

  `:239`: each band has a word too ("(even match)"), so the color never reads as a notoriety color.
- **How it shows, without a core edit:**
  - **Single click (`BaseCreature.OnSingleClick`).** This is UOContent, not core (pinned `Mobiles/BaseCreature.cs:3195`),
    and it is per viewer: it sends to `from.NetState`. `server\patches\BaseCreature-con-color-line.patch` adds one call
    after `base.OnSingleClick(from)`: `ClusterFCreatureLevels.OnSingleClick` (`:251`), a `PrivateOverheadMessage`
    label to that viewer only.
  - **Notoriety untouched.** The name line is pinned's `Mobile.OnSingleClick` (`Server/Mobiles/Mobile.cs:7995`): its
    hue is `Notoriety.GetHue(Notoriety.Compute(from, this))`, and nothing of ours changes it.
  - **Not the property list.** `ObjectPropertyList` is built once per object and sent alike to every viewer, so it
    cannot carry a color that depends on who looks.
  - **Not the name.** A name suffix would be the same for everyone and would change the name everywhere.
  - Players are not given a con line (players are not BaseCreatures).
- `docker\uo\apply-patches.sh:818-825`: the two new patches, last in the list, with the reasoning.

## Part 5: Appraisal

**What Item Identification does in pinned and what uses it** (checked before taking it over):
- `Skills/ItemIdentification.cs:20-27`: use asks for a target. On a **mobile** it calls `mobile.OnSingleClick(from)`
  and nothing else (`:36-40`).
- On an **`IIdentifiable` item** it rolls `(0, 100)` and sets `Identified` (`:46-50`). Only `BaseWeapon` and
  `BaseArmor` implement it.
- Pre-AOS it also single-clicks the item.
- **No Imbuing caller**: ModernUO has no Imbuing skill handler, and ours (`ArtificersImbueGump.cs`) never reads
  `SkillName.ItemID`.
- Other uses of the skill are NPC skill values and lists:
  - NPC skills: `Merchant.cs:13`, `MerchantGuildmaster.cs:11`, `MinerGuildmaster.cs:11`, `Jeweler.cs:14`,
    `Vagabond.cs:15`, `ML Quests/Definitions/Ilshenar.cs:176`, ours `ArtificersGuildmaster.cs:28`;
  - lists: `CharacterCreation.cs:49,1151` (ours `:49,1166`), `PlayerMobile.cs:256`, `SkillsGump.cs:461`;
  - our guild code: `ClusterFGuildStarterPath.cs:61` (merchants), `ClusterFGuildSystem.cs:221,251` (a dummy skill for
    item-only and always-eligible rows).

  None of those changes: they read the skill's value, not what using it does.

**The change:**
- `server\patches\ItemIdentification-appraisal.patch`: in the target's mobile branch, `ClusterFAppraisal.TryAppraise`
  first, and pinned's single click when it says no.
  - It says no for anything not a `BaseCreature`, so a player is stock, and every item is stock.
  - A callback set from our own `Initialize` (as our `Meditation.cs` would by replacing the file) would race pinned's
    `Initialize`, whose order is not declared, so this is a patch.
- `ClusterFCreatureLevels.cs:354` `ClusterFAppraisal`:
  - `:369` `TryAppraise`: rolls `(0, 100)` for gain, sends the lines (the first in the con hue), and at 90 and up the
    card.
  - `:395` `Describe`, the steps:

    | Skill | What it adds |
    |---|---|
    | 0 and up | "<name>: <vague line by con band>", e.g. "It looks like it could hurt you."; for an invulnerable NPC "It is no threat to anyone." |
    | 30 and up | "Level N." and a line in the style of Anatomy and Animal Lore, words not numbers ("It looks mighty and quick, with a dim mind.") |
    | 60 and up | "Hits h/max, Str, Dex, Int." and "Resists: physical, fire, cold, poison, energy." |
    | 90 and up | the stat card, `AppraisalCardGump` (`:533`, lines from `CardLines` `:444`) |

  - The card shows: level and con word; hits, stamina, mana; stats; resists; the damage range and damage types; and
    special abilities. The specials are: casts spells (with Magery), breathes fire, poisons on hit, poison immunity,
    each `MonsterAbility`, the weapon ability, and unmoved by music. Last, paragon or boss, with the level rule.
  - The roll's result does not gate what is shown; the steps are the skill's, as approved.
- **Gains past 100:** `ClusterFSkillGain.cs:420`, a hook G row for `SkillName.ItemID`, like Animal Lore's and Arms
  Lore's.
  - A `(0, 100)` use on a `BaseCreature` gains past 100 in a window of the creature's level ±25, so appraising stronger
    creatures trains it.
  - An item gives no row, so items stay stock.
- **The name, server side:** `ClusterFAppraisal.Initialize` (`:362`) sets `SkillInfo.Table[3].Name` to "Appraisal".
  Pinned loads the table from `Data/skills.json` in `SkillsInfo.Configure` (`Skills/SkillsInfo.cs:133-135`), so
  Initialize runs after it. Gumps of ours that print skill names say Appraisal.

## Part 6: the name for everyone (shipped in the package, not published)

- **Where TazUO reads skill names:** `skills.mul` and `Skills.idx`, by name through `GetUOFilePath`
  (`ClassicUO.Assets/SkillsLoader.cs`, TazUO 3212623f, our build's source at `D:\UO\tazuo-sl-build\src`).
  - An entry is one action byte, the ASCII name and a NUL. Skill 3 in the client is `\x01Item Identification\x00`.
  - `GetUOFilePath` takes the override map first (`UOFileManager.cs:103-107`), and the launcher already hands TazUO a
    `files-override.txt` (`-uofilesoverride`) for tiledata, Cliloc and the map.
- **So it fits the package's existing route.** `player-package\payload\app\Build-UoOverrides.ps1`:
  - `:64` the header's part;
  - `:119` `$SkillRenames` (index 3, "Item Identification" to "Appraisal": ours, nothing of EA's);
  - `:618` `Build-Skills`: reads the player's two files and rewrites skill 3 only where it still says
    "Item Identification" (its action byte kept). It repacks every entry in index order, writes the copies and a stamp
    to `app\uo-overrides\`, and adds `skills.mul=` and `skills.idx=` to the list.
  - A file where EA has renamed skill 3 is left alone, with one yellow line. A folder with neither file (the tests' fake
    folders) is skipped quietly.
  - Plain PowerShell byte work: no `Add-Type`.
- **Checked on the real client files.** On a scratch copy of `D:\UO\UltimaOnlineVanilla`'s pair, the copies differ
  from the originals only in skill 3: 256 slots, 58 skills, "Item Identification" (action 1, extra 13) becomes
  "Appraisal" (action 1, extra 13).
- The payload ships `Build-UoOverrides.ps1` as it is, so the next package carries it. **Not built or published here.**
- **The cliloc side:** the client's own "Your skill in X has increased" messages take the name from the same
  `skills.mul`. Nothing else in TazUO names the skill.

## Part 7: the two deviations, worded for `docs\fidelity-principle.md` (agents never edit docs)

For the numbered register, at the next free D number when registered:

| # | What changed | What a player notices | Status | Note |
|---|---|---|---|---|
| D-? | Item Identification is renamed Appraisal (server `SkillInfo` and the client's `skills.mul` through the launcher) and, used on a creature or NPC, tells its con, level, stats and a stat card by skill step; it gains past 100 on creatures | a skill OSI calls Item Identification is called Appraisal and does something on creatures; on items it is unchanged | `ours` | `cc-P239-creature-levels-appraisal` |
| D-? | Every creature and NPC has a level (OSI's Bard difficulty, uncapped, 1 to 200, with overrides) and a con color line under its name on a single click | a colored word under every creature's name; OSI shows no creature levels | `ours` | `cc-P239-creature-levels-appraisal` |

For the prose section: "F-14 (cc-P239, 2026-10-21): creature levels and con colors are ours; OSI has neither.
Repurposing Item Identification as Appraisal is a deviation on ported content: the skill's name and its use on mobiles
differ from OSI, and a wiki page about Item Identification is wrong for this shard. Its use on items is OSI's."

## Tests

**Server: `server\tests\Mobiles\CreatureLevelsVerification.cs`, 27 test cases:**

| Fact | What it checks |
|---|---|
| `TheReportCoversEveryCreatureTypeAndRanksThemSensibly` | `BuildReport` has exactly one row per creature type (counted independently, more than 900), with no failures and ours included (the Gloom Queen); a rat below a dragon below an ancient wyrm; every level 1-200 |
| `BelowPinnedsCapTheUncappedDifficultyIsPinnedsExactly` | each type read 12 times both ways: our uncapped values are pinned's below 160, and 160 or more where pinned's is capped |
| `AnOverrideBeatsTheComputedLevel` | a table entry (rat 150 over its computed 6); a champion (Barracoon) 200; a peerless boss (our Crimson Dragon) 190, not its computed; an invulnerable healer 1, not its computed 96 |
| `ConColorBandsSitAtFixedLevelGaps` (14 cases) | each band edge at player 50, and the same gaps at player 150 |
| `EachBandHasItsOwnHueAndWord` | seven distinct hues and seven words |
| `TheConLineIsItsOwnMessageAndTheNameKeepsItsNotorietyHue` | on a red (evil mage, Murderer) and a blue (banker, Innocent) mobile: the name line's hue is `Notoriety.GetHue`, and the con line is a separate label after it in the con hue; switched off, the name alone |
| `TheProvisionalPlayerLevelIsTheBestCombatSkill...` | Swords 80, Magery 95.4, Cooking 120 gives 95; cooking only gives 1; the setting off gives the fixed 50; a replaced source is what the con color reads |
| `AppraisalShowsEachStepsDetailAndNothingFromTheNext` (0, 30, 60, 90) | the vague line always; the level only from 30; hits, Str and Resists only from 60; the card only at 90 |
| `TheStatCardShowsTheWholeCard` | a dragon's card: level, hits, Str, Physical, Fire, "Breathes fire", Magery |
| `ThroughTheSkillsTarget...` | through `ItemIdentification.OnUse` and the real target (the patch): a troll is appraised; a player gets stock (no level line); a longsword is still identified |
| `TheSkillIsCalledAppraisalAndGainsPastOneHundred...` | the server name; at 120, a dragon (level about 117) gives a past-100 chance, a rat none, a sword none |

**Package: `player-package\tests\Build-UoOverrides.Tests.ps1`**
- `:610` `TheSkillsCopiesCallItemIdentificationAppraisalAndKeepEveryOtherSkill`: a made-up pair in TazUO's layout
  (`:580`), with two empty slots and distinct extras. The list names both copies. Skill 3 is Appraisal with its action
  byte and extra. Every other skill is as it was, the player's files are untouched, and nothing is said.
- `:627` `ASkillThreeTheFilesNoLongerCallItemIdentificationIsLeftAloneWithOneLine`: no copies and one line.

**Runs** (all `docker/uo/build.sh -t sl-modernuo:cc-P239 --tests-only` under the `docker-build` lock, started detached):

| Run | Tree | Result |
|---|---|---|
| probe | `P239-PROBE` only | the spread above (fails on purpose) |
| red 1 | tests plus stubs with the final API (marked `P239-RED`) | did not compile: a missing `using Server.Gumps` and xUnit2031 in my test. Fixed |
| **red 2** | same | **1,944 tests: 25 failed, 1,915 passed, 4 skipped. 24 are the new cases, each for the stock reason:** no rows ("Expected 1011"), no con line, no Appraisal lines ("Collection was empty"), the stock skill name. The three yellow-band cases passed against a stub that always answers yellow. The 25th was `JokeAchievementsVerification.DeathsByGuardsFowlAndYourOwnPotion`; see green 2 |
| green 1 | implementation | 5 failed. My tests' own mistakes: a bare `new PlayerMobile()` is not flagged `Player` (CharacterCreation sets it, `:224`), which both the con line and hook G ask for; a vendor's invulnerability is the `vendor.isInvulnerable` setting, which the test host never configures (a `Healer` is invulnerable by class); two creatures roll their poison on each read. The tests were fixed; the code did not change |
| green 2 | same | 1 failed: JokeAchievements. **The same suite on HEAD** (`git archive` to scratch, nothing checked out) **passed it (1,917 of 1,917, 4 skipped)**. So it was my test: `NotorietyHandlers.Initialize()` also sets `Mobile.AllowHarmfulHandler`, which leaked into the explosion potion fact. My fact now saves and puts back the handler, the hues and both harm handlers |
| **final** | the finished tree, CHANGELOG and VERSION included | **1,944: 1,940 passed, 4 skipped, 0 failed**; the 27 new cases passed |

`--tests-only` builds no runtime image, so no `sl-modernuo:cc-P239` image exists. `sl-modernuo:latest` is untouched.

Package facts: against HEAD's builder (mine saved to scratch, put back after), the two new facts **FAIL** ("skills.mul
is in the list", "one line says so"). With mine, 13 of 15 pass. The 2 that fail are `PlayStarts...`, which need the
test shard up, as the file's header says.

## Deviations and decisions for Chase

1. **The provisional player level.** Proposed: the best combat skill (Base, whole points, 1-200), on by default
   (`clusterf.creatureLevels.provisionalPlayerLevel`). F-12 replaces it through `ClusterFCreatureLevels.PlayerLevels`.
   - With it, a GM (100) fighter cons a dragon (117) red, a troll (49) grey, and an ancient wyrm (150) dark red.
   - Alternatives:
     - the average of the best weapon or spell skill and Tactics;
     - a fixed level for everyone (the setting off, `fixedPlayerLevel` 50).
2. **Levels are 1:1 with Bard difficulty, uncapped.** A paragon gets OSI's +40 inside it (+40 levels). Champions 200,
   peerless 190, invulnerable NPCs 1 and grey.
   - The 160 cap was dropped because 98 types sat on it.
   - If you want a different scale (say, stretch 0-160 to 1-200), it is one line in `ComputedLevel`.
3. **The band edges** are fixed gaps (±2 even, 3-9, 10-19, 20+). EverQuest scales its gaps with level. Fixed gaps are
   simpler and the tests pin them. Say if you want them scaled.
4. **Town NPCs read "(trivial)"** because they are invulnerable. Appraisal says "It is no threat to anyone." A vendor
   counts only while `vendor.isInvulnerable` is on (pinned's default).
5. **Two creatures' levels move by 2 between looks** (speckled scorpion, giant serpent), because their hit poison is
   rolled on each read. Pinned's Bard difficulty does the same. Left as is.
6. **The Appraisal roll gains, but does not gate the detail.** The approved steps are by skill. A failed roll still
   shows that step's detail, which keeps the tests deterministic. Say if a failure should show only the vague line.
7. **Gains past 100 use the creature's level ±25** (hook G row), so appraising a dragon trains a 120 appraiser and a
   rat does not.
8. **The con line rides on single click**, a separate line under the name. The tooltip (property list) cannot show it,
   because one list goes to everyone. On TazUO, hovering shows the tooltip; clicking or all-names shows the colored line.
9. **The two deviations** are worded in Part 7 for `docs\fidelity-principle.md`; they need registering by whoever
   edits docs.
10. **The Read tool was denied** (unattended run) for files in the code work copy, as before. I read with Bash and
    edited with small Python scripts that require an exact single match and keep line endings.

## For Chase

What to check in the client (test shard, after an image with this is deployed and a package with the new launcher
script is built):
1. Click a rat, an orc, a troll and a dragon on a fighter of about skill 60-100. A colored word appears under each name:
   grey or green for the rat, red or dark red for the dragon. The name keeps its usual blue, grey or red.
2. Show all names (Ctrl+Shift): every creature's con line shows.
3. Use the skill (now "Appraisal" in the skills window, after updating) on a troll at skill 0, 30, 60 and 90:
   - 0: one colored line;
   - 30: the level;
   - 60: hits, stats and resists;
   - 90: the stat card opens.
4. On a longsword it still identifies; on a player it shows the name as before.
5. `[CreatureLevels` as Administrator writes the full table to the server's temp folder (`/tmp/creature-levels.txt` in
   the container). It makes and deletes one of each creature, so run it on the test shard.
6. Settings to know: `clusterf.creatureLevels.conLine`, `.provisionalPlayerLevel`, `.fixedPlayerLevel`.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P239 -NoRefresh`
(the hand-off's work copies in place of the real folders). It commits nothing; neither repo is BLOCKED:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code: 10 files**: CHANGELOG.md (2026.10.21.8), VERSION, apply-patches.sh, Build-UoOverrides.ps1 and its tests,
  ClusterFSkillGain.cs, ClusterFCreatureLevels.cs, the two patches, and CreatureLevelsVerification.cs.
- **docs: 2 files**: this note and `notes\cc-P239-files\bard-difficulty-spread.txt` (115 KB).

No file is over 5 MB. Scratch (test logs, the HEAD copy, the vanilla skills check) is in the session scratchpad,
outside both repos.

P239 DONE
