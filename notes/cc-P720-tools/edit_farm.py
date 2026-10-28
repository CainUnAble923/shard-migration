"""cc-P720 items 1-2: TutorialFarm.cs. A farm laid with an older layout is replaced (its addon and its door); the isle's
farmhouse door is the cottage's (south wall, WestCW)."""
import sys

p = sys.argv[1] + '/server/customizations/Tutorial/TutorialFarm.cs'
s = open(p, encoding='utf-8').read()


def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:80], s.count(old))
    s = s.replace(old, new)


rep('''            if (FindAddon<TutorialIsleFarmAddon>(map, TutorialIsleFarmLayout.Anchor) is { } placed)
            {
                present++;
                if (!dryRun) { FixGateSign(placed); } // cc-P718
            }
            else''', '''            // cc-P720: a farm laid with an older layout (P663's hillside farmhouse) is taken up, with its door, and laid again.
            if (FindAddon<TutorialIsleFarmAddon>(map, TutorialIsleFarmLayout.Anchor) is { } old && !IsCurrent(old))
            {
                if (!dryRun)
                {
                    old.Delete();
                    FindDoor(map, TutorialIsleFarmLayout.OldDoorSpot)?.Delete();
                }

                addons++;
                if (!dryRun) { new TutorialIsleFarmAddon().MoveToWorld(TutorialIsleFarmLayout.Anchor, map); }
            }
            else if (FindAddon<TutorialIsleFarmAddon>(map, TutorialIsleFarmLayout.Anchor) is { } placed)
            {
                present++;
                if (!dryRun) { FixGateSign(placed); } // cc-P718
            }
            else''')

rep('''                if (!dryRun) { MakeDoor().MoveToWorld(TutorialIsleFarmLayout.DoorSpot, map); }''',
    '''                if (!dryRun) { MakeIsleDoor().MoveToWorld(TutorialIsleFarmLayout.DoorSpot, map); }''')

rep('''        public static BaseDoor MakeDoor() => new DarkWoodDoor(DoorFacing.SouthCW);
''', '''        public static BaseDoor MakeDoor() => new DarkWoodDoor(DoorFacing.SouthCW);

        /// <summary>cc-P720: the isle farmhouse's door, in the cottage's south wall (OSI's 0x06A5 there).</summary>
        public static BaseDoor MakeIsleDoor() => new DarkWoodDoor(DoorFacing.WestCW);

        /// <summary>
        /// cc-P720: true when <paramref name="addon"/> holds exactly today's layout (art and offsets; the gate sign as the
        /// addon lays it). A farm laid before (P663's hillside farmhouse) is not.
        /// </summary>
        public static bool IsCurrent(BaseAddon addon)
        {
            var a = TutorialIsleFarmLayout.Anchor;
            var wanted = TutorialIsleFarmLayout.Pieces.Where(p => IsleArt(p.Id) != null)
                .Select(p => (IsleArt(p.Id)!.Value, p.X - a.X, p.Y - a.Y, p.Z - a.Z)).OrderBy(t => t).ToList();
            var placed = addon.Components.Select(c => (c.ItemID, c.Offset.X, c.Offset.Y, c.Offset.Z)).OrderBy(t => t).ToList();
            return wanted.SequenceEqual(placed);
        }
''')

rep('using System.Collections.Generic;\n', 'using System.Collections.Generic;\nusing System.Linq;\n')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('edited', p)
