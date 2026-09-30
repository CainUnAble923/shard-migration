"""F-1 red runs C and D, each break aimed at one fact. Same apply/restore/SHA-256 machinery as redrun.py."""
import sys

sys.argv = sys.argv  # noqa
exec(open(r'C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-shard-migration/e1270c9e-f74d-4ed0-afa7-c526ef24aa10/scratchpad/redrun.py',
          encoding='utf-8').read().split('\ndef sha(p):')[0])

R = C + 'ClusterFCraftRun.cs'
J = C + 'ClusterFCraftRejects.cs'

BREAKS['C'] = [
    # fact 1: items mode counts attempts.
    (R, 'public int Counted => CountAttempts ? Attempts : ExceptionalOnly ? Exceptional : Made;',
        'public int Counted => Attempts; // RED C'),
    # fact 3: no cap.
    (R, 'Target = Math.Min(requested, cap),', 'Target = requested, // RED C'),
    # fact 4: rejects left where they are made.
    (J, '        var from = run.From;\n        var pack = from.Backpack;\n',
        '        return; // RED C\n        var from = run.From;\n        var pack = from.Backpack;\n'),
    # fact 5 (moved): no check.
    (R, '        if (from.Map != run.StartMap || from.Location != run.Start)\n        {\n            return MakeXStop.Moved;\n        }\n',
        '        // RED C: moved not checked\n'),
    # fact 5 (gump closed): Stop ignored.
    (R, '        if (run.StopRequested)\n        {\n            return MakeXStop.Stopped;\n        }\n',
        '        // RED C: Stop ignored\n'),
]

BREAKS['D'] = [
    # fact 2: an attempt counted only when it makes something.
    (R, '        run.Attempts++;\n\n        if (made == null)\n',
        '        if (made != null) run.Attempts++; // RED D\n\n        if (made == null)\n'),
    # fact 5 (tool): no check.
    (R, '        if (run.Tool == null || run.Tool.Deleted || run.Tool.UsesRemaining < 1)\n        {\n            return MakeXStop.Tool;\n        }\n',
        '        // RED D: tool not checked\n'),
    # fact 5 (pack full): no check.
    (R, '        if (pack == null || made?.Deleted == false && !made.IsChildOf(pack) || pack.TotalItems >= pack.MaxItems)\n        {\n            return MakeXStop.PackFull;\n        }\n',
        '        // RED D: pack not checked\n'),
    # fact 5 (overweight): no check.
    (R, '        if (StaminaSystem.IsOverloaded(from))\n        {\n            return MakeXStop.Overweight;\n        }\n',
        '        // RED D: weight not checked\n'),
    # fact 5 (died): a refusal after death not recognised.
    (R, '        if (from.Deleted || !from.Alive)\n        {\n            reason = MakeXStop.Died;\n        }\n        else if',
        '        if (false) // RED D\n        {\n            reason = MakeXStop.Died;\n        }\n        else if'),
    # fact 5 (materials): reported as something else.
    (R, '        context.Run = null;\n        context.LastRun = run;\n',
        '        if (reason == MakeXStop.Materials) reason = MakeXStop.CannotCraft; // RED D\n        context.Run = null;\n        context.LastRun = run;\n'),
]

exec('def sha(p):' + open(r'C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-shard-migration/e1270c9e-f74d-4ed0-afa7-c526ef24aa10/scratchpad/redrun.py',
                         encoding='utf-8').read().split('\ndef sha(p):')[1])
