# P652: Town Houses, townsfolk, and resting player guide

October 26, 2026. Documentation only. Created [the player guide draft](wiki-drafts/town-houses-townsfolk.md). No code changed, and nothing was published or activated.

## Scope and source snapshot

The guide describes the merged stage-1 implementations from P631 and P634. It labels test leases, disabled conversations, and unimplemented rest separately. It does not turn the design's later-stage instructions into player instructions.

Code HEAD: `a3f017e279e29eed0ac12c506ef51e6310291583`. Notes HEAD before this task: `5f8d062986ce9db36253607c955f3d31dea9c70c`. Pinned engine sources were read from `D:/UO/ModernUO-pinned`, matching the Dockerfile's `d4531cd94b739613155225c234900de9f47d2c88` pin. Both work copies were clean when inspection began.

Read both work-copy `AGENTS.md` files first, then `docs/direction-decision.md`, `docs/tasks.md`, the governing-document index, and the question queue's standing answers. All writes stay in this work copy's `notes/`. No `server/uo/` source or live configuration was read.

## Sources read

Design, build, review, and earlier guide material, relative to this notes directory:

- [P409 Town Houses design](cc-P409-town-houses-design.md).
- [P542 design handoff](cc-P542-cont-fixup-town-houses-design.md).
- [P550 Town Houses design corrections](cc-P550-review-town-houses-design.md).
- [P566 townsfolk and rest design](cc-P566-design-townsfolk-features.md).
- [P631 townsfolk build](cc-P631-build-townsfolk-rest.md).
- [P634 Town Houses build](cc-P634-build-town-houses.md).
- [P643 townsfolk source review](cc-P643-review-build-townsfolk-rest.md).
- [P646 Town Houses source review](cc-P646-review-build-town-houses.md).
- [P560 earlier guide handoff](cc-P560-guide-town-houses.md) and [its planned-only page](wiki-drafts/town-houses.md). That page was left unchanged; P652 supplies the separately requested combined draft.

Canonical code evidence, relative to the code work copy:

| Source | Player-facing evidence |
|---|---|
| `server/customizations/Leaseholds/ClusterFLeaseSite.cs:89-160` | Single rectangle; sides 1-32; height difference 0-60; outside street spot; region, occupancy, and overlap checks. |
| `server/customizations/Leaseholds/ClusterFLeaseSite.cs:178-273` | Door registration; player/account checks; free staff assignment; ordinary `HouseSign`; door swaps and linked replacement pairs. |
| `server/customizations/Leaseholds/ClusterFLeaseSite.cs:277-321`, `:340-345` | Lease ending deletes the house and restores registered originals; the staff command is test-shard-only. No packing operation. |
| `server/customizations/Leaseholds/ClusterFLeasehold.cs:61-74`, `:96-133` | Width/depth storage calculation; inclusive height range; town-parented region; ageless; AOS capacity overrides; zero player vendor capacity. |
| `server/patches/BaseHouse-leasehold-region.patch` | Region factory and parent/3D-area constructor keep the house region owned by `BaseHouse`. |
| `server/customizations/Townsfolk/ClusterFTownsfolk.cs:35-112`, `:125-193` | Mara/Ellis identities; no teaching, loot, or accepted drops; double-click/Talk entry; seven named menu labels and response path. |
| `server/customizations/Townsfolk/ClusterFTownsfolkService.cs:35-60`, `:80-127` | Disabled default; default range 3; cooldowns 3/15; living participants, same map, visibility, LOS, NPC region; nearest matching resident. |
| `server/customizations/Townsfolk/ClusterFTownsfolkService.cs:135-229` | Read-only tutorial phase; regular/whisper speech; private NPC reply; per-player and per-NPC/topic cooldowns; shared speech/menu checks. |
| `server/customizations/Townsfolk/ClusterFTalkRules.cs:85`, `:495-561` | 160-character speech limit; exact normalized aliases, optional NPC name prefix, phase fallback. |
| `server/data/townsfolk-talk.json` | Actual aliases and directions; plaza/trades use New Haven; innkeeper profile is data only; no paid-rest invitation. |
| `server/tests/Townsfolk/TownsfolkTalkVerification.cs` | Read fixture and fact declarations alongside the build/review evidence. Existing tests cover the shipped table, matching, dispatch, cooldowns, read-only phase, menu, and identity; P643 records coverage limits. |
| `server/tests/Multis/LeaseholdVerification.cs` | Read existing facts covering region ancestry, footprint lookup, doors, refusals, and serializer round trips. They do not certify real-building client acceptance. |
| `docker/uo/Dockerfile:61-64`, `docker/uo/apply-patches.sh:831-835`, `CHANGELOG.md:35`, `:45` | Dialogue is copied into the build; housing patch is registered; both release notes describe staff/test-stage behavior. |

Read-only pinned ModernUO evidence, with paths relative to `Projects/UOContent/`:

| Source | Why it matters |
|---|---|
| `Multis/Houses/BaseHouse.cs:677-750`, `:1290-1299` | AOS secure storage is an item budget, not a container count. Usage includes secure contents, secure containers, lockdowns, and moving-crate contents. |
| `Multis/Houses/BaseHouse.cs:2157-2200`, `:2394-2489`, `:2537-2544` | Lockdown/release require co-owner; securing/unsecuring requires owner; lockdowns check both ceilings; secure storage checks and strongbox exception. |
| `Multis/Houses/BaseHouse.cs:3371-3455`, `:3541-3565`, `:3610` | House cleanup unlocks ordinary property and destroys strongboxes; account house entitlement; no deed by default. |
| `Multis/Houses/HouseSign.cs:105-175` | Ordinary sign opens the stock house menu rather than lease management. |
| `Regions/HouseRegion.cs:225-357` | Actual house speech phrases and permissions. |
| `Items/Construction/Doors/HouseDoors.cs:59-149` | House-door access uses house permissions and security levels under AOS. |
| `Gumps/Houses/ConfirmDemolishHouseGump.cs:99-131` | No positive price and no deed means ordinary player demolition refuses rather than ending the lease. |

Canonical filename and content searches were limited to customizations, patches, tests, dialogue, packaging, and release notes. The Townsfolk directory contains only `ClusterFTalkRules.cs`, `ClusterFTownsfolk.cs`, and `ClusterFTownsfolkService.cs`; Leaseholds contains `ClusterFLeaseSite.cs` and `ClusterFLeasehold.cs`. No innkeeper extension, inn-rest service/combat file, townsfolk seeder, rent implementation, or sublet implementation was found. These are source findings, not observations of a running world.

## Where design or shorthand differs from the merged code

1. **Availability:** P409 and P566 describe complete future systems. P634 supplies only staff test assignment, and P631 supplies only talk. No player rental, rent sweep, escrow, grace, eviction recovery, room rights, paid rest, or existing-innkeeper talk is present. The draft's opening and availability table carry this distinction.
2. **Town House boundaries:** P409 proposes several rectangles and a marker preview, with separate sign and ban spots. Current code uses one rectangle and one street spot for both sign and ban destination. Multi-rectangle buildings and preview remain P634 Draft B. The guide uses only the current dimensions and height limits.
3. **Storage terminology needs correction:** P634's phrase "8 lockdowns per floor tile, 1 secure per 16" is misleading under AOS. `SecuresFor` is integer `width * depth / 16` with a minimum of one, and `GetAosMaxSecures` returns it as the total item budget. Stock `CheckAosStorage` checks that budget for lockdowns and secure contents. Thus a 7 by 7 site reports 392 lockdowns but only 3 storage items, with ordinary lockdowns constrained by both limits. Additional stories do not increase area. This is our provisional implementation's behavior to revisit before release, not an upstream defect or a balanced capacity recommendation. No runtime capacity test was run for P652, and the guide does not certify every storage mutation path against that ceiling.
4. **Belongings protection is future work:** The adopted design protects registered property during termination. Current `EndLease` directly deletes the house. P634 explicitly discloses this; stock cleanup confirms loose lockdowns/secures and destroyed strongboxes. The guide tells test tenants to empty the house before staff end it and promises no crate or refund.
5. **Stock controls remain:** P409's future lease menu removes transfer and demolition. Current assignment creates a stock house sign. Transfer remains exposed, as P634 records; player demolition is refused because the price is zero and no deed exists. The guide distinguishes those controls from lease cancellation.
6. **Assignment eligibility:** P409 proposes excluding Young players and limiting launch facets. Current assignment checks a valid player and existing account house, with the normal staff exemption; it adds neither a Young/account-age requirement nor a Trammel-only restriction. No such new player restriction appears in the guide. Site placement is not proof that a building belongs on the eventual approved list.
7. **Placement and stationarity:** P566's Mara/Ellis coordinates are unverified candidates; P631 supplies no seeder. The guide publishes no arrival coordinates. Although their constructors set `CantWalk`, P643 traces an inherited named-move speech path that can relocate them. The draft does not promise they are immovable. No fix was found in this snapshot.
8. **Conversation region rules:** The shipped data uses New Haven, but the implemented check is NPC region ancestry by name, same map, range, and sight. It does not separately require Trammel or require the player to stand within the same region. The guide does not add either requirement. P643's region-key validation, reserved-command, and extra-topic-label findings remain review concerns; the guide uses only the shipped plain labels and aliases.
9. **Directions:** P566's sample says the League office is south. The shipped plaza help response says southwest, consistent with P631's anchor comparison. The guide follows the shipped text; no map walk was done here.
10. **Rest numbers are plans:** P631 records Chase's chosen 25 backpack gold, 120 seconds without harm, and 60-second reuse. Its stage-2 draft describes implementation still owed. These appear only in the guide's explicitly planned rest section, with no payment instructions or claim that speech, a Rest cliloc, or the innkeeper menu already works.
11. **Guard and door guarantees need acceptance:** The parented region and door restore paths exist, but P634 did not run a client acceptance pass. P646 records fixture protection, unsafe ban destinations, multi-overlap detection, and partially registered linked doors as source findings. Missing-parent recovery is only a staff warning today. The guide conditions guard coverage on the correct town region and does not present this as release-ready housing.

## Verification and limits

No lane tests apply. No new test or persistent validation gate was added, so there is no red/green test claim for this prose change. P631/P634's reported gated builds were read as historical evidence, not rerun. No Docker command, shard start, client session, world placement, full save/restart, account operation, Haven connection, deployment, or publication occurred.

Unverified: live switch values and NPC/site presence, final public building selection or prices, actual client rendering/journal delivery, end-to-end guard/door behavior, full-world restart ordering, and all later-stage payments and recovery. P643's packet/menu coverage concerns and P646's housing findings have not been fixed or independently reproduced by this task.

Used Windows PowerShell 5.1.26100.9711 for inspection and final checks. Both new files passed strict UTF-8 decoding, the under-5-MB check, no-em-dash/replacement-character/trailing-whitespace checks, and local Markdown link resolution. Both repositories passed `git diff --check`; new-file whitespace was checked directly because the files are untracked until the Golem commits.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointed at these work copies: exit 0. Its incidental write to `tools/progress.json` was restored from captured bytes in a `finally` block, and the before/after SHA-256 hashes matched. No generated report changes are retained or used as feature evidence.

Final scope: the code work copy is clean; the notes work copy has only the two requested new Markdown files. No `docs/` file changed. No commit, merge, push, or branch switch occurred. Stop-request checks between steps found no request.

P652 DONE
