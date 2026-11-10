"""cc-P856: one-off. The release copy's WinterDecorVerification.cs gets main's three updates (the facts that place or
count every row now count the winter set's rows too, an addon row is checked as a WinterSeasonAddon, and clearing takes
the addons' parts with them). python -P edit_wintertests.py <WinterDecorVerification.cs>"""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8").read()


def after(method, old, new):
    global s
    i = s.index(method)
    j = s.index(old, i)
    s = s[:j] + new + s[j + len(old):]


note = "   // cc-P856: the winter set's rows too"
after("public void TheAutomaticCheckPlacesInRangeRemovesAfterAndActsOnlyWhenTheSeasonChanges()",
      "var rows = ClusterFWinterDecorLayout.Rows.Length;", "var rows = ClusterFWinterDecor.AllRows.Length;" + note)
after("public void PlaceTwicePlacesOnceAndClearRemovesExactlyTheDecorBySerialAndNothingElse()",
      "var rows = ClusterFWinterDecorLayout.Rows;", "var rows = ClusterFWinterDecor.AllRows;" + note)
after("public void TheDecorAndTheStateSurviveARestart()",
      "var rows = ClusterFWinterDecorLayout.Rows;", "var rows = ClusterFWinterDecor.AllRows;" + note)
old = """                Assert.Equal(r.ItemId, p.ItemID);
                Assert.Equal(r.Hue, p.Hue);"""
assert s.count(old) == 1
s = s.replace(old, """                if (r.Layer == ClusterFWinterSetLayout.AddonLayer)
                {
                    Assert.IsType<WinterSeasonAddon>(p);   // cc-P856: an addon has no art of its own (its parts do)
                }
                else
                {
                    Assert.Equal(r.ItemId, p.ItemID);
                }

                Assert.Equal(r.Hue, p.Hue);""")
old = "            Assert.Equal(before - rows.Length, World.Items.Count);"
assert s.count(old) == 1
s = s.replace(old, """            // cc-P856: each winter set addon takes its parts with it
            var parts = ClusterFWinterSetLayout.Rows.Sum(r => WinterSetDesigns.All[ClusterFWinterSetLayout.DesignOf(r.Key)].Parts.Count);
            Assert.Equal(before - rows.Length - parts, World.Items.Count);""")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok", p)
