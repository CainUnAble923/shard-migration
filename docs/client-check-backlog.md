# Client spot-check backlog

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
