"""cc-P664 red runs: one copy of the edited Tutorial folder per behaviour, with that behaviour put back as it was (or
left out) behind the new API, which does not exist before the change, so the facts cannot compile there. Copies go to
m-<name>/Tutorial beside this file.

    python -P mutate.py <code copy>/server
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRV = sys.argv[1]
F = 'TutorialCopies.cs'
MUTANTS = {
    # P663: one isle for everyone (the Fold)
    'shared': {F: [("        var copy = CurrentCopyOf(pm) ?? PartyCopy(pm);\n",
                    "        return TutorialWorld.Isle;\n        var copy = CurrentCopyOf(pm) ?? PartyCopy(pm);\n")]},
    # no party sharing: every member gets a copy of their own
    'noparty': {F: [("        if (Party.Get(pm) is not { } party)", "        if (true || Party.Get(pm) is not { } party)")]},
    # no hold: a copy is freed as soon as nobody is online on it
    'nohold': {F: [("            if (now - last >= HoldAfterLeaving)", "            if (last != now)")]},
    # login ignores the copy's generation: a freed copy is taken as the trainee's own
    'nogen': {F: [("        return slot.InUse && Assigned.TryGetValue(pm.Serial, out var a) && a.N == slot.N && a.Generation == slot.Generation;",
                   "        return true;")]},
    # reset removes only what the seeding placed: strays stay
    'noreset': {F: [("        foreach (var item in World.Items.Values.Where(i => !i.Deleted && i.Map == map && i.Parent == null).ToList())",
                     "        foreach (var item in World.Items.Values.Where(i => false).ToList())")]},
    # the save leaves out who has which copy
    'nosave': {F: [("        writer.WriteEncodedInt(TutorialCopies.Assigned.Count);\n        foreach (var (serial, (n, generation)) in TutorialCopies.Assigned)",
                    "        writer.WriteEncodedInt(0);\n        foreach (var (serial, (n, generation)) in TutorialCopies.Assigned.Take(0))")]},
    # no line: a trainee who finds every copy in use is never taken to one
    'noline': {F: [("        while (Waiting.Count > 0 && Array.Exists(Slots, s => !s.InUse))",
                    "        while (false)")]},
}

for name, files in MUTANTS.items():
    out = os.path.join(HERE, 'm-' + name)
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(os.path.join(SRV, 'customizations', 'Tutorial'), os.path.join(out, 'Tutorial'))
    for rel, pairs in files.items():
        p = os.path.join(out, 'Tutorial', rel)
        s = open(p, encoding='utf-8', newline='').read()
        crlf = '\r\n' in s
        s = s.replace('\r\n', '\n')
        for old, new in pairs:
            assert s.count(old) == 1, (name, old[:60])
            s = s.replace(old, new)
        open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', '\r\n') if crlf else s)
    print('mutant', name)
