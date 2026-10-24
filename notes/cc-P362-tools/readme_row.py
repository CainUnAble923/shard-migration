"""cc-P362: adds patch 0005's row to client\\README.md (once). python -P readme_row.py <ShatteredLegacy repo>"""
import os
import sys

p = os.path.join(sys.argv[1], "client", "README.md")
t = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in t else "\n"
anchor = r"| `server\customizations\ClusterFExplorationManager.cs` (also duplicated in `ClusterFExplorationSync.cs`, cc-P240) |" + nl
assert t.count(anchor) == 1, "anchor"
assert "0005-ui-skins-appearance.patch" not in t
row = (r"| `0005-ui-skins-appearance.patch` | `3212623f` plus 0001 to 0004 | **UI skins** (cc-P362): Options > Interface > "
       r"**Appearance** picks a look per kind (backpack, bags, metal chests and the bank box, crates, spell scrolls), "
       r'"Classic (stock)" first and the default, with a small preview. Saved per profile (`Profile.SlSkins`). A pick '
       r"remaps the stock gump (or a scroll's art) to one of our PNGs under a NEW ID (`ExternalImageLoader.SetGumpRemap` "
       r"and `SetArtRemap`, after 0002's override and before the ID's own PNG) and redraws it (`Gump.Invalidate`, "
       r"`Art.Invalidate`); stock IDs are never overwritten, and a skin whose files are not here is not offered. The table "
       r"`Game\Managers\SlSkins.cs` is `player-package\vendor\shattered-legacy-art\skins.json` "
       r"(`player-package\tests\Ui-Skins.Tests.ps1` keeps them the same). New `SlSkins.cs` and `AppearanceTab.cs`, hooks "
       r"in five upstream files, 6 unit tests | none (client-side only) |" + nl)
t = t.replace(anchor, anchor + row)
open(p, "w", encoding="utf-8", newline="").write(t)
print("ok")
