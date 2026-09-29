# cc-P9: the test shard as an OSI Test Center

Brief: `D:\UO\cc-prompts\cc-P9-test-center.md` (2026-09-29). Server tree `D:\ShatteredLegacy`, pinned
`D:\UO\ModernUO-pinned` at 7c9215d97. ASCII only. Nothing deployed, built into a runtime image, restarted,
recreated or committed by this task.

**Precondition checked.** `D:\ShatteredLegacy` `git --no-optional-locks status`: clean, HEAD `4f35b6c` "P8: fix the
two test bugs d8077d7 swept in". P8's two patches and their `apply-patches.sh` lines (`:318-319`) are committed.

---

## 1. Part A: how the test shard is configured

| Question | Answer | Evidence |
|---|---|---|
| Where `sl-modernuo-test` is defined | `docker/uo/docker-compose.test.yml`, compose project `sl-uo-test`, service `modernuo-test`, `container_name: sl-modernuo-test`, image `sl-modernuo:latest` (the same image as live), `restart: "no"`, ports `2594:2594` tcp+udp | the file; `docker ps` shows it Up on 2594 |
| Volumes | `server/customizations` -> `/modernuo-projects:ro`; **`server/uo/modernuo/Configuration-test` -> `/modernuo/Configuration`**; `server/lib/uo/modernuo/Saves-test` -> Saves; client-data ro | compose file; `docker inspect sl-modernuo-test` Mounts agrees |
| Live's config | `server/uo/modernuo/Configuration` -> `/modernuo/Configuration` in `docker/uo/docker-compose.yml` | the file |
| **Separate?** | **Yes.** Two host directories, each bind-mounted into its own container. `test-shard.sh` and `Start-TestShard.ps1` seed `Configuration-test` by copying live's **only when it does not exist**, then rewrite the listener to 2594 and the server name. Nothing copies test back to live. | `docker/uo/test-shard.sh` "Its own Configuration copy"; `Start-TestShard.ps1` same block |
| `testCenter.enable` today | `"False"` in **both** (`Configuration/modernuo.json:161`, `Configuration-test/modernuo.json:159`) | grep |
| Listener setting | top-level `"listeners"`: live `["0.0.0.0:2593"]` (`Configuration/modernuo.json:8-9`), test `["0.0.0.0:2594"]` (`Configuration-test/modernuo.json:6-7`). Read by `ServerConfiguration.Listeners` (`Server/Configuration/ServerConfiguration.cs:39`, a `List<IPEndPoint>`) | grep, pinned |

Both config trees are under `server/uo/`, which `.gitignore:35` ignores. **So the config change in Part B is not
in any commit** and is not visible in `git diff`; it is recorded here instead.

Other differences between the two `modernuo.json` today (a plain `diff`): test has `maxAccountsPerIP` 5 vs live 25,
`encryptionAlgorithm` Argon2 vs SHA2, the listener and the server name. Nothing else.

### Things in our tree that change what "Test Center" means here

Found while confirming the brief; each changes a design choice below.

- **Both shards already accelerate gains.** `ClusterFSkillGain.cs` wraps all four `Mobile.SkillCheck*Handler`s
  (`:36-46`): 3 chance attempts per check and 5x the gain amount, on live and test alike
  (`clusterf.skillGain.*`, `Configuration/modernuo.json:107-109`). Its extra gains call `SkillCheck.Gain` directly
  (`:131`), so they do not pass through `GainFactor`. Part C's multiplier stacks on top of this: it raises the
  chance of the *first* gain roll in each attempt.
- **Our caps are far above pinned's Test Center caps.** `ClusterFSkillCaps` sets every skill cap to 300 and the
  total to 58 x 300 (`ClusterFSkillCaps.cs:106-123`, config `individualCap` 300, `totalCap` 0). `ClusterFStatCaps`
  sets `StatCap` to 1500 (`ClusterFStatCaps.cs:104-107`). Both apply on `PlayerLoginEvent` and on world load.
  Pinned's `FillBankAOS` **sets** the power-scroll skills' caps to 120 and `StatCap` to 250
  (`TestCenter.cs:226-231`): on this shard that is a *lowering*. Part D deals with it.

---

## 2. Pinned, confirmed line by line

All at 7c9215d97, `Projects/`.

| Brief's claim | Confirmed | Where |
|---|---|---|
| `testCenter.enable`, default false | yes | `UOContent/Special Systems/Engines/TestCenter.cs:17-20`. `Enabled` has a **private setter** (`:15`); only `Configure` assigns it |
| speech `set <skill> <value>`, `set str/dex/int` | yes, registered in `Initialize` only when `Enabled` (`:22-29`) | `:38-80`; stats 10..125 and `StatCap` (`:88-152`); skill 0..`skill.Cap` and total cap (`:154-190`) |
| speech `help` opens a gump | yes | `:81-85`, `TCHelpGump` `:671` |
| `FillBankbox` at creation | yes | pinned `Engines/Character Creation/CharacterCreation.cs:267`; ours `server/customizations/CharacterCreation.cs:245-248`, routed by `apply-patches.sh:235` |
| AOS fill: caps 120, StatCap 250, checks, gold, kegs, tools, ammo, maps, raw materials, spell stuff, ethereals, artifacts, bows | yes | `FillBankAOS` `:220-547`; `FillBankbox` `:549-555` picks it under `Core.AOS` |
| instant logout | yes | `Mobiles/PlayerMobile.cs:4333` |
| welcome text | yes | `Misc/WelcomeTimer.cs:19` |
| deletion age check | yes | `Accounting/AccountHandler.cs:22-23`, used at `:213` |
| `GainFactor` settable | yes | `Server/Skills.cs:443` |
| gain chance scaled by it | yes | `UOContent/Skills/SkillCheck.cs:119`, then floored at 0.01 (`:121-124`) |
| `AssemblyHandler.Invoke` | yes | `Server/AssemblyHandler.cs:132-149`: `Core.Assembly` first, then `Assemblies`, then `List.Sort(CallPriorityComparer)` |
| client delete path | **`:184`, not `:185`**: `DeleteCharacter` is `IncomingAccountPackets.cs:184-191`, calling `DeleteRequest` at `:190` | |

Also confirmed: default priority is 50 when a method has no `[CallPriority]` (`Server/Attributes.cs:74-85`); neither
`TestCenter.Configure` nor `AccountHandler.Configure` has one. `Main.cs:441` Configure, `:446` World.Load, `:448`
Initialize. `SkillInfo.Table` is filled in `SkillsInfo.Configure` (`UOContent/Skills/SkillsInfo.cs:135`), priority 50.

---

## 3. Part E before patching: the alternatives

The Part E patch is to an upstream file, so AGENTS.md wants its alternatives here before it is written.

`RestrictDeletion` is `private static readonly bool = !TestCenter.Enabled` (`AccountHandler.cs:22`). The class has no
static constructor, so it is `beforefieldinit` and the initializer runs no later than the first static access,
which is `AccountHandler.Configure` itself (`:56`). Its value then follows whether `TestCenter.Configure` happened to
run first, which is decided by an unstable sort of 50-priority methods.

| Option | Cost | Why not |
|---|---|---|
| **A. Patch `:22` to a property: `private static bool RestrictDeletion => !TestCenter.Enabled;`** | one line, one patch | chosen |
| B. `[CallPriority]` on `TestCenter.Configure` so it runs first | a patch to `TestCenter.cs` instead | Still depends on nothing else touching `AccountHandler`'s statics earlier (e.g. `Account.LogAccess` reads `AccountHandler.IPTable`, `Account.cs:1046`). It fixes the order, not the freeze. |
| C. Overwrite the field by reflection from our code | no patch | .NET refuses to set an `initonly` static after type init (`FieldAccessException`); and a reflection write into pinned is harder to see than a patch |
| D. Our own 0x83 packet handler with a copied `DeleteRequest` | no patch | Copies upstream logic; `docs/subsystem-policy.md` says a failing patch beats copied logic, because a pinned bump silently leaves the copy behind |

A single-line patch that fails loudly on a pinned bump is the smallest option that removes the freeze and not just
the order.

---

## 4. What changed

### Config (not in git; `server/uo/` is ignored)

`server/uo/modernuo/Configuration-test/modernuo.json`, and nothing else:

    "testCenter.enable": "True",                 (was "False")
    "testCenter.skillGainMultiplier": "5.0",     (new; the one constant for Chase to change)

Live's `Configuration/modernuo.json` untouched: sha256 `e6f8d5fb...4258b` before and after this task, `testCenter.enable`
still `"False"` at `:161`. The pre-change test config is kept at the scratchpad as `modernuo-test.pre-p9.json` for this
session only. **If the running test server rewrites its config before the recreate, check these two lines survived.**

### Code, all in `D:\ShatteredLegacy`

New folder `server/customizations/TestCenter/`, mirrored to `Projects/UOContent/TestCenter/` by `apply-patches.sh:212`
(pinned has no such folder, so nothing is overwritten):

| File | Part | What |
|---|---|---|
| `TestCenterLiveGuard.cs` | B | `Initialize`: one `logger.Error` line if `TestCenter.Enabled` and any `ServerConfiguration.Listeners` port is 2593 |
| `TestCenterSkillGain.cs` | C | `Initialize`: reads `testCenter.skillGainMultiplier` (default 1.0), multiplies every `SkillInfo.Table[i].GainFactor` from its remembered original, logs it; refuses and logs unless `TestCenter.Enabled` |
| `TestCenterFillCommand.cs` | D | `[TCFill`, Player level, registered in `Initialize` only when `TestCenter.Enabled`, 10-minute cooldown per character serial |
| `TestCenterKit.cs` | F, D | the registry (`Register(factory, amount)`), `PlaceKit` (gated), `RefillBank` (pinned's fill with our caps kept, then the kit) |
| `TestCenterKitEntries.cs` | F | our 32 resources, registered in `Configure` |
| `TESTKIT.md` | F | "When you add a new resource, add one line here", with the one-line example. Not compiled; `apply-patches.sh` reports it as a non-.cs NOTE and skips it |

Edited: `server/customizations/CharacterCreation.cs` (ours, a full replacement): `TestCenterKit.PlaceKit(newChar)` beside
`TestCenter.FillBankbox(newChar)`, inside the existing `if (TestCenter.Enabled)` in the Player-level branch.

Patch: `server/patches/AccountHandler-test-center-deletion.patch`, wired in `docker/uo/apply-patches.sh` after P8's
block. **This is a new pinned change carried as a patch**, like every other pinned change in the repo.

Tests: `server/tests/Misc/TestCenterVerification.cs`, namespace `ShatteredLegacy.Tests`.

### Why every hook reads `TestCenter.Enabled` in `Initialize` or at call time

`TestCenter.Enabled` is assigned in `TestCenter.Configure` at the default priority. Reading it from any other
default-priority `Configure` depends on the sort, which is the Part E defect itself. So the guard, the multiplier and
the command registration all run in `Initialize` (`Main.cs:448`, after every Configure and the world load), and the
kit and the fill read it at the moment they act. `SkillInfo.Table` has the same constraint (`SkillsInfo.cs:135`).

### Part B: log only, or refuse to start?

**Log only**, as the brief defaults. Reasons:

1. The live container has `restart: unless-stopped` (`docker/uo/docker-compose.yml`). A startup throw becomes a restart
   loop, which is a live outage caused by a config line, and the loop hides the one log line that explains it among
   repeated startup banners.
2. The only route to the Test Center on live is a hand edit of live's `modernuo.json`. The configs are separate bind
   mounts, and the seeding scripts copy live to test only when test's is missing, never the other way (section 1).
   A deliberate edit is better served by a loud message than by a shard that will not come up.
3. The port is a proxy for "this is live", not a proof. If the live port ever moves, a refusal would be silently
   wrong, which a log line is not.

The cost of this choice: a live shard with the Test Center on would really run it until someone reads the log. If
Chase would rather have the outage, the change is one line in `TestCenterLiveGuard.Initialize` (throw after the log).

### Part C: what else reads `GainFactor`

Nothing. Pinned has one reader, `SkillCheck.cs:119`, plus the setter's declaration (`Skills.cs:443`) and the constructor
that fills it (`Skills.cs:414`). Nothing in `server/customizations` reads or writes it (grep). The effect is on the
gain chance only, after which pinned floors it at 0.01 (`SkillCheck.cs:121-124`). Two things a reader should know:

- **It saturates.** At low skill the unscaled chance is already large, so 5x takes it past 1.0 and every eligible roll
  gains. The multiplier matters most in the upper range, where the chance is small.
- **It stacks with `ClusterFSkillGain`**, which both shards already run (section 1): up to 3 attempts per check, each
  success worth 5 gains. The multiplier raises the odds of each attempt's first gain. The 5x amount bonus
  (`ClusterFSkillGain.cs:126-138`) calls `SkillCheck.Gain` directly and is not scaled.

Read with `ServerConfiguration.GetSetting`, not `GetOrUpdateSetting`, so live's `modernuo.json` does not grow the key
on its next start and stays byte-identical. The cost is that the key is not self-documenting in a fresh config; it is
in the test config by hand.

### Part D: is `FillBankbox` safe to call twice?

The items: yes, a second call just adds a second set, which is what a refill is.

**The caps: no, not on this shard.** `FillBankAOS` *sets* (not raises) the caps of every skill in `PowerScroll.Skills`
(one of three era lists, `Items/Special/Special Scrolls/PowerScroll.cs:9-45`; I did not count the EJ one) to 120 and
`StatCap` to 250 (`TestCenter.cs:226-231`). Our `ClusterFSkillCaps`/`ClusterFStatCaps` hold every player at 300 and
1500 and re-apply only at login and world load. So `[TCFill` straight into pinned's fill would lower a playing
character's caps until they relog. At creation it is harmless: a new character starts below both, and the login
straight after creation re-applies ours: the create handler starts a `LoginTimer` (`IncomingAccountPackets.cs:175`),
whose tick calls `DoLogin` (`:517` -> `:267`), which raises `PlayerMobile.PlayerLoginEvent` (`:311`), where both ClusterF
cap handlers listen.

**Smallest safe route, taken:** `TestCenterKit.RefillBank` snapshots each skill's `CapFixedPoint` and `StatCap`, calls
pinned's `FillBankbox`, then puts back any cap it lowered. Neither setter clamps the skill or stat *value*
(`Skills.cs:205-219`, `Mobile.cs:1731-1743`), so nothing is lost in between. No patch. Creation keeps calling pinned's
`FillBankbox` unchanged.

The cooldown lives in memory, so a server restart clears it. On a test shard that is harmless.

### Part F: the registry

- **Convention:** entries register in `Configure`, the tree's place for filling a registry before the world loads
  (pinned `SkillsInfo.Configure` fills `SkillInfo.Table`, `SkillsInfo.cs:135`; `CommandSystem.Register` from
  `Configure` in `AccountHandler.cs:65` and ours `ClusterFSkillGain.cs:32`). Registering is inert; only placing is
  gated, and placing reads `TestCenter.Enabled` at the time, so the Configure order does not matter here.
- **Placement:** one `Bag` named "Shattered Legacy Test Kit", dropped in the bank. Stackables: one stack of the amount
  (capped at 60000). Non-stackables: one item per unit up to `MaxNonStackable` = 25, with a `logger.Warning` if an entry
  asks for more. A factory that throws or returns null is logged and skipped, because this runs inside character
  creation and must never break it. With zero entries nothing is placed.
- **Existing custom resources, all registered.** Counted from the files, 32 types:
  - `ClusterFExtendedOres.cs`: `PlatinumOre ToxicOre BlazeOre FrostOre ObsidianOre MythrilOre AdamantiumOre CelestialOre`
    (1000 each) and the eight matching `*Ingot` (5000 each);
  - `ClusterFExtendedLumber.cs`: `IronwoodLog GhostwoodLog EmberbarkLog FrostbarkLog ShadowbarkLog RunewoodLog
    VoidwoodLog StarwoodLog` (1000 each) and the eight matching `*Board` (5000 each).
  Found as every class in `server/customizations` deriving from `BaseOre|BaseIngot|BaseLog|Log|Board|BaseHides|
  BaseLeather|BaseReagent|BaseScales|BaseGranite|BaseClothMaterial`; only these two files hit. Their `CraftResource`
  values are ours (`ResourceInfo.cs` replacement adds tiers Platinum..Celestial and Ironwood..Starwood). The
  `Items/Resource/*` and `Items/Quest/*` `ICommodity` items are ServUO ports (OSI content), not our own, so they are
  **not** registered.

(Test runs and the deletion gates follow.)
