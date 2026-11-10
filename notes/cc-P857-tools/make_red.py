# cc-P857: build the red copies of VariableCarpet.cs into red/: "stub.cs" (the code before the change: the types the facts
# name, all inert) and one mutant per check, each breaking exactly one rule. Run: python -P make_red.py
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Items/Addons/VariableCarpet.cs'
RED = os.path.join(HERE, 'red')
os.makedirs(RED, exist_ok=True)
src = open(SRC, encoding='utf-8').read()

MUTANTS = {
    # nobody-on-the-area check gone
    'm-occupied.cs': ('        foreach (var m in map.GetMobilesInBounds(', '        foreach (var m in Array.Empty<Mobile>()) // RED\n        //'),
    # deed-in-pack check at placement gone
    'm-inpack.cs': ('        if (Deleted || !IsChildOf(from.Backpack))\n        {\n            from.SendLocalizedMessage(1042001); // That must be in your pack for you to use it.\n            return VariableCarpetResult.NotInPack;',
                    '        if (Deleted)\n        {\n            from.SendLocalizedMessage(1042001); // That must be in your pack for you to use it.\n            return VariableCarpetResult.NotInPack;'),
    # one-floor check gone
    'm-floors.cs': ('        if (a.Z != b.Z)\n        {\n            from.SendMessage("Both corners', '        if (false)\n        {\n            from.SendMessage("Both corners'),
    # the cap ignores the setting
    'm-cap.cs': ('Math.Max(MinSide, MaxSideOverride ?? ServerConfiguration.GetOrUpdateSetting(MaxSideKey, DefaultMaxSide))', '100'),
    # the minimum gone
    'm-min.cs': ('        if (width < MinSide || height < MinSide)\n        {\n            return VariableCarpetResult.TooSmall;', '        if (false)\n        {\n            return VariableCarpetResult.TooSmall;'),
    # anyone may roll it up
    'm-owner.cs': ('public bool CanRemove(Mobile from) => !Deleted && BaseHouse.FindHouseAt(this)?.IsOwner(from) == true;', 'public bool CanRemove(Mobile from) => !Deleted;'),
    # the confirm is skipped: a double-click rolls it up at once
    'm-confirm.cs': ('        from.SendGump(new VariableCarpetRemoveGump(this));', '        TryRemove(from);'),
    # no range check on taking it up
    'm-range.cs': ('    public bool IsNear(Mobile from)\n    {', '    public bool IsNear(Mobile from)\n    {\n        return true;'),
    # the hue is not applied
    'm-hue.cs': ('{ Hue = VariableCarpetSettings.HueAt(hueIndex) }', '{ Hue = 0 }'),
    # the house's addon list is not told
    'm-houselist.cs': ('        house.Addons.Add(addon);\n        Delete();', '        Delete();'),
    # the middle is laid as border
    'm-layout.cs': ('            _                   => Middle', '            _                   => NorthCorner'),
}

for name, (old, new) in MUTANTS.items():
    if src.count(old) != 1:
        sys.exit(f'{name}: anchor found {src.count(old)} times')
    open(os.path.join(RED, name), 'w', encoding='utf-8', newline='\n').write(src.replace(old, new))
    print('wrote', name)
