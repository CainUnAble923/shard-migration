# P599: refresh the High Seas fishing guide draft

Written October 25, 2026. Documentation only. Updated `notes/wiki-drafts/high-seas-fishing.md` for P269 and its P587 fix-up as merged. This note is the requested work record. No code changed.

## Scope and editorial choices

Read AGENTS.md in both work copies first, then the direction decision and task-list guidance. Both copies started clean. Code checked at `8b0ccb80c00aedd9898be6f453d419b0a2119f2c`; notes started at `0e67b68b1fb60b28acef4ebfcec96e3a99d5d789`.

Read P269's implementation notes, the fishing P587 integration notes, P598's subsequent review, and the earlier P393/P426 guide and review evidence. P594's patch-note evidence was also consulted. Current source, rather than an implementation-note headline, determines the guide's access claims.

- Replaced obsolete planned labels for bait, enhanced bait, hooks, lava-pole fishing, the Oracle, summoning, fish pies, delivery orders, SOS oddments, and Corgul's implemented encounter pieces.
- Explained bait use, hook effects and wear, lava catches, the Oracle mechanism, delivery steps and standing, pie use, and the existing Cooking pattern gate.
- Kept built mechanisms distinct from normal acquisition. Lava traps and some bait have a delivery reward path, conditional on fish-monger placement. Current orders cannot award hooks, the Oracle, or Charybdis bait. Pie ingredients and normal champion access remain incomplete.
- Included P598's missing cancellation action because it affects accepting an order and dry docking. Referenced unresolved item-handling defects without publishing duplication instructions or claiming repairs.
- Kept guild Cooking deeds and proposed guild Fishing deeds separate from the implemented fish-monger deliveries. Retained the ship assessment's planned status and the original guide's unresolved naval-direction and training differences.
- Corgul is described as built but requiring staff placement, with altar and boat access unfinished. The guide does not repeat the disproven claim that a Mysticism spellbook is absent or promise the omitted handbook as current loot.

## Source evidence

Paths below are relative to the code work copy. `H/` means `server/customizations/Services/Expansions/High Seas/`. Line numbers identify the current source reviewed here, not runtime observations.

| Guide change | Evidence |
|---|---|
| Bait prompt, compatible equipment, combining cups, consumption | `H/Items/Fish/Bait.cs:79`, `:168`, `:177`, `:187`, `:210`, `:232`; `server/patches/FishingPole-high-seas-bait-hooks.patch`, `OnFishedHarvest` and tooltip additions. |
| Matching bait doubles a rare-catch roll, enhanced triples it; attire adds only with matching bait | `H/Items/Fish/FishInfo.cs:257`, `:287`, `:289`, `:383`, `:390`. Skill, habitat, and equipment filters still apply. |
| Hook application, replacement, effects and wear | `H/Items/Fish/Hooks.cs:67`, `:89`, `:102`; `server/patches/Fishing-high-seas-bait-hooks-lava.patch`, junk-proof skip and finishing callbacks; pole patch's `OnFishedHarvest`. |
| Lava routing, catch table, rock splitting | `H/HighSeasFishing.cs:39`, `:117`, `:175`, `:251`; `H/Items/LavaFishItems.cs:87`, `:96`, `:111`, `:120`, `:143`. Rock output is decorative; splitting can fail for the east-facing rock. |
| SOS oddments, bikini, barnacled salvage and strongbox | `H/HighSeasFishing.cs:85`, `:104`, `:108`, `:110`, `:113`; `server/patches/Fishing-high-seas-bait-hooks-lava.patch`, `ConstructCatch` additions. The bikini is pre-chest salvage, not a guaranteed chest reward. |
| Oracle charges and Charybdis mechanism | `H/Items/OracleOfTheSea.cs:26`, `:54`; `H/Spawners/CharybdisSpawner.cs:31`, `:103`, `:138`, `:149`; `H/HighSeasFishing.cs:298`, `:307`, `:316`. |
| Fish-monger setup and interaction | `H/Generate.cs:24`, `:58`; `H/Quests/ProfessionFishQuest/FishMonger.cs:75`; `ProfessionalFisherQuest.cs:33`, `:46`, `:146` in that quest directory. The setup lists Britain, Moonglow, Trinsic, Vesper, Jhelom, Skara Brae, Papua, and Sea Market for Trammel and Felucca. |
| Delivery quantities, destination, accepted fish and whole-catch handling | Quest-directory `ProfessionalFisherQuest.cs:116`, `:126`, `:161`; `ShippingCrate.cs:169`, `:196`, `:241`, `:253`, `:271`, `:283`. The guide gives the intended loaded-boat delivery procedure, not the remote-delivery bypass reported by P598. |
| Actual rewards cannot advance beyond tier 1 | Quest-directory `ProfessionalFisherQuest.cs:116` fixes one line and `:126` clamps it to at most 20 catches. `PlayerFishingEntry.cs:68` awards at most 3 points per catch, hence at most 60 per order. `FishQuestHelper.cs:125` requires 100 for tier 2. `ProfessionalFisherQuest.cs:170` and `FishQuestHelper.cs:157` use order points rather than accumulated reputation. |
| Reachable reward list and bait limits | Quest-directory `FishQuestHelper.cs:84` lists tier 1: Bait, LavaLobsterTrap, FishingGuideBook1, FishingGuideBook2, PowerScroll, FishingPole. `:194` limits tier-1 bait to the first rare-fish rows and `:198` allows enhanced bait. `:215` restricts Charybdis bait to tier 4; `H/Items/Fish/FishInfo.cs:88`, `:308` prevent fishing it up instead. The ascending tier conditions also leave tiers 3 and 4 unreachable. |
| Standing command and no usable cancellation action | Quest-directory `PlayerFishingEntry.cs:50`, `:206`; `ProfessionalFisherQuest.cs:277` only gives an in-progress Close button. `ShippingCrate.cs:223`, `:229` refuse disposal drops. P598 also checked its SmallCrate parent and pinned boat's nonempty-hold docking restriction. |
| Pie duration, effects, limits and consumption | `H/Items/Fish/FishPies.cs:67`, `:83`, `:121`, `:159`, `:182`, `:229`, and concrete pie definitions starting at `:247`; `server/patches/AOS-fish-pies.patch`. Fairy Salmon and Lava effects have no active consumer. The EJ player-versus-player exclusion is in `ScaleDamage`. |
| Oven recipes and pattern access | `server/customizations/Engines/Craft/CookingCraftRegistrations.cs:94` onward registers recipes with minimum Cooking 55 or 61 and oven requirements. `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:126`, `:153`, `:274` classify and check learned patterns. The guide gives the normal band-II book route without claiming the book supplies ingredients. |
| Missing ingredients | Searched canonical customizations, patches, and pinned ModernUO UOContent for `MentoSeasoning`, `SamuelsSecretSauce`, `DarkTruffle`, and `FreshGinger`. The matching files are `server/customizations/Engines/Craft/CookingCraftRegistrations.cs` and `H/Items/Resources/Cooking Ingrediants.cs`. They contain recipe requirements and item definitions, with no supplier. |
| Pie drops and Corgul's current scope | `H/Mobiles/Charybdis.cs:554`, `:558` roll two to five pies from its pie list. `H/Mobiles/Corgul/CorgulTheSoulbinder.cs:122` lists its current unique rewards. P269 records the staff-placement and missing altar/boat-warp work; P598 confirms that this access remains deferred after P587. |

Confirmed that P587's merge `db4c85b` is an ancestor of the checked code. Comparing P269's `19fd417` with its imported fix-up `30b225c` produces no differences for the High Seas customization directory, verification fixture, fishing and pie patches, or pole migration. P587 reports a successful build and test suite; those are attributed historical results, not tests rerun for this guide. P598's source findings remain relevant after that integration, especially the stronger tier-1 restriction that corrects P269's tier-1-or-2 summary. The read-only ModernUO source is pinned at `d4531cd94b739613155225c234900de9f47d2c88`.

## Verification and limits

No lane tests are required for this documentation-only task. No new tests were added. Source inspection does not verify the deployed server version, settings, NPC placement, accessible lava or island water, client display, sailing, timer-driven fights, or save round trips. These remain unverified. No Haven connection, deployment, account change, build, commit, merge, push, or branch switch was performed.

Ran `tools/progress.py --dry-run` against the work copies with `Path.write_text` suppressed in memory, because the report builder otherwise writes `tools/progress.json` even in dry-run mode. It completed; the attempted generated-report write was suppressed. No progress artifacts were changed, preserving the prompt's draft-and-notes scope.

Final review: `git diff --check` passed in both work copies. All relative Markdown links in the guide resolve. Both edited Markdown files use ASCII text, contain no em dashes or trailing whitespace, and are below 5 MB. Reviewed the remaining planned labels to ensure implemented fishing features are no longer labeled planned. Only the requested guide and this task note are changed; the code work copy is clean.

P599 DONE
