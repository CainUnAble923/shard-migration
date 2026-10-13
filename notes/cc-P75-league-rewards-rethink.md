# cc-P75: League rewards rethink after keeping TazUO's assistants

Run 2026-10-12 by Claude Code (autopilot hand-off after P70). Notes only: no code, no patch notes, no version bump. The
brief's Part B target `docs\design\league-rewards-rethink.md` is this file, since agents never edit `docs\`.

**Where the facts come from.** Two research subagents in this session read:
- the shard's docs, notes, roadmap, design folder and customizations;
- the TazUO client at our shipped commit.
Each cited file:line, and every file:line below is theirs: I did not re-read the source myself in this run. I fetched
TazUO's own wiki pages myself (section A.2). Treat the citations as read once, by an agent.

Short names:
- **SM** = `D:\UO\shard-migration`.
- **SL** = `D:\ShatteredLegacy`.
- **C** = `SL\server\customizations`.
- **T** = `D:\UO\cc-p40-work\tazuo-3212623f\src\ClassicUO.Client` (the shipped commit). **GM** = `T\Game\Managers`.

---

## Part A: facts

### A.1 The auto loot reward and the League reward shop: planned versus built

**Built (code exists):**
- **Renown, a spendable account currency, and LifetimeRenown, which never drops:** `C\ClusterFAccountData.cs:34-40`,
  `GrantRenown` `:516`, `SpendRenown` `:529`, `RenownSource` `:537`. **`SpendRenown` has no callers**: nothing spends
  Renown yet (`:348` says so).
- **Achievement points (AP), a permanent score:** granted with each achievement (`C\ClusterFAchievements.cs:1125-1126`)
  and shown in the achievements gump (`:1852`).
- **League rank** follows LifetimeRenown (`C\ClusterFLeagueRanks.cs:261`, `:443`), so spending Renown never costs rank.
- The only reward shop gump in the code is Clean Up Britannia's
  (`C\Services\CleanUpBritannia\CleanUpBritanniaRewards.cs:297`), which F-13 names as its template
  (`SM\docs\feature-queue.md:1307`).

**Planned only (no code):**
- **F-13, the League reward shop and AP-gated titles** (`feature-queue.md:1284-1380`).
  - The rule is "AP unlocks, Renown buys" (`:1300`, `:1320`). The shop sits at the League Registrar (`:1323-1327`).
  - The starter list was approved and is "Ready to batch" (`:1375-1380`). AP opens a tier and Renown is the price:
    titles, a League tabard, cloak, banner and regalia, a hair deed, a blessed recall rune, a trophy statuette,
    pigment, and Loot Boxes Bronze, Silver and Gold (`:1335-1350`).
  - Its guardrails rule out item properties, power scrolls, artifacts, bless deeds, and skill or stat items (`:1352`).
- **F-33's Clockwork Scavenger, "the League auto-loot reward" (Option A, Chase 2026-10-05):** the League grants a
  construct that loots corpses into the owner's backpack, and the mule's Clockwork Load Harness III reroutes it to the
  mule (`feature-queue.md:2624-2627`). The Salvage Bin II handles loose ground items (`:2650`).
  - **Not built.** cc-P70 lists it as missing (`SM\notes\cc-P70-mule-modules.md:345`).
  - **A correction to cc-P70.** Its Load Harness tooltip says "the redirect hook is" built
    (`C\Mobiles\Mule\MuleModuleData.cs:71-72`). There is no dedicated Scavenger hook in the code. The nearest seam is
    `MuleSatchels.AutoUnload` (`C\Mobiles\Mule\MuleModules.cs:1032`), a satchel hook, not a Scavenger one. The tooltip
    should read "not built" (a one-line data fix for the next builder prompt).
  - The roadmap already warns against an AFK looting bot (`SL\roadmap.md:810-844`, ":844 Avoid making it an AFK looting
    bot"). It also plans a `[claim` command and loot routing (`:773-808`), all unbuilt.
- **F-40, achievement loot boxes** (`feature-queue.md:3168-3192`): earned, rolled at earn time, opened in guard zones or
  homes; six tiers. No LootBox class exists.
- **F-41, fanfare** (`:3194-3204`). Not built.
- **F-24's League work** pays Renown, XP and rank; its milestone bonuses add bank slots, BOD slots and job slots
  (`:1998-2001`). The bank-slot part leans on `ClusterFBankLimit`; the rest is not built.

### A.2 Our TazUO build and its assistants

**What we ship:** TazUO **v26.0909.63**, commit **`3212623f63436be1c0f4e3b308b202b29597c026`**
(`SM\notes\cc-P26-animated-runestone.md:43`; `SL\player-package\payload\app\Build-UoOverrides.ps1:56`).
- Source: `D:\UO\cc-p40-work\tazuo-3212623f`. `D:\UO\TazUO` is the installed client, not source.
- The package copies the binaries as they are (`SL\player-package\Build-PlayerPackage.ps1:78`). It ships no profile
  defaults: `Launch-Settings.ps1:38-85` writes only login and server keys, so every agent default is TazUO's own
  (`T\Configuration\Profile.cs`).

| Feature | What it does | Default |
|---|---|---|
| Autoloot (`GM\AutoLootManager.cs`) | moves matching items out of a corpse the client has opened | **off** (`Profile.cs:735`) |
| Auto-open corpses | opens corpses within range, which feeds Autoloot | **on**, range **2** (`Profile.cs:321-322`) |
| Scavenger (`GM\ScavengerManager.cs`) | picks up matching ground items as the player moves | **on** (`Profile.cs:818`), but its list starts empty, so in effect it does nothing until the player adds entries (unverified) |
| Autobuy, Autosell (`GM\BuySellAgent.cs`) | buys or sells configured items when a vendor list opens | **off** (`Profile.cs:849, 852`) |
| Auto Bandage (`GM\BandageManager.cs`) | bandages self, friends and pets below a threshold, within 3 tiles | **off** (`Profile.cs:222`; distance `AccountSettingsSave.cs:25`) |
| Self-heal (`GM\SelfHealManager.cs`) | casts heal and cure on yourself | **off** (`Profile.cs:240`) |
| Auto-skinning | skins an opened corpse with a knife from the pack | **off** (`Profile.cs:737`) |
| Organizer Agent (`GM\OrganizerAgent.cs`) | moves matching items between containers, on command only | each set starts disabled (`:140`) |
| Dress Agent (`GM\DressAgentManager.cs`) | equips or unequips a saved set, on command only | manual |
| Legion scripting (`T\LegionScripting\`) | IronPython: move items, use skills, pathfind, answer gumps, autoloot, log out, in endless loops | off until a script runs |

TazUO's wiki also lists **Nearby Loot**, **Treasure Maps & SOS** and an **SOS Locator**
(`https://github.com/PlayTazUO/TazUO/wiki`, sidebar). They were not read in source here; they bear on the mule's
Survey Saddle Roll (section B.6).

**Can the server switch them off or limit them? No.**
- **TazUO's wiki "Server Owners" page** (`https://github.com/PlayTazUO/TazUO/wiki/Server-Owners`, fetched 2026-10-12)
  documents only the global chat packet. It names no feature flag and no way to disable an assistant. A "Custom server
  gump controls" page does not appear among the wiki's listed pages; 35 pages are unlisted, so this is unverified.
- **The one server-sent off switch is TazUO's own enhanced packet 0xCE, `DisableFeatures`**
  (`T\Network\EnhancedPackets\EnhancedPacketHandler.cs:55-71`). The only feature it defines is `TreeToStumps`
  (`EnhancedPacketDisabledFeaturesEnum.cs:3-6`); unknown IDs are dropped, and the player can turn enhanced packets off.
- **The Razor feature negotiation (0xF0) is acknowledged and ignored** (`T\Network\...\KrriosClientSpecial.cs:67-78`).
  Razor's "disallow" flags do nothing to TazUO's own agents.
- **So the server's only levers are its own rules:** reach, range, weight, rate, looting rights. Chase's decision to
  keep the agents (2026-10-11) is therefore also the only practical option short of a forked client.

### A.3 Planned or built League rewards a TazUO agent makes pointless

- **The Clockwork Scavenger (auto-loot into the backpack, F-33 Option A).** Autoloot plus auto-open corpses does exactly
  this in the client, for free, with filters, for anyone. **Pointless as a reward.**
- **The mule's Clockwork Load Harness II "auto-sort into bags"** (cc-P70, not built). The Organizer Agent sorts by item
  type on command. **Mostly pointless**: drop it, or keep it only for sorting while the owner is away from the mule.
- **The Field Medic Pack II's "bandage the mule from 6 tiles"** (cc-P70, needs a patch). The Auto Bandage agent already
  bandages pets within 3 tiles automatically. The 3-to-6-tile range is the only difference. **Low value; do not patch
  for it.**
- **The Survey Saddle Roll II's quest arrow to a map or SOS** (cc-P70, built). TazUO lists "Treasure Maps & SOS" and an
  "SOS Locator" on its wiki. **Partly duplicated, unverified until read**. The mule's arrow still works for maps kept in
  the *mule's* pack, which a client tool can only point at if it can see that container.
- **Nothing in F-13's shop list is affected.** It sells titles, cosmetics, a rune and loot boxes, nothing an agent does.
- **The Trader's Ledger I-II (sell from the mule's pack) is not duplicated.** Autosell sells from the player's own pack
  at the vendor's sell list, and pinned refuses items whose root is not the seller (cc-P70 section 5).

### A.4 What the client agents cannot do (where server rewards stay valuable)

1. **Nothing while the player is offline, or while the client is closed.** Every manager returns unless in game
   (`GM\AutoLootManager.cs:453`, `GM\ScavengerManager.cs:303`); every action is a packet from the client
   (`T\Game\Managers\Structs\MoveRequest.cs:59-64`).
2. **Short reach.** Corpses open within 2 tiles by default (`T\Game\GameObjects\PlayerMobile.cs:376`), the Scavenger
   works within 3 (`GM\ScavengerManager.cs:289`), and the server enforces reach on every pickup in any case.
3. **No remote bank.** No agent sends anything to the bank; the Dress Agent refuses the bank layer
   (`GM\DressAgentManager.cs:42`); Legion's `API.Bank` works only if the bank is already open
   (`T\LegionScripting\LegionAPI.cs:370-380`).
4. **No weight change.** No agent knows weight; an overweight pickup is simply refused by the server.
5. **Only reachable, known containers.** A destination must be in the client's cache; buy and sell need a live vendor
   list (`GM\ScavengerManager.cs:339-355`; `GM\OrganizerAgent.cs:213-226`).
6. **Tools and the player's own skills.** No salvage agent exists; skinning needs a knife (`GM\AutoSkinningManager.cs:84-98`).
   A script can only do what the player could do by hand.
7. **One action at a time, throttled** (`GM\ObjectActionQueue.cs:19-47`; 1 s between Scavenger moves, `Profile.cs:638`).
8. **Nothing server-side:** no change to drop rolls, luck, bank capacity, looting rights, item conversion, or anything
   that persists outside the client's local profile.
9. **AFK while online is allowed and unlimited** (no idle check in any agent). AFK farming is allowed on the shard
   (Chase), so the rewards below must stay sane when the player is not watching.

---

## Part B: proposal

### B.1 In plain language

Our TazUO already loots corpses, picks up ground items, buys, sells, bandages, sorts and dresses, all inside the
player's client, all off by default but one click away, and the server cannot switch any of it off. A League reward
that does what the client already does is worth nothing. A server reward is worth something when it does what the
client cannot:
- work at a distance;
- reach the bank;
- change weight;
- convert items;
- act while the player is offline;
- touch luck, rolls and capacity.

The planned auto-loot Scavenger falls on the wrong side of that line. The rewards below sit on the right side. They
follow the League rule (**AP unlocks the tier, Renown pays the price**) and F-13's guardrails (no item power).

### B.2 Replacement rewards

Price tiers are relative to F-13's list, where the most expensive item is 1,000 Renown at 1,750 AP. Size is the rough
build size: S a day, M a few days, L a week or more.

| # | Reward | What it does | Why a client agent can't | AP / Renown | Tag | Size | Exploit risk and guard |
|---|---|---|---|---|---|---|---|
| 1 | **Loot Courier** (keep, sharpened) | Gold from your own kills goes straight to your bank; tier II also sends flagged commodities (ore, ingots, reagents, gems, hides) | No agent reaches the bank (A.4.3); the courier works at any range the kill happened | I 250 AP / 150; II 750 AP / 400 | ours | M | Bank flooding while AFK: obeys `ClusterFBankLimit` (overflow stays on the corpse). Only items you have looting rights to (`Corpse.CanLoot`, cc-P45's seam). No player corpses |
| 2 | **Featherweight satchels** (keep) | A League loot satchel line: monster loot (gold, reagents, gems, hides, bones) weighs less inside, -25% / -40% / -55%, hued on the ore ladder up to Celestial (tiers named for the metals) | Agents cannot change weight (A.4.4) | I 100 AP / 100; II 500 / 250; III 1,000 / 500; then Valorite and Celestial hues as AP badges at 1,750 | ours (the ore satchels' `GetTotal` pattern, `C\CompactOreSatchel.cs:92-101`) | S-M | Stacking with the mule's Ore Hopper: a satchel's contents are not discounted twice (cc-P70 already skips satchel contents). Cap the reduction at the ore satchel top (70%) |
| 3 | **Field Salvager** (keep, changed) | Items dropped into it are salvaged when you are near a forge (or your mule's Field Smelter Rig), with a League tier giving a little better yield. It reuses `SalvageBag.SalvageAll` (made internal by our patch) and `SmithGuildSalvageBag.IngotReturn`; it does not copy them | No salvage agent; agents need the tools and the forge themselves (A.4.6); the conversion is server-side | I 250 AP / 200; II 1,000 AP / 450 | ours | M | "On pickup" with no forge would let AFK scripts turn loot into ingots in a dungeon: keep the forge rule (Chase to decide if not). Yield bonus capped at +10% |
| 4 | **Corpse Claim** (keep the idea, changed from "corpse recall") | `[claim`, or a context entry: pull the contents you have looting rights to from your own kills within 12 tiles into your pack (or a satchel), on a 10-second cooldown. The roadmap's `[claim` (`SL\roadmap.md:773-808`) | Agents reach 2-3 tiles (A.4.2); the server can reach farther | 100 AP / 150 | ours | M | AFK mass looting is allowed, but limit it to your own kills and rights, never other players' corpses, never criminal acts (`Corpse.IsCriminalAction`). No recall of a corpse's body itself (it would move corpses through walls) |
| 5 | **Fortune Charm** (keep, small) | A consumable charm: the next F-40 loot box you earn rolls its quality one step better (never more items) | Box rolls are server-side (A.4.8); nothing in the client touches them | 500 AP / 300 each | ours | S, after F-40 | Stacking with the Fortune's Favor imbue (`SM\docs\artificers-imbuing-design.md:83`): take the better of the two, do not add |
| 6 | **League Warehouse** (new) | More bank room: +50 items and +200 stones per tier, on top of F-24's milestone slots | Bank capacity is server-only (A.4.8) | I 250 AP / 200; II 1,000 / 500; III 1,750 / 1,000 | ours (`ClusterFBankLimit`) | S | None of note; it pairs with the Loot Courier, which is the reason to cap the courier by bank space |
| 7 | **Overflow to the mule** (new; replaces the Scavenger's job on the mule) | When your pack is full or overweight, looted items you pick up go to your Compact Mule's pack instead, anywhere on the same map | Agents need the destination container in reach and in cache (A.4.5); the mule may be far off | 500 AP / 300 (needs a mule) | ours (`ClusterFBackpack.TryDropItem`, `C\ClusterFHuntersSatchelHooks.cs:5-27`, as the routing seam) | S-M | The mule becomes a remote bank: limit it to items picked up from corpses and the ground, not a manual "send" |
| 8 | **Expedition Ledger** (new, offline) | While you are offline, your active League jobs and guild work orders that need only bank materials are filled from your bank at the next save, paying their normal rewards | Nothing in the client runs while you are offline (A.4.1) | 750 AP / 400 | ours (F-24's job engine, not built) | L, after F-24 | A login-only alt farming jobs: count it toward the job's normal cooldown and caps |

**Rejected or merged:**
- **The Clockwork Scavenger as an auto-looter:** dropped (B.3).
- **"Corpse recall"** in the sense of moving the corpse: merged into Corpse Claim. Moving corpses has pathing and exploit
  problems (corpses through walls, out of guarded areas) for no gain over claiming the contents.
- **"Auto-salvage on pickup"** with no forge: changed into the Field Salvager, keeping the forge rule. The other way, AFK
  scripts would convert everything everywhere.

### B.3 The server auto-loot reward: proposed Dropped

**Proposed for Dropped: F-33's "Clockwork Scavenger is the League auto-loot reward" (Option A, 2026-10-05).**
- **Reason:** TazUO's Autoloot and auto-open corpses (A.2) do the same thing in the client, for every player, for free,
  with filters, and the server cannot turn them off. A server auto-looter would duplicate it at real cost (pathing, a
  tick, a mobile per player) for nothing, and it is the "AFK looting bot" the roadmap itself warns against
  (`SL\roadmap.md:844`).
- **What survives:** the mule's Load Harness III (redirect to the mule) becomes **Overflow to the mule** (B.2 #7), which
  needs no Scavenger.
- **The Scavenger name** could live on as a cosmetic construct companion if Chase wants the art.
- **Not edited here:** `docs\feature-queue.md` is unchanged; Chase passes the decision to the Feature Queue chat.

### B.4 Knock-on changes to cc-P70's modules (for the next builder prompt)

- Load Harness III: retarget to Overflow to the mule (B.2 #7), and fix its tooltip, which wrongly says a hook is built.
- Load Harness II: drop "auto-sort into bags" (the Organizer Agent does it), or keep it as sorting while away.
- Field Medic Pack II: drop the ranged-bandage patch plan (Auto Bandage covers pets within 3 tiles); keep self-cure.
- Survey Saddle Roll II: keep for maps in the mule's pack; read TazUO's "Treasure Maps & SOS" and "SOS Locator" source
  before investing more.

### B.5 Open questions for Chase

1. **Drop the Scavenger as an auto-looter?** (B.3) And keep the name for a cosmetic construct, or retire it?
2. **The Field Salvager's forge rule:** keep it (my recommendation, against AFK conversion) or allow salvaging anywhere at
   a lower yield?
3. **Corpse Claim's range and cooldown** (12 tiles, 10 seconds), and whether it should work on party members' kills.
4. **Loot Courier tier II's commodity list:** which items, and should it stop when the bank is full or spill into the mule?
5. **The Expedition Ledger:** wanted at all (offline progress is a big design step), and only after F-24's jobs exist?
6. **Prices:** the AP and Renown tiers above sit inside F-13's range (up to 1,750 AP and 1,000 Renown). Say if League
   utility should cost more than cosmetics.
7. **Should the server send TazUO's `DisableFeatures` for anything?** It can only disable tree stumps today, so no
   action is proposed. Recorded so nobody expects it to limit the agents.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code clean
docs dry run
```

One file pending in docs (this note), ASCII only. No code changed, and nothing was built.

P75 DONE
