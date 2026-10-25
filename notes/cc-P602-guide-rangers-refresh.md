# P602: Rangers, Custodians, and Healers guide refresh

October 25, 2026. Documentation only.

## Changes

Updated `notes/wiki-drafts/rangers-custodians-healers.md` with the Rangers' elixir of rebirth sale from P480 and a clearly planned Tracking Ping section from P563. Added source links and a refresh date scoped to these additions. The Custodian and Healer sections were left as reviewed on October 21.

The elixir section gives the member dashboard route, 375 gold member price, 500 gold animal trainer price, payment source, and the conditions for using the consumable. The Ping section describes the proposed radar display, fallback, base skill progression, focus, cost, cooldown, training rule, floor limits, and player visibility protections. All Ping tuning is identified as recommended rather than implemented or settled.

## Evidence

Paths below are relative to the code work copy unless identified as notes.

- `server/customizations/OutridersGuildmasterGump.cs:259-267,365-386`: member dashboard sale, membership check, price at three quarters of the trainer price, backpack or bank payment, and elixir delivery.
- `server/customizations/Tutorial/TutorialPetCare.cs:187-196`: `SBPetRebirth.Price` is 500 gold and its buy list sells the elixir.
- `server/patches/AnimalTrainer-elixir-of-rebirth.patch:4-8`: adds that buy list to animal trainers.
- `server/customizations/Items/Consumables/ElixirOfRebirth.cs:19-94`: backpack use, dead bonded pet, corpse gone, two tile range, living user, valid resurrection tile, and consumption on success.
- `notes/cc-P480-tutorial-first-play-fixes.md`, Part 8 and the elixir price section: supporting implementation notes.
- `notes/cc-P563-tracking-ping-design.md`, recommendation and proposed rules: design source. A search of canonical customizations and patches for `TrackingPing` and `Tracking Ping` found no implementation.

## Verification and limits

Read both work copies' AGENTS.md and the required direction and task documents. Reviewed the draft additions against the sources above. Lane tests: none, as requested for this documentation task. No tests were added or run. Live availability, configuration, and client behavior were not verified. No Haven connection, build, deployment, code change, or Git mutation was performed.

`git diff --check` passed. The draft and task note contain no em dashes and are each below 5 MB. Both new source links resolve to existing local notes. The shell reported Windows PowerShell 5.1. The code work copy remains clean.

Only the guide draft and this task note were edited. The prompt's explicit scope takes precedence over the standing progress regeneration instruction, which would edit additional files.

P602 DONE
