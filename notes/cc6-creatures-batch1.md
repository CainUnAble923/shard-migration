# CC6 batch 1 — twenty creatures, chosen for where they already spawn

Date: 2026-09-19. Agent: Claude Code (Fable 5.1), headless. Pinned ModernUO `7c9215d97`. ServUO pub57.
Files: `server/customizations/Mobiles/Normal/*.cs` (20), `server/customizations/Mobiles/AI/GoblinOppositionGroup.cs`,
`server/tests/Mobiles/Normal/CC6Batch1CreatureVerification.cs`. Also carried: the Q-046 `ShameWall` fix (§8).

**Status: done.** 20 creatures + 1 additive group + 1 test, built through `build.sh` (16 patches, 60 tests green,
6 new), all twenty spawned on the real map by their stock spawners in a headless run, save and reload identical,
final image (probe removed) loads clean. Nothing seen in a client. The S8 test route was extended by one line (§6).

## 1. The selection rule, stated before anything was ported

**Port the creatures the shard's own spawn data already places and cannot spawn.** Pinned ModernUO ships 109
spawn files under `Distribution/Data/Spawns`; the admin gump's "Generate spawners" imports them (`AdminGump.cs:3973-4012`),
`docker/uo/SERVER.md` records that the live shard ran `[GenerateSpawners` for `shared/**`, `post-uoml/**` and `uoml/**`
and generated Ter Mur, and `BaseSpawner.Spawn` resolves each entry through `AssemblyHandler.FindTypeByName` and marks
the entry `EntryFlags.InvalidType` when nothing declares it (`BaseSpawner.cs:1126-1131`). So every entry in that data
whose type is missing is a spawner a player can already walk up to and find empty. Counted from the files, not from
a description of them: **109 distinct entry names resolve to no type in pinned ModernUO plus our tree.** Those 109
are the playability list, and the batch is the low-to-mid-level part of it that is clean to port.

Within the 109, ordered by (entries naming it, then fame low to high); bosses, Renowned and quest NPCs excluded;
"clean" per P2's two checks plus CC3's correction that `SetWeaponAbility` translates.

**Why not "20 from the clean 60%" as briefed:** that 60% is a fraction of all 462 `Mobiles/Normal` files, 325 of which
ModernUO already declares. §2 has the recount. The brief's own goal — creatures a player meets in places they can
already reach — is what the spawn data answers directly, and 18 of these 20 are also in the clean set (the other two
are clean once `SetWeaponAbility` is counted as translating, which CC3 settled).

### The 109, by where ServUO keeps the source

| ServUO source | names | spawn entries | what they are |
|---|---|---|---|
| `Mobiles/Normal` | **53** | 164 | this row is CC6's; 20 ported here, 33 remain (§7) |
| `Mobiles/Named` (Renowned) | 17 | 18 | Abyss renowned bosses and the four Labyrinth elementals |
| `Mobiles/NPCs` + `Quests/` | 15 | 23 | Underworld quest NPCs and the Ter Mur townspeople |
| `Mobiles/Bosses` | 3 | 3 | Medusa, Slasher of Veils, Stygian Dragon |
| not in ServUO at all | 17 | 30 | ModernUO's own names (`EliteNinjaWarrior`, the Clan Chitter/Scratch rats, `GenericGuard`, `Dryada`…); nothing to port, a question for the name-mapping |
| other | 4 | 9 | `TreasureLevel1H`, `DockMaster`, `BoatPainter` (High Seas), `Sphynx` |

Full list with per-name entry counts and files: the `join.txt` table in the session scratch, reproduced in §7 for the
33 `Mobiles/Normal` names not taken here.

## 2. Does P2's 60% survive contact? Yes as a number, no as a plan

P2 measured 275 of 462 `Mobiles/Normal` files clean on both checks (no `new X(` to a missing type, no Pet Training
call). Recomputed today from the same 462 files with the same two checks: **275 clean, 72 with a missing type, 142 with a
Pet Training token** — P2's figure reproduces exactly.

But the denominator is wrong for planning, as `AGENTS.md` already says of every unfiltered count: 325 of those 462
are types ModernUO declares, and 7 more are ours. Of the **130 that are actually candidates**:

| bucket | files |
|---|---|
| clean on both checks | **62** |
| clean except `SetWeaponAbility`, which translates (CC3) | 6 |
| missing type only (a leaf item, a gump, a quest item) | 28 |
| Pet Training only (`SetSpecialAbility` / `SetMagicalAbility` / `SetAreaEffect` / `AbilityProfile`) | 18 |
| both | 16 |

So the pool this batch could draw from is **68 of 130 (52%)**, not 275 of 462, and after this batch it is 48. The
"60%" is true of the tree and says nothing about the backlog. File list: `candidates.txt` (scratch), one line per
file with its missing types and its Pet Training tokens.

**What P2 measured by name and building found otherwise: one thing in twenty files.** `TrapdoorSpider.OnDamagedBySpell`
matched by name and failed by signature (`(Mobile)` on ServUO, `(Mobile, int)` here). One build cycle, 29 seconds.
Everything else the name-match said would compile did.

## 3. The batch, and what each file needed

| # | Type | Spawned by (pinned data) | entries | Fame | Needed beyond the mechanical transformation |
|---|---|---|---|---|---|
| 1 | `GrayGoblin` | Underworld | 6 | 1500 | `TribeType` → `GoblinOppositionGroup` (§4) |
| 2 | `GrayGoblinMage` | Underworld | 3 | 1500 | same |
| 3 | `GrayGoblinKeeper` | Underworld | 1 | 1500 | same |
| 4 | `GreenGoblin` | Underworld | 5 | 1500 | same |
| 5 | `GreenGoblinAlchemist` | Underworld | 5 | 1500 | same |
| 6 | `GreenGoblinScout` | Underworld | 1 | 1500 | same; **AI_OrcScout → AI_Melee** (D-44); `IsPlayer()` → `AccessLevel == Player` |
| 7 | `EnslavedGrayGoblin` | Abyss | 1 (cap 30) | 1500 | nothing |
| 8 | `EnslavedGreenGoblin` | Abyss | 1 (cap 30) | 1500 | nothing |
| 9 | `EnslavedGoblinScout` | Abyss | 1 (cap 30) | 1500 | nothing |
| 10 | `EnslavedGoblinKeeper` | Abyss | 1 (cap 30) | 1500 | nothing |
| 11 | `EnslavedGreenGoblinAlchemist` | Abyss | 1 (cap 30) | 1500 | nothing |
| 12 | `EnslavedGoblinMage` | Abyss | 1 (cap 30) | 1500 | nothing |
| 13 | `TanglingRoots` | Underworld | 2 | 3000 | two `TimerStateCallback<Mobile>` → lambdas; `FountainOfFortune.UnderProtection` is ours (S2) |
| 14 | `SentinelSpider` | Underworld | 1 | 775 | `SetWeaponAbility` → `GetWeaponAbility` |
| 15 | `Gremlin` | Underworld | 1 | none | nothing |
| 16 | `TrapdoorSpider` | Ter Mur | 5 | none | **`CanStealth` has no counterpart: ServUO's `BaseCreature.OnMove` stealth branch inlined** (§4); `OnDamagedBySpell` signature |
| 17 | `Skree` | Ter Mur | 5 | none | **AI_Mystic → AI_Mage** (D-41's shape) |
| 18 | `UndeadGuardian` | Ter Mur (Tomb of Kings) | 2 | none | nothing |
| 19 | `PutridUndeadGuardian` | Ter Mur | 1 | 3000 | nothing |
| 20 | `Spellbinder` | Trammel Outdoors | 2 | 2500 | **AI_Spellbinder → AI_Mage** (D-45) |

46 spawner entries across the four files (`post-uoml/termur/Underworld.json`, `Abyss.json`, `TerMur.json`,
`post-uoml/trammel/Outdoors.json`); the test pins that number.

### Body, hue, sound versus method: the brief's third question

| needs something ModernUO lacks | files | what |
|---|---|---|
| a **body** | **0** | all 11 distinct bodies in the batch (8, 26, 50, 56, 0x9d, 334, 722, 723, 724, 733, 737) are rows in pinned `Distribution/Data/bodyTable.cfg`, five of them annotated with these creatures' names |
| a **hue** or **sound** | **0** | neither is a server-side table on ModernUO; hues and sound ids are client data and pass through as ints. Whether the client renders them is the client check's question, not a port question |
| an **AI type** | 3 | `AI_OrcScout`, `AI_Mystic`, `AI_Spellbinder` (§5) |
| a **BaseCreature virtual** | 1 | `CanStealth` (inlined) |
| a **BaseCreature mechanism** | 6 | `TribeType` (one additive group covers all six) |
| a **signature** | 1 | `OnDamagedBySpell(Mobile, int)` |
| a **helper** | 2 | `IsPlayer()`, `TimerStateCallback<T>` — one-token rewrites |

So for this batch the answer is **method, never appearance**: 0 of 20 need a body, hue or sound; 9 of 20 need a
method or mechanism, and 6 of those 9 are the goblins sharing one 30-line file.

## 4. Two parent members ported with the creatures

- **`TribeType` → `OppositionGroup`.** `AGENTS.md` priced the goblin pair at ~25 additive lines and no patch; it is
  35 lines with comments, `Mobiles/AI/GoblinOppositionGroup.cs`. ServUO under `Core.TOL` (this shard) uses
  `Tribe`/`IsTribeEnemy` in `IsEnemy` (`BaseCreature.cs:1349`) and `IsFriend` (`:1239`); ModernUO consults
  `OppositionGroup.IsEnemy` at the same two points (`:1316`, `:4083`). Membership is by type list, so the six Renowned
  goblins join the lists when ported. The test proves gray ↔ green enmity every pair both ways and no enmity within a
  tribe.
- **The enslaved goblins' `OppositionGroup.SavagesAndOrcs` override is inert on both emulators** and ported unchanged:
  neither list names them (`IndexOf` returns -1), and ServUO under TOL never reads `OppositionGroup` anyway. The test
  pins `IndexOf == -1` and `IsEnemy(enslaved, orc) == false`.
- **`CanStealth`.** ServUO's `BaseCreature.OnMove` (`:4858-4880`) lets a hidden creature with `CanStealth` spend
  `AllowedStealthSteps` and re-roll `Stealth.OnUse` when they run out. ModernUO's `BaseCreature` does not override
  `OnMove`; `Mobile.OnMove` (`Mobile.cs:4071`) reveals any hidden Player-access mobile whose steps are spent, which for
  a creature that just hid is its first step. Inlined as `TrapdoorSpider.OnMove`, the "port the old parent's
  members" shape from `AGENTS.md`. The test walks the spider one step hidden and asserts it stays hidden with steps
  granted, then runs it out of steps and asserts it reveals.

## 5. Deviations — note-local numbering, for `docs/fidelity-principle.md`

Shame ended at D-43.

| # | Deviation | Player notices | Reverses when |
|---|---|---|---|
| **D-44** | `GreenGoblinScout` runs `AI_Melee`; ServUO's `AI_OrcScout` (`Mobiles/AI/OrcScoutAI.cs`) is melee that hides while wandering, teleports to its target 4% of combat thinks, and flees below 20% hits | The scout does not hide, blink or flee; it still sweeps for hidden players every think (ported) | an OrcScout AI in ModernUO (also needed by `OrcScout`, 2 Sanctuary entries) |
| **D-45** | `Spellbinder` runs `AI_Mage`; ServUO's `AI_Spellbinder` (`Mobiles/AI/Magical AI/SpellbinderAI.cs`) is a Magery caster that also spirit-speak heals (5%), teleports (5%) and dispels (75%) | It casts Magery only; no self-heal, blink or dispel | a Spellbinder AI |
| D-41 (Shame's) | `Skree` runs `AI_Mage`; ServUO's `AI_Mystic` casts Mysticism with a 50% Magery fall-through | It casts Magery only; the Mysticism skill is set and unused | a Mysticism AI, the same item as CrazedMage |
| **D-46** | `ShameWall`'s constructor sets `Visible = true` (Q-046). ServUO leaves `BaseAddon`'s `false`, so a fresh wall's teleporters are inert until that wall's troll has died once | Nothing; the wall now behaves the same before and after its first troll. Without the fix a player at a fresh wall could not push through it | never; ServUO's literal value is the bug, the D-10/D-16 shape |

**Not deviations, recorded because they read like typos and are ServUO's:** the enslaved goblins' corpse is
"an goblin corpse"; `EnslavedGreenGoblinAlchemist` is named "Green Goblin Alchemist" with no "Enslaved" and wears the
free goblins' body 723 while its five siblings wear 334; `PutridUndeadGuardian` is "an putrid undead guardian";
`SentinelSpider` is "a Sentinel spider"; `EnslavedGoblinMage` is a melee creature with 510 Int and no Magery;
`GreenGoblinScout.OnThink` does not call the base (so no ML shout), as in ServUO; `Gremlin`, `TrapdoorSpider`, `Skree`
and `UndeadGuardian` set no Fame or Karma. All kept; UOGuide is the reference a player will use and these are what
pub57 shows.

**Q-008 applies to all twenty**: no speed override, every one lands on Medium 0.25/0.5, and the test asserts it.

## 6. What was proved

| Gate | Result |
|---|---|
| `build.sh` (patches, tests, image), FINAL | green, `sl-modernuo:cc6b1`; 16 patches applied, **60 tests passed** (54 before + 6), `structured customizations installed: 524` (503 + 21) |
| Test `CC6Batch1CreatureVerification` (6 facts) | all twenty construct with their ServUO name, corpse name, body, hue, fame and karma, hits > 0, Medium speed (Q-008), and `FindTypeByName` resolves each; **every stock spawn entry naming one of the twenty now resolves**, 46 entries, and exactly 89 of the 109 orphaned names remain (the test reads the 109 JSON files from the test host's `Data/Spawns`, the same files `[GenerateSpawners` reads); gray <-> green goblins are enemies every pair both ways and friends within a tribe; the enslaved goblins' `SavagesAndOrcs` override is inert (`IndexOf == -1`); the trapdoor spider starts hidden, keeps stealth on a walking step (steps granted by `Stealth.OnUse`), reveals when it runs out of steps at a run and when hit; tangling roots entangle a moving player (frozen, pulled onto the roots), the acid ticks (witnessed on the wheel tick it lands, see below), the player is untangled within six seconds and immune for fifteen; sentinel spider's `ArmorIgnore`, skree's taming values and Mysticism, spellbinder's three bodies and `Aggressor`, the scout's range 7, the gremlin's bow and arrows, the guardians' necro reagents, the roots' mandrake, a goblin's boots |
| Headless run 1, fresh save, real map, probe imports the four stock spawn files 3 s after start | `Generated 44 / 22 / 65 / 37 spawners (0 failures)`; **168 spawners, 700 entries, 126 entries still naming no type, 1,820 mobiles**; every one of the twenty live by its stock spawner: GrayGoblin 11, GrayGoblinMage 7, GrayGoblinKeeper 2, GreenGoblin 11, GreenGoblinAlchemist 11, GreenGoblinScout 1 (the Underworld, e.g. 1196,1022,-42), the six enslaved 4/2/1/3/6/6 (the Abyss goblin warren, e.g. 582,814,-45), TanglingRoots 5, SentinelSpider 1, Gremlin 1, TrapdoorSpider 10 and Skree 11 (Ter Mur, e.g. 1090,3729,-43), UndeadGuardian 7 and PutridUndeadGuardian 7 (Tomb of Kings, e.g. 37,92,-5), Spellbinder 20 (**Old Haven, 3705,2471,19**, Trammel); **127 live**; `Saving world done`, snapshot written, `Shutting down`; no warning but the three every fresh save prints |
| Headless run 2, reload run 1's save | `Loading world done (3603 items, 1836 mobiles)`; "32 spawners naming this batch present from save"; **every per-type count and sample location identical to run 1**, 127 live; save, shutdown, clean |
| Headless run 3, the final image (probe removed), fresh save | `Loading world done (617 items, 90 mobiles)`, listeners on 127.0.0.1, `Saving world done`, snapshot written, `Shutting down`; no `[cc6b1]` line, no warning but the usual three |
| Red proofs | build A: the `OnDamagedBySpell` signature (compiler); builds B and C: the trapdoor fact failed with the skill-check handler unwired and the roots fact with a fixed advance; build D: a throwaway diagnostic fact printed what the host does (timers fire, direct damage registers, `DamageEntries` cleared on full hits, `SkillCheckLocationHandler` null); build E green with the fixture line and the poll, nothing else changed in those facts |

Probe (`server/customizations/Probe/CC6Batch1Probe.cs`, deleted before FINAL, never committed): `Initialize` arms a 3 s
timer; on a fresh world it makes a Developer-access `PlayerMobile` and runs `CommandSystem.Handle` for
`[GenerateSpawners` on each of the four files, exactly what the admin gump does; then it counts spawner entries and
live instances per type. Harness in `%LOCALAPPDATA%\Temp\cc6b1\` (`run.sh`, the loopback `conf`, the logs).

**What the two test-host gaps were, because both looked like creature bugs for a build each:**

- **`HitsTimer` regeneration** (the Q-029 shape, already in Shame's mana-taint fact): a 4-point acid tick on a player
  is regenerated within the same fixed advance, and `Mobile.Hits`'s setter clears `DamageEntries` on full hits
  (`Mobile.cs:2022`), so neither hits nor the damage table witnessed it. Walk the clock one 8 ms tick at a time and
  read the entry on the tick it lands. Written into the fact.
- **`SkillCheckLocationHandler` is null in the test host.** The fixture's hand-picked list never calls
  `SkillCheck.Initialize`, so `Mobile.CheckSkill` is false for everything and `Stealth.OnUse` reveals the user.
  Fixed in the route, one line in the S8 fixture patch (`notes/s8-test-route.md` §12), not in the test. Any earlier
  test that rolled a skill would have taken its failure branch silently; none did, which is how it stayed hidden.

**Not verified, per the standing rule, and batched for the client spot check:** appearance of all twenty (bodies 8,
26/50/56, 0x9d, 334, 722, 723, 724, 733, 737; hues 1900 on the gray goblins, 1141 on the sentinel spider; the goblin
sound set 0x5FD-0x600 and the SA sound ids 1582-1609), the tangle in motion, the trapdoor spider's hide effect, and
whether the live world's spawners exist (Q-048).

## 7. The 33 `Mobiles/Normal` names still orphaned in the spawn data, for batch 2

Ordered by entries; the bucket is from §2's table.

| name | entries | bucket | what it needs |
|---|---|---|---|
| `Slith` | 12 (cap 184, the most-placed creature in Ter Mur) | both | `SlithEye`, `TatteredAncientScroll` (leaf items), one `SetSpecialAbility` |
| `SerpentsFangAssassin` | 11 | clean | nothing; fame 13000, the Citadel |
| `ChickenLizard` | 8 | missing | `ChickenLizardEgg` (an item with its own hatching mechanic; read it before pricing) |
| `ToxicSlith` | 8 | both | the two slith items + `ToxicVenomSac`, one ability |
| `DragonsFlameMage` | 8 | clean | nothing; fame 13000, the Citadel |
| `Rotworm` | 7 | both | `ArielHavenWritofMembership`, one ability; fame 500, the Underworld |
| `RuddyBoura` | 6 | both | `BouraSkin`, `Fur`, one ability; tameable |
| `StoneSlith` | 6 | both | slith items, `SetWeaponAbility` ×2 (translates) + `SetSpecialAbility` ×3 |
| `TrapdoorSpider`… | — | — | ported |
| `HighPlainsBoura` | 5 | both | `BouraSkin`, `BouraTailShield`, `Fur`, two abilities |
| `TigersClawThief` | 5 | clean | nothing; fame 13000, the Citadel |
| `KepetchAmbusher` | 4 | missing | `Fur`, `KepetchWax` |
| `WolfSpider` | 4 | pet | `SetMagicalAbility` + `AbilityProfile` |
| `FireAnt` | 3 | both | `SearedFireAntGoo`, `SetAreaEffect` |
| `LavaElemental` | 3 | clean | nothing; the Abyss, fame unset |
| `FireDaemon` | 3 | pet | `SetSpecialAbility` + `SetAreaEffect`; fame 15000 |
| `CoralSnake` | 2 | pet | `SetMagicalAbility` + `AbilityProfile`; fame 300 |
| `SkeletalLich` | 2 | clean(wa) | `SetWeaponAbility`; fame 6000 |
| `AcidSlug` | 2 | missing | `AcidSac`, `CongealedSlugAcid` |
| `Kepetch` | 2 | both | `Fur`, one ability |
| `BloodWorm` | 2 | pet | one `SetSpecialAbility` |
| `CrystalHydra` | 2 | both | `ShatteredCrystals`, one ability; fame 17000 |
| `OrcScout` | 2 | missing | `Yeast`; and it wants the OrcScout AI (D-44) |
| `MaddeningHorror` | 1 | both | `VileTentacles`, one ability; fame 23000 |
| `PitFiend` | 1 | clean | nothing; fame 18000 |
| `ClockworkScorpion` | 1 | pet | `SetMagicalAbility` + `AbilityProfile` |
| `ClanRibbonPlagueRat` | 1 (cap 15) | clean | nothing; fame 150 — note our `PlagueRat` (P1) is ServUO's *other* plague rat, named "a Clan Ribbon Plague Rat", and this one is a different type with body 238 |
| `FairyDragon` | 1 | missing | `DraconicOrb`, `FairyDragonWing`; fame 15000 |
| `ForgottenServant` | 1 (cap 35) | clean | nothing; fame 2500 |
| `LowlandBoura` | 1 | both | `BouraSkin`, `Fur`, one ability |
| `GargoyleShade` | 1 | clean | nothing; fame 4000 |
| `Niporailem` | 1 | missing | 14 Virtuous Epiphany pieces (CC9 ported the set; check the names) + treasure + sword |
| `IronBeetle` | 1 | both | one of the four hard-blocked Pet Training creatures (S3) |
| `SerpentsFangHighExecutioner` | 1 | missing | `SerpentFangKey`; fame 25000 |

**Batch 2, by the same rule:** the six clean ones (`LavaElemental`, `ForgottenServant`, `ClanRibbonPlagueRat`,
`GargoyleShade`, `SkeletalLich`, and the three Citadel humans if 13000 fame counts as mid), then the `Fur`/`BouraSkin`
leaf cluster (three boura + two kepetch, 5 creatures for 3 items) with their single abilities dropped on the
Saurosaurus precedent, then the slith cluster (3 creatures, 3 items). That is 19-22 files and would take the
`Mobiles/Normal` orphan row from 33 to about 12, all of them Pet-Training-only or high-level.

## 8. The Q-046 fix, carried along

`ShameWall.cs`: `Visible = true` at the end of the constructor, header comment rewritten to say why; `CanTeleport`
untouched. `ShameRevampedVerification.TheCaveTrollWallSinksAndComesBack…` had pinned the old reading
(`Assert.False(wall.Visible)` on a fresh wall); its two assertions flip to `True` and the comment says why. D-46 above.
Read, built, tested; not seen in a client — it stays on `docs/client-check-backlog.md`'s Shame list, where §9.1's
"stand in front of a fresh wall" check now expects to walk through it before the troll dies.

## 9. What it cost

Wall clock, local time, one session, headless. Session start about 15:21 (first tool output 15:23:41, after
`AGENTS.md` and `docs/tasks.md`).

| Phase | From | To | Elapsed |
|---|---|---|---|
| Orientation: `AGENTS.md`, `docs/tasks.md`, `notes/cc2-timed-port.md`, Q-046, the port recipe, the Despise and Shame notes' methods, `SERVER.md` | ~15:21 | 15:25 | ~4 min |
| The measurement: type index of pinned ModernUO + ours (6,732 + 1,032 declarations), the 462-file survey with P2's two checks, ServUO's spawn XML index, pinned ModernUO's spawn JSON index, the join, the categorisation | 15:25 | 15:29 | 4 min |
| Q-046 fix in `ShameWall.cs` and its test | 15:29 | 15:31 | 2 min |
| Selection and pre-flight: reading the 20 ServUO files (12 as diffs against one), every non-trivial member against pinned ModernUO, the tribe mechanism on both sides, the three AIs, `CanStealth`, the body table, the timer and effects signatures, the spawner import path, the previous session's harness | 15:31 | 15:36 | 5 min |
| Writing: 20 creatures (12 generated from a value table, 8 by hand), the group, the test, the probe, the harness | 15:36 | 15:44 | 8 min |
| Build A (29 s, one signature) -> B (2:27, 58/60) -> C (3:37, 58/60) -> D (diagnostic, 59/60 by design) -> E (green, 60) | 15:44 | 16:00 | 16 min, of which ~11 min inside `build.sh` |
| Headless run 1 (2:50, imports + save), run 2 (2:00, reload), FINAL build (3:30), run 3 (1:45) | 16:00 | 16:11 | 11 min |
| **To the final image, end to end** | **~15:21** | **16:11** | **~50 min** |
| Notes, state, questions, `progress.py`, commits | 16:11 | | ~20 min |

Against P2's estimate of ~1 hour for a batch of 20: **~50 minutes to a verified image, ~70 with the write-up**, so the
estimate held, but for different reasons than P2 gave. P2 priced 20 files at 1:10 each of reading and transforming
plus 0:44 per build; here the transformation was 8 minutes for all 20 (twelve near-identical goblins generated from
their values) and the builds were 2.5-3.5 minutes each through the gates, not 44 s (S5's correction). What ate the
middle of the hour was **the test host, not the creatures**: two of five build cycles were spent on host gaps that
looked like creature bugs, and the diagnostic build that told them apart was the cheapest step in the session. The
verification (test + three headless runs) is 27 of the 50 minutes, which is CC3's "verification is half the cost"
again.

Context: about 1.1M tokens of the 15M budget at this line (13.9M left). Compare CC3's 278k for 17 leaf files: the
measurement and the two host gaps roughly tripled a leaf batch.

## 10. Questions

- **Q-048** (non-blocking): the live world's spawners. `SERVER.md` says `[GenerateSpawners` ran for `shared/**`,
  `post-uoml/**` and `uoml/**`; `Saves/` was never read. If that holds, the twenty start spawning on the next deploy
  with no action, because the spawner entries are already there and `Spawn` re-resolves the name every tick. If the
  Underworld/Abyss/Ter Mur files were never generated live, `[GenerateSpawners Data/Spawns/post-uoml/termur/**.json`
  once, then `[save`. Either way it is a client-check item: stand in the Underworld's goblin rooms and count.
- The 17 names ModernUO's spawn data uses that ServUO has no type for (`EliteNinjaWarrior`, `MageDragonsFlameMage`,
  the seven Clan rats, `Dryada`, `GenericGuard`, the five Underworld NPC names, `BodySculptor`,
  `EscortableWanderingHealer`) are ModernUO's own naming, presumably for types upstream has not written yet.
  Whether any is a ServUO type under another name is a name-mapping question for the NPC batch, not this one.
