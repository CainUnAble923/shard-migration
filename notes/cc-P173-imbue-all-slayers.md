# cc-P173: Imbuing knows every slayer (Snow Elemental and 11 others are missing)

2026-10-18. Opus. Prompt: `D:\UO\cc-prompts\cc-P173-cont-imbue-all-slayers.md`. Not committed (the Golem commits
after DONE). Both repos were clean at the start.

## Headlines

- **The cause:** the imbue catalogue (`ArtificersImbueGump.cs`, `ImbueCatalogue`) registered 14 of pinned's 27
  slayers (`SlayerName.cs`, None aside). A weapon carrying any of the other **13** had no row, so the disenchant view
  listed nothing.
  - The 13: OrcSlaying, Terathan, LizardmanSlaughter, GargoylesFoe, BalronDamnation, Exorcism, FlameDousing,
    WaterDissipation, Vacuum, EarthShatter, BloodDrinking, SummerWind, ElementalBan.
  - The brief said 12 and listed 13: Exorcism is the extra one.
- **Reproduced red:** a War Axe with `Slayer = SummerWind`, the disenchant list (`GetActiveProperties`): **empty**
  ("disenchant sees: ", nothing after). The every-slayer fact named the 13 above. Chase's report exactly: the table
  "is not seeing slayer".
- **Fixed:** 13 rows, so **27 slayer rows, one per SlayerName**.
  - Disenchant now lists "Slayer: Summer Wind (Snow Elemental) [ON]".
  - Extract, through the table's own buttons, clears the axe's slayer and delivers "Essence of Slayer: Summer Wind
    (Snow Elemental)".
  - That row imbues it onto a Longsword.
- **Saved essences are safe.** The 14 old row names, which are what a `PropertyEssence.PropertyKey` holds, are
  unchanged. A fact pins all 14.
- **Super or lesser is OSI's:** the seven super slayers (ServUO `ItemPropertyInfo.cs:429-433`, IDs 121-127) are Silver,
  Repond, Reptilian Death, Exorcism, Arachnid Doom, Elemental Ban and Fey. That is the existing `SuperSlayers` set
  (`ArtificersImbueGump.cs`, cc-P82), unchanged. **The brief listed Daemon Dismissal as a super slayer; on OSI it is
  not.** Exorcism is the demon super slayer, and pinned's own `SlayerGroup` says Daemon Dismissal and Balron Damnation
  were folded into it. Kept lesser.
- **Spellbooks, instruments, talismans:** not imbuable on this table at all, and not on OSI either (Deviation 2).

## What changed

`D:\ShatteredLegacy` (uncommitted):

| File | Change |
|---|---|
| `server/customizations/ArtificersImbueGump.cs` | Comment :416 (every SlayerName has a row; the guard named). The cc-P173 block :433-451: why, the naming rule, Balron's OSI status, and 13 `AddSlayer` rows with the same costs, weights and threshold as the 14 before them (`AddSlayer`: 15 shards, 6000 gold, threshold 10, weapons only, family by `SuperSlayers`). The stale "verify against your ModernUO build" NOTE is gone |
| `server/tests/Misc/ImbueAllSlayersVerification.cs` (new) | The facts below |
| `CHANGELOG.md`, `VERSION` | `## 2026.10.18.14`: one Fixed line, one Staff line. VERSION 2026.10.18.13 → 2026.10.18.14 (.13 was committed with P171) |

`D:\UO\shard-migration`: this note; `testing\playtest-steps.json` (P173-1); `testing\bot-triage.md` (`### P173`);
`README.md`, `dashboard.html`, `tools\progress.json` from `tools\progress.py`.

**Names.** The pinned name first, as the existing 14 have it ("Silver (Undead)", "Repond (Humanoid)"), then OSI's
property name in brackets where it differs, from pinned `SlayerEntry.cs` `m_AosTitles` ("snow elemental slayer",
1060476). So:
- "Slayer: Summer Wind (Snow Elemental)", "Flame Dousing (Fire Elemental)", "Water Dissipation (Water Elemental)",
  "Vacuum (Air Elemental)", "Earth Shatter (Earth Elemental)", "Blood Drinking (Blood Elemental)";
- "Elemental Ban (Elemental)", "Exorcism (Demon)";
- and plain "Orc Slaying", "Terathan", "Lizardman Slaughter", "Gargoyle's Foe", "Balron Damnation".

Each `PropertyEssence` key is the row's name ("Slayer: <name>"). The existing 14 keep their names.

**What else reads the catalogue:**
- The table's button numbers: imbue 100 + the row's index in the item's list, extract 200 + it, craft 300 + the
  index in the whole list, under the 1000 confirm range (`BtnId`, :1523-1537).
  - Measured after the change: War Axe 75 rows, plate chest 37, gold ring 57, robe 26, whole catalogue 137.
  - All in range. The guard fact pins it.
- The mastery and craft-essence lists are paged (`ArtificersSatchel.cs`, the craft list in `ArtificersImbueGump.cs`).
- Rows are found by name everywhere they are saved (essences, mastery counts, work orders).

## Tests

Shard tests through `docker/uo/build.sh -t sl-modernuo:cc-P173` only.

**`ImbueAllSlayersVerification`**, 18 cases:
1. `ASnowElementalSlayerWarAxeIsSeenExtractedAndImbuedAgain`:
   - the disenchant list has the row;
   - extraction through the Imbuing Table's own buttons (Disenchant target, the row's Extract, Apply) clears the slayer
     and delivers the essence with that key;
   - the essence's row imbues Summer Wind onto a Longsword.
2. `EverySlayerNameHasExactlyOneRow`: for every SlayerName but None, exactly one slayer row reads it, and that row sets
   and clears it. Slayer rows = enum size - 1. This is the guard the prompt asks for: a new SlayerName in a pinned bump
   fails the build.
3. `AnOldEssenceKeyStillResolves`: the 14 old names, each resolving to exactly one row (14 cases).
4. `TheSuperSlayersAreOsisSeven`: every slayer's family, super or lesser.
5. `TheButtonRangesStillDoNotOverlap`: the row counts above.

**Seen red first** (old catalogue, `--tests-only`):
- 1 failed: the axe's disenchant list was empty.
- 2 failed: "no single row for" the 13.
- 4 failed (no row for them at all).
- 3 passed: it pins what must not change. **Seen red by mutation:** renaming the Ophidian row to "Slayer: Ophidian
  (Ophidian)" failed `AnOldEssenceKeyStillResolves(key: "Slayer: Ophidian")`, its only failure. Restored from a byte
  copy; `grep MUTATION` finds nothing.
- 5 was added after the red run, as a check on the change itself; it was not seen red (Deviation 4).

**After the fix:**
- tests-only: 1503 passed, 0 failed;
- the first full build had 3 unrelated failures (Deviation 3);
- **the final full build: `Built sl-modernuo:cc-P173 with patches applied and 1503 shard test(s) passing`** (1503
  passed, 0 failed, 4 skipped);
- a detailed run of the class in the built builder image printed the lines quoted here (18 of 18).

**Play-test tool tests:** `python -m unittest tools/tests/test_play_who.py`: 16 of 18. The 2 failures are earlier
work: M-001, P163-0, P164-0 and P165-1 to P165-6 have no Who or Where. P173-1 passes the shape test.

## Play-test items added

One, P173-1, under **For Chase** below. Sorted **BOT** in `testing\bot-triage.md` (`### P173`): the disenchant list,
the Extract row and the essence are gump text and an item the server sends. It has steps and a check line in
`testing\playtest-steps.json`.

## Deviations and decisions for Chase

1. **Balron Damnation (and Daemon Dismissal) are imbuable here but not on OSI.** ServUO's OSI table skips IDs 109-110,
   which are those two; on OSI both were folded into Exorcism. The brief asked for every SlayerName.
   - Daemon Dismissal was already in this table, so I added Balron Damnation the same way, as a lesser slayer.
   - The alternative: leave Balron out, or make both extract-only and never imbue.
   - Say if you want that; it would be a deviation either way, for `docs/fidelity-principle.md`.
2. **Slayers on spellbooks, instruments and talismans are not supported**, and I did not add them.
   - Pinned has `Slayer`/`Slayer2` on `Spellbook` and `BaseInstrument`.
   - `BaseTalisman` has a separate `TalismanSlayerName` (bear, vermin, ...), not `SlayerName`.
   - The table imbues only weapons, armor and shields, jewelry and clothing (`GetItemFlag`, :737): a spellbook has 0
     rows. It matches OSI, where Imbuing cannot touch spellbooks, instruments or talismans either.
   - Supporting them would mean new item kinds on the table, with their own rules (a spellbook's slayer is one slot,
     for its spell damage), not just more rows. Say if you want it.
3. **Flaky tests, unrelated to imbuing, were seen.** All passed on rerun or in other runs:
   - **First full build:** `CC6Batch2CreatureVerification` (HighPlainsBoura ControlSlots 1 for 2),
     `CC6Batch8Verification` (Medusa's random target picked another mobile left in the world) and
     `LootBoxFanfareVerification` (`:212`, an item deleted). The rerun was green with no change.
   - **Red run:** `WispOrbPossessionVerification` and `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies`.
   - **A pattern:** RaisedGarden has now failed once in each of P171 and P173, and the pet control-slot clamp has
     failed in P170 and P173.
   - They look like test-order or shared-world leaks; worth a CC prompt of their own.
4. **`TheButtonRangesStillDoNotOverlap` was not seen red.** It passes before and after the change (75 < 100); proving
   it would mean adding 25 rows to the weapon list. It is a measurement guard.
5. **No task-list tool exists in this session,** so per-step progress was not posted there; these sections follow the
   prompt's steps in order.
6. **Not deployed:** the test shard was not rebuilt or restarted by me. `sl-modernuo:cc-P173` (and
   `sl-uo-builder:cc-P173`) exist, and `latest` was not moved. The throwaway mutation builder image was deleted.

## For Chase

Rebuild the test shard from HEAD after the commit (or start it on `sl-modernuo:cc-P173`). Then, to try it in game:

1. **Snow Elemental slayer at the Imbuing Table:** an Artificers' Order member at an Imbuing Table, with the War Axe
   that has Snow Elemental Slayer (or `[add WarAxe` and `[set Slayer SummerWind` on it) and a second plain weapon.
   - Disenchant and target the axe; read the list.
   - Extract "Slayer: Summer Wind (Snow Elemental)".
   - Imbue it onto the second weapon.
   - **Pass:** the list shows "Slayer: Summer Wind (Snow Elemental) [ON]". The extract removes the slayer from the axe
     and gives an "Essence of Slayer: Summer Wind (Snow Elemental)". The second weapon then says snow elemental slayer.

Also answer Deviations 1 and 2 when convenient.

## Repo size rule

No file over 5 MB in either repo. The new test is about 11 KB; the other changes are lines in existing files. Build
logs and scratch stayed in the session scratchpad, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun` (after `tools/progress.py`):

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

Code: 4 files pending (`CHANGELOG.md`, `VERSION`, `ArtificersImbueGump.cs`, the new test). Docs: 8 (this note, the two
`testing\` files I wrote, the importer's `testing\SUMMARY.md` and `testing\play-tests.json` refreshed from Haven by the
dry run, `README.md`, `dashboard.html`, `tools\progress.json`). Nothing BLOCKED.

P173 DONE
