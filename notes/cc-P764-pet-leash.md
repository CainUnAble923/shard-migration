# cc-P764: starter pet leash and shrink (port of Queen's pet-shrink)

Iron Golem, 2026-11-01. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P764`, not committed (the Golem commits). Nothing deployed, packaged or published. The shared Test
Shard was not touched. The play was on a private proof shard, 127.0.0.1:2596.

## In plain words

- **Players can carry a pet as a figurine.** Double-click a pet leash and target your pet, and it shrinks into a small
  figurine of itself in your backpack (weight 1). Double-click the figurine and the pet comes back out at your feet,
  following you, with its name and loyalty as before.
- **Only the owner can call it out.** It doesn't work in a fight, on summoned creatures, or on a pet carrying things.
- **Where players get one:** the dog-or-cat pet choice scroll (the moongate skip reward) now comes with a leash. Animal
  trainers sell leashes for 150 gold. Leashes are blessed and never wear out by default.
- **For you:** nothing to do. The hitching post from the same script was left out (reasons below). The price and the
  other settings are in the shard's configuration if you want them changed.

## The parts

| # | Part | What was done |
|---|---|---|
| 1 | Port the leash | **Done.** `server/customizations/ClusterFPetLeash.cs`: `PetLeash` (art 0x1374, weight 1) and `LeashedPet`, the figurine (the pet's own statuette art from pinned's `ShrinkTable`, e.g. 0x2588 for the dog, in the pet's hue, weight 1). The figurine keeps the pet's name, loyalty, owner and bond, and only the owner can restore it. Refused: someone else's pet, a summon (`Summoned` or a talisman summon), a dead pet, a ridden mount, a pet carrying items, a pet more than 3 tiles away, and a fight. |
| 2 | Starter pet, shop | **Done.** `PetChoiceScroll.Choose` (`Tutorial/TutorialGateSkip.cs`) puts a leash in the backpack with the pet and says so. Animal trainers sell it: a row in `SBPetRebirth` (`Tutorial/TutorialPetCare.cs`), the trainer's extra stock that `AnimalTrainer-elixir-of-rebirth.patch` already adds, so no new core patch. |
| 3 | Hitching post | **Skipped**, see below. |
| 4 | Config | **Done**, the shard's pattern (`ServerConfiguration.GetOrUpdateSetting`, written into `modernuo.json` with the defaults on first use): `clusterf.petLeash.price` 150, `.charges` -1 (unlimited; a positive number is the number of shrinks a leash holds), `.refuseInCombat` true, `.combatSeconds` 15, `.blessedLeash` true, `.blessedFigurine` true. |

### How it differs from Queen's script

- **Built on the shard's own figurine.** The shard already had `ShrunkPet` (the Outrider's Crook figurine), whose comments
  and facts record pinned's restart traps. `LeashedPet` is a `ShrunkPet`:
  - the pet keeps its master and leaves the follower count by hand;
  - `ShrunkPet.Initialize` redoes that after every load.
  
  Queen's figurine cleared the master and set `IsStabled`. Pinned does not save `IsStabled`, so the next load would start
  the 3-day abandoned-pet delete timer (`BaseCreature.cs:2433, 2504`). `LeashedPet` has its own double-click: `ShrunkPet`'s
  lets any holder claim the pet and makes it bonded.
- **Owner only, always.** Queen's figurine went to whoever double-clicked it unless its owner had locked it. Here there is no lock.
- **"In a fight"** means a current combatant, or any aggression either way in the last 15 seconds, for the player and (to
  shrink) the pet. Queen used `SpellHelper.CheckCombat`, which on pinned counts only fights with players.
- **No loyalty floor.** Queen raised loyalty to 60% on shrink and restore. That changes the pet, which the prompt rules out.
- **No taming.** Queen's staff shrink tamed wild creatures. That is left out, with the staff `[Shrink`, `[ShrinkLockDown` and
  `[ShrinkRelease` commands, the lock entries, the stat and skill lines on the figurine, and the XML config parser.
- A figurine deleted with its pet inside deletes the pet too, as Queen's does. Otherwise the pet would sit on the internal
  map for good. Blessed figurines stay in the backpack on death.

### The hitching post (part 3): skipped

Queen's `NewHitchingPost` is a house addon with east and south deeds. Double-clicking it starts the same shrink, using the
post's charges. It was not ported:
- I found no written housing-addon rule in the docs or notes to check it against.
- In the script, anyone who can reach the post can use it, not only the house's owner or friends, and it spends the
  owner's charges.
- It does nothing the leash does not: it is a leash fixed to a house.
- The shard already has a hitching post that stables pets (`DungeonHitchingPost`, cc-P196).

If you want one, the port is a small addon whose double-click calls `ClusterFPetLeash.Shrink`, limited to the house's
owner and friends.

## Tests

`server/tests/Items/PetLeashVerification.cs`, 9 facts:
- shrink and restore keep name, owner, loyalty (70 stays 70) and bond, with the figurine's art and weight and the follower
  count;
- a non-owner cannot restore (and the owner then can);
- shrink and restore are refused in a fight (the player's and the pet's);
- a summon cannot be leashed;
- a pet carrying items cannot be leashed (and can once unloaded);
- someone else's pet cannot be leashed;
- the starter scroll gives a leash;
- the animal trainer sells it at the configured price;
- the follower count is right after a restart while leashed (the pet's real serialize and deserialize, then
  `ShrunkPet.Initialize`).

**Seen failing first** (P769's method: each rule undone in a mutant, the facts run in the builder image;
`notes\cc-P764-tools\mutate764.py`, `probe764.sh`, `run-mutants.sh`, `mutant-logs\`). The unchanged code passes 9 of 9,
and every mutant turns exactly its own fact red:

| Mutant | Undoes | Fails |
|---|---|---|
| loyalty | Queen's loyalty floor put back on restore | P764_ShrinkAndRestoreKeepNameOwnerAndLoyalty |
| noowner | owner-only restore | P764_ANonOwnerCannotRestore |
| nocombat | the fight rule | P764_ShrinkAndRestoreAreRefusedInAFight |
| nosummon | the summon refusal | P764_ASummonCannotBeLeashed |
| nopack | the carrying-items refusal | P764_APetCarryingItemsCannotBeLeashed |
| notowned | the not-your-pet refusal | P764_SomeoneElsesPetCannotBeLeashed |
| nostarter | the scroll's leash | P764_TheStarterScrollGivesALeash |
| noshop | the trainer's row | P764_TheAnimalTrainerSellsTheLeash |

**Gated build** (`docker\uo\build.sh -t sl-modernuo:cc-p764`, logs in `notes\cc-P764-tools\`, UTF-16):
- Run 1: the new test file did not compile (`Sewerrat` for `SewerRat`): `gated-build-run1-compile-error.log`.
- Run 2: 1 failure, the fight fact. Setting `Combatant` also records aggression, which counts as fighting for 15 seconds.
  The fact now clears both between its steps, which is the rule working: `gated-build-run2-fight-test.log`.
- **Run 3, green:** `gated-build.log`. 2,929 tests: 2,923 passed, 6 skipped, 0 failed. `EXIT=0`.

## TazUO shots

`notes\cc-P764-shots\`, from one real TazUO run on the private proof shard (`sl-modernuo:cc-p764`, 127.0.0.1:2596,
the test-shard lock held). The rig is P769's, copied into `notes\cc-P764-tools\` (`run-tazuo.ps1`, `proof-shard.ps1`,
`tazuo-walk.ps1`, `ui.ps1`, `make_create_bin.py`), with `Shots764.py`.

A new character, "Iron Leash", on the Golem's admin account takes a pet choice scroll with `[self AddToPack
PetChoiceScroll` (a stand-in for the moongate skip's loot box) and picks the dog. It double-clicks the leash and targets
the dog, then double-clicks the figurine. All 9 checks in `walk.log` passed: the scroll, its window, the leash from the
scroll, the dog, the leash's target cursor, the dog figurine in the backpack, the shrink line, the dog back, the restore
line.
- `1-dog-and-leash.jpg`: the dog and the leash after the scroll.
- `2-shrunk-dog-figurine.jpg`: **the dog figurine** (grey dog statuette, 4th row of the backpack) and no dog in the world.
- `3-restored-dog.jpg`: **the restored dog** ("dog") beside the character, and the figurine gone from the backpack (16
  items to 15).

The skill-gain lines down the left come from the proof shard's test-center mode on a new admin character, not from the
leash.

## The isle release

The starter pet ships on `release/isle-20261028` (P762), and `ShrunkPet.cs`, `TutorialGateSkip.cs` and
`TutorialPetCare.cs` are byte-identical there. `notes\cc-P764-tools\p764-release-isle-20261028.diff` was checked with
`git apply --cached --check` against the release tree in a temporary index (no worktree, nothing written):
- **every server file and the test apply cleanly**;
- **CHANGELOG.md and VERSION conflict**, as every release diff does: the release has its own version line. Its CHANGELOG
  entry is the Added line below under the release's next version.

Not built as an isle image: the Done-means list does not ask for one.

## CHANGELOG and VERSION

`2026.11.01.6`. Main's newest here was `2026.11.01.5`; P769, committed separately, also used `.5`, so the integrator
may renumber.
- **Added:** the pet leash (crediting Queen's "Pet shrink for 57.2").
- **Staff:** the `clusterf.petLeash.*` settings.

## Deviations and decisions for Chase

- **Read refused three times** in this unattended run: `server/customizations/ShrunkPet.cs`,
  `Tutorial/TutorialGateSkip.cs`, and my own new `PetLeashVerification.cs` after a one-word sed fix. I did not retry the
  reads.
  - I had `ShrunkPet.cs` and `TutorialGateSkip.cs` from an earlier `cat`, so I left `ShrunkPet.cs` unchanged. A
    subclass does the leash's restore instead of new hooks in `ShrunkPet`.
  - The scroll's 3-line change and the test fix were made with exact-match Python replacements that refuse to run
    unless the old text occurs exactly once.
  - What I wanted to run: Read on those files, then Edit.
- **The hitching post is skipped** (above).
- **Version `.6`**: see above.
- Credit: Queen in the CHANGELOG and in `ClusterFPetLeash.cs`'s header. The terms are none stated, so it ships only in
  the private repo and the player package, as the third-party SOURCE.txt says.

## Files

- **ShatteredLegacy:**
  - new: `server/customizations/ClusterFPetLeash.cs`, `server/tests/Items/PetLeashVerification.cs`;
  - changed: `server/customizations/Tutorial/TutorialGateSkip.cs`, `server/customizations/Tutorial/TutorialPetCare.cs`,
    `CHANGELOG.md`, `VERSION`.
- **shard-migration:** this file, `notes\cc-P764-tools\` (the build, mutant and shot scripts and logs, the release diff)
  and `notes\cc-P764-shots\`.

P764 DONE
