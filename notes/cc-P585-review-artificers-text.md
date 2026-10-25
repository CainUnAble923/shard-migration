# P585: review of the Artificers' guildmaster text

Reviewed October 25, 2026. Review completed after a Golem budget pause and resume.

## Scope and evidence

Read both work-copy AGENTS.md files, the direction decision and task-list instructions, P460's implementation note and its adjacent Codex review. That review reported no findings. The three corrections P460 made agree with the guide and the relevant implementation; the findings below concern text left around those corrections.

P460 commit `32b6983d6d190514de9103cc79a2a41c5d4b569c` is an ancestor of local code `main`. The work-copy HEAD and local main are both `6b7437172d2d87af5f7ad2b4daa6048ed6f20efe`. The guildmaster gump, guild system and P460 test file have no differences between P460 and main.

Read `server/customizations/ArtificersGuildmasterGump.cs`, the relevant joining, Apprentice-task, welcome and hall-page paths in `ClusterFGuildSystem.cs`, `server/tests/Misc/ArtificersTextVerification.cs`, `CHANGELOG.md` and `VERSION`. Compared them with `notes/wiki-drafts/artificers-order.md` and checked the underlying imbuing, formula-book, gear and trial paths. Read the related portions of `ImbuingReworkVerification.cs` and `GuildStarterPathVerification.cs`. Tests were inspected, not executed. No new tests or code changes are part of this review.

Code paths below are relative to the ShatteredLegacy work copy. Guide paths are relative to shard-migration. Findings describe the checked source and built-in defaults. Live settings and client rendering are unverified; no Haven connection was made.

## Findings

Two bugs and two risks remain in our guildmaster text. These are ours to fix, not upstream content defects. No code change is included.

1. **bug** - `server/customizations/ArtificersGuildmasterGump.cs:129`. The About page says Essence Shards are gathered from "disenchanting and imbuing work," so a newcomer is told that imbuing earns its own currency. Successful imbuing actually spends Shards and awards Standing (`ArtificersImbueGump.cs:1880` and `:1898`); the guide's Work and rewards table distinguishes those rewards. Suggested fix: name disenchanting, extraction, work orders and the Apprentice task as Shard sources, and say successful imbuing earns Standing.

2. **bug** - `server/customizations/ArtificersGuildmasterGump.cs:155`. What We Enhance promises skill bonuses on robes and cloaks, but the default skill rows allow jewelry or configured crafter gear, which defaults to HalfApron and FullApron (`ArtificersImbueGump.cs:488`, `:499` and `:538`; `Imbuing/ImbuingTable.cs:136`). The guide explicitly limits crafting and gathering skill bonuses to aprons at `notes/wiki-drafts/artificers-order.md:83`; `ImbuingReworkVerification.cs:338` checks the gear restrictions. Suggested fix: describe general attribute bonuses on clothing, and identify aprons as the default clothing eligible for crafting and gathering skill bonuses.

3. **risk** - `server/customizations/ArtificersGuildmasterGump.cs:176`. Joining Requirements still presents the skill-or-diamonds task before telling the reader to click Join "when you are ready," without saying that the task is separate from entry. This preserves the impression that Imbuing 20.0 or three Diamonds are required to join, although `ClusterFGuildSystem.CanJoin` has no skill or tribute requirement (`ClusterFGuildSystem.cs:313`) and only `CompleteApprenticeTask` checks them (`:397`); the guide separates these steps at `notes/wiki-drafts/artificers-order.md:13` and `:19`. Suggested fix: state that joining requires neither skill nor tribute, then label the displayed requirement as the optional next Apprentice task after joining.

4. **risk** - `server/customizations/ArtificersGuildmasterGump.cs:212`. Rewards says the Master Formulary follows the Order's trial and that advanced tiers and rare properties "come from" quests, commissions, loot boxes and bosses, without marking those routes as planned. The guide marks the trial and advanced acquisition routes as planned (`notes/wiki-drafts/artificers-order.md:42` and `:102`), and the trial is waived by default (`ClusterFGuildPromotion.cs:33` and `:79`). A search through canonical customizations and patches for the grant API, tier-key writes and literal knowledge keys found acquisition through reading books and the staff grant interface, with no normal reward caller; `ImbuingTable.cs:191` builds books only through Full. Suggested fix: mark the advanced reward routes as planned and explain that the trial requirement is currently waived under the defaults.

The relevant knowledge-write files inspected were `server/customizations/Imbuing/ClusterFImbueKnowledge.cs` (key storage and grant API) and `server/customizations/Imbuing/ImbueFormulaBooks.cs` (book reading and the staff grant interface). Other text matches in `ArtificersImbueGump.cs` were menu labels, not acquisition paths. The advanced-route finding is limited to these checked canonical sources, not a claim about live player data or external rewards.

## Verification and limits

The existing P460 facts check free joining, Apprentice-task rewards, learned tiers and the forge wording. They do not check the About page's currency sources, the Joining Requirements page, clothing skill eligibility or whether the advertised advanced reward routes exist. Their reported P460 red/green build results were read in its note, not independently rerun. No build or lane tests are required for this text-only review.

Ran `python tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies: exit 0. It reported setup 7/7 resolved and an existing Needs overseer review section. The known dry-run defect changed `tools/progress.json`; the wrapper restored that snapshot byte-for-byte immediately. No generated progress changes are retained.

Final checks: only this note changed in shard-migration; the code work copy is clean. The note is below 5 MB, contains no em dash and has no trailing-whitespace errors. No code, tests, docs-directory files or services were changed. Shell commands ran under Windows PowerShell 5.1.26100.9711. No commits, branch switches, builds, deploys or Haven connections were made.

The first run paused when the stop-request file said the Golem's weekly Codex budget was spent. The user resumed the same task after removing the request. The final wording, duplicate-finding and scope checks are complete; nothing remains for P585.

P585 DONE
