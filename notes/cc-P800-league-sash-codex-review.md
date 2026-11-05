# Codex review: P800

CC task P800: the League sash upgrades over time. Reviewed by Codex (`codex exec review`, read-only) after P800 DONE and before the Golem's commit, 2026-11-05 16:19.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The implementation substantially follows the approved plan, with release-diff, build-log and screenshot artifacts present. However, replacement handling permits duplicate sashes, and configuration changes do not update existing sash appearances or cached tooltips. Builds were not rerun during this read-only review.

- **medium** [P2] Refresh existing sashes after loading changed configuration (`server\customizations\LeagueShop\LeagueSash.cs:370`)
  When staff edit `firstHue`, a step's metal or its bonus and run `[LeagueSash reload`, this assignment changes the table but never refreshes existing items. Their serialized hue remains unchanged and their cached property lists can continue advertising the previous bonus, even though `WornBonus` immediately pays the new percentage. Restarting also retains the saved hue. Reapply the configured appearance and invalidate properties on existing sashes after a successful reload and world load.
- **medium** [P2] Include held sashes before issuing a replacement (`server\customizations\LeagueShop\LeagueSash.cs:539`)
  If a player lifts their sash onto the cursor and opens Elara's sash page, `Find` misses it because it searches only equipment, backpack and bank. `Issue` then supplies a free replacement without deleting or invalidating the original; returning the held sash leaves two usable sashes bound to the same character. This violates the one-sash-per-character requirement. Track the existing item independently of its current container, or otherwise prevent replacements while the original still exists.

(1.7 minutes, 629,141 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The supplied release diff, build logs, and screenshots cover most requested deliverables. However, replacement issuance permits duplicate sashes, and configuration reloads leave existing sash appearances and tooltips inconsistent with their effective behavior.

- **medium** [P2] Refresh existing sashes after reloading their configuration (`notes\cc-P800-tools\p800-release-isle-20261028.diff:596`)
  When staff changes `firstHue`, a step's metal, or its bonus and runs `[LeagueSash reload`, this only replaces the table. Existing sashes retain their previous hue and cached properties, although bonus calculations immediately use the new table. A disabled bonus can therefore still be advertised, and a changed metal can retain the wrong visible color. Refresh existing sash hues and invalidate their properties after a successful reload; also reconcile saved hues on load.
- **medium** [P2] Count the cursor-held sash before issuing a replacement (`notes\cc-P800-tools\p800-release-isle-20261028.diff:701`)
  When a player lifts their sash onto the cursor, ModernUO internalizes it and stores it in `Mobile.Holding`, so this lookup returns null. Opening Elara's sash page then offers a free replacement; returning the original to the backpack leaves two character-bound sashes. Include the held item in the lookup and replacement checks to enforce the required one-sash-per-character limit.

(1.6 minutes, 732,483 tokens)
