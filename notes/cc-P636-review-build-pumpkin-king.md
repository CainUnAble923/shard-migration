# P636: Review of P624, Pumpkin King stage 1

Reviewed October 26, 2026. Notes only. No code changed.

## Scope and evidence

Read both work-copy AGENTS.md files, the direction decision and task list, both `cc-P624-*.md` notes, the P564 design and its review, and the P408 and P461 reviews. Checked Chase's October 25 instruction in the completed `cc-P624-build-pumpkin-king.md` prompt. It asks for the first stage of the ordered design, with the remaining stages supplied as drafts. P624 implements PK1 and supplies those drafts. Leaving PK2 purchases and ring confirmation, PK3 equipment selection, and PK4 client acceptance for subsequent tasks follows that ordering.

Source snapshots:

- Code work copy: `a3f017e279e29eed0ac12c506ef51e6310291583`.
- Notes work copy before this note: `782363353dc7c3e394b61925f34878f7c672f6f5`.
- P624 implementation: `feadac2d361bd31d3bb6c1cbb16a2b96fcea30fd`, merged by `d49fbec`.
- Read-only ModernUO: `d4531cd94b739613155225c234900de9f47d2c88`, clean when checked.
- Read-only ServUO pub57: `d76bf4443cf76d081ddaf8f57c87ff33749256af`.

The event code and verification file have no subsequent changes between P624 and this code snapshot. Below, `event/` means `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/` in the code work copy. `pinned/` means `D:/UO/ModernUO-pinned/Projects/`.

## New finding

### Medium [P2]: Include the bosses' summoned Revenants in shutdown ownership

**Location:** `event/Spawner.cs:181`, with ownership entry points at `Spawner.cs:357`, `Spawner.cs:384`, and `Spawner.cs:261`.

**What happens:** Ownership covers creatures placed by `DoSpawn` and creatures hatched from tracked pumpkins. It misses creatures summoned by the bosses' normal spellcasting. An event Jack can cast Vengeful Spirit, creating a Revenant with Jack as its summoner. `off`, `remove`, or seasonal shutdown deletes Jack but leaves that Revenant alive. The Revenant can continue pursuing its target, including across facets, until the target dies or its spell duration expires. This is a temporary combat leftover, not a permanent saved creature leak. It contradicts the design's shutdown promise that event combat ends when normal dungeon spawners resume.

**Source evidence:**

- `event/Creatures/JackThePumpkinKing.cs:39` selects MageAI, and lines 68-71 give Jack 120 Magery, Necromancy, and Spirit Speak. `event/Creatures/JackInTheBox.cs:24` and `:53` establish the same spellcasting route for the second boss.
- `pinned/UOContent/Mobiles/AI/MageAI.cs:70`, `:252`, and `:262` enable necromancy casting and include `VengefulSpiritSpell` in the damage-spell selection. The shard's `server/patches/MageAI-pet-magery-mastery.patch` changes SmartAI selection, not this necromancy branch.
- `pinned/UOContent/Spells/Necromancy/VengefulSpirit.cs:49` creates the Revenant and calls `BaseCreature.Summon`. At Jack's Spirit Speak, the calculated duration is 90 seconds, with a separate unsummon timer two seconds longer. `pinned/UOContent/Mobiles/BaseCreature.cs:3841` assigns the summon flag and master, then starts that timer and places the creature at lines 3859-3862. None of these paths registers event ownership.
- `pinned/UOContent/Mobiles/Monsters/AOS/Revenant.cs:83` checks the target and expiry, not whether the caster survives. Lines 91-122 let it follow the target across facets. `BaseCreature.OnDelete` at `BaseCreature.cs:3672` and `OnAfterDelete` at `:2708` do not delete creatures summoned by the deleted caster. Stopping an unsummon timer there concerns the deleted creature itself.
- `event/Spawner.cs:181` builds the shutdown list from `Owned`, `Spawn`, and `Boss` only. The Revenant belongs to none of them. `pinned/UOContent/Mobiles/Monsters/AOS/Revenant.cs:60` excludes Revenants from serialization, which limits this finding to the running encounter.

**Fix:** Extend encounter ownership to exact summons of event-owned casters. Retain those associations when a boss dies or a room rotates, so later shutdown still removes its surviving summons. Keep them out of room kill progression. Preserve unrelated player summons and hand-added bosses. Use the caster relationship or explicit registration, not a region-wide deletion by creature type. This is our event cleanup repair, not a reason to change global spell duration or summon behavior.

**Missing regression:** `server/tests/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonVerification.cs:1183` exercises Jack's pumpkins through `SchedulePumpkins`, but never creates his spell summons. Add a deterministic real Vengeful Spirit summon from an event boss, then shut down immediately and assert that it is deleted before its natural expiry. Cover both a living boss and a boss killed before shutdown, preserve an unrelated player's Revenant, and verify no room kill is credited for a summon. Watch that regression fail before repairing cleanup. Runtime reproduction was not run in this review; the finding is based on the complete creation and deletion paths above.

## Other review results and limits

The changed code separates cleanup ownership from room progression, invalidates controller callbacks before deleting owned entities, preserves the version-0 field order, and seeds version-0 ownership from the saved current spawn and boss. The keyed deletion snapshot captures control state before ModernUO clears it. The original random tally assertion now uses a scoped forced roll. No additional save-format defect was identified by source inspection.

Excluded findings already recorded by P408 and P461 and carried into P564. P624's remaining-stage drafts remain the handoff for the deferred work. Its disclosed inability to recover already-untracked version-0 entities is not a new finding.

The new save test at `SorcerersDungeonVerification.cs:1527` reloads controller references twice into the same test world and checks cleanup afterward. It does not restart a server or reconstruct every entity and timer. Full world reload and restored-pumpkin timing therefore remain unverified here, consistent with the outstanding acceptance and timer work. This is a limit on the evidence, not an additional copy of P461's existing timer-test finding.

No lane tests or build were requested or run, and no tests were added. P624's recorded red/green and gated-build results are prior evidence, not independently reproduced results. Live deployment, current-world ownership, client rendering, and exploit behavior in a running shard remain unverified. No connection to Haven, deployment, shared-world action, or Git mutation was made.

Ran the required progress calculation against these work copies with `--dry-run` and generated writes suppressed in memory. The tool still attempts to write `tools/progress.json`; that write was discarded. No README or progress artifact changed.

## Files inspected for this review

P624 implementation and tests:

```text
server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/Spawner.cs
server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/Generate.cs
server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonData.cs
server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/Creatures/JackThePumpkinKing.cs
server/tests/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonVerification.cs
```

Supporting shard sources:

```text
server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/Creatures/JackInTheBox.cs
server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/EnchantedOriginArtifacts.cs
server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonRewards.cs
server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/Items/EscapingAndSterlingRewards.cs
server/customizations/Services/PointsSystems/PointsSystem.cs
server/customizations/ClusterFSeasonalSwitch.cs
server/tests/Route/ShardTestClock.cs
server/patches/MageAI-pet-magery-mastery.patch
server/patches/SpellHelper-pet-ability-hooks.patch
server/patches/BaseCreature-pet-ability-hooks.patch
```

Pinned sources:

```text
Projects/UOContent/Mobiles/BaseCreature.cs
Projects/UOContent/Mobiles/CreatureEvents.cs
Projects/UOContent/Mobiles/AI/MageAI.cs
Projects/UOContent/Mobiles/AI/BaseAI/BaseAI.cs
Projects/UOContent/Mobiles/Monsters/AOS/Revenant.cs
Projects/UOContent/Spells/Necromancy/VengefulSpirit.cs
Projects/UOContent/Spells/UnsummonTimer.cs
Projects/Server/Mobiles/Mobile.cs
Projects/Server/Timer/Timer.cs
Projects/Server/Timer/Timer.TimerWheel.cs
Projects/Server/Serialization/Persistence.cs
```

P636 DONE
