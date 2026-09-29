# cc-P7: the drops pinned already wrote and left switched off (gates 9 and 12)

2026-09-29, CC. Brief: task P7 (pasted). Not deployed, not restarted, no `docker compose`, no image retagged: the only
build was `docker/uo/build.sh --tests-only`, which stops before the runtime image. `docs/`, `docker-compose.yml`,
`Distribution/Data/Spawns`, `D:\UO\ServUO-pub57` and `D:\UO\ModernUO-pinned` untouched (the last two read only).

## 0. The answer

**Predicted by the audit: gate 9, 7 new files greedy (11 alone); gate 12, 2 (6 alone). Delivered: 2, both from gate
9. Gate 12 delivers 0.**

Two files move from unreachable to reachable, **`MyrmidonGloves.cs`** and **`GreymistChest.cs`**, through two patches,
Miasma and Lady Lissith. Miasma's other 15 drop types were already reached some other way, which is why the audit
credited Miasma with one file. I checked all 17 against `content_index.py reach` on the live tree, before the patches
count (section 2.7). Every other target in the brief is declined, each for a reason read from source, not from the
audit:

| Target (brief's line) | Line confirmed? | Types exist? | Carrier reachable? | Guard | Verdict | Files delivered |
|---|---|---|---|---|---|---|
| `Miasma.cs:54` `MyrmidonGloves` | **yes**, `:54` (block `:44-73`) | all 16 of the switch, ours | **yes**, `Spawns/shared/malas/Labyrinth.json:15` | 2.5%, then 1 in 16: **0.156% per kill** for any one piece | **patched** | **1** (`MyrmidonGloves`) |
| `LadyLissith.cs:53` `GreymistChest` | **yes**, `:53` (block `:46-61`) | `GreymistChest` ours; **`LissithsSilk` and `ParrotItem` in neither tree** | **yes**, `Spawns/shared/ilshenar/TwistedWeald.json:15` | 2.5% | **patched, chest roll only** | **1** (`GreymistChest`) |
| `Ilhenir.cs:163-167` five Grizzle pieces | **yes** | all 5 ours | **no.** Nothing places a Corrupt champion spawn | 5% then 1 in 5, behind `Core.ML` | **declined** | 0 |
| `ChampionSpawnInfo.cs:126-128` Gorilla, Allosaurus, Dimetrosaur | **yes** (block `:123-129`) | **6 of 9 absent**: `DragonTurtle` (the champion), `MyrmidexDrone`, `MyrmidexLarvae`, `WildTiger`, `GreaterPhoenix`, `Infernus` | no spawn of the type exists or is generated | n/a | **declined** | 0 |
| `DefInscription.cs:445` `ScrappersCompendium` | **yes** (block `:442-453`) | compendium ours; `DreadHornMane`, `Taint`, `Corruption` pinned | **no.** Rare recipe 400 can never drop | `AddRareRecipe` | **declined** | 0 |
| gate 12: Barracoon, Neira | n/a | ours are **twins** of pinned types players already get | n/a | n/a | **declined: it would be D35 again** | 0 |
| gate 12: `ChampionSpawnType` | `:17-20` commented | the Valley entry above | | | **declined**, same as the Valley row | 0 |

**The audit's gate 9 and 12 rows should read: 2 files delivered by two patches, against 9 predicted greedy and 17
alone; about 1 unit spent of the 3 costed.**
The rest is not cheap, because each piece waits on something the audit did not cost: a champion placement, a
recipe-drop system, six creature ports, or nothing at all (the twins).

## 1. What changed

| File | Change |
|---|---|
| `D:\ShatteredLegacy\server\patches\Miasma-pinned-waiting-drop.patch` | New. Two hunks: removes `/*` and the TODO line (replaced by a two-line SL comment) at `:44-45`, and `*/` at `:73`. Pinned's 16-case body is untouched. |
| `D:\ShatteredLegacy\server\patches\LadyLissith-pinned-waiting-drop.patch` | New. Same shape at `:46-47` and `:61`. It also line-comments the `LissithsSilk` and `ParrotItem` rolls (`:55-59`): both types are missing from pinned and ours, so the full block would not compile. |
| `D:\ShatteredLegacy\docker\uo\apply-patches.sh` | Two `apply_patch` lines after the Virtue patch, plus a comment block naming this note and the declined targets. |
| `D:\ShatteredLegacy\server\tests\Mobiles\PinnedWaitingDropsVerification.cs` | New. Four facts, `namespace ShatteredLegacy.Tests`. |

Each patch carries the standard 3 lines of context per hunk and **no body lines**. Neither hunk spans the 16-line
switch or the drop lines, so a pinned bump that edits only the body still applies. Both applied at `--fuzz=0`, first
against a fresh copy of the two pinned files, then in the real builder (`[patches] Applied: ...`, "All 20 patches
applied successfully").

Not committed. `D:\ShatteredLegacy` had two unrelated modified files before I started (`docker/website/html/index.html`,
`scripts/Shard-Console.ps1`); I did not touch them.

## 2. Each target, established

### 2.1 Miasma: patched, 1 file

1. **Names.** All 16 `new X()` in the block resolve to ours, `Server.Items`, each with a parameterless `[Constructible]`
   constructor. `HunterGloves` and `HunterLegs` live in `Hunter/HuntersGloves.cs` and `HuntersLegs.cs`: the file
   names are plural and the classes are not, which matches what pinned spells. None is declared in pinned, under that
   name or as an alias; the test asserts `FindTypeByName` and `FindTypeByFullName` return ours.
2. **Carrier.** Miasma is a stock pinned creature placed by pinned's own spawn data,
   `Distribution/Data/Spawns/shared/malas/Labyrinth.json:15`, `maxCount 1`. Reach on that basis is the audit's `spawn`
   rule. Whether that spawner exists in the *live* world was not checked, because I did not open the save.
3. **Guards.** `Utility.RandomDouble() < 0.025`, then `Utility.Random(16)`. No expansion check. Not effectively zero:
   2.5% per kill for some piece, 1 in 640 kills for a given piece. `IsParagon = true` in the constructor, and the paragon
   chest goes through `OnBeforeDeath` (`BaseCreature.cs:2964`), not this `OnDeath`.

**Fidelity, needs Chase:** ServUO's Miasma (`Scripts/Mobiles/Named/Miasma.cs:67-89`) rolls `Utility.Random(18)` with
two more cases, `GreymistLegs` and `MyrmidonChest`. Pinned wrote 16. I shipped **pinned's 16 as written**, because the
brief's premise is completing pinned's intent, not redistributing loot. The effect: those two pieces are not in
Miasma's table, and each of the 16 is 1/16 rather than 1/18. If ServUO's 18 is the one a wiki documents, that is a
deviation for `docs/fidelity-principle.md`, and a two-line change to this patch. Unverified which is OSI.

### 2.2 Lady Lissith: patched (chest only), 1 file

1. **Names.** `GreymistChest` is ours (`Sets/Acolyte/GreymistChest.cs`). **`LissithsSilk` and `ParrotItem` exist in
   neither tree**; ServUO has them (`Items/Quest/LissithsSilk.cs`, a `PeerlessKey`; `Items/Addons/Parrot.cs`). So
   uncommenting pinned's block whole fails the build. The patch enables the chest roll and leaves the other two
   line-commented, in place, so the next person sees exactly what is missing.
2. **Carrier.** `Spawns/shared/ilshenar/TwistedWeald.json:15`, `maxCount 2`.
3. **Guard.** 2.5%. The silk and parrot rolls came after it and consumed randomness; with them commented, the chest
   roll is the only one left, and its own odds are unchanged.

`GreymistChest` is unreached on the live tree without this patch (section 2.7), and nothing else in pinned or ours
creates one, so this patch is its only path.

**Fidelity:** Lissith's other two drops are still missing. Reverses when `LissithsSilk` (a peerless key, so it waits on
the Twisted Weald peerless, B14) and `ParrotItem` are ported.

### 2.3 Ilhenir: declined, nobody can reach him

The five Grizzle types are ours, the lines are at `:163-167`, and the guard is `Core.ML` (true here), 5%, then 1 in 5.
**But Ilhenir is only ever the champion of `ChampionSpawnType.Corrupt`** (`ChampionSpawnInfo.cs:102`), and nothing
places one:

- `GenChamps.cs:30-54` generates Lost Lands spawns with no type, one ForestLord, and five dungeon types. None is
  Corrupt.
- A spawn with no type is `RandomizeType`, and `ChampionSpawn.Start` (`ChampionSpawn.cs:327-337`) rolls only among
  VerminHorde, UnholyTerror, ColdBlood, Abyss and Arachnid.
- No pinned spawn file names Ilhenir (`Distribution/Data`: only `categorization.json`, the `[add` menu). Neither does
  ours.

So only a GM who sets a champion spawn's `Type` to Corrupt by hand produces him, and that is staff reach (audit rule 5).
Uncommenting would add a patch that has to survive every pinned bump and delivers nothing. **Reverses when** something
places a Corrupt champion spawn. That is ServUO's Corrupted Forest / Ter Mur champion placement, a `GenChampEntry` row
or a generator of ours, and it becomes a two-hunk patch identical in shape to Miasma's. Five files.

### 2.4 The Valley champion (gate 9's `ChampionSpawnInfo.cs:126-128`, gate 12's `ChampionSpawnType`): declined

The three types the audit names are ours, but they sit in a table entry that also needs:

- **Six creatures in neither tree**: `DragonTurtle` (the champion itself), `MyrmidexDrone`, `MyrmidexLarvae`,
  `WildTiger`, `GreaterPhoenix`, `Infernus`. ServUO has each as one file.
- **An enum member pinned's own comments disagree about.** The commented enum lists `// DragonTurtle` (`:19`), but the
  commented table entry uses `ChampionSpawnType.Valley` (`:123`).
- **An ordinal pinned has already planned.** `GetInfo` indexes `Table[(int)type]` (`:139-148`), and `ChampionSpawn`
  serializes `_type` (`ChampionSpawn.cs:67-69`; the legacy reader is `(ChampionSpawnType)reader.ReadInt()`, `:1307`).
  Pinned's commented order is Unliving, Pit, DragonTurtle, Khaldun, i.e. 9-12. Adding Valley alone makes it 9, so a
  saved Valley spawn becomes an Unliving spawn the day pinned uncomments its own list. **That is a save-compatibility
  trap, and AGENTS.md rule 7 declines it outright.** Doing it right means adding Unliving and Pit too, and those need
  `PrimevalLich` and `AbyssalInfernal`: gates 17 and 19.
- **Title plumbing.** `ChampionTitleContext` carries one serialized field per type (`:53-57` onward); a new type needs
  its own.
- **A placement.** Even built, no generator places a Valley spawn.

**Reverses when** the six creatures are ported and the Unliving/Pit/Valley trio is taken on as one piece of work.
That is an encounter-scale item (audit cost 5+ at least), not a patch.

### 2.5 Scrapper's Compendium: declined, the recipe can never drop

The compendium is ours; `DreadHornMane`, `Taint` and `Corruption` are pinned (`Items/Resources/MiscMLResources.cs`).
The block is under `/* TODO` (no "uncomment once added") at `:442-453`, gated `Core.ML`. **The blocker is
`AddRareRecipe(index, 400)`.** It puts 400 in `m_RareRecipes` (`CraftSystem.cs:279-283`), which is read only by
`RandomRareRecipe()` (`:116-124`). **Nothing in pinned or ours calls `RandomRareRecipe()`.** `CraftmansSatchel` calls
`RandomRecipe()`, the non-rare list. So nobody can learn recipe 400, and nobody can craft the item. On top of that,
`DreadHornMane` has one source, Dread Horn, which is gate 21 and not ported.

**Reverses when** something calls `RandomRareRecipe()` for inscription (ServUO drops rare recipes from peerless
bosses) and Dread Horn is ported. One file, 2+ gates away.

### 2.6 Gate 12's Barracoon and Neira: declined, they are the twins

The audit's own `--sources` output (re-run in this session: `reach --sources --json`) names what gate 12 would put in
the world: `GauntletsOfAnger` through ServUO's `Barracoon.cs`, and `ShroudOfDeceit` through ServUO's `Neira.cs`.
**Both are ours, and both are twins of pinned artifacts that players already get:**

- Pinned `Barracoon.cs:65` drops **`GuantletsOfAnger`** (pinned's spelling). Pinned `Neira.cs:72` drops
  **`ShroudOfDeciet`** (pinned's spelling).
- Audit section 4 (`reachability-audit.md:221-222`) and `type-identity.md:234-263` already record them as twins with
  swapped spellings.

"Patching Barracoon and Neira" would therefore swap a reachable, pigment-dyeable pinned artifact
(`BasePigmentsOfTokuno.cs:37,52` lists pinned's two) for our dormant twin. That changes a stock table (the gate 3/5
question), for negative value. It is the D35 near-miss, arriving from the other direction. `type-identity.md:327`
already recommends dropping ours. **Nothing here to patch; gate 12's "Pinned has all three. A patch" is wrong.**

### 2.7 The count, and a gap in the instrument this patch shape exposes

`python tools/content_index.py reach --sources --json <scratch>/reach.json`, run in this session against the live
`D:\ShatteredLegacy\server\customizations` (default `CONTENT_INDEX_OURS`). Of the 17 drop types the two patches enable,
**15 are already `reached`** (the other Miasma pieces, through other sources). **2 are `unreached`: `MyrmidonGloves`,
`GreymistChest`.** File level agrees: `Sets/Myrmidon/MyrmidonGloves.cs` and `Sets/Acolyte/GreymistChest.cs` are
`unreached`.

**Instrument gap, for whoever owns `content_index.py`:** the tool treats a patch's **added** lines as roots (audit
section 2). In an uncomment patch, the `c.DropItem(new MyrmidonGloves())` lines are **context**, not added: only the
comment markers change. So after these patches are committed, `reach` will still report both files unreached. Fix
shape: for a `.patch` whose target is a pinned file, treat a context line inside a hunk whose removed lines include
`/*` or `*/` as live. Or simpler, apply the patches to a scratch copy of pinned and index that. Not done here, because
the tool is not in this brief. **Until then, the audit's appendix will overstate unreached by these 2.**

## 3. Tests

`server/tests/Mobiles/PinnedWaitingDropsVerification.cs`, four facts:

| Fact | Asserts |
|---|---|
| `EveryDropTypeIsOursConstructibleAndResolvesByItsName` | each of the 17 types resolves by short and full name to **ours** (the D35 check) and constructs; `Miasma` and `LadyLissith` resolve by the names the spawn files use |
| `MiasmaDropsEachOfPinnedsSixteenIntoTheContainer` | for each `Utility.Random(16)` result 0..15, with the 2.5% roll passing, `OnDeath(c)` puts **exactly one** item in `c`, of pinned's case type |
| `MiasmaDropsNothingOnARollAtItsChance` | a roll of exactly 0.025 drops nothing, which pins pinned's `<` and its chance |
| `LadyLissithDropsGreymistChestAndNothingElse` | with every roll passing, `c` holds exactly one `GreymistChest` (the silk and parrot lines really are off); at 0.025, nothing |

The rolls are too rare to meet through real kills (1 in 640 per piece), so the facts script `BuiltInRng.Generator`. Its
setter is `internal`, and `Server.csproj:50` gives `UOContent.Tests` `InternalsVisibleTo`. Pinned's own
`Server.Tests/Helpers/PredictableRandom.cs` does the same. The creature is constructed before the script goes in.
`OnDeath` is called directly with a `Backpack`, which is the container the uncommented `c.DropItem` lines write to.

**Results:** see section 5.

## 4. Proposed client-test rows (for `docs/client-test-queue.md`; not written there, `docs/` is not mine)

Neither row can be checked from source alone, because both depend on the live world. **Both need a person in the
client.**

1. **Miasma is actually spawned in the Labyrinth on the live shard.** Go to the Labyrinth (Malas), confirm a spawner
   holds Miasma, kill it. *Expected:* corpse normal; the set-piece drop is 2.5%, so one kill proving nothing is fine.
   What this row checks is the **carrier**, the one assumption in section 2.1 I could not verify. Staff shortcut:
   `[add Miasma`, kill, repeat, or `[props` a spawner.
2. **Lady Lissith is actually spawned in the Twisted Weald.** Same shape (Ilshenar, `TwistedWeald.json:15`).

A third, optional one for whoever reviews the drops: `[add MyrmidonGloves` and `[add GreymistChest`, and check the
tooltip shows the set name and piece count. That is the set-armour tests' territory, already covered by
`ArmourSetBonusVerification`, so it is not needed for P7.

## 5. Build and red proof

**Green.** `docker/uo/build.sh --tests-only` from `D:\ShatteredLegacy`: patches gate `[patches] Applied:
Miasma-pinned-waiting-drop.patch`, `... LadyLissith-pinned-waiting-drop.patch`, "All 20 patches applied
successfully". Test gate: **185 passed of 185**, all four new facts among them. Stopped before the runtime image. No
image retagged, nothing restarted.

**Red.** Same build without the two patches, built by hand from a **scratch copy** of `server/{customizations,tests,
migrations,patches}` and `docker/uo`, with the patch files and their two `apply_patch` lines removed. I built it there
and not by editing `D:\ShatteredLegacy`, because P6's note records an autocommit capturing a red stub mid-run. It was
tagged `sl-uo-builder:p7-red` so the real builder tag stayed green, and that tag was deleted afterwards. Patches gate:
"All 18 patches applied successfully". Tests, filtered to this class:

| Fact | Without the patches |
|---|---|
| `MiasmaDropsEachOfPinnedsSixteenIntoTheContainer` | **Failed**: `Assert.Single() Failure: The collection was empty` |
| `LadyLissithDropsGreymistChestAndNothingElse` | **Failed**: same |
| `EveryDropTypeIsOursConstructibleAndResolvesByItsName` | passed, as it should: it guards names and twins, not the patch |
| `MiasmaDropsNothingOnARollAtItsChance` | passed, **and cannot go red this way**: an empty `OnDeath` also drops nothing. It guards the other direction, a bump or edit that loosens pinned's `< 0.025` |

So the two facts that carry this gate were watched failing without the patches and passing with them.

## 6. For Chase

1. **Commit** the four `D:\ShatteredLegacy` changes together: two `.patch` files, the `apply-patches.sh` lines, and
   the test. The test fails without the patches, so it must not land alone. `docker/website/html/index.html` was already
   modified before I started and is not mine.
2. **Fidelity decision (non-blocking):** Miasma, pinned's 16 or ServUO's 18 (section 2.1).
3. **Audit rows 9 and 12** want the delivered numbers from section 0, and gate 12's "A patch" wants striking.
4. **Instrument gap** in section 2.7, if the audit is re-run after this lands.
