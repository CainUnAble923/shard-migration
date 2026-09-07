# Gap register: everything declined, degraded, or left broken

**One place for every gap, with what a player notices and what closes it.** Compiled 2026-09-07
from `docs/fidelity-principle.md`, `docs/subsystem-policy.md`, `notes/s3-decline-costs.md`
(the measured menu), and the S1, S2, S5 and CC3 notes.

**Nothing here changed anything a player already had.** The shard as it ran before this project
is untouched. Every entry is on content added since, or a gap in content not yet added.

Three dispositions, and every row has one:

- **OURS** — additive `.cs` plus targeted patches in our own tree. The normal path.
- **UPSTREAM** — worth offering to ModernUO, because it is standard OSI content or a real
  upstream defect. Ours to maintain until they take it, if they ever do.
- **WON'T** — declined with its ratio recorded, revisitable when the surrounding content changes.

---

## A. Live gaps a player can notice

Ordered by how likely someone is to hit it. Every one traces to section B.

| # | What a player sees | Root cause | Closed by | Disp. |
|---|---|---|---|---|
| A1 | **A tamed `Dimetrosaur` is stronger than it should be.** ModernUO has no `OnAfterTame`, so `AnimalTaming`'s `ScaleStats(0.50)` applies instead of ServUO's Hits/4 | Pet Training | B2 | OURS |
| A2 | **`Saurosaurus` has no Tail Swipe and no Life Leech**, 2 of its 3 abilities | `SetSpecialAbility` | B2 | OURS |
| A3 | **`Dimetrosaur` has no poison breath area attack** | `SetAreaEffect` | B4 | OURS |
| A4 | **Six dinosaurs lose `AttacksFocus`** and use normal `FightMode` targeting | Pet Training | B2 | OURS |
| ~~A5~~ | ~~A completed Aloron set gives no cold-damage eating~~ **CLOSED 2026-09-07 by S6.** Note the mechanic is a **capped delayed heal**, not damage reduction: `DamageEaterContext.OnDamage` calls `DelayHeal`. My original wording here said reduction and was wrong (Q-027) | — | S6 | **DONE** |
| A6 | **The Aloron set has no Dinosaur Slayer**, effect and tooltip both. Tooltip omitted deliberately: a slayer line that does not slay is worse than no line | `SlayerName` lacks `Dinosaur`/`Myrmidex` | small additive enum + patch | OURS |
| A7 | **Queen Zhah is undressed.** All seven of her gargoyle items are absent from ModernUO | missing items | leaf ports | OURS |
| A8 | **`Archaeosaurus` and `Saurosaurus` give no dragon blood when carved** | property and item both absent | leaf port | OURS |
| A9 | **The Fountain of Fortune is not placed**, so `LuckyCoin` only ever shows its failure message | nothing calls `MoveToWorld` | **Q-021: Ter Mur `(1121, 957, -42)`, three lines** | OURS |
| A10 | S5's `MinionOfScelestus` loses `SetSpecialAbility` and `TaintedLifeAura` | Pet Training | B2 | OURS |

**A1 is the one I would fix first for feel.** A *buff* is worse than a loss: a player reading
UOGuide will not notice a number that is wrong in their favour, so it never gets reported and
never gets fixed.

**A9 is the cheapest win on the page.** Three lines, and it turns a ported cluster from
unreachable into reachable.

### Cosmetic only, listed so nobody re-opens them

The fountain's luck bonus showing in the status bar where ServUO hides it (the cheaper patch was
also the more robust one); property-list ordering in the set block; `RaptorClaw.IsArtifact` and
`SolesOfProvidence.IsArtifact`, both ServUO-only virtuals with zero readers in ModernUO;
`SetSelfRepair` using ModernUO's self-repair formula, where the two emulators already differed.

### Closed already

- **`LuckyCoin.OnDoubleClick`** — restored by S2 across all twelve coin droppers, pinned by a
  test. The original decline rested on a factual error: `EnchantedEssence` and `RelicFragment`
  are leaf items, not Imbuing dependencies.

---

## B. Subsystems ModernUO does not have

Measured in S3 against pinned `7c9215d97`. **Unblocked** is files we would gain, after removing
types ModernUO already declares. Full method and file lists in `notes/s3-decline-costs.md` §3.

| # | Subsystem | Cost | Unblocked | Ratio | Upstream files patched | Fits layering | Disp. |
|---|---|---|---|---|---|---|---|
| ~~B1~~ | **`SAAbsorptionAttributes`** — **BUILT by S6.** 744 additive lines, **one** upstream patch (`AOS.cs`, 16 added, 0 changed), no core-project patch, no serialization version bumped | actual: **8 finished, 5 carrier-ready** | — | 1 | Yes | **DONE** |
| B2 | Pet Training, `SpecialAbility` group | 4 / ~4,100 | 53 | ~13:1 | 6 + `AOS.Damage` | Yes | **WAIT** (2026-09-07) |
| B3 | Pet Training, `MagicalAbility` group | slice of B2 | 18 | — | same | Yes | **WAIT** |
| B4 | Pet Training, `AreaEffect` group | +1 / 596 | 17 | — | same | Yes | **WAIT** |
| B5 | Pet Training, gate + profiles + gumps | 6 / ~4,050 | 11 | **~2:1** | +6 more | Yes, **poor value** | WON'T for now |
| B6 | *Pet Training, all four* | *11 / 8,664* | *79* | *~7:1* | *17* | — | — |
| B7 | **`Services/PointsSystems`** | 12 / 2,857 | **55** | ~4.6:1 | — | Yes | **OURS — queued as S7.** Hard dependency of B9 and B13 |
| B8 | Myrmidex Invasion | 6 / 2,197 | 9 | ~1.5:1 | 2 | Yes | WON'T for now |
| B9 | City Loyalty | 28 / 8,177 | 15 | ~0.5:1 | 11 | Yes, wide | WON'T, gated on B7 |
| B10 | Shadowguard | 14 / 11,222 | 8 | ~0.6:1 | 4 | Yes | WON'T |
| B11 | Vendor Searching | 4 / 2,545 | 5 | ~1.2:1 | 5 | Marginal | WON'T |
| B12 | **Skill Masteries** | 45 / 8,542 | 14 | ~0.3:1 | **35** | **No** | **WON'T — strongest decline.** 35 upstream patch points against a `BaseCreature` upstream is actively refactoring. Fails questions 2 and 3 of `subsystem-policy.md` at once |
| B13 | Vice vs Virtue | 57 / 9,613 | 5 | ~0.1:1 | 21 | Marginal | WON'T |
| B14 | Instanced Peerless | 13 / 1,543 | 2 | ~0.15:1 | 2 | **No base to instance** | WON'T |
| B15 | Exploring the Deep | 70 / 10,292 | 2 | ~0.03:1 | 1 | Yes | WON'T |
| B16 | ServUO's ML quest framework | 22 / 6,269 | (176) | — | — | — | **WON'T — wrong question.** ModernUO already ships `Engines/ML Quests`: 109 files, 240 quests. Two engines for one job. The *quests* are section C |
| — | *armour sets, S1, built* | *1 / 387 + 3 patches* | ***111*** *(124 including absorption-blocked)* | *~111:1* | *3* | *yes* | **UPSTREAM candidate** |

**B1 is the best ratio on the board and it closes A5.** It is queued.

**Pet Training is the one real decision left.** B2 through B4 close A1 through A4 and A10, which
is most of section A. B5 is the expensive half and buys almost nothing. **Buying B2-B4 without
B5 is the shape to aim for**, and S3 measured them separately for exactly that reason.

---

## C. Content declined, or not yet reachable

| # | What | Size | Disp. |
|---|---|---|---|
| C1 | **164 of the 203 missing ML quests translate mechanically.** One standard objective type each. The mapping holds for 4 of 5 types, verified by S5 | 164 quests | **OURS — a real content batch, unscheduled** |
| C2 | **39 quests hand-write a `BaseObjective` subclass**, 25 of them a class called `InternalObjective`. My brief set aside `QuestionAndAnswerObjective`, which is only **2** of the 39. **The tail is 12.5x the thing I was looking at** | 39 quests | OURS, needs its own decision |
| C3 | **Valley of One** — reopened by S5, but a **poor first batch**: 3 of its 7 quests need a hand-written objective, against 19% across the 203 | 7 quests | OURS, not first |
| C4 | **Myrmidex Threat quest line** | 10 quests | OURS, gated on B8 |
| C5 | The eight **Aloron pieces** and the **TigerPelt set** | done | **CLOSED by S1** |
| C6 | `MoonstonePowerGenerator` — Myrmidex content, reached the CC3 list because "moonstone" matched a keyword | 1 file | WON'T, gated on B8 |
| C7 | **The unmeasured rows.** Revamped Dungeons at 255, artifacts at 466, decoration at 297 are all *unfiltered* counts. The creatures row went 462 → 137 when filtered. These are plausibly inflated by a similar factor | unknown | **Measure before scheduling** |

---

## D. Our own defects and infrastructure gaps

| # | What | Impact | Disp. |
|---|---|---|---|
| ~~D1~~ | ~~The S4 test route cannot construct any `BaseCreature`~~ **CLOSED 2026-09-07 by S8.** **And the cause I recorded here was wrong** (Q-031): the data file *was* in the test output all along, since `UOContent.Tests.csproj` copies 272 files there. Nothing ever called `NPCSpeeds.Configure`, because `UOContentFixture` uses a hand-picked list. Missing call, not missing data, and the two point at different fixes | — | S8 | **DONE** |
| D2 | **ModernUO has no `Quest.StartingItem` equivalent.** How many of the 203 need one is genuinely unmeasured | unknown, blocks some quests | OURS, measure. Q-025 |
| D3 | **`docker-compose.yml` has an uncommitted change** repointing the live script mount at `server/customizations` read-only. Directionally right, unverified, deploy-affecting | live shard | **CHASE.** Q-009 |
| D4 | **Build cost is 6x what the estimate says.** 20s unchanged, **266s with one changed file**, against `cc2-timed-port.md`'s 0:44 which predates S4 and did not compile or run tests | every batch estimate is optimistic | fix the estimate |
| D6 | **The runtime image ships 16 test-infrastructure assemblies of 53.** Pre-existing since S4, because the Dockerfile publishes `ModernUO.slnx` | inert, cosmetic | **Recorded, not scheduled.** Q-032. **The trap:** that same publish line provides the compile gate. Any fix must lose the test assemblies *and* still fail the build on a deliberately broken test |
| D5 | **`server/uo/` build tree is stale**, missing five current customizations, and predates the F1 recovery | confusing, not harmful | leave; it is gitignored and generated |

---

## E. Upstream ModernUO defects worth reporting

| # | What | Evidence | Disp. |
|---|---|---|---|
| **E1** | **`SetPassword` stores an unverifiable hash under SHA1/SHA2.** `_passwordAlgorithm` is still the enum default at the first `SetPassword`, so the phrase choice and the stamped algorithm disagree and `CheckPassword` can never match. With auto-account-creation on, a new player logs in once and never again | Proven three ways in P1: the stored hash was exactly `SHA512("p1testpass")`, a packet capture confirmed correct credentials, and rewriting the hash to `SHA512("p1adminp1testpass")` fixed login immediately | **UPSTREAM.** Costs us nothing now (the SHA2 block is reverted) and is a real defect. `notes/cc1-p1-runtime-validation.md`, Q-007 |
| E2 | **The armour set-bonus system.** Standard OSI content ModernUO lacks. We built it in 387 lines plus three small patches | S1, plus five passing tests | **UPSTREAM candidate.** If taken, our maintenance on the highest-value thing we have built drops to zero, and the 111 files it unblocks stop being ours to keep working across version bumps |

---

### Follow-on from S6

**B1b — the carrier class.** S6's "57 unblocked" was a *reference* count. Resolved through the
inheritance chain (Q-028): **8 finished, 5 carrier-ready, 31 one small carrier class away, 13
blocked by other subsystems all along.** The **31** are a bounded, concrete follow-on rather than
a subsystem, and may be the best ratio left now that S6 has landed. **Cost it before scheduling
it** — that is the whole lesson of this row.

## Standing decisions

**2026-09-07, Pet Training: WAIT.** Not on value, on timing. It patches 6-7 upstream files
including `AOS.Damage`, and upstream is refactoring `BaseCreature` right now with `SpeedClass` an
open behaviour change. Revisit once the delta-saves project and the `BaseCreature` conversion
settle. Gaps A1-A4 and A10 stay open and logged meanwhile.

**2026-09-07, upstream contributions: not now.** E1 and E2 stay available; neither expires.

## Recommended order

**For how OSI the shard feels**, which is what section A measures:

1. **A9, place the Fountain.** Three lines. Turns a whole ported cluster from unreachable to reachable.
2. **B1 / S6, `SAAbsorptionAttributes`.** Best ratio on the board, closes A5, already queued.
3. **A7 and A8**, the missing gargoyle items and dragon blood. Leaf ports, no subsystem needed.
4. **B2-B4, the Pet Training ability groups without the gate.** Closes A1 through A4 and A10, which is the rest of section A. This is the one real decision left.
5. **A6**, the Dinosaur Slayer enum entry.

**For volume**, C1's 164 mechanically-translatable quests is the largest single unlock and needs
no subsystem at all.

**Do first regardless: D1.** The test route cannot construct a creature, and the next 137 files
are creatures.
