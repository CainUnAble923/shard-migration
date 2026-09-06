# F4 and F5 — the last two Foundation items

Date: 2026-09-06. Agent: Claude Code. Pinned ModernUO `7c9215d97`.

## F4 — delete `server/customizations/migrations/`

Removed. Three files, all tracked:

```
server/customizations/migrations/Server.Items.PetMimic.v0.json
server/customizations/migrations/Server.Items.PetMimic.v1.json
server/customizations/migrations/Server.Items.PetMimic.v2.json
```

`server/customizations` now has no subdirectories and no files below the top level.

### A correction to the stated reason

`AGENTS.md`, `backlog.md` and `tasks.md` all describe these as PetMimic JSONs that **diverge
from** the canonical v0-v8 set in `server/migrations/`, and call them save-corruption
material. Checked before deleting, and the divergence claim does not hold:

```
v0 semantically IDENTICAL
v1 semantically IDENTICAL
v2 semantically IDENTICAL
```

Parsed as JSON and compared, all three are **equal** to their canonical counterparts. The only
difference is whitespace: the canonical files put each property on one line, the copies
pretty-print each property across eight. A `diff` shows a wall of changes and none of them
mean anything.

**Deleting them is still right, but for a different reason.** The hazard is not that they
disagree with the canonical set. It is that they are a *truncated* set: v0-v2 where canonical
runs v0-v8. A second, partial copy of the migration files is worth nothing when it agrees and
is dangerous when it stops agreeing — and if a future change ever pointed the installer at
them, versions 3 through 8 would simply be absent.

So: no save corruption was ever waiting to happen from content drift, and the "diverging"
framing overstates what is on disk. The truncation is the real defect, and it is the one that
justifies removal. Recording this rather than repeating the docs, per the rule that source
evidence beats a stated rule. No doc was edited.

### The F2 interaction that made this urgent

Before F2, these were inert purely because the installer used `-maxdepth 1`. F2 added
subdirectory mirroring, which is exactly the "if the copy strategy ever changes" condition the
docs warn about — the copy strategy changed in this same session. They stayed out only because
the mirror installs `*.cs` only, and the runner named each skipped non-`.cs` file in the build
log. That was a deliberately narrow guard held until this deletion; it is now moot.

### Verification

Full `docker build --target builder`: succeeds, zero compiler errors. The `NOTE: not
installed` lines for the three JSONs are gone from the build log, because there is nothing
left to skip.

---

## F5 — make `RegenRates` routing explicit

`RegenRates.cs` is now excluded from the additive `find` by name and routed with an explicit
`replace_file`, like the other replacements. Exclusions go from six to seven, replacements
from six to seven.

### It really is a replacement

Both trees declare `public static class RegenRates` at line 10:

```
ours:            server/customizations/RegenRates.cs:10  public static class RegenRates
pinned upstream: Projects/UOContent/Misc/RegenRates.cs:10  public static class RegenRates
```

Same type, same namespace. If both reached the build it would be a duplicate-type error, so
ours has always had to overwrite upstream's — it just did so as a side effect of the additive
copy landing in `Misc/`, which is where upstream's file happens to live.

### Why "by accident" was worth fixing

The old arrangement produced the right file for the wrong reason, and the failure mode was
silent. If a future pin bump moved `RegenRates.cs` out of `Misc/`, the additive copy would
still drop ours into `Misc/` while upstream's file sat, unmodified, at its new path. Best case
a duplicate type stops the build; worst case upstream's stock regeneration rates win and
nobody notices, because nothing in the pipeline was ever asserting anything.

Made explicit, `replace_file` asserts the destination exists first. Simulating exactly that
move:

```
[patches] FAILED: RegenRates.cs — destination Projects/UOContent/Misc/RegenRates.cs does not exist in pinned upstream
[patches] ERROR: 1 item(s) did not apply. Failing the build.
>>> EXIT: 1
```

That is the whole value of the change: the same file lands, but a pin bump that moves it now
fails loudly instead of quietly reverting the shard to stock regeneration.

### Verification

- The installed `Projects/UOContent/Misc/RegenRates.cs` is byte identical to
  `server/customizations/RegenRates.cs`. Same outcome as before, now asserted.
- All 9 patches apply, runner exits 0.
- Full `docker build --target builder` succeeds, zero compiler errors.

## Foundation is 7/7

`python tools/progress.py` shows all seven setup defects resolved. What that now rests on, in
order: the runner fails on a failed patch (F2), every patch in `server/patches` applies (F3),
the tree compiles from pinned upstream plus only tracked canonical inputs (F1, verified as
part of F3), the stale migration copies are gone (F4), and every full-file replacement is
routed explicitly and asserted (F5).

**What is still not verified is runtime behaviour.** Foundation proves the build is honest,
not that the shard plays correctly. The five patches repaired in F3 compile and apply, but
none has been exercised in a client — see the "Not verified" section of `f3-patch-triage.md`.
That is CC1's first opportunity.
