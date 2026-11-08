# cc-P801: one deliberate break per behaviour, each written as changed sources under notes/cc-P801-tools/mutants/<name>/.
# run-mutants.sh builds each in one container and runs the jail facts. Each must turn a fact red; see mutants.txt.
import os, shutil
S = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/'
OUT = 'D:/UO/golems/Iron/shard-migration/notes/cc-P801-tools/mutants/'
J, TT, WT, CT = 'TutorialJail.cs', 'TutorialTradeTrials.cs', 'TutorialWingTrials.cs', 'TutorialCoreTrials.cs'
M = {
 'no-shown-color': (J, 'IShownNotoriety shown => shown.ShownNotoriety,', 'IShownNotoriety shown => null,'),
 'orange-wrong': (J, '"Orange", 0x90, Notoriety.Enemy,', '"Orange", 0x90, Notoriety.Criminal,'),
 'tam-real-murderer': (J, 'person.RangeHome = 0;', 'person.RangeHome = 0; if (i == 4) { person.Kills = 5; }'),
 'click-not-answered': (J, 'base.OnAosSingleClick(from);\n            Answer(from);', 'base.OnAosSingleClick(from);'),
 'people-harmable': (J, 'public int ShownNotoriety => TutorialJail.People[Role].Noto;\n        public override bool IsInvulnerable => true;', 'public int ShownNotoriety => TutorialJail.People[Role].Noto;'),
 'gray-seen-by-all': (J, 'PlayerMobile pm when source == target && ', 'PlayerMobile pm when '),
 'gray-is-real-crime': (J, 'trial.Player.Delta(MobileDelta.Noto); // the client', 'trial.Player.Criminal = gray; trial.Player.Delta(MobileDelta.Noto); // the client'),
 'gray-karma-loss': (J, 'Overhead(pm, "Your name is gray", 0x3B2);', 'pm.Karma -= 50; Overhead(pm, "Your name is gray", 0x3B2);'),
 'crate-before-names': (J, 'else if (trial.Steps.Contains(TutorialJail.CrateStep) || !NamesDone(trial))', 'else if (trial.Steps.Contains(TutorialJail.CrateStep))'),
 'crate-done-on-take': (J, 'SetGray(trial, true);\n', 'SetGray(trial, true); trial.Steps.Add(TutorialJail.CrateStep);\n'),
 'drop-back-ignored': (J, 'public override bool OnDragDrop(Mobile from, Item dropped) => TutorialWingTrials.JailDropped(from, dropped);', ''),
 'ledger-before-crate': (J, 'if (JailTrial(from) is not { } trial || !trial.Steps.Contains(TutorialJail.CrateStep) ||', 'if (JailTrial(from) is not { } trial ||'),
 'guards-no-thief-needed': (J, 'JailTrial(e.Mobile) is { JailThief: { Deleted: false } thief, JailStriking: false } trial &&', 'JailTrial(e.Mobile) is { JailStriking: false } trial && trial.JailThief is var thief &&'),
 'any-word-calls': (J, 'e.Speech.Contains("guards", StringComparison.OrdinalIgnoreCase)', 'e.Speech.Length > 0'),
 'strike-twice': (J, 'trial.JailStriking = true;\n', ''),
 'strike-is-instant': (J, 'guard.SayTo(pm, GuardCallLine);\n', 'guard.SayTo(pm, GuardCallLine); Step(trial, TutorialJail.ThiefStep);\n'),
 'thief-public': (J, 'public bool ShowsTo(Mobile viewer) => viewer == _trainee;', 'public bool ShowsTo(Mobile viewer) => true;'),
 'lost-pouch-stays-gray': (J, 'if (trial.JailGray && trial.Loaners.Count == 0)', 'if (false)'),
 'lost-pouch-earns': (J, 'SetGray(trial, false);\n                Show(trial.Player, trial);', 'SetGray(trial, false); trial.Steps.Add(TutorialJail.CrateStep);\n                Show(trial.Player, trial);'),
 'gray-outlives-lesson': (J, 'private static void EndJail(Trial trial)\n        {\n            SetGray(trial, false);', 'private static void EndJail(Trial trial)\n        {'),
 'ledger-not-own': (J, 'Karma: {pm.Karma}.', 'Karma: 0.'),
 'seed-twice': (J, 'if (Has(map, id, at)) { continue; }', ''),
 'no-reopen': (CT, "if (TutorialWingTrials.ReopenJail(pm)) { return true; } // cc-P801: the jail's window again", ''),
 'gump-closes-on-step': (WT, 'pm.SendGump(new TutorialJailGump(trial));', ''),
 'cant-finish-early-check': (TT, 'TutorialJail.Key => (TutorialJail.Hall, "the New Haven jail"), // cc-P801', ''),
 'now-line-all': (J, 'var left = TutorialJail.People.Where(p => !trial.Steps.Contains(p.Step)).Select', 'var left = TutorialJail.People.Select'),
}
del M['cant-finish-early-check']  # the arrow's name: read in the shots, no fact
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
for name, (rel, a, b) in M.items():
    s = open(S + rel, encoding='utf-8', newline='').read()
    if '\r\n' in s:
        a = a.replace('\n', '\r\n'); b = b.replace('\n', '\r\n')
    assert s.count(a) == 1, (name, s.count(a))
    d = OUT + name
    os.makedirs(d)
    open(d + '/' + rel, 'w', encoding='utf-8', newline='').write(s.replace(a, b))
    open(d + '/target', 'w').write(rel)
print(len(M), 'mutants')
