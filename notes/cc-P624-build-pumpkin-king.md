# P624: Pumpkin King event, stage 1 (encounter ownership, shutdown, kill credit)

Written 2026-10-25 by the Iron Golem (Claude Code). Builds stage 1 of [cc-P564-design-pumpkin-king.md](cc-P564-design-pumpkin-king.md): its first ordered draft, **PK1: Finish encounter ownership, shutdown, and kill credit**. The later stages are drafted as prompts at the end of this note.

## In plain words

- When Treasures of Sorcerer's Dungeon ends (by date, or with `[SorcerersDungeon off` or `remove`), it now takes away every undead it raised. That includes those left standing in earlier rooms and the ones that hatch from Jack the Pumpkin King's pumpkins. Before, those stayed behind in the dungeon for good. Nothing else in the dungeon is touched.
- Jack's unholy pumpkins now land only inside Sorcerer's Dungeon, only while he is the event's boss and the event is on. Before, a player who ran out of the dungeon (or a throw that landed after the event ended) could drop pumpkins and their undead anywhere.
- Killing someone else's tamed pet in the dungeon no longer counts toward an artifact of Enchanted Origin. Before, it counted as a wild kill.
- For Chase: the image `sl-modernuo:cc-P624` is built and all 2,482 shard tests pass. It is ready to go out with the next Haven update while Halloween is on (the event ends 11-02); whether and when to deploy is yours. The event's `status` now also lists what the event owns ("Owned by the event (what off deletes)"). Nothing else needs a decision. The next stages (reward purchases, the missing equipment pool, the client check) are drafted below for the overseer to number.

## Scope: what stage 1 is

The P624 summary reads "encounter ownership and reward safeguards first, then the missing equipment pool and client checks". The design's ordered list makes PK1 the first and smallest slice. PK1 covers encounter ownership plus the kill-credit and drop-roll safeguards. The purchase safeguards (PK2) are a separate draft in the design, so I built PK1 only and drafted PK2 as the next prompt below. If the overseer meant stage 1 to include PK2, PK2's draft below is ready to go as written.

## What changed (ShatteredLegacy, branch golem/Iron/P624)

All in `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/` (called `event/` below), plus the event test file, CHANGELOG.md and VERSION. No upstream patch, no `server/uo/`, no new saved type, no global loot or death change.

| File | Change |
|---|---|
| `event/Spawner.cs` | Ownership kept apart from progression. `Spawn` is still the current room's undead and only a death out of it counts toward the boss. New `Owned` (every creature the event put in the world: each room's undead, each boss, every pumpkin hatchling) and `Pumpkins` (every unholy pumpkin an event Jack threw). A room's `Reset` forgets survivors for progression but keeps them in `Owned`. `Deactivate` now marks itself inactive and stops being the instance first, so no delayed spawn, throw or hatch of it can act. It then stops its timer, deletes its pumpkins and owned creatures, and only then restarts the stock spawners it paused (previously restart came first). The delayed callbacks check `IsLive` (active and still the instance). The save is now version 1: version 0's fields in their original order, then the two lists. A version 0 save seeds `Owned` from its `Spawn` and `Boss`. New helpers: `CountOwned`, `Owns`, `Own`, `AddPumpkin`, `OnPumpkinHatched`, `MayThrowPumpkins`, `MayPlacePumpkin`, `InDungeon`. |
| `event/Creatures/JackThePumpkinKing.cs` | The 5% branch is now `SchedulePumpkins(from)`. It captures the owning spawner when it schedules, and only when that spawner owns this Jack. For an event Jack, the throw a second later happens only while that spawner is live, the event is enabled, Jack is alive and still its boss, and the attacker is alive, on Ilshenar and inside Sorcerer's Dungeon. Each spot must also be inside the dungeon (on top of the existing fit check). Its pumpkins are registered with the spawner, and a hatching pumpkin hands its undead to the spawner. A Jack staff add by hand belongs to no spawner and throws exactly as in ServUO. The 5%, 1 second, 1-3 pumpkins, 5-10 second hatch, the twelve undead and 30% carving are unchanged. |
| `event/SorcerersDungeonData.cs` | The deletion snapshot now keeps the facet, the death spot and the controlled and summoned flags (`DeathContext`). Pinned's `BaseCreature.OnDelete` clears the control master right after raising the deleted event (`pinned/UOContent/Mobiles/BaseCreature.cs:3674` and `:3688`), so a tamed pet read as wild by the death event. Snapshots are keyed by creature and taken only for a creature at 0 hits. `Mobile.Kill` sets `Hits = 0` before `OnDeath` (`pinned/Server/Mobiles/Mobile.cs:4715` onward), so a staff `[delete` of a living creature takes none. Each is removed when its death is read, so a death inside another's deletion keeps both. A creature deleted at 0 hits with no death after it (one built without hit points) leaves an entry behind, so the table holds at most 64 and drops the oldest first. The deaths in progress are always the newest entries. The drop roll now goes through `DropRoll`, which `ForceDropRoll(roll)` pins for one `using` scope in tests; the server still uses `Utility.RandomDouble`. |
| `event/Generate.cs` | `off`/`remove` set `Enabled = false` before deleting anything, and report what was deleted from the ownership lists ("N creature(s) and P pumpkin(s) of the event's removed"). `status` adds a line "Owned by the event (what off deletes): N creature(s) in all rooms, P unholy pumpkin(s)". It is separate from the current room's spawned and killed counts, and from the existing world census. |
| `server/tests/.../SorcerersDungeonVerification.cs` | Five new facts (below). The flaky tally assertion in `AKillInTheDungeonTalliesAndRollsAnArtifactOfEnchantedOrigin` now pins a failed roll, rather than hoping the 0.09% live roll missed. |
| `CHANGELOG.md`, `VERSION` | 2026.10.25.8, three Fixed lines. |

### Kill-event ordering, checked before choosing keyed storage

The design asked me to verify the ordering. In pinned, `BaseCreature.OnDeath` calls `base.OnDeath` (which deletes a non-player: `Mobile.cs:4890`, `Delete()`), and then raises `CreatureDeathEvent` at its end (`BaseCreature.cs:3669`). `CreatureDeletedEvent` is raised inside that `Delete`, from `OnDelete`, before the control master is cleared. Anything that kills a second creature between those two points (an `OnDelete` effect, or another system's death handler, of which the shard has many: `ClusterFAchievements`, `ClusterFLeagueBestiary`, `ExodusEncounter` and others) used to overwrite P408's single slot. The outer creature then lost its credit. The new fact shows this with a creature whose deletion kills another: the old code credited 2000 where 4000 was due. So I used keyed storage.

## Tests: red first, then green

How I ran them: the probe ran on builder image `sl-uo-builder:cc-P613` (same event sources as this branch's base), with the four event files and the test file bind-mounted, and `dotnet test` filtered to `SorcerersDungeonVerification`. The scripts and logs are in the session scratchpad.

| New fact | What it pins |
|---|---|
| `OffDeletesEverythingTheEventOwnsAndNothingElse` | A room completed with three survivors, then a second room. An old-room survivor's death does not count for the new room. `Owned` is exactly the survivors plus the current room. `off` with a spawn pending deletes them all, keeps an unrelated Zombie and a same-art (0xC6A) "unholy pumpkin" item, and after five minutes of clock nothing has come back. |
| `JacksPumpkinsLandOnlyInTheLiveEncounterAndGoWithIt` | Room 9's Jack throws: pumpkins land around a player inside the dungeon and are all the event's. They hatch after 5-10 s into undead the event owns, which are not room progress (a hatchling's death leaves the kill count alone). With the player outside the dungeon on Ilshenar, none land. `off` deletes the landed pumpkins, the hatchlings and Jack, and five throws pending at `off` place nothing. A hand-added Jack still throws as in ServUO. |
| `KillCreditIsJudgedAsTheCreatureWasWhenItDied` | Through the real death hook, with the roll pinned to fail so tallies show the credit: a wild Lich is credited 2000 (fame 8000 / 4); a tamed, non-bonded pet gives nothing; a summoned creature, a bonded pet, a kill outside the region and a dead player give nothing. Two players with looting rights are each credited while the room counts the death once. A death inside another's deletion credits both. No snapshot is left pending afterwards. |
| `TheDropRollIsPinnedThroughTheRealDeathHook` | A failed roll keeps the exact tally and gives nothing. A good roll puts an artifact in the pack and empties the tally. With no pack it goes to the bank, and with the bank full it goes to the player's feet. Disposing the scope restores `Utility.RandomDouble`. |
| `TheSpawnersSaveKeepsWhatTheEventOwnsAndReadsVersionZero` | A hand-written version 0 blob loads: kills, boss and spawn are kept, and `Owned` is seeded with the spawn and the boss, which `Deactivate` then deletes. A version 1 save through `PointsSystemPersistence`, loaded twice, gives each time: room 2, 5 kills, the boss, the current spawn, the earlier room's two survivors in `Owned`, the outstanding pumpkin, the paused stock spawner, no timer, tally 999 and 3 points. `remove` after the load deletes every owned creature and the pumpkin, restarts the stock spawner and removes the researcher. |

**Red on the old code.** P408's code plus only the test seams: empty `Owned`/`Pumpkins` lists, `ForceDropRoll`/`DropRoll`, a `PendingDeaths` returning 0, and `SchedulePumpkins` extracted unchanged. The 4 facts that describe defects failed; the other 12 passed.
- At the first check: the off, save and Jack facts failed on their ownership-list assertions ("Expected: [4 serials] Actual: []"). The kill-credit fact failed with "Expected: 0, Actual: 2000": the tamed pet paid.
- With the list assertions taken out of a copy of the tests (so the behaviour shows):
  - off: "an earlier room's Zombie outlived off" (2 of 2).
  - save: "an earlier room's survivor outlived remove after a load".
  - Jack: pumpkins landed beside a player outside the dungeon. With that case skipped too, "an event pumpkin outlived off".
  - kill credit: the tamed pet's tally logged as 2000, and the nested death gave "Expected: 4000, Actual: 2000".
- `TheDropRollIsPinnedThroughTheRealDeathHook` covers behaviour that already worked, so it passed on the old code. It went red under mutation m1 below.

**Mutations of the fixed code**, for the guard parts that pass on the old code. Each was run alone, and each failed where it should:

| Mutant | Result |
|---|---|
| m1: the drop roll ignores the pinned value (`Utility.RandomDouble()`) | the drop fact red: "Assert.Single() Failure: The collection was empty" |
| m2: any owned creature's death advances the room | off fact and Jack fact red: "Expected: 0" on the kill count |
| m3: a pending regular spawn ignores that the event went down | off fact red: a creature came back after off ("Expected: 1, Actual: 2") |
| m4: a dead player is credited | kill-credit fact red: "Expected: 0" on the dead player's tally |

Under m3 and m4 the Jack fact also failed once, on "collection was empty". That was a test flake, not the mutants. One throw places 1-3 pumpkins and skips a spot a mobile stands on, so about 7% of throws place nothing. I changed the fact to throw until something lands (up to 30 throws), and where nothing may land it throws five times. The red runs were then repeated (same 4 red), and the green run passed 16 of 16 three times in a row.

**Green:** 16 of 16 in the class, on three runs.

**The first gated build failed on my own fact, and that was a real finding.** `KillCreditIsJudgedAsTheCreatureWasWhenItDied` expected 0 pending snapshots at its end, but found 31 in the full suite. Other facts build creatures without hit points (Hits 0) and delete them, which takes a snapshot that no death ever reads. The cap kept that bounded. However, my first version emptied the whole table when it filled, which could also have dropped a snapshot a death was still about to read. I changed it to drop the oldest entry only. The fact now starts its nested-death case from an empty table (`ForgetPendingDeaths`, test support) and checks that the table is empty again after both deaths and after a staff delete. The class was green again (16 of 16) before the second gated build. This change came after the red runs above; it does not touch what they showed.

**Gated build:** I took the `docker-build` lock (11.3 GB free at the first launch, 4.7 GB at the second) and released it afterwards. The first `docker\uo\build.sh -t sl-modernuo:cc-P624` failed on the pending-snapshot check above. The second finished with EXIT=0: "Built sl-modernuo:cc-P624 with patches applied and 2482 shard test(s) passing". Of 2,486 tests, 2,482 passed and 4 were skipped (the real-map-data facts); none failed. The images are `sl-modernuo:cc-P624` = `7b13acc0e321` and `sl-uo-builder:cc-P624` = `719b3991ce47`. Both logs are `build-P624-run1.log` and `build-P624.log` in the session scratchpad.

## Deviations and decisions for Chase

- **Deliberate repair, for `docs/fidelity-principle.md` (the overseer promotes it):** an event Jack's pumpkins are confined to the live encounter inside Sorcerer's Dungeon. ServUO throws them wherever the attacker stands a second later, even after the event has ended. A hand-added Jack keeps ServUO's behaviour. The source's combat numbers are unchanged. Reversal: drop the `owner` checks in `CreatePumpkin_Callback`.
- **Ownership cleanup** extends P408's deviation 7 (the boss goes with the event): earlier rooms' survivors and the pumpkins' undead go too. Off and remove never sweep the rooms by type or art.
- **Saves from before this build** (spawner version 0) cannot name survivors of rooms they had already forgotten, or undead hatched from pumpkins. Loading one seeds ownership from the saved current room and boss only. It does not hunt for the rest, and does not delete ordinary dungeon creatures to make up for it. If the live world has leftovers from P408 runs, they need a separate staff action that Chase authorises. I did not inspect any world.
- **Read tool denied:** this unattended run auto-denied the Read tool on the ShatteredLegacy work copy (the first attempt was a Read of `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonData.cs` before editing it). I read with `cat` and made every edit with a scratchpad Python script, `apply.py`. It applies exact text replacements and refuses any that do not match exactly once. Nothing was skipped because of this.
- Not done here (they are later stages): reward purchase checks, the ring's one-time choice, the SA equipment pool, delayed reward timer coverage, the isolated server and client acceptance pass, title deeds.

## Unverified

- Nothing was run against a running shard or a client. The facts run on the test host, which has no map files (every spot fits, z 0) and registers the region itself. Real-map fit and the region edges in game belong to the PK4 acceptance pass.
- The live world's existing leftovers, and what the deployed build is, were not inspected. No connection to Haven was made.

## Remaining stages, as prompt drafts for the overseer to number

These follow the design's PK2-PK5, carried forward with what stage 1 now provides. `P<nn>` is for the overseer to fill in.

---

### Draft: Pumpkin King stage 2: purchases and the ring's one-time choice

```
# CC task P<nn>: Pumpkin King stage 2: purchases cannot overspend, the ring's skill cannot be overwritten

**Model:** Opus

**Touches:** server

**Summary:** Stage 2 of `notes\cc-P564-design-pumpkin-king.md` (PK2), after P624's stage 1. The Sorcerer's Dungeon reward gump delivers on confirmation before an unchecked point deduction, so two pending confirmations can spend the same points twice. The Sterling Silver Ring's final confirmation does not recheck that its skill slot is still unset.

## The work

1. Read the design's "Reward confirmations" section and P624's notes. In `event/SorcerersDungeonRewards.cs`, override the existing virtual `OnConfirmed` (BaseRewardGump.cs:186) with one server-loop transaction: check the current user, a live researcher on the same facet within range, a valid catalog row and the current balance; construct the item; require `DeductPoints` to succeed before delivery (delete the item on a failed debit); deliver to the backpack; on failure delete the item and refund the exact debit once. Do not call the base delivery as well. Do not change shared BaseRewardGump or other collections; note the inherited defect for them separately.
2. In `Items/EscapingAndSterlingRewards.cs` at the ring's final confirmation (around line 172), also recheck the bonus slot is unset; a second pending choice must not replace the first. Keep cancel, transfer and failed-confirmation behaviour.
3. Red-then-green tests in `server/tests/.../SorcerersDungeonVerification.cs`, driving the real confirmation callbacks: two pending 50-point purchases with 50 points deliver once; insufficient funds, cancel, a moved or deleted researcher, another facet and a full backpack lose no points and give no free item; refund exactly once on delivery failure; two pending different ring skills keep the first; cancel, deletion and transfer. Use `ShardTestClock.Arm()`; pin randomness rather than rerunning.
4. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG lines for what players see.
5. Notes `notes\cc-P<nn>-pumpkin-king-stage-2.md`. Last line `P<nn> DONE`.

Prices, the seven-item catalog and reward attributes stay as they are.
```

---

### Draft: Pumpkin King stage 3: the SA equipment pool and timed reward coverage

```
# CC task P<nn>: Pumpkin King stage 3: restore the Stygian Abyss artifact pool, cover the timed rewards

**Model:** Opus

**Touches:** server

**Summary:** Stage 3 of `notes\cc-P564-design-pumpkin-king.md` (PK3). Artifacts of Enchanted Origin never come as Stygian Abyss equipment: ServUO picks the SA tables half the time outside Tokuno and Malas, and the port's two-argument selector never does.

## The work

1. Read the design's "Restore the artifact equipment pool" section (the complete SA arrays in ServUO's order and the type each resolves to) and P624's notes. Add an event-local selector in `event/EnchantedOriginArtifacts.cs` or a sibling `EnchantedOriginLoot.cs`: ServUO's 50% SA branch (which includes ordinary equipment too), with entry weights as in the source; the full SA weapon list including Shortblade, StoneWarSword and GargishDagger; the pinned Type1 armour aliases, no duplicate armour. No global loot patch.
2. Take the death region and facet from P624's `DeathContext` (SorcerersDungeonData passes it to ProcessKill) rather than asking a deleted creature; keep authentication, property application and the tally reset on an award.
3. Red-then-green tests: a baseline failing regression for the missing branch; both branches chosen deterministically; every expected entry resolves and constructs; weights by entries; property roll and saved registry on a throwing weapon. Also real timer assertions with `ShardTestClock`: the Jack in the Box toy opens at about 9 s and resets 5 s later; the heart's five blood effects without damage; a pumpkin restored from a save hatches exactly once. Mutation evidence for behaviour that already worked.
4. `docker\uo\build.sh -t sl-modernuo:cc-P<nn>` green under the docker-build lock. CHANGELOG lines for what players see.
5. Notes `notes\cc-P<nn>-pumpkin-king-stage-3.md` listing any remaining property-roll or table differences for the overseer. Last line `P<nn> DONE`.
```

---

### Draft: Pumpkin King stage 4: play the event, check it in the client, write the player guide

```
# CC task P<nn>: Pumpkin King stage 4: acceptance pass on a scratch shard and the client, and the player guide

**Model:** Opus

**Touches:** server

**Summary:** Stage 4 of `notes\cc-P564-design-pumpkin-king.md` (PK4), after stages 1-3. Prove the event plays end to end on an isolated scratch shard, and in the supported client, before it is described to players.

## The work

1. Under the test-shard lock, on a throwaway loopback-only container with scratch saves (never Haven, never a shared world): on, room rotation, a boss, Jack, off, remove, save and reload. Use `[SorcerersDungeon status|on|off|remove|boss 9` (with `dryrun` first), console `tosd`, `[TOSDSpawner`, GM `[EnchantedOriginArtifact`. Read stage 1's "Owned by the event" status line before and after off and after a reload; no event creature or pumpkin may survive off or remove.
2. In the supported client package (record client and package versions): the nine bodies, Jack's outfit, pumpkin missiles 0xC6A-0xC6C and sounds 0x491/0x48F; the entrance dressing at the design's coordinates; the reward items and the bag's oddities; the researcher's menus, prices, Enchanted Origin message, ring selection, and the clilocs the design lists. Walk the entrance from the stock route.
3. Exercise earning, turn-in, purchases, the ring, bag (October only), toy and heart as a normal player. Test-only currency stays in the scratch saves.
4. Write the evidence and a short player guide in `notes\`: dates (10-24 to 11-02), entrance, shared rooms, earning versus spending, prices, the October-only bag, the three title deeds not offered.
5. Notes `notes\cc-P<nn>-pumpkin-king-acceptance.md`. If no usable client is available, finish the server half and leave client acceptance open. Last line `P<nn> DONE`.

No deploy, no wiki publish, no Shard Console buttons for this test.
```

---

### Draft (optional, only if Chase wants reward titles): size the shared reward-title system

```
# CC task P<nn>: size the reward-title system the Pumpkin King's title deeds need

**Model:** Opus

**Touches:** docs-only

**Summary:** PK5 of `notes\cc-P564-design-pumpkin-king.md`. The researcher omits ServUO's three title deeds (Hero of the Unloved 20, Savior of the Demented 30, Slayer of the Pumpkin King 50) because the shard has no reward-title collection. Measure what a faithful one needs before any PlayerMobile change is proposed.

## The work

1. Measure the smallest faithful saved title collection, title selection and display, and a BaseRewardTitleDeed port, against pinned's existing title paths; list its consumers and alternatives.
2. Supply the file list, patch arguments, save/load design, tests, and a separately reviewable implementation prompt that would then add the three deeds at source prices to the reward list and researcher previews.
3. Notes `notes\cc-P<nn>-reward-titles-sizing.md`. Last line `P<nn> DONE`.

Design only: no code, no PlayerMobile patch, no inert deeds for sale.
```

P624 DONE
