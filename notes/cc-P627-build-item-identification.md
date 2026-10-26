# P627: item identification, stage 1 (the tooltip seam, the registry, weapons and armor, switched off)

Written 2026-10-25 by the Iron Golem (Claude Code). Builds stage 1 of [cc-P607-item-identification-design.md](cc-P607-item-identification-design.md), Chase's option B (10-25 evening: item-wide discovery, so once appraised an item shows its stats to everyone; Appraisal reveals magic stats, Arms Lore reveals resists; crafted items known; what is visible today stays visible). The design's build order for B is: "finish the disclosure policy/registry and a red leak test first, then the complete gear families and non-OPL outputs, then utility/trap adapters and economy/gain routes, then adoption and both-client verification. Keep the policy disabled until the whole supported surface is covered." This is the first step, made playable on the test shard for weapons and armor. The later stages are drafted as prompts at the end of this note.

## In plain words

- Nothing changes for players yet: the feature ships **switched off**. On the test shard, staff can turn it on with `[ItemKnowledge on` (and off again; nothing learned is lost).
- With it on, a new magic weapon or armor that drops from a monster shows only "Unidentified" and "Resistance and condition: uninspected" in its tooltip, under its plain name (a longsword, not "the Blade of Secrets"). The hidden numbers are not even sent to the client, so a tooltip script cannot read them either.
- Appraisal on such an item names its magic from 30 skill and reads the values from 60 (hard items need more). Arms Lore assesses its resists, damage types and condition from 30 and measures them from 60. Each skill unlocks only its own side, and what anyone learns shows to everyone who looks at that item. Once both sides are known, the item shows its ordinary tooltip.
- For Chase: nothing to decide now. Items that exist today and anything crafted are never hidden. To see it, on the test shard: `[ItemKnowledge on`, then kill a few monsters with magic loot (or `[ItemKnowledge conceal` and target a weapon), then use Appraisal and Arms Lore on it. Paid identification, the identification wand, jewelry and clothing, loot boxes and the Appraiser's quotes are the next stages.

## What changed (ShatteredLegacy, branch golem/Iron/P627)

| File | Change |
|---|---|
| `server/customizations/ClusterFItemKnowledge.cs` (new) | The policy, the property catalog, the registry (`ItemKnowledgeStore`, a `GenericPersistence`), Appraisal and Arms Lore stages, and `[ItemKnowledge`. |
| `server/patches/Item-property-list-policy.patch` (new) | Pinned `Server/Items/Item.cs`: a static `Item.PropertyListPolicy` delegate, consulted in `InitializePropertyList` before the item's full virtual builder. If it returns true it has filled the list; the stock builder and child properties are skipped. |
| `server/patches/LootPack-unidentified-magic.patch` (new) | Pinned `Misc/LootPack.cs` `Mutate`, AOS branch: after the runic attributes are rolled, `ClusterFItemKnowledge.OnLootMagic(item)`. |
| `server/patches/ItemIdentification-item-knowledge.patch` (new) | Pinned `Skills/ItemIdentification.cs`: an item target goes to `ClusterFItemKnowledge.TryAppraise` first. It returns false (the stock route runs) for anything not managed. |
| `server/patches/ArmsLore-item-knowledge.patch` (new) | Pinned `Skills/ArmsLore.cs`: after a successful weapon or armor inspection, beside P226's field maintenance, `ClusterFItemKnowledge.OnArmsLore`. |
| `docker/uo/apply-patches.sh` | Registers the four, after `ItemIdentification-appraisal.patch`. Each applies on top of the existing patch on its file (`Imbue-custom-property-hooks`, `ItemIdentification-appraisal`, `ArmsLore-field-maintenance`), with the argument in the comment. |
| `server/tests/Items/ItemKnowledgeVerification.cs` (new) | 8 facts, below. |
| `CHANGELOG.md`, `VERSION` | 2026.10.25.13, one Staff line (players see nothing while it is off). I skipped .12 because P626 uses it. |

### How it works

- **Only stamped items are managed.** A row in the registry marks an item as an unknown find. With the policy on, `LootPack.Mutate` stamps every new magic weapon and armor it makes (monster loot); `[ItemKnowledge conceal` stamps one by hand. Nothing else is ever stamped: items that exist today, crafted goods (smiths, runic tools), vendor stock, loot boxes and quest rewards keep their full tooltips. This is how stage 1 meets "what is visible today stays visible" and "crafted items known" without the design's adoption scan. A world with no rows has nothing to adopt. Stage 4's draft revisits this when more creation paths stamp.
- **The seam.** Pinned builds an item's cached list in `Item.InitializePropertyList` (`Item.cs:2584` in pin, shifted by the Imbue patch). The design rejected the alternatives, and I agree. Setting `Identified` does nothing for AOS tooltips. A return inside each stock builder misses derived overrides and the shard's own `Item.ExtraProperties` lines (Imbue, level gear), which run inside the base builder. Filtering in TazUO leaves the values in the packet. So the policy runs before the whole virtual chain. For a managed item it builds the full stock list privately (a scratch `ObjectPropertyList`), reads it back as (cliloc, argument) pairs, and passes on only lines the catalog gives an owner whose track allows them. The policy's output then goes through the normal `Terminate` and hash, so the client sees an ordinary, consistent list.
- **Allowlist, not blocklist.** Every cliloc the stock weapon and armor builders emit is in the catalog with an owner: Public, Appraisal or Arms Lore (pinned `BaseWeapon.GetProperties`, `BaseArmor.GetProperties`, the `AosAttributes`, `AosWeaponAttributes`, `AosArmorAttributes` and `AosSkillBonuses` builders, `Item.AddResistanceProperties`; slayer titles from `SlayerGroup`). A line no entry names is dropped while the item is concealed, including free text and the shard's extra lines. As the design asks, an unknown property stays hidden until someone reviews it. The name line is replaced by the item's plain art name (`1020000 + ItemID`): never its `Name`, label or type, so an artifact's or a custom name stays unknown. Art and hue are still visible, as the design accepts.
- **Owners:**
  - Public: weight, faction, race-only, exceptional, crafted by, engraving, one- or two-handed, skill required, and strength requirement. The strength requirement is Appraisal's while a lower-requirements enchantment is on the item, because the effective number would give it away.
  - Appraisal: every AOS attribute, hit spell and leech; slayers; skill bonuses; mage weapon and armor; self repair; durability bonus; lower requirements; balanced, velocity and immolated; artifact rarity; charges.
  - Arms Lore: physical, cold, fire, poison, energy, chaos and direct damage; weapon damage, speed and range; durability; the five resists; reflect physical damage; poison charges.
- **Stages:**
  - Magic: Unidentified, then Named ("Appraised traits: hit life leech, swing speed increase, slayer" plus "Magic values unknown"), then Values (the lines themselves). For a resist-only item, Named says its magic concerns resistance and points to Arms Lore.
  - Arms: Uninspected, then Assessed ("Inspected: fire damage, durability, ...; values not measured"), then Measured (the lines).
  - Both complete: the policy steps aside and the ordinary full tooltip shows.
- **Appraisal:** pinned ItemIdentification's item target. Below 30 Value: "You sense magic, but cannot identify it." From 30 the reachable stage is Named, from 60 Values. Difficulty is the design's first model, `D = clamp(15 x properties + 0.75 x strongest intensity, 10, 175)`, with the shard's own readers (the Appraiser's `RequisitionProperties.PropertyCount` and `IntensityOf` over the imbuing catalogue). Names are at `max(0, D - 60)`, values at D, each with a window 25 either side: `chance = clamp((skill - (d - 25)) / 50, 0, 1)`. Each use makes one roll, read against each reachable stage, so it never rolls once per property. A failure changes nothing, there is one second between attempts per character, and a known item says so without a roll. Values also sets the stock `Identified` flag (legacy labels). No skill gain from a managed item in this stage: the design's one-opportunity-per-find gain rule is stage 3.
- **Arms Lore:** after pinned's own successful inspect (its `CheckTargetSkill` and messages, and P226's field maintenance, unchanged), Value 30 assesses and 60 measures. Never lowers a stage.
- **On and off:** `[ItemKnowledge status|on|off|conceal|forget` (Administrator, DevTool, test shard only). The switch and the rows are saved (`ItemKnowledgeStore`, version 0). Switching rebuilds every managed item's tooltip. Off, every item shows its ordinary list and the Appraisal and Arms Lore routes are stock; nothing is forgotten. Rows of deleted items are dropped at save.

### A finding for balance (not changed)

The design's formula counts a slayer at full intensity. The test sword (hit life leech 20, swing speed 10, a silver slayer, 20% fire damage) has 4 properties and D 135 (the slayer is its strongest property at 100). Its names are at 75: 18% at 59 skill, the most a character can bring to the names stage (at 60 and up an Appraisal aims at the values). Its values are at 135: no chance below 110, certain from 160. The design says the formula "needs a real-item spread and balance review before implementation". I kept it exactly and record this for that review: an ordinary slayer weapon is expert work under it.

## Tests: red first, then green

How I ran them: builder image `sl-uo-builder:cc-P625` (this branch's base content), with `ClusterFItemKnowledge.cs`, the fact file and the four patched pinned files (`Item.cs`, `LootPack.cs`, `ItemIdentification.cs`, `ArmsLore.cs`, each built by applying the shard's existing patches for that file and then mine) bind-mounted; `dotnet test` filtered to `ItemKnowledgeVerification`. Every fact reads the item's real cached list (`Item.PropertyList.Buffer`, what the client is sent), so the seam is what is tested; `ObjectPropertyList.Enabled` is on for the facts so `InvalidateProperties` rebuilds as on the shard. Scripts, the stub, the mutants and every log are in the session scratchpad.

| Fact | What it pins |
|---|---|
| `AConcealedWeaponSendsNoneOfItsSecrets` (the leak test) | The stock list carries hit life leech 20 and an extra line from `Item.ExtraProperties` ("Hidden power: 42"). Once concealed, the list sent has the plain art name (also the header), "Unidentified", the uninspected line, one-handed and skill required. It has none of: leech, swing speed, the slayer, physical and fire damage, weapon damage and speed, durability, the custom name, the extra line, or any "20", "10" or "42". |
| `TheTwoTracksAreIndependentAndCompleteGivesTheOrdinaryTooltip` | Arms Lore at 65 measures fire damage 20 and durability while the magic stays unidentified. Appraisal at 59 names leech, swing speed and slayer ("Magic values unknown") and the measured resists stay. An expert's Appraisal completes it: the `Identified` flag is set and the list is exactly the stock list again. |
| `AppraisalAloneNeverMeasuresResists` | Appraisal at 120 shows leech 20 and the slayer, keeps the uninspected line and no damage types, weapon damage or durability. Arms Lore at 40 then assesses: "Inspected: ... fire damage ... durability ..." with no numbers. |
| `AppraisalStagesOneRollAndThePause` | At 20, "You sense magic". At 59, a roll exactly at the stage's chance fails and changes nothing. Trying again at once is refused for a second; after it, a roll under the chance names the magic. The formulas: names at D - 60, values at D, the window values (1.0, 0.5, 0.0), and a plain longsword at the floor of 10. |
| `ThePinnedSkillHandlersReachThePolicy` | Through `UseSkill` and the real targets: pinned ItemIdentification reaches Values on a concealed sword in the pack; pinned ArmsLore's success measures it. |
| `MonsterLootStampsNewMagicGearOnlyWhileOn` | `LootPack.SuperBoss.Generate` on orcs: with the policy on, every magic weapon and armor generated is concealed and shows "Unidentified"; with it off, none has a row. |
| `WhatIsVisibleTodayStaysVisible` | An unstamped sword (crafted, or found before) shows its exact stock list with the policy on. A concealed one shows its stock list with the policy off, Appraisal takes the stock route then, and it is concealed again when switched back on. |
| `TheRegistrySurvivesASaveAndLoad` | Through the store's own Serialize and Deserialize: the on switch and a row (Named, Measured) come back; a deleted item's row is not saved. |

**Red on the old code:** a stub `ClusterFItemKnowledge` with the same public names and no behaviour, with only the seam present in `Item.cs` (the facts compile against `Item.PropertyListPolicy`) and pinned's `LootPack`, `ItemIdentification` and `ArmsLore` as the build has them today. 8 of 8 failed.

**Green:** 8 of 8.

**Mutations of the finished code**, each run alone, each red where it should be:

| Mutant | Red facts |
|---|---|
| m0: the seam calls the policy but the stock builder still runs after it (`Item.cs`) | leak test, both track facts |
| m1: a line no catalog entry names is passed on instead of dropped | leak test (the "Hidden power: 42" line) |
| m2: fire damage owned by Appraisal instead of Arms Lore | both track facts |
| m3: loot stamps even with the policy off | the loot fact |
| m4: the on switch is not read back on load | the registry fact |
| m5: no pause between appraisals | the stages fact |

What the first runs found:
- The design's difficulty made the test sword too hard for the skills I first chose (59 for names, 100 for values). That is the balance finding above; the facts now use skills that fit the formula rather than changing it.
- The silver slayer's title is cliloc 1060479, which my catalog covers through `SlayerGroup`; the stock list showed it.
- The first leak-test run subscribed its extra line after the sword's list was already cached, so the stock list did not carry it. The fact now invalidates after subscribing, and asserts that the stock list carries the line before checking that the concealed one does not.

**Gated build:** I took the `docker-build` lock and dropped the Docker VM's page cache first (10.0 GB available at the first launch, 12.9 GB at the second).
- The first `docker\uo\build.sh -t sl-modernuo:cc-P627` stopped in `apply-patches.sh` with "FAILED: SmallBOD-crafted-only.patch - present in /patches but never applied or skipped by name". That was right after my four patches had applied. It is the known pipefail race (a "never applied" right after "Applied:" lines), and that patch is registered and untouched by me. I ran it once more, as the known fix says.
- The second run finished with EXIT=0: "Built sl-modernuo:cc-P627 with patches applied and 2510 shard test(s) passing". Of 2,514 tests, 2,510 passed and 4 were skipped (the real-map-data facts); none failed.
- All 8 item-knowledge facts passed in it, against the build's own patched files. The four new patches applied in order, and so did every existing fact on tooltips, Appraisal, Arms Lore and loot.
- I released the lock afterwards. The images are `sl-modernuo:cc-P627` = `d9763750f132` and `sl-uo-builder:cc-P627` = `4a8c6200828e`. The logs are `build-P627-run1.log` and `build-P627.log` in the session scratchpad.

## Deviations and decisions for Chase

- **Opt-in stamping instead of an adoption scan.** The design proposes concealing every supported new item by default and grandfathering existing ones with an explicit LegacyKnown record. Stage 1 inverts that: only items stamped at a creation path are concealed, so nothing that exists is touched and there is nothing to adopt. Trade-off: a creation path nobody stamps leaves its items visible (safe, never a leak). Stage 2 adds the other paths (loot boxes, rewards, champion and boss artifacts). I recommend keeping opt-in. Stage 4's draft asks whether the design's adoption record is still wanted.
- **Leaks that stay open while the policy is on (test shard only):** the League Appraiser's free quote and price breakdown, requisition matching messages, the imbuing gump and unravel previews, shop sale names, the legacy single-click route for clients without tooltips (only the stock `Identified` flag guards it), and secure trade. All are stage 2 or 3 work in the drafts. This is why the policy stays off: the design says "do not publish a partially protected feature".
- **No item gain:** Appraisal on a managed item does not train in stage 1; the stock route (unmanaged items) trains as before. The gain rules (one opportunity per genuine find and stage) are stage 3.
- **Serial reuse:** a row is keyed by serial and dropped for deleted items at save. Within one session a deleted item's serial is not reused by ModernUO's allocator in practice; stage 4's draft adds an explicit delete hook.
- **Fidelity:** the design's proposed fidelity entry is for the overseer to promote once the policy is switched on anywhere but the test shard.

## Unverified

- The tooltips in a real client (TazUO and a stock client): the server sends an ordinary list, but nobody has hovered one yet. Stage 4's draft has the both-client check.
- Derived artifacts and set pieces with their own `GetProperties` overrides: the seam covers them by construction (the policy runs before any override), but no fact builds one. Their extra lines are dropped while concealed.
- Monster loot on the real shard: the fact uses pinned's `LootPack.SuperBoss`; the shard's own loot tables that do not go through `LootPack.Mutate` are not stamped (safe: they stay visible).
- Performance: the policy builds the stock list twice for a concealed item (once privately), only when its tooltip is rebuilt. With the policy off it is one dictionary lookup per tooltip build.

## Checks before handing over

`git diff --check` is clean in ShatteredLegacy, and the new files (the customization, the four patches, the facts, this note) are plain ASCII with no trailing whitespace (a patch's blank context line is a single space, as in every existing patch). Nothing was committed or deployed, Haven was not touched, no world or test shard was started, and the policy is off in the build. The Read tool worked this time; no step was skipped.

## Remaining stages, as prompt drafts for the overseer to number

`P<nn>` is for the overseer to fill in. The order follows the design's for option B.

---

### Draft: item identification stage 2: every gear family and every non-tooltip output

```
# CC task P<nn>: item identification stage 2: jewelry, clothing and the other gear families, and every route that names or prices an item

**Model:** Opus

**Touches:** server

**Summary:** Stage 2 of `notes\cc-P607-item-identification-design.md` (option B, Chase 10-25), after P627's stage 1 (`notes\cc-P627-build-item-identification.md`): the seam and registry exist, weapons and armor from monster loot are managed, the policy is off. This stage covers the rest of the gear and closes the outputs that are not the tooltip.

## The work

1. Read the design's "Which information belongs to which skill", "Names and example tooltips" and "Put concealment before the full property builder" sections and P627's notes. Extend `ClusterFItemKnowledge`'s catalog and `IsSupported` to jewelry (`BaseJewel`), clothing and hats (`BaseClothing`, `BaseHat`), shields, spellbooks and slayer instruments, with an owner for every cliloc their stock builders emit; review the shard's extra lines (Imbue `ClusterFImbueEffects`, level gear `ClusterFLevelGear.AddTooltip`, `BaseSetWeapon` and other set pieces) and give each an owner or leave it concealed with a note.
2. Stamp the other creation paths of new magic gear while the policy is on: loot boxes (`LootBoxRoller`, before any description or reveal), the shard's own loot tables that bypass `LootPack.Mutate`, champion and boss artifacts, quest and event rewards. Crafting never stamps.
3. Close the non-tooltip outputs for a concealed item with the same name policy: the legacy single-click and equipment-info labels, shop sale names (`GenericSell` name/label), `LootBoxRoller.Describe`, the loot box reveal gump and flying loot, the player vendor gump, secure trade (show "Unidentified"/"Uninspected", and clear both acceptances if knowledge changes during a trade).
4. Red-then-green tests reading the real cached lists and gump/packet outputs: a ring, a hat, a set piece, an imbued item and a level gear item concealed with no secret line; a loot box's contents concealed before its reveal; a shop name and a trade window showing the safe name. Seen failing first; mutation evidence for guards that pass on the old code.
5. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. Keep the policy off. CHANGELOG Staff line.
6. Notes `notes\cc-P<nn>-item-identification-stage-2.md` with the catalog additions and anything left concealed. Last line `P<nn> DONE`.
```

---

### Draft: item identification stage 3: the economy routes, services, the wand and earned gain

```
# CC task P<nn>: item identification stage 3: the Appraiser's paid identification, the wand, blind sales, closing the quote leaks, and item gain

**Model:** Opus

**Touches:** server

**Summary:** Stage 3 of `notes\cc-P607-item-identification-design.md`: everything that turns hidden values into gold or information gets the identification rules, and Appraisal on found items trains the skill under the design's limits.

## The work

1. Read the design's "One Appraisal action and the alternative identification routes", "Trade, shops, banks and containers" and "Skill gain" sections and P627's notes.
2. League Appraiser (`Requisitions/Appraiser.cs`): Identify magic 100 gold and Inspect arms 50 gold per supported item, quoted before payment, rechecked on confirmation (distance, map, ownership, knowledge, gold), charged once, free for mundane and already-known tracks. On unknown magic show only the published blind price; no breakdown or property-specific requisition message until known (`RequisitionItems.cs` 329-343, 384-409).
3. Blind NPC sales: unidentified magic sells at a published category price (start 25% of the ordinary schedule), never from hidden values; validate per family below the minimum identified payout.
4. Identification wand (`Items/Wands/IDWand.cs`): through the same service, reveals the magic track only, one charge only when it adds knowledge, the shared one-second limit, no gain.
5. Gate the imbuing, unravel, reforging and level-spending screens behind the needed knowledge.
6. Item gain: one opportunity per genuine found item per magic stage, shared across accounts, consumed by the first eligible attempt (success or failure), only on an item the user may access and only when the stage's window can teach the user; persisted with the row; none for crafted, bought, staff, tutorial, known, mundane or vendor/trade targets. Use the shard's gain pipeline (`ClusterFSkillGain`), and update the ItemID row and its call-site facts.
7. Red-then-green tests: atomic, idempotent payments and wand charges; no fee for no-ops; blind price independence from hidden values; no hidden-value leak in quotes, matching or gumps; gain consumed once per stage across two characters, a restart and a trade. Seen failing first.
8. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. Keep the policy off. CHANGELOG Staff line (player lines when it goes on).
9. Notes `notes\cc-P<nn>-item-identification-stage-3.md`. Last line `P<nn> DONE`.
```

---

### Draft: item identification stage 4: hazards, the report card, lifecycle, both clients, and switching it on

```
# CC task P<nn>: item identification stage 4: hazard assessment and the report card, serial lifecycle, the both-client check, and the go-live decision

**Model:** Opus

**Touches:** server, client-package

**Summary:** Stage 4 of `notes\cc-P607-item-identification-design.md`, the last of option B: the 90+ hazard stage and item report card, the registry's lifecycle rules, a real two-client check, and the decision to switch the policy on.

## The work

1. Read the design's "Mundane items, general items and hazards", "Changes to an item" and "Introduction, fidelity and verification plan" sections and the notes of P627 and stages 2 and 3.
2. Appraisal 90+: hazard assessment through adapters for actual curse flags and supported magical traps (never mechanical trap details, never opening or disarming), and an item report card gump showing both tracks as known. Uncertainty is reported, never "safe". One acknowledgement before first equipping gear with unassessed hazards.
3. Lifecycle: an item delete hook drops its row (no serial reuse inheritance); stack split and merge rules; staff duplication; a changed enchantment, damage distribution or set membership invalidates the affected track (property revision). Adoption: P627 stamps opt-in at creation paths instead of the design's LegacyKnown scan; confirm with Chase (Ask-Chase.ps1) whether that stays, and record the answer.
4. Both clients on a loopback scratch shard under the test-shard lock (never Haven): the TazUO package and a stock client, hover, journal, single click, an open bank, a vendor and a secure trade, before and after appraisal; frames in the notes. Check the client package's skill name says Appraisal.
5. Red-then-green tests for hazards, the card, the delete hook, revision invalidation and split/merge. Seen failing first.
6. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. Then ask Chase (Ask-Chase.ps1) whether to switch the policy on for the live shard's next deploy; do not switch it on yourself. CHANGELOG player lines written for when it goes on.
7. Notes `notes\cc-P<nn>-item-identification-stage-4.md` with the fidelity entry for the overseer. Last line `P<nn> DONE`.
```

P627 DONE
