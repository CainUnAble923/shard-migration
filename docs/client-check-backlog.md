# Client spot-check backlog

Everything ported since P1 is verified **structurally**: it compiles, its type registers, the
world saves and reloads, and 28 tests pass. None of it has been **looked at**. This is the list of
what a client session would actually settle, accumulated across eight tasks.

**Chase runs the client. No agent does.** Nothing here is urgent, and none of it blocks porting.

## When to do this

**After CC9 lands, in one sitting.** Batching is the whole point: standing up a client, logging
in and spawning things costs the same whether you check five items or fifty, and CC9 will add a
few hundred artifacts whose entire risk is visual.

**Bring it forward only if** a ported item turns up looking wrong in normal play, or if something
below starts blocking a decision.

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

### 6. Artifacts, CC9 — the big one

Whatever CC9 ships. Spawn a sample across each directory rather than all of them, since the risk
is uniform: wrong art, wrong hue, missing property lines. **Prioritise anything where
`IsArtifact` or `ReforgedSuffix` was deleted**, since those are the deliberate deviations.

## How to run it

Same throwaway loopback-only container the agents use, not the live shard. `build.sh` produces
the image; bring it up, log in with a GM account, and work down the list. Anything that looks
wrong goes in `notes/` as a finding, and I will turn it into a task.
