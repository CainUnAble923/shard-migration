# cc-P31: cleanup of the League Registrar's field office decor

Date: 2026-10-02. Agent: Claude Code. Pinned ModernUO `7c9215d97`. Built in `D:\ShatteredLegacy`, **not committed**.
No world was changed: nothing placed, moved or removed on live or test; no shard deployed, restarted or recreated.
`sl-modernuo:latest` was not moved (`d353a3fb86f2` before and after). Image: `sl-modernuo:cc-p31-office` = `1435530e239f`.

**Gate before starting.** `git --no-optional-locks status` in `D:\ShatteredLegacy` at `56cae9d`: nothing uncommitted under
`server\customizations` or `server\tests`. Uncommitted were only the overseer's `design\registrar-office\` changes
(`layout.json`, `registrar.py`, two PNGs, and the new `cleanup\` folder), which this task reads and does not edit.
P19 is committed (`f49e693`, 2026-10-01 05:02). I could not verify that no other prompt was working in
`D:\ShatteredLegacy` beyond the tree; nothing changed under me during the run.

**Numbering:** no clash found. `D:\UO\cc-prompts` holds one file each for P30, P31 and P32, and no other P31 under `notes\`.

Tools and outputs: `notes/cc-P31-tools/` (README there). `gen_office_layout.py` and `breaks.py` WRITE to `D:\ShatteredLegacy`.

> **Headlines**
>
> 1. **Built:** the layout regenerated from the 14-component design (outside 3, office 8, quarters 3, counted from the
>    file); only 0x0BCF is named now; `[ClusterFSeedRegistrarOffice replace` and `replace dryrun`. **410 tests pass**
>    (2 new facts, 3 updated). Every fact touched was watched red on a break of its own (section 4).
> 2. **Part A: no stop.** The server surface z at 3461,2602 is **18**. The walk tiles are still clear.
> 3. **Why a plain re-run does not update a P19 world:** an addon builds its components once, in its constructor, and
>    a saved one loads back with the components it was saved with; the seeder skips any of the three types already on
>    Trammel. So the 18 stay until `replace` swaps them (section 1.3).
> 4. **The brief's change table checks out against the files.** Diffing `cleanup\layout_p19.json` against `layout.json`
>    gives exactly the five P19-only components the brief lists, and the one new candelabra position. Fact 6 asserts
>    this from the two files. `layout_p19.json`'s SHA-256 equals the `DesignSha256` P19 shipped
>    (`a68ea589...`), so the fixture is exactly what P19 built from.
> 5. **`[ShardCommand]` has no field for a second mode.** I put `replace` and `replace dryrun` in `Summary`, `Usage`
>    and `Description`, which the console already shows; `Rerun`, `DryRun` and the rest still describe the default form.
>    No `scripts\` edit (section 3.5).

---

## 1. Part A: facts

### 1.1 Surface z at 3461,2602 (A1)

Same method as P19: a port of pinned **`Map.GetTopSurfaceZ(Point3D)`** (`Projects/Server/Maps/Map.cs:491-565`) over
the server's own map files, in `notes/cc-P31-tools/office_z.py` (P19's tool, unchanged, reading the new `layout.json`).
Output `office_z.out.txt`:

```
office,0x0B26,candelabra,3461,2602,18,13,13,18,0,0x05A7@41+3[-](thatch roof) 0x049C@18+0[surf](grey slate tile) 0x07A3@13+10[surf|bridge](stone)
```

**Server z 18 = layout z 18.** The surface is the slate floor static 0x049C at 18 (over the stone bridge static at
13+10, half height 5), as for every other floor prop in the house. No static furniture on the tile; the window 0x000F
is on 3462,2602, the wall beside it. The other 13 components are unchanged and still match as in P19 section 1.1
(13 exact, the hourglass +3 on the books by design; same rows in the output).

### 1.2 Walk tiles (A2)

The walkability table at the end of `office_z.out.txt` (P19's `Map.CanSpawnMobile` port, with every component of the
**new** layout on its tile) is unchanged: all eleven P19 section 1.2 tiles are standable (14 outside the front door,
18 for the other ten) with no component on any of them. The candelabra moved **away** from the walkway (3461,2600) to
3461,2602, which is not one of those tiles; the nearest, 3460,2602 (SE of the Registrar, where a visitor stands), is
west of it and clear. Fact 3 still pins no component on a door tile, a door swing tile or the Registrar's tile.

### 1.3 How the seeder decides an addon exists, and why a re-run does not update a P19 world (A3)

- `[ClusterFSeedRegistrarOffice` calls the shared placer `ClusterFMineCampSeeder.SeedAddons`
  (`ClusterFMineCampSeeder.cs:125-167`). For each of the three types it calls `FindTent(type)` (`:169-181`), which
  returns any non-deleted item whose **exact runtime type** is that type and whose map is Trammel. If one exists, it
  prints "already on the world ... nothing placed" and moves to the next type. It never looks at the components.
- The components are made in the addon's constructor: `RegistrarOfficeAddon()` calls
  `ClusterFMineCampSeeder.AddComponents(this, ClusterFRegistrarOfficeLayout.Office)`, i.e. from whatever table the
  build had **when the addon was constructed**.
- A saved addon is not reconstructed on load. Pinned `BaseAddon` stores its components as a serialized list
  (`[SerializableField(0)] List<AddonComponent> _components`, `Projects/UOContent/Items/Addons/BaseAddon.cs:39-40`) and
  `Deserialize` reads that list back (`:278-286`); each `AddonComponent` is its own saved item with its own item id and
  offset (`AddonComponent.cs:106-112`). The `[Constructible]` constructor does not run.
- **So on a world that has P19's version**, after deploying this build: the three types are on Trammel, so the plain
  command places nothing ("placed 0 of 3"), and the 18 P19 components stay exactly as saved: north signpost and sign,
  bulletin board, globe, candelabra at 3461,2600. Fact 6 asserts this before running `replace`. Hence `replace`.

---

## 2. What changed, file by file

All in `D:\ShatteredLegacy\server`. ASCII in every file touched (checked byte by byte). No pinned file, patch,
`Distribution/Data`, `design/`, `docker/`, `scripts/` or `docs/` touched.

| File | What |
|---|---|
| `customizations/ClusterFRegistrarOfficeLayout.cs` (generated) | 14 components (3 / 8 / 3), new design SHA-256 `e583cb43...`. Generator path in the header now `notes/cc-P31-tools/` |
| `tests/Misc/RegistrarOfficeLayoutDesignCopy.cs` (generated) | the new `layout.json` verbatim and its hash |
| `tests/Misc/RegistrarOfficeLayoutP19Copy.cs` (new, generated) | `cleanup/layout_p19.json` verbatim and its hash: the P19-world fixture. Same route into the test container as the design copy, because the container holds nothing from `design/` |
| `customizations/ClusterFRegistrarOfficeSeeder.cs` | `SignItemIDs = [0x0BCF, 0x0BD0]` replaced by `const int SignItemID = 0x0BCF` (`:46`); command parses `replace` and `replace dryrun` (`:71-104`); `Replace(dryRun)` (`:117-146`) and `FindOfficeAddons()` (`:148-162`); header and class comments updated |
| `customizations/ClusterFMineCampSeeder.cs` | `SeedAddons` and `FindTent` take an optional `removing` set (`:127-132`, `:169-174`): addons the caller is about to delete count as gone. Null for P16 and for the plain office seed, so both behave as before; P16's facts still pass |
| `tests/Misc/RegistrarOfficeVerification.cs` | facts 1, 2, 4 updated; facts 6 and 7 new; helpers to build a P19 world |

In this repo: `notes/cc-P31-tools/`. **Re-run `notes/cc-P31-tools/gen_office_layout.py` (not P19's) after any change to
`layout.json`**; P19's would still work for the two files it writes but would not refresh the P19 fixture.

---

## 3. Part B

### 3.1 Regenerated layout (B1)

`gen_office_layout.py` output: `layout.json components: 14 {'outside': 3, 'office': 8, 'quarters': 3}`,
`layout_p19.json components: 18 {'outside': 5, 'office': 10, 'quarters': 3}`. The two files differ by exactly the
brief's table (diffed by script, not read off the brief): removed 0x0B98 and 0x0BD0 at 3460,2595,15, 0x1E5F at
3458,2598,18, 0x1047 at 3461,2598,18, 0x0B26 at 3461,2600,18; added 0x0B26 at 3461,2602,18. Each area's first component
(the addon's origin) is unchanged, so `replace` places the new addons where the old ones stood.

### 3.2 Sign naming (B2)

**Removed**, not left harmless. With 0x0BD0 out of the table nothing new could carry it, so the naming code now names
only `SignItemID = 0x0BCF`. This does not affect saved P19 addons: a component's `Name` is saved with it (P19 section
3.3) and nothing reads the id list after construction; `replace` deletes the old sign anyway.

### 3.3 `replace` (B3)

`ClusterFRegistrarOfficeSeeder.Replace(dryRun)`:

1. `FindOfficeAddons()`: every non-deleted item on Trammel that is a `BaseAddon` whose exact type is one of the three
   (`RegistrarOfficeOutsideAddon`, `RegistrarOfficeAddon`, `RegistrarQuartersAddon`). All copies, if a world somehow
   has more than one. Nothing else is a candidate, whatever its item id or tile.
2. One line per addon: type, serial, location, map, component count ("would delete" or "deleted"). Then a total.
3. Real run: `Delete()` on each addon. Pinned `BaseAddon.OnAfterDelete` deletes its own components
   (`BaseAddon.cs:267-276`), and only those.
4. Places the current layout through the same placer as the plain command, passing the found addons as `removing`, so
   a dry run reports the placement as if the deletions had happened ("would place ... 3 of 3"), including any foreign
   item on the new tiles (listed, never touched, as before).

Dry run output on the P19 fixture. Not seen in a log (passing tests' output is not printed); these are the exact
strings fact 7 asserts, with the counts and origins from the two layout files, serials elided:

```
RegistrarOfficeOutsideAddon 0x........: would delete at (3458, 2595, 15) (Trammel), 5 components.
RegistrarOfficeAddon 0x........: would delete at (3458, 2600, 24) (Trammel), 10 components.
RegistrarQuartersAddon 0x........: would delete at (3456, 2597, 18) (Trammel), 3 components.
ClusterF registrar office replace: would delete 3 addons (18 components).
RegistrarOfficeOutsideAddon: would place at (3458, 2595, 15) (Trammel), 3 components.
RegistrarOfficeAddon: would place at (3458, 2600, 24) (Trammel), 8 components.
RegistrarQuartersAddon: would place at (3456, 2597, 18) (Trammel), 3 components.
ClusterF registrar office dry run: would place 3 of 3 addons.
```

**Twice is once.** A second `replace` deletes the three it placed (14 components) and places three identical ones:
same types, item ids, tiles, z and names; only the serials differ. Fact 6 compares the two states.

On a world with **no** office yet, `replace` deletes nothing ("0 addons (0 components)") and places all three, the same
as the plain command.

### 3.4 Plain command (B4)

Unchanged: `[ClusterFSeedRegistrarOffice` and `status|dryrun` call `Seed`, which skips any type already on Trammel.
Fact 2 (seed twice, places once) and fact 6 (plain seed on a P19 world places 0 of 3) pin it.

### 3.5 `[ShardCommand]` (B5)

`ShardCommandAttribute` (`server/customizations/ShardCommandAttribute.cs`) has one `Rerun`, one `DryRun` word and one
`Summary` per command; **it has no field for a second mode** with its own re-run behaviour or dry run. So, per the
brief, I stopped there:

- `Rerun = CommandRerun.Skips` and `DryRun = "dryrun"` are kept: the attribute documents `Rerun` as the default form's
  behaviour (`ShardCommandAttribute.cs`, the `CommandRerun` comment), and the plain form still skips.
- `Summary` now ends "'replace' (dry run: 'replace dryrun') swaps an older office decor for the current one, deleting
  only its own three addons." `Usage` is `ClusterFSeedRegistrarOffice [status|dryrun|replace [dryrun]]`, and
  `Description` says the same. The console reads `Usage` and `Summary` from source (`Shard-Console.ps1:1336-1348`,
  `:1397-1398`) and still finds `dryrun` as a word of `Usage`; `CommandDeclarationVerification` passes.
- **Not done (scope):** the console's dry-run button still runs `[ClusterFSeedRegistrarOffice dryrun`, not
  `replace dryrun`. Giving it a second button needs an attribute field and a `scripts\` change; flagged for the overseer.

---

## 4. Tests and red/green runs

`server/tests/Misc/RegistrarOfficeVerification.cs`. Brief test numbers in brackets; facts 1 to 5 are P19's numbering,
so the brief's new tests 5 and 6 are facts 6 and 7.

| # | Fact | What it pins |
|---|---|---|
| 1 [1] | `TheLoadedLayoutIsTheDesignFile` | table equals the new `layout.json` (hash checked) in order; 14 = 3 + 8 + 3, counted |
| 2 [2] | `SeedingTwicePlacesTheDecorOnce` | dry run places nothing; two runs place 3 addons once, 14 components at their design tiles |
| 3 [3] | `NoComponentSitsOnADoorItsSwingOrTheRegistrarTile` | unchanged from P19; runs against the new table |
| 4 [4] | `TheSignReportsTheLeagueName` (renamed from `BothSigns...`) | exactly one sign, 0x0BCF at 3463,2597,13, named and with that property-list header; one "wooden sign" in the table; nothing else outside named |
| 5 | `TheRegistrarFacesHerDesk...` | unchanged from P19 |
| 6 [5] | `ReplaceSwapsAP19OfficeForTheCurrentLayoutAndNothingElse` | builds a P19 world from the fixture (the three real types, P19 components, both signs named); P19-only set computed from the two files equals the brief's five; plain seed places 0 of 3 and leaves 18; places unrelated things (Static 0x1E5F on the old board tile, Static 0x0B98 on the old signpost tile, a DarkWoodDoor on the front door tile, an Item beside the candelabra); `replace`: P19 addons and all their components deleted, exactly the 14 current components in the house box (any AddonComponent, any owner), none of the five, one named sign; second `replace` gives the same state; every unrelated thing still there, same tile |
| 7 [6] | `ReplaceDryRunChangesNothing` | on a P19 world: `World.Items.Count` and every addon/component (serial, id, tile, name) unchanged; P19 addons not deleted; one "would delete" line per addon with its serial, location and count; "would place" line per type with the new counts |

All through `docker/uo/build.sh` (red runs with `--tests-only`). Breaks by `notes/cc-P31-tools/breaks.py` on byte copies;
restored, SHA-256 checked equal, `grep -rl P31-BREAK server` empty before the final build.

| Run | Breaks | Result |
|---|---|---|
| check | none | 410 passed (all 7 office facts) |
| red A | layout **not regenerated** (P19's generated table and design copy from git HEAD); `replace dryrun` deletes | **405 passed, 5 failed**: fact 1 (14 expected, 18); fact 2 (14 expected, 18); fact 4 (`Assert.Single`: 2 signs); fact 6 (P19-only set empty, the brief's five expected: the table is P19's); fact 7 (`World.Items.Count` 817 expected, 796: 21 = 3 addons + 18 components deleted by the dry run) |
| red B | candelabra on the Registrar's tile 3459,2601 in the office area table; real `replace` deletes nothing | **407 passed, 3 failed**: fact 3 ("0x0B26 at (3459, 2601, 18) is on the Registrar's tile"); fact 1, expected (table differs at the candelabra); fact 6 (3 of 3 P19 addons not deleted) |
| red C | real `replace` also deletes every loose item in the house box | **409 passed, 1 failed**: fact 6 ("Static 0x1E5F at (3458, 2598, 18) was deleted") |
| final | none, restored and hash-checked | `docker/uo/build.sh -t sl-modernuo:cc-p31-office`: **410 passed**, "Built sl-modernuo:cc-p31-office with patches applied and 410 shard test(s) passing." Image `1435530e239f`; `latest` still `d353a3fb86f2` |

Not measured: a before-count on HEAD. 408 is 410 minus my two new facts, not a separate run (P19 recorded 333; other
prompts since have added the rest). Not watched red separately: fact 6's "no P19-only component remains" against a break
that leaves just one of the five (red A and B fail fact 6 earlier in the method).

---

## 5. Checklist for Chase

1. **Commit** with `D:\UO\Commit-ShardWork.ps1`. In `D:\ShatteredLegacy`: the six server files in section 2. The
   overseer's uncommitted `design\registrar-office\` changes (including `cleanup\`) are in the same tree and should go
   in the same commit: the generated files' hashes are of those exact `layout.json` and `layout_p19.json`. Here:
   this note and `notes/cc-P31-tools/`.
2. **Rebuild the test shard** from the console ("Rebuild through the gates"); the gate should say 410 passed. That
   retags `sl-modernuo:latest`; `sl-modernuo:cc-p31-office` is this task's image.
3. **On the test shard**, as Administrator:
   1. `[ClusterFSeedRegistrarOffice replace dryrun`: should list three "would delete" lines with **5, 10 and 3
      components** (P19's office), "would delete 3 addons (18 components)", then "would place" with **3, 8 and 3**.
      If it says 0 addons, the test world never had P19's office; `replace` then just places it.
   2. `[ClusterFSeedRegistrarOffice replace`: same lines with "deleted" and "placed 3 of 3".
   3. Check by eye: no signpost or sign on the north (back) wall; one sign on the east wall, single-click shows
      "League of Extraordinary Citizens"; no bulletin board, no globe; the candelabra in the SE corner (3461,2602),
      not in the walkway between the desk and where visitors stand.
4. **Screenshot the office** for the overseer: inside (`[go 3460 2600 18`), and the east wall with its sign from the
   road (east of 3463,2597).
5. **Live-world commands** (Administrator, in game, after the test shard looks right). P19 section 6 recorded that
   live had not been seeded as of its 2026-09-29 save copy; the dry run tells you which case you are in.

   | Command | What it does | Re-run |
   |---|---|---|
   | `[ClusterFSeedRegistrarOffice replace dryrun` | lists the office addons it would delete (serial, location, component count) and what it would place; changes nothing | safe, any number of times |
   | `[ClusterFSeedRegistrarOffice replace` | deletes the three office addons on Trammel (and only their own components), then places the current 14-component office. Touches no other item, NPC, door or static. On a world with no office it only places | safe: a second run ends in the same state (new serials, same props); it never duplicates |
   | `[ClusterFSeedRegistrarOffice dryrun` | lists what the plain form would place; changes nothing | safe |
   | `[ClusterFSeedRegistrarOffice` | plain form: places any of the three addons not already on Trammel. **Does not update a P19 office** (section 1.3) | safe: skips what is there, never duplicates |

   Use `replace` on live whether or not P19's office is there; the plain form is only for a world that has none.

Open, unverified:
- Nothing was run in a client: the look of the cleaned office, and the sign reading from the road.
- Whether live currently has P19's office (the dry run answers it).
- The console's World setup tab offers only the plain dry run as a button (section 3.5).
