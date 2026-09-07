# How this project works

Written 2026-09-07, at Chase's request, because a future session (and a future Chase) will
want the shape of the thing rather than the history of it.

## The loop

1. Claude writes a prompt for one task.
2. Chase pastes it into a **fresh** Claude Code chat.
3. Claude Code works, commits to both repos, and writes findings in `notes/`.
4. Chase says it is done.
5. Claude reads the commits and the note, **verifies the claims that matter**, answers the
   questions it opened, updates `docs/`, and writes the next prompt.
6. Chase pushes.

One task, one chat, every time. Nothing about this loop requires Chase mid-task.

## Who does what, and why

| | Can | Cannot |
|---|---|---|
| **Claude Code** | build, run a container, run tests, see whether something actually works | change direction, edit `docs/`, deploy |
| **Claude (overseer)** | review, decide, maintain `docs/`, write prompts, answer the queue | compile anything, push to GitHub |
| **Chase** | everything with consequences | - |

The split follows *who can verify a claim*. Claude cannot compile, so Claude never writes code
and never asserts that something builds. Claude Code can compile but cannot see the whole
backlog or carry a decision between chats, so it does not make decisions that outlive its
session.

**Chase owns anything irreversible or account-affecting**: `docker compose up`, restarts, image
deploys, world saves, money, and direction. No agent ever touches the live shard.

## The repo is the memory

Every Claude Code chat starts with **no memory of the previous one**. `AGENTS.md` and `docs/`
are how a fresh chat reconstructs the world in its first minute.

That is why a stale line in `AGENTS.md` is a real defect and not a tidiness issue. One stale
rule ("decline anything resting on a missing subsystem") kept steering agents wrong for two
tasks after the decision had changed, and it cost real content.

**`notes/` is the agents'. `docs/` is Claude's.** Agents write what they found; Claude decides
what it means. When an agent disagrees with a decision, it says so in the question queue rather
than quietly doing something else. That is how the armour set-bonus system and the entire quest
category got reopened.

## The question queue

`notes/codex-questions.md`. An agent cannot wait hours for an answer, so it:

1. records the question,
2. picks the most reasonable option,
3. **states the assumption it is proceeding on**,
4. keeps working.

Claude answers later, and the answer either confirms the assumption or says what to change.
Nothing stalls, and Chase is never the bottleneck mid-task.

## Why so much of this is measurement

**Nine counts on this project have been stated without counting, and all nine were wrong.** Two
of them drove decisions:

- The armour set-bonus system was declined because "ModernUO ships zero files for it". It was
  **387 lines** and freed **114 files**.
- The whole Mondain's Legacy quest category was declined because "ModernUO ships a different
  quest engine". ModernUO already ships **240 quests** on the same engine.

The expensive failure on this project has never been bad code. It has been **confidently doing
the wrong work, or skipping work worth doing.** So surveys earn their place: S3 shipped no code
at all and removed 223 files of backlog that did not exist.

Hence the standing rules: count the artifact rather than a description of it, publish the file
list beside the count, filter by what ModernUO actually lacks, and never adjust the work to
match a number in a document.

## What actually makes it work: the disagreement

Claude Code has corrected the overseer on:

- both "fidelity traps" in the original port recipe, one of them exactly backwards
- `SetWeaponAbility`, which was not blocking and made 57 files look blocked
- `TribeType`, same shape, another 53 files
- the `187` unblock ratio used to justify building a subsystem (really 114)
- "six tests" when there were four
- the premise under the entire quest decline

If it simply did what the prompts said, the shard would have less content and several documents
would be confidently wrong. This is why prompts say things like *"a well-evidenced no in an hour
is a good result"* and *"never adjust the work to match a number in a document, including one in
your own brief."*

An agent that stops and says the brief is wrong is doing the job. An agent that quietly makes the
work fit the brief is not.

## The four lanes

- **F** - Foundation. Fixing what was already broken before any porting. Done, 7/7.
- **P** - Proving. Validate the port recipe, time it. Output is knowledge, not content.
- **S** - Subsystems and enabling work. Builds (S1, S6, S7), infrastructure (S4), one survey
  (S3), one spike (S5). Not tests, despite the pattern; these ship real code.
- **C** - Content batches. The volume.

**The S lane has been worth more per hour than the C lane so far**, because each one either
unlocks a category or deletes phantom work. That is not a detour; it is why the remaining work
is measured in hundreds of files rather than thousands.

## Three content lanes, three different rule sets

1. **Ported OSI content** (C and S tasks). `docs/fidelity-principle.md` applies: port unchanged,
   so UOGuide and Stratics do our documentation.
2. **Community scripts** (`docs/community-scripts-wishlist.md`). Someone else's custom code.
   Licensing to resolve, quality unverified, and every item is documentation debt.
3. **Our own custom systems** (ClusterF, PetMimic, the League, the guild systems). Already ours,
   already documented only by us. Improving them is shard design, not acquisition.

Keeping them separate is what stops the fidelity accounting from being contaminated by choices
that were made deliberately for other reasons.
