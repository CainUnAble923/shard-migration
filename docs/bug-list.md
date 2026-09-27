# Bug list: defects to look at fixing

Distinct from `patch-backlog.md`, which is about capability ModernUO does not have. This file is
about things that are **wrong**: ours, ServUO's, and ModernUO's.

**The rule that governs most of this file**, set by S2's D-4 and followed since:

> A ServUO bug that produces a *missing* result is copied faithfully. Fixing it would hand our
> players behavior no OSI or ServUO player gets, which is a fidelity deviation in the direction
> nobody thinks to check a wiki for. A ServUO bug that produces a *broken* result is fixed.

"Missing" means a branch never fires, a drop never rolls, a name reads oddly. "Broken" means the
game shows the wrong thing or a player cannot proceed. D-10, D-16 and D-46 are the three fixes; §3
is everything left alone.

**The `Dn` numbers in this file are local to this file** and are not the `D-n` deviations in
`fidelity-principle.md`. Only the hyphen tells them apart, which is thin, so: **the next free number
here is D24.** I collided four of them on 2026-09-26 by numbering new rows from the highest in
section 1 without reading section 2, and `notes/gate-integrity.md` was written against the wrong
two as a result. Read the whole file before taking a number.

---

## 1. Open, ours, worth fixing

| # | What | Impact | Where |
|---|---|---|---|
| **D21** | **Docker Desktop's port publishing hides every client address.** Every connection reaches ModernUO from `172.19.0.1`, the bridge gateway, whether it came from loopback, the LAN or the internet: 34 of 34 `Client:` lines on live, and probes from both `127.0.0.1` and `192.168.1.58` logged identically | **three features are silently off.** `ServerList` cannot tell a LAN client from an internet one, so `autoDetect` relays everyone to the container's own address; `maxAccountsPerIP` is a **shard-wide total**, not per household; and `IPRateLimiter` exempts every client as private (`IPRateLimiter.cs:59`). Any per-IP ban would ban everybody | `notes/player-package.md` A.1. Reverses under host networking, or on a Linux host where Docker preserves the source address. Neither is small. **Until then, treat every per-IP feature as off** |
| **D22** | **`docker compose -f docker-compose.test.yml down --remove-orphans` would stop the live shard.** Both compose files sit in the same directory and so share the project name `uo`, which makes compose report `sl-modernuo` and `sl-ddns` as orphans of the test stack | one flag away from a live outage, on a command that reads as safe | one line, `name: sl-uo-test` at the top of the test file, then remove the old test container once by hand. Not done in the task that found it: it changes the test stack's network |
| **D23** | **`sl-ddns` is unhealthy and rewrites Cloudflare every ten minutes.** It reads the record back through the router's split DNS, which answers `192.168.1.58`, so it never sees the value as correct although Cloudflare already holds `216.247.206.76` | API churn, and a health status nobody can trust | give ddns-updater a public resolver. Which setting does that is unverified |
| **D19** | ~~**`Start-TestShard.ps1 -Fresh` cannot produce a usable shard.**~~ It wipes `Saves-test`, re-copies the live `Accounts` folder in, builds, and starts the container. The copy succeeds (`Accounts.bin`, 1281 bytes, correct path), but **with no world save present ModernUO does not pick the accounts up**: `Loading world done` reports only what the seeders just created, `Accounts.Count` is 0, and `AccountPrompt.Initialize` blocks on `ConsoleInputHandler.ReadLine()` at "Do you want to create the owner account now?" The listener never opens | **every `-Fresh` run ends here.** This is the September defect (section 2, D7) resurfacing in the one code path written to prevent it. The guard protects a world save that has lost its accounts, which is not the case `-Fresh` creates | **FIXED 2026-09-26.** Cause probed: `Persistence.Load` resolves every saved entity through `SerializedTypes.db`, and `-Fresh` seeded `Accounts/` without it, so every account hit `ctor == null` and was skipped **silently**. Both scripts now seed that file too, and the PowerShell one reads the container log after `up` and prints the `docker attach` recipe if it finds the prompt instead of the listener. Watched failing |
| **D20** | **The S3/S9 content index cannot see `[TypeAlias]` names, or secondary types nothing references.** It strips string literals before indexing, so a name that exists only inside a `[TypeAlias(...)]` looks absent; and it resolves one primary type per file, so everything else in a discarded file vanishes unless some candidate happens to reference it | **this is what produced the kilts.** S9's own appendix prints `upstream: GargishClothKilt` for three of them and then bucketed them as needing a patch, when what they needed was ordinary content work. Measured: 45 alias-only names that are ServUO types, 26 ServUO files whose primary type is alias-only, 19 classes deriving from one, and 482 unreferenced secondary types across 234 discarded files | `notes/armour-set-completion.md` Part B. Fix: index alias strings as declarations of the aliased type, and report every secondary type of a discarded file. Both scripts exist in that task's scratch, about 80 lines together. **482 is an upper bound and must not be quoted as a content backlog** |
| **D15** | **The test host regenerates one hit point every 8 ms**, in every fact. `UOContentFixture` never runs `RegenRates.Configure`, so `Mobile.DefaultHitsRate` is `TimeSpan.Zero`, `HitsTimer` runs at a zero interval and a damaged mobile gains a hit on every wheel tick: 125 a second | any fact that reads hit points across an `Advance` after damage is measuring regeneration, not the effect. One fact was bitten (D11) and two work around it deliberately | **Q-060 answered: leave it, write the rule down, and add a guard fact.** The rule belongs in the `ShardTestClock` header and `notes/port-recipe.md` |
| **D16** | Two `ShardTestClock` truths its own header does not state. **`Arm()` leaves dropped timers flagged `Running`**, so an object created before an `Arm()` holds a timer that can never fire or restart. And **`Core.Now` is wall-clock after any fact that makes a test NetState**, because `PacketTestUtilities.CreateTestNetState` sets `Core._now = DateTime.UtcNow` (`:62`), so `Epoch` is not the process-wide base the header implies | harmless today: every timed fact creates its objects after `Arm()`, and nothing reads the date or time of day. A later fact that does either would be wrong and would look right | `notes/gate-integrity.md` A.5. Fix the header when something next touches that file |
| **D17** | `NewHavenQuestBoardVerification.cs`'s header still says no fact there can send a gump. **D12 made that false** | a note that will send the next reader down the headless route for no reason | drop the sentence in the Q-058 picker task, which rewrites that file anyway |
| **D13** | **`NewHavenQuestBoard.Place()` searches Trammel only.** A board on any other map, `Map.Internal` included, is invisible to the search, so `Place()` builds a second one and the first keeps every quest held from it | GM-only, and no board is placed yet | one line. Folded into the Q-058 picker task |
| **D14** | **Nothing places a Fountain of Fortune**, three weeks after Q-021 answered where it goes (Ter Mur `1121, 957, -42`). `grep -rn "1121, 957\|FountainOfFortune()" server/` finds only the constructor and its test | the LuckyCoin's only reachable outcome is still its failure message, which is what D-4 of S2 said in September | an answered question that was never implemented. Small task |
| **Q-009 / D3** | `docker-compose.yml` carries an **uncommitted change** repointing the live script mount at `server/customizations` read-only. Directionally right, never verified, deploy-affecting | live shard | **CHASE decides.** Oldest open item on the project |
| **D4** | **Build cost is 6x the published estimate.** 20s unchanged, 266s with one changed file, against `cc2-timed-port.md`'s 0:44 which predates S4 and neither compiled nor ran tests | every batch estimate is optimistic | fix the estimate, not the build |
| **D6** | The runtime image ships **16 test-infrastructure assemblies of 53**, because the Dockerfile publishes `ModernUO.slnx` | inert, cosmetic | Q-032. **The trap:** that same publish line is the compile gate. Any fix must lose the test assemblies *and* still fail the build on a deliberately broken test |
| **D5** | `server/uo/` build tree is stale and predates the F1 recovery | confusing, not harmful | leave; gitignored and generated |
| **D2** | ModernUO has no `Quest.StartingItem` equivalent. **How many of the 203 quests need one is unmeasured** | blocks an unknown slice of the quest row | Q-025, measure before the quest batch |

## 1b. Our own documentation defects, because a wrong note costs as much as a wrong line

Six D-numbers and one patch row have now been written claiming ModernUO lacks something it has.
All were caught in review or by a later batch, none reached a player, and all share one cause.

| What was wrong | Found by | Cause |
|---|---|---|
| **D-47**: `SkeletalLich` "casts Magery only; its Necromancy is set and unused" | review, Q-050 | stock `MageAI` carries the necromancer branch; it casts necro 44-48% of the time |
| **D-45**: `Spellbinder` loses "spirit-speak heal, teleport and dispel" | review, 2026-09-26, while building the D-register | pinned `MageAI` has all three as its own constants: `HealChance = 0.10`, `TeleportChance = 0.05`, `DispelChance = 0.75` (`:18-20`). ServUO's are 5%, 5%, 75%. **The whole deviation is 5 points of heal chance.** This is the `HealChance` trap already named in `AGENTS.md`, so the trap was written down and the entry it had already produced was never revisited |
| **D-44**: `GreenGoblinScout` loses "hide, blink and flee below 20%" | settled 2026-09-26. **The flee claim is wrong**, the other two stand | the scout runs `AI_Melee`, and pinned `MeleeAI` overrides `BaseAI`'s `FleeHealthThreshold => 0.0` to `0.2` with `FleeChance => 0.1` (`MeleeAI.cs:9-10`). Restate D-44 at two thirds its recorded size |
| **My own claim that pinned's AI base class was "not in the checkout"** | me, an hour later | I ran `find` in the cloud container, where only staged files exist, and read the empty result as a fact about the pinned tree. It is at `Projects/UOContent/Mobiles/AI/BaseAI/BaseAI.cs`. **The same error as the rest of this section, one level up:** an absence where I happened to look, taken as an absence in the thing itself. It reached a committed document. The check is to list the directory on the machine that holds the tree |
| **P1's top row**: `AI_NecroMage`, "189 lines for 20 creatures, best value on the board" | review, Q-050 | written from D-47 without checking pinned. Withdrawn |
| **D-55, D-56, D-62, D-68**: `DragonBreath` dropped as a Pet Training loss on four creatures | CC6 batch 5, Q-054 | pinned has it as `MonsterAbilities.FireBreath`/`ColdBreath`. **CC4 had already used it** |
| Three "losses" in one CC6 batch 3 brief: `SetAreaEffect(AuraDamage)`, `HealChance`, `SetMagicalAbility(Poisoning)` | CC6 batch 3, in pre-flight | the first two exist under other names; the third only ever ran in a `Deserialize` branch |
| CC9 §2b listing `GargishClothKilt` as an extract still to do | CC6 batch 5 | pinned registers that name as a `[TypeAlias]` of its stock armour |

**The single cause:** reasoning from ServUO's vocabulary to ModernUO's capability. A missing enum
member, a missing method name or a missing type name is evidence about the *name*. The check that
settles it is to grep pinned for what the thing **does**, and it takes one command.

**The counter-habit that works**, and the reason none of these shipped: every batch's pre-flight
greps both trees for every type it is about to touch, and reports what it finds rather than what the
brief told it. Batches 3, 4 and 5 each corrected their own brief this way, three times over.

## 2. Fixed, kept so the cause is not re-learned

| # | What it was | Cost |
|---|---|---|
| D7 | A fresh test world blocks on `AccountPrompt` forever. No accounts means `ConsoleInputHandler.ReadLine()` on stdin: `docker ps` says Up, the listener never opens, the client hangs at "verifying account". The prompt fires at container start, so attaching later shows nothing to answer | **a week** |
| D8 | The test shard relayed clients onto the **live** shard. `Configuration-test` copied the live config, which advertises `192.168.1.58` with `autoDetect` false | a test session could silently run against live |
| D9 | `docker-compose.yml` mounted the **live world save**, so testing wrote into the real world | one stray account reached the live save before this was caught |
| D10 | `MAKE X` label invisible: `AddLabel` given `0x7FFF`, an RGB555 color, where a hue index belongs | open since June; affected the **live** shard |
| **D11** | **The build gate went red about one run in five, and the cause was not timing.** `CC6Batch8Verification`'s stygian fireball fact asserted a hit was still visible 4 s after the damage, in a host that regenerates 125 hits a second (D15). The player had 125 max hits, not the ~300 its comment assumed, because ML caps a player's `Str` at 150. So a roll of 126-150 killed and the fact passed; a roll of 120-125 left the player alive to regenerate, and the fact failed. **6 rolls in 31, 19.4% by construction**; measured 8/50 on HEAD and 15/60 in process, 0/50 after, plus 10/10 full `build.sh` runs. Fixed by reading the hit on the wheel tick it lands and asserting the fireball's own range | four wasted FINAL attempts on 2026-09-26, and **every green build claimed before it was a 4-in-5 draw**. My prompt's "wall-clock dependency", "streaks" and 35% rate were all noise |
| **D18** | **`progress.py` and `build.sh` disagreed on the test count by exactly one**, from CC6 batch 2 until 2026-09-26: 69 against 68, then 137 against 136, then 138 against 137. The cause was that `progress.py` counted the **substring** `[Fact]`, and `AthenaeumIsleQuestVerification.cs:7` carries one **in a comment**. It now counts attribute lines and agrees with the gate | every test count this project published for three weeks was one high | found and fixed in the armour-set task. The constant gap was the clue and nobody followed it |
| **D12** | **No shard test could assert on a gump**: the builder stage had none of the runtime stage's native libraries, so the first gump a test compiled killed the test host in `LibDeflateBinding`'s finalizer. Fixed with one 2.1 MB layer after the ModernUO clone, carrying exactly the runtime stage's list less what line 6 already had, and proved by `GumpOnTheWireVerification`, which was watched dying on the old Dockerfile and is kept as the gate for that layer | the quest board task spent most of ninety minutes proving its gumps headless instead. `libzstd` and `libargon2` were the same trap waiting for the first test to touch archives or password hashing |
| S8/D1 | The test route could not construct any `BaseCreature`. **The cause first recorded here was wrong** (Q-031): the data file was in the test output all along. Nothing called `NPCSpeeds.Configure` | a wrong diagnosis that survived a week |

**A diagnostic that proves nothing, learned 2026-09-26 while D19 had the shard blocked:**
`Test-NetConnection <host> -Port <published port>` against a Docker-published port **succeeds whether or
not the process behind it is listening**, because Docker's forwarder accepts the connection itself. It was
used to rule out the server side and it ruled out nothing; the answer was in `docker logs` the whole time.
`docker ps` saying Up is the same kind of non-evidence. For "is the shard actually accepting players", read
the log for the listener, or connect a client.

**The pattern in D7 through D9, worth naming:** three of the four were *test rig* defects that made
the rig quietly point at production. None was found by reasoning; each was found by asking the
machine. The week D7 cost was spent on four plausible fixes applied without first probing whether
the thing being fixed was the thing that was broken.

## 3. ServUO behavior copied on purpose, do not "fix" these

Every one of these reads like a typo and is ServUO's. They are here so the next reader does not
correct them, and so that if we ever change the rule we know what the list is.

**Unreachable branches and dead rolls**

- `ToxicSlith`'s drop switch rolls `Utility.Random(2)` over cases 0 and **2**, so the `SlithEye`
  branch never fires: a toxic slith drops a venom sac 2.5% of the time and never an eye.
- The fountain's buff branch rolls `Utility.Random(4)` over a **six**-case switch, so special
  protection and balm boost never fire (S2 D-4, the precedent for this whole section).
- `LowlandBoura.OnDeath` says `if (Controlled) return;` and then `if (!Controlled)`.
- `Race.RandomFacialHair(this)` returns an int and discards it on both emulators. It has never
  assigned facial hair to anyone.
- `GreenGoblinScout.OnThink` does not call the base, so no ML shout.

**Names and appearance**

- `PitFiend` is "a Pit fiend", capital P, and its header says it was copied from the daemon.
- The enslaved goblins' corpse is "an goblin corpse"; `PutridUndeadGuardian` is "an putrid undead
  guardian"; `SentinelSpider` is "a Sentinel spider".
- `EnslavedGreenGoblinAlchemist` is named "Green Goblin Alchemist" with no "Enslaved", and wears
  the free goblins' body 723 while its five siblings wear 334.

**Values that look wrong**

- `ClanRibbonPlagueRat` sets `Tamable = false` with a `MinTameSkill` of **−0.9**.
- `EnslavedGoblinMage` is a melee creature with 510 Int and no Magery.
- `LavaElemental`, `GargoyleShade`, the three sliths, `Gremlin`, `TrapdoorSpider`, `Skree` and
  `UndeadGuardian` set no Fame or Karma. `ForgottenServant` has no `[CorpseName]`.
- `GargoyleShade` has no Energy resistance.

## 4. ServUO bugs we did fix, and why each cleared the bar

| # | What | Why it is "broken", not "missing" |
|---|---|---|
| D-10 | `GargishWarHammer` flips to `0x48C1`, not ServUO's `0x481` | `0x481` is a Prism of Light **pillar** graphic. Every other gargish weapon flips to itemID+1. ServUO's value turns a flipped war hammer into a pillar |
| D-16 | `DarkwoodCrown` flips to `0x3168`, not `0x3169` | `0x3169` is the flipped Vulture Helm. Same shape |
| D-46 | `ShameWall` sets `Visible = true` in its constructor | ServUO leaves `BaseAddon`'s `false`, so a fresh wall's teleporters are inert and **a player cannot push through it** until that wall's troll has died once (Q-046) |

## 5. ModernUO upstream

| # | What | Evidence | Disposition |
|---|---|---|---|
| **E1** | **`SetPassword` stores an unverifiable hash under SHA1/SHA2.** `_passwordAlgorithm` is still the enum default at the first `SetPassword`, so the phrase choice and the stamped algorithm disagree and `CheckPassword` can never match. With auto-account-creation on, a new player logs in once and never again | proven three ways in P1: the stored hash was exactly `SHA512("p1testpass")`, a packet capture confirmed correct credentials, and rewriting the hash to `SHA512("p1adminp1testpass")` fixed login immediately | **report upstream.** Costs us nothing now; the SHA2 block is reverted |
| **E3** | **A held ML quest is saved against its giver's serial only**, with no type (`MLQuestEntry.cs:520`, and upstream's own TODO at `:536` says "Serialize quester TYPE too"). `Deserialize` drops the instance if that serial is gone. **So deleting a quest giver silently removes that quest from every player's log at the next restart**, even though a replacement giver takes the quests over while the server keeps running | read from pinned source in `notes/new-haven-quest-board.md` §4.4; not probed across a restart | **report upstream.** Live hazard for us in two places: never `[remove` the New Haven board, and the New Haven seeder's `replace` mode for the 26 trainers has the same effect. `NewHavenQuestBoard.Place()` moves a board and never replaces one, for this reason |
| **E2** | ModernUO has **no armour set-bonus system**. Standard OSI content. We built it in 387 lines plus three small patches | S1, five passing tests, 111 files unblocked | **contribute upstream.** If taken, our maintenance on the highest-value thing we have built drops to zero |

---

## Keeping this file honest

- A defect found during a task goes in that task's `notes/` file first, with what proved it. It is
  promoted here in review.
- **A fix is not a fix until a test has been watched go red without it.** `AGENTS.md` requires the
  red proof and this file assumes it.
- Anything in §3 that a player actually complains about moves to §1 with their complaint attached.
  The rule in the banner is a default, not a verdict.
