# cc-P65: Evo pets 1, the evolution framework and the EA-art stages (F-35)

Run 2026-10-12 by Claude Code (autopilot hand-off after P50). Builder, test shard only. Gates at start: P62, P63 and P64
are in `cc-prompts\completed\`; `git -C D:\ShatteredLegacy status --short` was empty; pinned is at
`d4531cd94b739613155225c234900de9f47d2c88` (every pinned citation below is at that commit).

Short names: **P** = `D:\UO\ModernUO-pinned\Projects`, **C** = `D:\ShatteredLegacy\server\customizations`,
**T** = TazUO `D:\UO\cc-p40-work\tazuo-3212623f\src`, **S** = `D:\UO\ServUO-pub57\Scripts`. Client data:
`D:\ShatteredLegacy\client-data\classic-client-7.0.117.0`.

**Where the citations come from.** Three research subagents in this session read the loop reset and body table route,
the animations, and the pet hooks and stats; each reported file:line. I re-read myself everything the build depends on:
`Body.cs`'s table, `Mobile.Animate`, `BaseCreature.OnDeath` and `OnDelete` (the XP bug below), `Mobile.OnDeath`, the
sound overrides, the bandage and swing body-type checks, and `ExecuteReset`. The rest is as the agents read it.

## Summary

| Part | Built | Biggest risk |
|---|---|---|
| A. Framework | `EvoPetData` (lines, stages, gates, art-pending flag, an empty abilities slot, one stat curve, hues, Echo lines), `EvoPetSettings` (XP, server settings), `EvoPet` (one class for every line). XP per kill it damaged; step-ups with gates on the stage entered; art-pending stages skipped; the stage-3 pick and the hue picked once. | **F-12 is not built: there is no loop reset and no loop count.** Gates read `EvoPet.OwnerLoopsSource` (0 until F-12 sets it); staff stand in with `[EvoPet loops`. |
| B. Test path | `[EvoPet give <line>` and stage, xp, bond, loops, pick and info; `EvoPet.GivePet` for the Farmhand. | - |
| C. Kitsune row | Fox stage 4, art-pending, with the shapeshift rules as comments. No shapeshift code. | - |
| D. Body table | 15 bodies typed Animal at Configure (`ShardBodyTypes`). **The brief's list missed 1410** (the dog's stage 5, typed Equipment). | Writes pinned's private table by reflection; it fails loudly if pinned reshapes it. |
| E. Animations | Classic bodies are right as they are. **Every UOP-era body showed the wrong action** (hit played an attack, feeding a death, 1309 vanished); `EvoPet.Animate` remaps them. | Unverified in a client; checklist in section 8. |

Build: **1062/1062 shard tests pass**, the 10 new facts watched red, then green. Image `sl-modernuo:cc-p65` built.

## 1. The loop reset (F-35: keeps its stage through it)

**There is no loop reset in our code, and no loop count.** F-12 is not built:
- no `LoopCount`, `Loops`, `CurrentLoop` or `MaxLevel` member on `PlayerMobile` or the account data in `C` or the patches;
- the code says so: `C\StaffHub\StaffHubGump.cs:328-329` ("Levels and Loops panel arrives with F-12"),
  `C\ClusterFAccountData.cs:103-104` and `C\ClusterFGuildStarterPath.cs:14` ("once per loop" is once per character until
  loops exist).

**The nearest stand-in is the Reset Stone's reset**, `ClusterFDevTools.ExecuteReset` (`C\ClusterFDevTools.cs:109-225`;
the stone calls it, `C\ClusterFResetStone.cs:147-156`). It zeroes skills, sets stats to 10, and clears quests, guilds,
exploration, achievements, Renown, discoveries, League flags and bulletins. **It never touches followers, the stable, a
pet's master or a pet's skills** (no reference to `Followers`, `Stable`, `ControlMaster`, `Release` or `BaseCreature`).

**How the framework keeps the stage:** everything evolution needs (line, stage, XP, picks, hue, Bond Trial flag) lives
on the pet, never on the owner. **Fact 7** gives a player a stage-3 dog with a pick and a hue, runs `ExecuteReset` with
every option on, and checks stage, XP, pick, body, hue, master and bond are unchanged. When F-12 builds the real reset,
that fact is where to add a call to it.

**The loop gates** read the owner's loop count through `EvoPet.OwnerLoopsSource` (`Func<Mobile, int>`, 0 until F-12
sets it). Staff stand in for it per pet with `TestOwnerLoops` (`[EvoPet loops <n>`); the gate uses the larger.

## 2. What was built (Part A)

All in `C\Mobiles\Evo\`:
- `EvoPetData.cs`: the records `EvoLine`, `EvoStage`, `EvoStageStats` and `EvoSounds`, plus `EvoPetData`: the four lines, the stat
  curve, the hue list and the Echo lines. `EvoPetSettings` holds the XP numbers as server settings.
- `EvoPet.cs`: `EvoPet` (one `BaseCreature` for every line) and `EvoAnimations` (Part E).
- `EvoPetGumps.cs`: `EvoHueGump` and `EvoPickGump`.
- `EvoPetCommands.cs`: `[EvoPet`.
- `ShardBodyTypes.cs`: Part D.

### 2.1 Data in code, argued

A table in code, not a data file. The compiler checks every row; tests read it directly (facts 1, 8, 9); a row carries
its own comments (the kitsune's rules); nothing in it wants translating. Adding a line or a stage is a row. The numbers
staff tune without a build are server settings instead (`evoPets.xpToEnter.stage2` to `stage5`, `evoPets.xpRatePercent`
in `modernuo.json`), the way `ClusterFPetMimicSettings` does it.

**One class, not one per line**: lines differ only in data now, and the role abilities (later) will hang off the
stage row's `Abilities` slot, so a per-line class would hold nothing.

### 2.2 The data as built

Gates are on the stage being entered. XP is the total to enter (section 3).

| Stage | Dog (protector) | Cat (striker) | Fox (trickster) | Bird (scout) | Gate to enter |
|---|---|---|---|---|---|
| 1 | 217 dog, "pup" | 201 cat, "kitten" | 1423 small fox, "kit" | 254 crane, "chick" | - |
| 2 | 739 leather wolf | 1309 baby tiger | **L_Fox, art pending** | 832 phoenix bird | XP |
| 3 | **pick:** 1547, 1548, 1549, 1546, 1552, 1551 | **pick:** 1254 tiger, 1426 lion | 246 bake kitsune (loop 1) | **L_Bird 01, art pending** | XP (fox: + owner loop 1) |
| 4 | 277 cu sidhe (loop 1) | 1416 sabertooth (loop 1) | **kitsune, art pending** (loop 5 + Bond Trial) | **L_Griffin, art pending** (loop 1) | XP + owner loop 1 |
| 5 | 1410 windrunner | 1573 manticore (large) | (none) | 243 lesser hiryu | XP + owner loop 5 + Bond Trial |

Live today, as decided: **Dog 5, Cat 5, Fox 2 (1423, 246), Bird 3 (254, 832, 243)** (fact 1). Every stage is a
different body (fact 1 checks no body repeats in a line). The fox's gates follow the brief's rule by position: its
second-to-last stage (246) needs loop 1, its last (the kitsune) loop 5 and the Bond Trial.

**Art-pending rows** carry body 0 until their art ships; turning one on is setting its body number and dropping
`ArtPending`, nothing else. The pet steps past a pending stage to the next enabled one, and the gates of the stage it
enters still apply (fact 5: a fox goes 1423 to 246 and needs loop 1; a bird goes 832 to 243 and needs loop 5 and the
Bond Trial). With nothing enabled above, `EvoStatus` says "at its top for now" ([props and `[EvoPet info`); the player
is told nothing, as asked.

**Sounds** per body, from the class that uses it: Dog 0x85 (`P\UOContent\Mobiles\Animals\Town Critters\Dog.cs:13`),
leather wolf 0xE5 (`S\Mobiles\Normal\LeatherWolf.cs:24`), Cu Sidhe 0x577/0x578/0x576/0x579
(`P\...\ML\Animal\CuSidhe.cs:109-117`), windrunner 0xA8 (`S\...\Windrunner.cs:57`), cat 0x69 (`Cat.cs:14`), baby tiger 362
(`S\Quests\Eodon\Valley of One Quest\Creatures.cs:21`), tigers and sabertooth 0x670-0x673 (`S\...\WildTiger.cs:83-86`),
lion 0x3EF (`S\...\Lion.cs:18`, used for the manticore too), bake kitsune 0x4DB-0x4DF (`P\...\SE\BakeKitsune.cs:90-98`),
crane 0x4D7 (`Crane.cs:12`), phoenix 0x8F (`Phoenix.cs:13`), lesser hiryu 0x4FB-0x4FF (`LesserHiryu.cs:84-92`). The
small fox and the dog breeds have no class of their own anywhere: they use the dog's sounds. **Unheard.**

### 2.3 Stats per stage: one curve for every line (placeholder)

Stage 1 sits on a town dog: pinned `Dog.cs:15-35` gives Str 27-37, Dex 28-43, Int 29-37, hits 17-22, damage 4-7,
physical resist 10-15, MagicResist 22-47, Tactics and Wrestling 19-31, armour 12. Stage 5 sits on a Cu Sidhe:
`CuSidhe.cs:28-55` gives Str 1200-1225, Dex 150-170, Int 250-285, hits 1010-1275, damage 21-28 (Cold/Energy), resists
50-65/25-45/70-85/30-50/70-85, Wrestling 90-97, Tactics 90-99, MagicResist 75-90, Anatomy 65-69, **4 control slots**.
Ours stays at 1 slot at every stage (F-35), so stage 5 is a Cu Sidhe for a quarter of the slots. Flagged for Chase.

| Stage | Str | Dex | Int | Hits | Damage | Resists P/F/C/Po/E | Wrestling/Tactics/MR/Anatomy | Armour |
|---|---|---|---|---|---|---|---|---|
| 1 | 32 | 35 | 30 | 20 | 4-7 | 12/5/5/5/5 | 25/25/30/0 | 12 |
| 2 | 90 | 70 | 45 | 70 | 7-11 | 22/12/15/12/15 | 50/50/45/20 | 20 |
| 3 | 240 | 105 | 90 | 220 | 11-16 | 32/20/30/22/30 | 70/70/60/40 | 30 |
| 4 | 560 | 135 | 170 | 520 | 16-22 | 44/28/52/32/52 | 85/85/72/55 | 40 |
| 5 | 1210 | 160 | 265 | 1140 | 21-28 | 57/35/77/40/77 | 93/95/82/67 | 50 |

All physical damage at every stage (the line roles come later). Each step-up sets these and **heals it fully**; skills
only rise (what it learned by use stays). AI is melee for every line; the fox's 246 is a mage in pinned, and its role
(trickster spells) belongs to the abilities batch.

### 2.4 The serialization

`EvoPet` is `[SerializationGenerator(0, false)]` with generated fields (`C\Mobiles\Evo\EvoPet.cs`): 0 line key,
1 stage, 2 XP, 3 hue chosen, 4 picks (`int[]`, by stage number), 5 Bond Trial done, 6 test owner loops. A later field
is a version bump through the generator, the shard's usual route. The chosen hue is the mobile's own `Hue`, which
`Mobile` already saves. `[AfterDeserialization]` grows the picks array if a line gains stages. Fact 2 round-trips all of it.
Stabling keeps the mobile itself (`P\UOContent\Mobiles\Vendors\NPC\AnimalTrainer.cs:252-266`, `PlayerMobile.Stabled`
is a set of mobiles), so the state survives the stable. Not tested here.

## 3. XP and step-ups

**Only from fights it deals damage in**, per kill:
- On every creature's death (`CreatureEvents.CreatureDeathEvent`, raised at `P\UOContent\Mobiles\BaseCreature.cs:3540`
  and `:3669`), each controlled evo pet in the victim's damage list earns `XpForKill(victim, its share of the victim's
  hits)`. The list covers melee, spells and poison alike, since all damage goes through `Mobile.Damage(from)`
  (`P\Server\Mobiles\Mobile.cs:5956`, which registers the entry). No patch.
- **Placeholder formula:** `share x (20 + victim Fame / 25) x evoPets.xpRatePercent / 100`, at least 1. A rabbit
  (Fame 150, 5 hits) killed outright is 26; 2 of its 5 hits 10 (fact 3 measured exactly that);
  a lich (Fame 8,000) 340.
- Nothing for killing a pet or a summon (anyone's), so pets cannot farm each other.
- **A bug found and fixed on the way:** a creature's normal death deletes it (`Mobile.cs:4899-4902`), and the delete
  releases its master (`BaseCreature.cs:3688`) **before** the death event fires (`:3669`). So "was it someone's pet"
  cannot be read in the death event. The delete event fires first, while it is still controlled (`:3673`); `EvoPet`
  notes it there in a weak table. Fact 3 caught it (a tame rabbit gave XP).

**XP to enter each stage** (total, never reset; `EvoPetSettings`, server settings): stage 2 **500**, stage 3 **3,000**,
stage 4 **13,000**, stage 5 **53,000**. Placeholders until F-12. A stage-1 pet fighting pests reaches stage 2 in about 20
rat-sized kills; stage 5 is about 160 lich-sized kills.

**Step-up:** new body (or the owner's pick), stats from the curve, Arch Protection's particles and sound
(`FixedParticles(0x375A, 9, 20, 5027)`, sound 0x1F7; `P\UOContent\Spells\Fourth\ArchProtection.cs:100-101`), and one
Echo line to the owner. A blocked gate is said once per stage, in the Echo's voice.

**The Echo's lines (placeholders for Chase)**, in `EvoPetData`:
- stage 2: "The Echo: Look at that. It grew. One of you had to."
- stage 3: "The Echo: Bigger teeth. Same appetite. You two suit each other."
- stage 4: "The Echo: You have done this before, you know. It was smaller last time."
- stage 5: "The Echo: There it is. The one that remembers every loop with you."
- loop gate: "The Echo: It is ready. You are not. Loop {n} time(s) first, then we will talk."
- Bond Trial gate: "The Echo: One more step, and it wants proof you will not leave it behind. (The Bond Trial is not
  built yet; staff can mark it done.)"
- pick: "The Echo: It is changing. Choose what it becomes; there is no going back."
- hue chosen: "The Echo: <hue>. Good choice. You always pick that one."

**The Bond Trial** is not designed: a per-pet flag staff set (`[EvoPet bond on`), named as such in the blocked message.

**The stage-3 pick:** when it has the XP for a stage with several bodies, the owner gets `EvoPickGump` (names, since a gump
cannot draw a creature body), and the pet waits at its stage until they choose. Closing the gump is fine: double-clicking
the pet reopens it. **A pick cannot be changed later** by the player (fact 4); staff can (`[EvoPet pick <stage> <body>`).

**The hue:** picked once by the owner, from `EvoHueGump` (shows the line's stock statuette in each hue where there is one:
dog 0x2588, cat 0x211B, `P\UOContent\Misc\ShrinkTable.cs:18` over `Distribution\Data\shrink.json`). Closing it is fine:
double-clicking the pet reopens it until a hue is chosen. It stays through every stage (fact 6). **The placeholder list,
for Chase:** natural (0), shadow (0x455), snow (0x47E), rust (0x2C), sand (0x8A5), storm (0x59B), ember (0x21). The art of
the UOP bodies is coloured, so how each hue looks on them is unverified.

**Plain pet rules:** 1 follower slot at every stage (`ControlSlots` set once in the constructor, never while controlled,
since it has no change hook, `BaseCreature.cs:509`); bonded at once; bonded death and resurrection stock
(`BaseCreature.cs:3482-3498`, `ResurrectPet` `:4126`). `Tamable` is false: a released evo pet cannot be taken by another
tamer. Flagged for Chase.

## 4. Part D: body types

**Route.** The shard overrides no `Distribution\Data` file today: the Dockerfile ships pinned's Data unchanged
(`docker\uo\Dockerfile:97`), no patch targets Distribution, and the rule is written down ("Distribution/Data is pinned",
`C\ClusterFMineCampLayout.cs:6`; `C\Engines\ML Quests\Definitions\AthenaeumIsle.cs:89-91` used an API instead of a CRLF
data patch). So `ShardBodyTypes` sets the types in code at Configure. `Body` keeps its table private
(`P\Server\Mobiles\Body.cs:38`, `static readonly BodyType[] m_Types`, filled by the static constructor from
`Data/bodyTable.cfg`, `:40-73`), and the types are getters only, so the array is written through reflection.
- If pinned renames or reshapes the field, `Apply` throws at start: the server does not come up quietly wrong.
- If `bodyTable.cfg` was not found, the table is empty (`Body.cs:42-46`) and `Apply` throws with that reason.
- Alternatives: a patch to `bodyTable.cfg` (a first data-file patch, against a CRLF file the patch step strips CRLF
  from) or a patch to `Body.cs` adding a setter (a core change). Both are heavier for the same result.

**The bodies (15).** The brief's list of 14 **missed 1410**, the dog's stage 5, which `bodyTable.cfg:590` types
Equipment (P59 section B.2). It is included.

| Body | bodyTable.cfg before | Other users found (pinned and `C`) |
|---|---|---|
| 739 | :980 Monster | none |
| 832 | :993 Monster | pinned barkeeper checks only: `PlayerBarkeeper.cs:186`, `BarkeeperGump.cs:15` (a vendor's body, not a creature) |
| 1309, 1426, 1573, 1423, 1547, 1551, 1552 | missing | none |
| 1254 | :1117 Animal (unchanged) | none |
| 1416 | :596 Equipment | **our sabertooth costume** (`C\Items\Equipment\Suits\SabertoothedTigerCostume.cs:12`, a player's BodyMod) |
| 1546, 1548, 1549 | :638-640 Equipment | none |
| 1410 | :590 Equipment | none |

Excluded as not bodies: hues, sounds, item IDs and coordinates with the same numbers.

**What changes for the costume:** a player in it now has an Animal body. Bandages still use Healing (players are excluded,
`P\UOContent\Items\Skill Items\Misc\Bandage.cs:177`). Their weapon swing now sends the animal actions (an Equipment body
sent none: `BaseWeapon.cs:2737-2801`, the default branch returns), which show an attack on 1416; being hit sends 7, which
1416 shows as an attack (the remap is the pet's, not the player's). Small, and better than no swing at all.

**Doors:** `CanOpenDoors => !Body.IsAnimal && !Body.IsSea` (`BaseCreature.cs:1053`). Fact 8: every entry types as
listed, every live stage body is an animal, and a pet on 1547 or 1410 cannot open doors. **The test host does load
`bodyTable.cfg`** (the fact passes after `Apply`; it failed in the red run with the writes removed).

## 5. Part E: animations

**The classic bodies are right as they are** (217, 201, 277, 254, 246, 243: animal layout in `anim.mul` or through
`Bodyconv.def`, every group 0-12 present).

**The UOP-era bodies were wrong.** Pinned sends only packet 0x6E (`P\Server\Mobiles\Mobile.cs:6772-6833`, virtual);
on an Animal body: swing 5 or 6 (`P\UOContent\Items\Weapons\BaseWeapon.cs:2737-2801`), hurt 7 (`:2697-2734`), feed 3
(`BaseCreature.cs:4583-4590`), idle 3, 9 or 10 (`:2985-3010`), anger 10 (`:1762-1769`); death is chosen by the client.
TazUO plays the action number as the group, modulo 13 for an animal (`T\...\MobileAnimation.cs:1458-1505`, `:587-645`),
then applies the body's AnimationSequence replacement (`T\ClassicUO.Renderer\Animations\Animation.cs:281`). The UOP
bodies number their groups in the monster layout (4 and 5 attack, 10 get hit, 22 walk, 25 stand, 26 and 28 idles; no
eat). So, before the fix:

| Body | Swing | Hit | Feed | Idle 9 |
|---|---|---|---|---|
| dogs 1546-1552 | attack | **attack** | **dies** | **attack** |
| 1254, 1416, 1426 | attack | **attack** | **second death** | **attack** |
| 1309 (no replacement table in the data) | 5 right, **6 invisible** | **invisible** | **dies** | **invisible** |
| 739, 832 (MONSTER in mobtypes.txt) | attack | attack | dies | attack |

Packet 0xE2 does not help: TazUO maps it by the Animal type too (`T\...\MobileAnimation.cs:1509-1560`).

**The fix**, `EvoPet.Animate` through `EvoAnimations.Remap`, on the 15 UOP bodies only (fact 9):

| Pinned sends | We send | Why |
|---|---|---|
| 5, 6 (swing) | 4 or 5 | 4 is an attack on every one; 5 is its own attack on most, mapped to 4 on the rest |
| 7 (hurt) | 10 | every UOP body has group 10, get hit |
| 12 (breath) | 4 | 1309 has no 12 |
| 3, 9, 10 (feed, idle, anger) | nothing | no eat or fidget group is reachable; the client plays its own idles (26, 28) |
| anything else | unchanged | death is client-side and right on all of them |

Walking, running, standing and idles are the client's own and right. **Unverified in a client**: the group meanings
(read from renders), 1309's missing table, and anything but TazUO. 739 and 832 are MONSTER in `mobtypes.txt`, so a
missing group falls back to stand there.

## 6. Part B: getting one

- `[EvoPet give <dog|cat|fox|bird>` then target a player: `EvoPet.GivePet(player, line)` makes a stage-1 pet, runs the
  taming path's own steps (`SetControlMaster`, `Owners.Add`, follow order; `P\UOContent\Skills\AnimalTaming.cs:440-446`),
  bonds it at once (F-35: arrives bonded), puts it at their feet and opens the hue picker. No free slot: pinned's own
  message, nothing made (fact 10).
- **The tutorial's Farmhand** will call the same `EvoPet.GivePet(player, "dog" or "cat")` when the player chooses.
- Target an evo pet: `[EvoPet stage <n> [body]` (ignores XP and gates; raises XP to the stage's), `xp <amount>` (adds,
  then steps up as gates allow), `bond <on|off>`, `loops <n|-1>` (stands in for the owner's loop count), `pick <stage>
  <body>` (staff only), `info`.
- Nothing in the world spawns one.

## 7. Part C: the kitsune row

Fox stage 4 in `EvoPetData.Fox`: art-pending, loop 5 and the Bond Trial, with F-35's rules as comments: the fox form
(246) fights; the woman form (female body 401 wearing the fox ears and one tail, the KitsuneEarsTail worn-item route) is
movement only; never send her an attack or cast animation; if she would die in woman form, shift to fox first; auto-shift
into fox on combat and back a few seconds after with a smoke puff, plus a manual command; always female; one tail. No
shapeshift code.

## 8. In-game checklist for Chase (test shard, `sl-modernuo:cc-p65`)

**Bodies (Part E)**: `[EvoPet give dog` on yourself, then `[EvoPet stage <n> <body>` on the pet for each body below. Attack
a rabbit (`[add Rabbit`) or a training dummy, let something hit it (`[add Mongbat` near it), and `[kill` it. You should see:

| Body | Stage | Swing | Hit | Death | Idle |
|---|---|---|---|---|---|
| 217 dog, 201 cat | 1 | bite | flinch | falls | sits, sniffs |
| 739 leather wolf | dog 2 | lunge | flinch (not a lunge) | falls | stands, no eating pose |
| 1546-1549, 1551, 1552 dogs | dog 3 (each pick) | lunge or bite | flinch, not an attack | falls | no death pose while idle |
| 277 cu sidhe | dog 4 | bite | flinch | falls | as stock |
| 1410 windrunner | dog 5 | attack | flinch | falls | client idles |
| 1309 baby tiger | cat 2 (`[EvoPet give cat`) | swipe, **never vanishes** | flinch, **never vanishes** | falls | no vanishing |
| 1254 tiger, 1426 lion | cat 3 | swipe | flinch | falls | no second death |
| 1416 sabertooth | cat 4 | swipe | flinch | falls | as above |
| 1573 manticore | cat 5 | attack | flinch | falls | as above |
| 1423 fox, 246 kitsune | fox 1, 3 (`[EvoPet give fox`) | bite | flinch | falls | 246 as stock |
| 254 crane, 832 phoenix, 243 hiryu | bird 1, 2, 5 (`[EvoPet give bird`) | peck | flinch | falls | 832 flies (its data has a flying flag) |

Also: none of them opens a door (walk it at a closed door with "all follow me" on the far side).

**A dog walked from stage 1 to 5** (about two minutes): `[EvoPet give dog` on your character, pick a hue (try closing
the gump and double-clicking the pet: it comes back). `[EvoPet xp 500`: a flash, an Echo line, a leather wolf.
`[EvoPet xp 2500`: the pick gump opens; close it, double-click the pet, pick a breed: it becomes that dog. `[EvoPet xp 10000`:
it stays, and the Echo says to loop first. `[EvoPet loops 1`: Cu Sidhe. `[EvoPet xp 40000` and `[EvoPet loops 5`: the Echo
says the Bond Trial is not built. `[EvoPet bond on`: windrunner. `[EvoPet info` and `[props` show "at its top for now".
Kill something with it in between and watch `[EvoPet info`'s XP rise.

**A loop reset with a stage-3 pet:** with a stage-3 dog (a breed picked), use the Reset Stone on yourself with everything
ticked. The dog keeps its breed, colour, stage and XP, still follows you, and is still bonded.

**Also**: stable and claim a stage-3 pet (it should come back the same); let it die and resurrect it (bonded, stock).

## 9. Decisions for Chase

1. **XP numbers** (section 3): 500 / 3,000 / 13,000 / 53,000 total, and the kill formula. Tunable as server settings
   without a build; they wait on F-12.
2. **The stat curve** (section 2.3): stage 5 is a Cu Sidhe on 1 slot. Same curve for every line until the roles come.
3. **The hue list** (section 3): seven placeholders. The UOP bodies' art is coloured, so some hues may look odd on them.
4. **The Echo lines** (section 3): placeholders in the Echo's voice.
5. **The Bond Trial**: a staff flag until it is designed.
6. **The pick is permanent** for players (staff can change it). Say if players should get one change.
7. **A released evo pet cannot be re-tamed** by anyone (`Tamable` false). Say if it should be.
8. **Stage names** ("pup", "young hound", "hound", "guardian hound", "windrunner"; "kitten", "cub", "great cat",
   "sabertooth", "manticore"; "kit", "fox", "bake kitsune", "kitsune"; "chick", "firebird", "great bird", "griffin",
   "hiryu"): they are its default name ("a pup") until the owner renames it. Placeholders.
9. **The sabertooth costume** now swings with animal actions (section 4). Fine as is, or exclude 1416 from the change.
10. **When F-12 lands**: set `EvoPet.OwnerLoopsSource` to the real loop count, and add the real reset to fact 7.

## 10. Build and tests

All through `docker\uo\build.sh -t sl-modernuo:cc-p65`; `sl-modernuo:latest` not moved; nothing deployed, restarted or
committed. Logs `D:\UO\cc-p65-build*.log` (not committed).

| Run | Result |
|---|---|
| 1, 2 (`--tests-only`) | compile errors, fixed: `SendGump` needs `using Server.Gumps`; `DamageEntries` is a `ValueLinkList`, walked through `ToArray()` (`P\Server\Collections\ValueLinkList.cs:386`) |
| 3 (`--tests-only`) | 1061/1062: the XP fact caught a real bug, a tame victim gave XP (section 3); fixed |
| 4 **red** (`--tests-only`) | six deliberate breaks (a data row, body never set, no XP handler, no body types, no remap, not bonded): **all 10 evo facts failed**, nothing else did (1052 passed, 10 failed) |
| **5** full build | **1062/1062 passed; image `sl-modernuo:cc-p65` built** ("Built sl-modernuo:cc-p65 with patches applied and 1062 shard test(s) passing") |

The facts (`server\tests\Mobiles\Evo\EvoPetVerification.cs`): 1 the data (lines, live stages, picks, gates, distinct
bodies, curve ends, empty abilities slot); 2 each line at stage 1, and the round trip; 3 XP only from kills it damaged,
none from pets or kills it took no part in; 4 a dog walks its whole line through XP, the pick (once), the loop gate and
the Bond Trial, and `OwnerLoopsSource`; 5 art-pending stages skipped with gates, the top for now; 6 the hue, once, kept;
7 the owner's reset leaves the pet as it was; 8 the body types and doors; 9 the animation remap; 10 `GivePet`, and no
free slot.

The CHANGELOG has 2026.10.12.7 with two staff lines; VERSION is 2026.10.12.7.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the last change:

```
Repo Result
---- ------
code dry run
docs dry run
```

8 files pending in code (5 new evo files, the test, CHANGELOG.md, VERSION), 1 in docs (this note). Nothing refused; no
file near 5 MB.

P65 DONE
