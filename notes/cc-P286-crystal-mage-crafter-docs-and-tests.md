# cc-P286: Crystal, SL_Mage and SL_Crafter wiki pages and test plans

2026-10-21. Prompt: `shattered-legacy-prompts/claimed/Crystal/cc-P286-crystal-mage-crafter-docs-and-tests.md` (claimed
from `queue/` at 12:37 UTC). Golem: Crystal, a Claude Code cloud session (machine `CLOUD`), GitHub only. Branches
`golem/Crystal/P286` cut from `origin/main`: code repo `2ab20d7` (version 2026.10.21.7), docs repo `125bcac`. Scripts
repo read at `main` `04148f2`: it still holds the five scripts (SL_Combat, SL_Loot, SL_Lumberjack, SL_Mining,
SL_Retaliate); **SL_Mage and SL_Crafter are not in it**, so the prompt's step 4 (review the scripts) could not run.

## Headlines

1. **Two draft wiki pages**, `uo:drafts:sl_mage` and `uo:drafts:sl_crafter`, written from the design docs: what each
   trains, setup, the window's buttons, what it never does, known limits. In `uo:drafts:` with a first line saying
   the script ships when Chase publishes it, as the prompt says for a script not yet in the scripts repo. The drafts hub
   lists them. No CHANGELOG line for players (nothing a player can use yet); one Staff line under 2026.10.21.8.
2. **Two test plans** in `notes/cc-P286-test-plans.md`: 12 steps each, from the docs' "Still to verify in game" lists,
   with the character to make, where to stand, what to look for and what each step proves. Because the scripts are not
   readable here, the plans say what the log should say rather than quoting it, and ask the tester to copy the exact
   lines back.
3. **The shard gaps the docs found, checked on today's main (section 3):** Magery to the cap is **not** fixed; Resist to
   the cap is **half** fixed (Curse and the necromancy curses reach the cap, the Mana line does not); the craft
   ceilings past 100 for Tailoring, Alchemy, Inscription and Cooking are **not** fixed; and the "nothing teaches at
   Blacksmithy 100" the crafter hit is recipe gating's Band V, not a missing ceiling. Reported only; P283 designs.
4. **One correction outside the two pages:** my P217 draft `uo:drafts:test_crystal` described the staff Dev Testing
   Crystal, and since then P190 (2026.10.20.15) built a different **Test Crystal**, the per-character skill gain booster
   every tester gets. The page now covers both, the booster first, so a tester reading it before the plans above sets
   the right crystal Off.

## 1. The pages

Under `docker/wiki/content/pages/uo/drafts/` on the code repo's branch:

| Page | Lines | From |
|---|---|---|
| `sl_mage.txt` (new) | 63 | `design/sl-mage-script.md`: the spell list, the circle table (min = -18 + 14 x (circle - 1), shown as 0 where negative; max = min + 40; mana 4 to 50), the Resist thresholds (Mana Drain 56, Paralyze 66, Mana Vampire 111, Curse to 120 and, on this shard, to the cap), the three v1 bug fixes as behaviour (bags opened, missing spell skipped, three failures skip for 30 minutes), REG_STOCK 150 |
| `sl_crafter.txt` (new) | 62 | `design/sl-crafter-script.md`: the eight crafts, batch 25 Craft X, Pick for (Fastest / Balanced 12 / Cheapest 0.5, described in words), recycle and deeds, restock (four batches), BOD gathering (built, not proven), the 400-tile walks, the v3 setup, the limits |
| `start.txt` (updated) | 11 | the two pages added; the Test Crystal line corrected |
| `test_crystal.txt` (rewritten) | 31 | `TestCenter/TestCrystal.cs:1-20, :38` (Off, 2x, 5x, 10x, 25x; test shard only; deletes itself elsewhere; below 10 skill nothing changes), CHANGELOG 2026.10.20.15; the Dev Testing Crystal part kept from P217 |

Rules kept from P217: plain language, no staff commands on a page (`[TCFill` and `[GiveTestCrystal` are "ask staff"),
no made-up screenshots, DokuWiki syntax as the existing seed. The two script pages carry no "Needed images" list on
purpose: the scripts are unpublished and the window may change before it ships; the test plan asks for the screenshots.

## 2. The test plans

`notes/cc-P286-test-plans.md`. Each plan opens with the character (skills, items, gold-free), the place, then a
12-row table: do, look for, proves. Every "Still to verify" item from the docs is a row:

- SL_Mage: `GetSpellsInSpellbook` after opening the book (row 2), the "not in book" text (3), the Curse buff name (5),
  summon release by context menu (6), meditation-blocking messages (7), the restock walk (8), "bank" from a distance
  (9), whether the gain-to-cap fix is in (10, with the answer from section 3), plus the v1a to v1d bugs and the stuck
  detector (1, 11, 12).
- SL_Crafter: material row names (3), the salvage bag entry (4), BOD tooltip and combine-contained (5), the accept
  gump and drop-on-NPC turn-in (7), the Foresters' picker (8), the Setup dropdown layout (1), bank restock (9), plus
  the menu read and Craft X parsing on today's build (2), the 100 wall (10) and Inscription's mana cap (11).

## 3. The shard gaps, checked on main 2ab20d7

Paths under `shattered-legacy-infrastructure/server/customizations/`.

| Gap the docs name | Fixed? | Evidence |
|---|---|---|
| **Magery gains to the cap** (SL_Mage: "8th circle above 120", "Whether the shard's Magery/Resist gain-to-cap fix is actually in") | **No.** The 8th circle's window ends at 120 and nothing of ours extends the casting schools. | `ClusterFSkillGain.cs:24` ("Not the casting schools (Chase: a Training Ward or a quest line, later)"); `:393-397` ("The Magery and Mysticism resist rolls pass the cap and stop at 111 by their own gate; they are left alone"); no `Spell*` or `Magery*` patch under `server/patches/` touches the gain (the three are the Urali trance, pet ability hooks and the spellbook talisman). CHANGELOG 2026.10.06 lists the 17 skills that pass their top; Magery is not among them. |
| **Resisting Spells gains to the cap** (SL_Mage: "Mana Vampire above Resist 120") | **Half.** The curse windows reach the cap: `SpellHelper.cs:371` (Curse's stat curse, `CheckSkill(MagicResist, 0, 120)`) and the four necromancy curses get hook G's gain-only roll on (0, cap + worn bonus). The Mana line (Mana Drain, Paralyze, Mana Vampire, `GetResistSkill`) is stock and stops where the doc says. So Resist climbs past 120 **only from Curse**, which needs Evaluating Intelligence above 0 and no curse already on. SL_Mage's "When only Curse teaches Resist" branch is the one that matters past 120; its Mana Vampire probe will read stuck. | `ClusterFSkillGain.cs:393-397` (the `MagicResist` row: location, (0, 120)); the hook G section from `:315` (its rule, `:20-25` in the header); CHANGELOG 2026.10.06 ("Resisting Spells ... keep rising with use, up to your skill cap"). The SL_Mage page and test plan say so. |
| **Craft ceilings past 100 for Tailoring, Alchemy, Inscription, Cooking** (SL_Crafter: "no ceiling path past their stock top items") | **No.** The ceiling table has four crafts and returns 0 for every other system. | `ClusterFCraftGain.cs:76-80` (`CeilingFor(system, res)`: `DefBlacksmithy or DefTinkering` to the metal ladder, `DefCarpentry or DefBowFletching` to the wood ladder, `_ => 0.0`); the header `:1-3` names the same four. Burrowhide (Tailoring 45, `Engines/Craft/BurrowhideTailoringRegistration.cs:1`) is a starter material, not a ceiling. Arms Lore to 200 (P226, CHANGELOG 2026.10.20.17) is its own path, not a craft ceiling. |
| **"Nothing left that teaches" at Blacksmithy 100** (SL_Crafter in-game run 10-16: "every visible item tops out at or below 100, and the shard's ceiling path starts at Platinum (Base 112.5). Shard design gap, not a script bug.") | **Not a missing ceiling; it is recipe gating.** Stock Blacksmithy items run to 140 (the kabutos), so there are items that teach between 100 and 112.5, but they sit in Band V (100 to 120) and are hidden until the account learns each one from a scroll; the menu's hint line says how many and where. The Platinum ceiling then starts at 112.5. So the way on at 100 is Band V scrolls (the Society's shop from rank 4, large bulk orders, loot boxes), which the script cannot buy or read. | `Engines/Craft/ClusterFRecipeTable.cs:45` (Band V, 100 to 120, scrolls), `:81` (the shop rotation at rank 4 and 5); `ClusterFCraftGain.cs:9-11` ("Stock items top out at 140 (Blacksmithy, the kabutos)"); `ClusterFMetalTiers.cs:20` (Platinum 112.5). The SL_Crafter page's Known limits say this in player words. |
| **Herbalism reagents** (P218's note; the prompt's "the herbalism reagents") | **Still not built.** The only mentions in main are the tutorial's gathering wing and the Alembic guild; the design now lives in the prompts repo. | `Tutorial/TutorialStations.cs:108` ("Herbalism (Order of the Alembic, not built)"); `shattered-legacy-prompts/design/f-herbalism-reagents.md` (design, 2026-10-21). |

Nothing here is designed or changed; P283 (queued, gain paths for every skill) owns the first three rows.

## 4. What I could not check from GitHub alone

- **The scripts themselves.** Not in the scripts repo (`main` `04148f2` lists the five of P144), so no review against
  the API gotchas, and the pages' button names and limits are the design docs' words, not the window's. When the
  scripts land, a one-prompt review against `design/legion-api-gotchas.md` is the prompt's step 4, still owed.
- **The in-game text** the plans ask the tester to copy (the "not in book" message, the Curse buff name, the salvage
  bag entry). The plans are written so the copying is the result.
- **Whether the design docs' ModernUO facts hold at `d4531cd94`** (the ML cast table, `GetResistSkill`'s thresholds,
  `AddStatCurse`'s skill check): the pinned tree is not in the cloud. The gaps in section 3 rest on our own code,
  which is.

## 5. Working as a cloud Golem, this prompt

Same as P217 and P218: the claim and the status lines went through the GitHub API tool (`git push` to the prompts
repo's `main` is refused here), everything else was ordinary git on the two `golem/*` branches. Having the design
docs in `design/` is what made this prompt possible at all; keeping them there, and adding the scripts to the scripts
repo, is what would let the next one review the code.

P286 DONE
