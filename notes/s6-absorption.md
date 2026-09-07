# S6 — `SAAbsorptionAttributes`, the Stygian Abyss damage eater

**Status: built, gated green, A5 closed.** Completed 2026-09-07.

The property reaches the tooltip **and** the effect reaches combat. Both halves shipped together,
because the half that shows numbers without doing anything is worse than neither.

---

## 1. Verdict

| Question from `docs/subsystem-policy.md` | Answer |
|---|---|
| Unblock ratio | 57 files reference it. **8 are finished by S6, 5 more are carrier-ready, 31 each need a small carrier class S6 deliberately did not build, and 13 were never absorption-blocked at all.** See §6 — the 57 is a reference count, not a port-now count, and this is the first time that distinction has been drawn on this figure. |
| Fits the layering pattern? | **Yes, S1's shape exactly.** Two additive files, one field on a class of ours, one hook into `UOContent`. Zero upstream serialization versions bumped, zero fields added to any upstream class, **no core-project patch** — S6 is cheaper here than S1, which needed one. |
| What breaks on a bump, would we notice? | One patch, and a committed test that fails when the patch stops being reached. §3. |

**The three dependency claims S3 made were all correct, and two are stronger than S3 stated.** I
verified each in `D:\UO\ServUO-pub57` rather than relying on the measurement:

- `RunicReforging.GetSAAbsorptionAttributes` (`RunicReforging.cs:2765-2780`) is a **16-line
  four-branch type test** returning the item's own attributes, exactly as S3 said. Inlined as an
  interface test.
- `Enhancement.GetValue(m, SAAbsorptionAttribute)` (`Abilities/Enhancement.cs:220`) returns 0
  unless something wrote an absorption attribute into `EnhancementList`. The **only** writer that
  ever does is `Abilities/EnhancementTimer.cs:62`, and `grep -rn "new EnhancementTimer" Scripts/`
  returns **nothing**. It is dead code in ServUO too. The term is zero on ServUO, not merely zero
  here.
- `SkillMasterySpell.GetAttributeBonus(m, SAAbsorptionAttribute)`
  (`Core/SkillMasterySpell.cs:1174`) is a switch with **one** arm: `CastingFocus`, from
  Perseverance. It cannot return non-zero for any Eater or Resonance attribute **in ServUO
  either**, so dropping it costs the damage eater exactly nothing. It would matter only if Skill
  Masteries were built and only for Casting Focus.

**S3's cost estimate was good and slightly pessimistic.** Budget ~1,120 lines; actual **1,031**:

| Piece | Lines |
|---|---|
| `SAAbsorptionAttributes.cs` (enum, class, `IAbsorptionItem`, aggregation, tooltip block) | 342 |
| `Abilities/SAPropEffects.cs` (the damage-eater subset of ServUO's 768) | 402 |
| `AbsorptionAttributesVerification.cs` (6 tests) | 223 |
| `AOS-damage-eater-hook.patch` | 25 (16 added lines) |
| `BaseSetArmor.cs` delta | 31 |
| Eight Aloron pieces, one line each | 8 |

The 402 rather than 768 is because eight of ServUO's nine `PropertyEffect` kinds — Soul Charge,
Splintering, Searing, Bane, Bone Breaker, Swarm, Sparks, Battle Lust — are weapon properties
belonging to systems this shard does not have. Only `DamageEaterContext` came.

---

## 2. The thing everyone has been describing wrong, including S3 and me

**The damage eater does not reduce damage.**

`docs/gap-register.md` A5 says "gives no cold-damage eating", `notes/s3-decline-costs.md` §6 says
"assert that damage taken with an eater item equipped is **reduced**", and the name says eater. All
of that reads as damage reduction. It is not what the code does.

`DamageEaterContext.OnDamage` (`SAPropEffects.cs:239`) takes the full damage, computes a share of
each damage-type component, and schedules a **heal three seconds later**
(`Timer.DelayCall(TimeSpan.FromSeconds(3), DoHeal, ...)`). The victim takes the hit in full and
gets part of it back, capped at 30% of that component for a matching eater and 18% for the generic
`EaterDamage`, with at most 20 heals pending at once. `totalDamage` is never touched, which is why
the hook can sit anywhere in `AOS.Damage` without changing anything downstream.

This matters for two reasons and neither is pedantry:

1. **A test written to S3's description would have been written wrong**, asserting reduced damage
   that never happens.
2. **A player reading UOGuide will see the heal**, so getting this right is the fidelity call.

Recorded here rather than in `docs/` per the lane rule. `docs/gap-register.md` A5's wording and
`notes/s3-decline-costs.md` §6's "reduced" both want correcting on review.

---

## 3. Maintenance cost — what a pinned-commit bump has to reconcile

**Read this before bumping `MODERNUO_COMMIT` in `docker/uo/Dockerfile`.** It is the companion to
`notes/s1-armour-sets.md` §3, and it is shorter, because S6 patches one file where S1 patched
three.

`apply-patches.sh` has been a hard gate since F2, so the patch fails the build loudly rather than
drifting. **No method body of ModernUO's is reimplemented anywhere in S6**, so there is no
copied-upstream-logic category to watch.

### Patched upstream files: one

#### `AOS-damage-eater-hook.patch`

- **File:** `Projects/UOContent/Misc/AOS.cs`, inside
  `AOS.Damage(Mobile, Mobile, int, bool, int, int, int, int, int, int, int, bool, bool, bool)`.
  **`UOContent`, not the core project.** S6 needs no core patch.
- **Change:** 16 added lines, **zero changed lines**. An `if (ignoreArmor) … else …` calling
  `DamageEaterContext.CheckDamage(...)`, inserted between the reflect-physical block and the
  `if (totalDamage <= 0) { return 0; }` guard. That is where ServUO calls it, at
  `Scripts/Misc/AOS.cs:288-291`.
- **What it assumes about upstream, precisely:**
  1. `AOS.Damage` still exists and is still what deals typed damage to a `Mobile`.
  2. The reflect block still ends with the two closing braces the hunk uses as leading context,
     immediately followed by a blank line and `if (totalDamage <= 0)`.
  3. `totalDamage`, `phys`, `fire`, `cold`, `pois`, `nrgy`, `direct` and `ignoreArmor` are all
     still in scope under those names at that point.
  4. `Projects/UOContent/Misc/AOS.cs` still has `using Server.Items;` — `DamageEaterContext` is
     declared in `Server.Items`, and it is line 4 of the stock file.
- **A bump breaks it if:** ModernUO restructures the tail of `AOS.Damage`, renames any of those
  locals, moves the `totalDamage <= 0` guard, or splits typed damage out of `AOS.Damage`.
- **If the patch fails:** re-derive the insertion point at whatever now computes `totalDamage`
  before applying it. The block adds behaviour to nobody — with no `IAbsorptionItem` equipped,
  `CheckDamage` finds no context and no value and returns having done nothing.
- **Ordering:** two other patches touch `AOS.cs` (`AOS-set-attribute-aggregation` at ~line 507 and
  `AOS-pet-mimic-attribute-aggregation` at ~line 577), both inside
  `AosAttributes.GetValue`. This hunk is ~280 lines above both and shares no context with either,
  so the three are independent and `patch` resolves them by context in any order. **Do not move
  this hunk down into `GetValue`'s neighbourhood.**

### The failure mode this patch has that S1's do not

**The patch can keep applying while the eater silently stops working.** If upstream reroutes damage
so that something other than `AOS.Damage` deals it — or adds a path that bypasses it — the hunk
still applies, the build stays green, every tooltip still reads "Cold Eater 8%", and nothing eats
anything. That is precisely the case S4's route exists for.

`ColdDamageThroughAosDamageReachesTheEater` is the test that catches it. **It was proved to fail**:
`apply-patches.sh` was temporarily changed to skip the patch, and the gated build reported
`Failed: 1` with the message the assertion carries, `AOS.Damage did not reach
DamageEaterContext.CheckDamage — the damage hook is gone`. The change was reverted and the build
re-run green. A gate that has never been seen to fail is not a gate.

### What a bump does **not** have to reconcile

- **No upstream serialization version is bumped**, so no upstream migration JSON is ours.
- **No upstream class gains a field.** `SAAbsorptionAttributes` extends `BaseAttributes`, which
  ModernUO already ships; `AosAttributes` and `AosArmorAttributes` extend it the same way. Nothing
  about `BaseAttributes` changes.
- **No core-project patch.** `Projects/Server` is untouched by S6.
- The new `[SerializableField(11)]` on **our own** `BaseSetArmor` is appended at version 0. The
  generator writes a save-flag bit per field and skips a field whose bit is clear, so a
  `BaseSetArmor` saved before S6 deserializes with the default and no migration is needed. Proved
  by `AbsorptionSurvivesASerializationRoundTrip`.

### Specific upstream churn to check, from `docs/upstream-watch.md`

- **OPL revision hash collisions, PR #2615.** S6 adds up to twelve property lines to an item's
  tooltip (`SAAbsorptionAttributes.GetProperties`, clilocs 1113593-1113598 and 1113691-1113696).
  The same caution `upstream-watch.md` raises for S1's set-bonus lines applies here, with more
  lines. After a bump that crosses #2615, confirm an Aloron piece still hashes and refreshes.
- **`BaseCreature` to the SerializationGenerator, and #2592 `SpeedClass`.** S6 touches no creature
  and needs none, so neither affects it. Noted so nobody re-derives that.
- **`AOS.Damage` itself is not in any work item listed on `upstream-watch.md`** as of 2026-09-07.
  That is a hypothesis about intent, not evidence; the test is the evidence.

### Bump checklist for S6

1. `docker/uo/build.sh` — a failed patch fails step 1, a failed test fails step 2.
2. If `AOS-damage-eater-hook.patch` fails, re-derive against the tail of `AOS.Damage`; assumption
   list above.
3. If it **applies** but `ColdDamageThroughAosDamageReachesTheEater` fails, damage has been
   rerouted around `AOS.Damage`. That is the expensive case: find the new path and move the hook.
4. If `AbsorptionSurvivesASerializationRoundTrip` fails, the generator's treatment of appended
   fields changed — check `BaseSetArmor` first, `SetStateSurvivesASerializationRoundTrip` too.

---

## 4. What was built

### Additive — 2 files, 744 lines

| File | Lines | What |
|---|---|---|
| `server/customizations/SAAbsorptionAttributes.cs` | 342 | The `SAAbsorptionAttribute` enum (ServUO `Misc/AOS.cs:2726-2751`), `SAAbsorptionAttributes : BaseAttributes` (`:2753-3058`), the `IAbsorptionItem` interface, the aggregation walk, and the twelve-line tooltip block lifted from ServUO `BaseArmor.GetProperties:2905-2939`. Lands in `Projects/UOContent/Misc/`. |
| `server/customizations/Abilities/SAPropEffects.cs` | 402 | `EffectsType`, `PropertyEffect`, `DamageType`, `DamageEaterContext`. The damage-eater slice of ServUO's 768-line file. |

### Changed — our own files

- `Items/Artifacts/Equipment/Armor/Sets/BaseSetArmor.cs`: implements `IAbsorptionItem`, gains
  `[SerializableField(11)] _absorptionAttributes` and emits the tooltip block. +31 lines.
- The eight Aloron pieces: `AbsorptionAttributes.EaterCold = 2;` restored, replacing the two-line
  omission comment S1 left. **Counted, not assumed**: `grep -c EaterCold` over ServUO's
  `Alorons Set/` returns 1 for each of eight files, all at line 23.

### Patched upstream — 1 file, 16 added lines, 0 changed lines

`server/patches/AOS-damage-eater-hook.patch`, registered in `apply-patches.sh` after
`PlayerMobile-fountain-luck-bonus.patch`. §3 is the whole of it.

### Tests — 1 file, 6 facts

`server/tests/Items/Artifacts/Equipment/Armor/Sets/AbsorptionAttributesVerification.cs`.

### The design decision, and why it is S1's

ServUO carries `SAAbsorptionAttributes` on `BaseArmor`, `BaseWeapon`, `BaseJewel` and
`BaseClothing`, and reads it back through `RunicReforging.GetSAAbsorptionAttributes`, a four-branch
type test. Putting a field on those four ModernUO classes would bump four upstream serialization
versions and make four upstream migrations ours forever — the failure S1 was built to avoid.

So **the type test becomes an interface test**: `IAbsorptionItem`, implemented by content of ours,
with the aggregation walking `m.Items` and testing `is IAbsorptionItem`. Behaviourally identical
for every item that carries the property, and the only difference is that a *stock ModernUO* item
can never have an eater. Nothing is lost: **ModernUO's loot generator has no absorption property to
roll**, so no stock item ever would have. `StockArmourEatsNothing` pins that.

Note S3 said the property must reach five base classes including `BaseTalisman`. **It is four.**
ServUO's own reader has no talisman branch (`RunicReforging.cs:2767-2779`), even though two talisman
artifacts set the property — so on ServUO those two talismans' eaters do not aggregate either. Not
our bug and not ours to fix; recorded so nobody ports a talisman carrier expecting it to work.

---

## 5. Verification

Headless throughout. No client, not on Chase's machine, `--network=none` on every container,
scratch save directory under `%TEMP%\claude\s6run`, scratch `Configuration` with
`listeners: ["127.0.0.1:2593"]` and autosave off. Nothing touched the live stack, `Saves/`,
`Accounts/`, or the uncommitted `docker-compose.yml` (Q-009). No deploy; nothing started or
restarted.

### Gated build

`docker/uo/build.sh -t sl-modernuo:s6` — **green end to end**. 83 structured customizations, 4
shard test files, **14 patches applied**, **20 tests passed**, `sl-modernuo:s6` built, exit 0. No
warning from any file of ours; the build's one warning (NETSDK1194, `--output` on a solution) is
pre-existing and upstream.

Two build-fix cycles were needed, both the same mistake and worth naming: **C#'s "Color Color" rule
bit twice.** `PropertyEffect` has an instance property `Timer` and a static property `Effects`, and
inside `DamageEaterContext` those shadow the `Server.Timer` and `Server.Effects` **types**.
`Effects.SendPacket(...)` failed with `CS1061: 'List<PropertyEffect>' does not contain a definition
for 'SendPacket'`. Both call sites are now written `Server.Timer.` and `Server.Effects.` with a
comment. ServUO gets away with the bare names because it inherited them; we should not copy that.

### The six tests

| Test | What it pins |
|---|---|
| `AloronPiecesCarryTheirColdEater` | `EaterCold == 2` on a piece, `EaterFire == 0`, and the piece is an `IAbsorptionItem`. This is A5 itself. |
| `AbsorptionAggregatesAcrossEquippedItems` | Four worn pieces sum to `EaterCold == 8`; `DamageEaterContext.GetValue(DamageType.Cold, m) == 8`; fire stays 0. Per-piece, not a set bonus — ServUO puts `EaterCold` on the piece, not in `SetAttributes`. |
| `StockArmourEatsNothing` | A stock `LeatherChest` is not `IAbsorptionItem`, aggregates 0, and creates no context. |
| **`ACompletedAloronSetEatsColdDamage`** | **The proof asked for.** A player in a completed Aloron set, hit for 100 pure cold, is healed for exactly **8** three seconds later. |
| **`ColdDamageThroughAosDamageReachesTheEater`** | **The patch.** `AOS.Damage` creates a `DamageEaterContext` on an eater-wearing victim and none on a victim in stock armour. Proved to fail with the patch skipped. |
| `AbsorptionSurvivesASerializationRoundTrip` | `EaterCold`, `EaterFire` and `CastingFocus` survive `Serialize`/`Deserialize` on `BaseSetArmor` field 11. |

**Why the heal is measured in one test and the patch in another, rather than both at once.** The
first version of `ColdDamageThroughAosDamageReachesTheEater` asserted on hit points after driving
`AOS.Damage`. It failed with `healed=40 expected=3`: `Mobile.Damage` starts `Mobile.HitsTimer`,
which does `Hits++` per tick and re-arms, and `Timer.Slice` turns the wheel without advancing
`Core.Now`, so four seconds of wheel restored the entire 40-point hit. **Regeneration, not the
eater.** `ACompletedAloronSetEatsColdDamage` avoids it because it never calls `Mobile.Damage` and
`Timer.Init(0)` clears the wheel before the only timer that matters is scheduled. Splitting the two
leaves both halves deterministic and the chain covered end to end. **Worth knowing before anyone
writes another timer-dependent test on this route:** `Timer.Slice` advances the wheel, not the
clock, and any test that damages a mobile and then slices is measuring regeneration.

### Runtime, real server

`sl-modernuo:s6`, `--network=none`, scratch everything: server started, loaded map definitions and
371 regions, ran every ClusterF seeder, loaded the world (618 items, 90 mobiles), and reached
`Listening: 127.0.0.1:2593` with **no exceptions**. Container removed afterwards.

**What that run does and does not prove.** It proves the assembly with two new types and a changed
`BaseSetArmor` loads and a world builds on it. It does **not** exercise field 11 in a real save,
because no `BaseSetArmor` instance exists in the seeded world — the console has no way to create an
item without a client, and `save`/`shutdown` cannot be driven over piped stdin (the console reader
wants a tty; S4 hit the same wall). Field 11's round trip is proved by test instead. Stated rather
than glossed.

---

## 6. What "57 unblocked" actually means, now that it is built

S3's list is **57 files and 57 lines long** — the count and the list agree, which after this
project's record is worth saying. All 57 exist on disk in `D:\UO\ServUO-pub57\Scripts`; verified.

But **57 is a reference count, not a port-now count**, and nobody has drawn that distinction
before. Classified by what each file actually needs, reading its base class:

Classified by resolving each file's declared base class through ServUO's own inheritance chain —
scripted, not eyeballed, and the groups sum to 57:

| Group | Files | State after S6 |
|---|---|---|
| **The eight Aloron pieces** | **8** | **Done.** Already in our tree, now complete. A5 closed. |
| The five Darden set pieces | 5 | **Carrier-ready.** `BaseSetArmor` gives them both the set state and the eater. They still need `SetItem.Darden` content and the `DragonTurtleHide*` armour they derive from — content work, no subsystem. |
| `BaseArmor` descendants (11) and `BaseShield` descendants (4) | 15 | One `BaseAbsorptionArmor` covers both: ServUO's `BaseShield : BaseArmor` (`Items/Equipment/Armor/BaseShield.cs:6`). Not built; see below. |
| `BaseWeapon` descendants | 6 | Need a `BaseAbsorptionWeapon`. |
| `BaseClothing` descendants | 4 | Need a `BaseAbsorptionClothing`. |
| `BaseJewel` descendants | 3 | Need a `BaseAbsorptionJewel`. |
| `BaseTalisman` descendants | 2 | Need a carrier — **and would not aggregate even on ServUO**, per §4. |
| `Items/Artifacts/DespiseArtifacts.cs` | 1 | One file declaring armour, clothing, jewellery **and** a weapon. Needs four of the carriers, so it is the last of these to become portable, not the first. |
| Blocked by a *different* missing subsystem | 13 | `Enhancement.cs`, `EnhancementTimer.cs` (both dead code even in ServUO), `SAPropEffects.cs` (partly ported here), the Mannequin property, the four LootGeneration files (Imbuing, `ItemPropertyInfo`, `ItemPropertiesGump`, `RunicReforging`), both Vendor Searching files (B11), `VvVChests` (B13), `SkillMasterySpell` (B12), Shadowguard `Artifacts.cs` (B10). **These were never absorption-blocked.** |

8 + 5 + 15 + 6 + 4 + 3 + 2 + 1 + 13 = **57**.

Two entries are filed under a directory that misleads and are worth naming, because a future batch
picking "the jewellery ones" from paths would get them wrong: `Equipment/Jewelry/DragonJadeEarrings.cs`
and `Equipment/Jewelry/ObsidianEarrings.cs` both derive from `GargishEarrings`, which is `BaseArmor`
in ServUO, not `BaseJewel`. Likewise three files under `Equipment/Armor/` — `MantleOfTheFallen`,
`SpinedBloodwormBracers`, `SummonersKilt` — are `BaseClothing`. The table above is by resolved base
class, not by folder.

**So the honest ratio for S6 is not 57:1.** It is: 8 files finished, 5 made carrier-ready, 31 more
one small class away each, and 13 that were counted against the wrong subsystem. That is still
good value for 744 lines and one patch — the carriers are cheap and each unlocks a group — but
"57 files unblocked" would be the sixth count this project quoted without checking what it meant.

### Why the four extra carriers were not built

The brief said: repeat S1's shape, one additive file plus one damage hook, and **stop and say so**
if it starts wanting more. It did not want more — the shape held exactly — and four more carrier
classes is more. It is also precisely the boundary S1 drew: `notes/s1-armour-sets.md` §8 defers
`BaseSetWeapon`, `BaseSetJewel`, `BaseSetClothing` and `BaseSetQuiver` for the same reason.

**Each is small and none needs a patch.** A carrier is: derive from the ModernUO base class, add
one `[SerializableField]`, implement `IAbsorptionItem`, call
`SAAbsorptionAttributes.GetProperties` in `GetProperties`. `BaseSetArmor`'s delta was 31 lines and
most of that was documentation. `IAbsorptionItem`, the aggregation and the patch are all
kind-agnostic and need no further change. **They should be built with the first batch of content
that needs them**, not speculatively, and the batch and the carrier belong in the same task.

---

## 7. Deviations — deliberate, for `docs/fidelity-principle.md`

Three, all omission rather than approximation, per "prefer turning a system off over running it
differently".

### D6-1. `GetValue` drops its `Enhancement` and `SkillMasterySpell` terms

Both verified to contribute **exactly zero to any Eater or Resonance attribute in ServUO itself**
— §1 has the evidence. This is a deviation on paper only: no value reachable in ServUO is
unreachable here. If Skill Masteries is ever built, add the term back for `CastingFocus`.

### D6-2. Eight of ServUO's nine `PropertyEffect` kinds are absent

Only `DamageEaterContext` came across. Soul Charge, Splintering, Searing, Bane, Bone Breaker,
Swarm, Sparks and Battle Lust are weapon properties belonging to systems this shard does not have,
and each drags in more. The `EffectsType` enum keeps all nine members so a later port is additive
rather than a renumbering. **No item in our tree sets any of the eight**, so nothing is degraded.

### D6-3. The absorption tooltip block sits a few lines lower than ServUO's

ServUO emits it inside `BaseArmor.GetProperties`, between the soul-charge and spell-channeling
lines. ModernUO's `BaseArmor` offers no hook there and patching one in would buy ordering and
nothing else, so `BaseSetArmor.GetProperties` emits it after `base.GetProperties(list)`. Same
twelve clilocs, same order within the block, a few lines lower in the tooltip. Cosmetic, and the
identical judgement as S1's D-4.

**Not a deviation, listed so it is not re-raised:** the eaten-damage particle effect is byte-identical
to ServUO's. ModernUO's `Effects.SendTargetParticles` helper hardcodes `fixedDirection: true` and a
different explode effect, so the packet is built through the public
`OutgoingEffectPackets.CreateParticleEffect` instead, with ServUO's arguments verbatim.

---

## 8. Corrections to earlier documents

For Chase to log on review; `docs/` is not mine to edit.

1. **`docs/gap-register.md` A5 and `notes/s3-decline-costs.md` §6 both describe the eater as
   reducing damage.** It heals, three seconds later. §2. S3's suggested test — "damage taken with
   an eater item equipped is reduced" — would have asserted something that never happens.
2. **`notes/s3-decline-costs.md` §6 says the property must reach five base classes including
   `BaseTalisman`.** ServUO's own reader has four branches and no talisman branch. §4.
3. **`docs/gap-register.md` B1 says "1 damage hook" under *Upstream files patched*.** Correct, and
   worth keeping: S6 shipped with **one** `UOContent` patch and **no core patch**, making it
   cheaper on a bump than S1.
4. **The "57 unblocked" figure is a reference count.** §6 breaks it down. The list and the count
   agree at 57 — S3 measured honestly — but 13 of the 57 are blocked by other subsystems and were
   never absorption's to unblock.

---

## 9. What it cost

| Phase | Wall clock |
|---|---|
| Read `AGENTS.md`, `docs/subsystem-policy.md`, `docs/gap-register.md`, S6 in `docs/tasks.md`, `notes/s1-armour-sets.md`, `notes/s4-test-route.md`, `docs/upstream-watch.md` | ~9 min |
| Source study: ServUO `SAAbsorptionAttributes`, `SAPropEffects`, the `AOS.Damage` call site; **verifying all three dependency claims in ServUO** | ~11 min |
| Checking every type and signature against `D:\UO\ModernUO-pinned` before writing a line — `BaseAttributes`, `IPropertyList.Add`, `Timer.DelayCall`, `Timer.Slice`, `Mobile.Heal`, `Effects.SendPacket`, `OutgoingEffectPackets`, `Core.SA`, `World.Loading`, name collisions | ~8 min |
| Write the two files, the patch, the `BaseSetArmor` delta, the eight Aloron lines | ~10 min |
| Write the tests | ~7 min |
| Four gated build cycles: two compile fixes, one test fix, one green | ~13 min |
| **Negative proof: skip the patch, watch the test fail, revert, re-run green** | **~6 min** |
| Runtime smoke run | ~6 min |
| Classifying the 57 and writing this file | ~12 min |
| **Total** | **~82 min** |

**Two things are worth carrying forward and neither is about absorption.**

- **The Color Color rule cost both compile cycles.** A ported ServUO class whose members shadow
  ModernUO type names (`Timer`, `Effects`) compiles in ServUO and does not here, or worse, compiles
  and resolves to the wrong thing. Qualify them.
- **`Timer.Slice` advances the wheel, not the clock.** Any test that damages a mobile and then
  slices is measuring hit regeneration. This is the first timer-dependent test on the S4 route and
  it will not be the last.

The S1 lesson held again: checking every type against `ModernUO-pinned` first meant the two
compile errors were both this one C# subtlety, not a single missing API.

---

## 10. What S6 leaves for later

- **The carrier classes** — `BaseAbsorptionArmor` (which covers shields too), `BaseAbsorptionWeapon`,
  `BaseAbsorptionClothing`, `BaseAbsorptionJewel`, and a talisman carrier that would be inert. §6.
  Build each with the content batch that needs it.
- **The Darden set**, which now needs only content: `SetItem.Darden`, the `DragonTurtleHide*`
  armour, and the five pieces. It is also blocked on A6 (`SlayerName.Myrmidex`) for its set slayer,
  exactly as Aloron is for Dinosaur.
- **A6 is unchanged by S6.** The Aloron set still has no Dinosaur Slayer, effect or tooltip. A5 is
  closed; A6 is not, and the two were separate deviations in `notes/s1-armour-sets.md` for a
  reason.
- **`docs/gap-register.md` A5 can be marked closed**, with the §2 wording correction.
- **Nothing here needed a `BaseCreature`**, so **Q-026 / D1 was not touched and did not bite.** The
  brief asked me to say if I needed one: I did not. `PlayerMobile` is constructible in the fixture
  and is the right victim for a damage test anyway.
