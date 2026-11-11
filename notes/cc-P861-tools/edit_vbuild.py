# cc-P861: one-off edit of ClusterFVisualBuilder.cs: the statify verb, parked addons on undo steps, store version 1.
p = r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\ClusterFVisualBuilder.cs"
s = open(p, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:60], s.count(old))
    s = s.replace(old, new)


rep('''    public List<ClusterFBuilderHue> Rehued { get; } = new();
}''', '''    public List<ClusterFBuilderHue> Rehued { get; } = new();

    // cc-P861: addons [VBuild statify parked on the internal map; undo brings them back, a dropped step deletes them.
    public List<ClusterFBuilderStash> Stashed { get; } = new();
}''')
rep('''public sealed record ClusterFBuilderHue(Serial Serial, int Hue);''', '''public sealed record ClusterFBuilderHue(Serial Serial, int Hue);

/// <summary>cc-P861: an addon statify parked on the internal map, and where it stood.</summary>
public sealed record ClusterFBuilderStash(Serial Serial, Point3D From, int MapIndex);''')
rep('''        foreach (var m in step.Moved)
        {
            if (World.FindItem(m.Serial) is { Deleted: false } item)
            {
                item.Location = m.From;
                n++;
            }
        }''', '''        foreach (var m in step.Moved)
        {
            if (World.FindItem(m.Serial) is { Deleted: false } item)
            {
                item.Location = m.From;
                n++;
            }
        }

        // cc-P861: a statify's addon back where it stood (its statics went with step.Placed above).
        n += AddonStatify.Restore(step);''')
rep('''        Steps.Add(step);
        if (Steps.Count > ClusterFVisualBuilder.MaxUndo)
        {
            Steps.RemoveAt(0);
        }''', '''        Steps.Add(step);
        if (Steps.Count > ClusterFVisualBuilder.MaxUndo)
        {
            // cc-P861: a statify step that falls off the history can no longer be undone: its parked addon goes.
            AddonStatify.Discard(Steps[0]);
            Steps.RemoveAt(0);
        }''')
rep('''            case "forget":
                {
                    _sessions.Remove(from.Serial);''', '''            case "statify":
                {
                    // cc-P861: freeze a placed addon into plain statics (StaffBuildTools/AddonStatify.cs).
                    AddonStatify.Begin(from);
                    return;
                }
            case "forget":
                {
                    // cc-P861: nothing is left to undo, so the addons statify parked are deleted for good.
                    foreach (var t in s.Steps)
                    {
                        AddonStatify.Discard(t);
                    }

                    _sessions.Remove(from.Serial);''')
rep('''forget | capture <name> [build|world]]''', '''forget | capture <name> [build|world] | statify]''', 2)
rep('''for a seed or [PlaceBuild; it places and deletes nothing.")]''', '''for a seed or [PlaceBuild; it places and deletes nothing. cc-P861: statify targets an addon and freezes it into plain statics where it stood (art, hue, name, light), one undo step that puts the addon back; it refuses an addon in a house or one a seeder keeps.")]''')
rep('''    public const int CurrentVersion = 0;

    private static ClusterFVisualBuilderStore _instance;''', '''    // 1 (cc-P861): each step also saves the addons statify parked. A version 0 save reads with none.
    public const int CurrentVersion = 1;

    private static ClusterFVisualBuilderStore _instance;''')
rep('''                w.WriteEncodedInt(t.Rehued.Count);
                foreach (var h in t.Rehued)
                {
                    w.Write(h.Serial);
                    w.WriteEncodedInt(h.Hue);
                }''', '''                w.WriteEncodedInt(t.Rehued.Count);
                foreach (var h in t.Rehued)
                {
                    w.Write(h.Serial);
                    w.WriteEncodedInt(h.Hue);
                }

                w.WriteEncodedInt(t.Stashed.Count);
                foreach (var a in t.Stashed)
                {
                    w.Write(a.Serial);
                    w.Write(a.From);
                    w.WriteEncodedInt(a.MapIndex);
                }''')
rep('''                c = r.ReadEncodedInt();
                for (var k = 0; k < c; k++)
                {
                    t.Rehued.Add(new ClusterFBuilderHue(r.ReadSerial(), r.ReadEncodedInt()));
                }''', '''                c = r.ReadEncodedInt();
                for (var k = 0; k < c; k++)
                {
                    t.Rehued.Add(new ClusterFBuilderHue(r.ReadSerial(), r.ReadEncodedInt()));
                }

                if (version >= 1)
                {
                    c = r.ReadEncodedInt();
                    for (var k = 0; k < c; k++)
                    {
                        t.Stashed.Add(new ClusterFBuilderStash(r.ReadSerial(), r.ReadPoint3D(), r.ReadEncodedInt()));
                    }
                }''')
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
