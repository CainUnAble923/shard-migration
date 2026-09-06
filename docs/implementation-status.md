> **OBSOLETE as of 2026-09-06.** Written when the plan was to migrate the shard to ServUO.
> The shard stays on ModernUO; see `direction-decision.md`. Its source-tree facts and the
> SHA-512 comparison remain accurate; its ported-file table describes reverted work.

# Implementation status

Measured against source trees on 2026-09-06.

## Source trees

- ModernUO reference: `D:\UO\ModernUO-reference`, detached at pinned commit `7c9215d97`.
- ServUO pub57 reference: `D:\UO\ServUO-pub57`, kept pristine on `pub57`.
- ServUO scratch clone: `D:\UO\ServUO-work` (not a deliverable or fork).
- Canonical shard source: `D:\ShatteredLegacy\server\customizations`.
- Excluded entirely: `D:\ShatteredLegacy\server\uo`.

## Phase 0

- ModernUO/ServUO SHA-512 compatibility was re-verified in the pinned ModernUO and pub57
  source trees: both hash ASCII `username + password`, truncate the input to 256 characters,
  and use SHA-512. ModernUO emits contiguous hex; ServUO emits hyphenated hex.
- SHA2 startup enforcement is staged in the shard infrastructure working tree, but the
  canonical-only Docker image does not currently compile due to the baseline gaps recorded in
  `shard-inventory.md`.
- Live server configuration and deployment state are unverified.

## Phase 2 ports

| Canonical file | ServUO destination | Status | Verification |
|---|---|---|---|
| `CleanedDebris.cs` | `Scripts/Custom/ShatteredLegacy/Items/CleanedDebris.cs` in scratch clone | Ported, uncommitted | Source API/pattern checked; full build unverified because local Roslyn execution was denied |

No later script should be ported until the current script passes a full ServUO build, per the
repository working agreement.
