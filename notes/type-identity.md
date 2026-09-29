# Type identity: D34, the sweep, and D35

2026-09-29. Tests: `D:\ShatteredLegacy\server\tests\TypeIdentity\TypeIdentityVerification.cs` (10 facts).
Type list: `notes/type-identity-types.txt`. Nothing in `docs/` was edited.

## 0. The answers

1. **D34 does not fire in this build. No rename was made.** `GargoyleAlchemist` and pinned `Glassblower`'s alias do
   share a bucket in the save path's map, `[Server.Mobiles.GargoyleAlchemist, Server.Mobiles.Glassblower]`, and **ours
   is first**. So every lookup returns ours, the save round trip returns ours, and 578 bytes written are 578 read.
   `GargoyleStoneCrafter` is the same: ours wins on every map, and 565 of 565 bytes round-trip.
2. **But "first" is a compiler artifact, not a property of the source.** The order is neither directory order nor
   path order (§1.3). **So the answer is gated, not settled.** If a future build flips it, `build.sh` now fails with
   the bucket printed.
3. **The sweep found nothing else of ours.** **8,508 types** in `Server.dll` and `UOContent.dll` were looked up by their
   own full name, **1,160 of them ours**, with zero failures on the save map and zero on the case-insensitive map.
   **4,281 spawnable types** were looked up by short name the way spawners do, **900 of them ours**, again zero
   failures. It turned up one upstream case, pinned-only and not gated: `Blight` (§2.4).
4. **D35: both spellings are distinct types and neither shadows the other.** Measured, not read (§3). **The
   misspelling is ModernUO's, not ServUO's.** I recommend dropping ours (§3.4). Nothing was deleted.
5. **The brief's premise that the world is being regenerated conflicts with the repo, and the live save shows it
   matters.** `Saves/SerializedTypes.db` names `Server.Mobiles.GargoyleAlchemist`: **the live world already holds at
   least one** (§1.5). A rename would orphan them. It happened not to be needed, but the rename instruction rested
   on that premise.

---

## 1. Task A: D34

### 1.1 The signature, read first

`public static Type FindTypeByFullName(string name, bool ignoreCase = true)` (pinned `Server/AssemblyHandler.cs:186`).
**The second argument is `ignoreCase`.** The brief's `false` therefore means *case-sensitive*, which happens to be the
right map to probe, because it is the one saves use:

| Path | Lookup | Map | Pinned citation |
|---|---|---|---|
| save / load | `FindTypeByHash(GetTypeHash(type.FullName))` | full name, case-**sensitive** | written `MemoryMapFileWriter.cs:246`, resolved `GenericEntityPersistence.cs:309` |
| type refs inside entity data | same pair | same | `BufferWriter.cs:287`, `BufferReader.cs:150` |
| spawners, `[add`, spawner gump, `ImportSpawners` | `FindTypeByName(name)` | **short** name, case-**in**sensitive | `BaseSpawner.cs:1126`, `ImportSpawnersCommand.cs:216` |
| quests, BODs, talismans, feature flags | `FindTypeByFullName(name)` | full name, case-insensitive | `QuestSerializer.cs:72`, `LargeBulkEntry.cs:28`, `TalismanAttribute.cs:49` |

Consequence for `GargoyleStoneCrafter`: pinned's alias is `GargoyleStonecrafter`, a different string, so it
**cannot** collide on the save map at all. It can collide on the other two, where it lands in the same bucket. The
probe covers all four lookups for both vendors.

### 1.2 What it returned

```
full, case-sensitive:   Server.Mobiles.GargoyleAlchemist
full, case-insensitive: Server.Mobiles.GargoyleAlchemist
by hash (save path):    Server.Mobiles.GargoyleAlchemist
short name (spawners):  Server.Mobiles.GargoyleAlchemist
bucket: [Server.Mobiles.GargoyleAlchemist, Server.Mobiles.Glassblower]

saved Server.Mobiles.GargoyleAlchemist, loaded as Server.Mobiles.GargoyleAlchemist
entity bytes written 578, read 578
saved Server.Mobiles.GargoyleStoneCrafter, loaded as Server.Mobiles.GargoyleStoneCrafter
entity bytes written 565, read 565
```

**The round trip is not a `World.Save`.** That cannot be driven in the test host, because it posts to a loop nothing
pumps. The fact performs the two steps of a save that involve the type, using the real writer, reader and lookup:

1. It writes the type as the index does: flag 2 plus the hash.
2. It writes the entity's bytes.

Then it does what `GenericEntityPersistence` does on load: resolve with `FindTypeByHash`, take the `(Serial)`
constructor, `Deserialize`, and compare the byte count as `InternalDeserialize` does. Load has one type-resolution
call (`:309`), and this exercises it. What it does not exercise is the file I/O and the `SerializedTypes.db` fallback,
which only runs when the hash lookup returns null.

### 1.3 Why it is ours, and why that is not a guarantee

The bucket is a `HashSet` filled in `Assembly.GetTypes()` order (`AssemblyHandler.cs:251-263`), which is TypeDef order.
Measured in the built `UOContent.dll`: **`GargoyleAlchemist` is TypeDef 746 and `Glassblower` 1,460**. For the other
pair, `GargoyleStoneCrafter` is 775 and `StoneCrafter` 1,495.

That order is **not** the ordinal order of source paths: they diverge at the first entry, where the first TypeDef comes
from `Regions/NoTravelSpellsAllowedRegion.cs`. It is **not** raw directory order either: `ls -f` lists `Mobiles`
before `Misc`, and ours is in `Misc/`. It is whatever order the SDK and Roslyn hand the files over in, and **no source
file states it.** I did not chase the exact rule; the gate makes it unnecessary.

**The test measured the shipped binary.** `UOContent.dll` in the test output, in `/build/modernuo/Distribution` and in
`/modernuo/Distribution` have the same sha256, `5a5ba232…5d86`.

### 1.4 Order in the test host versus production

The fixture loads `["Server.dll", "UOContent.dll"]`. Production loads `["UOContent.dll"]` (`Data/assemblies.json`) and
searches `Core.Assembly` last. **Neither D34 nor any bucket holding a type of ours can be affected**, because both
sides of every such bucket are in `UOContent.dll`. The sweep checks each assembly's own cache for exactly that reason.
Eleven full names exist in both assemblies. All are compiler plumbing: `ThisAssembly`, and ten
`<PrivateImplementationDetails>` nested types. None is an entity.

### 1.5 The rename, and why it was right not to need one

The probe passed, so per the brief nothing was renamed. But the brief's cost model for a rename does not hold here,
and it should be recorded before anyone reaches for one:

| Type table | `GargoyleAlchemist` | `GargoyleStoneCrafter` |
|---|---|---|
| `server/lib/uo/modernuo/Saves` (live) | **present** | absent |
| `Saves-test` | present | present |
| `Saves-test.aside-20260929-112645` | present | present |
| `Saves-test.aside-20260929-112812` | present | absent |
| `Backups/Automatic/2026-09-29-08-55-00` | present | absent |

A type in `SerializedTypes.db` means at least one instance was written in that save (`WriteSnapshot` adds each
entity's type to the set, `GenericEntityPersistence.cs:66-123`). So **the live world holds `GargoyleAlchemist` NPCs
today.** A rename would reach the load's "Bad type ... Delete all of those types? (y/n)" prompt
(`GenericEntityPersistence.cs:159-178`). "Acceptable because the world is being regenerated" is contradicted by
AGENTS.md rule 7 and `docs/direction-decision.md:38`. `notes/reachability-audit.md` §7.3 already flagged this and it
is still unresolved.

**If the gate ever goes red on this bucket**, the options are these. None of them is free, which is the reason to
decide now rather than then:

- **(a) Rename ours with no alias**, as the brief says. Orphans every saved one; `ClusterFRoyalCitySeeder` re-seeds
  (its `HasAnyGargoyleVendors` check at `:259` looks only for `GargoyleAlchemist` on Ter Mur, so it would see none). Clean, if a lost vendor is acceptable.
- **(b) Rename ours and alias the old name.** This reintroduces the collision. The brief rules it out and it is right.
- **(c) A `.patch` removing the alias line from pinned's `Glassblower`.** Keeps every saved NPC and costs one line. The
  alias exists for importing RunUO or ServUO saves, which this shard never does.

**My recommendation: do nothing now.** The gate holds the current order on every build. If it ever fails, take
(c): it is the only option that loses nothing, and the gate's red is the moment to write that patch's alternatives
note, per AGENTS.md. Decision is Chase's; nothing here was changed.

---

## 2. Task B: the sweep

### 2.1 What it asserts

`EveryTypeResolvesToItselfByFullName` walks `AssemblyHandler.GetTypeCache(asm).Types`, the list the maps are built
from, for every loaded assembly. For each type it asks that assembly's own cache for the type's full name, on both
the case-sensitive and case-insensitive maps. It then calls the public `FindTypeByFullName(name, false)` and
`FindTypeByHash` on every type of ours, which is the brief's probe stated in general form.

- **A save-map miss fails** whoever owns the type.
- **A case-insensitive miss fails** only when one side is ours. Pinned-only misses are printed and not gated.

`EverySpawnableTypeResolvesToItselfByShortName` does the same through `FindTypeByName`, as `BaseSpawner` calls it. It
covers every public, concrete, non-nested `Item` or `Mobile` with a parameterless constructor. A miss fails when
either side is ours, **so it also catches a pinned creature whose spawn entry one of our types would capture.** That
is the fresh-world failure mode: `[GenerateSpawners` resolves by short name.

Compiler-generated types (`<>c`, display classes, embedded attributes) are skipped: 588 of them.

### 2.2 Which types are ours

This is read from `UOContent.pdb`, not grepped. Each type's source documents come from its methods' debug info, plus
Roslyn's type-definition-documents record for types with no method bodies. **A type counts as ours when every
non-generated document is a file `apply-patches.sh` installed from `/customizations`.** That directory is present in
the builder image the tests run in, and the fact throws if it is not.

So partial extensions of pinned types (`PlayerMobile`, `Corpse`, `BaseGuildmaster`, `Mining`) and the seven full-file
replacements count as pinned's. `TheOursClassifierKnowsOursFromPinned` pins five known answers in both directions
rather than a floor on a number.

**It went red on its first run.** It counted 347 types, not `GargoyleAlchemist`, because the serialization
generator's output lives on disk under `Projects/UOContent/obj/` and was being read as a pinned document. Fixed by
ignoring `obj/`. That fact exists for exactly that failure.

### 2.3 The count

| | All | Ours |
|---|---|---|
| Types in the classifier's set | | **1,275** |
| compiler-generated, skipped by the sweep | 588 | 115 |
| **checked by full name** | **8,508** | **1,160** |
| **checked by short name (spawnable)** | **4,281** | **900** |

The full list of the 1,275, each marked G (generated) or S (spawnable), is `notes/type-identity-types.txt`.
**1,275 = 115 G + 900 S + 260 neither**, counted in that file.

**This is not the reachability audit's "891 content types"** and should not be compared with it. The two differ in
three ways:

- Mine includes top-level ClusterF types.
- Mine requires a public parameterless constructor.
- Mine is read from the compiled assembly.

The source scan gave 1,211 declarations in customizations. It counts partial extensions of pinned types, nested
types and the replacements, and misses generated ones. I did not reconcile it type by type, because the test's
number is the one that means something.

### 2.4 Findings

- **Ours: zero.** No type of ours is shadowed on any map, and no type of ours shadows a pinned one.
- **The source scan predicted exactly the runtime's candidates:**
  - one exact alias hit (`GargoyleAlchemist`)
  - one case-only hit (`GargoyleStoneCrafter`)
  - three self-aliases of ours: `Rotworm`/`RotWorm`, `TongueOfTheBeast`, `WallOfHungryMouths`. They alias their own
    case variant and resolve to themselves.
  - 29 pinned self-aliases of the same kind.
- **Upstream, not gated: `Server.Items.Blight` is shadowed by `Server.Ethics.Evil.Blight` on the short-name map.**
  `[add Blight`, a spawner entry `Blight`, and the Add-menu line in `Distribution/Data/categorization.json` resolve
  to the Ethics power, not the ML resource. Crafting uses `typeof(Blight)` (`DefBlacksmithy.cs:362` and others) and is
  unaffected. **ModernUO's to report, not ours to fix.** No D-number proposed.

### 2.5 Watched fail

I added, temporarily, `[TypeAlias("Server.Mobiles.GargoyleAlchemist", "Server.Mobiles.Gargoylearmorer")]` on
`GargoyleVendorHelper`, which is declared ahead of both vendors in the same file, so it enters both buckets first.
`build.sh --tests-only` **went red, 171/175, "No image was built"**, with exactly the predicted lines:

```
SAVE  ours   Server.Mobiles.GargoyleAlchemist -> Server.Mobiles.GargoyleVendorHelper (ours)
CI    ours   Server.Mobiles.GargoyleAlchemist -> Server.Mobiles.GargoyleVendorHelper (ours)
CI    ours   Server.Mobiles.GargoyleArmorer -> Server.Mobiles.GargoyleVendorHelper (ours)
API   ours Server.Mobiles.GargoyleAlchemist -> byName ..GargoyleVendorHelper, byHash ..GargoyleVendorHelper
```

The two short-name failures, the D34 probe and the D34 round trip also failed. The case-only alias failed `CI` and
**not** `SAVE`, which is the distinction the gate has to draw. After that I restored the file (`cmp`-identical to
the saved original), and the full gate went **green at 177/177**.

### 2.6 What it cannot see

- A **name held only in data**: a spawn file, `categorization.json`, or `Decoration/`. When nothing declares or
  aliases the name, the name is absent rather than shadowed. That is Q-048's territory, not this one's.
- **Assemblies other than these two.** None are loaded.
- **Order in a build it did not run in.** It runs in every build, which is the point.

---

## 3. Task C: D35

### 3.1 Distinct or shadowed? Distinct, measured

`D35_BothSpellingsAreDistinctTypesAndNeitherShadowsTheOther`, both pairs:

```
Server.Items.GauntletsOfAnger -> ours;   short name -> ours
Server.Items.GuantletsOfAnger -> UOContent (pinned); short name -> pinned
LabelNumber ours 1094902, pinned 1094902
Server.Items.ShroudOfDeceit -> ours;     short name -> ours
Server.Items.ShroudOfDeciet -> UOContent (pinned); short name -> pinned
LabelNumber ours 1094914, pinned 1094914
```

No `[TypeAlias]` names any of the four spellings in pinned, ServUO or ours. **Four types, four buckets, no D34
shape.** Apart from the class name and a comment, ours and pinned's bodies are identical for both items.

### 3.2 What pinned's reachable code references: its own misspellings, everywhere

| Pinned reference | Spelling |
|---|---|
| `Mobiles/Special/Barracoon.cs:65`, champion `SharedList` | `GuantletsOfAnger` |
| `Mobiles/Special/Neira.cs:72`, champion `UniqueList` | `ShroudOfDeciet` |
| `Engines/Treasures of Tokuno/BasePigmentsOfTokuno.cs:37, :52`, dyeable replicas | both misspelt |
| `Distribution/Data/categorization.json:2349, :2419`, Add menu | both misspelt |
| `Migrations/Server.Items.GuantletsOfAnger.v0.json`, `...ShroudOfDeciet.v0.json` | both misspelt |

Our correctly spelt types are referenced by nothing in either tree.

### 3.3 Whose misspelling? ModernUO's

| Tree | Gauntlets: file / class | Shroud: file / class |
|---|---|---|
| ServUO pub57 | `GauntletsOfAnger.cs` / `GauntletsOfAnger` | **`ShroudOfDeciet.cs`** / `ShroudOfDeceit` |
| pinned ModernUO | `GauntletsOfAnger.cs` / **`GuantletsOfAnger`** | `ShroudOfDeceit.cs` / **`ShroudOfDeciet`** |
| ours | `GauntletsOfAnger.cs` / `GauntletsOfAnger` | `ShroudOfDeciet.cs` / `ShroudOfDeceit` (ServUO's file name kept) |

ServUO spells both **classes** correctly. Its only error is one file name, and a file name has no runtime meaning.
ServUO references its own correct names (`Barracoon.cs:87`, `Neira.cs:84`, `CleanUpBritanniaData.cs:628, :631`).
Where the misspelling came from before ModernUO I did not check.

**The fidelity rule has no opinion here.** It governs OSI behaviour players can see. Players see cliloc 1094902 and
1094914 either way, "[Replica]" included. A class name is visible only to staff typing `[add`.

### 3.4 Recommendation: drop ours, both of them. Chase decides

1. **Pinned's are the real ones.** Champion spawns, pigments, the Add menu and the serialization schema all name
   them, and ours duplicate them in every value.
2. **Ours are not merely dormant.** `[add GauntletsOfAnger` gives a staffer ours, and ours is **not** in pinned's
   `m_Replicas`, so Pigments of Tokuno cannot dye it. That is a real behavioural difference: the only way to hand out
   the correctly named item is to hand out the one that behaves wrong.
3. **The cost is nearly zero today.** Neither type is in any save table checked in §1.5. `D25` says live holds no CC9
   type, and these are CC9 batch 5. A removal is still a save-compatibility change, so re-check the tables on the
   day.
4. **Not the alternative, renaming pinned's to the correct spelling.** That would be a patch against pinned plus a
   `[TypeAlias]` for the old name, to fix a spelling no player sees.

If kept instead, backlog tools should count them as twins. The reachability audit's twin sweep already does.

---

## 4. Where the brief was wrong or incomplete

1. **"The world is being regenerated"** contradicts AGENTS.md rule 7 and `direction-decision.md:38`, and **the live
   save holds `GargoyleAlchemist`** (§1.5). The rename instruction's justification ("acceptable precisely because the
   world is being regenerated") therefore is not established. It did not matter this time.
2. **The second argument of `FindTypeByFullName` is `ignoreCase`**, not a flag about aliases or full names. The brief
   said to check it; this is what it is.
3. **"`GargoyleStoneCrafter` collides case-insensitively only"** is right, and more precisely it **cannot** affect a
   save. It shares a bucket on the short-name and insensitive maps, and ours wins both.
4. **"Pinned misspells the class in both cases"** is confirmed. The brief left open whose misspelling it is. The class
   misspelling is ModernUO's; ServUO's is one file name.
5. Line citations checked and correct: `AssemblyHandler.cs:188-228` and `:251-263`, and `build.sh:36`. The namespace
   is on `:38`, and the comment explaining it is on `:36-37`.

---

## 5. Proposed bug-list rows (text only; `docs/` untouched)

> | **D34** | ... *(existing text)* ... | **SETTLED FOR THIS BUILD 2026-09-29, and now gated.** Probed at runtime: bucket
> `[GargoyleAlchemist, Glassblower]`, **ours first**, so every lookup (save hash, full name either case, short name)
> returns ours, and a save round trip reads back 578 of 578 bytes as `GargoyleAlchemist`. `GargoyleStoneCrafter`
> likewise, 565/565. **No rename.** The order is TypeDef order (746 against 1,460), which no source file determines,
> so it is enforced by `server/tests/TypeIdentity/TypeIdentityVerification.cs` on every build rather than assumed.
> **Correction to this row's premise: the live save's type table holds `GargoyleAlchemist`**, so a rename is not free.
> If the gate ever goes red here, prefer a one-line patch dropping `Glassblower`'s alias over renaming ours.
> `notes/type-identity.md` §1 |

> | **D36** *(new: the gate D34 implied)* | **Nobody had ever asked whether a type of ours is shadowed in the type table.**
> D34 and D35 were both found by accident | **Asked 2026-09-29 and the answer is none.** 8,508 types by full name
> (1,160 ours) and 4,281 spawnable types by short name (900 ours), zero failures. Ours are classified from
> `UOContent.pdb`, not grepped. Watched fail with a planted alias, then green, 177/177. One upstream-only shadow,
> `Blight`, is ModernUO's | **CLOSED on creation; the test is the deliverable.** `notes/type-identity.md` §2,
> `notes/type-identity-types.txt` |

> | **D35** | ... *(existing text)* ... | **Established 2026-09-29, recommendation pending Chase.** (1) Four distinct
> types, no shadowing, measured by a test fact. (2) Pinned's own code names only its misspellings: `Barracoon.cs:65`,
> `Neira.cs:72`, `BasePigmentsOfTokuno.cs:37,52`, `categorization.json`, its migrations. (3) **The misspelling is
> ModernUO's**: ServUO spells both classes right and misspells one file name, so the fidelity rule has no stake. And
> `[add GauntletsOfAnger` hands a staffer ours, which pigments cannot dye. **Recommend dropping ours**, while no save
> table holds them. `notes/type-identity.md` §3 |

D36 is a suggestion. If a gate that found nothing does not merit a D-number, fold it into D34's row.

---

## 6. Proof, reproduction, and what was not done

- **Gate:** `docker/uo/build.sh --tests-only`, three runs.
  - First run: classifier red. Watched and fixed.
  - Planted alias: red, 171/175. Restored.
  - Final: green, **177/177**, including the 10 new facts.
- **Output:** the facts' printed output is readable with the filtered `dotnet test ... --logger
  'console;verbosity=detailed'` in `sl-uo-builder:latest`. `build.sh`'s normal verbosity prints output only for
  failures.
- **Uncommitted work in the build:** the build tree includes another session's uncommitted
  `server/customizations/Engines/Craft/*CraftRegistrations.cs` (4 files) and `server/tests/Engines/Craft/`. They are
  in 177, and **the TypeDef order was measured with them present.** Not measured without them. They are not in my
  commit.
- **No runtime image built.** I ran `--tests-only` throughout, so `sl-modernuo:latest` did not move. That was
  deliberate, so as not to bake another session's uncommitted files into the tag the test shard runs.
- **Nothing deployed, no compose.**
- **`tools/progress.py`** was run as `--dry-run` only: "772 customization files, 23 patch files". Its output was not
  committed because it counts the other session's untracked files.
