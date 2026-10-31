# cc-P740: isle wake easier to see, bandages for the healing lesson, Echo off the isle: stopped, a question for Chase

Iron Golem, 2026-10-30. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P740`. Nothing changed in the code copy yet. Nothing built, deployed or published.

## In plain words

- Nothing in the game has changed yet. Before starting, I found that item 5 does not match the game: the Wakening Isle
  has no sparring or weapons-training lesson. The sparring echo already lives in New Haven, and P743 moves it to the
  warrior area there.
- The only "Echo" on the isle is the pale gray rat of the Death and resurrection lesson (it kills you, Sera brings you
  back). Taking "Echo" off the isle would remove that lesson, which your note did not ask for.
- **For you:** pick one on the Golem card or by email (question Iron-P740-20261030-205205-8ea9): keep the death lesson
  (my recommendation; nothing is removed from the isle), or remove the death lesson from the isle too.

## What I found (item 5)

- `combat.weapons` ("Pick your weapon", the blue "sparring echo") is a wing lesson started from Rook in New Haven; it
  runs in the training yard behind the Little Shop of Magic (`TutorialWingTrials.Yard`, 3633, 2562 on Trammel). It does
  not run on the isle.
- On the isle, `TutorialWorld.Echo` (6736, 3998) is the death lesson's creature, `TutorialDeathEcho`, the "pale gray rat"
  in the isle's training yard (`core.death`, "Death and resurrection"). No isle step, sign or quest line names sparring.
- Equipping a weapon and war mode are taught in Wren's farm lesson (the pitchfork, Tab): unchanged either way.

## The plan for items 1 to 4 (unchanged by the answer)

From `notes\cc-P732-isle-wake-pose.md` and `Tutorial/TutorialWake.cs`:
1. **Lighter:** the opening dark (level 24) becomes a dusk level picked from TazUO shots of a new character.
2. **Lying down:** keep P732's held pose (death animation backward, longest frame delay); add an overhead line from the
   start ("You lie on the wet sand...") and bring "Move to get up." in earlier.
3. **Slower get-up:** the get-up drawn over about 2.5 s with moves refused while it plays, then the dawn, then the first
   lesson's lines and the held windows (patch notes, achievements).
4. **Bandages:** a per-player bandage stack on the farmhouse table by Pip, and Wren's overhead hint at the healing step
   when the trainee has none; the lesson completes either way.
Then facts red-first, the gated build, before/after TazUO shots in `notes\cc-P740-tools\shots\`, the bot on the whole
isle, and a check that the change applies to `release/isle-20261028`.

P740 STOPPED: asked Chase (Iron-P740-20261030-205205-8ea9)
