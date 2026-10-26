# P640: review of P628 guard patrols pilot and P635 fix-up

Reviewed October 26, 2026. Code HEAD: `a3f017e279e29eed0ac12c506ef51e6310291583`.
Notes HEAD before this review: `67fb1629af64fed87e9997fd7fc354db47c5bab9`.

P628 delivered stage 1, the observe-only witness contract, rather than a working
patrol town. That matches the first stage in P608 and the scope stated in P628's
handoff. Physical guards, dispatch, routes, New Haven qualification, and Persuasion
remain later stages. Their absence is not a new finding against this stage.

There are three new findings below: two medium and one low. These are defects in
the recorder and its evidence contract. It still delegates enforcement to stock
guards, so this review does not claim a new player-facing punishment exploit.

## Sources and earlier reviews

Read both work copies' `AGENTS.md`, the direction decision, task list, and these
notes in the migration work copy:

- `notes/cc-P608-guards-patrol-design.md` and its Codex review.
- `notes/cc-P628-build-guard-patrols-pilot.md` and its Codex review.
- `notes/cc-P635-cont-fixup-build-guard-patrols-pilot.md` and its Codex review.

Compared the design and P628's recorded Chase direction: option C, physical guards
in one test town first, New Haven qualified separately, and no Persuasion erasure
of crime. The design's unanswered balance proposals were not treated as approved
requirements.

Code files reviewed:

- `server/customizations/ClusterFGuardWitness.cs`
- `server/patches/GuardedRegion-witness-observe.patch`
- `server/tests/Regions/GuardWitnessVerification.cs`
- The P627/P628 registration blocks in `docker/uo/apply-patches.sh`
- The corresponding `CHANGELOG.md` section and version handling in P635's handoff

Upstream citations below use `U/` for
`D:/UO/ModernUO-pinned/Projects/UOContent/` and `S/` for
`D:/UO/ModernUO-pinned/Projects/Server/`. That read-only tree is clean at
`d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`.
Also searched the shard's patches for changes to the cited callback paths.

Excluded the existing reviews' findings about test-shard activation enforcement,
merging unrelated offenses within one second, and failure to check the action's
location. P635's review repeats the latter two. They are not counted again here.

## New findings

### 1. Medium (P2): owner callbacks manufacture witnesses away from a pet's crime

**Location:** `server/customizations/ClusterFGuardWitness.cs:366`, with incident
construction at `:244` and witness collection at `:273`.

**What happens:** A controlled or summoned creature's criminal action is not just
one callback for the creature. `U/Mobiles/BaseCreature.cs:2897-2904` first calls its
base criminal action, then calls `master.CriminalAction(false)` for a player
master. `S/Mobiles/Mobile.cs:4535-4537` consequently enters the master's own region
with the master as the mobile. The new hook treats that propagated legal flag as
a separate physical crime by the master and scans for witnesses around the
master's current position.

For example, place a pet and its victim on one Cove street and its visible master
on another street more than 14 tiles away. A bystander beside the master, unable
to see the pet's offense, is added to a new incident against the master. That
bystander can report this incident. Conversely, the pet's actual witnesses get
an incident containing only the pet, with no responsible-master field or link.
The same ownership issue applies to summons. The further owner forwarding in
`U/Mobiles/BaseCreature.cs:2907-2940` is another reason to test the whole harmful
action rather than manually invoking only a region callback.

P608's law section (`notes/cc-P608-guards-patrol-design.md:46`) requires attribution
to the acting creature and its responsible master while keeping sight evidence
about the actual act. A legal flag forwarded to an owner does not establish that
nearby people saw an offense. This differs from the previously reported
action-location bug: even a correct victim-location check on aggression leaves
this separate, victimless owner `CriminalAction` callback intact.

**Fix:** Carry the originating act and acting creature through ownership
attribution. Snapshot the responsible master on that incident without treating
the master's forwarded criminal flag as a second witnessed act. Keep visibility
and last-seen evidence separate for the creature and master; never infer the
master's position from seeing the pet. Preserve stock legal consequences.

**Missing test:** Through a real pet/summon harmful action, use separate witnesses
beside the actor and beside the distant owner. Assert that only witnesses to the
act receive report authority, the responsible owner is captured, and no owner
location is disclosed to witnesses who never saw the owner. The existing crime
fact at `server/tests/Regions/GuardWitnessVerification.cs:174` uses player
`CriminalAction` and `AggressiveAction` calls and does not exercise ownership.

### 2. Medium (P2): incidents rejected by stock guard eligibility remain reportable

**Location:** `server/patches/GuardedRegion-witness-observe.patch:31` and
`server/customizations/ClusterFGuardWitness.cs:224`, with report selection at `:329`.

**What happens:** The observe hooks run before `CheckGuardCandidate`. That stock
method first calls `IsGuardCandidate` (`U/Regions/GuardedRegion.cs:236-241`), which
rejects guards, dead mobiles, staff, blessed mobiles, and invulnerable creatures
at `:337-344`. The recorder checks only enabled state, deletion, map, and pilot
jurisdiction. Its incident has no legal-eligibility field, and report selection
checks only witness membership and age.

For a concrete callback trace, a visible blessed player in Cove can execute a
criminal action. `Mobile.CriminalAction` sets the flag and invokes the region.
The recorder creates a witnessed incident; stock `CheckGuardCandidate` then
rejects the player because they are blessed. A nearby player who saw them can
nevertheless submit that incident as a suspect-bearing guard report. The same
mismatch exists for the other stock exclusions. This is about eligibility at
the event, not whether a later attack needs to revalidate changing law.

P608 specifies existing guard-eligible offenses (`:44`) and legal eligibility in
the incident record (`:76`). Currently a report does not mean that its incident
ever qualified for guards. Future dispatch cannot safely treat these records as
the requested contract without rebuilding this missing distinction.

**Fix:** Capture eligibility using the stock law and exclusions at the correct
point in the real action. Either omit rejected incidents or mark them explicitly
as diagnostics that cannot become suspect reports. Retain the separate future
requirement to recheck lawful attack permission before enforcement.

**Missing test:** Through the patched criminal-action entry point, compare a
normal eligible player with a blessed player and an invulnerable creature. The
rejected actors must not produce reportable suspect evidence. Cover the assist
hook as well; none of the current four facts invokes `DoBeneficial`.

### 3. Low (P3): caller history retains every caller for the process lifetime

**Location:** `server/customizations/ClusterFGuardWitness.cs:130` and `:324`.

**What happens:** Each living player who calls in the enabled pilot becomes a
strong key in `_lastCall`. There is no eviction after the two-second limit, on
logout, or after deletion. Incident and report lists have caps, but this separate
dictionary does not. Its only clear is `ResetForTests` at `:144`, which gameplay
never calls; switching observation off at `:391` does not release it. A long
observation session therefore keeps accumulating caller mobiles even after their
reports have been evicted. Repeated calls by one mobile overwrite its entry, so
the growth is by distinct caller, not by utterance.

**Fix:** Prune expired/deleted caller entries with bounded work, or use a bounded
cooldown mechanism whose records expire. Keep the two-second report limit.

**Missing test:** Advance beyond the cooldown after calls from distinct mobiles,
including one deleted caller, run cleanup, and verify old entries are released
while a fresh caller is still rate-limited. The current speech fact checks the
cooldown's behavior but not retained caller state.

## Fix-up, persistence, and verification limits

P635 did not change the witness implementation. Git blob IDs match P628 commit
`dff2f5c` and the reviewed HEAD for all three implementation files listed above:
the customization, observation patch, and verification file. The P627 and P628
registration blocks both remain in `apply-patches.sh:847-867`; the shared
`2026.10.25.14` changelog section retains both Staff entries. No new merge defect
was found there.

No save/load defect was identified within this stage. `Enabled`, incidents,
reports, and cooldowns are transient static state, and P628 explicitly says a
restart disables observation. There are no owned patrol mobiles, posts, routes,
or saved active assignments in this implementation. Their persistence and reboot
tests belong to the later stages; saving old culprit references would conflict
with the design's instruction to discard transient pursuits on restart.

This was a source review. Callback outcomes above were traced through the source,
not reproduced in a running shard. No new tests were written, no tests or builds
were run, and the earlier notes' red/green and build results were not independently
rerun. Real Cove geometry, floors, live guard populations, runtime configuration,
and performance remain unverified. The existing four facts were read in
`server/tests/Regions/GuardWitnessVerification.cs`.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` set to these
work copies; it completed successfully. Despite the option's documented behavior,
`build()` writes `tools/progress.json` before the dry-run return. Restored that
incidental snapshot change byte for byte from HEAD to keep this review notes-only.
No code or `docs/` files changed. No container, client, deployment, Haven
connection, save/account operation, commit, merge, push, or branch switch was
performed.

P640 DONE
