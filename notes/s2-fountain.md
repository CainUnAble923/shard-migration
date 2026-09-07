# S2 — Fountain of Fortune cluster

Done 2026-09-07. Reverses the second of the two declines `docs/subsystem-policy.md` lists, and
closes Q-010.

---

## 1. The verified file list

**The brief's estimate was wrong in both directions, and the interesting half is the second one.**

> "`Items/Addons/FountainOfFortune.cs` (318 lines) plus a handful of leaf items including
> `EnchantedEssence`, `RelicFragment`, `GemologistsSatchel` and `SolesOfProvidence`", "roughly
> 900 lines".

The four named files are right and 318 is right. But the **core** of the cluster is **465 lines
across 4 files, about half the estimate**, and the **whole** cluster is **2,292 lines across 38
files, about 2.6x it**. One reward branch carries the entire difference.

### What I added, and why

`GemologistsSatchel.cs:26` reads `Server.SkillHandlers.Imbuing.IngredTypes`:

```csharp
Type type = Server.SkillHandlers.Imbuing.IngredTypes[Utility.Random(...Length)];
```

`IngredTypes` is a 42-entry `Type[]` at
`Scripts/Services/LootGeneration/Imbuing/Core/Imbuing.cs:1735`. Counted against
`D:\UO\ModernUO-pinned` at `7c9215d97`:

| | Count |
|---|---|
| Types in the array | 42 |
| Already in pinned ModernUO | 6 (`ParasiticPlant`, `LuminescentFungi`, `FireRuby`, `WhitePearl`, `BlueDiamond`, `Turquoise`) |
| Already in `server/customizations` | 1 (`RaptorTeeth`, from CC3) |
| **Missing, and therefore added to this task** | **35** |

The brief's premise is correct as far as it goes: `EnchantedEssence` and `RelicFragment` really
are leaf items in `SAQuestItems.cs` and Imbuing really does only consume them. The premise just
does not cover the satchel, which is the one member of the cluster that reaches *into* Imbuing
rather than being reached into.

**It is not a subsystem pull-in, and that is what decided it.** All 31 of the
`Items/Resource/` ingredient files are `Item, ICommodity` stackables carrying an ItemID and a
cliloc and nothing else; `grep -oE "new [A-Z][A-Za-z0-9_]*\("` across all 31 returns **zero
matches**. `PowderedIron` is a plain `Item`. The remaining 4 are classes in `SAQuestItems.cs`,
two of which the core cluster needed anyway. Only `IngredTypes` itself — a static data table —
lives on a subsystem class.

Raised as **Q-020** with the numbers before writing anything. Chase chose option A, port all 35.
Zero deviations, and the 35 are Stygian Abyss drop content CC5 and CC6 want regardless.

### What I dropped

**Nothing from the cluster.** Two things reachable *from* it were deliberately left out, and
neither is part of it:

1. **`Services/Underworld/Generate.cs`** is the only place ServUO constructs a
   `FountainOfFortune` (`:183`, at `(1121, 957, -42)` on Ter Mur). That file also generates the
   Maze of Death, Navrey's Lair, the Puzzle Room and the Experimental Room. **Porting the
   fountain does not port the Underworld, so nothing places one automatically.** A GM must
   `[add FountainOfFortune`. Deviation D-3 below.
2. **`Services/Pet Training/SpecialAbility.cs`** calls `FountainOfFortune.UnderProtection` at
   `:2120` and `:2198`. That is the Pet Training subsystem, out of scope and untouched. The
   static is now present for it if Pet Training is ever taken on.

### The list

Everything below is `D:\UO\ServUO-pub57\Scripts\` on the left and
`D:\ShatteredLegacy\server\customizations\` on the right.

**Core cluster — 4 files, 465 ServUO lines**

| ServUO source | Lines | Ported to |
|---|---|---|
| `Items/Addons/FountainOfFortune.cs` | 318 | `Items/Addons/FountainOfFortune.cs` |
| `Items/Artifacts/Equipment/Clothing/SolesOfProvidence.cs` | 34 | same path |
| `Items/Quest/SAQuestItems.cs:290-346` `EnchantedEssence` | 57 | `Items/Quest/EnchantedEssence.cs` |
| `Items/Quest/SAQuestItems.cs:622-677` `RelicFragment` | 56 | `Items/Quest/RelicFragment.cs` |

**Restored, not new — 1 file**

| ServUO source | Lines | Ported to |
|---|---|---|
| `Items/Quest/SAQuestItems.cs:444-524` `LuckyCoin` | 81 | `Items/Quest/LuckyCoin.cs` (`OnDoubleClick` + `InternalTarget` restored) |

**The satchel and its forced dependencies — 34 files, 1,827 ServUO lines**

| ServUO source | Lines | Ported to |
|---|---|---|
| `Items/Containers/GemologistsSatchel.cs` | 58 | same path |
| `Items/Quest/SAQuestItems.cs:526-581` `MagicalResidue` | 56 | `Items/Quest/MagicalResidue.cs` |
| `Items/Quest/SAQuestItems.cs:158-202` `BouraPelt` | 45 | `Items/Quest/BouraPelt.cs` |
| 31 files in `Items/Resource/` (below) | 1,668 | `Items/Resource/<class>.cs` |

The 31: `SeedRenewal.cs`, `ChagaMushroom.cs`, `CrystalShards.cs`, `BottleIchor.cs`,
`ReflectiveWolfEye.cs`, `FaeryDust.cs`, `SilverSnakeSkin.cs`, `ArcanicRuneStone.cs`,
`SlithTongue.cs`, `VoidOrb.cs`, `SpiderCarapace.cs`, `DaemonClaw.cs`, `VialOfVitriol.cs`,
`GoblinBlood.cs`, `LavaSerpenCrust.cs`, `UndyingFlesh.cs`, `CrushedGlass.cs`,
`CrystallineBlackrock.cs`, `PowderedIron.cs`, `ElvenFletchings.cs`, `DelicateScales.cs`,
`EssenceSingularity.cs`, `EssenceBalance.cs`, `EssencePassion.cs`, `EssenceDirection.cs`,
`EssencePrecision.cs`, `EssenceControl.cs`, `EssenceDiligence.cs`, `EssenceAchievement.cs`,
`EssenceFeeling.cs`, `EssenceOrder.cs`.

**Three of those ServUO filenames disagree with the class inside them** — `SeedRenewal.cs` holds
`SeedOfRenewal`, `LavaSerpenCrust.cs` holds `LavaSerpentCrust`, and `ElvenFletchings.cs` holds
`ElvenFletching`. (`VialOfVitriol.cs` matches its class; its misspelling is in the attribute,
`[TypeAlias("Server.Items.VialVitirol")]`, which is carried across verbatim because it is a save
compatibility key, not a typo to fix.) **Ours are named after the class**, following
`RaptorTeeth.cs` and `LuckyCoin.cs`. The directory still mirrors ServUO's, which is what the
rule asks for; only those three basenames differ.

**Infrastructure — 3 files**

| File | What |
|---|---|
| `server/patches/PlayerMobile-fountain-luck-bonus.patch` | new, 1 line changed |
| `docker/uo/apply-patches.sh` | one `apply_patch` line, or the runner fails the build for an unaccounted patch |
| `server/tests/Items/Addons/FountainOfFortuneVerification.cs` | new, 5 `[Fact]`s |

**Total: 38 ported files, 2,292 ServUO lines, plus 3 infrastructure files.**

Checks: 4 + 34 = 38, and 465 + 1,827 = 2,292. Another way to reach the same 38, which is how
I caught the error below: the 35 missing ingredient types, plus `FountainOfFortune`,
`SolesOfProvidence` and `GemologistsSatchel`, which are not ingredients. `LuckyCoin` is a 39th
file touched but not a new one.

> **Correction, before the commit.** I first wrote 36 and 32 here, and they were wrong: the
> satchel group is 34 files, not 32, so the total is 38, not 36. The line figures were right
> throughout — 1,827 and 2,292 both check out — which is exactly why the file count slipped
> past a read-through. Caught by counting `git diff --cached --name-status` against the table
> instead of trusting it. **Seven for seven.** The rule is not "count carefully once", it is
> "count the artifact at the end as well", and this repo has now paid for that lesson in a
> document whose own opening paragraph is about miscounting.

---

## 2. The luck patch is the whole reason this ships with a test

`FountainOfFortune` is content-shaped in its parts and subsystem-shaped in its wiring: a reward
loop, three static tables, a defrag timer, a resurrect hook, and one patch into upstream. Per
`docs/subsystem-policy.md` that means a committed regression test, and S2 is the first content
task to use S4's route in anger.

**What ServUO does.** The fountain's luck reward goes into `PlayerMobile.RealLuck`
(`Mobiles/PlayerMobile.cs:4397`), which is a *separate property* from `Luck`. Counted, not
eyeballed: **21 read sites across 20 files** (`grep -rn RealLuck` gives 22 lines, one of which is
the declaration) — `LootPack`, `Paragon`, `Mining`, `TreasureMapChest`, `RunicReforging` and the
seasonal-event point systems among them. `Luck` itself, the value the status packet sends the
client, does not include the bonus.

**What ModernUO has.** No `RealLuck`. Three luck consumers in total, and all three read
`Mobile.Luck`:

| ModernUO site | ServUO equivalent reads |
|---|---|
| `Misc/LootPack.cs:71` | `RealLuck` |
| `Mobiles/Special/Paragon.cs:209` | `RealLuck` |
| `Engines/Treasures of Tokuno/TreasuresOfTokuno.cs:197` | `RealLuck` |
| `Server/Network/Packets/OutgoingMobilePackets.cs:553` (status bar) | `Luck` |

So three of the four should include the fountain bonus and one should not.

**Chosen: one patch to `PlayerMobile.Luck`.** It gets the three behavioural sites right and the
cosmetic one wrong (D-2 below). The faithful alternative — add a `RealLuck` property and patch
all three call sites — is three patches into three unrelated content files ModernUO actively
develops, against one patch into a file we already patch. `docs/subsystem-policy.md` weighs
reconciliation burden explicitly, and 3:1 on a cosmetic difference is not a close call. Recorded
here so it can be revisited if the status-bar reading ever bothers anyone.

**And this is exactly the failure mode S4 was built for.** If a bump rewrites
`PlayerMobile.Luck`, the patch stops applying and the build fails loudly. If a bump instead
stops routing loot through `Mobile.Luck`, **the patch still applies, everything still builds,
and the fountain's luck reward silently stops mattering.** Nothing but
`FountainLuckBonusReachesPlayerMobileLuck` would notice.

---

## 3. Deviations

**D-1. `SolesOfProvidence` loses `IsArtifact`.** ModernUO has no `IsArtifact` on `BaseClothing`
or anywhere else — `grep -rn "bool IsArtifact"` over `Projects/` returns nothing. Every ServUO
consumer of it is itself absent here: `RunicReforging`, `BasePigmentsOfTokuno`, `NaturalDye`,
`SpecialNaturalDye`, `AlterItem`, `ArcaneGem`, `GenerateGameDocs`. **Inert either way.** The
item's actual property, `Attributes.Luck = 80`, is intact.

**D-2. The fountain's luck bonus shows in the status bar; in ServUO it does not.** A player who
wishes and rolls luck sees their Luck reading rise by 400 for the hour, where a ServUO player
gets the loot benefit invisibly. Cause and reasoning in section 2. Arguably an improvement —
the message says "Your luck just improved!" — but it is a difference from the source and it is
logged as one.

**D-3. Nothing places a fountain.** ServUO builds one at `(1121, 957, -42)` on Ter Mur inside
`Services/Underworld/Generate.cs`, which we have not ported and which is a dungeon generator,
not part of this cluster. **On this shard the fountain exists as a `[add FountainOfFortune`
addon and nowhere else**, so `LuckyCoin`'s "That is not sacred waters. Try looking in the
Underworld." is currently the *only* outcome a player can reach without a GM. That is a real
gap and Chase should decide whether to place one; it is one `MoveToWorld` call if so, and it is
deliberately not in this task. **Raised as Q-021.**

**D-4. Two fountain reward cases are unreachable, upstream and here.** ServUO's buff branch
rolls `Utility.Random(4)` over a **six**-case switch, so `case 4` (special protection) and
`case 5` (balm boost) never fire in ServUO either. **Ported unchanged.** Widening the roll
would hand our players a buff no ServUO or OSI player gets, which is a fidelity deviation in
the direction nobody thinks to check a wiki for. The dead cases are left in place with a
comment so the next reader does not "fix" them either.

Consequence worth knowing: `FountainOfFortune.UnderProtection` therefore always returns false,
which matters to `TanglingRoots` (one of the twelve coin droppers, not yet ported) and to Pet
Training's `SpecialAbility`. Both will compile and behave exactly as they do on ServUO.

**D-5. `IngredTypes` lives at its consumer.** ModernUO has no Imbuing skill handler, so the
42-entry array sits in `GemologistsSatchel.cs` as a `private static readonly Type[]`.
**Contents are the ServUO array verbatim, all 42 entries in source order, no substitutions and
no omissions** — that is what porting the 35 bought. If Imbuing is ever ported, that array is
the thing to delete. Structural only; no behaviour differs.

**D-6. Upstream quirk carried, not fixed.** The fountain's last addon component uses
`++itemID` where the other fifteen use `itemID++`, so graphic `0x1740` is skipped and `0x1741`
used instead. Ported unchanged with a comment.

### Q-010 is CLOSED

`LuckyCoin.OnDoubleClick` and its `InternalTarget` are restored in
`server/customizations/Items/Quest/LuckyCoin.cs`. The coin now asks for a target, accepts an
`AddonComponent` whose `Addon` is a `FountainOfFortune`, and otherwise says "That is not sacred
waters."

**`docs/fidelity-principle.md` should drop the Q-010 entry.** That is the overseer's edit, not
mine — flagged here per the `notes/` / `docs/` split.

**All twelve coin droppers are covered by the one restoration**, as the brief says:
`GreaterPoisonElemental`, `EnragedEarthElemental`, `GreenGoblin`, `GreenGoblinAlchemist`,
`GreenGoblinScout`, `BloodWorm`, `Gremlin`, `IronBeetle`, `Mimic`, `SentinelSpider`,
`TanglingRoots`, `WolfSpider`. **One caveat on that sentence: only one of the twelve is in the
tree today** (`GreaterPoisonElemental`, from P2). The other eleven are CC6 backlog. The
restoration is genuinely once-for-all; it just currently applies to one creature.

---

## 4. ServUO → ModernUO conversions worth reusing

Beyond the standard ones already in `notes/port-recipe.md`:

- **`ICommodity` changed shape.** ServUO's `TextDefinition ICommodity.Description` is ModernUO's
  `int ICommodity.DescriptionNumber`. `IsDeedable` is unchanged.
- **`ResurrectGump` takes no callback.** ServUO's
  `ResurrectGump(m, healer, msg, fromSacrifice, hitsScalar, callback)` has no ModernUO
  counterpart; ModernUO's is `(healer, msg, fromSacrifice, hitsScalar, price)` and the target
  comes from the `NetState` in `OnResponse`. **Subclass it rather than patch it** — the class
  is not sealed and `OnResponse` is overridable, so `FountainResurrectGump` calls `base` and
  then sets the cooldown only if the player actually got up. One fewer patch than the obvious
  route, and no upstream logic copied into our tree.
- **`Timer.DelayCall` starts itself** in ModernUO. ServUO's paired `.Start()` is a double start;
  drop it.
- **Unpersisted instance state.** ServUO recreates its cooldown dictionaries in `Deserialize`
  rather than writing them. With `[SerializationGenerator]` the same effect comes free from
  field initialisers, which run on both the `[Constructible]` and the `(Serial)` path. Anything
  ServUO does *after* `reader.ReadInt()` — here `AddFountain(this)` — goes in an
  `[AfterDeserialization(false)]` method.
- **`DateTime.UtcNow` is `Core.Now`.**

---

## 5. Phase timings

| Phase | Wall clock | How measured |
|---|---|---|
| Reading, dependency walk, counting, writing all 40 files | **not separately timed** | everything up to the first build was done by **07:40:04Z**, the only anchor I have. Recording that rather than inventing a split. |
| Build cycle 1 — full `build.sh`, **failed at the test gate** | **3m 57s** | 07:40:04Z to 07:44:01Z |
| Isolating that failure (Git Bash path mangling, Q-022) | ~1 min | one manual `docker run` with `MSYS_NO_PATHCONV=1`: 9/9 passed |
| Build cycle 2 — full `build.sh`, **green** | **under 2 min** | ended 07:49:21Z; its start was not separately recorded, so this is bounded, not measured |
| Runtime run 1 — start, load, save, shutdown | **1m 27s** | 02:50:56 to 02:52:23 container-local |
| Runtime run 2 — reload, save, clean shutdown | **1m 31s** | 02:53:18 to 02:54:49 container-local |
| Reflection probe over the shipped assembly | ~30s | one `dotnet run` in the runtime image |

Both runtime figures are dominated by the fixed `sleep`s in the harness invocation, not by the
server: the world loads in 0.81s and saves in 0.24s.

**Two build cycles, one failed, and the failure was not in the ported code.** Both UOContent and
UOContent.Tests compiled clean on the first attempt — 38 new files, one patch and five new tests
with zero compiler errors, which is what the pre-build dependency check against
`D:\UO\ModernUO-pinned` is for.

---

## 5a. Verification results

**Build — `docker/uo/build.sh`, full green.**

```
[patches] All 13 patches applied successfully.
[patches] structured customizations installed: 77 file(s).
[patches] shard tests installed: 2 file(s).
== 2/3 running ShatteredLegacy.Tests tests (test gate) ==
     Passed: 9
[tests] 9 test(s) passed.
== 3/3 building runtime image sl-modernuo:latest ==
Built sl-modernuo:latest with patches applied and 9 shard test(s) passing.
```

All nine: S1's four, unchanged and still green, plus S2's five.

```
Passed FountainOfFortuneVerification.FountainLuckBonusReachesPlayerMobileLuck [3 ms]
Passed FountainOfFortuneVerification.AWishConsumesOneCoinAndSetsTheDailyCooldown [7 ms]
Passed FountainOfFortuneVerification.TheLastCoinIsDeletedRatherThanLeftAtZero [7 ms]
Passed FountainOfFortuneVerification.DoubleClickingACoinInTheBackpackAsksForATarget [69 ms]
Passed FountainOfFortuneVerification.GemologistsSatchelCarriesGemsAndImbuingIngredients [1 ms]
```

**Build cycle 1 failed, and not on anything in this task.** See Q-022: Git Bash rewrites
`-w /build/modernuo` into `C:/Program Files/Git/build/modernuo` before `docker run` sees it, and
the daemon rejects it. The gate reported a daemon error as "tests did not pass". Fixed in
`docker/uo/build.sh` with an `MSYS_NO_PATHCONV=1` prefix and a comment saying why.

**Runtime — throwaway container, loopback-only, scratch save directory.** Not the live stack,
never deployed, `listeners: ["127.0.0.1:2593"]`, `serverListing.address: 127.0.0.1`,
`autosave.enabled: False`, a scratch `Saves/` under the temp tree.

```
run 1  [INF] Loading world done (618 items, 90 mobiles) (0.38 seconds)
       [INF] Listening: 127.0.0.1:2593
       [INF] Saving world done (0.24 seconds)
       [INF] Writing world save snapshot done (0.34 seconds)

run 2  [INF] Loading world done (622 items, 91 mobiles) (0.81 seconds)   <- reload of run 1's save
       [INF] Listening: 127.0.0.1:2593
       [INF] Listening: 127.0.0.1:12000 (Pings)
       [INF] Saving world done (0.24 seconds)
       [INF] Shutting down                                                <- exit 0
```

**Type registration, read off the shipped `UOContent.dll` rather than off the source.** Sampled
14 of the 38, chosen to cover every base type and all four filename-vs-class renames:

```
OK  Server.Items.FountainOfFortune   base=BaseAddon  generated=[Serialize(IGenericWriter) Deserialize(IGenericReader)]  ctors=[() (Serial)]
OK  Server.Items.GemologistsSatchel  base=Bag        generated=[...]  ctors=[() (Serial)]
OK  Server.Items.SolesOfProvidence   base=Sandals    generated=[...]  ctors=[() (Serial)]
OK  Server.Items.LuckyCoin           base=Item       generated=[...]  ctors=[(Int32) (Serial)]
OK  SeedOfRenewal / LavaSerpentCrust / ElvenFletching / VialOfVitriol     (the four renames)
OK  EnchantedEssence / RelicFragment / MagicalResidue / BouraPelt / EssenceOrder / PowderedIron
PlayerMobile.Luck declared here: True
GemologistsSatchel.IngredTypes length = 42
```

None of `Serialize`, `Deserialize` or the `(Serial)` constructor is in our source, so their
presence is direct evidence the generator ran. `PlayerMobile.Luck declared here: True` is the
luck patch, read back off the assembly the server actually loads. **`IngredTypes length = 42`
with no null entries is the point of the whole Q-020 detour**, checked at runtime rather than
assumed from the source.

**What is still unverified, and it is the same gap every content task has had.** No *instance*
of a fountain has been in a saved world. The container console has only `save`, `shutdown` and
`restart`, so there is no headless way to place one — `notes/port-recipe.md` covers why. The
five tests exercise `OnTarget`, the cooldown, the coin and the satchel directly, which is more
than any previous port had, but **the addon's own components surviving a save and reload needs a
client.** Batch it into the next client spot check.

**One incidental upstream bug, found while setting the throwaway config up.** With
`pingServer.enabled: "False"`, ModernUO's `PingServer.Shutdown()`
(`Projects/Server/Network/PingServer.cs:145`) dereferences a listener it never created and
throws `NullReferenceException` on every shutdown, which CrashGuard then reports as a crash.
Nothing to do with this port — it reproduces on stock — but **anyone who turns the ping server
off on the live shard gets a crash report on every clean shutdown.** Not filed as a question
because nothing here needs it; noted so the next person who sees that stack does not go hunting.

---

## 6. What this cost, honestly

**The dependency walk was worth more than the port.** The port itself is mechanical — 35 of the
38 files are a data table with a `[Constructible]` around it. The walk is what turned "roughly
900 lines" into 465 and 2,292 and found the one edge that mattered.

**Six for six on unverified counts.** `AGENTS.md` says every count in this project stated
without counting has been wrong five times. The brief's "roughly 900 lines" is the sixth, and it
was wrong in both directions at once, which is a new failure mode: the estimate was too big for
the thing it described and too small for the thing that thing needed. Publishing the list beside
the count is what caught it. **The rule earned its keep again; do not relax it.**
