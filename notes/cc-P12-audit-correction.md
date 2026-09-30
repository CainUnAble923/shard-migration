# cc-P12: the reachability audit's gate numbers, made honest (D39)

2026-09-30, CC. **A correction pass. Nothing built, measured or re-run.** Read and wrote only inside
`D:\UO\shard-migration\notes`, plus read-only greps of `D:\UO\ServUO-pub57` to check two facts (section 4). No
`build.sh`, no docker, `D:\ShatteredLegacy` not opened, `docs/` not edited. `docs/client-test-queue.md` and
`docs/feature-queue.md` were already modified in this working tree before I started; not mine. Nothing committed.

---

## 0. The answer

**The planning curve's first figure, "gates 1-5: 5 units, 117 files, 31%", is 65 files, 17%, delivered.** All five of
those gates have now been attempted, so there is no prediction left in it. The whole curve, restated with delivered and
predicted kept in separate columns:

| After | Predicted 2026-09-29 | Restated | Delivered | Still predicted | Of 372 |
|---|---|---|---|---|---|
| gates 1-5 | 117 | **65** | 65 | 0 | 17% |
| gates 1-9 | 167 | **104** | 69 | 35 | 28% |
| + Clean Up Britannia | 214 | **151** | 69 | 82 | 41% |
| all 27 | 292 | **227** | 70 | 157 | 61% |

**Why the instrument over-counts, in one line:** it finds the code site that would put a type in the world and stops
there. It never asks whether that site's own preconditions are met (a recipe, a resource, a placed carrier), and the
hand grouping on top of it read "pinned declares the owner" as "pinned has the list". **Gate 5 and blacksmithy hit
exactly because their sources are terminal**: the only precondition is something already in play (a player with ingots,
a spawner that is running), and pinned has the identical slot.

---

## 1. The brief undercounted the built gates

**The brief and D39 say four gates have been built. Nine have been built or attempted.** Ground rule 3: I counted them.
The brief's four rows are right as far as they go; it leaves out three craft gates from `notes/craft-registrations.md`
and Niporailem.

| Gate | Predicted (greedy) | Delivered | In the brief? | Source |
|---|---|---|---|---|
| 1 Blacksmithy | 33 | **33** | **no** | `craft-registrations.md` §0 |
| 2 Tailoring | 26 | **1** | yes | same |
| 3 Treasure chests | 24 | **0** | yes | `cc-P8-loot-tables-and-d35.md` §0, §2.2 |
| 4 Tinkering | 17 | **14** | **no** | `craft-registrations.md` §0 |
| 5 Stealables | 17 | **17** | yes | `cc-P8` §3.2, §3.4 |
| 7 Carpentry | 8 | **2** | **no** | `craft-registrations.md` §0 |
| 9 Pinned's commented drops | 7 | **2** | yes (with 12) | `cc-P7-pinned-waiting-drops.md` §0 |
| 12 Champion lists, bosses | 2 | **0** | yes (with 9) | `cc-P7` §0, §2.6 |
| 13 Niporailem | 1 | **1** | **no** | `reachability-audit.md` §1.3 |
| **Total** | **135** | **70** | | |

This matters to D39's framing. "Three of four missed badly" becomes **three exact (1, 5, 13), one close (4, 14 of 17),
five badly (2, 3, 7, 9, 12)**. The two gates the brief left out that hit (blacksmithy, Niporailem) are the evidence for
what a sound prediction looks like, which is the part of this task the brief says matters most.

Other brief figures, checked: tailoring 26 -> 1, right. Gates 9 + 12, "9 greedy, 17 alone" -> 2: right (7 + 2, 11 + 6).
Gate 3, 24 -> 0: right. Gate 5, 17 -> 17: right. The audit's "81 entries" in pinned's stealable table is 80 (`cc-P8`
§0); no file count depends on it.

---

## 2. What changed in `notes/reachability-audit.md`

| Where | Change |
|---|---|
| §0, before "Five one-file gates reach 117" | a dated italic line: 117 and 167 are predictions since built against; delivered 65, and 69 + 35 predicted; pointer to §3 |
| §3, under the heading | a correction box: what was corrected, that the ranked numbers are left as measured, what "delivered" means (source and tests, not client), P7's carriers unverified in the live save |
| §3 table | **new "Delivered" column**, after "Alone": a figure and the note section for each of the nine built gates, "not built" elsewhere, "70 from the 9 built" on the totals row. Inserted by script so no other cell moved (diff: 24 rows, one cell each) |
| §3 curve | **replaced** by a table with "Predicted", "Restated", "of which delivered", "of which predicted" columns, how the restated figures are built, three cautions on the predicted part, and the denominator stated |
| §3.1 (new) | the record (predicted, delivered, where the difference went); the mechanism (conditions A-D); why gates 1 and 5 hit; each unbuilt gate rated |
| §6, recipe row | dated italic: overstates gate 2 by 25, not 13, and resources overstate too |
| §7 item 5 | dated italic: "90 files alone" is 84 in the table and 50 delivered |
| Appendix A, top | dated italic: HEAD as measured; 70 of these files since delivered, see §3 |

Everything added is dated 2026-09-30 so the original measurement and the correction stay distinguishable. No original
number was edited or deleted.

---

## 3. What each number now rests on

**Delivered figures** are each taken from the note that built the gate, not recomputed here:

- **Craft gates (1, 2, 4, 7):** `content_index.py reach` on the live tree before and after, diffed per file against
  Appendix A, plus a hand check of every resource source (`craft-registrations` §3, §7) and 6 test facts watched red.
  50 files, 51 of the 340 counting `VillainousEpiphany`, which Niporailem had already reached.
- **Gate 5:** hand classification of ServUO's 158 stealable entries against both trees, 58 test facts, map statics and
  land tiles probed at every point, the weight cap checked (`cc-P8` §3). 55 types, 17 files.
- **Gate 9:** `reach --sources --json` on the live tree for the 17 drop types before the patches (15 already reached),
  plus 4 facts (`cc-P7` §2.7, §3). **Caution:** the reach tool will still call these two files unreached after the
  patches commit, because an uncomment patch's drop lines are context, not added lines (`cc-P7` §2.7). Anyone re-running
  the audit will see gate 9 deliver 0 until that is fixed.
- **Gates 3 and 12:** zero by reading, each declined target given a reason from source (`cc-P8` §2.2, `cc-P7` §2.3-2.6).
- **Gate 13:** the audit's own measurement on HEAD plus CC9 close's files (§1.3).

**Disjointness.** The 70 can be summed because each note measured its gate against that gate's own Appendix A group and
no file is in two groups. I checked the groups in Appendix A; I did not re-derive them.

**None of the delivered figures has been seen in a client.** The stealables and P7's drops go live on the next deploy;
P7's carriers (Miasma in the Labyrinth, Lady Lissith in the Twisted Weald) are unverified in the live save. The client-test
rows are proposed in `cc-P7` §4 and `cc-P8` §9.

**Predicted figures** are the audit's greedy column, unchanged. They carry two opposite errors that I cannot net off
without re-running the cover, so the restated curve is **the best available figure, not a bound** in either direction:

- **Could be low.** 65 files that built gates predicted and did not reach are back in the pool. Gates whose "Alone"
  exceeds their greedy figure (6, 8, 11, 14, 18) might pick some up: at most +15, +5, +2, +2, +5, and only for files
  their alone set contains. Gate 8 and gate 3's dinosaurs are the likeliest overlap. Unverified.
- **Could be high.** Every unbuilt gate still has the one-hop blindness in section 4.

The only true upper bound per gate is still its "Alone" figure, and then only on conditions A-D holding.

---

## 4. Why the instrument over-counts

### 4.1 What it measures, and what the gate figures assumed

The instrument's question is: **does some ServUO site construct, list or spawn X, and does pinned declare that site's
owner?** It answers that well. Across nine built gates, one credited source was not a source (`CrystalShards`, the first
resource in an `AddCraft` read as its product) and one reached type is not (`Putrefaction`, through a method nothing
calls), both in `craft-registrations` §4.1.

The gate figures then assumed that **a site found is X delivered.** That needs four more things, and every miss is one
of them:

| | Condition | Failed in |
|---|---|---|
| **A. No second condition** | once the site runs, X is handed over: no recipe, no scarce resource, no points, no objective | tailoring (25 recipe-gated, no recipe source), carpentry (6, peerless ingredients nothing drops), tinkering (a resource, a Doom recipe), gate 9 (Scrapper's rare recipe, never rolled) |
| **B. Live carrier** | whatever runs the site is itself placed in a world | gate 9 (Ilhenir, a Corrupt champion nobody places), gate 3 (Eodon guardians: no map points at Eodon) |
| **C. Pinned has the slot** | a "patch into a pinned list" needs the list | gate 3 (no lists; every file needs logic), gate 12 |
| **D. Nothing absent or twinned** | the entry needs no type in neither tree, and X is not a duplicate of something reached | gate 9 (Valley: six absent creatures and an ordinal trap), gate 12 (twins, D35 again), gate 3 (absent essences and specials) |

**A and B are the instrument's blindness**: it follows one edge, into X, and never the edges into the site. The audit
knew this for recipes (§6, 13 files) and it was undercounted by half inside one gate. **C and D are hand errors** in the
grouping and costing (`gatemap.py`), which §6 never listed. D39's statement, "counted a reference as reach without
checking the entry's other conditions", is A exactly; the gate 3 miss is C, a different fault, and worth naming
separately because a better instrument would not have caught it. Only reading pinned's chest would.

### 4.2 Why blacksmithy and gate 5 were different

Both sources are **terminal**: the site's only precondition is something already known to be in play, and pinned has
the identical slot.

- **Blacksmithy:** iron ingots only, no recipe (A); a player and a stock tool (B); pinned's `CraftSystem` appends and
  three hooks already did (C); 34 types, all ours, no twins (D). `craft-registrations` §0 says it outright: "Blacksmithy
  survived exactly because every one of its entries takes iron ingots."
- **Stealables:** each entry is its own carrier, a fixed placement, with the spawner enabled on the live world (B, read
  from the save, `cc-P8` §3.3); Stealing 100 and a weight cap, both checked (A); pinned ships the same table (C); the 11
  entries with absent types were never in the 17 files (D).

The same shape predicts the near-miss: tinkering is terminal for 14 of 17, and its three failures are A.

**The test for any prediction:** *is the source terminal, and does pinned have the slot?* A craft entry is terminal only
with stock resources and no recipe. A drop only if the creature is spawned. A reward table only if the currency can be
earned. A quest reward only if the giver is placed and every objective is reachable.

### 4.3 Two facts checked for the ratings

Read-only in `D:\UO\ServUO-pub57`, to rate gates 8, 17 and 19 on source rather than on the audit's text:

- `Scripts/Services/Expansions/TimeOfLegends.cs:98-133`: `CheckRecipeDrop` drops one of the 12 Aloron's and Darden's
  pieces directly (`Loot.Construct`, a third of successful rolls) and a recipe scroll otherwise, **only for kills where
  `SpellHelper.IsEodon(c.Map, c.Location)`**, at `Fame / 1,000,000` plus luck. So gate 8's set pieces need no recipe
  (A holds) but do need Eodon kills (B), which the gate's own spawn half supplies.
- `Scripts/Services/ChampionSystem/ChampionSpawnType.cs:147,154`: `AbyssalInfernal` and `PrimevalLich` are champion
  bosses. Their gates are Ilhenir's shape.

---

## 5. Which unbuilt gates to trust

A rating from existing notes and the two checks above, **not a re-measurement**. The same table is in the audit, §3.1.3.

| Gate | Predicted | Read | The condition at risk |
|---|---|---|---|
| **8** ToL drops + Eodon spawns | 14 | **mostly sound**, if both halves are built together | B (Eodon kills), plus C: pinned's death event passes only the creature (audit gate 6), and `IsEodon` in pinned is unchecked |
| **10** Clean Up Britannia | 47 | **count probably sound; cost is the risk** | a reward table is terminal once points can be earned; check the reward list for absent types (D). The 20 units are untested |
| **15** Virtue Artifacts | 7 | **count probably sound; cost rides on S7** | S7 unbuilt, shared with Shame |
| **17, 19** Primeval Lich, Abyssal Infernal | 6, 5 | **count sound, cost wrong** | B: needs a champion spawn of their type placed; `cc-P7` §2.4's ordinal trap means Unliving, Pit and Valley are one piece of work, not 5 units each |
| **6** Imbuing drops | 21 | **suspect, and low value** | B per creature, unchecked; worthless without imbuing |
| **11** Other crafts | 4 | **suspect** | A, tailoring's exact shape. `parse_defs.py` from `craft-registrations` answers it in minutes |
| **14** Underworld generator | 3 | **suspect** | a four-link chain; each link is an A |
| **16, 18** Quests | 7, 12 | **suspect until read** | A and B for each quest's giver and objectives |
| **21-27** | 14 | **suspect** | peerless placement and keys; gate 3's fidelity fork |

**Most trustworthy next pieces, if the curve is the guide:** gate 8 (verify two pinned facts first) and gate 10 on count.
**Least:** gate 11, which looks like one unit and is the shape that already failed three times.

**A re-measurement is not the only honest fix, and I did not start one.** For the built gates the correction is
complete: their numbers are delivered, not predicted. For the unbuilt ones, applying A-D in writing to each file's source
before a brief is an hour's reading per gate and would have caught every miss in section 1. Extending `content_index.py`
to follow second hops (recipes, resources, carrier placement) would be a new measurement, worth doing only if many gates
are about to be briefed at once. The two tool faults already on record (`craft-registrations` §4.1; `cc-P7` §2.7) should
be fixed first if it is ever re-run.

---

## 6. Proposed `docs/bug-list.md` D39 closing text

Plain text, for Chase to place; `docs/` not edited. It replaces the fix column's "Fix is a correction pass ... Until
then, treat any gate's file count as a ceiling and re-derive before briefing it."

> **DONE 2026-09-30 (cc-P12).** §3 of the audit now records delivered against predicted for all nine gates built or
> attempted, not four: blacksmithy 33/33, tailoring 1/26, treasure chests 0/24, tinkering 14/17, stealables 17/17,
> carpentry 2/8, gate 9 2/7, gate 12 0/2, Niporailem 1/1. 70 delivered against 135 predicted. The curve is restated
> with delivered and predicted in separate columns: gates 1-5 are **65 files (17%)**, not 117; gates 1-9, 104 (69
> delivered, 35 predicted); all 27, 227 (70, 157). Cause, in §3.1: the instrument follows one edge into a type and never
> the site's own preconditions (a recipe, a resource, a placed carrier), and the hand grouping read "pinned declares the
> owner" as "pinned has the list" (gate 3). Gates 1 and 5 hit because their sources are terminal and pinned had the
> slot. **Standing rule: before briefing any gate, check each file's source for a second condition, a live carrier,
> pinned's slot and absent or twinned co-requisites, and brief the number that survives.** Unbuilt gates rated in
> §3.1.3: 8 and 10 look sound on count, 17 and 19 sound on count with the wrong cost, 6, 11, 14, 16, 18 and 21-27
> suspect. No re-measurement. `notes/reachability-audit.md` §3, §3.1; `notes/cc-P12-audit-correction.md`

The D39 problem column also says "Four gates have now been built". If the row is kept as history, a note that it was
nine is enough; the closing text above carries the full list.

---

## 7. Not done

- No re-run of `content_index.py`, the greedy cover or `gatemap.py` (brief). So the "could be low" caution in section 3
  is unquantified beyond the "Alone" ceilings.
- The two known tool faults and P7's uncomment-patch gap were not fixed; the tool is not in this brief.
- Appendix A's groups were not re-derived, and still list the 70 delivered files as unreachable, as measured at HEAD on
  2026-09-29. A dated line at its top now says so and points to §3.
- No D-number or Q-number taken.
