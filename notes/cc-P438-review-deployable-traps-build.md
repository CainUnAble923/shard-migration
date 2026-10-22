# P438: review of P275 deployable traps

Reviewed 2026-10-22. Notes only; no code or tests changed, no build or gameplay tests run, and no connection to Haven.
The findings below come from reading the canonical source and pinned ModernUO at
`d4531cd94b739613155225c234900de9f47d2c88`, verified against the Dockerfile pin and a clean reference checkout.
Runtime reproduction and client behavior remain unverified.

Read P275's build note and P201's design. No separate P275 Codex review was found beside the build note;
the broader P379 merge review mentions the movement watcher but reports no trap finding.
P275's already recorded omissions, saved caltrops slow, and spotting-roll persistence are not repeated here.

## Findings

Paths beginning `server/` are in ShatteredLegacy. Paths beginning `Projects/` are in `D:/UO/ModernUO-pinned`.

1. **bug** | `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:145`: Spending a trap changes its deadline to two minutes without updating its scheduler registration, so a trap spent shortly after placement can remain in the original 30-minute bucket and keep occupying its owner's allowance (`Projects/Server/Items/Item.cs:340`, `Projects/Server/Items/DecayScheduler.cs:175`). Call `SetLastMoved()` after changing the charges and add a clock-driven test that processes the scheduler and observes deletion after the spent deadline.

2. **bug** | `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:514`: Rearming skips the area-cap check, so players can spend their traps, let other players fill the area's six armed slots, and then rearm the spent traps to exceed the cap. Check `ArmedNear` before restoring charges, including the payload-drop path, and test multiple owners rearming beside an already full area.

3. **bug** | `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:244`, `:344`: With trap PvP enabled and player combat allowed in Felucca, snare and shackle traps freeze players without calling `Harm`, so the owner gets no criminal action or aggression entry for the hold (`Projects/Server/Mobiles/Mobile.cs:8394`). Record the harmful act for each held victim before applying the effect, and test both hold-only traps against an innocent player rather than relying on the existing bear-trap PvP test.

4. **bug** | `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:255`, `:327`: Caltrops and bear traps call `BleedAttack.BeginBleed` directly, bypassing the immunity checks in `BleedAttack.OnHit`, so a bleed-immune creature such as a Crystal Elemental receives unresisted bleed ticks (`Projects/UOContent/Items/Weapons/Abilities/BleedAttack.cs:29`, `:61`, `:82`; `Projects/UOContent/Mobiles/Monsters/AOS/CrystalElemental.cs:49`). Apply the stock bleed-immunity and transformation checks before starting bleed, and test that an immune target still takes the permitted initial physical hit without acquiring bleed.

5. **risk** | `server/customizations/Items/Traps/Deployable/DeployableTraps.cs:289`: The optional Felucca PvP mode admits guildmates, party members, and the owner's pets whenever `CanBeHarmful` permits them, including as secondary blast, gas, or shackle targets, because only the owner has an explicit exclusion. This follows P201's broad target rule, so decide the intended friendly-fire policy before enabling it and add explicit friend/master exclusions and collateral-target tests if allies should be protected.

6. **risk** | `server/customizations/Items/Traps/Deployable/DeployableTraps.cs:388`: Placement accepts a `SafeZone` whose guards are disabled because the only region exclusions are active guards and houses, allowing players to consume kits inside a combat-free area (`Projects/UOContent/Engines/ConPVP/SafeZone.cs:13`). Reject safe zones explicitly and test a safe zone with guards disabled; the normal harmful-action handler already blocks combat there, so this is a placement and wasted-kit risk, not evidence of safe-zone damage (`Projects/UOContent/Misc/Notoriety.cs:162`).

7. **risk** | `server/tests/Items/Traps/DeployableTrapsVerification.cs:165`, `:341`, `:524`: The damage assertions only check that hits decreased, the decay assertions only read `DecayTime`, and placement tests cover an active guard zone and the owner's count, leaving resistance scaling, actual cleanup, safe-zone placement, rearm caps, and mixed friendly/hostile area victims uncovered. Add focused regressions for the findings above plus fixed damage rolls against known physical/fire resistances and area blasts beside an owner, player, pet, and summon, proving each new assertion can fail before recording a passing run.

## Checks with no additional finding

- No owner is accepted as a direct or secondary target: `DeployableTraps.IsTarget` excludes `m == owner` at line 281, and area victims pass that same filter at `DeployedTrap.cs:233`; the default monster-only mode also excludes players, controlled creatures, and summons.
- No direct physical/fire resistance bypass found: `DeployedTrap.cs:384` uses the normal `AOS.Damage` overload, which sets `ignoreArmor` to false and applies resistances (`Projects/UOContent/Misc/AOS.cs:34`, `:117`). Stock bleed intentionally deals direct damage; finding 4 concerns applying it to immune targets.
- No permanently abandoned deployable trap found on ordinary ground: `Decays` is explicitly true at `DeployedTrap.cs:114`, ground placement registers decay through `Item.MoveToWorld`, and deletion removes the trap from `Placed` at `DeployedTrap.cs:611`; finding 1 concerns late spent cleanup, not perpetual persistence.
- Active guarded towns and houses are rejected by `DeployableTraps.cs:388`. No additional finding in the practice lesson, Tinkering registrations, or Rootdeep floor-trap seeding and its test cleanup.

## Source coverage

Reviewed the P275 implementation files:

- `server/customizations/Items/Traps/Deployable/DeployableTraps.cs`
- `server/customizations/Items/Traps/Deployable/DeployableTrapKit.cs`
- `server/customizations/Items/Traps/Deployable/DeployedTrap.cs`
- `server/customizations/Items/Traps/Deployable/TrapLesson.cs`
- `server/customizations/Engines/Craft/TinkeringCraftRegistrations.cs`
- `server/customizations/ClusterFRootdeepSeeder.cs`

Reviewed `server/tests/Items/Traps/DeployableTrapsVerification.cs` and the P275 seeder/cleanup paths in
`server/tests/Regions/RootdeepVaultVerification.cs` and `server/tests/Regions/RootdeepWayInVerification.cs`.
Also checked the existing Remove Trap and Detect Hidden hook patches, the build assembly routing, and the pinned
harm, safe-zone, damage, bleed, and decay implementations cited above.

No tests were added, so no red/green test claim is made. The reported P275 build result was not rerun for this review.
Ran `tools/progress.py --dry-run` with both work-copy path overrides successfully; despite its flag, it rewrote
`tools/progress.json`, which was restored byte for byte from HEAD to keep this review notes only.
Final scope check: the code work copy is clean, and this note is the only added file in the notes work copy.

P438 DONE
