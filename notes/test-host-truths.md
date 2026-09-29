# P1: the tiledata seed, extracted, and the test-host truths written down

2026-09-28. Bug-list **D27** (with D15, D16, D26, D28). Work is in `D:\ShatteredLegacy`, **uncommitted, not
deployed**, alongside D27's and D28's own uncommitted changes, which were already in the tree.

- New: `server/tests/Route/TestTileRows.cs`, which holds the scope, the row constants and one fact that proves the scope.
- Moved onto it: `GargoyleStartingClothesVerification` (D26) and `BestialArmsIsOnTheArmsLayerAndGoesOnOverAGargishChest`
  (D28). **Neither keeps any reflection.** `grep SetMaxItemValue server/tests` now hits only `TestTileRows.cs`.
- Headers: `Route/ShardTestClock.cs` (D16's timer half, plus a pointer to D27), `Route/TestHostTileData.cs` (two stale
  lines), and D26's fact header. Notes: `notes/port-recipe.md`.
- Final `build.sh`, all three stages: **151 of 151**, `sl-modernuo:latest` built. That is 150 before plus the one fact
  I added. No production code changed.

**Read §6 first.** Most of the brief's §3 had already been done on 2026-09-26 (commit `7dfe7d1`). The D15 guard fact
exists, and the `ShardTestClock` header no longer states anything false about `Core.Now`. What was actually missing
was D16's timer half and all of D27.

---

## 1. The mechanism

```csharp
// D28's fact, as it now reads
using var tiles = TestTileRows.Seed(
    TileRows.GargishLeatherArmsType2,
    TileRows.GargishLeatherChestType1,
    TileRows.BestialArms
);
```

- **`TileRows`** holds one named constant per row, **nine** in all. These are D26's six and D28's three, and no row that
  no fact uses. Each constant is named after the class built on that graphic and carries every `ItemData` field (name,
  flags, weight, quality, animation, quantity, value, height), with the layer its quality means in a trailing comment.
  So what a fact depends on can be read at the call site, and the values and their source are in one file.
- **`TestTileRows.Seed(params TileRow[])`** returns an `IDisposable` scope. On creation it saves `MaxItemValue` and each
  named row, writes the rows, and raises `MaxItemValue` to `ItemTable.Length - 1` (`0xFFFF`, what `Load` sets for the
  shard's file, `TileData.cs:382`). `Dispose` restores the rows in reverse order, then the mask. Disposing twice is
  harmless. It refuses an empty list ("name the rows") and a row named twice.
- It must be opened **before** the items are built, because `BaseArmor` and `BaseWeapon` read the row once, in their
  constructors. The header says so, and the scope's own fact asserts it.
- **`TestTileRowsVerification.SeedPutsAStockPieceOnItsRealLayerAndDisposePutsTheHostBack`** is the gate on the scope
  itself. It records the mask, the row and a stock piece's layer before, inside and after, prints all of them, then
  asserts that the row is written, the mask is raised and the piece is on `Arms` inside, and that everything is exactly
  as it was afterwards. If the scope stops seeding or stops restoring, this fact fails by name.

The three D27 §4 constraints all hold:

1. **No `tiledata.mul` at test time.** The rows are literals. I re-read all nine from the shard's
   `client-data/classic-client/tiledata.mul` with an independent parser that follows pinned `TileData.Load` field for
   field. The parse ends at exactly 3,188,736 bytes, and the guard's two sanity rows (`0x13CC` weight 6 quality 13,
   `0xF52` weight 1 quality 1) check out. **All nine match the constants the two facts had, field for field.** As D28 §4
   said, every one of them has flags `0x404002`, quantity 0, value 0 and height 1. I still made those four fields
   explicit per row rather than fixed, because a future weapon row will not share them. Script: `rows_p1.py`, in this
   session's scratchpad.
2. **Nothing global.** The guard fact is unchanged and green (§2). Red C below shows it catching a leaked mask.
3. **Parallel safety:** §5.

---

## 2. Proof

Three red runs (`build.sh -t sl-modernuo:p1-red --tests-only`) and one green (`build.sh`). Each run took about six
minutes. **No `sl-modernuo:p1-red` image exists afterwards** (`docker images`), so every red run stopped at the test
gate as it should. Between runs the files were restored from copies in the scratchpad, `cmp` showed them identical to
those copies, and `grep "P1 RED"` over `server/tests` was empty before the green run.

### Red A: both call sites removed, scope intact. The proof the brief asked for.

The two `using var tiles = TestTileRows.Seed(...)` statements were commented out and nothing else changed.

```
  Failed ShatteredLegacy.Tests.ArmourSetCompletionVerification.BestialArmsIsOnTheArmsLayerAndGoesOnOverAGargishChest [1 ms]
  Error Message:
   Assert.Equal() Failure: Values differ
Expected: Invalid
Actual:   Arms
  Stack Trace:
     at ...ArmourSetCompletionVerification.cs:line 360
  Standard Output Messages:
 chest 0x304 layer=Invalid equipped=False; GargishLeatherArmsType2 0x302 layer=Invalid; BestialArms 0x4052 layer=Arms equipped=True

  Failed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: False) [27 ms]
  Error Message:
   Assert.NotNull() Failure: Value is null
  Stack Trace:
     at ...GargoyleStartingClothesVerification.cs:line 129
  Standard Output Messages:
 worn  Backpack                   layer Backpack  0x0E75
 worn  BankBox                    layer Bank  0x0E7C
 pack  RedBook                    layer Invalid  0x0FF1
 pack  Gold                       layer Invalid  0x0EED
 pack  Dagger                     layer Invalid  0x0F52
 pack  Candle                     layer TwoHanded  0x0A28
 pack  GargishClothChestType1     layer Invalid  0x0406
 pack  GargishClothKiltType1      layer Invalid  0x0408

  Failed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: True) [1 ms]
  Error Message:
   Assert.NotNull() Failure: Value is null
  ... (same, with GargishClothChestType2 0x0405 and GargishClothKiltType2 0x0407 in the pack)

Total tests: 151
     Passed: 148
     Failed: 3
BUILD FAILED: ShatteredLegacy.Tests tests did not pass. No image was built.
```

Each failure is the right one:

- **D26** fails at `:129`, `FindItemOnLayer(Layer.InnerTorso)`, with the whole outfit in the pack on `Invalid`. That is
  D27 exactly. Its two D26 assertions (no legs, a kilt present) passed before it, as its header says they should.
- **D28** does not fail on its first assertion. `arms.Layer == Arms` holds without any rows, because since D28
  `BestialArms` sets its own layer. It fails on the next one, `Assert.Equal(stock.Layer, arms.Layer)` at `:360`, the
  assertion D28 wrote as "the seeded rows are live". The stock arms read `Invalid`, and `equipped=True` shows the arms
  went on only because no chest had. So **that one assertion is what makes this fact depend on the seed**, and it did
  its job.

### Red B: the scope writes the rows but does not raise the mask

The single `SetMaxItemValue.Invoke(null, [LoadedMaxItemValue])` in the scope's constructor was commented out.

```
  Failed ShatteredLegacy.Tests.TestTileRowsVerification.SeedPutsAStockPieceOnItsRealLayerAndDisposePutsTheHostBack [2 ms]
  Error Message:
   Assert.Equal() Failure: Values differ
Expected: 65535
Actual:   0
  Stack Trace:
     at ...Route/TestTileRows.cs:line 243
  Standard Output Messages:
 before: MaxItemValue=0 row 0x302 quality=0 layer=Invalid; inside: MaxItemValue=0 quality=19 layer=Invalid; after: MaxItemValue=0 quality=0 layer=Invalid

Total tests: 151
     Passed: 147
     Failed: 4
```

The other three failures are the same three as red A, with the same messages and lines.

**This measures what D27 had only deduced from reading source.** Inside the scope, row `0x302` really holds quality 19,
and a `GargishLeatherArmsType2` built there is still `Invalid`. Seeding rows without raising the mask does nothing. It
is also why a helper that "just seeds rows" would have been a trap.

### Red C: the scope never restores

`Dispose` was made to `return` right after setting `_disposed`.

```
  Failed ShatteredLegacy.Tests.TestTileRowsVerification.SeedPutsAStockPieceOnItsRealLayerAndDisposePutsTheHostBack [4 ms]
  Error Message:
   Assert.Equal() Failure: Values differ
Expected: 0
Actual:   65535
  Stack Trace:
     at ...Route/TestTileRows.cs:line 250
  Standard Output Messages:
 before: MaxItemValue=0 row 0x302 quality=0 layer=Invalid; inside: MaxItemValue=65535 quality=19 layer=Arms; after: MaxItemValue=65535 quality=19 layer=Arms

  Failed ShatteredLegacy.Tests.TestHostTileDataVerification.TheHostHasNoItemTileDataSoArmourAndWeaponsAreOnNoLayer [< 1 ms]
  Error Message:
   Assert.Equal() Failure: Values differ
Expected: 0
Actual:   65535
  Stack Trace:
     at ...Route/TestHostTileData.cs:line 80
  Standard Output Messages:
 MaxItemValue=65535; LeatherChest layer=Invalid, EquipItem=False, parent=none; Dagger layer=Invalid; plain item weight=1

Total tests: 151
     Passed: 149
     Failed: 2
```

Two things came out of red C that I did not set out to measure:

- **The guard caught the leak by itself, and its printed line measures D27 §5's prediction about a global mask**, which
  until now was deduced. With the mask raised over empty rows, a `LeatherChest` stays `Invalid` and a plain item weighs
  a fictional **1**, where the host gives 0 and the shard gives 6.
- **Nothing else noticed.** In the console logger's order, 141 of the 151 results were reported after the scope's fact,
  so the leaked mask (and the seeded `0x302`) sat under all of them. The guard was the only one to fail. I have not
  established that the logger's order is exactly execution order, though with parallelization disabled I expect it is.
  If it holds, the guard is the only thing in the suite that would notice a fact leaving tile state behind. It is also a
  data point for the separate global-mask decision: raising the mask breaks nothing visibly, which is exactly why it
  should not be done by accident.

### Green: the final files, full `build.sh`

```
== 1/3 building builder stage (patches gate) ==============================
== 2/3 running ShatteredLegacy.Tests tests (test gate) ==========================
Total tests: 151
     Passed: 151
== 3/3 building runtime image sl-modernuo:latest =================================
Built sl-modernuo:latest with patches applied and 151 shard test(s) passing.
  Passed ShatteredLegacy.Tests.TestTileRowsVerification.SeedPutsAStockPieceOnItsRealLayerAndDisposePutsTheHostBack [4 ms]
  Passed ShatteredLegacy.Tests.TestHostTileDataVerification.TheHostHasNoItemTileDataSoArmourAndWeaponsAreOnNoLayer [< 1 ms]
  Passed ShatteredLegacy.Tests.ShardTestClockVerification.ADamagedMobileRegainsExactlyOneHitPerWheelTick [< 1 ms]
  Passed ShatteredLegacy.Tests.ArmourSetCompletionVerification.EachGargoyleHalfCompletesWithItsKilt [1 ms]
  Passed ShatteredLegacy.Tests.ArmourSetCompletionVerification.BestialArmsIsOnTheArmsLayerAndGoesOnOverAGargishChest [1 ms]
  Passed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: False) [68 ms]
  Passed ShatteredLegacy.Tests.GargoyleStartingClothesVerification.AGargoyleWithNoProfessionStartsInAChestAndAKiltAndNoLegs(female: True) [1 ms]
```

**151** is the 150 before this task plus `TestTileRowsVerification`. Counted: `grep -rnE '^\s*\[(Fact|Theory)'` gives
150 attributes, and D26's theory has two cases.

One thing to disclose: in red A, the scope's own fact was an earlier draft that asserted before printing. I rewrote it
to print first before red B, so the three facts red A is about are unaffected. Every other file in red A was the final
text, apart from the two commented-out call sites.

---

## 3. The corrections, old line beside new

### `server/tests/Route/ShardTestClock.cs`

**`Arm()`'s doc comment** was the one place that still claimed too much for D16:

| Old | New |
|---|---|
| `/// Core.TickCount, dropping timers left behind by an earlier test.` | `/// Core.TickCount, emptying it. Every timer on the wheel is dropped and stays flagged Running,` `/// so it never fires and Start() on it is a no-op until something Stops it (D16, see the header).` |
| `/// Call it BEFORE scheduling anything the test intends to fire.` | `/// Call it BEFORE scheduling anything, or constructing anything that starts a timer, that the` `/// test intends to fire.` |

**The header** gains two paragraphs after the existing D16 clock paragraph. It had no line on this subject, so nothing
was removed:

> WHAT ARM DOES TO A TIMER ALREADY RUNNING (D16): it drops it from the wheel but leaves it flagged Running. Timer.Init
> swaps in empty rings and never touches the flag (Projects/Server/Timer/Timer.TimerWheel.cs:43-52), and Start()
> returns at once while Running (Timer.cs:108), so the timer never fires and a Start() on it does nothing. Only a Stop()
> first clears the flag (Timer.cs:145, 160). So an object built before Arm() [...] can silently lose that timer, unless
> its own code happens to Stop it first. Create anything with a timer AFTER Arm().
>
> The host differs from the shard in one more way that is not about time: it has no tile data (D27) [...]
> TestHostTileData.cs pins that, and TestTileRows.cs is how a fact gets real rows for its own duration.

The citations are my own reads of pinned: `Timer.TimerWheel.cs:43-52` (`Init`), `Timer.cs:108` (`if (Running) return`),
`:145` (`Stop`'s guard) and `:160` (`InternalStop` clears the flag).

**One refinement of `gate-integrity.md` A.5.** It says such a timer "will never fire or restart". "Never fire" is true.
"Never restart" is true only of `Start()`: a `Stop()` clears the flag, and then `Start()` works. The header says that.
I also left out A.5's "a stale `Stop()` cannot corrupt the new wheel". Reading `InternalStop` and `Detach`, I think it
is right, but the rule does not need it and I had not proved it.

**For completeness, the D16 clock half was corrected before this task,** in `7dfe7d1` on 2026-09-26. The lines it took
out were the false ones the brief means:

| Old (before `7dfe7d1`) | Now |
|---|---|
| `/// The clock the test host starts from. [...] Arm pins it here` `/// once, and it only ever moves forward afterwards.` | `/// The floor Arm raises the clock to. [...] It is not a process-wide base: CreateTestNetState sets Core._now to` `/// the wall clock, which is later than this, and Arm then leaves it there (see the header).` |
| `/// Takes control of the clock for the current test: pins Core.Now to <see cref="Epoch"/> the` `/// first time it is called in a process, and [...]` | `/// Takes control of the clock for the current test: raises Core.Now to <see cref="Epoch"/> if` `/// it is below it (nothing has set it yet), and [...]` |

I checked the cited line, pinned `Server.Tests/Helpers/PacketTestUtilities.cs:62`: it is `Core._now = DateTime.UtcNow;`.

### `notes/port-recipe.md`, section "Writing a shard test fact that reads hit points, the clock, a worn item, or a gump"

| Old | New |
|---|---|
| `## Writing a shard test fact that reads hit points, the clock, or a gump` | `## Writing a shard test fact that reads hit points, the clock, a worn item, or a gump` |
| `date or the time of day. Create anything with a timer after `Arm()`, not before.` | `...**Create anything with a timer after `Arm()`, not before.** `Arm()` empties the timer wheel but leaves every timer that was on it flagged `Running`, and `Start()` returns at once while `Running` (pinned `Timer.cs:108`), so a mobile, creature or item built before `Arm()` holds a timer that never fires and that a `Start()` cannot revive; only a `Stop()` first clears the flag (D16).` |

Added, with no old line:

- A paragraph saying D15, D16 and D27 are one fact about the host. It records that D15 and D27 each have a guard fact
  and **D16 has none**; I first wrote that all three had one, which is false, and corrected it before handing back.
- A D27 paragraph ("the host has no tile data"), with four rules: open a `TestTileRows.Seed` scope naming the rows
  before building the items; add a missing row to `TileRows` from `tiledata.mul`, never read the file at test time; do
  not set a layer by hand, which hid D28; and never set `MaxItemValue` in the fixture.

### The new helper's own header (`Route/TestTileRows.cs`)

This is new text, with no old line to set beside it. It gives the D27 mechanism with pinned citations, the fact that
the mask is the part people miss, when to use the scope and what a call site looks like, "open it before building the
items", the three rules, the parallel-execution answer (§5), and how to add a row.

### Two more headers that had gone stale, so both now point at the scope

`Route/TestHostTileData.cs` (the D27 guard):

| Old | New |
|---|---|
| `live server, not Arms, and the Bestial fact wears it on Arms by hand (notes/d27-worn-item-facts.md).` | `InnerTorso unnoticed while the Bestial fact wore it on Arms by hand (D28, fixed).` |
| `its own duration, restoring both. GargoyleStartingClothesVerification is the one fact that` `does; its header has the row values and where they came from.` | `A fact that needs real layers or weights opens a TestTileRows.Seed scope naming the rows it` `needs (TestTileRows.cs): it seeds them AND raises MaxItemValue for the fact's duration, and restores both.` |
| `at every fact that equips, weighs or reads a layer, and retire the reflection in` `GargoyleStartingClothesVerification.` | `at every fact that equips, weighs or reads a layer, and retire TestTileRows and its callers.` |
| `goes red, on purpose. That change alters what 148 other facts are measuring` | `goes red, on purpose. That change alters what every other fact is measuring` (the count had gone stale twice already) |

`GargoyleStartingClothesVerification.cs`: its eight-line explanation of the reflection and the row values became four
lines pointing at `TestTileRows.cs`. The values now live there, with the same provenance. D28's fact comment, "Copied
from GargoyleStartingClothesVerification (D26) rather than shared [...] whether to extract it is an open decision",
became a pointer to the scope, since the decision is made.

---

## 4. D15's guard fact existed

**It exists, and it has since 2026-09-26:**
`ShardTestClockVerification.ADamagedMobileRegainsExactlyOneHitPerWheelTick`, now at
`server/tests/Route/ShardTestClock.cs:277`. It was added in `7dfe7d1` ("regen guard fact"). It damages a
`PlayerMobile` by 20, asserts that the whole hit is visible on the tick it lands, and then asserts that exactly one hit
is back after one 8 ms `Advance`. It passed in the green run above. The header rule Q-060 asked for is at `:42-55`,
and `port-recipe.md` has carried the same rule since the same day (`4669945`). I did not write a second one.

**What no guard pins is D16.** Neither `Arm()`'s effect on a running timer nor `CreateTestNetState` moving the clock to
wall time is asserted anywhere. They are now written down in both places, but nothing goes red if either changes. A
guard would be small, for example "a timer started before `Arm()` does not fire across an `Advance`, and `Running` is
still true". It was not in this brief, so I did not add one. It is Chase's call.

---

## 5. Parallel execution

**It is not safe under parallel execution, and it does not need to be.** `TileData.ItemTable` and `MaxItemValue` are
static and process-wide. A fact running at the same time as a seeded one would see the raised mask and the seeded rows,
and red C shows how quietly that would pass.

It cannot happen here, for a reason that can be checked, and the check is stronger than D27 §5 stated:

- **All 29 shard test classes** carry `[Collection("Sequential UOContent Tests")]`. That is 28 before this task, plus
  `TestTileRowsVerification`. I counted with `grep -A1` on the attribute followed by a `class` line. The raw attribute
  count is 30, because my header quotes the attribute once in a comment. Every file with a `[Fact]` or `[Theory]` has
  the attribute (`grep -L` finds none without it).
- **Pinned defines that collection with `DisableParallelization = true`** (`UOContent.Tests/Fixtures/UOContentFixture.cs:10`).
  D27 §5 said the facts in the collection run in sequence. They also never run beside **any other** collection.
- `build.sh` runs only `FullyQualifiedName~ShatteredLegacy.Tests` (`build.sh:72`).

The scope's header says this, and names the condition that breaks it: a shard test class leaving the collection. The
same condition already holds up `ShardTestClock` and every fact that moves `Core.Now`, so nothing new was engineered
around it. The header also says scopes must be disposed in reverse order, which `using var` does.

---

## 6. What the brief restated wrongly

1. **§3: "the `ShardTestClock` header, which currently states two things that are false (D16)".** It did not. The false
   statements (Epoch "pins it here once", "the first time it is called in a process") were corrected on 2026-09-26 in
   `7dfe7d1`, and a D16 clock paragraph was added to the header then. D16's other half, `Arm()` and `Running`, was
   never stated falsely. It was **omitted**, which is exactly what the bug-list D16 row says ("two `ShardTestClock`
   truths its own header **does not state**"). The one line that came close to misleading was `Arm()`'s
   "dropping timers left behind", and that is what I changed. D16's "fix" column ("fix the header when something next
   touches that file") was half done by that commit, and the D16 row was never updated to say so.
2. **§3: "Check D15's guard fact exists. [...] If it was never written, write it."** It was written, in the same commit.
   §4.
3. **§3: `notes/port-recipe.md` as a place to put all three.** Two of the three were already there (D15, and D16's
   clock half, since `4669945`). What it lacked was D27 and the reason behind "create timers after `Arm()`".
4. **§2, constraint 2: "You measured the side effects for one fact."** D27 §5 did not measure them. It **deduced**
   them from `Item.cs`: that layers would not improve and that weights would become 1. Red C above is the first time
   they were measured, and only for the guard's three readings. The measurement agrees with the deduction.
5. **§3's D27 line: "every `BaseArmor` and `BaseWeapon` is `Layer.Invalid`."** It holds only for those that do not set
   their own layer. `Bow` and most two-handers do, and so do `GargishEarrings`, `GargishNecklace` and, since D28,
   `BestialArms`. Red A shows this directly: `BestialArms` read `Arms` with no rows at all. D27 §1 has the qualified
   version. This matters for the next fact author, because an item that sets its own layer needs no seed for its layer.
6. **§1 is right.** The trigger quoted is D27 §5's wording. The two facts, their `finally` blocks and the identical
   reflection are all as described, and D28 §4 had already named its fact as the one that fired the trigger. The
   "150 tests" figure in §4 was right too: 150 before this task, counted.

---

## Not done, and why

- **`tools/progress.py` was not run.** It rewrites `README.md` and `tools/progress.json`, both already modified in the
  working tree, while P2 and P3 are running. It is better run once, by whoever commits.
- **`docs/` was not touched.** Candidates for promotion: the D16 row's status (the header is now complete, but there is
  no guard); the D27 row, where the mechanism now exists and the "hand-set layer is why this went unnoticed" sentence is
  superseded by D27 §3.2; and the fact that `DisableParallelization = true` makes the parallel argument stronger.
- **Commits in `D:\ShatteredLegacy`.** The tree also holds D27's untracked guard and D28's two files, all uncommitted
  before this task. My changes build on them: the D28 fact I moved onto the scope exists only in the working tree. So
  they need to go in together, or D27 and D28 first.

## Method and scratch

In this session's scratchpad, not committed: `rows_p1.py` (the independent row re-read), `red-a.log`, `red-b.log`,
`red-c.log`, `green.log`, and `final/` (the copies each red run was restored from). No container was started, stopped
or restarted. `sl-modernuo-test` was not running before this task and was not touched. `D:\UO\ServUO-pub57` and
`D:\UO\ModernUO-pinned` were only read. P2's and P3's files were not opened for writing. The green run rebuilt
`sl-uo-builder:latest` and `sl-modernuo:latest`, and no running container uses either.
