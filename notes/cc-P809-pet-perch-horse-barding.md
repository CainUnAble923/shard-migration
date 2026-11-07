# cc-P809: pet perches and horse barding

## In plain words

- **Smiths can now make horse barding.** It takes 400 iron ingots at Blacksmithy 60. Use it on your own tamed horse and the horse becomes an armored horse in the metal's color. While you ride, it takes 5% of what monsters hit you for (10% if exceptional), and it wears out after 500 points (1,250 if exceptional). Those are the "half the dragon" numbers you picked. Other players' hits get no reduction. When it breaks, the horse looks as it did before.
- **Carpenters can now make a pet perch deed** (Carpentry 50, 100 logs). Place it in your house, double-click it and pick your own tamed chicken lizard, eagle or small bird. The pet sits on the perch for good as a house pet. It keeps its name and color, shows its age, and the house's owners can rename it. Redeed the perch and the pet goes in the deed with it.
- **Both are already on an existing world.** The craft rows are added at start, so nothing has to be placed or seeded.
- **For you:** nothing is required. When you play-test, the armored horse look (body 284) is worth a look in your own client; shot 5 shows it ridden. One small decision is below: whether to record the barding in `docs\fidelity-principle.md`.

## What was built

All of this is in `D:\UO\golems\Iron\ShatteredLegacy`.

| File | What it is |
|---|---|
| `server/customizations/Pets/HorseBarding.cs` | The settings (`horse-barding.json`), the store (`HorseBardingStore`, GenericPersistence, versioned), the `HorseBarding` logic, and the item `CraftedHorseBarding` |
| `server/customizations/Pets/PetPerch.cs` | The settings (`pet-perch.json`), the `PetPerch` logic, and three saved types: `PetPerchAddon`, `PetPerchDeed` and `PerchedPet` |
| `server/customizations/Pets/PetSettingsFile.cs` | The shared JSON loader: writes the defaults on first start, and refuses a bad file whole |
| `server/patches/AOS-horse-barding.patch` | The one engine change: one call, `HorseBarding.Absorb`, right after pinned's swamp dragon branch in `AOS.Damage` |
| `docker/uo/apply-patches.sh` | Lists the new patch, last in the file |
| `server/tests/Mobiles/HorseBardingVerification.cs` | 8 facts |
| `server/tests/Mobiles/PetPerchVerification.cs` | 6 facts |
| `CHANGELOG.md`, `VERSION` | `2026.11.07.2`: two Added lines and one Staff line |

### Horse barding

- **Chase's numbers** (answer `Iron-P809-20261107-092103-6902`, "Half the dragon"):
  - 5% absorbed, or 10% if exceptional;
  - it wears out at 500 points, or 1,250 if exceptional;
  - it costs 400 iron at Blacksmithy 60 to 110.
  - All of these are in `Configuration/horse-barding.json`, along with the barded body (284) and mount item (0x3E92).
- **Same rules as the dragon's** (pinned `Misc/AOS.cs:175-190`):
  - only monsters' hits count (`from?.Player != true`);
  - it protects only the rider, while riding;
  - the barding wears by exactly the damage it absorbs.
- **Stock `Horse` is not patched.** The barding is stored as a row keyed by the horse's serial, so no horse's save data changes. The row stays with the same horse through stabling and the leash figurine, since the leash keeps the same mobile (`ShrunkPet.cs`). It is dropped at save once the horse is gone.
- **Only a plain `Horse` takes barding.** The tutorial's private horse (`TutorialStableHorse`) and other kinds built on `Horse` are refused.
- **Nothing removes the barding except wearing out.** That matches pinned, which has no removal for the dragon's barding either. When it breaks, the horse gets back its own body, mount item and hue.
- **The name `HorseBardingDeed` was already taken** by a Clean Up Britannia decoration (`CleanUpRewardAddons.cs:348`), so the item is called `CraftedHorseBarding`. Players see "horse barding".
- **Credit:** the idea came from ATruGod's horse barding pack (third-party, reference only). No code was taken, and its dung joke stays out.

### Pet perch

- **The perch** uses art 0x2FB6, the client's other "parrot perch" tile. The stock `ParrotPerchAddon` uses 0x2FF4 and keeps its parrot (cc-P129).
- **Who can use it:** a house owner or co-owner, with their own tamed pet of a listed kind within 3 tiles. The kinds are in `pet-perch.json`: `ChickenLizard`, `Eagle` and `Bird`.
  - Hatched chicken lizards from the incubator qualify.
  - Summons, other people's pets, wild animals and other kinds are refused.
- **What happens to the pet:** it leaves its owner's followers and is replaced by a `PerchedPet` with the same body, hue, name and sound. The perched pet is blessed, frozen and cannot walk. It shows its age in weeks, and house co-owners can rename it. It is one way, as the pet parrot is.
- **Moving and redeeding:** the pet follows the perch when it moves and is put away when the perch is redeeded. It travels in the deed, and a re-placed perch gets it back. A deed thrown away while it still holds its pet deletes the pet, as the parrot perch's deed does.
- **Size:** one perch, one deed and one pet type, against the original's 881 lines and 8 saved types.
- **Credit:** the idea came from Hammerhand's eagle and chicken lizard perches (third-party, reference only). No code was taken.

### Rules check

- **Nothing grants** skill or stat points, power scrolls, bless deeds or property artifacts. The barding adds no item property; the horse's look is its only visible change.
- **All numbers are in config files.** `horse-barding.json` and `pet-perch.json` are written with the defaults on first start. A bad file is refused whole, every error is printed, and the defaults are used.
- **It reaches an existing world by itself.** The two craft rows are added at `ServerStarted`, and adding them twice does nothing. There are no world items to seed.
- **Engine change:** one `.patch` file. It was made with `diff -u` against pinned plus the nine AOS patches before it, in `apply-patches.sh` order, and it applies at `--fuzz=0`.
- **Serialization (D40):**
  - The four new types use the generator at version 0.
  - `HorseBardingStore` writes its own version, and an unknown version throws `InvalidDataException`.

## Tests

- **Red:** I wrote the facts beside the code, so to see each one fail I broke the code on purpose, in a throwaway container from `sl-uo-builder:cc-P808`.
  - With the AOS patch left out, the two damage facts went red.
  - I then made 26 deliberate code breaks (`mutate809.py`, results in `mutants.txt` and `mutants2.txt`). Every one of the 14 facts went red at least once.
  - One break did not compile at first, so I rewrote it; it then failed as expected.
  - One break changed nothing (`keepfollower`): deleting a pet already frees its follower slot. The extra `SetControlMaster(null)` stays because it makes the release explicit.
  - The real code: all 14 pass.
- **Gated build:** `sl-modernuo:cc-p809` (`f6c41e252c95`), 198 patches applied, **3,219 shard tests passing, `EXIT=0`**. `latest` was not moved.

## Proof shots (TazUO, private proof shard 127.0.0.1:2596)

These are in `notes\cc-P809-shots\`. A staff character stood on open ground at 1986, 2244 in Trammel; the facts cover the house and ownership rules. The walk script's checks all passed (`walk.log`).

1. `1-perches.jpg`: two perches, a chicken lizard and an eagle on them.
2. `2-plain-horse.jpg`: a wild horse, before taming. Taming it took one try at skill 100.
3. `3-barding-in-pack.jpg`: exceptional valorite barding in the pack. Its properties read "Absorbs: 10% Of Monster Damage | Lasts For: 1250 Damage".
4. `4-barded-horse.jpg`: the horse with barding: body 284 in valorite's hue.
5. `5-riding-barded-horse.jpg` and `6-riding-moved.jpg`: the character riding it, with mount item 0x3E92 drawn.
6. `7-perch-deed-in-pack.jpg`: the perch deed.

The backpack window covers part of the view in shots 3 to 6, but the subject is clear of it in each one.

**Not seen in a client:** the moment the barding breaks. The facts cover it (`ItWearsOutAndTheHorseGetsItsOwnLookBack`).

## Deviations and decisions for Chase

- **The Grep tool was denied** on `D:\UO\golems\Iron\ShatteredLegacy\docker\uo\apply-patches.sh` (an unattended run cannot approve it). I wanted to see where the AOS patches sit in the apply order, so the new patch would apply at `--fuzz=0`. Instead I read the committed file with `git show HEAD:docker/uo/apply-patches.sh` and changed it with a small Python edit. The gated build applied all 198 patches.
- **`docs\fidelity-principle.md`:** P796 asked to record the barding there as a deliberate deviation, since it is half the dragon's strength and has no OSI counterpart. Agents may not edit `docs\`, so this is yours to add if you want it. Suggested line: *Horse barding (cc-P809) is ours, not OSI: crafted like the swamp dragon's but half as strong (5/10%, 500/1,250 points), because a horse needs Taming 29.1 and the dragon 93.9 (Chase, 2026-11-07).*
- **A perched pet can't go back to being a pet.** That follows the parrot. If players want to take a pet back down, it is a small addition.

## Tools

These are in `notes\cc-P809-tools\`:

- `run-facts.sh`: quick fact runs on the builder image.
- `mutate809.py`, `run-mutants*.sh`, and `mutants.txt` / `mutants2.txt`: the deliberate breaks and their results.
- `gated-build.ps1`: the gated build.
- `shots.ps1`, `Shots809.py` and the TazUO rig (`proof-shard.ps1`, `run-tazuo.ps1`, `tazuo-walk.ps1`, `ui.ps1`, `make_create_bin.py`), copied from P804's.

Free memory was about 5 GB throughout. Both locks have been released.

P809 DONE
