# F3 — triage of the failing patches

Date: 2026-09-06. Agent: Claude Code.
Follows `notes/f2-patch-runner.md`, which found them. Pinned ModernUO `7c9215d97`.

## Result

Eight patches were broken, not seven. The eighth,
`AOS-pet-mimic-attribute-aggregation.patch`, had never been invoked by the runner, so F2
listed it separately and left it alone. Wired in during triage, it turned out to be malformed
in the same way as the rest — so it was never a working patch that someone forgot to call, it
was a broken patch that the missing call had hidden.

Five repaired, three removed. All nine remaining patches now apply cleanly and the tree
compiles.

| Patch | Verdict | Reason |
|---|---|---|
| `AOS-pet-mimic-attribute-aggregation.patch` | **repaired** | Needed. `PetMimic` attributes are otherwise never aggregated. Was malformed *and* never invoked. |
| `Bandage-pet-mimic-targeting.patch` | **repaired** | Needed. Without it `PetMimic.TryFeed` is unreachable — bandages just say "cannot be used on that". |
| `BaseWeapon-talisman-durability.patch` | **repaired** | Needed. The talisman layer is not one of the armour positions, so a `PetMimic` never loses durability. |
| `CraftGump-MakeXClear.patch` | **repaired** | Needed. A manual single craft must cancel an in-flight Make X repeat. |
| `CraftGumpItem-MakeX.patch` | **repaired** | Needed. The MAKE X button itself; nothing else reaches `CraftCountGump`. |
| `SmithBOD-PostValorite.patch` | **removed, split** | Replaced by `SmallSmithBOD-PostValorite.patch`. Its `LargeSmithBOD` half is dead; that file is replaced wholesale. |
| `BulkMaterialType-PostValorite.patch` | **removed** | Obsolete: `server/patches/BulkMaterialType.cs` already carries the post-Valorite enum and replaces the file wholesale. |
| `CraftItem-HammerBODAutoFill.patch` | **removed** | Obsolete: `server/customizations/CraftItem.cs` already carries the auto-fill call and replaces the file wholesale. |

**None of the eight was obsolete because ModernUO changed.** That was the question F3 asked,
and the answer is no in every case. Three were obsolete because *our own* full-file
replacements had absorbed their content, which is a different problem: the same customization
existed in two mechanisms at once and only the silent runner kept that from being obvious.

## Why they were broken

Detailed in `f2-patch-runner.md`. Summary: seven of the eight were never valid unified diffs.
Prose where a hunk header belongs, hunk line counts that do not match the body, literal `...`
ellipses standing in for real code. Only `BaseWeapon-talisman-durability.patch` was a
well-formed diff that had drifted out of context.

`Bandage-pet-mimic-targeting.patch` had a second, separate defect worth remembering: its
target path contains a space (`Items/Skill Items/Misc/Bandage.cs`) and the header had no tab
before the timestamp field, so `patch` read the filename as ending at the first space. Any
future patch touching a path with a space needs the tab. `git diff` does **not** emit one —
`diff -u` on two real files does.

## How the repairs were made

Not by hand-editing the patch files, which is what produced the mess. For each one:

1. Extract the file from a pinned `7c9215d97` checkout into an `a/` tree.
2. Copy to a `b/` tree and apply the intended change, with the edit anchored on an exact
   string that must appear exactly once — so a silently-missed edit fails loudly.
3. `diff -u a/<path> b/<path>` to produce the patch.
4. Run the strict runner from F2 against pinned upstream and require all nine to apply.
5. Full `docker build` to require it compiles.

The intent for each repair came from the old patch's `+` lines, which were readable even
where the diff framing was not. Content is unchanged from what was intended; only the diff
framing was rebuilt. `AOS.cs` additionally matched, line for line, the applied form still
present in the retained build tree at `server/uo/.../Misc/AOS.cs` — an independent check that
the reconstruction is what the shard actually ran.

Every referenced symbol was checked to exist before generating a patch: `PetMimic.TryFeed`
(`PetMimic.cs:1501`), `PetMimic.Attributes` (`:365`), `PetMimic.OnHit` (`:397`, and it does
implement `IWearableDurability`), `CraftCountGump`'s constructor (`CraftCountGump.cs:23`),
`CraftContext.RepeatCount/RepeatItem/RepeatTypeRes` (`:36`, `:38`, `:40`), and the non-generic
`Mobile.FindItemOnLayer(Layer)` the BaseWeapon change needs (`Mobile.cs:7429`).

`PetMimic.cs:376` carries the comment "BaseWeapon.AbsorbDamage calls OnHit on equipped
IWearableDurability items", which is exactly what
`BaseWeapon-talisman-durability.patch` makes true. The customization documented a dependency
on a patch that had not applied in some time.

## The one judgement call

`SmithBOD-PostValorite.patch` targeted two files, and only one half was dead. Deleting it
whole as "superseded" would have been wrong and is the trap F2 flagged. It is removed and
replaced by `SmallSmithBOD-PostValorite.patch` carrying only the live half: the
`m_PostValMaterialChances` table and the 30% post-Valorite upgrade in `CreateRandomFor`.

The name changed because the old one implied both files. If anyone is looking for the
LargeSmithBOD behaviour, it is in `server/patches/LargeSmithBOD.cs`, not in a patch.

## Verification

```
[patches] Applied: PlayerMobile-individual-stat-cap.patch
[patches] Applied: Healer-resurrection-policy.patch
[patches] Applied: HealerGuildmaster-resurrection.patch
[patches] Applied: AOS-pet-mimic-attribute-aggregation.patch
[patches] Applied: Bandage-pet-mimic-targeting.patch
[patches] Applied: BaseWeapon-talisman-durability.patch
[patches] Applied: CraftGump-MakeXClear.patch
[patches] Applied: CraftGumpItem-MakeX.patch
[patches] Applied: SmallSmithBOD-PostValorite.patch
[patches] Checking every patch file is accounted for...
[patches] Structural fixes...
[patches] All 9 patches applied successfully.
>>> EXIT: 0
```

Nothing is in `SKIPPED_PATCHES`; the accounting check requires every file in
`server/patches/` to be applied or explicitly skipped with a reason, and nothing is skipped.

Then the full builder stage, `dotnet publish ModernUO.slnx -c Release`: **succeeds**, zero
compiler errors.

## This also verifies F1

CC0 asks for F1 to be verified rather than trusted. The build above is that check: a clean
Docker build from pinned ModernUO `7c9215d97` plus only tracked canonical inputs, compiling
to `/modernuo/Distribution`. It succeeds, so `server/customizations compiles standalone` is
true — and now demonstrably so, since a patch failure can no longer pass silently.

Worth being precise about why the flag was previously wrong. It was not that the tree failed
to compile; it is that the evidence was worthless. The old runner exited 0 with seven failed
patches, so a green build proved only that the *unpatched* tree compiled. It is the F2 gate
that gives this build its meaning.

## Not verified

**Runtime behaviour of the five repaired patches has not been tested.** They compile and they
apply. Nobody has fed a PetMimic a bandage, hit one with a weapon to watch durability drop,
or clicked MAKE X. The MAKE X button positions (x=140, label at 175) are carried over from the
original patch and have not been looked at in a running client; they may overlap BACK at x=50
or MAKE NOW at x=270.

Per the boundaries, nothing was deployed and the live shard was not touched. Spawning and
clicking these is worth doing when CC1 next puts a client in front of the build.
