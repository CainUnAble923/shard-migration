# cc-P91: fixture shaped like cc-P71 (a deploy code block, then a numbered in-game checklist)

## Headlines

- Not a checklist: this list is under Headlines, not For Chase.

## Deviations and decisions for Chase

1. Not a checklist either: decisions are not play-tests.

## For Chase

Commit, then deploy (Windows PowerShell, `;` between commands):

```
cd D:\ShatteredLegacy; git status --short
docker tag sl-modernuo:cc-p91 sl-modernuo:latest
```

Then restart the test shard the usual way. The log should show `[ShardVersion] Shattered Legacy 2026.10.10 ...`.

In-game checklist (a staff character can `[set` its own skills):

1. Nerve Strike at Bushido 200 against a monster, twenty times: about one strike in twenty does not paralyze. At 120,
   about two in twenty do not.
2. Stable slots: Taming, Lore and Veterinary 200, then stable pets at an animal trainer. The 24th is refused, and 23 fit.
3. `[version` shows 2026.10.10 and the bulletin lists the five lines.

P91 DONE
