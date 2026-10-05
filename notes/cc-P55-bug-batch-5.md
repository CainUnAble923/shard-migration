# cc-P55: bug batch 5 (D69 to D76)

Builder task, 2026-10-05. Brief: `D:\UO\cc-prompts\cc-P55-bug-batch-5.md`. Engine authority: `D:\UO\ModernUO-pinned` at
`d4531cd94b739613155225c234900de9f47d2c88` (`git rev-parse HEAD` today); every pinned file:line below is against it.
`C\` = `D:\ShatteredLegacy\server\customizations`, `P\` = `server\patches`, `T\` = `server\tests`, `PIN\` =
`D:\UO\ModernUO-pinned\Projects`. Scratch: `D:\UO\cc-p55-work\`. Shard HEAD `411a922`, tree clean when I started. No
clash: nothing else wrote in `D:\ShatteredLegacy` while I worked (P54 is notes only). Nothing committed, nothing deployed,
no shard restarted, `sl-modernuo:latest` not moved.

## Headlines

1. **All eight parts done. Final build `docker\uo\build.sh -t sl-modernuo:cc-p55`: 45/45 patches (44 plus 1 new),
   749/749 shard facts (686 plus 63 new), image `sl-modernuo:cc-p55` = `b574b7e9fb95`.** `sl-modernuo:latest` is
   `a1158037d0d0` (P53's image) before and after.
2. **Red then green.** One red tree (`D:\UO\cc-p55-work\make-red.py`, built `--tests-only` as `sl-modernuo:cc-p55-red`,
   log `red.log`) undoes every P55 behaviour while keeping every API the facts call: **59 failed, 690 passed**. That is 55
   of the 63 new facts plus the 4 old hammer facts I had to update. The 8 new facts that stay green there are guards over
   behaviour P55 does not change (listed under "Facts, red then green").
3. **Part A pace (Chase's three rules, overseer's numbers kept):** T1 1,000 and T2 2,500 a metal; gain chance
   `max(0.05, 1 - current / cap)`; +3 exceptional, +1 normal. Expected crafts to fill a T1 metal: about 4,000 normal or
   1,300 exceptional (was 100). Table in Part A.
4. **Part B needs one pinned patch, `P\Ore-smelt-at-forge.patch`:** pinned's forge step is private and drives a target
   cursor. The patch makes it reachable (internal), adds `SmeltAt` and an ingot destination; the satchel calls the forge's
   own code once per pile, so the ratio, the skill check and the loss cannot drift. **Consequence for you:** the forge
   treats every post-Valorite ore as difficulty 50 (`PIN\UOContent\Items\Resources\Blacksmithing\Ore.cs:178`), so the
   satchel now smelts Platinum to Celestial at 50 Mining, where its own old table said 100. Deviation line D below.
5. **Part C: no stock cliloc reads "Smelt Ore".** The ore satchel reads **"Smelt"** (3006143, stock); the exact words need a
   client cliloc, which needs a Cliloc.enu pipeline we do not have (P52 Part B). I did not add one. The lumber satchel reads
   **"\* Magically Chops Logs into Boards \*"** (1158775, OSI's line for its own Lumberjack's Satchel).
6. **Part H, a design gap for you (headline-worthy):** OSI's vanilla turn-in pays far more item value than the guild bank
   on big deeds. A large Valorite exceptional plate deed pays a non-member, at any smith, about 200,000 gold **and a
   Valorite runic hammer every time**; a member banking gets about 1,500 Seals, a tenth of the catalog's 15,000-Seal Valorite
   runic. So I had to set cash out low to make banking the better deal (half the gold, the item 1 in 40), and **a member is
   now better off leaving the Society for large deeds**. Before P55 a member could take any deed to a regular smith for
   OSI's rewards; now that path pays them the guild's way. Numbers in Part H.
7. **Brief premises checked:** 74 `Reg(` calls (counted: 74). `C\ClusterFSmithBODSystem.cs:34-41` (the F-25 text's "smith
   vendors replaced with no-ops") has been wrong since cc-P32; the real vendor list is in Part H. "Large follows the stock
   gate, not P42's 70.1": **they are the same number**: stock is `Base >= 70.1` (`PIN\UOContent\Mobiles\Vendors\NPC\
   Blacksmith.cs:96`, `Weaponsmith.cs:68`) and P42's `LargeOrderSkill` is 70.1 on Base; the only difference is P42 also
   lets a Dev Testing Crystal through. Not verified by me: T5's old hue being near-black (I did not decode hues.mul).
8. **Found, not fixed (Part C sweep):** the pack mule's Breed entry shows **"Close"** (3006131); the trash bag's dump
   entry and the pet mimic's status entry both show **"Talk"**. No stock "Breed" cliloc exists. Listed in Part C.

## What changed (all uncommitted)

Shard (`D:\ShatteredLegacy`):
- `C\HammerOfHephaestus.cs` (full-file replacement, routed as before): Part A.
- `P\CraftItem-shard-hooks.patch`: two `+` lines now pass `quality == 2` to the familiarity hook (Part A). Hunk sizes
  unchanged.
- `P\Ore-smelt-at-forge.patch` (new) and its `apply_patch` line with the argument in `docker\uo\apply-patches.sh`: Part B.
- `C\CompactOreSatchel.cs` (Smelt Ore moved here), `C\ReinforcedOreSatchel.cs`, `C\SurveyorsSatchel.cs`,
  `C\DeepdelversSatchel.cs`, `C\MasterExpeditionSatchel.cs`: Parts B, C, D, E. `C\SeasonedLumberSatchel.cs`: Part C.
- `C\JacobsReinforcedPickaxe.cs`, `C\JacobsProspectorPickaxe.cs`, `C\JacobsDeepdelverPickaxe.cs`,
  `C\JacobsWorldbreakerPickaxe.cs`: Part E.
- `C\ClusterFAchievements.cs`: Parts F, G.
- `C\ClusterFSmithBODPayout.cs` (new), `C\ClusterFSmithBODSystem.cs`, `C\ClusterFAccountData.cs`,
  `C\SmithBulkOrderChoiceGump.cs`, `C\SmithGuildBook.cs`: Part H.
- Facts, new: `T\Engines\Craft\HammerFamiliarityPaceVerification.cs` (A, 8 cases), `T\Items\OreSatchelVerification.cs`
  (B to E, 25), `T\Misc\AchievementEarnedLineVerification.cs` (F, G, 15), `T\Misc\RegularSmithBODVerification.cs` (H, 15
  cases). Updated: `T\Engines\Craft\HammerFamiliarityVerification.cs` and
  `T\Engines\Craft\HammerHeldBonusVerification.cs` (they encoded the old +1 and the old cap 250; Part A).
- No migration JSON: no generated save shape changed (Part D, E argue it). `CharacterGuildData` (hand-written) went v1 to v2.

This repo: this note; `README.md`, `dashboard.html`, `tools\progress.json` from `tools\progress.py` ("812 customization
files, 50 patch files, 548 tests in 106 files"). `docs\bug-list.md`, `docs\feature-queue.md`, `docs\fidelity-principle.md`,
`notes\passdown-overseer-2026-10-03.md` and `notes\art\satchel-hues.png` were already modified or new when I started; not
mine, not touched.

## Part A: Metal Familiarity rises too fast (D69)

**Cause.** `RecordFamiliarity` added 1 on every successful craft to caps of 100 (T1) and 250 (T2), so T1 filled a metal in
100 crafts.

**Change** (`C\HammerOfHephaestus.cs`):
- `HammerFamiliarityPace` (`:113`): `GainChance = max(0.05, 1 - current / cap)`, `GainAmount = exceptional ? 3 : 1`,
  `Roll` rolls once (Utility.RandomDouble, so a seeded `BuiltInRng.Generator` replays it) and never passes the cap.
- `FamCap` public: T1 1,000 (`:147`), T2 2,500 (`:527`). Both `RecordFamiliarity` (`:305`, `:687`) take `exceptional`
  and roll through the pace. T1's refund chance reads the familiarity after the roll (`:319`): still
  `familiarity / cap * 20%`, 20% at the cap. T2's skill bonus formula is unchanged and reads `FamCap`, so +2.5 at the cap.
- The hook (`P\CraftItem-shard-hooks.patch`, the two `RecordFamiliarity` lines) passes `quality == 2`. `quality` is
  `CompleteCraft`'s own parameter (`PIN\UOContent\Engines\Craft\Core\CraftItem.cs:1313`), set to 2 by the exceptional roll
  in `CheckSkills` (`:852-855`) before the item exists. Argued: the only other place the quality is known is after the
  item is made (a bigger move of the hook); customizations alone cannot see it.
- Panel, tooltips and the restore gump read the caps (`:972`, the T1 refund line says "familiarity/1,000"; rows read
  "n/1,000" or "n/2,500"; T2 header "n/42,500"); tooltips say "Metal Familiarity: n (cap 1,000 a metal)" (the old text
  said "forge strikes", no longer true). The T1 to T2 upgrade carries values over capped at 2,500 (`:1376`).
- **Existing hammers keep their stored numbers** (the save format is untouched, still v1): a hammer at the old cap 100 now
  sits at a tenth (2.0% refund); a T2 at 250 in every metal now gives +0.2 instead of +2.5 (rounded to a tenth).

**Pace table** (expected crafts from 0, computed from the formula, `D:\UO\cc-p55-work` inline Python; "all exceptional"
is every craft exceptional):

| Hammer | Kind | 25% of cap | 50% | 90% | 100% |
|---|---|---|---|---|---|
| T1 (1,000) | all normal | 288 | 693 | 2,298 | 3,986 |
| T1 (1,000) | all exceptional | 97 | 231 | 763 | 1,336 |
| T2 (2,500) | all normal | 719 | 1,732 | 5,752 | 9,980 |
| T2 (2,500) | all exceptional | 240 | 578 | 1,914 | 3,334 |

Before: T1 100 crafts and T2 250 crafts to the cap, per metal. Mixed quality lands between the two rows.

**Facts** (`T\Engines\Craft\HammerFamiliarityPaceVerification.cs`): A1 caps 1,000 and 2,500 and the panel's rows and
header show them; A2 the chance is exactly 1, 0.5 and 0.05 at 0, half and near the cap, and 4,000 seeded rolls
(`new Random(5505)`) gain 100%, 46-54% and 3.5-6.5%; A3 (both tiers) +3 exceptional, +1 normal, capped; A4 T1 at the cap
shows 20.0% and 100 shows 2.0%, T2 with every metal at 2,500 held gives +12.5 (10 + 2.5); A5 (both tiers) a hammer saved at
the old cap loads its numbers unchanged; A6 through the real craft hook, exceptional ringmail gloves add 3 and regular ones
add 1. **Updated old facts:** `HammerFamiliarityVerification` rolls 0.0 (every craft exceptional), so it now expects 3 a
craft; `HammerHeldBonusVerification` A5 used 250 Iron as "the cap" for +0.1, now 2,500.

## Part B: ore satchel smelting matches the forge (D70, PT-12)

**Cause.** `ReinforcedOreSatchel.SmeltAllOre` gave `Math.Max(1, ore.Amount / 2)` for every pile with no roll (HEAD
`ReinforcedOreSatchel.cs:145`). Pinned's forge (`Ore.cs:166-257`): difficulty by metal (`:168-179`, everything not Dull
Copper to Valorite is 50), refuse below it (`:184-188`), refuse one small ore (`:190-195`), `CheckTargetSkill(Mining,
forge, difficulty - 25, difficulty + 25)` (`:197`), small = Amount / 2 (odd: one ore left), large = Amount x 2, mediums =
Amount (`:213-231`); a failure halves the pile or shrinks a single ore (`:243-256`). Freshly mined ore is large three times
in four (`:52-59`), so the satchel gave a quarter of the forge's ingots for typical piles.

**Seam, argued before patching.** The forge step is `BaseOre.InternalTarget.OnTarget`, a private class behind a target
cursor. Options:
- No patch: double-click each pile and invoke `from.Target` on the forge. Rejected: it replaces any target the player has
  pending, says "Select the forge..." once per pile, and drops the ingots loose in the backpack.
- Copy the formula into the satchel. Rejected by the brief (drifts).
- **Chosen:** `P\Ore-smelt-at-forge.patch`, 2 hunks, `--fuzz=0`: the class becomes `internal` and gains
  `SmeltAt(from, forge) => OnTarget(from, forge)` and `internal Container IngotDestination`; where the forge put the ingot
  in the backpack it tries the destination first and falls back to the backpack. With no destination (every stock use)
  the line behaves as before. Precedent: `Resmelt-smelt-one.patch` (cc-P18) made Resmelt's target internal for Craft X.

**Change** (`C\CompactOreSatchel.cs`): `SmeltAllOre` (`:206`) finds a forge within 2 tiles (`FindForge`, `:275`, the same
search as `DefBlacksmithy.CheckAnvilAndForge`, `PIN\UOContent\Engines\Craft\DefBlacksmithy.cs:30-90`, returning the item or
a `StaticTarget`; the forge step's own `IsForge` still decides), then for each pile calls the forge step with the satchel
as destination (`:244`). It counts ingots by the change in the backpack's ingot total (the satchel is inside it), and a pile
that made none is "failed" when the forge changed it and "left unsmelted" when it refused it. One summary line at the end:
"Smelt Ore: 4 piles: 3 smelted into 28 ingots, 0 failed, 1 left unsmelted." The forge's own per-pile messages also appear
(501988 "You smelt the ore... put the metal in your backpack", which is true: the satchel is in it; 501990 on a failure;
501986 "You have no idea how to smelt this strange ore!"). No forge: 1044265 "You must be near a forge.", nothing touched.

**Facts** (`T\Items\OreSatchelVerification.cs`): B1 six piles (large 10, medium 10, medium clump 10, small 10, small 11,
one large ore) each give exactly what the stock target gives for the same pile, run beside it as a player drives it
(double-click, target the forge), with the same ore left over, and every ingot in the satchel; B2 at 99 Mining a forced
failed check halves a 10 Valorite pile to 5 and turns a single large ore into a medium clump; B3 no forge: nothing; B4
four mixed piles at 90 Mining: iron large and small and Dull Copper smelt (23 iron, 5 Dull Copper), Valorite is refused
and left whole.

## Part C: satchel menu labels (D74, PT-14)

**Cause.** `base(6277)`; pinned adds 3,000,000 to any number at or below 0x7FFF (`PIN\Server\ContextMenus\
ContextMenuEntry.cs:39-48`), and 3006277 is "Salvage Ingots".

**How P29 F did it, done the same way:** pick a stock cliloc by reading the client's own `Cliloc.enu` with
`notes\cc-P29-tools\cliloc.py` (a port of pinned's reader), and put the number in the entry. Read from EA's
`D:\UO\UltimaOnlineVanilla\Cliloc.enu` (124,000 entries) and ClassicUO's copy (117,628), same text in both:
- Ore satchel: no entry reads "Smelt Ore" (searched every entry containing "smelt"). **Chosen 3006143 "Smelt"**
  (`C\CompactOreSatchel.cs:316`). Others seen: 1011072 "Smelt item", 1044016 "SMELT ITEM".
- Lumber satchel: its code turns every log into boards of the same wood (`ProcessAllLogs`). No "Process Logs", "Make
  Boards" or "Mill" entry exists. **Chosen 1158775 "\* Magically Chops Logs into Boards \*"** (`C\SeasonedLumberSatchel.cs
  :163`): OSI's own line for its Lumberjack's Satchel, which does this. Shorter alternative: 1015101 "Boards".
- **A client cliloc for the exact words "Smelt Ore": not added.** Per the brief I say it first: it needs patching each
  player's BWT-compressed `Cliloc.enu` through the package (P52 Part B describes the work and its unknowns). Your call.

**Sweep: every `ContextMenuEntry` in `C\`** (20 entry classes; counted with `grep ": ContextMenuEntry"`, each number read
from its constructor and resolved in EA's Cliloc.enu):

| Entry | File:line | Sends | Client shows | Does | Verdict |
|---|---|---|---|---|---|
| ImbueTableEntry | `ArtificersGuildmaster.cs:49` | 1114267 | Imbue Item | imbuing table | right (P29 F) |
| GuildMembershipEntry | `ClusterFGuildSystem.cs:748` | 3006146 | Talk | opens the guild hall | right |
| TalkEntry (Foresters, Miners' Liaison, Outriders, League Registrar, Survey Archivist) | `ForestersGuildmaster.cs:111`, `MinersCompactLiaison.cs:111`, `OutridersGuildmaster.cs:110`, `LeagueRegistrar.cs:97`, `SurveyArchivist.cs:75` | 3006146 | Talk | opens the NPC's menu | right |
| HammerFamiliarityEntry | `HammerOfHephaestus.cs:931` | 1112530 | Knowledge | familiarity panel | right (P52 B) |
| SmeltOreEntry (was ReinforcedOreSatchel's) | `CompactOreSatchel.cs:318` | was 3006277, **now 3006143** | was Salvage Ingots, **now Smelt** | smelts ore | **fixed** |
| ProcessAllLogsEntry | `SeasonedLumberSatchel.cs:165` | was 3006277, **now 1158775** | was Salvage Ingots, **now \* Magically Chops Logs into Boards \*** | logs to boards | **fixed** |
| SalvageIngotsEntry / SalvageClothEntry / SalvageAllEntry | `SmithGuildSalvageBag.cs:382, 393, 404` | 3006277 / 3006278 / 3006276 | Salvage Ingots / Salvage Cloth / Salvage All | exactly that | right |
| ConscriptEntry / ReleaseEntry | `Items\Quest\WispOrb.cs:484, 513` | 1153285 / 1153284 | Conscript / Release | exactly that | right |
| AppraiseforCleanup | `Services\CleanUpBritannia\CleanUpTrash.cs:148` | 1151298 | Appraise for Cleanup | exactly that | right |
| FeedEntry | `PetMimic.cs:1591` | 3006135 | Eat | feeds the mimic | near enough; reported |
| **PackMuleBreedEntry** | `PackMule.cs:235` | 3006131 | **Close** | **breeds the mule** | **wrong, reported** (its comment says "Tame"; no stock "Breed" cliloc) |
| **DumpEntry** | `TrashBag.cs:120` | 3006146 | **Talk** | opens the dump-for-points gump | **wrong, reported** |
| **CheckStatusEntry** | `PetMimic.cs:1609` | 3006146 | **Talk** | opens the status gump | **wrong, reported** (3000132 "Status" exists) |
| RegularSmithBulkOrderEntry (new, Part H) | `ClusterFSmithBODPayout.cs:450` | 3006152 | Bulk Order Info | the stock entry's number | right |

I fixed only the two satchels (the brief's "clearly wrong" set). The mule, the trash bag and the mimic are wrong but
outside D74; say if you want them (the mimic and the bag have stock clilocs that fit; the mule needs our own).

**Facts:** C1 on the wire the ore entry is 3006143, the lumber entry 1158775, neither 3006277, and the lumber satchel's real
menu carries 1158775 (modeled on `ImbuingTableLabelVerification`).

## Part D: Smelt Ore on satchel tiers 3 to 5 (D71, PT-13)

**Cause.** The entry and the smelt lived on `ReinforcedOreSatchel`; T3 to T5 derive from `CompactOreSatchel`.

**Change, from one place:** `CompactOreSatchel` holds the entry (`:187`), the smelt and the label, gated by `virtual bool
CanSmeltOre` (`:101`, false); T2 to T5 override it true. **No field, no base class and no version changed**, so every saved
satchel of every tier reads exactly as before: the generated serializers write the same bytes (all five classes still
`[SerializationGenerator(0, false)]` with no fields). That is why there is no migration JSON and no frozen byte stream here:
there is no old shape different from the new one. The fact below round-trips a T3 satchel saved in its pre-P55 state.
The T4 and T5 doc comments no longer promise "Smelt All" as future work.

**Facts:** D1 (5 cases) T2 to T5 show one Smelt entry and clicking it smelts a large pile of 10 to 20 ingots; T1 shows
none and `SmeltAllOre` does nothing; D2 a T3 satchel saved with its old hue loads, keeps its name and capacity, shows the
entry and takes the Verite hue.

## Part E: satchel and pickaxe tier hues (D72)

**Change.** `CompactOreSatchel.TierMetal` (`:92`, virtual) names each tier's metal; `TierHue` (`:95`) is
`CraftResources.GetHue(TierMetal)`, read from the metal's own entry (`C\ResourceInfo.cs`, the `m_MetalInfo` table), never a
literal. The pickaxes do the same with `const CraftResource TierMetal` and `FunctionalHue => CraftResources.GetHue(TierMetal)`.

| Tier | Satchel | Metal | Old hue | New hue | Pickaxe of the same tier | Old pickaxe hue |
|---|---|---|---|---|---|---|
| T1 | Compact Ore Satchel | Iron | 0x0482 | 0x0000 (none) | Jacob's Pickaxe (pinned replacement `P\JacobsPickaxe.cs`) | 0 (unchanged, already Iron) |
| T2 | Reinforced Ore Satchel | Gold | 0x8A5C | 0x08A5 | Jacob's Reinforced Pickaxe | 0x8A5C |
| T3 | Surveyor's Ore Satchel | Verite | 0x026C | 0x089F | Jacob's Prospector Pickaxe | 0x026C |
| T4 | Deepdelver's Ore Satchel | Valorite | 0x0455 | 0x08AB | Jacob's Deepdelver Pickaxe | 0x0455 |
| T5 | Master Expedition Satchel | Platinum | 0x0B2A | 0x0481 | Jacob's Worldbreaker Pickaxe | 0x0B2A |

**Existing items take the new hue on load**, in an `[AfterDeserialization]` method (`C\CompactOreSatchel.cs:333`,
`C\JacobsReinforcedPickaxe.cs:76` and the same in the other three), and only when the item still wears its tier's old hue.
Why on load and not on next use: the hue is saved by `Item` itself, and the load is the one moment that reaches every
satchel and pickaxe, in banks, houses and offline packs, with no player action; checking for the old literal keeps any
hue staff set by hand. **Exhaustion is safe without a new field:** a pickaxe's exhausted state is its hue
(`Hue == ExhaustedHue`, 0x0415), which is unchanged and is never an old functional hue, so a saved exhausted pickaxe loads
exhausted and a saved working one (old hue) loads working in the new hue. No hue on these items has the 0x8000 bit now.

**Facts:** E1 (5 cases) each new satchel's hue equals its metal's `GetHue` and the table value, no 0x8000 bit; saved in its
old hue it loads in the new; saved in a staff hue (0x21) it keeps it. E2 (4 cases) each pickaxe likewise, and a saved
exhausted one (0x0415) loads still exhausted.

## Part F: achievements say what earned them (D73)

**Cause.** Each threshold was a literal in the grant code (`if (kills >= 100) TryGrant(acct, "combat.century")` and so on,
HEAD `ClusterFAchievements.cs:875-1205`), with a second copy in each progress bar, so nothing tied the text to the rule.

**Change** (`C\ClusterFAchievements.cs`): an `AchievementTrigger` (`:65`; kinds `:24`) on every definition: kind, threshold,
skill level, skill, facet. The grant code now reads it: `GrantCounted` (`:1043`, every counted kind: kills, ore, ingots,
logins, gold, AP, renown, quests, ore types), `GrantSkills` (`:1059`, any skill, several skills, one skill, all on Base),
`GrantEvent` (one-time events, a facet by name). The progress bar's threshold is the trigger's (the second copy is gone).
`Describe()` (`:95`) writes the plain words from the same object; `EarnedLine` (`:213`) is "(Earned: ...)". Shown in the
earn popup after the flavor text (`:1688`, the popup 20 taller) and on every earned row of the list (`:2003`; rows now
64 high, five a page). Flavor text unchanged. Locked rows keep the description (which already says what to do).

Every line, as generated (74): e.g. "(Earned: slew 100 creatures)", "(Earned: mined 1,000 colored ore)", "(Earned: reached
100 in Mining)", "(Earned: reached 100 in 3 skills)", "(Earned: set foot in Felucca)", "(Earned: finished 38 New Haven
trainer quests)", "(Earned: held 10,000 gold in your bank)".

**Found while doing it:** `mining.ore_1k` and `ore_10k` describe "Mine 1,000 total ore", but their counter counts colored
ore only (`C\CompactOreSatchelRoutingHook.cs:215-219`: iron is not a tracked type). The Earned line says "colored ore",
which is what awards it; the description is unchanged (it is not flavor text, but I left it for you to word).

**Facts** (`T\Misc\AchievementEarnedLineVerification.cs`): F1 all 74 have a line from their trigger, keep their flavor, and
each progress bar's target is the trigger's threshold; F2 (10 cases, one per counted or skill kind: kills, Old Haven
mages, colored ore, ore types, ingots, bank gold, logins, any skill, several skills, one skill) one short of the threshold
awards nothing, the threshold awards it, and the line shows that number; F3 the popup and the earned row carry the flavor
and the line.

## Part G: retire the achievements above 200 (D75)

**Change.** `AchievementDef.Retired` (`:210`), set on the six (`retired: true`, `:396, :590, :630, :652, :674, :696`):
`skills.paragon` (any skill 250), `skills.grandmaster` (300), `skills.triple_grandmaster` (three at 300),
`skills.mining_legend`, `skills.smith_legend`, `skills.magery_legend` (300). `TryGrant` refuses a retired key (`:1116`) on
every path, staff grants included (the admin command says it is retired). Lists: a retired one never appears as locked;
**a holder sees it in its own section, "-- Retired (No Longer Awarded) --", after the locked ones** (`:1904`), still with
its AP and Renown (nothing is taken back). Progress: `ProgressCount` (`:1099`) leaves retired ones out of both numbers, so
the header reads "n/68". Item bonuses above 200 cannot earn them: retired is checked first, and the skill triggers read Base
anyway.

**Every other achievement, title or reward keyed to a skill above 200: none.** Checked: every skill trigger (the fact
below asserts the retired set is exactly the skill triggers above 200; the 200 rungs `skills.master`, `triple_master` and
the three `_elite` are reachable at the cap and stay); skill titles stop at 120 (`PIN\UOContent\Misc\Titles.cs:438`, "Legendary"); every `Skills[...].Base/Value` comparison in `C\` (15, none above 150:
armored meditation 150, P53); P53's sweep of every decimal 200-500 found only these six. F-12's level ladder is not built.

**Facts:** G1 the retired set is exactly the six and exactly the skill triggers above 200; G2 a character with every skill at
300 Base, plus a +100 Mining bonus, plus a staff grant, gets none of the six and does get the five 200 rungs; G3 a holder's
retired achievement survives the persistence item's save and load, the Skills tab shows it under Retired, a non-holder never
sees it; G4 the count is 2/68 for a holder of one retired and two live.

## Part H: regular smiths, Society members, bank or cash out (D76, PT-11, F-25 items 3 and 6)

**Every stock vendor that issues or accepts smith BODs** (grepped `SmithBOD|NextSmithBulkOrder` in `PIN\UOContent` and
`IsValidBulkOrder|SupportsBulkOrders|: Blacksmith|: Weaponsmith` in pinned, `C\` and `P\`):
- `Blacksmith` (`PIN\UOContent\Mobiles\Vendors\NPC\Blacksmith.cs:76-127`) and `Weaponsmith` (`Weaponsmith.cs:48-100`,
  AOS only), pinned.
- Their subclasses: `GeorgeHephaestus` (pinned, `Engines\ML Quests\Definitions\NewHavenSkillTraining.cs:1821`, a
  Blacksmith: the New Haven trainer) and our `GargoyleWeaponsmith` (`C\ClusterFGargoyleVendors.cs:280`).
- The Society's `BlacksmithGuildmaster` (pinned `Guildmasters\BlacksmithGuildmaster.cs:7`, our partial
  `C\ClusterFSmithBODSystem.cs:45`): not a regular smith.
- No other vendor touches smith deeds. (Tailor and Weaver take tailor deeds only.)

**1. Regular smiths offer Small or Large** (`C\ClusterFSmithBODPayout.cs:317-560`). Partial declarations of `Blacksmith`
and `Weaponsmith` (`:562`, `:576`) add two overrides neither pinned class has, so no patch: `AddCustomContextEntries` swaps
the stock "Bulk Order Info" entry (3006152) for `RegularSmithBulkOrderEntry` (same number, same timer check and the same
"available in about n minutes" message as stock, `PIN\...\BaseVendor.cs:1378-1418`), which opens `RegularSmithBulkOrderGump`
(Small; Large at 70.1, otherwise "needs 70.1 Blacksmithy (yours is n)").
- **Large gate: stock's, `Base >= 70.1`** (`ClusterFRegularSmithBODs.StockLargeSkill`, `:320`, citing `Blacksmith.cs:96`
  and `Weaponsmith.cs:68`). Same number as P42's; no Dev Testing Crystal bypass here.
- **Stock generation and timer stay, and either choice starts the timer.** `CreateChosen` (`:343`) calls the vendor's own
  `CreateBulkOrder(pm, true)`, which sets the timer (1, 2 or 6 hours by skill) and rolls small or large as stock; if it
  rolled the kind chosen, that deed is offered; if not, it is deleted and a stock deed of the chosen kind is made
  (`SmallSmithBOD.CreateRandomFor(m)`, `new LargeSmithBOD()`). So the timer is never copied and cannot drift. Opening or
  closing the menu starts nothing; cancelling pinned's accept gump after choosing has spent the timer, as stock does. The
  20% offer after buying from the smith (`BaseVendor.cs:554-566`) is unchanged (random). Deeds are stock deeds; the
  "Orders that still teach me" setting stays Society-only.

**2. Who gets what at a regular smith.** `OnDragDrop` (`TryMemberTurnIn`, `:407`): a non-member, or anything that is not a
smith deed, goes to pinned's `BaseVendor.OnDragDrop` (OSI's gold, item and fame), unchanged. A Society member's complete deed
is paid the guild's way (below), with the stock turn-in's own effects kept: the ML 10-second inspection pause and, under SE,
the timer reset (`OnSuccessfulBulkOrderReceive`). **One exception:** a member's large deed below 70.1 is not the guild's to
pay (the guildmaster's refusal already says "Any blacksmith will take this one"), so the stock path pays it.

**3. Bank or cash out, for members, at the guildmaster, at regular smiths and from the guild book** (`ClusterFSmithBODPayout`,
`:52-235`):
- **Bank** (default): `ComputeGuildReward`'s Seals, the current payout.
- **Cash out**: the deed's own OSI rewards (`BaseBOD.GetRewards`, `PIN\UOContent\Engines\Bulk Orders\BaseBOD.cs:61-69`):
  **half the OSI gold** (`CashOutGoldShare = 0.5`, `:56`; a bank check above 1,000 as stock pays it), the OSI fame, and the
  OSI item reward **with a 1 in 40 chance** (`CashOutItemChance = 0.025`, `:59`; otherwise the item is deleted unseen).
- **Standing and the Blacksmithy skill checks are the same either way**: both are the guild's reward for the work, not
  for the payout choice, so neither path is pushed for rank.
- **The setting**: `CharacterGuildData.SmithTurnIn` (`C\ClusterFAccountData.cs:650`), version 2 (`:612`, read `:707`,
  written `:748`, an unknown value fails loudly); v0 and v1 records read as "always bank". Shown and cycled (bank, cash
  out, ask) at the guildmaster's Bulk Order gump (`C\SmithBulkOrderChoiceGump.cs:79`) and on the guild book's order page
  under P46's teaching toggle (`C\SmithGuildBook.cs:352`). "Ask each time" shows `SmithTurnInChoiceGump` (`:241`): Bank
  (with the Seal figure), Cash out, or close to keep the deed. At a smith the deed bounces back to the pack while the
  choice is open.
- The guild book follows the setting too (I read "at both" as "every turn-in a member makes"; cash out from the book pays
  the gold into the pack).
- **No double pay, no dodge:** `CanPay` (`:122`) is checked at the moment of paying, choice gump included: the deed still
  exists, is in the member's backpack (a guild book in the pack counts; the bank box does not), is complete, the
  large-order skill is met, the member is still a member, and the smith (when paid at one) is within 12 tiles. The deed is
  deleted by the payment. A deed dropped on a smith is in the player's hand (a lifted item sits on the internal map,
  `PIN\Server\Mobiles\Mobile.cs:5173`), so a drop pays without the backpack check (`inHand`).

**The numbers** (bank against cash out, midpoint gold: `ComputeGold` pays 90% to 111% of the table, `PIN\UOContent\Engines\
Bulk Orders\Rewards.cs:474-501`; items valued at their own Seal catalog price, `C\SmithSealCatalogGump.cs:59-106`; the
115 power scroll, which the catalog does not sell, at 150, the midpoint of its neighbours on OSI's reward ladder, Ancient
Smithy Hammer +10 at 750 points (100 Seals) and +15 at 850 (200 Seals); gold valued at the guild's own rate, 3 Seals per
400 gold of deed value, `SealsForGold`):

| Deed | OSI points, item | OSI gold | Bank (Seals) | Cash out | Cash out in Seals | A non-member gets (OSI) |
|---|---|---|---|---|---|---|
| Small iron, 10, regular | 10, Sturdy Shovel (50) | 150 | **3** | 75 gold + 1/40 shovel | 0.6 + 1.3 = **1.8** | 150 gold + a shovel (51 Seals' worth) |
| Small Valorite exceptional, 20 (plate chest) | 800, power scroll 115 (150) | 12,000 | **90** | 6,000 gold + 1/40 scroll | 45 + 3.8 = **48.8** | 12,000 gold + the scroll (240) |
| Large Valorite exceptional plate, 20 | 1,200, Valorite runic hammer (15,000) | 200,000 | **1,500** | 100,000 gold + 1/40 runic | 750 + 375 = **1,125** | 200,000 gold + the runic (16,500) |

Banking beats cashing out by a third to a half on all three. The last column is headline 6: the guild pays a member far
less item value than OSI pays a non-member on the big deeds, by catalog price. If that is not what you want, the knobs are
the catalog prices (F-25's store work) or the two cash-out constants.

**Facts** (`T\Misc\RegularSmithBODVerification.cs`): H1 (both vendors) the menu has the choice entry and no stock entry, and
it opens Small and Large; H2 at 70.0 no Large button, the rule refused again and no timer started; at 70.1 Large; H3 (40,
60, 80) small chosen gives a small deed (at 80 swapped from the stock roll's large), the timer equals the stock request's
for the same skill (1, 2, 6 hours), a second request waits; H4 a non-member gets gold and no Seals; H5 (both vendors) a
member gets the deed's Seals and standing and no gold, and the default is bank; H6 cash out pays exactly half the OSI gold,
gives the shovel on a 0.0 roll and not on 0.99, no Seals, standing up; H7 bank beats cash out in Seals for the three
deeds above, from the live catalog prices; H8 default bank, a v1 record reads bank, every mode survives save and load,
and the version is 2; H9 "ask" at a regular smith, the guildmaster and the book shows the choice, keeps the deed, and Bank
pays; H10 a stale choice after the deed was paid elsewhere pays nothing; the large skill, the backpack and the 12 tiles are
checked when the button is pressed; H11 both gumps show the one setting and cycle it.

## Facts, red then green

63 new cases in four files; 4 old cases updated. Red: `D:\UO\cc-p55-work\make-red.py` (A: caps 100/250, a sure +1, the
hook's quality dropped; B: Amount / 2 with no forge step; C: both labels 6277; D: T3-T5 lose the entry; E: old hues, no
rehue; F: empty lines, every threshold one step late; G: nothing retired; H: stock entry kept, members paid the stock way,
Large ungated, no swap, cash out at full gold and a sure item, the setting neither saved nor cycled).

| Fact | Red | Green |
|---|---|---|
| A1 caps and panel; A2 chance and seeded rolls; A3 +3/+1 capped (2); A4 bonus at cap; A6 hook quality | red | green |
| A5 stored values unchanged (2) | **never red by design** (a guard: P55 never rescales) | green |
| B1 forge count: large, medium, clump, small odd, one large | red | green |
| B1 small even (10) | **never red**: Amount / 2 equals the forge for an even small pile | green |
| B2 failure loss; B4 mixed piles | red | green |
| B3 no forge | **never red**: refusing without a forge is unchanged behaviour | green |
| C1 labels | red | green |
| D1 T2, T3, T4, T5; D2 saved T3 | red | green |
| D1 T1 | **never red**: T1 had and has no entry | green |
| E1 (5); E2 (4) | red | green |
| F1; F2 (10); F3 | red | green |
| G1; G2; G3/G4 | red | green |
| H1 (2); H2; H3 at 80; H5 (2); H6; H7; H8; H9; H10; H11 | red | green |
| H3 at 40 and 60 | **never red**: below 70.1 the stock roll is always small, so there is nothing to swap | green |
| H4 non-member stock | **never red**: unchanged behaviour, a guard | green |
| Old: `HammerFamiliarityVerification` (4), `HammerHeldBonusVerification` A5 | red at build 1 against the new code (old expectations), green after the update | green |

## Builds

| Build | Command | Result |
|---|---|---|
| 1 | `build.sh -t sl-modernuo:cc-p55 --tests-only` (code, no new facts) | 45/45 patches; 686 tests, 5 failed: the old hammer facts' +1 and cap-250 expectations |
| 2 | same, all new facts | builder failed: analyzer xUnit2031 (`Assert.Single(x.Where(...))`) in my H1 |
| 3 | same | 749 tests, 2 failed, both my facts: A6 crafted a plate chest at 0.9 success chance, so its 0.999 craft failed (now ringmail gloves at 65); G3 looked only at page 1 of a paged list |
| 4 | same | **749/749** |
| red | red tree, `-t sl-modernuo:cc-p55-red --tests-only` | 45/45 patches; 749 tests, **59 failed**, 690 passed |
| final | `build.sh -t sl-modernuo:cc-p55` | **45/45 patches, 749/749, image `b574b7e9fb95`**; `latest` still `a1158037d0d0` |

Builder tags made: `sl-uo-builder:cc-p55`, `sl-uo-builder:cc-p55-red`. Docker answered throughout. The "Item.Amount <= 0
error" lines in every log are pre-existing (109 to 111 of them in P52's and P53's logs too).

## Deviations and decisions for you

Register lines (numbers are yours to assign; the register ends at D-114):
- **D-105 (amend), smith BODs on two paths:** a Society member is now paid the guild's way at every smith; regular smiths
  issue by a Small/Large choice. **Ours (cc-P55 H).**
- **D-115 Ours (cc-P55 H, Chase 2026-10-05).** Any blacksmith or weaponsmith asked for a bulk order lets the player choose
  small or large (large at 70.1 Blacksmithy, stock's gate); OSI picks large by a (skill - 40) / 300 roll. The stock timer
  and the 20% offer on purchase are unchanged.
- **D-116 Ours (cc-P55 H).** Society members' completed smith deeds are banked as Smithing Seals or cashed out for half
  OSI's gold, its fame and a 1 in 40 chance at OSI's item, by a per-character setting (default bank). OSI banks points per
  craft at a turn-in choice (ServUO `BulkOrderSystem.cs:105-142`); the rates are ours.
- **D-117 Ours (cc-P55 B, Chase 2026-10-05).** The ore satchels (tiers 2 to 5) smelt every pile near a forge as the forge
  does, through the forge's own code. OSI has no such satchel.
- **D-118 Ours (cc-P55 A).** The Hammer of Hephaestus's Metal Familiarity pace (caps 1,000/2,500, a rolled gain, +3
  exceptional). Ours entirely.

Decisions:
- **Part H headline 6:** members get less item value than non-members on big deeds. Options: raise bank value (catalog
  prices, F-25 store work), raise cash out (still under bank), or accept it.
- **Part B:** satchel smelting of post-Valorite ore now needs 50 Mining, as the forge does. If the forge itself should ask
  more for those ores, that is a forge change (pinned `Ore.cs:168-179`) and the satchel follows it automatically.
- **Part C:** "Smelt" instead of "Smelt Ore" unless you want a client cliloc. Lumber: "\* Magically Chops Logs into
  Boards \*" or "Boards". And the mule's "Close", the trash bag's and mimic's "Talk".
- **Part F:** the two colored-ore achievement descriptions say "total ore".
- Smaller: the achievements list now shows five rows a page (was six) so the Earned line fits; each smelted pile prints the
  forge's own message before the summary line; the New Haven trainer George Hephaestus is a Blacksmith and offers the
  choice too.

## For Chase

Deploy to the test shard first:

1. `docker tag sl-modernuo:cc-p55 sl-modernuo:latest`
2. `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -Down`
3. `D:\ShatteredLegacy\docker\uo\Start-TestShard.ps1 -SkipBuild`

In game on the test shard (a smith character; `[SetSkill Blacksmith 100`, `[SetSkill Mining 100` as needed):

4. **Hammer (D69):** single-click the Hammer of Hephaestus, choose Knowledge: every row reads "n/1,000" and the refund line
   says "familiarity/1,000". On the Reinforced hammer: "n/2,500". Craft about 20 plate pieces at a forge: Iron familiarity
   climbs by 1 or 3 per craft (3 for each exceptional), nearly every craft while it is low.
5. **Ore satchel (D70, D74):** `[add ReinforcedOreSatchel`, put in it `[add IronOre 10` (repeat for a few piles), stand next
   to a forge, single-click the satchel: the entry reads **Smelt**. Choose it: each pile gives the forge's count (a large
   pile of 10 makes 20 ingots), the ingots are in the satchel, and the last line reads "Smelt Ore: n piles: ...". Step away
   from the forge and try again: "You must be near a forge."
6. **Tiers (D71):** `[add SurveyorsSatchel`, `[add DeepdelversSatchel`, `[add MasterExpeditionSatchel`: each has Smelt.
   `[add CompactOreSatchel`: no Smelt.
7. **Hues (D72):** the five satchels side by side: T1 plain, T2 gold, T3 verite green, T4 valorite blue, T5 platinum.
   `[add JacobsReinforcedPickaxe` (gold), `[add JacobsProspectorPickaxe`, `[add JacobsDeepdelverPickaxe`,
   `[add JacobsWorldbreakerPickaxe` match. An existing satchel or pickaxe on the test world changes colour at the restart in
   step 3; an exhausted pickaxe stays charcoal and still says it is exhausted.
8. **Lumber satchel (D74):** `[add SeasonedLumberSatchel`, single-click: "\* Magically Chops Logs into Boards \*".
9. **Achievements (D73, D75):** `[achievements`: every earned row shows its flavor line and then "(Earned: ...)"; the header
   reads "n/68". Earn something new (on a fresh character, kill any creature): the popup shows the line too.
   `[ClusterFAchievement grant skills.grandmaster` answers "is retired and is never awarded".
10. **Regular smith (D76):** on a character **not** in the Society, single-click any Blacksmith in town, choose Bulk Order
    Info: a gump with Small and Large (Large needs 70.1). Choose Small, accept; ask again: "An offer may be available in
    about n minutes". Fill and hand in a deed: gold, as before.
11. **Member at a regular smith:** on a Society member (`[guild` to join), hand a complete deed to a town Blacksmith:
    "Society of Smiths: +n standing, +n Smithing Seals banked." and no gold.
12. **The setting:** at the Society guildmaster, Bulk Orders: the line "Completed orders: Always bank"; press its button: "Always
    cash out", again: "Ask each time". Open the Smithing Guild Book, order page: the same line and button. With cash out,
    hand in a deed: about half the usual gold, now and then a reward item. With ask: a two-button gump; Bank pays Seals,
    closing keeps the deed.
13. Promote to `docs\`: close D69 to D76 in `bug-list.md`; register lines above in `fidelity-principle.md`; F-25 items 3 and 6
    delivered in `feature-queue.md`.

P55 DONE
