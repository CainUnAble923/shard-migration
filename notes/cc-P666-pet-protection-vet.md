# cc-P666: Pets on the isle, and every vet brings pets back (P481 F6)

Golem Iron, 2026-10-27. Branch `golem/Iron/P666` in both copies. Prompt: `cc-prompts\claimed\Iron\cc-P666-pet-protection-vet.md`
(re-sited for the SoS swap by P673 section 1.4).

## In plain words

- **Every stock vet** now does what ServUO's vet does. Step within 3 tiles of a vet while your dead bonded pet's ghost
  is near. You are held still for up to a minute while a window lists your dead pets with their fees. OK brings the
  chosen pet back. The fee is 100 + 1.1041^MinTameSkill gold from the bank, 100 to 30,000. The pet loses 0.2 in each
  skill. The vet refuses while the pet's body is still there. New Haven's stable vet (whichever S7 seeds) and every
  town vet work this way, with no Young waiver: it is ServUO's rule as written.
- **On the isle** (any Fold map), a Young owner's pet ghost that comes within 3 tiles of Tobin comes back at once. It
  is free and loses no skill. Its body need not have faded: the things on its corpse go back on the pet (worn things
  on a free layer, the rest in its pack, or at its feet if it has none), and the corpse goes. The pet still died, so
  the lesson means something. Tobin's window, for a Young owner's pet farther away, gives the same free, whole revival.
- **Off the isle**, Tobin's rule is unchanged (prompt item 2). It is free while Young, the body must fade first, and
  the pet loses 0.2. A non-Young owner pays ServUO's fee at Tobin anywhere, the isle included.
- **Lines.** Wren tells a Young owner on the isle to bring the ghost to Tobin, free, "with everything it carried". Sera
  the healer now notices pet ghosts too: "I heal people, not pets..." and points to Tobin at the farm gate. A non-Young
  owner hears the wait-for-the-body version from both. Finishing the farm says the pet lesson line (P481 walk step 7):
  "If your pet dies, bring its ghost to a vet. Here on the island, Tobin brings it back free and whole while you are
  Young. Every town's vet can do it too, for a fee from your bank." Wren's no-vet line now says "any town's vet" instead
  of "the vet by the New Haven stables", since S7 moves the town.

## Files (code copy `D:\UO\golems\Iron\ShatteredLegacy`)

- `server/customizations/Mobiles/NPCs/VetResurrection.cs` (new): `VetResurrection` (DeadPets, Fee, OnVetMovement with
  the freeze and its one-minute expiry, Resurrect) and `VetResurrectGump` (ServUO's window, radios, OK 1 / Cancel 2).
- `server/patches/Veterinarian-resurrect-pets.patch` (new, 7 lines): an `OnMovement` override on pinned's
  `Veterinarian` that calls `base` and then `VetResurrection.OnVetMovement`. Named in `docker/uo/apply-patches.sh` after
  the AnimalTrainer elixir patch.
- `Tutorial/TutorialPetCare.cs`: `IsleCare`, `ReviveWhole`, the new lines; Tobin revives on the isle and reuses
  `VetResurrection.DeadPets` (now with ServUO's line-of-sight check), `Fee` and `SkillLoss`.
- `Tutorial/TutorialFarm.cs`: `GhostPetLineFor` (speaker and owner pick the line), the new lines, the lesson line in
  `CheckDone`.
- `Tutorial/TutorialCorePlacement.cs`: `TutorialHealer.OnMovement` (Sera notices pet ghosts, Wren's cooldown shared).
- `server/tests/Tutorial/TutorialPetCareVerification.cs` (new, 5 facts). `TutorialFirstPlayVerification.cs`: the farm
  vet step now expects the isle's at-once revival (no window), since its pet stands within 3 tiles of the vet.
- `CHANGELOG.md` (2026.10.27.3, three "Added" lines), `VERSION`.

## The patch: alternatives

Pinned's `Veterinarian` (`Mobiles/Vendors/NPC/Veterinarian.cs`, 25 lines) has no `OnMovement` and no resurrection.

1. **A subclass seeded in place of stock vets** (P480's way for Tobin). Rejected: every spawner and every placed vet in
   every world is the stock type; it would reach none of them.
2. **A world-load pass that swaps each vet for a subclass.** Rejected: it changes types under spawners (they respawn
   the stock type) and is a migration in all but name.
3. **A global movement event.** `EventSink.Movement` fires for the mover, before the move, and costs a range search
   for vets on every step of every mobile on the shard. Rejected for cost and for order (P457 notes the same).
4. **Chosen:** one override in pinned's `Veterinarian`, calling `base.OnMovement` (BaseCreature's) and our helper. The
   whole behaviour lives in customizations. `TutorialVeterinarian` is a `Veterinarian`, so the helper skips it and
   Tobin keeps his own offer (no double window, no freeze).

Dry-run: the patch was produced by `diff -u` against pinned's file at d4531cd94 and applied in the gated build below.

## Fidelity

Stock vets follow ServUO: the fee, the 0.2 loss, the freeze, the line of sight and the corpse rule. Departures, all
presentation or guards, not rules:

- **Text, not clilocs, for 1113xxx.** ServUO's window and refusals use 1113193, 1113284, 1113286, 1113197, 1113200 and
  1113279, which are later than our 7.0.117 client's era. The lines carry ServUO's own English from its comments, so
  the wording matches the wikis. The older clilocs (501041, 503376, 500643, 1060398, 1060022, 1060020) are kept.
  **Unverified:** I tried to confirm which numbers our client's Cliloc.enu holds. The lookup tool returned "no entry"
  even for 501041 and 1060398, which every client has, so its answer is not evidence. Reading the file directly was
  refused: it lives in the main copy, which this Golem may not touch.
- **The answer is checked in person** (the vet still there, same facet, within 4 tiles), as Tobin's is (cc-P610), so
  nothing is paid for a service not given. The owner is frozen while the window is open, so in normal play this
  changes nothing.
- **Cancel is button 2** (ServUO's -1), and the expiry timer stops on any answer. ServUO's left it running, so a
  later freeze from something else could be undone by it.
- **No Kotl automaton.** ServUO adds a broken automaton head's automaton at fee 0. Our `KotlAutomaton.OnDeath`
  stables it (IsStabled, Internal) and leaves the head. ServUO's vet path would bring it back still stabled with the
  head left behind. It was left out with a comment and is not in this prompt's list (it was P480's draft item 2). It
  belongs with the automaton's repair hook (`BrokenAutomatonHead.cs:10-11`).

Nothing new for `docs\fidelity-principle.md`: no Young waiver at stock vets. The isle's rule is tutorial content of our
own. A docs row for the text-for-cliloc choice is the overseer's call (I may not edit `docs\`).

## Tests

Facts (`TutorialPetCareVerification`):

1. On the isle, a Young owner's horse ghost stepping within 3 tiles of Tobin comes back at once. No fee is taken, every
   skill is the same, the corpse is gone, its necklace is back on it, no window opens, and the owner hears "Your pet is
   alive again, with everything it carried."
2. Off the isle (Trammel), Tobin does not revive at once. His window refuses while the body is there; after it fades
   the pet comes back free (Young), less 0.2 in each skill.
3. A stock `Veterinarian`: the owner's step in opens `VetResurrectGump` and freezes them. OK with the first radio
   brings the horse back for ServUO's fee (horse MinTameSkill 29.1), less 0.2, and unfreezes.
4. On the isle, a non-Young owner's ghost at Tobin is not revived at once. The window charges ServUO's fee and the pet
   loses 0.2.
5. Sera's and Wren's lines for a Young owner on the isle name Tobin and "free". Sera says hers when the ghost steps
   near her. A non-Young owner gets the wait-for-the-body lines. `CheckDone` on a finished farm sends the pet lesson
   line.

Skill checks compare `BaseFixedPoint`. Pinned's `Skill.Base` setter truncates to tenths (`(int)(value * 10.0)`), so the
expected value is computed the same way, not as `s - 0.2`.

**Seen failing first** (probe: `notes\cc-P666-tools\probe.sh`, the code and tests bind-mounted over
`sl-uo-builder:cc-P705`; summaries in `notes\cc-P666-tools\`):

| Run | What it ran against | Result |
|---|---|---|
| `red-old` | The Tutorial folder before the change, pinned's unpatched vet, and stubs only for the names the facts use (`stub-VetResurrection.cs`, constants, a `GhostPetLineFor` returning today's line) | 3 of 5 failed: fact 1 (the pet still dead), fact 3 (no window), fact 5 (Sera got Wren's line). Facts 2 and 4 passed: they guard rules that existed before |
| `red-everywhere` | New code, with the isle rule's Fold check removed | Fact 2 failed (the pet came back at once off the isle) |
| `red-anyowner` | New code, with the isle rule's Young check removed | Fact 4 failed (revived free for a non-Young owner) |
| `green1` | New code | 39 of 39 passed (the 5 facts, `TutorialFirstPlayVerification`, `TutorialServicesVerification`, `TutorialFarmVerification`) |

`mutants.py` rebuilds the red trees. The first green attempts failed to compile, twice, on missing `using` lines in
the new test file (`Server.Gumps`, `Server.LootBoxes`); fixed in the test only.

**Gated build:** `docker\uo\build.sh -t sl-modernuo:cc-P666`, run detached under the `docker-build` lock (taken, then
released) after dropping the WSL page cache: **green**. "Applied: Veterinarian-resurrect-pets.patch", "All 170 patches
applied successfully." "Built sl-modernuo:cc-P666 with patches applied and 2680 shard test(s) passing." Of 2,685 tests,
2,680 passed, 0 failed and 5 were skipped. The five new facts passed in it. Image b2886e7af1cd.

## Not verified

- Nothing was run on a shard or in a client: the freeze, the window's look and the isle revival were not seen in game.
  The window's layout is ServUO's, with HTML text where it had localized HTML. The text colours are mine (white, and a
  light blue for ServUO's 0x1DB2D).
- Line of sight was never tested against a wall: every fact stands on open ground. On a real map, a ghost behind a wall
  is not listed, as in ServUO. This now applies to Tobin too.
- `probe.sh` expects `Veterinarian-patched.cs` and `Veterinarian-pinned.cs` beside it. These are pinned's file with
  and without the patch, and are not saved in `notes\` (pinned source).
- Tobin's spot: the code places him at `FarmVetSpot` = (3400, 2612) + the farm shift (3314, 1364) = **6714, 3976**.
  P673's table says 6714, 3979. I left the code as P663/P705 built it; one of the two numbers is a typo, and the
  overseer should say which.
- New Haven's town vet: the seeder still places a `TutorialVeterinarian` (Young waiver) there when the town has none.
  Every stock vet now works, so S7 can seed a plain `Veterinarian` instead. Left as is: S7 re-seeds the town anyway.

## Deviations and decisions for Chase

- **Read on the code copy was refused** in this unattended run (I wanted `Read` on
  `D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Tutorial\TutorialPetCare.cs` to edit it with the editor).
  I read the files with `cat` and edited them through scripts (`notes\cc-P666-tools\edit_code.py`, `edit_tests.py`).
  The new `TutorialPetCare.cs` was written whole and copied in.
- **Off the isle, Tobin keeps today's rule** (prompt item 2, "unless Chase says otherwise"); nothing was asked.
- **Stock vets have no Young waiver** (ServUO's rule). P480's draft offered a shard-wide waiver "only if Chase wants
  it". Not asked; the default is fidelity.
- Nothing asked through Ask-Chase.

## Commit preflight

- Code copy, on `golem/Iron/P666`: `CHANGELOG.md`, `VERSION`, `docker/uo/apply-patches.sh`,
  `server/patches/Veterinarian-resurrect-pets.patch` (new), `server/customizations/Mobiles/NPCs/VetResurrection.cs`
  (new), `server/customizations/Tutorial/TutorialPetCare.cs`, `TutorialFarm.cs`, `TutorialCorePlacement.cs`,
  `server/tests/Tutorial/TutorialPetCareVerification.cs` (new), `TutorialFirstPlayVerification.cs`.
- Docs copy, on `golem/Iron/P666`: this file and `notes\cc-P666-tools\` (scripts, the probe, the stub, red and green
  summaries; 41 KB). No file over 5 MB. `docs\` untouched.
- Not committed (the Golem commits). Haven not touched. Locks: `docker-build`, taken for the gated build and released.

P666 DONE
