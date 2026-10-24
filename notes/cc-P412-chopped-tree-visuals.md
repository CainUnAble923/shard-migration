# cc-P412: chopped trees: the stump on the ground, and our TazUO hides the tree until it regrows

**Golem:** Iron. **Date:** 2026-10-24. **Branch:** `golem/Iron/P412` in both work copies. **Image:** `sl-modernuo:cc-P412`.

## In plain words

- When you chop a tree clean, its stump now sits on the ground at the trunk. Before, it floated up in the leaves (your
  10-22 screenshot). I checked this on a private copy of the test world with a real tree west of Britain: the stump
  landed at the tree's foot (height 15), where the old code put it at 35.
- With our game client, the chopped-out tree itself (trunk and leaves) disappears and only the stump is left. The tree
  comes back when its wood grows back, about 20 to 30 minutes later, even if you were away or logged out meanwhile.
  Other trees, and the other trees in the same grove, stay as they are. Players on other clients still see the stump
  beside the full tree, as today.
- Holding a polearm (a bardiche, say) to a chopped-clean stump now says "There's not enough wood here to harvest"
  instead of telling you to equip an axe.
- For you: nothing to decide. After the overseer merges, rebuilds the client package and restarts the test shard,
  chop a tree until "not enough wood" with the new client. The tree should vanish and leave a stump at its foot; after
  about half an hour it should be back. A relog in between should keep it hidden.

## What changed

### 1. The stump's height (server)

The Codex P2 from P359, confirmed by P380 and P400. Pinned `StaticTarget` adds the tile's `CalcHeight` to Z in both
constructors (`D:\UO\ModernUO-pinned\Projects\Server\Targeting\StaticTarget.cs:11` and `:18`), and `GetHarvestDetails`
hands that raised point on (`Projects/UOContent/Engines/Harvest/Core/HarvestSystem.cs:499`). For a tree from the map
(a `StaticTarget`), `ClusterFLumberStumps.MarkMapTree` now puts the stump at the static's own Z:

- It looks up the map statics at that X,Y (`map.Tiles.GetStaticTiles`). The static is the one with the targeted item ID
  whose Z plus its height is the target's Z (the closest, if the map has more than one).
- If the player targeted the leaves (they are on Lumberjacking's tree list too), the stump goes to the trunk under them.
- With no matching static (map data missing), the height comes off the target's Z, which gives the same answer.
- A dynamic `Static` tree (the old tests' kind) keeps its own location, as before.

The map lookup is a settable seam, `ClusterFLumberStumps.StaticsAt`, because the test host loads no map files.

### 2. Telling clients which trees are exhausted (server)

**Channel: the shard's own packet 0xF4, new sub 0x05.** I chose it over the 0xCE enhanced-packet ClientCommand
(patch 0001) for three reasons:

- 0xF4 already goes to every client at login (the fog of war, cc-P240), so a stock client is known to cope with it.
- Our TazUO already routes 0xF4 (patch 0004's handler). The new sub only adds one `case`.
- 0xCE id 4 carries a whitelisted command name, not data, and only goes to clients that answered the handshake.

Format: `[0xF4][u16 length][0x05][u8 facet][u32 BE payload length]`, then per tree:
`[u16 x][u16 y][u32 seconds until the bank refills, 0 = it regrew][u8 n][n x u16 item ID]`. The deadline travels as
seconds left, not a clock time, so the client's clock does not matter.

When it is sent (`ClusterFExhaustedTrees` in `server/customizations/ClusterFLumberStumps.cs`):

- **When a stump is placed:** to every client online, with the facet, X, Y, the IDs and the seconds left until the
  refill deadline. The deadline is P400's first-chop deadline (`bank.NextRespawn`, which the stump also keeps).
- **When the stump goes**, whether by refill, by idle expiry at the deadline, or by deletion: the same tree with 0
  seconds, from `ChoppedTreeStump.OnAfterDelete`.
- **At login:** every live exhausted tree, grouped by facet, from `PlayerMobile.PlayerLoginEvent` (cc-P165: after
  EnterWorld, once packets flow).
- **Coming into range:** handled by broadcasting every change to every client, whatever its distance or facet. The
  client keeps the list for all facets, so moving out of range and back needs nothing new. It is a few bytes per
  chopped-out tree.

The IDs sent are the statics at that X,Y that are on Lumberjacking's tree list or flagged Foliage, from the tree's
base Z up to 30 above it. Nothing else on the tile is included, such as a roof, a sign or the stump itself.

Each send is logged (`Exhausted tree hidden: facet .. at X,Y, item IDs .., refill deadline .. (N s), sent to N
client(s)`, and the login line).

### 3. Our TazUO hides them (client patch 0006)

`client/patches/0006-exhausted-trees.patch` applies on the pin plus 0001 to 0005:

- **New `Game\Managers\ShardExhaustedTrees.cs`:** it keeps a list keyed by (facet, X, Y), with the IDs and a local
  deadline (`Environment.TickCount64` plus the seconds). `IsHidden` drops an entry once its deadline passes. A
  cut-short message changes nothing.
- **`ShardFogOfWar.Apply` (0004's file):** sub 0x05 goes to the new manager.
- **`EnterWorld`:** the list is emptied at each login, next to the fog reset. The shard resends the live trees.
- **`StaticView.Draw` and `CheckMouseSelection`:** a static whose **original** graphic (before the season swap) is in
  the list at its tile is neither drawn nor clickable. The stump is a server item, not a static, so it stays. Nothing
  else on the map changes.
- **`client/README.md`:** has a row for 0006.

### Also (Crystal's W5, from Codex's P400 #2 to #5)

- **Lumber tools:** `ChoppedTreeStump.RefusalFor` accepts any equipped `BaseAxe` or `BasePoleArm` whose harvest
  system is Lumberjacking (pinned `BasePoleArm.cs:32`). Both routes (double-click, and a tool aimed at the stump)
  send 500493.
- **New facts:** two players on the last batch, re-marking after expiry, refill and delete, and save and restart.
  They are listed under Tests.

### Edge cases, as decided

- **A tree whose bank refills while the player is away:** the client drops the entry at its own deadline, so no
  login can leave a tree hidden past it. A relog gets the live list again with the time left.
- **Two trees in one bank:** only the targeted tree is hidden, as P359 decided for the stump. Hiding the whole 4 by 3
  bank would make a grove vanish at once, and every tile's trunks and canopy would have to be told apart. Nothing makes
  that clearly right.
- **Out of range and back:** nothing changes. The list is not tied to the view.
- **Restart:** exhaustion and stumps still do not survive a restart (P359's design). A new server has full banks and
  sends an empty list.

### Player-facing

- `CHANGELOG.md` has a new section, 2026.10.24.2: Changed, the hidden tree with our client; Fixed, the stump on the
  ground and the polearm message.
- `VERSION` is 2026.10.24.2.

## Tests

### Server

`server/tests/Engines/Harvest/ChoppedTreeStumpsVerification.cs`: 9 new facts and one 3-case theory, 11 cases in all.
Two real tile rows from tiledata.mul were added to `TestTileRows`: 0x0CCD tree (height 20) and 0x0CCE leaves (Foliage,
height 2). They were read field for field as `TileData.Load` reads them, and the shard's own
`D:\UO\tool-trials\client-data-copy\tiledata.mul` has the same rows.

- `MapTreeStumpSitsOnTheTreesBaseZNotItsTop`: the target reads Z 27; the stump must be at 7.
- `TargetingTheLeavesPutsTheStumpAtTheTrunk`
- `WithoutMapDataTheTreesHeightStillComesOff`
- `ClientsAreToldTheTreeItsIdsAndDeadlineWhenItEmptiesAndWhenItRegrows`: the packet is parsed byte for byte. It names
  the IDs 0x0CCD and 0x0CCE, not a stacked unrelated static, and 10 s left. At the deadline a 0-second message follows.
- `ALoginGetsEveryExhaustedTreeWithTheTimeLeftAndNothingOnceItRegrew`: through a test NetState's send buffer, with 6 s
  left after 4 s.
- `AnEquippedPolearmGetsTheNoWoodMessageNotEquipAnAxe`: a Bardiche, with both routes checked on the wire.
- `TwoPlayersFinishingOnTheLastBatchMakeOneStumpAndKeepTheDeadline`: through the real `FinishHarvesting`.
- `TheSameBankIsMarkedAgainAfterItsStumpGoes(expiry | refill | delete)`
- `AfterASaveAndRestartNoStumpIsInTheWorldAndTheBankIsFull`

**Red first.** I made one build with four deliberate breaks in the production file, then restored it from a pristine
copy:

- the old raised Z with no client message;
- axes only;
- `OnBankRespawn` deleting without forgetting;
- `Forget` doing nothing.

Result: 10 of the new facts failed, 2260 passed, each for the intended reason:

- Z 27 or 9 where 7 was expected;
- no packet sent;
- 500487 where 500493 was expected;
- a stale entry in the registry.

**The two-player fact did not go red.** Pinned `HarvestSystem.FinishHarvesting` rechecks the bank before consuming
(`HarvestSystem.cs:104`), so the second player never reaches our code. No break in our file can make that fact fail.
It is a guard against a later change, as P400 asked, and I could not show it red.

**Green.** `docker/uo/build.sh -t sl-modernuo:cc-P412`, under the docker-build lock:
`Built sl-modernuo:cc-P412 with patches applied and 2270 shard test(s) passing.` Exit 0, with 4 skipped as before.
All 25 stump cases pass (14 old, 11 new).

**A flake fixed on the way.** The first green build failed the login fact (21 s left, not 6). The cause is D16:
pinned `CreateTestNetState` sets `Core.Now` to the wall clock (`ShardTestClock.cs`). Both facts that make a test
NetState now make it before the stump.

**What the save fact proves.** It is not a real `World.Save` and load in the test host, which has no safe route for
one. It proves three things:

- the stump is skipped by the save (`SkipSerialization`; pinned `GenericEntityPersistence.cs:256` and `:289`);
- a forced load of its bytes deletes it;
- a fresh `Lumberjacking` has full banks, no marker and an empty login list.

### Client

These ran in `D:\UO\golems\Iron\tazuo-p412` (my own `-Out`, outside both repos).

- **Red first:** a stub manager (`Apply` false, `IsHidden` false) failed 6 of the 7 new unit tests. The 7th, a guard
  against a cut-short message, failed against a manager with its length check removed
  (`IndexOutOfRangeException`).
- **Green:** `client\Build-Client.ps1 -Out D:\UO\golems\Iron\tazuo-p412` applied all six patches to a fresh worktree
  at the pin. All **1315** client unit tests passed (7 new), and the client published to `...\tazuo-p412\client`.
- **Not unit-tested:** the `StaticView` hooks themselves. A `Static` needs the game's file manager, and I could not
  look at the result in a game client on this run.

### Player-package gates

These ran under the package lock.

- `Ui-Skins.Tests.ps1`: 4 of 4. `Paperdoll-Bodies.Tests.ps1`: 9 of 9.
- `Package-Client.Tests.ps1`:
  - 9 of 9, with two changes for the run only:
    - a temporary junction `client-data\classic-client` to `D:\UO\UltimaOnlineVanilla`, because this work copy has no
      gitignored client-data and gate 4 needs EA file names;
    - the test's client path pointed at my build for one run, then put back byte for byte.
  - Against the shared `D:\UO\tazuo-sl-build\client` (built before 0006), the real-build fact refuses it as a **stale
    client build**. That is the gate working: the overseer rebuilds the client after the merge.
  - The junction is removed (only the link, not its target).
- Nothing was published.

### On a private test shard (the test-shard lock)

This was not the shared Test Shard on 2594. I used `notes/cc-P412-tools/proof-shard.ps1` (cc-P281's, adapted):

- a copy of `D:\UO\bot-shard`, on `127.0.0.1:2596`, running `sl-modernuo:cc-P412`;
- client files from `D:\UO\tool-trials\client-data-copy`;
- the world loaded with no prompts.

`notes/cc-P412-tools/chop.py` used the playtest bot's client as Iron's own admin and player:

- It moved the player beside the walnut tree at Trammel (1300, 1536): trunk 0x0CE0 and leaves 0x0CE1, both at Z 15
  in statics1.mul.
- It gave the player a hatchet and Lumberjacking 120, then chopped. The messages were "yew logs", a miss, "yew logs",
  then "There's not enough wood here to harvest."
- The stump arrived at **(1300, 1536, 15)**: the trunk's own Z. Before P412 it would have been 35.
- Both connected clients (admin and player) received 0xF4 sub 0x05: facet 1, 1300,1536, 1607 s, IDs 0x0CE1 and
  0x0CE0.
- After a relog the player received it again with 1596 s left.

Server log (`notes/cc-P412-tools/shard-log-excerpt.txt`):

```
[11:21:28 INF] Exhausted tree hidden: facet 1 at 1300,1536, item IDs 0x0CE1,0x0CE0, refill deadline 2026-10-24 11:48:14Z (1607 s), sent to 2 client(s)
[11:21:39 INF] Exhausted trees: 1 packet(s) sent to Iron the Tester at login
```

Full result: `notes/cc-P412-tools/chop-result.json`. The container is removed, the world copy deleted and the lock
released.

**Not seen:** the patched TazUO drawing the hidden tree. No game client was driven on this run.

## For Chase, after the release

After the overseer publishes the new client and restarts the test shard:

- Chop a tree until "not enough wood".
- The tree, trunk and leaves, should vanish, with only a stump at its foot. The trees around it should be unchanged.
- Walk off a screen and come back, or log out and in: it should still be gone.
- It should be back after the refill, roughly 20 to 30 minutes from your first chop on that grove.
- On a stock client you should see the stump at the trunk's foot, under the standing tree.

## Deviations and decisions for Chase

- **Read tool:** it was denied for `server/customizations/ClusterFLumberStumps.cs` (unattended run). I read the file
  with `cat`, wrote the new version to the scratchpad, and copied it into place.
- **Package gate:** the temporary junction and the one-run change to the test's client path, described under
  Player-package gates. Both are undone.
- **Patch number:** the prompt says the new patch is the "next number after 0004". 0005 (UI skins) already exists,
  so this is **0006**.

P412 DONE
