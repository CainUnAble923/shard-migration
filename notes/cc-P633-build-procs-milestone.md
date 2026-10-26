# P633: weapon procs at the levelable gear milestone, stage 1

Written 2026-10-26 by the Iron Golem (Claude Code). Builds the first playable slice of [cc-P569-design-procs-levelable-milestone.md](cc-P569-design-procs-levelable-milestone.md). Chase's decision (10-25 evening, `D:/UO/overseer/decisions-2026-10-23.md` 20:15 entry: "P569 level 100 one PvE proc"): unlock at item level 100 for 100 points, one PvE-only proc, cooldowns shared.

## In plain words

- Players will not notice anything yet. On the test shard only, staff can turn on "weapon milestones" with `[LevelGearProcs on` (it switches off again at restart).
- With it on, a levelable crafted weapon at item level 100 shows a "Weapon milestone" button at the bottom of `[ItemLevel`. For 100 of the weapon's points and one property slot it can bind one permanent effect: Stormstrike (12 energy damage) or Emberstrike (12 fire damage). A confirmation window asks first.
- In a fight with a wild creature, each damaging hit has a 5% chance to set it off. Then it rests for 10 seconds, a rest shared by you and your companions and kept on the weapon if it changes hands. Players, pets and summons are never struck by it.
- Nothing for you to do now. Before it reaches players it still needs the "weapon too high for your level" rule (waiting on the player level work), the imbuing window counting the milestone's slot, and a play test in the client. Those are the drafts at the end.

## Status

Done. The Iron Golem (Opus), branch `golem/Iron/P633` of both repos, not committed (the Golem commits). The gated build is green (section 4). No shard was started, no world command run, no package built or published, nothing deployed, no Haven contact. The `docker-build` lock was held for the gated build only.

## 1. What "stage 1" means here

The design's ordered list starts with prerequisites that add no proc behavior: (1) the F-12 player level service and purchase ledger, (2) the shared gear and imbuing budget, then (3) the saved choice and purchase flow, (4) the combat hook and cooldowns, (5) client acceptance. Step 1 is large and not playable, and none of it has been built (I searched `server/customizations` and `server/tests` for an acting-level service, attunement or `IPlayerLevelSource` replacement: only the provisional `ClusterFCreatureLevels.cs` source exists). The prompt asks for "the smallest playable slice", and the design itself allows "an isolated disabled proc build may still be reviewed" while its release gate waits on step 1.

So stage 1 here is design steps 3 and 4 together, cut to the minimum and kept off: the saved choice, the guarded purchase on a Milestone page, the one weapon hit call, the two effects, and the shared cooldowns with their save file. It runs only behind the test shard's in-memory switch, the pattern P630 used for the League Echo.

Deliberately left for later stages (drafts in section 6), each a recorded deviation from the design's full release rules:

| Left out | Why, and what stage 1 does instead |
|---|---|
| Acting-level dormancy (`min(item level, player level + Arms Lore margin)`) | No real F-12 level service exists, and the design forbids building it on the provisional combat-skill source. The purchase saves `RequiredLevel = 100` so the later stage can enforce it without a save change; until then the proc never goes dormant. This is the main reason the feature stays off for players. |
| Imbuing's view of the milestone slot | `ClusterFLevelGear.SlotsUsed` now counts the milestone as a slot, so `[ItemLevel` spending and the milestone purchase both see it. The imbuing gump does not read `SlotsUsed`, so an imbuer could still fill a fifth property on a weapon with a milestone. The design's shared-budget stage owns that, together with the existing reverse-order hole (P534). Intensity mode's 100-point reservation is also that stage's. |
| `intensityCost` setting | Belongs to the shared budget stage; not added, so no inert setting appears in `modernuo.json`. |
| Client check of the pages and visuals | Stage 5 (needs a scratch shard and the packaged client). |

## 2. What was added (ShatteredLegacy)

| File | What |
|---|---|
| `server/customizations/LevelGear/LevelGearProcs.cs` (new) | `LevelGearProcSettings`: `clusterf.levelGear.procs.enabled` (false), `unlockLevel` 100, `pointCost` 100, `chanceBasisPoints` 500, `cooldownSeconds` 10, `companionOwnerRange` 18, and per choice `stormstrike.enabled`/`emberstrike.enabled` (true) and `.rawDamage` (12). `Problem()` checks the design's ranges; an invalid value turns the feature off and prints one startup line. `EnabledOverride` is the test shard switch, never written to the settings file. `LevelGearProc`: the stable keys `stormstrike` (energy) and `emberstrike` (fire). `LevelGearProcPurchase`: key, required level, purchase level, purchase time, paid cost. `LevelGearProcCooldowns`: a `GenericPersistence` named `LevelGearProcs` (version 0) holding owner and weapon end times as absolute UTC, writing only unexpired entries of still-existing mobiles and items. `ClusterFLevelGearProcs`: `WhyNotBuy`/`Buy` (one synchronous check of every rule, on every call), `OnWeaponHit` (the hook), `OwnerOf`, `IsTarget`, the owner-neutral tooltip line, and `[LevelGearProcs [status\|on\|off]` (GameMaster, `CommandShard.TestOnly`). |
| `server/customizations/LevelGear/LevelGearMilestoneGump.cs` (new) | The Milestone page (price, slot, chance, cooldown, PvE, each choice's damage and the exact refusal reason, or the bound effect and the viewer's cooldown) and the confirmation ("Bind Stormstrike to this weapon for 100 item points? This choice is permanent until a paid respec is available.", with live points and slots). Only the confirmation buys, through `Buy`, which re-reads everything. |
| `server/customizations/LevelGear/LevelGearGump.cs` | One more row on a weapon's `[ItemLevel` page: the Milestone button, shown only while the feature is on or once a milestone is bought. |
| `server/customizations/LevelGear/ClusterFLevelGear.cs` | `LevelGearState.Proc`; store version 1 appends a flag and the purchase to each row (a version 0 row loads with no milestone, never inferred from its level); `SlotsUsed` counts a milestone as one slot; the tooltip adds `Milestone: Stormstrike (PvE)`. |
| `server/patches/BaseWeapon-level-gear-proc-hit.patch` (new) | One call, `ClusterFLevelGearProcs.OnWeaponHit(this, attacker, defender, damageGiven)`, at the end of `OnHit`'s `damageGiven > 0` branch: after the weapon's own hit spells and area effects, before `OnGaveMeleeAttack`, the special move and the custom imbue callback, as the design places it. Made against the assembled tree of `sl-uo-builder:cc-P632` (every patch applied), `--fuzz=0`. |
| `docker/uo/apply-patches.sh` | Registers the patch after `AOS-level-gear-attribute-aggregation.patch`, so after every BaseWeapon patch, with its reason. |
| `CHANGELOG.md`, `VERSION` | 2026.10.26.5, one Staff line (players do not see it). |

How a hit is judged (`OnWeaponHit`, in this order; any failure returns before the roll, so a blocked strike draws no random number):

1. Not already inside a milestone effect; positive `damageGiven`; feature on; the weapon has a known, enabled choice.
2. The weapon is the attacker's current, equipped weapon, a crafted non-artifact `BaseWeapon` that is not `Fists`.
3. The owner: a player striking, or a controlled, non-summoned `BaseCompanion` whose `ControlMaster` is a living, online player on the same map within 18 tiles. Other pets and creatures have none.
4. The target: a living, non-blessed `BaseCreature` with no master, not controlled or summoned, not `NoKillAwards`, the attacker's current combatant, on the same map, in weapon range and line of sight, and `CanBeHarmful`. A Whirlwind or splash victim that is not the combatant is refused.
5. Neither the owner's nor the weapon's cooldown is running (clock seam `Now`).
6. One `Roll(10000)`; below 500 succeeds.
7. Both cooldowns are set to now + 10 s before anything else, then a re-entry guard, `DoHarmful`, the stock visual (`BoltEffect(0)`, or the fireball particles 0x36D4 and sound 0x15E), and one `AOS.Damage` of 12 at 100% energy or fire, from the attacker (so a companion stays the damage source).

## 3. Tests: red first, then green

`server/tests/Misc/LevelGearProcVerification.cs`, 8 facts:

1. `TheMilestoneIsBoughtOnceAtLevel100For100Points`: off by default; level 99 refused, 100 bought; 99 points refused and nothing changed; armour refused; a weapon not carried refused; exact 100 points leaves 0, saves the key, required level 100 and cost 100, and takes one more slot; a replayed purchase is refused with nothing paid; bought at level 150, still required level 100 (purchase level 150); five properties already, refused.
2. `ARealWeaponHitRollsTheMilestone`: a real `Katana.OnHit` against an Ettin being fought: a roll of 500 does nothing; 499 sets both cooldowns to T0 + 10 s; the next hit draws no roll.
3. `StormstrikeIsTwelveEnergyAndEmberstrikeTwelveFire`: 12 damage at 0 resist, 6 at 50 energy resist; Emberstrike 12 through 100 energy resist (it is fire).
4. `TheCooldownIsSharedByTheOwnerAndKeptOnTheWeapon`: a second milestone weapon of the same player is held at 9.999 s and strikes at exactly 10 s; that weapon handed to another player during its cooldown does not roll.
5. `OnlyAWildCreatureBeingFoughtCanBeStruck`: a player, another player's pet, a creature not being fought, a zero-damage strike and a weapon in the backpack: no roll.
6. `ACompanionUsesItsOnlineOwnersCooldown`: offline owner, no roll; online (a test NetState), it strikes for 12 and the owner, not the companion, gets the cooldown.
7. `PurchasesAndCooldownsSaveAndLoad`: a hand-written version 0 store with a level 150 row loads with no milestone; a purchase round-trips every field; an unexpired owner cooldown round-trips as its absolute time and an expired weapon cooldown is dropped.
8. `AnInvalidChanceTurnsTheMilestoneOff`: `chanceBasisPoints` 20000 turns it off and a hit does nothing; back to 500, it strikes.

Run on the builder image `sl-uo-builder:cc-P632` (this branch's base, merge `313d94d`), with the four LevelGear sources and the fact file copied in, the new patch applied with `patch -p1 --fuzz=0`, and `dotnet test` filtered with the gate's flags (`--network=none --security-opt seccomp=unconfined`). Script and logs are in the session scratchpad.

- **Red, behaviour**: an inert stub with the same names (`WhyNotBuy` always "Weapon milestones are not built.", `OnWeaponHit` returns 0, the cooldown store writes nothing, and the gear store and `SlotsUsed` as on `HEAD`). All 8 failed. Fact 1 failed on its first purchase assertion (`Assert.Contains() Failure: Sub-string not found`); facts 2 to 8 failed at their first `Buy` ("Expected: null, Actual: Weapon milestones are not built.").
- **Red, the hook**: the real code with the patch left out. Fact 2 alone failed ("Expected: int[] [10000], Actual: List<int> []": the hit never reached the service); the other 7 passed, which shows they test the service and fact 2 tests the hook.
- **Green**: all 8 passed, and the 7 existing `LevelGearVerification` facts still passed (15 of 15).

One test-host finding, fixed in the test: the host has no tiledata, and a weapon's layer comes from tiledata, so a test katana had layer 0 and `Mobile.Weapon` never found it (my probe printed `weapon=False parent=True ...`). The test sets `Layer.OneHanded` explicitly; in game the layer comes from the client data as usual.

## 4. The gated build

`docker/uo/build.sh -t sl-modernuo:cc-P633` under the `docker-build` lock: `[patches] All 168 patches applied successfully.` (the new one included), then the shard tests: total 2573, passed 2569, skipped 4, failed 0 (the 8 new facts among them), then the image. Last lines: `Built sl-modernuo:cc-P633 with patches applied and 2569 shard test(s) passing.` and `EXIT=0`. Lock released.

A process slip, recorded honestly: while the build was still running I saved this notes file with its final DONE line already in it, and removed that line within a minute, before the build finished. `git status` and `git log` afterwards showed no commit had been made from it.

## 5. What I could not verify

- The Milestone page and confirmation, and both visuals, in the client: no shard was started (stage 5).
- Ranged and thrown weapons at runtime: `BaseRanged.OnHit` and `BaseThrown` call `base.OnHit`, per the design's reading of pinned source, but my facts drive only a katana. The draft for stage 3 adds them.
- Double Strike, Whirlwind and native hit-spell coexistence at runtime: the hook's position follows the design (before the special move, after the hit spells) and step 4 of the judge refuses a non-combatant, but no fact drives a special move yet (stage 3 draft).
- A full world save and restart: the store and cooldown buffers round-trip, but the save file's lifecycle registration was not exercised on a running shard (stage 5).
- Combat balance: none measured.

## 6. Remaining stages as prompt drafts

For the overseer to number. Each is `Touches: server`, must not run at the same time as another of these (they share the LevelGear files and the BaseWeapon patch), and keeps `clusterf.levelGear.procs.enabled` false.

### Draft A: weapon milestone dormancy by acting level (needs the F-12 level service)

**Model:** Opus

**Touches:** server

**Summary:** P633 built weapon milestones (Stormstrike, Emberstrike) behind the test shard switch with no dormancy. Add the design's attunement rule: the proc acts only while `min(item level, wearer level + Arms Lore margin)` reaches the purchase's saved `RequiredLevel`.

1. Read `notes/cc-P569-design-procs-levelable-milestone.md` (Attunement section), `notes/cc-P633-build-procs-milestone.md` and P568's attunement design. If the real F-12 player level service (not the provisional `ClusterFCreatureLevels` source) and P568's acting-level API do not exist yet, stop and say so: do not build a proc-only level reader.
2. Use that API in `ClusterFLevelGearProcs.OnWeaponHit` (after the owner is resolved, before the roll; a companion uses its owner's level) and in `WhyNotBuy` (purchase stays allowed on an earned level-100 weapon whose proc would be dormant for the buyer; the page says so). Missing provider: dormant, and purchases refused.
3. The Milestone page shows `Dormant: acting level N of 100 required` for the viewer only; the tooltip stays owner-neutral.
4. Red-then-green facts: acting 99 dormant, 100 active; wearer 95 with +5 active, 94 dormant; bought at 150 still needs 100; a loop reset keeps the choice and points and makes it dormant, and it returns at the threshold; a companion follows its new owner's level; no provider refuses use and purchase. Gated build with a prompt tag. Notes; CHANGELOG Staff line.

### Draft B: shared gear and imbuing budget, with the milestone slot

**Model:** Opus

**Touches:** server

**Summary:** Make imbuing and `[ItemLevel` count property slots the same way, including the weapon milestone P633 added, as the P569 design's step 2 and P534's reverse-order finding require.

1. Read the P569 design (State, settings, and property accounting), P534's levelable gear design-versus-build note and P633's notes.
2. Add `LevelGearPropertyBudget` (shared reader: stored plus purchased properties, a stored property and its level increase in one slot, the milestone one extra slot even beside Hit Lightning, dormant or disabled purchases still counted). Use it in `ClusterFLevelGear.WhyNotBuy`, `ClusterFLevelGearProcs.WhyNotBuy` and `ArtificersImbueGump`'s display and server-side mutation. Keep `ClusterFImbueKnowledge.MaxSlots` (Master Formulary) for imbuing and `BaseSlots` for gear. In intensity mode, add `clusterf.levelGear.procs.intensityCost` (100, valid 1-1000) and reserve it.
3. Do not change other `CountActiveProperties` callers, loot valuation or extraction.
4. Red-then-green facts: level-first and imbue-first give the same count; four slots allow a milestone, five refuse; Hit Lightning plus a milestone is two; a Master Formulary sixth imbue slot still works; intensity at the limit and one above. Gated build. Notes.

### Draft C: weapon milestone combat coverage (ranged, thrown, special moves)

**Model:** Opus

**Touches:** server

**Summary:** P633's facts drive only a katana's `OnHit`. Prove the milestone through the other weapon paths and the special moves, fixing anything they show.

1. Read the P569 design (Combat dispatch, Tests and acceptance) and P633's notes.
2. Facts through real `OnHit`: a crafted bow and crossbow (`BaseRanged`) and a crafted `BaseThrown` weapon; a native Hit Lightning on the same weapon still fires and does not add to the milestone's chance; Double Strike's second swing may roll after a failed first and is blocked after a successful one; a Whirlwind secondary target never rolls; a lethal primary strike or native proc leaves no milestone on the corpse; a milestone kill keeps the normal death credit and the later creature and special-move callbacks run safely; AOS leech and the damage-eater hook behave as for any AOS damage; no recursive milestone.
3. Each fact red against a deliberately broken variant first (or, for coverage that already passes, the hook removed), then green. Gated build. Notes.

### Draft D: weapon milestone scratch-world acceptance and release proposal

**Model:** Opus

**Touches:** server

**Summary:** Requires drafts A to C done. On a disposable loopback-only scratch shard, check the weapon milestone end to end in the packaged client and write a release proposal. Never live.

1. Take the `test-shard` lock. Scratch saves only; no Haven.
2. `[LevelGearProcs on`; make a crafted weapon levelable, `[LevelGearSet 100 100`, buy each effect through the pages; check the refusal texts, the confirmation, the tooltip, the visuals, a companion's strikes, a save and restart during a cooldown (the remainder survives), and a loop reset with dormancy.
3. Record timing samples for a slow and a fast weapon and a companion party; change no default unless Chase approves.
4. Notes: client version, screenshots, a release configuration proposal, and wiki-ready text (prerequisites, level 100, price, one slot, permanent choice, PvE only, native hit-spell coexistence, shared companion cooldown, dormancy) plus the custom-system and fidelity register entries for the overseer to promote. Live enablement is a separate, authorized release.

P633 DONE
