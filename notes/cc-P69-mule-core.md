# cc-P69: The Compact Mule, core build (tiers, bloodlines, breeding, League quest)

Run 2026-10-12 by Claude Code (autopilot hand-off after P65). Builder, test build only. At start
`git -C D:\ShatteredLegacy status --short` was empty; pinned is `d4531cd94b739613155225c234900de9f47d2c88` (every pinned
citation below is at that commit). **C** = `D:\ShatteredLegacy\server\customizations`, **P** =
`D:\UO\ModernUO-pinned\Projects`. One research subagent read the League code for the errand's host; its citations are
marked "(agent)". I read and re-checked everything else, including all of the mule code this task rewrote.

## Headlines

1. **Built: five tiers, bloodlines, saved breeding, the League errand and the module hooks.** No patch to pinned.
   **1073/1073 shard tests pass**; the 11 new facts were watched red, then green. Image `sl-modernuo:cc-p69`.
2. **The mule costs 1 follower slot** everywhere: the code, both deeds and the Exchange gump (it said 1 while the code
   and deeds said 2). The cost is computed in one place, `PackMule.Compute`, so Trailwise Tack III can set it to 0.
   Loaded mules have their owners' follower counts set right, online or not.
3. **The Civic Mule Exchange no longer sells a mule.** It is now the tier-up window. Its first step (tier 1 to 2)
   costs the old Exchange price.
4. **The base mule comes from a League errand at the Registrar**, "The Compact's Mule". It is gated at League rank
   Dull Copper (2): register, bring 50 iron ore and 25 iron ingots, and collect a bonded tier 1 mule. One per character,
   and a lost one can be replaced for a fee.
5. **Breeding is saved.** The foal deed is made the moment two mules breed, with its genes rolled, and waits on the
   internal map with its due time and owner saved. A restart no longer loses the foal (fact 8).
6. **Existing mules load as tier 3 (Shadowhide).** Their old stats are tier 3's range exactly. HP quality is read from
   their hits, the other qualities are rolled; no traits, generation 0, no parents. Facts 6 and 11 load real version-0 bytes.
7. **A real bug caught by an existing test:** `PlayerMobile.AllFollowers` is null until a character has had a
   follower, so the new Exchange window crashed for such a character (`SmithBackButtonsVerification`). Fixed.

## 1. Part A: one follower slot

- `MuleNumbers.SlotCost` (default 1) in `PackMule.Compute` is the one place the cost is set. `PackMule.SetSlotCost`
  changes it as P47 6 prescribes: `RemoveFollowers()`, set `ControlSlots`, `AddFollowers()` (`P\UOContent\Mobiles\BaseCreature.cs:2625, 2639`).
  Pinned has no change hook on `ControlSlots`, so setting it bare would leave the owner's count wrong.
- Both deeds and the errand summon through one method, `PackMule.SummonFor`. It checks `Followers + ControlSlots`
  against `FollowersMax`, so the three agree by construction. The Exchange text no longer mentions a slot count.
- **On load**, a mule whose `ControlSlots` differs from the computed cost (every v0 mule: 2) gets `ApplyNumbers` on the
  next tick:
  - **Owner offline:** `Followers` is saved on the owner and `RemoveFollowers`/`AddFollowers` work on the mobile
    whether or not it has a connection, so the count is right when they log in.
  - **Stabled mule:** it has no `ControlMaster` (stabling calls `SetControlMaster(null)`, `P\UOContent\Mobiles\Vendors\NPC\AnimalTrainer.cs:252-266`
    (agent)), so its cost is simply set, and it counts at the new cost when it is claimed.
- Fact 2: 1 slot; a 2-slot mule's cost set back to 1 moves the owner from 2 to 1; a hook setting 0 takes the owner to 0;
  no free slot means nothing is summoned.

## 2. Part B: the tiers as built (`C\Mobiles\Mule\MuleData.cs`, `MuleData.Tiers`)

HP, pack, resists, slots and metal are Chase's (2026-10-05). Str, Dex, Stam, skills, damage and armor are mine,
scaled so tier 3 is today's mule (Str 400-450, Dex 86-105, Stam 120-150, skills 80-95, damage 10-14, armor 55).

| Tier | Name (shown "a Bronzeback mule") | HP | Pack (stones / items) | Resists | Slots | Hue (the metal's own) | Str | Dex | Stam | Skills (MR, Tactics, Wrestling) | Damage | Armor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Compact | 150-190 | 1,600 / 150 | 25-45 | 1 | Dull Copper 0x973 | 250-300 | 70-85 | 80-100 | 70 | 6-9 | 35 |
| 2 | Bronzeback | 200-250 | 2,400 / 225 | 35-55 | 2 | Bronze 0x972 | 325-375 | 78-95 | 100-125 | 80 | 8-12 | 45 |
| 3 | Shadowhide | 250-310 | 3,200 / 300 | 45-65 | 3 | Shadow Iron 0x966 | 400-450 | 86-105 | 120-150 | 87.5 | 10-14 | 55 |
| 4 | Valorite-Barded | 320-400 | 4,000 / 400 | 55-70 | 4 | Valorite 0x8AB | 475-525 | 95-115 | 145-175 | 95 | 12-16 | 62 |
| 5 | Celestial | 420-500 | 5,000 / 500 | 60-75 | 5 | Celestial 0x08AF | 550-600 | 105-125 | 170-200 | 100 | 14-18 | 70 |

- **Hue from the ladder, not numbers:** `MuleTier.Hue => CraftResources.GetHue(Metal)`, the same table the ingots and
  ore use (`C\ResourceInfo.cs:1222`; Dull Copper 0x973 at :623, Valorite 0x8AB at :693, Celestial 0x08AF "radiant gold"
  at :776; all five values above read from that file). Fact 1 checks each tier's hue against `GetHue`. **How each looks on the mule body is
  unverified: no client ran.** If one looks wrong, the fallback is Chase's "or at least the barding gear is hued
  such": hue the Expedition Barding module (the modules prompt), not the animal.
- **Quality places a stat in the tier's range:** `min + (max - min) x quality / 100` for HP, Str, Dex and Stam.
  - **Pack:** quality places it between 90% and 100% of the tier's figure, so Chase's figure is the top. Flagged for Chase.
  - **Resists, today's shape:** each resist is `min + span x (shape/2 + quality/200)`, with shape 1 for physical, 0.5
    for cold and poison, and 0 for fire and energy. At quality 100 physical is the tier's top and fire and energy its
    middle; at quality 0 physical is the middle and fire and energy the bottom. Every value stays inside the tier's range.
- **Display:** the name shows the tier. The properties show tier and sex, the five qualities, the traits, the family,
  generation and Legendary, and module slots used out of the total.
- **Upgrade** (`C\Mobiles\Mule\MuleUpgrades.cs`, one record per step: from-tier, Miners' Compact rank, currencies, gold):

| Step | Miners' Compact rank | Currencies | Gold |
|---|---|---|---|
| 1 -> 2 | none | 25 Mining Vouchers, 25 Smithing Seals, 25 Trail Marks, 25 Timber Tokens (the old Exchange price) | 25,000 |
| 2 -> 3 (placeholder) | Journeyman (2) | 60 Mining Vouchers, 40 Smithing Seals, 40 Timber Tokens, 40 Tinkers' scrip | 50,000 |
| 3 -> 4 (placeholder) | Master (3) | 120 Mining Vouchers, 80 Smithing Seals, 80 Trail Marks, 60 Arcane scrip | 100,000 |
| 4 -> 5 (placeholder) | Grandmaster (4) | 250 Mining Vouchers, 150 Smithing Seals, 100 Essence Shards, 100 Warriors' scrip, 100 Arcane scrip | 250,000 |

  - **No multi-currency payment existed.** `GuildResources.TryPay` takes one scrip (`C\GuildResources.cs:294`), and the
    Exchange hand-rolled four. `MuleUpgrades.TryUpgrade` is the smallest one that serves: it lists every shortfall,
    takes nothing unless all of it is there, then takes it all. The Testing Token waives it, as it did the purchase.
  - Guilds with no named currency show as "<guild name> scrip" (`ClusterFGuildSystem.GetDef`).
  - **Where:** the Civic Mule Exchange gump (the same class, opened from the five guild dashboards, whose button now
    reads "Civic Mule Exchange (mule upgrades)"). It lists the mule you ride and those following within 12 tiles (up to
    three), with each one's next step, cost and shortfall, and an Upgrade button that re-checks on the press.
  - **An upgrade keeps** quality, traits, lineage, name, bond and pack, and heals the mule (fact 4).

## 3. Part C: bloodlines

**Saved on the mule** (`PackMule` v1 fields): sex, cooldown, tier, five qualities (0-100), up to three traits (`id x 10 +
grade`), family name, generation, both parents (`uint` serials; the generator has no `Serial` field type in pinned),
the inherited Legendary count, and the module list.

**Traits, per grade I / II / III** (`MuleData.Traits`; each has a `MuleTrait` id the module code can read):

| Trait | Effect | I | II | III |
|---|---|---|---|---|
| Burdened Bloodline | pack weight and items | +5% | +10% | +15% |
| Stoneback | physical resist | +3 | +6 | +9 |
| Emberblood | fire resist (and, later, a Field Smelter Rig boost) | +3 | +6 | +9 |
| Surefooted | stamina | +10% | +20% | +30% |
| Deepdelver | damage taken inside a dungeon region (melee and spell) | -5% | -10% | -15% |
| Nightmare-Kin | Magic Resist skill | +5 | +10 | +15 |
| Celestial Tempered (rare) | every resist, and hit points | +2, +2% | +4, +4% | +6, +6% |

Resists never go above 80 (`MuleData.ResistCap`), traits and modules included.

**Lineage:**
- The family name runs down the line: the higher-tier parent's name, or the dam's (female) on a tie, or the other
  parent's if that one has none.
- The first foal of two unnamed parents draws a name from 20 in `MuleData.FamilyNames` ("Ironhoof", "Stonecart", ...).
  Staff can rename it with `[props FamilyName`.
- **Legendary:** each mule carries the count of tier 5 generations before it. A foal of two tier 5 parents inherits the
  larger of their counts; reaching tier 5 adds one. Three in a row make the line Legendary, shown in the properties.

## 4. Part D: breeding

Today's rules are kept: the owner owns both, one male and one female, a 7-day cooldown each, 24-hour gestation.

**Inheritance** (`MuleBreeding` in `MuleData.cs`; the rules are in `MuleGenes.Breed`). "Lore" is the breeder's Animal Lore
factor: 0 at 120 or below, 1 at 200, linear (0.5 at 160).

| Roll | Chance | Lore at 200 adds |
|---|---|---|
| Each stat quality: the better parent's value | 50% | +30% (80%) |
| Otherwise: parents' average + a roll of -5..+5 | (the rest) | |
| A trait one parent has passes | 35% | +15% (50%) |
| A trait both parents have passes | 70% | +15% (85%) |
| ...and goes up one grade | 20% | +10% (30%) |
| A new grade I trait (never Celestial Tempered) | 5% | +5% (10%) |
| Celestial Tempered, new, from two tier 5 parents | 2% | none |

- **Strong parents:** grade III only when both parents are tier 4 or higher (otherwise a grade is capped at II).
  Celestial Tempered passes or appears only between two tier 5 parents.
- **More than three traits:** the highest grades are kept first, then those both parents carried, then at random.
- **The foal starts at tier 1**, generation = the higher parent's + 1.

**The foal deed** (`BredPackMuleDeed` v1) carries the genes from the moment of breeding.
- It shows sex, tier 1, generation, family, the five qualities and the traits before it is used.
- It is blessed and tradeable.
- Using it summons a bonded tier 1 mule with those genes (fact 9).
- A version 0 deed (from before) rolls fresh genes when used, as generation 1.

**Saved gestation.** `PackMuleBreedingSystem.StartBreeding` makes the deed and calls `BeginGestation(owner, now + 24h)`:
the deed goes to the internal map with `DeliverAt` and `Recipient` saved, and a timer delivers it to the bank. After a
load, `[AfterDeserialization]` arms the timer again from the saved due time (at once, if it is already due). Fact 8
round-trips a pending deed and delivers it at its due time. An owner deleted before delivery takes the foal with them.

**Bonded on acquisition:** every deed, the errand and the replacement summon a bonded mule (`SummonFor`).

## 5. Part E: the League errand (`C\Mobiles\Mule\MuleErrand.cs`; Registrar page in `C\LeagueRegistrarGump.cs`)

**Host: the Registrar's own gump**, a new "The Compact's Mule (errand)" row and page.
- It is the League's NPC in New Haven and already reads the character's rank.
- Its Promote button set the pattern this follows: every check again on the press (agent: `LeagueRegistrarGump.cs:271-343`).
- An MLQuest was weighed and not used (agent: objectives `CollectObjective` and the rest, `P\UOContent\Engines\ML Quests\Objectives\`).
  It would need a quest-item toggle, carry the 10-quest cap, and need the reward to fit the pack, and the rank gate,
  one-per-character and the replacement would still be custom code.

**State:** the character's League record, `CharacterLeagueData` v0 -> **v1**: `MuleErrandStage` (0 not taken,
1 taken, 2 delivered, 3 done) and `MuleGranted`. Only that record's version moved, not the account record's. Its
reader now takes 0 to `CurrentVersion` and still fails loudly on a newer one. The existing unknown-version fact adapts by
itself (`CurrentVersion + 1`); fact 11 reads hand-made v0 bytes.

**Steps:**
1. **Take it** at the Registrar: registered, and League rank **Dull Copper (2)** or higher.
   - Iron comes with registration. Dull Copper needs 100 lifetime Renown (the account achievements give about 115),
     Apprentice in one guild, and the chapter 1 trial, waived by default (agent: `ClusterFLeagueRanks.cs:443-462`,
     `ClusterFAchievements.cs:411-440`). So it is reachable in well under an hour. Chase may prefer Iron (section 9).
2. **Deliver 50 iron ore and 25 iron ingots** at the Registrar. They are counted in pack and bank, satchels included,
   through `GuildResources.TryPay` (`C\GuildResources.cs:294-348`), which says what is short and takes nothing until
   all of it is there.
   - **Why a turn-in:** no per-character "ore mined" or "ingots smelted" counter exists. Iron ore does not fire
     `NotifyMining`, and forge smelting does not fire `NotifyIngotsSmelted` (agent). Bringing both proves mining and smelting.
3. **Collect the mule:** a bonded tier 1 Compact Mule, if a follower slot is free.
   - **The Haul contract:** F-38 is not built. `MuleErrand.FirstHaulContract` is the hook it will set; until then the
     player gets one line pointing them at Haul contracts on the League's board.

**One per character:** the errand is offered only at stage 0 and never again once `MuleGranted` is set.

**A mule lost for good:** a bonded mule is lost only if released or deleted (a dead bonded mule is still a follower).
- The page offers "Replace my mule" only when `MuleGranted` is set and the character owns no `PackMule` at all:
  ridden, following, stabled or auto-stabled. Any mule, bought, bred or errand, counts.
- The fee is 5,000 gold and 10 Mining Vouchers, through the same `TryPay`. Death and the slot are checked before the fee.
- A replacement is a fresh tier 1 mule; the lost bloodline is not recovered.

`PackMuleDeed` stays, for staff and as a reward item. Nothing sells it.

## 6. Part F: hooks for the module prompt

- **A saved, empty module list:** `PackMule.Modules` (`List<Item>`, field 14), and `ModuleSlots` from the tier table.
- **One place for the numbers:** `PackMule.Compute(mule)` returns a `MuleNumbers` from tier, quality and traits (pack
  weight and items, resists, stamina and the rest, slot cost, dungeon damage scale, keep-pack). Modules add through the
  static event `PackMule.ModifyNumbers`, then the caps apply. `ApplyNumbers` writes it all to the mule. The pack's
  capacity reads it live (`PackMuleBackpack`).
- **Death:** the pack drops to the corpse unless `MuleNumbers.KeepPackOnDeath` is set: that one flag is read in both
  `OnBeforeDeath` and `GetInventoryMoveResultFor`. Soul Tether II or a barding upgrade sets it from `ModifyNumbers`.
  Fact 3 switches it.
- **Traits for modules:** `PackMule.GradeOf(MuleTrait id)`.

## 7. Migration of existing mules

- `PackMule` v0 -> **v1** through the generator's `MigrateFrom(V0Content)`, the PetMimic pattern. The v0 schema is
  `server\migrations\Server.Mobiles.PackMule.v0.json` (`IsMale` bool, `NextBreedTime` DateTime), written by hand in the
  pinned format: the build does not emit our types' schemas.
- A v0 mule:
  - becomes **tier 3** (today's stats are tier 3's range);
  - **HP quality** is where its saved hits sat in 250-310; the other four qualities are rolled;
  - no traits, generation 0, no parents, an empty module list;
  - then, a tick after the load, its numbers are applied (tier 3 stats and Shadow Iron hue) and its slot cost becomes 1.
- `BredPackMuleDeed` v0 -> v1 the same way (`Server.Items.BredPackMuleDeed.v0.json`, no fields).
- **Fact 6 builds real version-0 bytes:** BaseMount's own part (written through a non-virtual call to
  `BaseMount.Serialize`), then the v0 header and the two v0 fields. It reads them back as tier 3, HP quality 50 from
  280 hits, the saved sex and cooldown, no traits and no parents. The fact detects from a v1 save whether the generator
  writes the version header as a plain or an encoded int, so it does not rest on a guess.
- `PackMuleBackpack` keeps version 0; its capacity is computed, not saved.

## 8. Build and tests

Through `docker\uo\build.sh -t sl-modernuo:cc-p69`; `latest` not moved, nothing deployed, restarted or committed. Logs
`D:\UO\cc-p69-build*.log` (not committed).

| Run | Result |
|---|---|
| 1, 2 (`--tests-only`) | compile: the generator already makes public properties for `Parent1`, `Parent2`, `Modules` and `Rolled` (mine removed); `Guilds()` is not on `ClusterFGuildSystem` (`GetDef` used) |
| 3 (`--tests-only`) | 1072/1073: `SmithBackButtonsVerification` found the null `AllFollowers` (headline 7); fixed |
| 4 **red** (`--tests-only`) | ten deliberate breaks (a tier number, slot cost 2, traits ignored, no tier-up, v0 to tier 1, no grade cap, gestation not saved, foal genes dropped, no rank gate, v1 fields not read): **all 11 mule facts failed**, plus `AccountDataSerializerVerification`'s round trip (it reads the League record too); nothing else |
| 5 full build | **1073/1073; image built** |
| **6** full build | after the CHANGELOG edit (section 10): **1073/1073; image `sl-modernuo:cc-p69` built** ("Built sl-modernuo:cc-p69 with patches applied and 1073 shard test(s) passing") |

**The facts** (`server\tests\Mobiles\Mule\MuleVerification.cs`):
1. The tier table and the hues.
2. Slots and the follower count.
3. `Compute`, shape, traits, cap, hook and the pack-on-death check.
4. A tier-up keeps everything.
5. Upgrade costs, all-or-nothing payment, and the rank.
6. Round trip and version 0 bytes.
7. Inheritance bounds over 1,500 breedings per pair of parent tiers, and the Lore curve.
8. Saved gestation and delivery.
9. The foal deed's mule.
10. The errand: gate, short delivery, delivery, collect, once only, and replacement.
11. The League record's version 0 bytes.

## 9. Deviations and decisions for Chase

1. **Errand gate:** Dull Copper (2). Iron (1) would open it the moment a player registers. `MuleErrand.RankGate`.
2. **Errand turn-in:** 50 iron ore and 25 iron ingots. Replacement fee: 5,000 gold and 10 Mining Vouchers.
3. **Upgrade steps 2 -> 3 to 4 -> 5** (section 2): placeholders, rising. They use Tinkers', Arcane and Warriors' scrip,
   which have no named currency yet.
4. **Str, Dex, Stam, skills, damage and armor per tier** (section 2): mine.
5. **Pack within a tier:** quality places it from 90% to 100% of your figure. Say if it should always be your figure.
6. **Traits per grade** (section 3), Deepdelver's effect (less damage in dungeons) and Celestial Tempered's
   (a little of everything): proposals.
7. **Inheritance numbers and the Lore curve** (section 4): as the overseer draft, with my roll sizes.
8. **Family names:** 20 in a list, drawn for a new line; the higher-tier parent's, or the dam's, after that.
9. **Hues on the body:** unverified. If a metal hue looks wrong on the mule, move it to the barding (the modules prompt).
10. **A replaced mule** is a fresh tier 1 with a new bloodline.
11. **Any mule blocks a replacement**, bought or bred included.
12. **Register line, proposed for the overseer** (agents do not edit `docs\`; the last number read was D-122):
    "D-123 | **Ours (cc-P69, F-33).** The pack mule: five tiers with metal hues, a bloodline (stat quality, graded
    traits, lineage), breeding that passes traits, 1 follower slot, earned through a League errand. No OSI mule exists
    to deviate from; recorded so the system is in the register. | logistics companion | `visible` | `cc-P69`"

## 10. Patch notes

`CHANGELOG.md` 2026.10.12.8:
- **Added:** the five tiers; bloodlines; the League errand.
- **Changed:** 1 follower slot; the Exchange raises tiers instead of selling; the foal deed shows the foal.
- **Fixed:** a foal is no longer lost to a restart.
- **Staff:** `[add PackMule <tier>`; deeds are for staff and rewards; existing mules became Shadowhide.

`VERSION` is 2026.10.12.8. The wiki page was not published.

## For Chase

**Deploy (when you choose):** commit (autopilot does), then build with `docker/uo/build.sh` and recreate the test shard
as usual. Existing mules load as Shadowhide tier 3, and their owners' follower counts drop by one each a moment after
the world loads. Players need nothing new in the package: the mule body is stock.

**In-game checklist (test shard):**
1. **Errand:** on a fresh character, register at the Registrar and open "The Compact's Mule": refused at Iron.
   Reach Dull Copper (play to it, or set the rank with the League rank tools), take the errand, try to deliver with 49 ore
   (refused, nothing taken), deliver 50 ore and 25 ingots, collect: a Compact mule (Dull Copper hue), bonded, 1 slot.
   Open the page again: "You have your mule". Release the mule, open the page: "Replace my mule" with the fee.
2. **Tier-up:** with the four currencies and 25,000 gold (or the Testing Token), open any trade guild's Civic Mule
   Exchange with the mule beside you: Upgrade to Bronzeback. Check its name, hue, more hits, a bigger pack, and that
   its pack contents, name and bond stayed. Look at each tier's hue on the body (`[add PackMule 3`, 4, 5).
3. **Breeding across a restart:** two of your mules, one of each sex (`[props IsMale`), context menu Breed, target the
   other. Save and restart the test shard within 24 hours (or `[props` the pending deed on the internal map:
   `DeliverAt`); the foal deed still arrives in your bank when due.
4. **Foal deed tooltip:** hover the deed: sex, tier 1, generation, family line, qualities, bloodline.
5. **Trade a foal deed** to another character, who uses it: the mule is theirs and carries the foal's genes.
6. **Old mules:** on the test shard's existing mules, check they show Shadowhide, 1 slot, and the owner's follower count.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last change:

```
Repo Result
---- ------
code dry run
docs dry run
```

22 files pending in code, 1 in docs (this note); nothing refused, nothing near 5 MB. Every file this task wrote is
ASCII. `PackMuleBackpack.cs` keeps its old box-drawing banner and one em dash from before this task (the line changed
here is ASCII); `PackMule.cs`'s old banner went with its rewrite.

P69 DONE
