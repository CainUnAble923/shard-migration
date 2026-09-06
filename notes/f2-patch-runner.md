# F2 — apply-patches.sh made a real gate, and the seven failures

Date: 2026-09-06. Agent: Claude Code.
Subject: `D:\ShatteredLegacy\docker\uo\apply-patches.sh`, pinned ModernUO `7c9215d97`.

## Status before this change (verified, not assumed)

The commit titled "Normalize patch runner in Docker build" (`d877a8a`) changed three lines
of `docker/uo/Dockerfile` and did not touch `apply-patches.sh`. The runner still had:

```bash
if patch ... < "$file"; then
    echo "[patches] Applied: $name"
else
    echo "[patches] WARN: $name did not apply cleanly (may already be applied or conflict)"
fi
```

and an unconditional `echo "[patches] All patches applied successfully."` at the end.

Baseline run of the unmodified script against pinned upstream:

```
7 patches failed
final line: [patches] All patches applied successfully.
exit code: 0
```

The confirmation and the exit code were both false. Reproduction is under
"How this was measured".

## What changed

1. **A failed patch fails the build.** Failures are collected, every one is reported with
   its `patch` output, and the script exits 1 at the end. One build run diagnoses all of
   them instead of one per run.
2. **Dry-run before applying.** `patch --dry-run` decides; only a patch that will apply
   cleanly is applied for real. Previously a patch could apply some hunks and fail others,
   leaving a half-patched tree for every patch after it. A failing patch now touches nothing.
3. **Every `.patch` file must be accounted for.** A file in `/patches` that no `apply_patch`
   line names now fails the build unless it is listed in `SKIPPED_PATCHES` with a reason.
   This caught an existing case; see "The eighth patch" below.
4. **Full-file replacements assert their destination exists.** `replace_file` refuses to
   write to a path that is not already a file in pinned upstream. A plain `cp` to a path
   upstream had renamed would silently create an orphan that nothing compiles against, and
   the override would vanish with no error.
5. **The Lumberjacking `sed` is checked.** `sed -i` exits 0 when it matches nothing. The
   result is now asserted with `grep`.

Deliberately unchanged: the `find -maxdepth 1 -type f -name '*.cs'` selection and the six
by-name exclusions, both required by `AGENTS.md`.

## Acceptance tests

Run against the pinned tree. Variant A is the current script with the seven known-bad
patches moved into `SKIPPED_PATCHES` — what a green run will look like once F3 is done.

| # | Case | Expected | Result |
|---|---|---|---|
| A | Green case, no bad patches in the apply list | exit 0 | **exit 0**, `All 3 patches applied successfully.` |
| B | Variant A plus one deliberately broken patch (real target file, context matching nothing) | exit 1 | **exit 1**, `ERROR: 1 item(s) did not apply` |
| C | Variant A plus a stray `.patch` file no line references | exit 1 | **exit 1**, `present in /patches but never applied or skipped by name` |

A matters as much as B: it shows the gate discriminates rather than always failing.

Then the real thing, `docker build --target builder -f docker/uo/Dockerfile .`:

```
#14 ERROR: process "/bin/sh -c ... /apply-patches.sh" did not complete successfully: exit code: 1
 > [builder  9/11] RUN ... /apply-patches.sh:
0.636 [patches] ERROR: 7 item(s) did not apply. Failing the build.
ERROR: failed to build: failed to solve: ... exit code: 1
```

## The seven failing patches

Verbatim errors from the strict runner against pinned `7c9215d97`.

### 1. `Bandage-pet-mimic-targeting.patch`

```
can't find file to patch at input line 3
Perhaps you used the wrong -p or --strip option?
|--- a/Projects/UOContent/Items/Skill Items/Misc/Bandage.cs
No file to patch.  Skipping patch.
patch: **** malformed patch at line 10:
```

Two independent defects.

- **Space in the target path.** The file is `Items/Skill Items/Misc/Bandage.cs` and it does
  exist (verified with `ls` in the pinned tree). A unified diff separates the filename from
  the timestamp field with a **tab**; these headers have no tab, so `patch` reads the name as
  ending at the first space and looks for `Projects/UOContent/Items/Skill`.
- **Wrong hunk line counts.** `@@ -111,6 +111,12 @@` claims six old lines, but the body has
  ten lines of context before the additions. `patch` runs out of declared hunk at line 10,
  a blank line, and reports malformed.

### 2. `BaseWeapon-talisman-durability.patch`

```
checking file Projects/UOContent/Items/Weapons/BaseWeapon.cs
Hunk #1 FAILED at 1646.
1 out of 1 hunk FAILED
```

The only one of the seven whose diff is **well formed**. The hunk header is valid and the
file is found; the context at line 1646 no longer matches pinned upstream. This is genuine
content drift and the only one that needs re-basing rather than rewriting.

### 3. `BulkMaterialType-PostValorite.patch`

```
patch: **** Only garbage was found in the patch input.
```

Its single `@@` line is prose, not a hunk header:
`@@ BulkMaterialType enum — append post-Valorite metals after Barbed ...`. Zero well-formed
hunks, so `patch` finds nothing it can parse.

**Also superseded.** `server/patches/BulkMaterialType.cs` already contains the same enum
members (`Platinum = 12` at line 21 through `Celestial = 19` at line 28) and is copied over
`Engines/Bulk Orders/BulkMaterialType.cs` wholesale earlier in the same script. Redundant
even if repaired.

### 4. `CraftGump-MakeXClear.patch`

```
checking file Projects/UOContent/Engines/Craft/Core/CraftGump.cs
patch: **** malformed patch at line 14:
```

Header `@@ -431,6 +431,12 @@` is well formed but its counts are wrong; line 14 is a blank
line where `patch` still expects added lines.

**Not superseded — this behaviour is currently missing.** After a baseline run of the old
runner, `grep -n RepeatCount CraftGump.cs` in the built tree returns nothing. The Make X
repeat-clearing never reached the build.

### 5. `CraftGumpItem-MakeX.patch`

```
patch: **** Only garbage was found in the patch input.
```

Both `@@` lines are prose, and the body contains literal `...` ellipses standing in for
omitted code. This was never a diff; it is a design sketch saved with a `.patch` extension.
It cannot be repaired, only rewritten from the intended behaviour.

### 6. `CraftItem-HammerBODAutoFill.patch`

```
checking file Projects/UOContent/Engines/Craft/Core/CraftItem.cs
patch: **** malformed patch at line 14:
```

Same wrong-count defect as #4.

**Superseded.** `server/customizations/CraftItem.cs` line 1190 already contains
`HammerBODAutoFill.TryAutoFill(clusterHohPm, item);`, and that file replaces
`Engines/Craft/Core/CraftItem.cs` wholesale before the patch runs. Confirmed present in the
built tree after a baseline run.

### 7. `SmithBOD-PostValorite.patch`

```
patch: **** Only garbage was found in the patch input.
```

All three `@@` lines are prose. **Partly superseded, and this one needs care in F3:** it
targets two files.

- The `LargeSmithBOD.cs` half is superseded — `server/patches/LargeSmithBOD.cs` already has
  `m_PostValMaterialChances` (line 23) and `CreateRandomFor` (line 82), and replaces the file
  wholesale.
- The `SmallSmithBOD.cs` half is **not** superseded. There is no `SmallSmithBOD.cs`
  replacement in `server/patches/`, so the post-Valorite upgrade block in `CreateRandomFor`
  is absent from the build. Do not delete this patch as obsolete on the strength of the
  LargeSmithBOD half alone.

## Pattern

Six of the seven are **authoring defects, not drift**: hand- or model-written illustrative
diffs with prose hunk headers, wrong line counts, or ellipses, saved as `.patch` and never
round-tripped through `patch`. Only `BaseWeapon-talisman-durability.patch` is a real
context-drift failure. Whatever produced these did not test them, and the runner that
swallowed failures is why that went unnoticed.

If F3 repairs rather than deletes any of these, generate them with `git diff` against a
checkout of pinned `7c9215d97` rather than editing them by hand.

## The eighth patch — never invoked at all

`server/patches/` holds **eleven** `.patch` files. The old runner named only ten.
`AOS-pet-mimic-attribute-aggregation.patch` has no `apply_patch` line, and never has had one
in any revision of the script in git history (checked every commit touching the file: `1f5dd63`
and `44db37b`, zero references in both). It has never been applied and never warned about.

Its diff is well formed (`@@ -574,6 +574,14 @@`, one hunk), so it may well apply. I have
**not** applied it: making the runner strict should be behaviour-preserving, and switching on
a previously-inert patch would change what the shard does inside a change meant only to make
failures visible. It is in `SKIPPED_PATCHES` with a pointer to F3, and the new accounting
check means no future patch file can go unreferenced silently.

**F3 should decide it explicitly**, alongside the seven. It aggregates `PetMimic` attributes
in `AOS.cs`, so if it is genuinely wanted, pet mimic attribute bonuses are not being counted
today.

## Caveat on "currently missing"

Claims above about behaviour being absent describe **a clean build from pinned ModernUO plus
the tracked canonical inputs**. What the live shard is running was built at another time and
may differ. Nothing here was checked against the running server, and nothing was deployed.

## How this was measured

A diagnostic image pins the inputs so the runner can be exercised without re-cloning:

```dockerfile
FROM debian:12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git libicu-dev gcc patch
RUN git clone https://github.com/modernuo/ModernUO.git /build/modernuo \
    && cd /build/modernuo && git checkout 7c9215d97
COPY server/customizations/ /customizations/
COPY server/migrations/ /build/modernuo/Projects/UOContent/Migrations/
COPY server/patches/ /patches/
```

Identical to the real builder stage's inputs, stopping short of running the script. Then:

```bash
sed 's/\r$//' docker/uo/apply-patches.sh | docker run -i --rm sl-patchlab:7c9215d97 bash -s
```

Each run starts from the image, so the tree is clean every time.

## Contradictions found — recorded, not acted on

Per the loop rule, raised as questions in `codex-questions.md` rather than fixed here.

- `D:\ShatteredLegacy\AGENTS.md` still opens with "This shard is being migrated from ModernUO
  to ServUO", contradicting the settled direction in `docs/direction-decision.md`.
- The two `AGENTS.md` files give different line counts for the same 111 files: 37,581 in the
  shard repo, 37,748 in this one.
- `D:\ShatteredLegacy\docker\uo\entrypoint.sh` has an uncommitted change forcing
  `accountSecurity.encryptionAlgorithm=SHA2`, commented as keeping accounts "bridgeable to
  ServUO" — a leftover of the abandoned migration.

---

## Addendum — subdirectory mirroring (folded into F2)

Added after the above, on Chase's instruction and the answer to Q-002, while
`apply-patches.sh` was still open. Analysis in `docs/flat-namespace-problem.md`.

**Behaviour.** Top-level `.cs` is unchanged: additive into `Misc/`, `-maxdepth 1`, same six
by-name exclusions. Anything in a **subdirectory** of `server/customizations` is now mirrored
to `Projects/UOContent/<same relative path>` instead of being flattened. Purely additive.

**Safety rule.** A subdirectory file whose destination file already exists upstream fails the
build, with a message to route it as an explicit replacement. Parent directories are created
as needed.

I did **not** implement the "fail if the parent path does not exist" check the answer
suggested. It would reject every ported dungeon, since `Services/Revamped Dungeons/Shame/`
does not exist in ModernUO — that is the whole point of the change. Reasoning and an offer to
add it behind an allowlist are in the Q-002 note in `codex-questions.md`.

**Non-`.cs` files in subdirectories are not installed**, and the runner now prints a NOTE
naming each one rather than ignoring it silently.

### Tests, against pinned `7c9215d97`

| # | Case | Expected | Result |
|---|---|---|---|
| D | `Shame/Generate.cs` and `Wrong/Generate.cs`, same basename | both land at their own paths, contents distinct | **pass** — `// shame` and `// wrong`, each at its own path |
| E | `Misc/AOS.cs` in a subdirectory, colliding with upstream | exit 1, upstream untouched | **pass** — exit 1, `would overwrite existing upstream file`, upstream `AOS.cs` intact |
| F | Regression: top-level install old script vs new | identical | **pass** — `Misc/` listing byte identical, 160 entries, empty diff |

D is the case `flat-namespace-problem.md` describes: under the old flat install one of those
two would have silently overwritten the other.

### The F4 interaction, now more urgent

The only subdirectory in `server/customizations` today is `migrations/`, holding exactly the
stale PetMimic v0-v2 JSONs. `AGENTS.md` calls them "save-corruption material if the copy
strategy ever changes" — and the copy strategy just changed. They are excluded because the
mirror installs `*.cs` only, and each skipped file is now named in the build log. F4 removes
them outright and is next.

### Aside: the customization count is 114, not 111

`find server/customizations -maxdepth 1 -type f -name '*.cs'` returns **114**. Both `AGENTS.md`
files say 111. The difference is the three files F1 recovered: `CraftContext.cs`,
`ResourceInfo.cs`, `OutridersGuildmaster.cs`. Related to Q-006 on the line-count discrepancy;
neither doc was edited.
