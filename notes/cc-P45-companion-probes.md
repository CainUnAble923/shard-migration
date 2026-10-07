# cc-P45: companion probes (risky classes and unverified engine behavior)

Written 2026-10-06 by CC from `D:\UO\cc-prompts\cc-P45-companion-probes.md`. Notes plus throwaway probe code only.

- **Engine:** `D:\UO\ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88` (checked with `rev-parse HEAD`).
  Citations below are as of that commit, paths relative to `Projects\`. "Ours" means `D:\ShatteredLegacy\server\`.
- **Shard:** a throwaway worktree of `D:\ShatteredLegacy` at `29db3d5` (detached), `D:\SL-probe-companions`. P66 was
  building in the main tree the whole time; nothing of mine touched it (see section 9).
- **How the probes ran:** 41 xUnit facts in the shard test route, plus one probe creature in `customizations\Probes\`.
  Built with `docker/uo/build.sh -t sl-modernuo:cc-p45-probe --tests-only` (builder `sl-uo-builder:cc-p45-probe`; no
  runtime image was built and `sl-modernuo:latest` was not touched). Iterations then ran only the P45 facts against
  that builder with the probe folders mounted. Final run: **41 passed, 0 failed**. In the full-suite build the other
  876 shard tests all passed beside the probes.
- **Evidence kept:** the worktree is gone, so every probe source and the final run's output are copied to
  `notes\reference\cc-P45-probes\` (9 `.cs` files, 1,791 lines, and `final-run-output.txt`). The "Actual" column
  below quotes that output.
- **Pinned citations in the brief re-checked at d4531cd94, all hold:** `Bandage.cs:454-546` (BeginHeal),
  `PlayerMobile.cs:3408-3440` (OnMove), `BaseCreature.cs:2504-2507` (abandoned-pet delete), `AITimer.cs:149`,
  `Spell.cs:260-262` (reagents; the brief's 260-263 is one line long), `HealerAI.cs:138`, `SamuraiSpell.cs:28-29`,
  `SkillCheck.cs:142` (pet gain x2).

Decided 2026-10-03 07:25 and folded in, not re-argued: **companions log out with their owner** (probe 6 builds on
it), and **free casting** (no reagents, no disturb; probe 7 casts with neither).

---

## Summary

| # | Probe | Verdict | Seam or patch | Size |
|---|---|---|---|---|
| 1 | Healer: bandage owner and sibling, gain, cure, resurrect, potions | **WORKS** | Real `Bandage.OnDoubleClick` then `Target.Invoke`; AI drives it from `OnThink` or the `ForcedAI` | 0 patches |
| 2a | Bard: targeted Peacemaking, Provocation, Discordance, gains | **WORKS** | Real handlers through `UseSkill` + `BaseInstrument.SetInstrument` + `Target.Invoke` | 0 patches |
| 2b | Bard: area Peacemaking that spares the party | **WORKS WITH OUR CODE** | Stock area mode calms the owner and siblings; our own area routine with the stock math | S, ours |
| 3a | Rogue: hide, stealth, step count, attack from hiding, revealed by players | **WORKS** | Real `Hiding`/`Stealth` handlers; stock `Mobile.OnMove` counts steps | 0 patches |
| 3b | Rogue: re-stealth when steps run out, running costs 2 steps | **WORKS WITH OUR CODE** | Override `OnMove` on the companion, copy of `PlayerMobile.OnMove` | S, ours (30 lines) |
| 3c | Rogue: monsters' Detect Hidden | **WORKS WITH OUR CODE** (parity gap) | Monster AI only ever reveals **players**; reproduce its roll for companions | S, ours |
| 3d | Rogue: lockpicking, Remove Trap, poisoning its own weapon | **WORKS** | Real `Lockpick`, `RemoveTrap`, `Poisoning` targets | 0 patches |
| 4 | Fight back while following; party-wide guard | **WORKS WITH OUR CODE** | `ForcedAI` overriding `DoOrderFollow`/`DoOrderGuard`; plus `StandsDownOnCommand => false` | S, ours |
| 5 | Room registry against the 3-day abandoned-pet delete | **WORKS WITH OUR CODE** | Registry sets `IsStabled` at load; the setter stops the timer | 0 patches |
| 6 | Logout with owner; restart while logged out; roomed stays roomed | **WORKS WITH OUR CODE** | `EventSink.Logout` + `PlayerMobile.PlayerLoginEvent`; `CanAutoStable => false` (ours) | S, ours |
| 6g | A ghost companion logged out | **WORKS WITH OUR CODE** | Dead-pet abandon sweep deletes it after 1 day unless `IsStabled` is set while away | S, ours |
| 7 | Target relay: owner's cursor, companion's spell | **WORKS** | `Target.Invoke(companion, picked)`; range and LOS run from the companion | 0 patches |
| 8 | Looting rights and criminal flags | **WORKS WITH OUR CODE** | Judge by the **owner** (`Corpse.CanLoot/IsCriminalAction(owner)`), then move items by code | S, ours |
| 9 | Mounts: ethereal and real, follow owner's mounted state | **WORKS WITH OUR CODE** | `Rider = companion` by code, from `OnThink`; no region in pinned blocks mounts | S, ours |
| 10 | Necromancy transformation spells by a creature | **WORKS** | Stock `TransformationSpellHelper.OnCast` | 0 patches |
| 11a | Penitent: damage scales up as health drops | **WORKS WITH OUR CODE** | `AlterMeleeDamageTo` / `AlterSpellDamageTo` on the companion | S, ours |
| 11b | Penitent: share of party damage moved to it | **WORKS WITH OUR CODE** for companions; **NEEDS PINNED PATCH** for a player | Companions: our `Damage` override. Players: one call in `AOS.Damage`, best as a line in ours `AOS-damage-eater-hook.patch` | 1 to 3 lines |
| 11c | Penitent: cheat death, heal the party | **WORKS WITH OUR CODE** | `OnBeforeDeath` returns false, `Hits = 1`, heal party | S, ours |
| 12a | Otherworlder: plot armor | **WORKS WITH OUR CODE** | `OnBeforeDeath` + temporary `Blessed` | S, ours |
| 12b | Otherworlder: party buff by companion count | **WORKS WITH OUR CODE** | `AddStatMod`/`AddResistanceMod` on every party member, players included | S, ours |
| 12c | Otherworlder cheat skills (Appraisal, Item Box, Fortune, Quick Study) | **WORKS WITH OUR CODE** (Fortune through an existing patch seam) | See 12c; nothing new in pinned | S each |
| 13 | One cheat-death cooldown per party | **WORKS WITH OUR CODE** | Per-owner state in the companion registry | S, ours |

**Pinned patches newly required by P45: 0 for the design as written, 1 optional** (Shared Burden on a player, 11b).
P41's four parity patches (gain x2, pet stat delay, Bushido, resurrection loss) are unchanged and still needed.

---

## A. The risky classes

Common setup for every probe: a `PlayerMobile` owner and one or more `P45ProbeCompanion`s
(`notes\reference\cc-P45-probes\P45ProbeCompanion.cs`): `BaseCreature`, body 0x190, `SetControlMaster(owner)`, bonded,
ordered `Follow` the way "all follow me" does, `Skills.Cap = 100000`, **no `SetDamage`**, and a static `AIFactory`
read by `ForcedAI`. The fixture does not run skill handlers' `Initialize`, so each probe calls the ones it uses (the
live server reaches them through `AssemblyHandler.Invoke("Initialize")`).

### A1. Healer: **WORKS**

| Test | Expected (pinned) | Actual |
|---|---|---|
| Companion double-clicks its bandages and the cursor is `Invoke`d on the owner at 20/100 hits (Healing and Anatomy 100, Dex 100) | AOS other-heal delay `3.2 - sin(dex/130) * 2.5` = 1.46 s (`Bandage.cs:508`); heal `anat/8 + heal/5 + 4` to `anat/6 + heal/2.5 + 4` = 36.5 to 60.7; one bandage consumed (`:100`) | delay **1.46 s**; hits **20 -> 73**; bandages **50 -> 49** |
| Same, on a sibling companion at 20/150 | Primary skill **Healing** (human body, `:172-180`), same formula | 1.46 s, **20 -> 81**, primary Healing |
| Self-heal | `5 + 0.5 * (120 - dex) / 10` = 6.0 s (`:493`) | **6.00 s** |
| 60 bandages on a sibling at Healing 50 / Anatomy 50 | `CheckSkill` both at the end of every tick (`:442-446`) | Healing **50 -> 55.2**, Anatomy **50 -> 55.5** |
| Owner poisoned (Lesser), bandage | Cure branch, chance `(heal - 30)/50 - level*0.1` = 1.4 (`:321`) | **cured** |
| Sibling killed (bonded, dead pet), Healing 120 | Non-master healer: `PetResurrectGump` to the master (`:277-282`) | **gump sent to owner**; companion stays dead until the owner accepts |
| Owner killed, ghost in war mode | Res chance `(120 - 68)/50` = 1.04; `ResurrectGump` to the patient (`:312`); delay +5 s for res (`:487`, `:508`) | **ResurrectGump sent**, delay **6.46 s** |
| Same, ghost **not** in war mode | `Target.Invoke` refuses an unseen target (`Server/Targeting/Target.cs:182-185`); a living mobile cannot see a ghost unless it manifests (`Server/Mobiles/Mobile.cs:7242-7243`) | `CanSee(ghost)` **false**. This is the player rule too. |
| Greater Heal and Greater Cure potions, real `OnDoubleClick(companion)` | `CanDrink` + `Drink` take any mobile (`BasePotion.cs:133-188`) | heal **20 -> 44**, potion consumed, empty bottle in pack; poison **cured** |

Healing uses the healer's own skill and Dex exactly as a player's. **Gain differs:** a controlled creature's gain
chance is doubled (`Skills/SkillCheck.cs:140-143`), already P41's parity patch 1. **Seam:** the companion's AI picks a
patient (owner, sibling, self by need) from `OnThink` or inside our `ForcedAI`, then runs the player path above:
`bandage.OnDoubleClick(this)`, `Target.Invoke(this, patient)`. Do **not** use pinned `CanHeal`/`CanHealOwner`
(`BaseCreature.cs:1466-1467`, default false; the separate non-bandage `HealStart` path P41 2.4 describes).

**Verdict: Support ships as designed.** Cleric (healing plus Chivalry) is unaffected by P45.

### A2. Bard: targeted **WORKS**, area **WORKS WITH OUR CODE**

The handlers need no `PlayerMobile` and no client cursor. The companion's instrument is set with the public
`BaseInstrument.SetInstrument(from, item)` (`Items/Skill Items/Musical Instruments/BaseInstrument.cs:353-356`), so
`PickInstrument` skips its own cursor (`:214-223`); `UseSkill` then leaves the skill's `Target` on the companion,
which our AI `Invoke`s.

| Test | Expected | Actual |
|---|---|---|
| Peacemaking, targeted, on a mongbat attacking the owner (Musicianship and Peacemaking 120) | Target mode pacifies a `BaseCreature` (`Skills/Peacemaking.cs:137-209`) | target `Peacemaking+InternalTarget`; mongbat **pacified 1:48**, combatant cleared |
| Peacemaking on itself (area mode) with the owner and a sibling in war mode | Area mode calms **every** mobile it `CanBeHarmful` (`:103-123`) | monster pacified, **owner's combatant cleared and war mode off, sibling pacified** |
| Provocation, monster A onto monster B | `Provoke` (`Skills/Provocation.cs:154-166`) | **A provoked**, A's combatant B, BardMaster = companion |
| Provocation on the owner | First target must be a `BaseCreature` (`:47`) | refused (no second cursor) |
| Provocation, monster onto a sibling companion | Second target only needs to be a `BaseCreature` (`:106`) | **accepted**: the monster turns on the sibling. Our AI must never pick a pet. |
| Discordance on a ratman, Discordance 120 | AOS effect `-20 + (120 - 100)/-2.5` = -28 to all resists (`Skills/Discordance.cs:177-201`) | effect **28**, physical **28 -> 0** |
| Discordance on a player | `!targ.Player` only (`:152`) | **no effect** |
| 80 area peaces, then 80 discords on fresh ettins, all at 50 | Gains through `CheckMusicianship` and `CheckSkill`/`CheckTargetSkill` | Musicianship **50 -> 63.9**, Peacemaking **50 -> 54.2**, Discordance **50 -> 54.2** |

Monster-only targeting (design: Troubadour never targets players): Provocation and Discordance enforce it for
players already; targeted Peacemaking does **not** (`Peacemaking.cs:142` is only `CanBeHarmful`), so our AI's target
choice enforces it. **Area peace cannot be restricted** without our own routine: same range
(`GetBardRange`, `BaseInstrument.cs:212`), same `CheckMusicianship` and `CheckSkill(Peacemaking, 0, 120)`, same
`Pacify(from, now + 1 s)`, but skipping the owner, the owner's followers, other players and their pets. About 40
lines, no patch. Gains differ by the pet x2 only.

Note for P66 (in flight, section 9): its `Bard-musicianship-reduction-osi.patch` changes the `music` term on these
same three lines through `ClusterFSkillClamps.MusicianshipReductionSkill(from)`.

**Verdict: Troubadour ships as designed**, with our area routine.

### A3. Stealth rogue

| Test | Expected | Actual | Verdict |
|---|---|---|---|
| `UseSkill(Hiding)` at Hiding 100 | `CheckSkill(Hiding, 0, 100)` at 100 is no challenge (`Skills/Hiding.cs:71`) | **hidden** | WORKS |
| `UseSkill(Stealth)` at Stealth 100 | Steps `Stealth / 5` under AOS (`Skills/Stealth.cs:99`); `IsStealthing` is set only for a `PlayerMobile` (`:101-104`) | **20 steps** | WORKS |
| Stock movement, walking | `Mobile.OnMove` counts down for any Player-access mobile and reveals at zero (`Server/Mobiles/Mobile.cs:4116-4127`) | revealed on **step 21** | WORKS |
| Stock movement, running | Stock reveals on any running step | **revealed** at once | differs from player |
| Real `Mobile.Move(East)` while stealthed | `Move` calls `OnMove` (`Mobile.cs:4096`) | moved one tile, steps **20 -> 19**, still hidden | WORKS |
| Our `OnMove` override, a copy of `PlayerMobile.OnMove` (`PlayerMobile.cs:3408-3440`) | Re-runs `Stealth.OnUse` when steps run out; running costs 2 | still hidden after **200** steps; running **20 -> 18** | WORKS WITH OUR CODE |
| Hidden, ordered to attack an adjacent mongbat | The swing reveals (`Mobile.cs:801-806`, `CheckCombatTime`) | hidden until the first swing, then **revealed** | WORKS |
| Monster with Detect Hidden 100, `AIObject.DetectHidden()` x60, hidden companion and hidden player (Hiding and Stealth 100) both in range | Monster AI only considers `trg.Player` (`Mobiles/AI/BaseAI/BaseAI.cs:1144-1145`) | companion revealed **0/60**, player **27/60** | **parity gap** |
| Player detector, Detect Hidden 100, area scan x40 | Contest `skill +-10` vs Hiding `+-10` for any mobile (`Skills/DetectHidden.cs:187-206`) | revealed **19/40** | WORKS |
| Monster `CanSee(hidden companion)` | Hidden is unseen at equal access (`Mobile.cs:7239-7241`) | **false** | WORKS |
| Lockpick on a locked chest (lock 50-90), Lockpicking 100 | 3 s timer, `CheckTargetSkill` (`Items/Skill Items/Thief/LockPick.cs:82-140`) | **unlocked**, `Picker` = the companion | WORKS |
| Remove Trap on an explosion-trapped chest | Needs Lockpicking and Detect Hidden 50 (`Skills/RemoveTrap.cs:16-28`) | trap **None**, no damage | WORKS |
| Poisoning: Greater Poison onto its own dagger | Dagger has Infectious Strike (`Items/Weapons/Knives/Dagger.cs:16`); charges `18 - 2 * level` (`Skills/Poisoning.cs:133`) | dagger **Greater, 14 charges**, karma -20 | WORKS |

**Guards** reveal only the mobile they are chasing (`Mobiles/Guards/WarriorGuard.cs:170`,
`ArcherGuard.cs:159`), so a hidden companion is revealed by a guard only if it is the guard's target. Read, not
probed. **Passive** detection (`DetectHidden.TryDetectStealther`, `DetectHidden.cs:61-128`) is Felucca PvP and checks
`CanBeHarmful`, party and guild, which a companion is outside; not probed.

**The parity gap and its fix (ours):** a hidden companion is invisible to every monster's Detect Hidden, where a
hidden player is not. The companion can roll the monster's own formula on itself from its `OnThink`: for each
monster in range with Detect Hidden, `max(dh/10, dh/1.2 - min(hiding/2.9, stealth/1.8)) / 100`
(`BaseAI.cs:1147-1160`), on the monster's own cadence (`AITimer.cs:151`, `:233`). About 30 lines. The alternative,
dropping `trg.Player` from `BaseAI.cs:1144`, is a pinned patch and would also change every non-player hider; not
recommended.

**Verdict: Rogue ships as designed** (no Stealing, per the design), with our `OnMove` override and our
monster-detection roll. Assassin and Trickster are covered: poison and burst from stealth, locks and traps all run
the real handlers.

---

## B. Other unverified items from P41

### 4. Fight back while following: **WORKS WITH OUR CODE**

| Test | Actual |
|---|---|
| Stock, following, a ratman attacks the owner; one `Obey()` | combatant **null** (`PetOrders.cs:37-39`) |
| Stock, following, the ratman attacks the companion | combatant **null**, order Follow (`BaseAI.cs:146-155`) |
| Stock, guarding, a ratman attacks a sibling | combatant **null**: pinned `FindGuardTarget` covers master and self only (`PetOrders.cs:785-837`) |
| `StandsDownOnCommand => false` on the companion, then attacked | order **Attack**, target the ratman (`BaseAI.cs:159-163`) |
| Our `P45ProbeFollowAI : MeleeAI` overriding `DoOrderFollow` and `DoOrderGuard`: owner, sibling, self attacked in turn | combatant **Ratman** each time, order stays **Follow**; under Guard a sibling's attacker is engaged, order stays **Guard** |

Seam: `ForcedAI` (`BaseCreature.cs:1063`), the virtuals at `PetOrders.cs:628` and `:668`, and the `internal`
`IsGuardAlly` (`PetOrders.cs:773-779`), which our code can call because customizations compile into UOContent. The
threat scan is ours (about 30 lines; `FindGuardTarget` is private). `StandsDownOnCommand` (`BaseCreature.cs:1387`)
is a one-line override that also gives "answers a direct attack". No pinned patch.

### 5. Room registry load order: **WORKS WITH OUR CODE**

**Correction to P41 6(b) and to the brief's framing:** `[AfterDeserialization]` is **not** deferred. It runs inside
the creature's own generated `Deserialize`.

| Test | Actual |
|---|---|
| Roomed companion (internalized, `SetControlMaster(null)`, `IsStabled`, `StabledBy`, `Owners` holding the owner), serialize, reset `IsStabled` (not saved), deserialize into the same object | right after `Deserialize`: **AfterDeserialization had already run** (the AI object was rebuilt, `BaseCreature.cs:2512`) and the **3-day delete timer was running** |
| Then set `IsStabled = true` as the registry's load would, advance 64 ms | timer **stopped** |
| No registry | timer running, delay **3.00:00:00** |
| A companion only given `SetControlMaster` (never tamed) | `LastOwner` **null**: `Owners` is filled by taming, not by `SetControlMaster`, so the delete branch (`BaseCreature.cs:2504`) never fires for it at all |

**Which runs first, proved:** the Mobiles persistence has priority 1 (`Server/World/World.cs:684`) and
`Persistence.Load` deserializes in priority order (`Server/Serialization/Persistence.cs:54-68`); a
`GenericPersistence` registry runs later (`ChampionTitleSystem` uses 10, `Engines/CannedEvil/ChampionTitleSystem.cs:37`).
So the creature's delete timer **always starts first**, and the registry wins anyway because the `IsStabled` setter
stops it (`BaseCreature.cs:897-906`). That is also how pinned's own stables survive (`PlayerMobile.cs:3099-3108`).
`ShouldSerializePendingDeleteTimer` then keeps it out of the next save (`BaseCreature.cs:757-758`). No patch.
Caveat: this is a serialize/deserialize of one object in the test host, not a world save and restart; the ordering
argument above is from the source.

### 6. Logout with owner: **WORKS WITH OUR CODE**

Seam: subscribe to `EventSink.Logout` (pinned uses it at `PlayerMobile.cs:944`, handler `:1520-1523`) and
`[OnEvent(nameof(PlayerMobile.PlayerLoginEvent))]` (`PlayerMobile.cs:1234-1277`). Ours
`patches\BaseCreature-PlayerMobile-can-auto-stable.patch` with `CanAutoStable => false` keeps companions out of
`AutoStablePets` on logout and at startup (`CheckPets`, `PlayerMobile.cs:1064-1083`).

The shape probed: at logout, `ControlOrder = Stay` and `Internalize()`, **keeping the control master**; at login,
`MoveToWorld(owner)` and `IssueOrder(Follow, owner, owner)`.

| Step | Actual |
|---|---|
| Logout (pinned auto-stable runs too) | companion on **Internal**, still **controlled**, **not** auto-stabled; the roomed one stays Internal and stabled |
| Restart while logged out (serialize, clear owner's unsaved followers, deserialize, startup auto-stable) | followers rebuilt to **1**, companion in `AllFollowers`, **no delete timer** (it is controlled) |
| Login | companion **on the owner's tile, order Follow**; the roomed one **still roomed**; followers **1** |

**Ghost companions need the registry marker:** the hourly loyalty sweep deletes a dead bonded pet whose owner is out
of sight for `BondingAbandonDelay`, one day (`BaseCreature.cs:5986-6006`, `:1391`). Probed: a ghost companion logged
out with its owner was **deleted** after one simulated day; the same with `IsStabled = true` while away was **not**.
So logout sets `IsStabled = true` (and login clears it), and since `IsStabled` is not saved, the registry restores it
at load, the same mechanism as rooms. Overriding `BondingAbandonDelay` to `TimeSpan.MaxValue` is not an option: the
sweep adds it to a `DateTime` (`:5998`), which would throw.

### 7. Target relay: **WORKS**

Companion casts Fireball (free casting) with `Stay` so it does not walk; the owner gets a relay target whose
`OnTarget` calls `companion.Target.Invoke(companion, picked)`.

| Pick | Companion to target | Owner to target | Actual |
|---|---|---|---|
| Near the companion | 5 | 14 | **25 damage** |
| Near the owner | 14 | 5 | **0 damage** (out of the spell's range) |

`Target.Invoke` checks range, visibility and LOS from the mobile it is called for (`Server/Targeting/Target.cs:178-190`),
and the spell target's range is the spell's (`Spells/Targeting/SpellTarget.cs:22-27`). LOS was not separately
probed: the test host has no map files (`map0.mul was not found`), so every LOS check passes there; the code path is
the same `from.InLOS` call.

### 8. Looting: **WORKS WITH OUR CODE**

| Test | Actual |
|---|---|
| Owner kills a ratman; companion lifts its gold, **Trammel** | `IsCriminalAction(owner)` false, `(companion)` **true**; `CanLoot(companion)` false: **lift refused** |
| Same, **Felucca** | lift succeeds and **both the companion and the owner are flagged criminal** |
| A stranger's kill; companion code `DropItem`s the gold straight into its pack (the Squire and Mercenary pattern) | in the pack, **no check, no flag** |

Why: looting rights are recorded for the damager's **master** (`BaseCreature.GetDamageMaster`, `:3992`;
`Corpse.cs:295-311`), never the pet, and a companion is in no party, so a monster corpse is innocent to it for two
minutes (`Misc/Notoriety.cs:332-348`, `Corpse.MonsterLootRightSacrifice` `Corpse.cs:92`). The criminal flag reaches
the owner through `BaseCreature.CriminalAction` (`:2897-2905`).

**Seam:** auto-loot asks `corpse.CanLoot(owner, item)` and `corpse.IsCriminalAction(owner)` (`Corpse.cs:860-861`,
`:750-770`), skips anything that would be criminal (design: auto-loot respects notoriety), and moves allowed items
by code. Never the lift path, which judges the companion as itself.

### 9. Mounts: **WORKS WITH OUR CODE**

| Test | Actual |
|---|---|
| `ethy.Rider = companion` when the owner mounts; `Mount.Rider = null` when the owner dismounts (an `OnThink`-style rule) | mounted; on dismount the ethereal is **back in the companion's pack**; the ethereal's slot counts on the **companion's** `Followers` (1), not the owner's |
| `EtherealMount.Validate(companion)` | **true** (no `PlayerMobile` gate, `Mobiles/Animals/Mounts/Ethereals.cs:170-207`) |
| Owner's tamed horse ridden by the companion | horse on **Internal**, master still **the owner**, owner's followers **unchanged** |
| Horse dismounted | back in the world with order **Come**; `IssueOrder(Follow, owner, owner)` sets Follow |
| `BaseMount.CheckMountAllowed(companion)` | **true**: it only checks `PlayerMobile` (`BaseMount.cs:283-309`) |

**Doom and Ter Mur beyond P41's grep:** pinned has **no** region that forbids mounts. `BaseRegion.MountsAllowed` is
`true` (`Regions/BaseRegion.cs:45`) with **0** overrides in UOContent (the only other hit is a test,
`UOContent.Tests/Tests/Mobiles/MountRegionTests.cs:84`), and the 34 files in `Regions\` include no Doom or Ter Mur
region class that touches mounting (`DoomGuardianRegion.cs` is a `DungeonRegion` with no mount member). Ter Mur's
only rule is **race**: a Gargoyle **player** cannot ride (`BaseMount.cs:301-305`). Ours: 1 file mentions mount
blocking, `customizations\Mobiles\Normal\MinionOfScelestus.cs` (a monster ability, not a region). So "dismount where
the owner cannot ride" reduces to "follow the owner's `Mounted` state", and a companion of a Gargoyle owner never
mounts. Whether OSI forbids mounts somewhere pinned does not: **unverified**, and out of scope (fidelity is pinned's).

### 10. Transformation spells: **WORKS**

| Cast by the companion (Necromancy 120) | Actual |
|---|---|
| Wraith Form | body **0x2EC**, hue 16385, context WraithFormSpell |
| Lich Form (switches from Wraith) | body **0x2ED**, context LichFormSpell |
| Lich Form again | toggled **off**, body 0, no context |

`TransformationSpellHelper.OnCast` (`Spells/Base/SpellHelper.cs:1173-1270`) has no player check. Effects that read the
transformation (Wraith mana drain, Lich regen, Vampiric Embrace leech) were **not** probed one by one; a Necromancer
companion keeps them or not per effect.

---

## C. The two rare branches

### 11. Penitent

- **(a) Wrath of the Wounded: WORKS WITH OUR CODE.** `AlterMeleeDamageTo` and `AlterSpellDamageTo` are virtual on the
  attacking creature (`BaseCreature.cs:4428`, `:4438`), called from `BaseWeapon.cs:1870` and `SpellHelper.cs:922`,
  `:989`, `:1074`. Probed: 100 damage stays **100** at full health, becomes **130** at 25%. A Support-based Penitent's
  **heals** have no healer-side hook (`Bandage.cs:418` calls `Patient.Heal` directly); scaling them means a top-up
  heal after the bandage lands. Ours.
- **(b) Shared Burden: companions WORKS WITH OUR CODE; a player NEEDS PINNED PATCH.** Probed with a `Damage` override
  on the companion: a sibling hit for 40 took **34** and the Penitent **6** (15%). The owner hit for 40 took **40**;
  the Penitent took **nothing**. No pinned seam reaches damage aimed at a player: `Mobile.Damage` offers only
  `Region.OnDamage(this, ref amount)` (`Server/Mobiles/Mobile.cs:5968`, a region hook) and `Mount.OnRiderDamaged`
  (`:6013`, only if riding our mount); `AOS.Damage`'s only per-target absorb is the swamp dragon's barding
  (`Misc/AOS.cs:175-188`). **Patch:** one call at the same place as ours `patches\AOS-damage-eater-hook.patch`
  (after the reflect block, before `m.Damage`), letting our code lower `totalDamage` and apply the share to the
  Penitent; 1 to 3 lines. It covers weapons and spells (both end in `AOS.Damage`); direct `Mobile.Damage` callers
  (e.g. some poison and ability damage) would not see it. **Patch-free fallback:** after-the-fact, heal back a share of
  each party member's hit loss and damage the Penitent by it from `OnThink`; it cannot prevent a killing blow.
- **(c) Last Rites: WORKS WITH OUR CODE.** `OnBeforeDeath` (`BaseCreature.cs:3220`), called by `Mobile.Kill` before
  anything else (`Mobile.cs:4737-4740`). Probed: a killing blow left the Penitent **alive at 1 hit**, not a dead pet,
  and healed the owner and a sibling **to full**.

### 12. Otherworlder

- **(a) Plot Armor: WORKS WITH OUR CODE.** Same hook; probed: survived at **1 hit**, **Blessed** for the window, and
  after 3 s Blessed was cleared. `Mobile.Damage` returns early while blessed (`CanBeDamaged`, `Mobile.cs:5963`).
- **(b) Power of Friendship: WORKS WITH OUR CODE.** `AddStatMod` and `AddResistanceMod` work on players and creatures
  alike. Probed with 2 companions: owner Str **100 -> 104**, physical **0 -> 2**; companion Str **100 -> 104**.
- **(c) Cheat skills** (not probed by test; seams read):

| Cheat | Hook | Patch? | Scoped to the owner's party? |
|---|---|---|---|
| Appraisal | Our speech or gump on loot the companion sees (AOS items already show properties) | No | Owner only, by design |
| Item Box | A companion backpack subclass with higher `MaxWeight`/`MaxItems`; ours `PackMule.cs` already replaces a creature's pack with `PackMuleBackpack` | No | n/a |
| Fortune | Loot luck is the **top damager's** luck (`Misc/LootPack.cs:92-112`), and a companion's damage is credited to its owner (`GetDamageMaster`), so Fortune raises the **owner's** `Luck`. Ours `patches\PlayerMobile-fountain-luck-bonus.patch` already makes `PlayerMobile.Luck` call into customizations (`FountainOfFortune.GetLuckBonus`) | **No new patch** if that call grows a companion term; renaming it to a general shard luck hook would be a 1-line edit of an existing patch | Yes: the term can include `Party.Get(owner)` members |
| Quick Study | Ours `ClusterFSkillGain.cs` replaces the skill-check handlers (`:35-46`) and decides boosts in `ShouldBoost` | No | Yes: check whether `from` is the owner, a party member, or a companion of either |

### 13. Shared cheat-death cooldown: **WORKS WITH OUR CODE**

Probed with one `DateTime` per owner: the Penitent's Last Rites fired, then the Otherworlder's Plot Armor **did not**
inside the same cooldown (it died), and fired again once the cooldown passed. **Where it lives:** in the companion
registry (the `GenericPersistence` from probes 5 and 6), keyed by owner, so it survives restarts and is shared by every
companion of that owner whatever their order of death. Not on the `PlayerMobile` (no field without a patch) and not on
each companion (two copies to keep in step).

---

## 1. Class paths verdict

| Path or branch | Verdict | What carries it |
|---|---|---|
| **Blade** | Ship as designed | `MeleeAI` under our `ForcedAI` (probe 4) |
| Knight | Ship as designed | Chivalry has no player gate (P41 2.4); not probed here |
| Blademaster | Ship as designed **with P41's Bushido patch** | `SamuraiSpell.CheckExpansion` (`SamuraiSpell.cs:28-29`) |
| **Bow** | Ship as designed | `ArcherAI` with P41's bolt fix |
| Ranger | Ship as designed | Not probed (tracking and wilds behaviour is ours) |
| Sharpshooter | Ship as designed | Not probed; Bushido patch if it uses Bushido |
| **Arcane** | Ship as designed | `MageAI`; free casting (decided); never heals master (P41), ours |
| Spellsword | Ship as designed | Not probed |
| Necromancer | Ship as designed | Probe 10 |
| **Support** | **Ship as designed** | Probe 1 |
| Cleric | Ship as designed | Probe 1 plus Chivalry |
| Troubadour | **Ship as designed** | Probe 2, with our area-peace routine |
| **Rogue** | **Ship as designed** | Probe 3, with our `OnMove` and monster-detection roll |
| Assassin | Ship as designed | Probe 3 (poison, burst from stealth) |
| Trickster | Ship as designed | Probe 3 (locks, traps); "distraction" is undefined in the design, so unprobed |
| Penitent | Ship as designed **if** the optional 11b patch lands; otherwise **ship reduced**: Shared Burden covers sibling companions only, never the owner | Probe 11 |
| Otherworlder | Ship as designed | Probes 12 and 13 |

**Nothing needs declining.** P41's plan to decline bard or rogue in B7 is withdrawn.

---

## 2. Corrected build order (P41 section 10, revised)

Folds in P45's results and every correction in `docs\companions\p41-companions-review.md`. Each batch builds through
`build.sh`, ships a test where it adds a gate (proved red first), and leaves the shard working. Sizes in brackets.

1. **B1 Companion base and record [M].** `BaseCompanion : BaseCreature`, generated serialization. Record: levels,
   loop, per-skill peaks, personality, path, branch, `Female` for sex, a **never-reused `LineageId`**, parents and
   generation (lineage ids). Player hits, stamina and mana; never `SetDamage`; weapon damage-type split on equip;
   `CanAutoStable => false`; `StandsDownOnCommand => false`; slot changes re-count followers (P41 11.3);
   `ClusterFSkillCaps.Apply` overload and `ShouldBoost` including companions. Tests: caps, weapon dice, gain boost.
2. **B2 Data tables [M].** Loader, validator, reload command, shard test over every shipped row. Tables, per the
   design: **`personality.json`** with the 9 personalities (7 common, Gloomy 5%, Isekai'd 1%) and the
   **personality-to-path map** (rolls happen within the bought path); **`classes.json`** with 5 paths x 2 branches
   plus Penitent and Otherworlder, gendered titles; **`speech.json`** with a **personality x moment x gender x
   path/branch** key (the class dimension carries the 50 combo epithets and lines from `companions-combo-lines.md`);
   **`party.json`** with party of 6 including the player, slot cost **1/1/2/2/3/3 by loop**, companions and pets
   sharing `FollowersMax`, and the floor reconciled against stock 5 (P47 owns the curve).
3. **B3 Parity patches [S each, argued first].** P41's four: pet gain x2 (`SkillCheck.cs:140-143`), pet stat delay,
   Bushido, resurrection loss with the Healing rule. Reagents and disturb stay unpatched (free casting, decided).
   Optional fifth, only if Chase wants Shared Burden on players: the `AOS.Damage` call from 11b.
4. **B4 Hiring and gumps [M].** **Two sources:** a **League vendor** selling **path contracts** (buyer picks the
   path only) and a **board of candidates** (name, gender, path shown; personality hidden; daily rotation). Lore
   gump as a `DynamicGump` with the owner check in `OnResponse`.
5. **B5 Commands [M].** `OnSpeech` parser (all, name, class group), never `e.Handled`; orders through `IssueOrder`.
6. **B6 Companion AI, part 1 [M].** `ForcedAI` with the probe-4 `DoOrderFollow`/`DoOrderGuard` threat scan
   (owner, siblings, self); Melee, Archer, Mage (with owner heals); the **target relay** (probe 7).
7. **B7 Companion AI, part 2 [L]. No probe left to run; nothing to decline.** Support: real bandages and potions
   (probe 1). Troubadour: real handlers plus our area routine, monster targets only, never a pet as the provoke
   target (probe 2). Rogue: our `OnMove`, the monster Detect Hidden roll, locks, traps, poisoning (probe 3).
   Knight and Cleric Chivalry with tithing. Auto-loot judged by the owner, items moved by code (probe 8).
8. **B8 Mounts [S].** Follow the owner's `Mounted` state from `OnThink`; ethereal and real both by code;
   `IssueOrder(Follow)` after a real mount dismounts (probe 9). ShrunkPet's two defects stay a separate task.
9. **B9 Rooms, logout and courier pigeon [M].** One `GenericPersistence` registry for rooms, logged-out companions
   (the `IsStabled` marker for ghosts) and the party cheat-death cooldown, restoring `IsStabled` at load (probes 5, 6,
   13). Logout and login through `EventSink.Logout` and `PlayerLoginEvent`. `RoomAttendant : PlayerBarkeeper`. The
   **courier pigeon** sends a letter to a roomed companion, which arrives after a travel delay and can be sent back;
   owner, travel, combat and cooldown checks (P41 6); deleting a pigeon never deletes a companion.
10. **B10 Drill Orders and League class trainers [S].** **Drill Orders** replace the 26 training contracts: a
    League consumable giving one class skill a period of faster gain, never past the previous peak or the current cap
    (through `ShouldBoost`). **5 League class trainers**, one per path, where branches are chosen and Drill Orders sold.
11. **B11 Rare branches [M].** Penitent (11a, 11c; 11b per Chase's patch decision) and Otherworlder (12a, 12b, the
    four cheat skills), sharing the B9 cooldown.
12. **Later, own chat:** breeding (record fields from B1).

---

## 3. Test-host artifacts found (for the overseer; not engine behaviour)

Three systems the live server configures were missing in the test host, each of which first looked like a finding:

1. **No poisons.** `PoisonKinds.Configure` (`Misc/PoisonKinds.cs:75-84`) never runs, so `Poison.Lesser` and the rest
   are null: `ApplyPoison(null-poison)` cures, and the Poisoning timer throws at `Poisoning.cs:133`. The probes call
   it once (`P45Helpers.EnsurePoisons`).
2. **No default weapon.** `Fists.Initialize` (`Items/Weapons/Fists.cs:40-43`) never runs, so `Mobile.Weapon` is null
   for an unarmed creature and `CheckCombatTime` never swings (`Mobile.cs:794-797`).
3. **No skill handlers.** `Peacemaking`, `Provocation`, `Discordance`, `Hiding`, `Stealth`, `DetectHidden`,
   `RemoveTrap` and `Poisoning` `Initialize` are not called, so `UseSkill` finds no callback.

Same class as Q-026. Candidates for `UOContentFixture-npc-speeds.patch`'s list; the overseer's call.

## 4. P66 in flight (read only, nothing touched)

At the end of this task the main tree had uncommitted P66 changes: `ClusterFSkillGain.cs` (+327 lines), a new
`ClusterFSkillClamps.cs`, and new patches `Bard-musicianship-reduction-osi.patch`,
`DetectHidden-osi-radius-found-gain.patch`, `Hiding-combat-range-osi.patch`, `BaseWeapon-block-chance-osi.patch`,
`NetherCyclone-resist-osi.patch`. The first three change lines my bard and rogue probes ran through (the Musicianship
term, the Detect Hidden radius, the Hiding combat range), clamping a **player's** skill to OSI's top; the Hiding patch
says "Creatures as pinned". **P45 results are as of `29db3d5` plus pinned and do not include P66.** When companions are
built, their skills above 100 or 120 should go through the same clamps, or a companion will out-hide and out-play a
player of equal skill. Unverified how the clamp helpers treat a creature.

## 5. Possible conflicts with decided design

None of the probes contradicts a decision. Three things need an explicit rule:

1. **Shared Burden on the owner** (11b) needs the optional pinned patch, or the Penitent is reduced to siblings.
2. **Hidden companions and monsters' Detect Hidden** (A3): pinned makes a hidden companion undetectable by monsters;
   "same math as a player" needs our roll.
3. **Owners and the abandoned-pet clock** (probe 5): a companion that is never added to `Owners` is exempt from the
   3-day delete and from `LastOwner`-based logic. Hiring should decide whether to add the buyer to `Owners`
   (taming does, `SetControlMaster` does not).

## 6. Unverified

1. A real world save and restart: probes 5 and 6 serialize and deserialize single objects; the load order is argued
   from `Persistence.Load` and the priorities, not observed in a running shard.
2. LOS in the relay (no map files in the test host; every LOS check passes there).
3. Per-effect behaviour of Wraith, Lich and Vampiric Embrace on a creature (only the forms were probed).
4. Guards revealing a hidden companion (read, not probed); passive Felucca detection (read, not probed).
5. The Otherworlder cheat skills (seams read, not probed); Ranger, Sharpshooter, Spellsword, Knight (not probed).
6. Whether OSI forbids mounts anywhere pinned does not.
7. How P66's skill clamps treat creatures.

## 7. Cleanup

- Worktree removed: `git -C D:\ShatteredLegacy --no-optional-locks worktree remove --force ..\SL-probe-companions`
  (forced because the probe files were untracked by design), then `worktree prune`. `worktree list` shows only
  `D:/ShatteredLegacy 29db3d5 [main]`, and `D:\SL-probe-companions` no longer exists. Main tree HEAD unchanged.
- Nothing committed in either repo. `CHANGELOG.md` and `VERSION` untouched by me.
- Left behind: the builder image `sl-uo-builder:cc-p45-probe` (no `sl-modernuo:cc-p45-probe` runtime image was made).
  Safe to delete: `docker image rm sl-uo-builder:cc-p45-probe`.

P45 DONE
