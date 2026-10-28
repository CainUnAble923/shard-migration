import os
os.chdir(r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Tutorial")


def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("TutorialFarm.cs", [
("""        /// <summary>The isle's farm addon.</summary>
        public static TutorialIsleFarmAddon? FindAddon(Map map) => FindAddon<TutorialIsleFarmAddon>(map, TutorialIsleFarmLayout.Anchor);""",
 """        /// <summary>The isle's farm addon.</summary>
        public static TutorialIsleFarmAddon? FindAddon(Map map) => FindAddon<TutorialIsleFarmAddon>(map, TutorialIsleFarmLayout.Anchor);

        // cc-P718 item 6: the farm gate's sign was P276's wall arm (0x0B97) with a board hung on it (0x0BCF), standing on
        // the ground, where it read as debris. On the isle it is a standing post with its board (0xA854) instead. The
        // generated layout keeps P276's pieces; the isle's addon swaps them as it is built, and FixGateSign mends a farm
        // placed before.
        public const int OldSignArm = 0x0B97;
        public const int OldSignBoard = 0x0BCF;
        public const int GateSignpost = 0xA854;
        public const string GateSignpostName = "Farm signpost: Wren the Farmhand at the gate";

        /// <summary>The isle farm's art for a layout piece, or null to leave it out.</summary>
        public static int? IsleArt(int id) => id switch
        {
            OldSignArm => GateSignpost,
            OldSignBoard => null,
            _ => id
        };

        /// <summary>cc-P718: swaps an isle farm's old gate sign for the standing post. Returns the pieces changed.</summary>
        public static int FixGateSign(BaseAddon addon)
        {
            var changed = 0;
            foreach (var c in addon.Components.ToArray())
            {
                if (c.ItemID == OldSignArm)
                {
                    c.ItemID = GateSignpost;
                    c.Name = GateSignpostName;
                    changed++;
                }
                else if (c.ItemID == OldSignBoard)
                {
                    c.Delete();
                    changed++;
                }
            }

            return changed;
        }"""),
("""            if (FindAddon<TutorialIsleFarmAddon>(map, TutorialIsleFarmLayout.Anchor) != null) { present++; }""",
 """            if (FindAddon<TutorialIsleFarmAddon>(map, TutorialIsleFarmLayout.Anchor) is { } placed)
            {
                present++;
                if (!dryRun) { FixGateSign(placed); } // cc-P718
            }"""),
("""            var a = TutorialIsleFarmLayout.Anchor;
            foreach (var (id, x, y, z) in TutorialIsleFarmLayout.Pieces)
            {
                AddComponent(new AddonComponent(id), x - a.X, y - a.Y, z - a.Z);
            }""", """            var a = TutorialIsleFarmLayout.Anchor;
            foreach (var (id, x, y, z) in TutorialIsleFarmLayout.Pieces)
            {
                if (TutorialFarm.IsleArt(id) is not { } art)
                {
                    continue;
                }

                var c = new AddonComponent(art);
                if (art == TutorialFarm.GateSignpost)
                {
                    c.Name = TutorialFarm.GateSignpostName; // cc-P718
                }

                AddComponent(c, x - a.X, y - a.Y, z - a.Z);
            }"""),
])
print("ok")
