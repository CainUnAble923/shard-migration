# P570: F-12 gate tiles and mount levels

Design prepared October 24, 2026. Notes only. No code or world placement changed.

## Recommendation and decision boundary

Add a reusable level entrance tile, a visible gate using the same entrance rule,
and riding requirements on our reward mounts. Use the character's current F-12
level. Keep ordinary transportation available at level 1. A reset preserves the
mount and its ownership but can temporarily prevent riding it. A restricted area
checks every entering character, including arrivals through travel and login.

Chase approved adding both features to F-12 on October 22. He has not approved the
thresholds, mount scope, reset behavior, or placements below. Those are concrete
recommendations for review, not claims about decisions already made. This note is
ready to turn into bounded build prompts after the questions at the end are
resolved. The gates depend on real F-12 progression, which is still unbuilt.

This is native custom content. Borrow the ideas from Level System 3, not its
XmlSpawner storage, gate classes, equipment scoring, XP tokens, or point-buy
progression. Attunement and milestone procs remain the separate F-26 work Chase
approved. They should read the same player-level service when they are built.

## Evidence and current state

Paths prefixed `S/` are relative to the ShatteredLegacy work copy. `M/` means the
shard-migration work copy. `U/` means the read-only `D:/UO/ModernUO-pinned` tree.
The inspected shard HEAD is `1020e36a42d31dde07612544ea2a6f9472911db8`, also the
local main ref in `D:/ShatteredLegacy` when checked. Migration HEAD is
`9e4d3cc89f6e295f71218ae258d022f40e930d97`. Pinned ModernUO is
`d4531cd94b739613155225c234900de9f47d2c88`. These are local source observations,
not a claim about the deployed server or a remote branch.

- The requested `notes/cc-P405-servuo-batch-1022-research.md` does not exist. The
  completed P405 prompt names `M/notes/cc-P405-servuo-batch-1022.md` as its actual
  deliverable. Read that note, its Codex review, and the completed prompt at
  `D:/UO/cc-prompts/completed/cc-P405-servuo-batch-1022-research.md`.
- P405's level-system-3 section, lines 589-658, names Kamras' source and the
  relevant third-party files: `Level_3_Master/Items/LevelReqTile.cs`,
  `Items/LevelGate.cs`, `Core/LevelHandler.cs`, `XMLAttachments/XMLPlayerLevelAtt.cs`
  and `XMLAttachments/LevelEquipXMLDynamic.cs`. Its summary at lines 636-638
  records mount requirements and gate tiles as ideas. P405 does not establish
  their exact trigger, mount list, or threshold numbers. Those details are
  **unverified** here. Per this prompt, third-party behavior is taken only from
  P405's notes; no download was opened, executed, or treated as a drop-in port.
- `D:/UO/overseer/decisions-2026-10-22.md`, the 09:35 entry, explicitly records:
  "F-12: add level gate tiles and mount level requirements to its level-gates list."
  The same entry settles attunement and proc purchases separately. The earlier
  09:22 default-to-recommendations entry is superseded by Chase's later answers.
- Read F-12 in `M/docs/feature-queue.md`, P282's completion note, the revised
  `M/notes/f12-levels-loops-caps.md`, and P517's report
  `M/notes/cc-P517-f12-numbers-vs-code.md`. Use the later 50, 100, then +5 to 200
  ladder, not the historical 1,000-level examples in the queue.
- `S/server/customizations/Tutorial/ClusterFLoops.cs:25` stores a per-character
  loop count. `:31` returns cap 50 at loop 0, 100 at loop 1, and +5 through loop
  21/cap 200. The reset hook at `:40` is empty. Graduation recording is not a
  working player XP or reset system.
- `S/server/customizations/ClusterFCreatureLevels.cs:41,59,98` provides
  `IPlayerLevelSource` but defaults to best combat skill. Separately,
  `S/server/customizations/LootBoxes/ClusterFLootBoxes.cs:58` uses total Base skill
  divided by ten. Neither value is an acceptable access credential.
- `S/server/customizations/Mobiles/Mounts/RewardMounts.cs:59` contains the reward
  definitions listed in the mount table below. `:110` summons an owned, bonded,
  one-slot mount. The base class at `:200` supplies a place for our property text
  and double-click check without re-parenting any saved creature.
  `RewardMountStatuette.cs:39,45,58` supplies the tooltip and consumable call path.
- `S/server/customizations/Mobiles/Mounts/RideableDragons.cs:54,69` still defines
  staff-only placeholder dragons. `S/server/customizations/PackMule.cs:560` calls
  the stock mount click path except when its rider is opening the pack. Neither
  needs to join the reward requirement table.
- `U/Projects/UOContent/Items/Misc/Teleporter.cs:186,208,220,258` exposes virtual
  `CanTeleport`, `StartTeleport`, `DoTeleport`, and `OnMoveOver`. Its constructor
  uses item 0x1BC3, hidden by default. Its denied `OnMoveOver` returns true,
  allowing walking onto the tile, so a blocking threshold needs its own override.
- `U/Projects/UOContent/Items/Skill Items/Magical/Misc/Moongate.cs:87,113` moves pets
  before the player and does not itself call `SpellHelper.CheckTravel` on use.
  `Teleporter.cs:236` also moves pets first. A spell check alone is insufficient.
- `U/Projects/UOContent/Mobiles/Animals/Mounts/BaseMount.cs:77` has a nonvirtual
  Rider setter, which can mount directly. `:190` is the normal double-click path,
  and `:283` checks region, mount-block status and gargoyle restrictions. Keep
  those existing rules. Ethereal mounts have a separate implementation and are
  outside the proposed reward-mount scope.
- Existing guards are a useful pattern: `S/server/patches/PlayerMobile-tutorial-island-gate.patch`
  covers `MoveToWorld` and `SetLocation`; `SpellHelper-tutorial-island-gate.patch`
  preflights spells. They are applied at `S/docker/uo/apply-patches.sh:866`.
  `S/server/customizations/Regions/RootdeepVault.cs:63,78,246` demonstrates a child
  region, travel restriction, and login recovery. Extend alongside these rules,
  preserving tutorial graduation and parent-region behavior.

## One access rule

The F-12 foundation must expose a saved, per-character current level and readiness
state. Proposed API names below are design names, not existing methods:
`ClusterFProgression.TryGetCurrentLevel(pm, out level)` and a synchronous
`AfterProgressionChanged(pm)` integration call. The foundation owns initialization,
XP, reserve credit, resets, and saving. This feature owns no second level record.
Invoke the change integration after both the new loop flag and the final credited
level are committed in memory. ClusterFLoops currently calls its reset hook before
writing the loop flag; calling area validation from inside that unfinished hook
would read the previous loop. Validate recovery destinations before committing the
reset, then publish the final progression state and reconcile access synchronously.

An entrance passes when `currentLevel >= requiredLevel`, the required loop and
existing chapter/quest conditions pass, and ordinary travel rules also pass.
Use `ClusterFLoops.LoopOf` for an additional loop condition. A character's level
cap, best skill, account AP, League rank, title, party leader, mount owner, or
previous highest level cannot substitute for current level.

Missing progression data on an initialized F-12 server denies restricted entry or
restricted riding with "Your level record is not ready. Try again shortly."
Do not clamp a malformed saved value into an access credential. Level 1 transport
and unrestricted exits remain usable. Initialize missing records through the F-12
foundation before exposing the character to gameplay.

Recommended source settings are `clusterf.levelAccess.enabled = false` and
`clusterf.mountLevels.enabled = false` until F-12 is ready. Enabling either without
the real provider must fail configuration validation. Do not silently activate a
skill-based fallback. Both settings affect only their explicitly registered custom
content. While disabled, existing content behaves as before; these settings grant
no ownership, quest completion, or tutorial exemption.

Staff above Player may bypass the new level rules for inspection. They still use
the existing mount and travel validation. NPC riders do not receive a player-level
test. Player-controlled followers use their controlling player's area eligibility;
wild creatures retain the area's normal spawn and movement rules. Staff tests must
also run with an ordinary Player account.

## What players see at an entrance

Use one saved `ClusterFLevelGateTile : Teleporter`, with a second
`ClusterFLevelGate : ClusterFLevelGateTile` appearance for a standing blue gate.
Both read an immutable access definition by saved `AccessKey`. The floor tile is a
marked threshold; the standing form is an obvious doorway. Both are permanent,
immovable world items. They are placed by staff/content seeders, never crafted or
sold. No gold, Renown, AP, key item, or XP is consumed by crossing.

The item name is the destination, for example "Veteran Annex entrance". Its
property list says "Requires current level 75" and, when applicable, "Requires
loop 2". Clicking it reports the viewer's status: "Current level 49 / required
50. Reach level 50 to enter." A Setting gate also states its loop requirement.
Do not put a viewer-dependent current level into the shared cached property list.

Stepping onto the threshold or double-clicking within one tile invokes the same
attempt routine. Check same map, range, line of sight, alive status, enabled and
active state, destination safety, progression and content eligibility immediately
before moving anyone. Set Delay to zero and refuse nonzero delays on this type.
Its `DoTeleport` override repeats validation even when called directly. Refusal
leaves the character and followers where they were and plays no success effects.
A denied player's `OnMoveOver` returns false. An inactive gate is walkable and
does not teleport; the area's boundary rule still applies.

Use stock combat and criminal checks for these new entrances, both enabled by
default. Ghosts cannot enter encounters, but every exit and safe recovery route
works for ghosts. Initial placements are same-facet custom dungeon entrances,
outside housing and boat routes. No new PvP or cross-facet travel is introduced.

On success, move the player and the eligible followers that stock TeleportPets
would carry, with ordinary sound/effects. Do not pull distant or stabled pets,
other party members, or pets owned by another player. Mounted players retain
their mount if eligible. Party members cross individually. Throttle repeated
refusal messages to one per character/access key per two seconds; keep that timer
in memory only.

The return tile is a distinct unrestricted exit. Put its destination outside both
entrance trigger footprints so movement cannot bounce between gates. Show the
requirement before the entrance, not only after a failed step.

## Entrance numbers and placement contract

These are the current-level bands proposed by P282. P570 uses them rather than
inventing a competing access ladder. They remain proposals awaiting approval.

| Required current level | Custom content band |
| ---: | --- |
| 1 | Practice and outer band; all normal transportation and exits |
| 25 | Combat contract T1, shallow dive or first custom annex |
| 50 | Combat T2, standard dive and starter mini-champion access |
| 75 | Combat T3 and veteran annex |
| 100 | Combat T4 and elite annex |
| 125 / 150 / 175 | Combat T5 / T6 / T7 and matching deep annexes |
| 200 | Custom capstone, also loop 21 and epilogue conditions |

For The Setting, floor N requires loop `N + 1` and current level `95 + 5*N`, for
N from 1 through 20. Thus floor 1 is loop 2/current 100; floor 20 is loop
21/current 195. The epilogue remains current 200. Reserve-credited levels count
normally. No required scroll may have its only source beyond the gate it unlocks.

Do not gate public OSI dungeons, public moongates, New Haven tutorial trials, the
recruiter, guild halls, banks, stables, or basic gather/craft/delivery work. An
annex is an explicitly bounded custom area, not an entire existing dungeon.

Each content prompt supplies a manifest row with AccessKey, display name, current
level, optional loop, named content predicate, map, Rectangle3D bounds including Z,
parent region, entrance and landing coordinates, exit coordinates, and a safe
outside recovery point. The tile references this definition; it cannot claim a
lower requirement than the destination region. Reject overlapping definitions
unless an explicit strictest-rule composition is authored. Reject missing keys,
invalid levels outside 1..200, internal maps, zero/unresolved destinations, unsafe
landings, and a recovery point inside a restricted area. An unresolved definition
never becomes an unrestricted gate.

No live coordinates are authorized or invented here. The Setting and the proposed
F-12 annex placements are not supplied by the inspected code. The reusable feature
can be compiled and tested on a scratch map before those areas exist. A production
placement prompt is not ready until its manifest and map clearances are supplied
and checked. Existing source coordinates for the tutorial are not substitute
locations for a new level gate.

## Keeping the area rule effective

A tile is an entrance, not the security boundary. Register a child
`ClusterFLevelAccessRegion` over each manifest area. Preserve its actual parent
and delegate all unrelated rules. `OnMoveInto` checks the entering character or
follower's player master, including crossing from an easier custom band.
`CheckTravel` rejects RecallTo, GateTo and TeleportTo for an ineligible character;
Mark is refused inside these encounter areas for players. Allowed access never
overrides a parent's stricter travel rule.

Add narrow UOContent patch calls alongside the existing tutorial guards in
PlayerMobile.MoveToWorld and SetLocation. They ask the new destination policy,
including controlled return/recovery handling, before movement. Add a matching
SpellHelper.CheckTravel preflight so a refused spell does not spend resources on
an otherwise doomed move. Keep tutorial and level policy results conjunctive.

Also preflight the master's destination at the start of BaseCreature.TeleportPets
(`U/Projects/UOContent/Mobiles/BaseCreature.cs:4092`). If the master cannot enter,
return before any pet moves. This closes the pets-first behavior in existing
Moongate and Teleporter uses without replacing their full methods. The player's
movement guard separately refuses the move. This hook must compose both tutorial
and level restrictions; a tutorial refusal must not strand the pets either.
Registered areas exclude boat footprints, so this task adds no boat hook. A later
area touching navigable water must provide whole-boat preflight before release.

On login and after world/progression initialization, inspect the actual saved or
logout position and relocate an ineligible character to the manifest's safe point
before accepting gameplay. Do not merely refuse the attempted login placement
and leave the character on Map.Internal. On real level reduction/reset, perform
the same recovery synchronously, before further player actions. Permit lifecycle
internalization and departure to the safe point. Preserve corpse location, death
status, inventory, dive progress and companion ownership; bring nearby following
pets to safety. Recovery adds no rewards or resurrection and has a recursion
guard. If the configured point is blocked, use a validated nearby outside tile,
then the configured safe hub; never send someone to (0,0,0).

## What players see on mounts

Start with the existing RewardMount family only. Ordinary horses, ostards,
nightmares, ethereals, the Pack Mule, tamed OSI mounts, evo mounts and staff-only
dragon prototypes receive no new requirement. This keeps reset travel practical
and bounds the first change to our own cosmetic rewards. Do not infer a mount's
requirement from its body, color, combat difficulty, sale price, or tame skill.

Recommended requirements are below. The 18 definitions were enumerated from
`S/server/customizations/Mobiles/Mounts/RewardMounts.cs:61` through `:78`; these
keys are the complete counted artifact list. Numbers are proposed riding levels,
not values found in P405 or current code.

| Required current level | Exact RewardMounts keys |
| ---: | --- |
| 1 | chestnut-draft, bay-draft, grey-draft, palomino-draft, saddled-horse |
| 25 | barded-warhorse, gilded-charger, bonewalker-steed, war-wolf |
| 50 | marsh-raptor, dusk-raptor, sky-raptor, bog-strider, riding-bear, riding-wolf |
| 75 | riding-drake, emberhoof |
| 100 | moonlit-unicorn |

These are prestige bands, not stronger combat stats or speed upgrades. The current
reward family uses horse-like numbers and one control slot. AP, Renown prices,
achievement unlocks, drop rates, ownership, bonding and normal follower limits stay
independent conditions. All requirements are reachable by loop 1; no reward mount
depends on the long +5 cap ladder. Future mounts must get an explicit table row.

Add `RequiredCurrentLevel` to the definition record, not the creature's save data.
Display "Requires current level 75 to ride" on the mount and its statuette and in
the existing shop description. A level-1 mount says "Rideable from level 1".
Shop acquisition, achievement awards, trading and opening a loot box remain
available under their existing rules. A low-level owner may call, lead, stable,
shrink and unshrink the mount; a statuette still calls its mount rather than
mounting it. Only the act of riding is restricted. The requirement is always
checked against the rider, so transferring a mount cannot transfer eligibility.

Example refusal: "You need current level 75 to ride an emberhoof. Your current
level is 49." Add the check to RewardMount.OnDoubleClick and then call the stock
base method. Do not copy BaseMount's form, range, poison, trade, ownership, race or
region checks into our class.

Close direct assignment with a narrow BaseMount Rider setter patch: when assigning
a non-null PlayerMobile to a RewardMount, ask the same policy before dismounting
either the previous rider or the proposed rider's current mount. A denied switch
must leave both existing relationships intact. Null assignments always work. Skip
the level guard during World.Loading (`U/Projects/Server/World/World.cs:112`) so
reference restoration cannot discard a saved mount. Login validation runs after
progression is available. NPC and unlisted mount assignments follow stock behavior.
This patch does not make direct Rider assignment a replacement for ownership checks.

The F-12 reset confirmation should warn about any mount that will become unusable
at the resulting current level. Apply reserve XP first, then compare the final
level, then dismount only if needed. Perform dismount and any area recovery before
the reset action completes. Canceling a reset does neither. A dismounted reward
remains bonded, owned and following at the safe location; it is never deleted,
converted back to a statuette, or automatically remounted later. Revalidate an
already ridden reward at login and at a deliberate level-lowering staff operation.
Raising a level only makes the next normal mounting attempt eligible.

## Code locations, saves, art and client work

Proposed additive code belongs under `S/server/customizations/Progression/`:
`ClusterFLevelAccess.cs` for definitions, checks and recovery coordination,
`ClusterFLevelGateTile.cs` for both item appearances, and
`ClusterFLevelAccessRegion.cs` for region composition. Use ModernUO partial classes
and generated serialization for the new items; save AccessKey and ordinary item
state, not duplicate player eligibility. Regions are rebuilt from definitions at
startup. Keep gate types and their final parents fixed from their first release.

Mount changes extend the existing files in `Mobiles/Mounts/`. Source-defined mount
requirements need no saved field or ancestry change. Reuse the F-12 foundation's
saved progression format. Existing reward mount serials and statuettes continue
to load; old saves only acquire new restrictions when the feature is enabled.

Budget four targeted patch files: PlayerMobile-level-access.patch,
SpellHelper-level-access.patch, BaseCreature-level-access-pets.patch, and
BaseMount-reward-level-access.patch. Register them in apply-patches.sh after any
existing patches to those files. Verify the assembled source, not just a hunk
applying. All targets are UOContent; no Server core patch is proposed.

Alternatives considered before authorizing future patch work: a tile alone misses
travel and direct moves; region/spell checks alone miss direct MoveToWorld and
existing moongate use; checking only RewardMount's click misses direct Rider
assignment; copying stock transport or mount methods creates silent upstream
drift. The narrow calls above retain the stock logic and make drift fail the build.
The additive region still handles parent rules and follower walking. Before a
pinned-commit bump, recheck all four hooks and run their behavioral regressions.

Use existing item 0x1BC3 visibly for the floor marker, subject to a client preview,
and existing blue gate item 0xF6C for the standing appearance. These IDs come from
pinned Teleporter and Moongate constructors, not an unused-ID guess. If the floor
marker is visually unsuitable, choose an existing passable floor graphic during
the preview; do not change tiledata flags globally. Check the item's trigger Z
and foot clearance on the actual map before placement.

No new bitmap, animation, gump, hue, cliloc, tiledata record, packet, or client code
is required by this design. Mount bodies and items reuse RewardMounts.Defs. No art
request is needed because this proposal asks Chase to create no art. Existing
custom mounts still require their already established player-package assets.
Their presence in the deployed package and their appearance were not checked here.
Player text uses server strings and current property-list/gump facilities. A
client visual check remains necessary for marker visibility, click range, messages,
tooltips, riding and dismounting. No new console button is proposed.

## Tests and release acceptance

Implement under `S/server/tests/Progression/LevelAccessVerification.cs` and
`MountLevelVerification.cs`, using the existing Sequential UOContent test route.
Extend the existing RewardMountVerification fixtures so their owner has real
eligible progression when the feature is enabled. Keep their summon, bond, shrink,
stable and serializer assertions. Do not turn the gate off merely to hide a failure.

Every added test must first fail against the previous behavior. For a new API,
record an initial missing-API/compiler failure, then also demonstrate a behavioral
failure with the access guard bypassed once the harness compiles. Restore the guard
and get a passing run. Record exact red/green output in each implementation note.
Do not claim a source search or a client plan is a behavioral test.

| Test group | Required observations |
| --- | --- |
| Authority and boundaries | A saved current level of 49 fails 50; exactly 50 passes even when skill proxies disagree. Cap 200/current 1 still fails. An alt does not inherit eligibility. Missing/malformed records deny restricted access. |
| Tile and gate | Real movement and double-click call paths, denied OnMoveOver false, successful transport, repeated/direct DoTeleport validation, range/LOS/map/alive/active checks, no delayed use, messages throttled, exit always available. |
| Area bypasses | Walking around a tile, each spell destination type, existing Moongate.UseGate, existing Teleporter.DoTeleport, Location/SetLocation/MoveToWorld, login/logout positions and parent-region restrictions. Test actual movement and pet locations, not just helper return values. |
| Followers and party | Each party member is checked separately; a high-level leader cannot carry another player. Denial moves no follower. Eligible owner's stock-following pets cross, distant/stabled ones do not. Ineligible owner's controlled follower cannot walk into the area. |
| Reset and recovery | Cancel leaves position/rider intact; reset checks final reserve-credited level, dismounts only when required, relocates out of a locked band, preserves inventory/pet/dive state, and does not leave a player internalized. Blocked recovery uses a safe outside fallback. |
| Mount table | Enumerate the exact keys above; below/exact thresholds, rider rather than former owner, ordinary Player and staff, existing ownership/race/trade/poison checks, direct Rider assignment and denied switch preserving both riders. |
| Existing content | Stock horse and Pack Mule remain rideable at level 1, NPC mounts work, ethereals retain stock behavior, tutorial island exit restriction still holds, and public OSI destinations have no level gate. |
| Persistence | Gate AccessKey survives generated-serializer round trip; missing definition denies use. Existing reward mounts/statuettes survive save/reload; World.Loading restoration is followed by login validation. No duplication or deletion on dismount. |

Run the shard's `docker/uo/build.sh` gate with a unique scratch image tag for each
implementation prompt. No live-stack build, restart or deploy is authorized.
Integration/save/client checks use a throwaway loopback-only shard and scratch
saves. Every PowerShell script/test uses powershell.exe 5.1. A server build does
not prove the floor marker or mount animation looks correct. Chase's eventual
release decision includes an explicit review of the new restrictions on already
owned reward mounts. The Golem handles commits after completion, not the agent.

## Ordered Golem prompts

These are suggested prompt titles, not newly allocated P numbers. Run them in
order, except the two implementation branches may be scheduled independently
after their shared prerequisite. No parallel agent work is requested here.

1. **F-12 foundation: expose real level reads and progression-change integration.**
   **Touches:** server
   Fold this requirement into the actual F-12 progression build. Persist and
   initialize current level per character, expose readiness and validated reads,
   and provide post-reset/post-reserve/login integration. Wire the F-14 level
   source and loot-box placeholder to that same authority as appropriate to the
   F-12 build. Preserve graduation semantics. Implement the approved XP/reset
   foundation under its own scope; a fabricated level field or skill adapter does
   not satisfy this dependency. Test saving and the change notification first.

2. **F-12 custom area access and gate tile framework.**
   **Touches:** server
   Add the definitions, region, both item forms, destination guards, SpellHelper
   preflight, and pets preflight described above. Default disabled, no production
   placements. Use synthetic test rectangles and validate all routes, tutorial
   coexistence, exits and recovery. Add the three movement-related patches and
   their apply-patches registrations. Deliver red/green evidence and a clean build.

3. **F-12 reward mount riding levels.**
   **Touches:** server
   Add the complete proposed mount table, tooltip/shop text, RewardMount click
   check, Rider setter patch, reset warning and post-credit/login revalidation.
   Keep acquisition and follower handling as specified. Existing mount tests must
   run with both disabled compatibility and enabled real progression. Deliver
   red/green evidence, save round trips and a clean build. Do not gate evo or OSI
   mounts as incidental work.

4. **Place the first approved custom annex gates.**
   **Touches:** server, map
   Run only after the owning area's map and content exist. Name that area and
   supply its reviewed manifest coordinates, Z bounds, parent, safe landings,
   unrestricted exit, and reachable scroll sources in the prompt. Update its
   existing seeder idempotently; do not edit OSI entrances. Validate map clearance
   and preview both art forms in a scratch client. If no map edit is needed,
   narrow Touches to server when the actual prompt is written. The Setting's
   floor integration is a later instance of this step, after its own build.

5. **F-12 gate and mount player check in a scratch shard.**
   **Touches:** docs-only
   Record an ordinary player's below/at-threshold attempts, a two-player party,
   travel and login recovery, reset with and without reserve, basic horse travel,
   and existing reward-mount appearances. Capture the package version and exact
   build/config used. Write findings and unresolved defects in notes only.
   Execution must use an already authorized throwaway loopback instance; this
   prompt authorizes neither Haven access nor deployment. Fixes receive separate
   server prompts. Release activation remains Chase's decision.

The overseer can promote the agreed access list and custom-content decisions to
the governing queue/fidelity record. This task does not edit migration docs/.

## Work performed and verification limits

Read both work-copy AGENTS.md files, the governing-document index, direction
decision, task list and subsystem policy before writing this design. Inspected
canonical shard files, the read-only pinned APIs cited above, P405, its completed
prompt, Chase's overseer answers, P282 and P517. Used PowerShell 5.1 and git grep
because rg is unavailable. No generated server/uo tree was read. No third-party
code, web service, Haven connection, game client, server build, live configuration
or account operation was used. No code, test or configuration was changed.

Lane tests: none. No new test was added for this documentation-only task. The
test matrix above is required future work, not a passing-test report. Exact
third-party gate behavior, deployed settings/package contents, map placements,
client visuals, progression throughput and the proposed thresholds' play balance
remain unverified. No outside art write or approval request is needed.

Validation completed in Windows PowerShell 5.1.26100.9711. The code work copy is
clean; the migration work copy contains only this new notes file. No docs/ change,
trailing whitespace, or em dash was found. The file is below 5 MB. Enumerated the
18 RewardMounts definition keys directly and checked the published table against
that list. Required tools/progress.py --dry-run returned exit 0 with SL_SHARD and
SL_MIGRATE set to these work copies. Restored its incidental progress.json write
byte-for-byte, keeping this task notes-only. STOP-REQUESTED was absent at the
completion checkpoint. No commit, merge, push, branch switch, or deployment occurred.

## Questions for Chase

1. **Should these use current level after a reset?** Recommended: yes for custom
   encounter entry and the listed reward-mount riding requirements. Check the
   final level after reserve credit, dismount/return to safety only if needed,
   and preserve ownership and progress. Alternative: mount riding unlocks remain
   permanent once earned, while area entry still uses current level.
2. **Which mounts should the first version cover?** Recommended: the RewardMount
   family and the exact 1/25/50/75/100 table above. Keep the Pack Mule, OSI/evo
   mounts and ordinary horses available under existing rules. Alternative: a
   smaller named reward subset. Extending to all mounts needs its own reviewed
   list and exceptions rather than an implicit BaseMount-wide requirement.
3. **Approve the entrance bands and Setting formula?** Recommended: P282's
   25/50/75/100/125/150/175 custom bands; Setting floor N needs loop N+1 and
   current 95+5N. Keep ordinary exits and the first required-scroll sources
   reachable. These numbers should be approved together with the F-12 build.
4. **Which area gets the first real placement?** Recommended: the first built,
   explicitly custom level-25 annex with a safe public landing and unrestricted
   return, after its manifest/map review. Do not choose an existing OSI dungeon
   or the tutorial merely because it already has coordinates. The framework can
   be built and tested before an area is selected.
5. **Can players obtain and call a reward mount before they may ride it?**
   Recommended: yes. Show the riding requirement in the shop and on the statuette
   before use, allow normal leading/stabling/shrinking, and keep AP/Renown and
   achievement rewards intact. This avoids holding up a reward claim on a reset.
6. **What should happen to mounts already owned when this is enabled?**
   Recommended: apply the same table to everyone after a clear release notice;
   preserve the mount, and dismount an ineligible rider at login. No grandfathered
   riding flag. Enable only once real progression and safe reset/login recovery
   have passed the scratch-shard checks. Alternative: gate only new future mount
   designs, leaving today's reward family unrestricted.

P570 DONE
