p = r"D:\UO\golems\Iron\ShatteredLegacy\server\tests\Tutorial\TutorialIsleWalkFixesVerification.cs"
s = open(p, encoding="utf-8").read()
pairs = [
("""        Assert.Contains(isle.GetItemsInRange<Static>(TutorialWorld.Ground(TutorialCorePlacement.ChatSignpost), 0),
            s => s.ItemID == TutorialCorePlacement.SignpostId && s.Name == TutorialCorePlacement.ChatSignpostName);""",
 """        var posts = new List<Static>();
        foreach (var post in isle.GetItemsInRange<Static>(TutorialWorld.Ground(TutorialCorePlacement.ChatSignpost), 0))
        {
            posts.Add(post);
        }

        Assert.Contains(posts, s => s.ItemID == TutorialCorePlacement.SignpostId && s.Name == TutorialCorePlacement.ChatSignpostName);"""),
("private static Point3D Beside(Mobile m, int dx)", "private static Point3D Beside(IEntity m, int dx)"),
]
for old, new in pairs:
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
