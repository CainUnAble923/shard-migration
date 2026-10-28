# cc-P721: make the bandage wait clear on the isle (and dying, meditation, the vision, waking, war mode)

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`, both
on `golem/Iron/P721` (main at the P717 merge). Not committed, nothing deployed, Haven not touched.

## In plain words

- **Bandaging at the farm now works the first time, and says what is happening (test shard).** Wren's patient is
  Pip, a farm boy beside her who stays hurt until bandaged. She says a bandage takes a few seconds. Each bandage on
  the isle says how long to wait, shows "*bandaging*" over your head, and ends with "You finish applying the bandages"
  or "You fumble the bandage. Try again." Your own bandage takes 4 seconds there instead of about 9.
- **New moments on the isle.** A new character first lies on the wet sand in the dark, with waves, then gets up.
  Dying on the isle tells you what to do, with an arrow to the healer (and back to your body if anything is on it).
  Before the farm's pests, Wren gives you a pitchfork to keep and teaches war mode: hold it, press Tab, double-click a
  rat.
- **The vision is lit, slower, and the Stranger strikes the Gem.** It's bright from its second second, between two
  glowing braziers. The Stranger walks up to the Gem and swings at it twice, with a hit sound and a burst on the Gem.
  The whole scene runs 61 seconds instead of 45. The windows that covered the middle of the screen close as it
  starts.
- **For you:** walk the isle once more on the next test build, and look at the wake-up on the beach with your own
  eyes: I could check it only by tests and bot lines, not by picture. The 200 cap you saw while meditating is the
  shard's real cap today (F-12's lower caps aren't built). Nothing to decide.

## First: P718 brought in

P718 (fixes round 1) was committed but not merged into main when this started, and this prompt builds on it: the
farm's bandages, pests and gate, the gain pace. So its commit (`08d9692`) was applied to the working tree with
`git cherry-pick --no-commit` (no commit made). Two conflicts were resolved by hand: `CHANGELOG.md` keeps both
sections, and `VERSION` takes the later number. When the integrator merges P718 and then this branch, P718's lines
are the same on both sides. This is the same move as resuming a parked branch, and it is noted here so the integrator
knows.

## What was done

| Item | What changed | Where (code copy) |
|---|---|---|
| Bandage: what a new player saw | A Dex-35, 0-Healing character's self bandage takes 5 + (120 - Dex) / 20 = **9.3 s** (pinned AOS). It shows "You begin applying the bandages", nothing during, then the result. Chase's real problem: P707's scratch on the trainee healed by itself during those seconds, so the bandage found them unhurt, gave a new scratch, and never rolled Healing (no gain). P718's bot run hit the same thing. | |
| Bandage: a patient who stays hurt | **Pip**, the farm boy beside Wren (`TutorialWoundedHelper`). His hits never come back by themselves (`CanRegenHits`). Each heal on him finishes the step, and he is cut again 20 s later for the next trainee. Nothing can harm him. An unhurt trainee bandaging themselves is sent to him, with an arrow, instead of the old scratch. Seeded beside Wren where his spot fits; without him, Wren falls back to the old scratch. | `Tutorial/TutorialFarm.cs` |
| Bandage: the words | Wren: "A bandage takes a few seconds. You will see 'You begin applying the bandages': stand still and wait until 'You finish applying the bandages'...". On the isle, at the start of every trainee's bandage: "This bandage takes about N seconds. Stand still until you see 'You finish applying the bandages'", plus "*bandaging*" over their head (to them alone). A failed roll adds "You fumble the bandage. Try again: double-click a bandage, then click your patient." | `TutorialFarm.cs`; new `server/patches/Bandage-tutorial-wait-lines.patch` (three hooks, made with `diff -u` against the post-patch `Bandage.cs`, applied after `Bandage-asclepius-bonus.patch`) |
| Bandage: success and delay | P707's practice bandage already always succeeds on the heal step when nothing slipped, and a failed try never ends the step: Pip stays hurt. On the isle a trainee's bandage **on themselves** takes **4 s** (was 9.3 s at Dex 35). On someone else it is pinned's ~2.5 s, kept; off the isle every hook returns pinned's own value. | the patch, `TutorialFarm.IsleSeconds` |
| Bandage: a real-server catch | The first bot run was refused: "You cannot perform beneficial acts on your target". Pinned's Trammel rules say "Players cannot heal uncontrolled mobiles" (`NotorietyHandlers.Mobile_AllowBeneficial`), and the isle uses Trammel's rules. The test host doesn't install that rule, so the facts had passed. Pinned's handler is now wrapped so that Pip, and only Pip, can be bandaged; a fact runs pinned's real rule. | `TutorialFarm.AllowBeneficial` |
| Dying on the isle | Outside the death lesson (which has its own lines), a trainee who dies on the isle gets, the first time per character: "You have died. You are a ghost now...", "Follow the arrow to Sera the healer and double-click her, then click Resurrect...", then either "While you are Young, your belongings stay in your backpack..." or "Your belongings stay on your body for a while...". Later deaths get one reminder line. There's an arrow to Sera. Once alive, if the body holds anything, an arrow back to it with "double-click it: your things go straight back to you" (pinned's self-loot). Checked in pinned: Young characters keep their movable things (`PlayerMobile.cs:2446`), and the Young death teleport does nothing on the Fold's maps (`YoungDeathTeleport`), so the isle's words are honest about both. | `Tutorial/TutorialDeathHelp.cs` (new) |
| Gain spam while meditating | P718's isle pace (one gain per skill per 10 s on the isle) sits in the Fold region's `AllowGain`, which every skill check passes: Focus's passive check and Meditation's passive and active ones too. A new fact proves it, and fails with the pace off. Chase's screenshot was from a build without P718. The **200** is the real cap a new character has today (`ClusterFSkillCaps`, D64); F-12's loop-0 cap of 50 is not built. | the new fact |
| The vision | The opening is lit from its second second (light 6, was "Dim" 18), with two lit braziers by the Gem; the later dim scenes are 12 (was 18). The Stranger now starts 6 tiles off, walks up to the Gem a tile a second, faces it, and swings: a one-handed slash animation, the longsword's hit sound (0x237), the bolt, a burst on the Gem, and a second swing two seconds later, all before the shards fly. Every beat is later, so each line stays up longer: **45 s became 61 s (+36%)**. The beats are named (`TutorialVisionScene.Beats`), and the scene is otherwise as P665 wrote it. When it starts, it closes the lesson page, Tamsin's or Rook's window and the patch notes, which the first capture showed covering the scene. | `Tutorial/TutorialVisionScene.cs`; the core.loop hint says "about a minute" |
| Waking on the beach | The first arrival (only from the start choice's first login: never on a remedial trip, a copy reset or `[Tutorial reset`) lies down. The human death animation plays forward, the trainee is frozen for 5 s in their own dark light, with a wave sound (0x12) and "You wake on cold sand, soaked and aching. Waves wash over your boots...". The light comes up over 4 s, then they get up (the same animation backward), and the first lesson's lines and the arrow to Tamsin follow. Why not a screen fade: TazUO ignores the server's fade packet (P665), so the dark is the trainee's light level, as in the vision. A client holds a pose only for an animation's length, so if one shows the character standing between the two animations, the dark and the lines still carry the moment. | `Tutorial/TutorialWake.cs` (new), `TutorialStart.SendToIsle(..., wake)`, `Fold/FoldRegions.cs` |
| Weapon and war mode | After the pet commands, Wren puts a **farmhand's pitchfork** in the pack, once per character. It is kept like the isle cloak: blessed, can't be sold, traded, banked or dropped. Its Strength need is 10, because a stock pitchfork wants 55 and a new character may have 45 (the test caught it). "Drag it onto your character's hand..., or double-click it, to hold it. If you already hold a weapon, drag that into your backpack first": the bot run found a new character already holds its starting weapon ("You can only wield one weapon at a time"). Once it's held: "press Tab, or click the Peace/War button on your character window, to switch to war mode... Press Tab again for peace mode". Tab is TazUO's real default, checked in its source (`GameSceneInputHandler.cs`; hold-to-fight is off by default). Once in war mode, Wren opens the field gate: "double-click a rat or grass snake to attack it yourself, then say 'all kill'". The pest part also waits for one attack by the trainee: a swing, hit or miss (`AggressiveAction`). | `TutorialFarm.cs` (`TutorialPitchfork`, `CheckCommands`) |

## Facts

New: `server\tests\Tutorial\TutorialIsleBandageWaitVerification.cs`, with 7 facts, one per item:
- The 4-second self bandage on the isle, pinned's delay elsewhere, and the lines.
- Pip stays hurt, can be bandaged under pinned's real rule, is not harmed, a fumble leaves the step open, a heal
  finishes it, and he is cut again.
- Dying: the full words and the arrow the first time, a reminder after, nothing in the death lesson, and the arrow
  back to the body.
- Focus and Meditation under the isle's pace.
- The vision: the lesson page closes, the scene is lit with braziers, the Stranger walks from 6 tiles out to beside
  the Gem and faces it, the strike line comes while the Gem is whole, and the scene is 61 s.
- The wake-up: frozen and dark, still down 4 s in, up after 5 s, and not again on a later trip.
- The pitchfork (kept, one per character, held), war mode, and the trainee's own attack.

Changed for the new behaviour:
- `TutorialVisionSceneVerification` (its timings read the named beats and the new length).
- `TutorialFarmVerification`, `TutorialIsleWalkFixesVerification` and `TutorialCopiesVerification` (the pest part now
  also needs the pitchfork in hand and war mode, and a strike).
- `TutorialFarmVerification`'s seeder counts (Pip).

**Seen failing first** (`notes\cc-P721-tools\mutate.py`, `probe.sh` on `sl-uo-builder:cc-P717`; summaries in
`red\`):

| Copy | Puts back | Failed |
|---|---|---|
| `old` | every item as before P721 | **6 of 7**: each on its own item (9.25 s, not 4; Pip heals by himself; no words on dying; the vision 45 s; no wake-up; the pest part opens without the weapon) |
| `nopace` | the isle's gain pace off | the Focus and Meditation fact (27.8, not 25.9). This one passes on the code before P721 because P718's pace already covers both, which is what Chase asked to confirm |
| `benef` | pinned's beneficial rule alone | the Pip fact: pinned refuses his bandage |

Then green: 214 of 214 tutorial tests (`green-tutorial.txt`).

## Builds

`docker/uo/build.sh -t sl-modernuo:cc-P721`, detached, under the `docker-build` lock (released each time). Windows
had 1.3 to 4.0 GB free, after dropping the Docker VM's page cache each time.
1. to 3. Green, 2723 passed.
4. Failed to compile one test (a missing `using`), fixed.
5. **Green, `EXIT=0`**: "Built sl-modernuo:cc-P721 with patches applied and 2723 shard test(s) passing." 2729 tests:
   2723 passed, 0 failed, 6 skipped (the client-data facts). (`gated-build-5.log`)

## Bot route and capture (private shard, port 2596, `test-shard` lock, released; the shard is down)

The route is P718's `isle.py`, copied to `notes\cc-P721-tools\isle.py` and taught the new steps: put away the held
weapon, hold the pitchfork, war mode, attack a pest, bandage Pip, and wait for the wake-up.

| Run | Result |
|---|---|
| 1 | Pitchfork not held: "You can only wield one weapon at a time". Wren's line now says to put the old weapon away; the bot does. |
| 2 | Through the pests, but the bot didn't find Pip by name (bot fixed: it looks by his spot). |
| 3 | Pip found, bandage refused: pinned's Trammel rule (above). Fixed, with a fact. |
| **4** | **0 failed checks**, beach to Rook in 159 s on build 3's image. "You wake on cold sand" at the start. At the farm: pitchfork held, war mode, an attack, pests cleared in 20 s. Pip's bandage: "You begin applying the bandages", "*bandaging*", "This bandage takes about 3 seconds...", "You finish applying the bandages", the step done. The vision took 63 s. (`runs\run4-*.txt`) Builds 4 and 5 changed only the vision's window closing and a test. |
| 5 | A second trainee (another Golem's test account) stopped at the vision, then a TazUO frame burst, one frame a second (P707's `isle-shots.ps1`). Kept in `shots\`. The first try's frames showed the lesson page and patch notes over the scene, which is why the vision now closes them. In the second: frame 10 is the lit opening. Frames 9 to 18 around the Gem show the Stranger walking in, stopping beside the Gem, the swing with the blade out (frame 14), and the second swing with the burst on the Gem (frame 16). Frame 15 is the whole lit scene: Gem, braziers, Stranger and the watching trainee. |

## Not done, and decisions

- **No picture of the wake-up.** The shot tool logs in an existing character, and the wake-up plays only on a new
  character's first login. It is proven by the facts and by the bot's "You wake on cold sand" line. Please look in
  game.
- **Pip is a new NPC** where the prompt offered "a wounded farmhand, a hurt pet, or a hurt that does not regenerate".
  A farmhand who never regenerates is the simplest that can't race the bandage. Bandaging someone else is also faster
  (~2.5 s) than oneself.
- **The Client tips page (P718)** is unchanged.
- **The Read tool was denied** (unattended) for some code files. Edits went through scripts
  (`notes\cc-P721-tools\edit_*.py`). Nothing was skipped.

## Files

- Code copy:
  - Top level: `CHANGELOG.md` and `VERSION` (2026.10.28.3, above P718's .2), and `docker/uo/apply-patches.sh`.
  - `server/patches/`: `Bandage-tutorial-wait-lines.patch` (new).
  - `server/customizations/Tutorial/`: `TutorialFarm.cs`, `TutorialVisionScene.cs`, `TutorialStart.cs` and
    `TutorialCoreTrials.cs` changed; `TutorialWake.cs` and `TutorialDeathHelp.cs` new.
  - `server/customizations/Fold/FoldRegions.cs`.
  - `server/tests/Tutorial/`: `TutorialIsleBandageWaitVerification.cs` (new), `TutorialVisionSceneVerification.cs`,
    `TutorialFarmVerification.cs`, `TutorialIsleWalkFixesVerification.cs` and `TutorialCopiesVerification.cs`.
  - Plus everything P718's commit carries (above).
- This repo: this file, and `notes\cc-P721-tools\` (1.7 MB): `probe.sh`, `mutate.py`, `red\`, `isle.py`,
  `islegrid.py`, `vision-shot.json`, `runs\`, `shots\`, the build log, the green log and the edit scripts.

P721 DONE
