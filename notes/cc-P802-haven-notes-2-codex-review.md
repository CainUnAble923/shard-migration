# Codex review: P802

CC task P802: New Haven tutorial notes, batch 2 (Chase playing 2026.11.03.1). Reviewed by Codex (`codex exec review`, read-only) after P802 DONE and before the Golem's commit, 2026-11-07 19:26.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The change implements much of the requested behavior, but teaching text is clipped, travel completion does not require Recall, and several explicitly requested lesson relocations remain unfinished. Builds and client behavior were not independently rerun during this read-only review.

- **medium** [P2] Complete the moves for lessons with existing fitting places (`server\customizations\Tutorial\NewHavenLessonPlaces.cs:14`)
  Items 6 and 8 require moving lessons when an appropriate place exists, but the notes explicitly leave Healing and Chivalry in the training yard despite identifying the healer's and ankh locations, and leave Bushido/Ninjitsu there on the release despite identifying both dojos. Needing a beneficial-region adjustment or unchecked echo tiles is unfinished implementation, not the prompt's exception for a missing building. Complete those moves, including their pointers and required region behavior, before marking P802 done.
- **medium** [P2] Count successful Recall casts rather than missing scrolls (`server\customizations\Tutorial\TutorialTradeTrials.cs:281`)
  The away/return steps accept proximity plus a reduced loan-scroll count, which does not establish that Recall occurred. After marking, a player can drop both Recall scrolls (the existing loan cleanup deletes them), walk to Rook, and walk back to finish without casting either spell. Track successful Recall events and their destinations instead. The new test manually consumes scrolls and teleports the player, so it does not catch this violation of item 2.
- **medium** [P2] Make the tour teaching text fully readable (`server\customizations\Tutorial\TutorialWingTrials.cs:823`)
  Tour stops now put their teaching exclusively in `Latest`, but this HTML area is only 60 pixels high with scrolling disabled. For example, `HousingStop1` contains roughly 380 characters, including the next-step directions, and cannot fit in that space. The remainder is clipped instead of being available in the window. Increase the area, paginate it, or enable scrolling; assertions against `gump.Latest` do not verify visibility.

(2.4 minutes, 1,187,461 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The changes implement much of the request, but the new tour display clips teaching, several explicitly requested relocations remain unfinished, and required client verification is missing.

- **medium** [P2] Capture the required lesson-window and release proof (`notes\cc-P802-haven-notes-2.md:262`)
  The submission explicitly has no lesson-window screenshots and uses main's town for the client shots, although testers use different release locations. This leaves the main requested UI changes and release placements without the required before/after client verification; string-property assertions cannot establish that teaching fits onscreen. Exercise the changed lessons on the private release proof shard and capture the requested evidence before DONE, including an actual farm-before view rather than two empty views. The repository's [proof checklist](../guides/building-and-decorating.md#L394-L397) also requires client views and a before shot for replacements.
- **medium** [P2] Finish relocating the lessons with existing suitable buildings (`notes\cc-P802-haven-notes-2.md:156`)
  Items 6 and 8 require these lessons to move when suitable places exist, but Chivalry, Bushido, Ninjitsu and Healing remain in the training yard. The audit identifies existing release dojos, an ankh garden and a healer's; unchecked echo tiles and the need to relocate the beneficial-action region are implementation work, not the prompt's exception for a missing building. Complete those moves and their pointers before marking P802 done.
- **medium** [P2] Give tour teaching enough space to remain readable (`notes\cc-P802-tools\p802-release-isle-20261028.diff:1250`)
  Tour-stop teaching is now rendered in a 60-pixel-high HTML box with scrolling disabled. Text such as `HousingStop1` spans substantially more than three lines, so its later instructions and next-step directions are clipped. Since the full system-message version was removed, players can no longer read the complete lesson. Size this area for its contents or enable scrolling; checking the `Latest` string alone does not test visibility.

(3 minutes, 1,677,347 tokens)
