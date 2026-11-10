# cc-P858: the mutants: red/<name>/ holds the one changed file (same name probe-inner.sh copies), each breaking one rule.
# (red/stub/ is written by hand: the code before the change.) Run: python -P make_red.py
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CUS = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations'
FILES = {
    'ShardLamps.cs': CUS + '/Items/Lights/ShardLamps.cs',
    'FestivalWagon/FortuneTellerWagon.cs': CUS + '/FestivalWagon/FortuneTellerWagon.cs',
    'FestivalWagon/FortuneTellerWagonDesign.cs': CUS + '/FestivalWagon/FortuneTellerWagonDesign.cs',
    'AchievementStore.cs': CUS + '/RewardStores/AchievementStore.cs',
    'FestivalStore.cs': CUS + '/RewardStores/FestivalStore.cs',
}

MUTANTS = {
    # a turned lamp forgets it was lit
    'm-flip-unlit': ('ShardLamps.cs', 'ItemID = Burning ? next.Lit : next.Unlit;', 'ItemID = next.Unlit;'),
    # the lamp does not turn
    'm-noflip': ('ShardLamps.cs', '        if (looks.Length < 2)\n        {\n            return;', '        if (looks.Length > 0)\n        {\n            return;'),
    # the look is always the first (an east lamp lights as a south one)
    'm-lookindex': ('ShardLamps.cs', '                if (looks[i].Unlit == ItemID || looks[i].Lit == ItemID)', '                if (i == 0)'),
    # the lamp burns out after an hour
    'm-burnout': ('ShardLamps.cs', '        Duration = TimeSpan.Zero; // never burns out', '        Duration = TimeSpan.FromHours(1);'),
    # the Achievement store has no lamps
    'm-ap-rows': ('AchievementStore.cs', '            if (key != ShardLampStock.HalloweenKey)', '            if (false)'),
    # the Halloween stock has no jack-o-lantern
    'm-jack-row': ('FestivalStore.cs', '        yield return R(s, "jacklantern",', '        if (false) yield return R(s, "jacklantern",'),
    # the wagon's parts lose their hues
    'm-hue': ('FestivalWagon/FortuneTellerWagon.cs', 'new FortuneTellerWagonComponent(p.ItemID) { Hue = p.Hue };', 'new FortuneTellerWagonComponent(p.ItemID);'),
    # the stall goes up without the wagon
    'm-up-wagon': ('FestivalStore.cs', '            var wagon = new FortuneTellerWagon();\n            wagon.MoveToWorld(w, Facet);\n            placed.Add(wagon.Serial);\n        }',
                   '        }'),
    # the wagon is placed but not tracked, so the stall's take-down leaves it
    'm-untracked': ('FestivalStore.cs', '            wagon.MoveToWorld(w, Facet);\n            placed.Add(wagon.Serial);\n        }', '            wagon.MoveToWorld(w, Facet);\n        }'),
    # an existing world never gets the wagon
    'm-topup': ('FestivalStore.cs', '        if (WagonAt is not { } w || !IsUp || Wagon != null)', '        if (WagonAt is not { } w || true)'),
    # the top-up places a second wagon every time
    'm-topup-twice': ('FestivalStore.cs', '        if (WagonAt is not { } w || !IsUp || Wagon != null)', '        if (WagonAt is not { } w || !IsUp)'),
}


def stairless(text):
    # the design as downloaded at the porch: the ladder back, no stair rows
    lines = [l for l in text.splitlines() if not (l.strip().startswith('new(0x0722') or l.strip().startswith('new(0x0721'))]
    i = next(n for n, l in enumerate(lines) if l.strip() == '];')
    lines.insert(i, '        new(0x3DB4, 0, 6, 10, 0, null, "a ladder"),')
    return '\n'.join(lines) + '\n'


for name, (rel, old, new) in MUTANTS.items():
    src = open(FILES[rel], encoding='utf-8').read()
    if src.count(old) != 1:
        sys.exit('%s: anchor found %d times' % (name, src.count(old)))
    out = os.path.join(HERE, 'red', name, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='\n').write(src.replace(old, new))
    print('wrote', name)

# m-ladder: the author's ladder, no stair (FestivalWagon/ needs both files: the folder replaces the copy's)
d = os.path.join(HERE, 'red', 'm-ladder', 'FestivalWagon')
os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'FortuneTellerWagonDesign.cs'), 'w', encoding='utf-8', newline='\n').write(
    stairless(open(FILES['FestivalWagon/FortuneTellerWagonDesign.cs'], encoding='utf-8').read()))
open(os.path.join(d, 'FortuneTellerWagon.cs'), 'w', encoding='utf-8', newline='\n').write(
    open(FILES['FestivalWagon/FortuneTellerWagon.cs'], encoding='utf-8').read())
print('wrote m-ladder')
# m-hue's folder replaces the copy's FestivalWagon/: it needs the design too
open(os.path.join(HERE, 'red', 'm-hue', 'FestivalWagon', 'FortuneTellerWagonDesign.cs'), 'w', encoding='utf-8', newline='\n').write(
    open(FILES['FestivalWagon/FortuneTellerWagonDesign.cs'], encoding='utf-8').read())
