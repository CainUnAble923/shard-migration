# Bug list: defects to look at fixing

Distinct from `patch-backlog.md`, which is about capability ModernUO does not have. This file is
about things that are **wrong**: ours, ServUO's, and ModernUO's.

**The rule that governs most of this file**, set by S2's D-4 and followed since:

> A ServUO bug that produces a *missing* result is copied faithfully. Fixing it would hand our
> players behavior no OSI or ServUO player gets, which is a fidelity deviation in the direction
> nobody thinks to check a wiki for. A ServUO bug that produces a *broken* result is fixed.

"Missing" means a branch never fires, a drop never rolls, a name reads oddly. "Broken" means the
game shows the wrong thing or a player cannot proceed. D-10, D-16 and D-46 are the three fixes; §3
is everything left alone.

---

## 1. Open, ours, worth fixing

| # | What | Impact | Where |
|---|---|---|---|
| **Q-009 / D3** | `docker-compose.yml` carries an **uncommitted change** repointing the live script mount at `server/customizations` read-only. Directionally right, never verified, deploy-affecting | live shard | **CHASE decides.** Oldest open item on the project |
| **D4** | **Build cost is 6x the published estimate.** 20s unchanged, 266s with one changed file, against `cc2-timed-port.md`'s 0:44 which predates S4 and neither compiled nor ran tests | every batch estimate is optimistic | fix the estimate, not the build |
| **D6** | The runtime image ships **16 test-infrastructure assemblies of 53**, because the Dockerfile publishes `ModernUO.slnx` | inert, cosmetic | Q-032. **The trap:** that same publish line is the compile gate. Any fix must lose the test assemblies *and* still fail the build on a deliberately broken test |
| **D5** | `server/uo/` build tree is stale and predates the F1 recovery | confusing, not harmful | leave; gitignored and generated |
| **new** | **`progress.py` and `build.sh` disagree on the test count**: 69 by `[Fact]` count in 16 files, 68 run by the gate. Disclosed in CC6 batch 2's commit, cause not chased | a reported number nobody can reproduce exactly | find the one test and make the two agree, or document why they cannot |
| **D2** | ModernUO has no `Quest.StartingItem` equivalent. **How many of the 203 quests need one is unmeasured** | blocks an unknown slice of the quest row | Q-025, measure before the quest batch |

## 2. Fixed, kept so the cause is not re-learned

| # | What it was | Cost |
|---|---|---|
| D7 | A fresh test world blocks on `AccountPrompt` forever. No accounts means `ConsoleInputHandler.ReadLine()` on stdin: `docker ps` says Up, the listener never opens, the client hangs at "verifying account". The prompt fires at container start, so attaching later shows nothing to answer | **a week** |
| D8 | The test shard relayed clients onto the **live** shard. `Configuration-test` copied the live config, which advertises `192.168.1.58` with `autoDetect` false | a test session could silently run against live |
| D9 | `docker-compose.yml` mounted the **live world save**, so testing wrote into the real world | one stray account reached the live save before this was caught |
| D10 | `MAKE X` label invisible: `AddLabel` given `0x7FFF`, an RGB555 color, where a hue index belongs | open since June; affected the **live** shard |
| S8/D1 | The test route could not construct any `BaseCreature`. **The cause first recorded here was wrong** (Q-031): the data file was in the test output all along. Nothing called `NPCSpeeds.Configure` | a wrong diagnosis that survived a week |

**The pattern in D7 through D9, worth naming:** three of the four were *test rig* defects that made
the rig quietly point at production. None was found by reasoning; each was found by asking the
machine. The week D7 cost was spent on four plausible fixes applied without first probing whether
the thing being fixed was the thing that was broken.

## 3. ServUO behavior copied on purpose — do not "fix" these

Every one of these reads like a typo and is ServUO's. They are here so the next reader does not
correct them, and so that if we ever change the rule we know what the list is.

**Unreachable branches and dead rolls**

- `ToxicSlith`'s drop switch rolls `Utility.Random(2)` over cases 0 and **2**, so the `SlithEye`
  branch never fires: a toxic slith drops a venom sac 2.5% of the time and never an eye.
- The fountain's buff branch rolls `Utility.Random(4)` over a **six**-case switch, so special
  protection and balm boost never fire (S2 D-4, the precedent for this whole section).
- `LowlandBoura.OnDeath` says `if (Controlled) return;` and then `if (!Controlled)`.
- `Race.RandomFacialHair(this)` returns an int and discards it on both emulators. It has never
  assigned facial hair to anyone.
- `GreenGoblinScout.OnThink` does not call the base, so no ML shout.

**Names and appearance**

- `PitFiend` is "a Pit fiend", capital P, and its header says it was copied from the daemon.
- The enslaved goblins' corpse is "an goblin corpse"; `PutridUndeadGuardian` is "an putrid undead
  guardian"; `SentinelSpider` is "a Sentinel spider".
- `EnslavedGreenGoblinAlchemist` is named "Green Goblin Alchemist" with no "Enslaved", and wears
  the free goblins' body 723 while its five siblings wear 334.

**Values that look wrong**

- `ClanRibbonPlagueRat` sets `Tamable = false` with a `MinTameSkill` of **−0.9**.
- `EnslavedGoblinMage` is a melee creature with 510 Int and no Magery.
- `LavaElemental`, `GargoyleShade`, the three sliths, `Gremlin`, `TrapdoorSpider`, `Skree` and
  `UndeadGuardian` set no Fame or Karma. `ForgottenServant` has no `[CorpseName]`.
- `GargoyleShade` has no Energy resistance.

## 4. ServUO bugs we did fix, and why each cleared the bar

| # | What | Why it is "broken", not "missing" |
|---|---|---|
| D-10 | `GargishWarHammer` flips to `0x48C1`, not ServUO's `0x481` | `0x481` is a Prism of Light **pillar** graphic. Every other gargish weapon flips to itemID+1. ServUO's value turns a flipped war hammer into a pillar |
| D-16 | `DarkwoodCrown` flips to `0x3168`, not `0x3169` | `0x3169` is the flipped Vulture Helm. Same shape |
| D-46 | `ShameWall` sets `Visible = true` in its constructor | ServUO leaves `BaseAddon`'s `false`, so a fresh wall's teleporters are inert and **a player cannot push through it** until that wall's troll has died once (Q-046) |

## 5. ModernUO upstream

| # | What | Evidence | Disposition |
|---|---|---|---|
| **E1** | **`SetPassword` stores an unverifiable hash under SHA1/SHA2.** `_passwordAlgorithm` is still the enum default at the first `SetPassword`, so the phrase choice and the stamped algorithm disagree and `CheckPassword` can never match. With auto-account-creation on, a new player logs in once and never again | proven three ways in P1: the stored hash was exactly `SHA512("p1testpass")`, a packet capture confirmed correct credentials, and rewriting the hash to `SHA512("p1adminp1testpass")` fixed login immediately | **report upstream.** Costs us nothing now; the SHA2 block is reverted |
| **E2** | ModernUO has **no armour set-bonus system**. Standard OSI content. We built it in 387 lines plus three small patches | S1, five passing tests, 111 files unblocked | **contribute upstream.** If taken, our maintenance on the highest-value thing we have built drops to zero |

---

## Keeping this file honest

- A defect found during a task goes in that task's `notes/` file first, with what proved it. It is
  promoted here in review.
- **A fix is not a fix until a test has been watched go red without it.** `AGENTS.md` requires the
  red proof and this file assumes it.
- Anything in §3 that a player actually complains about moves to §1 with their complaint attached.
  The rule in the banner is a default, not a verdict.
