# D28: `BestialArms` put back on the arms layer

2026-09-27, overnight task B. Bug-list **D28**, answers **Q-065**. Work is in `D:\ShatteredLegacy`,
uncommitted, not deployed.

- `server/customizations/Items/Artifacts/Equipment/Armor/Sets/Bestial/BestialArms.cs`: one line,
  `Layer = Layer.Arms;`, last in the constructor. Item ID and base call unchanged. LF and ASCII, as before.
- `server/tests/Items/Artifacts/Equipment/Armor/Sets/ArmourSetCompletionVerification.cs`: one new fact,
  `BestialArmsIsOnTheArmsLayerAndGoesOnOverAGargishChest`, and B11's hand-set layer removed for `BestialArms`.
- Final `build.sh`: **150 of 150** pass, `sl-modernuo:latest` built. No container started, stopped or restarted.
  Nothing committed.

The five things the brief asked for are sections 1 to 5. Section 5 is the one to read first: **§1 of the brief,
and my own D27 §4, got the mechanism half wrong.** The fix is the same either way.

---

## 1. No save holds a `BestialArms`

Checked **before** any code changed, and again at 20:53 CDT after the final build, with the armour-set task's
method (`notes/armour-set-completion.md`, the type-table table): every `SerializedTypes.db` parsed for `Server.*`
names, a positive control (`Server.Items.Dagger`) required in each, archives stream-decompressed and every
`SerializedTypes.db` member read. Script: `savecheck_d28.py` in this session's scratchpad, the CC9 `savecheck.py`
with `WANT = ['BestialArms']` and one change: **every archive file**, not only the last two of each kind as the
original read.

| Artefact | Tables read | `BestialArms` |
|---|---|---|
| Live `server/lib/uo/modernuo/Saves` | 1 (1,457 names) | none |
| `Saves-test` | 1 (202 names) | none |
| `Backups/Automatic`, every snapshot | 22 | none |
| `Archives/Daily`, all 30 files (2026-05-25 to 2026-09-27), every member | 591 | none |
| `Archives/Hourly`, all 24 files (2026-09-27-01 to 2026-09-28-00), every member | 288 | none |
| `Archives/Monthly`, all 3 files (2026-05 to 2026-07), every member | 37 | none |
| **Test container's own backups** (see below) | 10 | none |
| **Test container's own hourly archive**, 1 file, every member | 10 | none |
| **Total** | **960** | **0** |

**One control miss, explained, not ignored.** Of the 960, one table lacks `Server.Items.Dagger`:
`Archives/Daily/2026-05-28.tar.zst`, member `2026-05-28-09-55-01`. It is a real table (1,444 names;
`PlayerMobile` and `Longsword` present, and its neighbours an hour either side have the dagger): the world simply
held no dagger at that save. It is also four months before CC9 existed. Zero instances there too.

**Something the CC9 check did not look at.** `sl-modernuo-test` mounts only `Saves-test` from the host. Its
`Backups` and `Archives` live in the container's own filesystem, not under `server/lib`, so the host-side check
never sees them. I copied them out with `docker cp` (read-only on the container; nothing started or stopped) and
ran the same script over the copy: 10 automatic backups and 10 members of one hourly archive, 202 names each,
control present, none. **What that cannot cover**: backups made by earlier incarnations of the test container,
which went with those containers. The current `Saves-test`, which is what any instance would have to be in today,
has none.

**Containers**, by `docker inspect`: live `sl-modernuo` runs image `uo-modernuo` (image
`36cc709a82a6`), as D25 says; `sl-modernuo-test` runs image `2e7dcae65e54`, an **earlier** build of
`sl-modernuo:latest` (the tag has since moved; D26: a running container does not pick up a rebuilt image).

So the brief's expected case holds: **none anywhere, so the fix went in.** No migration needed today.

---

## 2. Red, then green

### Red: the new fact against the unfixed `BestialArms.cs`

`build.sh -t sl-modernuo:d28-red --tests-only`, with `BestialArms.cs` confirmed identical to HEAD
(`git diff --quiet`) and the test file already in its final form except for comment wording:

```
== 1/3 building builder stage (patches gate) ==============================
== 2/3 running ShatteredLegacy.Tests tests (test gate) ==========================
  Failed ShatteredLegacy.Tests.ArmourSetCompletionVerification.BestialArmsIsOnTheArmsLayerAndGoesOnOverAGargishChest [5 ms]
  Error Message:
   Assert.Equal() Failure: Values differ
Expected: Arms
Actual:   InnerTorso
  Stack Trace:
     at ShatteredLegacy.Tests.ArmourSetCompletionVerification.BestialArmsIsOnTheArmsLayerAndGoesOnOverAGargishChest() in /build/modernuo/Projects/UOContent.Tests/Tests/Items/Artifacts/Equipment/Armor/Sets/ArmourSetCompletionVerification.cs:line 374
  Standard Output Messages:
 chest 0x304 layer=InnerTorso equipped=True; GargishLeatherArmsType2 0x302 layer=Arms; BestialArms 0x4052 layer=InnerTorso equipped=False

Total tests: 150
     Passed: 149
     Failed: 1

BUILD FAILED: ShatteredLegacy.Tests tests did not pass. No image was built.
```

The printed line shows **both** halves failing, not only the first assertion: the layer is `InnerTorso`, and
`EquipItem` refuses the arms over a worn chest (`equipped=False`), which is what a player hits. The stock
`GargishLeatherArmsType2` reading `Arms` in the same host is the check that the seeded rows are live, so the red
is the item's fault and not the seeding's. The 149 that passed include B11, already without its hand-set layer
(section 3), the D27 guard (so the `finally` restores `MaxItemValue` to 0), and D26's fact.

### Green: the final files, full `build.sh`

```
== 1/3 building builder stage (patches gate) ==============================
== 2/3 running ShatteredLegacy.Tests tests (test gate) ==========================
Total tests: 150
     Passed: 150
[tests] 150 test(s) passed.
== 3/3 building runtime image sl-modernuo:latest =================================
Built sl-modernuo:latest with patches applied and 150 shard test(s) passing.
  Passed ShatteredLegacy.Tests.TestHostTileDataVerification.TheHostHasNoItemTileDataSoArmourAndWeaponsAreOnNoLayer [2 ms]
  Passed ShatteredLegacy.Tests.ArmourSetCompletionVerification.EachGargoyleHalfCompletesWithItsKilt [1 ms]
  Passed ShatteredLegacy.Tests.ArmourSetCompletionVerification.BestialArmsIsOnTheArmsLayerAndGoesOnOverAGargishChest [2 ms]
  Passed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: False) [29 ms]
  Passed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: True) [1 ms]
```

The runner prints a fact's output only on failure, so the green run has no `equipped=True` line to quote; the
assertions `armsOn`, `arms.Parent == m`, and both layers holding their pieces at once are what say it.
Between red and green the only non-comment change is the one line in `BestialArms.cs`. I ran green twice: after
the fix, and again after correcting two comments (section 5), so the quoted run is on the files as they stand.
150 = the 149 cases after D27 plus this fact.

**The fact**, for review: seeds `0x302`, `0x304` and `0x4052` with their real rows and raises `MaxItemValue` to
`0xFFFF`, all restored in `finally`, which is D26's reflection copied as the brief allowed. The rows, from
`client-data/classic-client/tiledata.mul` (3,188,736 bytes, the parse ending exactly there, D26's sanity rows plus
the gargish cloth chest and kilt re-checked), read field for field as pinned `TileData.Load` does:

```
0x0302 'gargoyle_leather_arm' flags 0x404002 weight 4  quality 19 (Arms)       anim 567
0x0304 'gargoyle_leather_che' flags 0x404002 weight 4  quality 13 (InnerTorso) anim 569
0x4052 'Gargoyle Armor Plate' flags 0x404002 weight 10 quality 13 (InnerTorso) anim 577
```

The mobile is a `PlayerMobile` with `Race = Gargoyle`, `Player = true` and 50 in each stat, so `BaseArmor.CanEquip`
runs its real race and strength checks instead of taking its non-player shortcut. It equips the chest, then the
arms, in a player's order, and asserts the arms are on `Arms`, on the same layer as ServUO's parent type, still
`0x4052`, worn, and that the chest is still on `InnerTorso` beside them.

---

## 3. B11's hand-set layer came out

`EachGargoyleHalfCompletesWithItsKilt` now does `var arms = new BestialArms(); m.AddItem(arms);` instead of
`Wear(m, new BestialArms(), Layer.Arms)`, with a two-line comment saying why. **It stays green**, in both runs:
in the red run it passed with the item on `Invalid` (the host has no rows, and the unfixed class sets no layer),
and in the green run it passes with the item on `Arms` from its own constructor. That is D27 §3.2's finding
again: `AddItem` is layer-blind and `SetHelper` walks `Mobile.Items`, so the fact never depended on the layer.

I removed it only from that one call, as asked. The other three Bestial pieces and the Virtuoso half still go
through `Wear`. `GargishEarrings` and `GargishNecklace` set their own layers too, so their hand-set layers are
redundant, but taking them out was not in the brief.

I did not add a layer assertion to B11. The new fact owns that claim; B11 is about set completion.

---

## 4. The §5 extraction trigger has fired

D27 §5 named the trigger for building the shared seed-and-restore scope as "the second fact that drives an
`EquipItem` path with armour or a weapon". `BestialArmsIsOnTheArmsLayerAndGoesOnOverAGargishChest` is that fact.
**The trigger has fired. Nothing was extracted**, per the brief; the decision is yours with both facts in front of
you:

- `server/tests/Engines/CharacterCreation/GargoyleStartingClothesVerification.cs:46-110` (D26, six rows, static
  save and restore helpers);
- `server/tests/Items/Artifacts/Equipment/Armor/Sets/ArmourSetCompletionVerification.cs`, the new fact (three
  rows, inline save and restore). Its header comment points here.

Side by side, what is actually duplicated: the `SetMaxItemValue` reflection (identical), the row tuple shape
(identical), the seed loop and the restore loop (identical apart from locals), and the flags `0x404002`, which
all nine rows share. What differs: which rows. D27 §5's sketch still fits both as written. One detail that sketch
should carry: both facts pass `quantity 0, value 0, height 1`, and every one of the nine real rows has exactly
those values, so a shared row constant can keep them fixed rather than take them as arguments. The parallel-safety
condition (every shard test class in `Sequential UOContent Tests`) is unchanged; I added no class.

---

## 5. What in §1 I now think is wrong

**The mechanism in D27 §4 (and so in the brief's §1, the bug-list D28 row and Q-065) is half right.** Reading
ServUO's `GargishLeatherArms` whole, not just its base call:

```
ServUO Scripts/Items/Equipment/Armor/GargishLeatherArms.cs
 10  public GargishLeatherArms() : this(0) { }
 16  public GargishLeatherArms(int hue)
 17      : base(0x302)
 18  {
 19      Layer = Layer.Arms;
 20      Weight = 4.0;
```

ServUO's `BaseArmor` does compute `Arms` from row `0x302` (`BaseArmor.cs:2373`), exactly as the note said. But
the parent **then sets `Layer = Layer.Arms` explicitly**, on line 19, and only after that does `BestialArms`
switch its item ID (`Bestial/BestialArms.cs:27`); ServUO's `ItemID` setter (`Server/Item.cs:4832-4855`) touches
weight, light and packets, never the layer. So the effective value is `Arms` by two routes, and one of them is a
statement in a file.

What that changes:

1. **"The inherited member is a value `BaseArmor` computes ... and it lives in no file" is wrong.** It lives in
   `GargishLeatherArms.cs:19`. This is AGENTS.md's final-parent rule in its **ordinary** shape: a statement in
   the old parent's constructor that the re-parent did not bring along. Our file's own header says it
   "reproduces stock `GargishLeatherArmsType2`'s own members", and it did: it reproduced **pinned's**
   `GargishLeatherArmsType2`, which has no layer line and relies on the row. ServUO's parent is the one with the
   line. The member list was taken from the wrong parent.
2. **"No file-to-file diff can catch it" is wrong for the same reason.** Diffing ServUO's old-parent constructor
   against ours would have shown the missing line.
3. **D27's sweep 2 had a blind spot, which is why it said "none".** It compared each ported type's **own** ServUO
   class for `Layer = Layer.X`. `BestialArms`' own class has no such line; its parent does. So "no second case"
   is proven for the shape sweep 2 looked at, not for this one: **ported types whose ServUO old parent assigns
   something in its constructor that our new parent does not**. I did not run that sweep: the brief said not to
   re-run D27's sweeps, and this is a new one nobody has reviewed. It is read-only and about the size of
   `layer_sweep.py`: for each re-parented type, walk ServUO's inheritance chain up to the first type we did not
   port, collect constructor assignments (`Layer`, `Weight`, `Hue`, anything), and diff against ours. **Worth
   scheduling**, because the same mistake (reproducing pinned's parent instead of ServUO's) could have dropped
   something other than a layer in other CC9 re-parents.
4. **Unchanged**: the defect, its player-visible effect, the row values, the saves reasoning, and the fix. The
   fix is now literally ServUO's statement rather than a reconstruction of an effective value, which is better,
   and the comment on the new line cites `:19`.

Smaller, in the brief itself: nothing else I could find. `0x304` is `GargishLeatherChestType1` (pinned
`GargishLeatherChestType1.cs:10`), the row values match, and D27 §4's line citations `:17`, `:2373` and `:27`
are all correct lines, `:17` just not the whole story.

**Not updated, because not mine to touch tonight**: the D28 row in `docs/bug-list.md` carries the "lives in no
file" wording and has no fixed status. That file has uncommitted edits in the working tree that are not from this
task, so I left it. It wants: the mechanism corrected per point 1, and the fix recorded.

---

## Method and scratch

In this session's scratchpad, not committed: `savecheck_d28.py` (+ `.out`, `_testct.out`), `anomaly.py` (the
control miss), `rows_d28.py` (the three rows), `red-run.log`, `green-run.log`, `testct/` (the test container's
copied backups). `D:\UO\ServUO-pub57` and `D:\UO\ModernUO-pinned` were only read. Tasks A and C's files were not
touched. Images: each run rebuilt the builder stage `sl-uo-builder:latest`; the red run built no runtime image (no
`sl-modernuo:d28-red` exists, as the gate intends); the green runs built `sl-modernuo:latest`, which no running
container uses. The row check covered all nine rows the two facts seed, D26's six included.
