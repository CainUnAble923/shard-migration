# cc-P286: in-game test plans for SL_Mage v1d and SL_Crafter v3d

2026-10-21, Crystal Golem. One plan per script, from each design doc's "Still to verify in game" list
(`shattered-legacy-prompts/design/sl-mage-script.md`, `design/sl-crafter-script.md`). The scripts are not in the
scripts repo, so the **exact log and journal wording below is what the design says the script does, not text read from
the code**: where a step says "look for", the tester reads `SL_Mage.log` or `SL_Crafter.log` (beside the script) and the
journal for a line that says that thing, and copies the exact line into the result. Both run on the test shard with the
Test Crystal **Off**, so gains are the shard's own.

## A. SL_Mage v1d

### The character

- A fresh test character, **Magery 30, Resisting Spells 20, Evaluating Intelligence 0, Meditation 50**, Intelligence
  about 60. Low Eval on purpose: step 5 checks the no-curse case.
- A spellbook with circles 1 to 5 and **no Magic Reflection** (v1d's bug was looping on it).
- Reagents: 100 of each of the eight, **inside a closed bag inside the backpack** (v1a's bug), plus 150 of each in the
  bank box, some of them inside a bag in the bank (v1c's bug).
- Stand at the **New Haven bank** (guarded; the harmful spells only ever target the caster). A second run of step 9
  stands one screen away from the banker, out of the bank's reach.

### The steps

| # | Do | Look for | Proves |
|---|---|---|---|
| 1 | Start the script with the reagent bag closed. | Journal: the bag opens; the script says what it will cast first instead of "Nothing to cast: out of reagents". Log: the plan line listing the spells it can cast. | v1b's nested-bag opening. |
| 2 | Press **Show plan**. | Every castable spell with a gain chance and a cost; Magic Reflection absent or marked "not in book". | `GetSpellsInSpellbook` after the book is opened returns the book's real list (verify item 1). |
| 3 | Add Magic Reflection's scroll to nothing; instead put a spell you do not own on the plan by giving the character a bare spellbook with only circles 1 to 3, then Start. | The exact server text when it tries a spell the book lacks, and the script's line that it is skipping that spell for the session. Copy both texts into the result. | The "not in book" message text (verify item 2). |
| 4 | Let it run 5 minutes at Magery 30. | Mana Drain and Curse picks; Magery and Resist both rise (skill window). Log: each cast with its gain-chance score. | The pick rule at low skill (mock-tested, now in game). |
| 5 | With Eval Int still 0, watch a Curse cast. | No curse icon appears (duration 6 x Eval / 5 s = 0); the script uses **Evaluating Intelligence on itself** and Eval rises; a later Curse shows a buff icon. Copy the buff's name from the buff bar. | The Curse buff name (verify item 3), and that the script handles Eval 0. |
| 6 | Raise Magery to 80+ by any means (Test Crystal 25x for this step, then Off) and let it run. | It casts an Air, Earth or Water Elemental and the elemental vanishes at once; log: "released" (or the script's word) on the summon's context entry; no confirm gump stays open. | Summon release by context menu (verify item 4). |
| 7 | Empty the character's mana (cast until out) with the script running. | It meditates; if meditation is refused (armor, moving, already meditating), the journal line that blocked it is logged and it retries after a pause rather than looping. Copy the blocking text. | Meditation-blocking messages (verify item 5). |
| 8 | Remove all Mandrake Root from the pack, with a chest set as storage 20 tiles away (**Set Storage**, target the chest). | It walks to the chest, takes Mandrake up to 150 for the current and next circle, walks back and keeps casting. Log: the restock line with the counts. | The restock walk, copied from SL_Crafter v3a (verify item 6). |
| 9 | Set Storage on a **banker** instead; remove a reagent; stand 6 tiles from the banker. | It says "bank" (journal shows the speech), the bank box opens, bags inside it are opened, the reagent is taken; then stand 12+ tiles away and repeat: it walks closer first, or logs why it could not. | The "bank" speech from a distance (verify item 7), v1c and v1d bank fixes. |
| 10 | Take Resist to 115 (Test Crystal, then Off) and run 30 minutes. | Curse still raises Resist past 120 (the shard extends the Curse window to your cap); Mana Vampire does not. Log: Resist gains after 120 come only after Curse casts. | Whether the shard's gain-to-cap fix is in (verify item 8): **partly**, see the P286 note section 3. |
| 11 | Take Magery to 119.9 and run 30 minutes. | No Magery gain past 120; after 200 probes the script flags Magery "stuck" with its note about the shard fix. Copy the line. | The stuck detector, and the Magery gap (P286 note section 3). |
| 12 | Press **Stop** mid-cast, then Start again. | A clean stop (no cursor left open, `API.HasTarget()` false), and the remembered storage and spot come back from the persistent vars. | Clean stop and `SL_Mage_Store` / `SL_Mage_Spot`. |

Passing: every row's "look for" seen; `SL_Mage.log` has no Python traceback; the character never attacked anything and
no summon was left behind.

## B. SL_Crafter v3d

### The character

- A fresh test character, **Blacksmithy 0, Tailoring 0, Inscription 30, Tinkering 0**, Strength 60 (carry weight),
  Intelligence 50 (Inscription batches are mana-capped).
- Tools: tongs, a sewing kit, tinker's tools, a scribe's pen; 500 iron ingots, 200 leather, 100 blank scrolls and the
  magic arrow reagents in a bag in the pack; the same again in a storage chest 25 tiles away, and in the bank box
  (some inside a bag).
- A trash barrel next to the work spot; a salvage bag (Society of Smiths) in the pack; one small smith deed and one
  small tailor deed held.
- Work spot: the **New Haven forge** (anvil and forge within reach). BOD giver: the New Haven blacksmith for step 9.

### The steps

| # | Do | Look for | Proves |
|---|---|---|---|
| 1 | Setup for: "All crafts (shared)" is the first dropdown choice. Set Work Spot, Set Storage (the chest), Set Trash. Then Setup for: Tailoring, Set Storage (a banker). | The dropdown lists "All crafts (shared)" first and then the eight crafts; each Set says which choice it applied to. | Setup dropdown layout (verify item 7). |
| 2 | Start on Blacksmithy. | The menu is read once ("30 of N items visible" or the script's count); log: the item picked, its gain chance and cost. A batch of 25 runs; the Craft X summary "Made N in M attempts" is read back and a new item picked. | Menu read and Craft X parsing (seen 10-16; re-check on today's build). |
| 3 | Watch the first restock. | It walks to the chest, takes four batches of ingots, walks back. Log: the material rows it looked for, by name. Copy the row names it printed and the chest's item names side by side. | Material list row names (verify item 1). |
| 4 | After a batch, with the salvage bag in the pack. | The bag's context menu entry is used and ingots come back; log the entry's exact label. | Salvage bag "Salvage All" entry (verify item 2). |
| 5 | Hold a small smith deed for an item it is making. | The deed's tooltip is parsed (log: the deed's item, amount, exceptional, material); the made items go in by "combine with contained items"; the deed count rises. | BOD tooltip parsing and combine-contained (verify item 3). |
| 6 | Hold a large smith deed and two finished smalls it covers. | The smalls go into the large; no gump left open. | Smalls into large. |
| 7 | Set the New Haven blacksmith as a BOD giver, then force the giver timer (the script's setting, or wait six hours). | It walks there, drops the finished deed on the NPC (turn-in), opens Bulk Order Info, accepts the offer gump, repeats until refused, walks back. Log each step. | Accept gump and drop-on-NPC turn-in (verify items 4 and 5). |
| 8 | Switch to Carpentry with the Foresters' Union guild master as the giver. | The Foresters' picker (carpentry or fletching deed) is answered; log which. | The Foresters' picker (verify item 6). |
| 9 | Switch to Tailoring (storage is the banker). | It says "bank", waits for the bank box, opens the bags inside it and takes leather; log the serial it used. Repeat from 12 tiles away. | Bank restock (verify item 8), v3c and v3d fixes. |
| 10 | Let Blacksmithy run to 100 (Test Crystal 10x, then Off). | At 100: "nothing left that teaches" and a list of the best items that would, each with its missing material. | v3b's advice; and the shard gap in the P286 note section 3 (Band V scrolls are the way on). |
| 11 | Switch to Inscription at 30 Int 50. | Batches sized to mana; magic arrow scrolls; the summary read back; when Inscription reaches its top stock item, the same "nothing teaches" stop. | Inscription mana cap, and the no-ceiling gap for Inscription. |
| 12 | Press Stop mid-batch. | Craft X stops (its own Stop), no cursor open, the storage and spots come back on the next Start. | Clean stop and `SL_Crafter_Stores` / `SL_Crafter_Spots`. |

Passing: every row's "look for" seen; `SL_Crafter.log` has no traceback; nothing was sold, nothing left on the ground,
and every walk ended back at the work spot.

## C. What to send back

For each script: the two log files, the journal lines copied into the rows above, and a screenshot of the control window
and of the Setup dropdown. A row that fails goes back as a new prompt pinned `**Golem:** Crystal` when the fix is in the
script, or to the shard's bug list when it is the server.
