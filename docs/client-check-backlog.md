# Client spot-check backlog

**RUN AND PASSED 2026-09-19.** Results at the bottom. 381 ported files, thirteen checks,
**one real defect found** (MAKE X, now fixed) and **zero content regressions**. The list below
is kept as the method; the Results section is what it produced.

Everything ported since P1 is verified **structurally**: it compiles, its type registers, the
world saves and reloads, and 44 tests pass. None of it has been **looked at**. This is the list of
what a client session would actually settle.

**Chase runs the client. No agent does.** No agent can: there is no client in the sandbox, and
the check needs a server built from current source, which is a deploy decision and his alone.

## When to do this

**CC9 has landed. This is due now**, in one sitting. It covers **381 ported files** across
S1, S2, S5, S6, S10 and CC9's five batches, plus one real defect pending since P1.

**Two things to settle before you start, or two sections are wasted:**

1. **You need a gargoyle character.** Most of CC9 is gargish equipment with
   `RequiredRaces => AllowGargoylesOnly`. On a human everything below reads "you cannot wear
   that", which is correct behaviour and looks exactly like a defect. Make a gargoyle before you
   begin.
2. **Nothing places a Fountain of Fortune** (checked 2026-09-15: no placement exists in
   `server/customizations`). Section 4 cannot run. Q-021 has the coordinates and it is three
   lines. Either land it first or skip section 4 and keep it on this list.

## What only a client can tell us

Everything else has been proven headlessly. These four things have not, and cannot be:

1. **Does it look right.** Body, hue, animation, item art. A wrong `body` value renders as an
   invisible or nonsense creature and compiles perfectly.
2. **Do gumps render.** Layout, overlap, and whether text is actually visible.
3. **Does the interaction complete.** A quest offered and finished, a fountain used, a bandage
   applied.
4. **Do the property tooltips read correctly** in-world, not just in a test assertion.

## The checklist

### 1. The one real defect, pending since P1

**MAKE X button label is invisible.** The patch passes `LabelColor`, an RGB555 value, to
`AddLabel`, which wants a hue index. Diagnosed in P1, never fixed, and it affects the **live
shard today** rather than any ported content. The button works and its position is fine.
**Confirm it, then it is a one-line fix.** This is the oldest item here and the only one that is
a bug rather than an unknown.

### 2. Creatures: do they look like creatures

`PlagueRat`, `GreaterPoisonElemental`, and the seven Eodon creatures (`Allosaurus`,
`Archaeosaurus`, `Dimetrosaur`, `Najasaurus`, `Saurosaurus`, `SilverbackGorilla`, `Raptor`), plus
`MinionOfScelestus`.

`[add <name>` each one. Looking for: correct body, correct hue, sane size, no invisible mobs.
Bodies and hues were carried across verbatim, so this is expected to pass, and it is exactly the
class of error a compiler cannot see.

### 3. Armour sets and absorption, S1 and S6

Equip a full **Aloron set**. Expect the set bonus to apply, the property list to read correctly,
and a completed set to eat cold damage. Note the mechanic is a **capped delayed heal** three
seconds after the hit, **not** damage reduction, so watch health recover rather than watching a
smaller number.

Also check the **TigerPelt** armour renders correctly. It was ported as ordinary armour after
CC3 recorded it as set content, which it is not.

### 4. Fountain of Fortune, S2 — blocked

**Nothing places a fountain yet**, so `LuckyCoin` can only ever show its failure message. Q-021
answers it: the OSI coordinates are Ter Mur `(1121, 957, -42)`, three lines of placement. **That
should land before this check**, otherwise there is nothing to look at.

Then: double-click a `LuckyCoin` at the fountain and confirm the reward loop and the luck bonus.
The luck bonus **shows in the status bar**, where ServUO hides it. That is a known deviation, not
a bug.

### 5. The Athenaeum Isle quest, S5

Take it from its quester, complete both objectives, and collect the reward. This is the one item
where the *headless* result is weakest: the objective mapping was proven by test, but "a player
can be offered this quest and finish it" was never observed.

### 6. CC9, 381 files — run it in four tiers, not file by file

The risk is uniform in *kind* (wrong art, wrong hue, missing property line) but it is not uniform
in *consequence*. Work down these tiers and stop when you run out of patience; tier 1 is twelve
minutes and settles the things nothing else can.

**Tier 1 — the two places we overrode the source on our own judgment.** Everything else in CC9
was copied from ServUO and diffed. These two are ours, and only a client proves them.

    [add GargishWarHammer     equip it, flip it. Expect a war hammer.
                              If it becomes a stone pillar, D-10 is wrong and ServUO's 0x481 was right.
    [add DarkwoodCrown        equip it, flip it. Expect a crown.
                              If it becomes a vulture helm, D-16 is wrong.

**Tier 2 — the seventeen types whose parent we changed.** Re-parenting onto a carrier means the
stock parent's members were reproduced by hand. Batch 3 got this wrong once and batch 4 caught it,
which is exactly why this tier exists.

    [add GargishBattleAxe     two-handed, axe swing sounds, and CHOP A TREE with it.
                              This is the one that actually broke. Batch 3 left it one-handed
                              with sword sounds and unable to harvest; batch 4 restored BaseAxe.
    [add LeatherTalons        shoes: footwear layer, wearable, correct art.
    [add GargishKiteShield [add GargishPlateArms [add GargishPlateKilt
    [add DragonTurtleHideChest (and Arms, Bustier, Helm, Legs)
    [add GargishDagger        knife: double-click should target for carving.
    [add SorcererHat [add VirtuososCap [add HumilityCloak [add BearMask
                              each should behave as its stock kind, not as a generic item.

**Tier 3 — sets completing.** The newest mechanism on the shard and the least exercised.

    Marksman   Feathernock + Swiftflight. Brand new shape: Swiftflight is a Bow implementing
               ISetItem directly, not a carrier child. Two pieces, set bonus should apply.
    Darden's   the five Dragon Turtle Hide pieces. Expect NO "Myrmidex Slayer" line (D-26).
    Virtuoso   four pieces including VirtuososArmbands.
    Bestial    bonus should apply; the set should NEVER rage, hue-shift or block heals.
               That is D-14 and it is expected, not a bug, until the hooks row lands.
    Aloron     still unverified from S1/S6. Completed set eats cold damage as a CAPPED DELAYED
               HEAL three seconds after the hit. Watch health recover, not a smaller number.

**Tier 4 — the wide sample.** Twenty or so, spread across `Items/Equipment/{Weapons,Armor,
Jewelry,Clothing,Suits}` and `Items/Artifacts`. Looking only for art, hue and a property list
that reads sanely. Pick a few costumes too: they should stay on when you take damage, which is
D-5 and is a known deviation from ServUO, not a defect.

**What is expected to be missing, so you do not report it as broken:** soul charge on the two
Signs of Chaos and `MysticsGuard` (D-21); hit-lower-defend on the three mace-and-shield head
pieces (D-22); the Despicable Quiver's resistance and Archery bonus (D-23); Epiphany's burst and
its "Set Ability" lines (D-24); the Tenth Anniversary Sculpture doing anything after "Your luck
just improved!" (D-28); `FirstAidBelt` speeding up bandages (D-27); self-repair on any completed
weapon, clothing or shield set (Q-038). Eight of those close together on the set-mechanic hooks
row in `docs/gap-register.md`, which is costed and waiting on your decision.

## How to run it

Same throwaway loopback-only container the agents use, **not the live shard**. `build.sh`
produces the image; bring it up, log in with a GM account, make a gargoyle, and work down the
list. Nothing here should ever touch `sl-modernuo`. Anything that looks
wrong goes in `notes/` as a finding, and I will turn it into a task.


---

# Results, 2026-09-19

First client verification on this project. Everything ported since P1 had been proven
structurally: it compiled, its type registered, the world saved and reloaded, 44 tests passed.
None of it had been **looked at**. Now it has.

## Content: thirteen checks, zero regressions

| # | Check | Result |
|---|---|---|
| 1 | `GargishWarHammer` flip → `0x48C1` | **PASS.** Still a war hammer. D-10 was right; ServUO's `0x481` is a typo |
| 2 | `DarkwoodCrown` flip → `0x3168` | **PASS.** Still a crown. D-16 was right |
| 3 | **Marksman set** completes (`Feathernock` + `Swiftflight`) | **PASS.** Hue change and set effect observed |
| 4 | `DragonTurtleHideChest` equips | **PASS** |
| 5 | `SorcererHat`, `HumilityCloak` equip | **PASS.** Batch 5 carrier children, stock parent members reproduced by hand |
| 6 | `ZombieCostume` survives damage (D-5) | **PASS.** Stays on, as designed |
| 7 | **Darden set** completes | **PASS.** No Myrmidex Slayer line, per D-26 |
| 8 | **Aloron set** eats cold damage | **PASS.** Cliloc 1113617 observed. **Closes A5** |
| 9 | **`GargishBattleAxe`** two-handed, axe sounds, chops wood | **PASS.** Batch 4's repair verified |
| 10 | Gargish block: `WarHammer`, `Dagger`, `KiteShield`, `PlateArms`, `PlateKilt`, `LeatherTalons`, `StoneWarSword`, `LargePlateShield` | **PASS.** All equip on correct layers |
| 11 | `MAKE X` label | **DEFECT CONFIRMED** 2026-09-19, **FIX VERIFIED** 2026-09-20. Renders white beside MAKE NOW. The first fix did not compile at the pinned commit and was repaired during CC4 (Q-045); this is the repaired version, built clean through `build.sh` and seen in a client |
| 12 | Race-gated items reject non-gargoyles | **PASS**, incidentally |
| 13 | Tier 4 art sample: `OrcishBow`, `PaladinSword`, `BlueDiamondRing`, `FireRubyBracelet`, `AssassinsCowl`, `MagesHood`, `VoidInfusedKilt`, `EvilOrcHelm` | **PASS.** All spawn with sane art |

**The two that could never have been checked any other way** are 1 and 2. Everything else in the
381 files was copied from ServUO and diffed against it. Those two are places we decided ServUO's
own value was wrong and overrode it on reasoning alone.

**Three decisions were validated, not just the content:**

- **Q-041, Swiftflight as `Bow, ISetItem` rather than a sixth carrier.** The argument was that
  `AOS-set-attribute-aggregation.patch` dispatches on `obj is ISetItem`, so the interface alone
  suffices. Check 3 is that being true in a client.
- **Q-040, the narrow re-parent rule.** Darden's pieces derive from the `DragonTurtleHide` types,
  which only works because batch 3 put those on `BaseSetArmor` **at port time**. Doing it later
  would have been unmigratable. Check 7 is that call paying out.
- **Batch 4's parent-member rule.** Check 9 is the `BaseAxe` repair working.

## The one defect: MAKE X

Pending since P1 in June, the oldest item on this list, and the only thing tested that affects
the **live** shard rather than ported content. `AddLabel(175, 390, LabelColor, "MAKE X")` passed
`0x7FFF`, an RGB555 colour, where `AddLabel` wants a hue index. Fixed with `AddHtml` and a
`BASEFONT` colour so both states render through the same path as the `MAKE NOW` label beside
them. **Closed 2026-09-20.** The label renders. Worth keeping the whole arc, because the failure was in
the record rather than the code: the fix as first committed called an `AddHtml` overload the pinned
gump builder does not have, broke HEAD, and was repaired during CC4 (Q-045). For a day this table
recorded MAKE X as passed when what had been confirmed in a client was the **defect**. The repaired
version was then built clean through `build.sh` and verified in a client. **Confirming a bug and
confirming its fix are two different entries.**

## What the exercise actually cost, and what it caught

Getting to the first `[add` took a week, and **every blocker was in the test rig, not the
content**:

1. **The test shard relayed clients onto the LIVE shard.** `Configuration-test` is a copy of the
   live config, which advertises `192.168.1.58` with `autoDetect` false.
2. **The test container mounted the live world save.** A test session would have written several
   hundred spawned artifacts into the real world.
3. **A fresh world blocks on `AccountPrompt` forever.** No accounts means
   `ConsoleInputHandler.ReadLine()` on stdin. `docker ps` says Up, the listener never opens, the
   client hangs at "verifying account" with no symptom on its own side. The prompt fires at
   container start, so attaching later shows nothing to answer.

All three are fixed in `docker/uo/`. All three were invisible until someone tried to connect,
which is the argument for having done this months earlier.

**And a process failure worth keeping.** Three fixes were written for "stuck on verifying
account" before anyone established whether a server was listening. The evidence was on disk the
whole time: `Saves-test` was empty, and a running ModernUO writes a save within minutes. It was
read twice and explained away. `AGENTS.md` already says a cause deduced from reading source is a
hypothesis and you probe the running system first. Four fixes were written without probing.


---

# Results, CC4 Despise, 2026-09-20

Verified the same session as the MAKE X re-check, on the throwaway test shard, fresh world.

| Check | Result |
|---|---|
| `[SetupDespise` completes | **PASS.** Controller, 2 ankhs, 6 gates, 47 spawners |
| Creatures spawn with power levels | **PASS.** "Hellion, Power Level: 1: Normal"; Rat, Darkmane, Skeletrus, Sagittarri, Fairy, Unicorn all present |
| **The two armies land in the right regions** | **PASS.** Evil side gave Hellion and Darkmane; good side gave Fairy, Sagittarri and Unicorn. This is the check that matters most, because CC4's first headless run had `Region.Find` returning the static dungeon everywhere and the controller finding zero spawners |
| Gates move the player | **PASS**, both pairs tested (`5476 737 5` ↔ `5458 610 50`, and the second pair) |
| Ankh hands out a `WispOrb` | **PASS.** Alignment offered, orb received |
| **Possession** | **PASS.** "Your Wisp Orb takes control of the creature!" and the creature reports itself under the player's control. Range refusal ("That is too far away") also fired correctly |
| The Call to Arms refusal | **PASS.** "your forces are not yet strong enough to heed it" with nothing conscripted, which is the designed behaviour |

**Still unverified, and two of them cannot be checked on this world:**

- **The boss sequence end to end.** Call to Arms → transport → overlord → cleanup, roughly 90 minutes of timers. Skippable rather than blocked.
- **`DespiseTeleporter` conversion.** `[SetupDespise` *converts* existing teleporters at the dungeon mouth (`5588, 631, 30`) so a possessed creature cannot follow the player out. A fresh world has none to convert, so this path has never run. **It will fire the first time this lands on the live shard, which does have decoration.** Worth watching for on that deploy.
- **`[DeleteDespise` with players inside.** Needs players.

**What this run establishes beyond the dungeon:** CC4's region work holds in a live world, not just in a headless probe. Every region in pinned ModernUO is Dynamic, so the "dynamic first" tie-break never separated the Despise regions from the static dungeon at equal priority, and the fix was to run them at priority 51. Two armies landing in two correct regions is that fix observed.
