# P653: player guide draft for the guard patrols pilot

Written October 26, 2026. Documentation only. Created [wiki-drafts/guard-patrols.md](wiki-drafts/guard-patrols.md) from the merged implementation, with P608 used for intent rather than as evidence of available features.

Code work-copy HEAD: `a3f017e279e29eed0ac12c506ef51e6310291583`.
Notes work-copy HEAD before this task: `5f8d062986ce9db36253607c955f3d31dea9c70c`.
Read-only ModernUO HEAD: `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`.

## Result and scope

The guide leads with the important limit: P628/P635 delivered an off-by-default, observe-only witness recorder in Cove on Trammel. Stock enforcement still runs. There is no physical patrol pilot to teach players to evade or summon yet. The guide explains ordinary guard calls, how players participate in a staff-supervised observation test, the recorder's numbers, what those numbers do not change, and unfinished features. It makes no live-release claim.

No code, tests, configuration, services, `docs/`, or other guide files were changed. No player-facing staff activation instructions or hidden achievement criteria were added to the guide. No art is needed.

## Sources read

Read `AGENTS.md` in both supplied work copies, then the notes repo's `docs/README.md`, `docs/direction-decision.md`, and `docs/tasks.md`. Paths below refer to the supplied work copies. `U/` means `D:/UO/ModernUO-pinned/Projects/UOContent/`; `S/` means that tree's `Projects/Server/`.

Build, design, and review material:

- `notes/cc-P608-guards-patrol-design.md` and its Codex review: proposed patrol law, placement, witness contract, pursuit, combat, New Haven safety, Persuasion, budgets, and staged rollout.
- `notes/cc-P628-build-guard-patrols-pilot.md` and its Codex review: stage-one scope, reported failing-first facts/build, and remaining stage drafts. Later-stage prompt drafts are future work, not completed features.
- `notes/cc-P635-cont-fixup-build-guard-patrols-pilot.md` and its Codex review: integration preserved P628's implementation; no new patrol behavior.
- `notes/cc-P640-review-build-guard-patrols-pilot.md` and its Codex review: further evidence-contract and retention defects; source-review verification limits.
- `notes/wiki-drafts/league-warrants-echo.md`: existing draft format for distinguishing disabled foundations from unfinished player access.

Implementation and supporting source:

| Source | What was checked |
| --- | --- |
| `server/customizations/ClusterFGuardWitness.cs:43-106` | Witness/incident/report fields and jurisdiction matching through region parents on one facet. |
| `server/customizations/ClusterFGuardWitness.cs:110-146` | Sight 14, normal/yell/whisper hearing 15/18/1, report age 15 seconds, merge window 1 second, caller cooldown 2 seconds; Cove/Trammel manifest; transient state. |
| `server/customizations/ClusterFGuardWitness.cs:174-212` | Living observer, ordinary access, same map, visible nonhidden actor, range and LOS; guard/player/civilian roles. No facing check. |
| `server/customizations/ClusterFGuardWitness.cs:222-288` | Event recording, culprit-location witness query, merged offenses, stored last-seen points. |
| `server/customizations/ClusterFGuardWitness.cs:293-358` | Living-player reports, most recent retained witnessed incident, hearing around corners in the same town, cooldown and report retention. No dispatch. |
| `server/customizations/ClusterFGuardWitness.cs:363-425` | Observe-only hook adapters; Administrator command registration at line 135; on/off/status/log; no player result message, runtime test-shard check, clearing on off, or persistence. |
| `server/patches/GuardedRegion-witness-observe.patch` | Calls the recorder before the existing speech, criminal aggression, criminal assistance, and criminal-action responses; never replaces or suppresses them. Disabled guarded regions return before these hooks. |
| `docker/uo/apply-patches.sh:860-867`, `CHANGELOG.md:57-61`, `docker/uo/Dockerfile:3` | Merged observation patch registration, Staff-only release description, upstream pin. |
| `server/tests/Regions/GuardWitnessVerification.cs` | Read the facts for sight, event witnesses, real speech/report entry, and jurisdiction. They also assert that the stock response still takes the culprit as guard focus. |
| `server/customizations/ShardCommandAttribute.cs` | `TestOnly` is descriptive command metadata, not an activation check. |
| `U/Regions/GuardedRegion.cs:153-365` | Stock construction, speech, candidate checks, eight-tile NPC fake call, 14-tile call search, renewable 15-second candidate window, eligibility exclusions and `AllowReds = Core.AOS`. No new law inferred from red names. |
| `U/Mobiles/Guards/BaseGuard.cs:11-95,222-335` | Instant-kill default true, nearby guard reuse/construction, target-location creation, teleporting attack, idle behavior. Runtime setting unverified. |
| `U/Skills/Stealing.cs:107-121,337-421` | Existing Young restrictions, revealing action, caught/criminal decisions, and eight-tile notice broadcast. A theft message is not witness evidence in this recorder. |
| `server/patches/Stealing-caught-osi-skill.patch` | Confirmed the shard already changes the caught-skill calculation; the guide does not quote upstream theft odds or attribute this existing change to patrols. |
| `U/Mobiles/BaseCreature.cs:2897-2940` | Criminal and harmful-action propagation to pet/summon owners, relevant to P640's ownership finding. |
| `S/Mobiles/Mobile.cs:4528-4537,5544-5592` | Criminal flag set before region callback; speech range and region delivery before ordinary recipients. |
| `tools/progress.py` | Reporter path overrides and the incidental snapshot write even under `--dry-run`. |

Searched canonical customizations, patches, tests, and build wiring for patrol/guard hooks and recorder references. The implemented service and its sole observation patch are the basis of the guide, not a keyword count. Did not inspect `server/uo/` or contact any running service.

## Where design, notes, and implementation differ

### Stage-one scope, rather than a missing feature claim

P608 proposes physical guards, authored posts/routes, ordinary combat, bounded search and pursuit, local relays, town conversion, New Haven safety qualification, and a shared routine-challenge adapter. The merged code only records observations. P628 explicitly calls this stage one, and P635 changes integration only. The guide excludes proposed combat stats, movement cadences, post allocations, arrival targets, and Persuasion thresholds from current rules.

Directly seeing a crime does not dispatch a guard through this service. Civilian witnesses do not automatically submit its reports. An investigation with no suspect does not start a search. No listener does not emit the design's "No guard answers nearby" message. Stock responses can still happen in all of those cases. The code also has no report-choice menu. These are scope boundaries, not behavior promised by the draft.

### Existing implementation defects carried forward

These are our recorder defects, previously raised in P628/P635/P640 reviews. They remain in this checkout. They were traced in source for this writing task, not reproduced at runtime or fixed here.

| Disagreement | Source evidence and effect on the guide |
| --- | --- |
| Advertised test-only activation is not enforced. | `ClusterFGuardWitness.cs:135,377-391` registers unconditionally and enables without checking shard identity. `ShardCommandAttribute.cs` declares metadata only. The guide says intended for test-shard use and off by default; it does not promise activation is impossible elsewhere. |
| Witnesses need not see the actual action location. | `Record` sets `location = culprit.Location` at line 240 and passes it to `Sees` at line 280. The helper's extra action-location LOS branch at line 191 never sees a different location through these hooks. Seeing the actor around a corner can credit a witness who cannot see the victim/action. The guide describes the actual actor check and warns that records can misattribute observations. |
| Distinct offenses can become one incident. | Line 241 merges by culprit and one-second age in the town, without checking victim, kind, or place. Lines 264-285 upgrade aggression, keep the first available victim and original incident time/place, and add witnesses from later callbacks. P628's assertion that the record captures exactly an act's witnesses is too strong. The guide identifies this merge limitation instead of claiming perfect evidence. |
| Pet/summon owner flags can manufacture a witnessed act at the owner's position. | `U/Mobiles/BaseCreature.cs:2897-2904` forwards `CriminalAction` to a player master; `S/Mobiles/Mobile.cs:4535-4537` invokes that master's region. `ClusterFGuardWitness.cs:366-367,240-285` records the master and scans nearby witnesses as if that position were another physical offense. Incident fields at lines 57-69 lack a responsible-master link. The guide warns about distant-owner records and does not claim correct pet/owner attribution. |
| Recorded incidents need not be guard-eligible. | Observation calls precede `CheckGuardCandidate` in the patch. `Record` at lines 222-288 has no eligibility field/check, unlike `U/Regions/GuardedRegion.cs:337-344`, which rejects guards, dead/staff/blessed actors, and invulnerable creatures. `Report` at line 329 considers only age and witness membership. The guide separates records from lawful enforcement and makes no promise that a suspect-bearing record authorizes punishment. |
| Caller cooldown history is unbounded. | `_lastCall` at line 130 retains mobile keys after the reporting window ends or reports are evicted; line 324 updates them without pruning. Only `ResetForTests` clears it, at line 144. Off at lines 390-392 does not clear records either. The guide distinguishes a restart from disabling and does not claim all diagnostic storage is bounded. |

There are also bounded retention limits: at most 64 incidents per town and 64 reports in the service, from `ClusterFGuardWitness.cs:114,118,256-260,352-355`. Old entries can be evicted before the report-age window ends under load. No performance or coverage guarantee follows from those caps. This is another reason the player guide describes the most recent *recorded* incident rather than promising that every crime remains reportable for 15 seconds.

## Verification and limits

This is a source-checked draft, not a client or live-shard check. No tests were added, so no new red/green claim is made. Lane tests are none. P628/P635's reported builds and test results were read, not rerun; no build was needed for these Markdown-only additions.

Unverified: running deployment and activation, `guards.instantKill` runtime value, bounty enablement, live/hand-placed guards, real Cove walls/floors and route reachability, client speech controls, new-player safety in a running world, and performance. The draft does not offer new patrol guarantees based on any of them.

Reviewed both complete drafts against the source references above. Both files use plain American English and ASCII punctuation, with no em dashes or trailing whitespace. Every relative Markdown link resolves. Each file is below 5 MB. `git diff --check` is clean in both work copies; direct whitespace inspection also covered the new, untracked Markdown files. Final scope review showed only the requested guide and this task note in the notes work copy, and a clean code work copy.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` set to the supplied work copies: exit 0, report produced. Intercepted its incidental `tools/progress.json` write in process memory and confirmed the existing snapshot bytes were unchanged. No progress artifacts or README files changed. PowerShell commands ran under Windows PowerShell 5.1.

No build, container, client, deployment, Haven connection, account/save operation, commit, merge, push, or branch switch was performed. Stop requests were checked between research, drafting, and final review; none was present at the final check.

P653 DONE
