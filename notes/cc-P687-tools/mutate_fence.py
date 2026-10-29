"""cc-P687: a mutant SosFenceRegions.cs for the C# facts' red run: every rule switched off (steps, landings and travel
allowed, housing allowed), the rooster island's turn-back spot inside its own fence and its box one tile short.
Usage: python -I mutate_fence.py <SosFenceRegions.cs> <out>"""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
for a, b in [
    ("        if (IsHeldBack(m) && !OnBoatAt(Map, newLocation))", "        if (false)"),
    ("        return OnBoatAt(Map, from) || !InAnyFence(from.X, from.Y) ? from : Spec.TurnBack;", "        return null;"),
    ("            case TravelCheckType.RecallTo or TravelCheckType.GateTo or TravelCheckType.Mark or TravelCheckType.TeleportTo\n                when endsInside:",
     "            case TravelCheckType.RecallTo or TravelCheckType.GateTo or TravelCheckType.Mark or TravelCheckType.TeleportTo\n                when false:"),
    ("    public override bool AllowHousing(Mobile from, Point3D p) => false;", "    public override bool AllowHousing(Mobile from, Point3D p) => true;"),
    ("[(2840, 1324, 3039, 1523)], new Point3D(2665, 1148, -1)", "[(2840, 1324, 3038, 1523)], new Point3D(2900, 1400, 0)"),
]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2])
