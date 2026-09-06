# Backlog

**Work top-down. One item per Codex chat. Do not skip ahead.**

Each item states its own acceptance criteria. An item is done when that criterion is met and
the work is committed, not when the code looks right. Tick the box, run
`python tools/progress.py`, include the result in the same commit.

If an item turns out to be wrong or blocked, do not silently substitute another. Open a
question in `notes/codex-questions.md` and move to the next item.

---

## Foundation — blocks everything below

- [x] **F1. Commit the recovery work and prove the tree compiles.**
  `CraftContext.cs`, `OutridersGuildmaster.cs` and `ResourceInfo.cs` are recovered but
  uncommitted, and `server/patches/ResourceInfo.cs` is deleted in the working tree.
  *Done when:* a clean Docker build from pinned ModernUO `7c9215d97` plus only tracked
  canonical inputs succeeds, and it is committed. Set
  `server/customizations compiles standalone` to true in `tools/progress-state.json`.

- [ ] **F2. Make `apply-patches.sh` fail on a failed patch.**
  It converts failures to warnings and exits 0. Seven patches currently fail.
  *Done when:* a deliberately broken patch fails the build, and the real seven are listed
  with their errors in `notes/`.

- [ ] **F3. Triage the seven failing patches.**
  For each: is it still needed, or did ModernUO change so it is obsolete?
  *Done when:* each of the seven is fixed, or removed with a one-line reason recorded.
  Update `patches_triaged` and `patches_obsolete` in `progress-state.json`.

- [ ] **F4. Delete `server/customizations/migrations/`.**
  Holds PetMimic v0-v2 JSONs diverging from the canonical v0-v8 in `server/migrations/`.
  *Done when:* removed, build still green, `stale ... migrations removed` set true.

- [ ] **F5. Make `RegenRates` routing explicit.**
  It works by accident: both it and ModernUO's land in `Misc/`, so ours overwrites. The other
  six replacements are explicitly routed in `apply-patches.sh`.
  *Done when:* it is in the exclusion list with an explicit `cp` line, like the others.

---

## Port pipeline — do this before bulk porting

- [ ] **P1. One reference port, start to finish.**
  Take a single ServUO creature from `Mobiles/Normal` with no dependencies. Convert its
  serialization to ModernUO's `[SerializationGenerator]` form, land it in
  `server/customizations`, build, run.
  *Done when:* it builds, spawns in game, and the exact steps are written to
  `notes/port-recipe.md` in enough detail that the next twenty ports copy it.

- [ ] **P2. Time the second port.**
  Do a second creature using only the recipe from P1.
  *Done when:* it builds and `notes/port-recipe.md` is corrected wherever P1's write-up was
  wrong or incomplete. Note roughly how long it took; that number prices everything after.

---

## Content — the ongoing backlog

Ordered by measured dependency cost. Everything here is near-zero coupling to subsystems
ModernUO lacks. Do not start until Foundation and P1/P2 are done.

- [ ] **C1. Eodon creatures.** 52 files, 6,607 lines, 0% dependency. Dinosaurs and tribal
  mobs. The most visible part of the Valley and the cleanest large block in ServUO.
- [ ] **C2. Revamped Dungeons.** 150 candidate files. Despise, Shame, Wrong, Covetous Void
  Spawn, Blackthorn, Exodus. Best value on the list: places to go and things to fight.
- [ ] **C3. High Seas, cheap half.** Fishing, rare fish, crabs and lobsters, fish pies, sea
  creatures. 0% dependency. Skip anything touching `BaseGalleon` or cannons.
- [ ] **C4. Creatures and NPCs.** 360 candidate files, 0% dependency. Take a batch at a time.
- [ ] **C5. Decoration and housing.** Addons, Decorative, New Magincia. 0% dependency.
- [ ] **C6. Crafting and resources.** Items/Resource, BulkOrders. 0% dependency.
- [ ] **C7. Artifacts and equipment.** 473 candidate files, 1-2%. Selectively: the pieces that
  anchor a dungeon or quest, not the whole set.
- [ ] **C8. High Seas, naval half.** ~54 files. Not blocked, but means extending ModernUO's
  `BaseBoat`. Its own mini-project; treat as a proposal before starting.

**Porting rule:** port unchanged. See `fidelity-principle.md`. Deviating from OSI behaviour
is a documentation debt only we can pay.

---

## Deferred — needs a subsystem built first

Not scheduled. Each is a build, not a port. Pick one up deliberately or not at all.

- Myrmidex Invasion (45 files) — the Valley works without it
- Shadowguard (8 files) — separate dungeon, own decision
- Skill Masteries (45), Vice vs Virtue (55), City Loyalty (27), Exploring the Deep (70)

---

## Standing rules

- **Never set a Goal in Codex for this project.** One scoped task per chat. On 2026-09-06 a
  Goal produced seven commits rewriting live customization files in the wrong direction.
- Run `python tools/progress.py` at the end of every session and commit the result.
- `docs/` is Claude's, `notes/` is Codex's.
