"""cc-P741: TutorialFarm.cs and TutorialCorePlacement.cs for the farm moved (run once)."""
p = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/TutorialFarm.cs'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)


rep('''        /// End points exclusive (Rectangle2D): x 6696-6712, y 3968-3982.''',
    '''        /// End points exclusive (Rectangle2D): x 6678-6694, y 3968-3982 (cc-P741: 18 west of P720's).''')
rep('''        /// cc-P718: the field's gate, in the two-tile gap of its east fence (6713, 3978-3979; the layout leaves it open).''',
    '''        /// cc-P718: the field's gate, in the two-tile gap of its east fence (6695, 3978-3979 since cc-P741; the layout leaves
        /// it open).''')
rep('''        public static readonly Point2D[] FieldGateSpots = [new(6713, 3979)];

        public static readonly Point2D FieldFenceSpot = new(6713, 3978);''',
    '''        public static readonly Point2D[] FieldGateSpots = [new(6695, 3979)];

        public static readonly Point2D FieldFenceSpot = new(6695, 3978);

        /// <summary>
        /// cc-P741 (Chase 10-30: "farm house should be east of farm and farm shifts west so no doubling back"): the field
        /// moved 18 tiles west and the farmhouse 12 east. These are where their pieces stood before (P720/P726), which the
        /// seeder clears from a world laid then: the gate and the fence piece by it, Pip's bench and blood, the pest and
        /// pen spawners (with what they spawned).
        /// </summary>
        public const int FieldMovedX = -18;
        public const int HouseMovedX = 12;
        public static readonly Point2D OldFieldGateSpot = new(6713, 3979);
        public static readonly Point2D OldFieldFenceSpot = new(6713, 3978);
        public static readonly Point2D OldPestSpot = new(PestSpot.X - FieldMovedX, PestSpot.Y);
        public static readonly Point2D OldPenSpot = new(PenSpot.X - FieldMovedX, PenSpot.Y);''')
rep('''        public static readonly Point2D PipSpot = new(6692, 3975);
        public static readonly Point3D PipBench = new(6692, 3975, 7);
        public static readonly Point2D OldPipSpot = new(6715, 3981); // cc-P721's, by the barrel south of the gate''',
    '''        public static readonly Point2D PipSpot = new(6704, 3975);
        public static readonly Point3D PipBench = new(6704, 3975, 7);
        public static readonly Point2D OldPipSpot = new(6715, 3981); // cc-P721's, by the barrel south of the gate
        public static readonly Point3D OldPipBench = new(6692, 3975, 7); // cc-P726's, before the farmhouse moved (cc-P741)''')
rep('''            (BenchId, new Point3D(6692, 3975, 7), "wooden bench"),
            (BenchId, new Point3D(6692, 3976, 7), "wooden bench"),
            (0x122A, new Point3D(6691, 3975, 7), "blood"),
            (0x122D, new Point3D(6691, 3976, 7), "blood"),
            (0x122C, new Point3D(6691, 3974, 7), "blood")
        ];''',
    '''            (BenchId, new Point3D(6704, 3975, 7), "wooden bench"),
            (BenchId, new Point3D(6704, 3976, 7), "wooden bench"),
            (0x122A, new Point3D(6703, 3975, 7), "blood"),
            (0x122D, new Point3D(6703, 3976, 7), "blood"),
            (0x122C, new Point3D(6703, 3974, 7), "blood")
        ];

        /// <summary>cc-P741: Pip's props where they stood before the farmhouse moved (cc-P726's), removed by the seeder.</summary>
        public static readonly (int Id, Point3D At, string Name)[] OldPipProps =
            PipProps.Select(p => (p.Id, new Point3D(p.At.X - HouseMovedX, p.At.Y, p.At.Z), p.Name)).ToArray();''')
rep('''            foreach (var at in new[] { PipBench, TutorialWorld.Ground(map, OldPipSpot) })''',
    '''            foreach (var at in new[] { PipBench, OldPipBench, TutorialWorld.Ground(map, OldPipSpot) })''')
rep('''            // cc-P720: a farm laid with an older layout (P663's hillside farmhouse) is taken up, with its door, and laid again.
            if (FindAddon<TutorialIsleFarmAddon>(map, TutorialIsleFarmLayout.Anchor) is { } old && !IsCurrent(old))
            {
                if (!dryRun)
                {
                    old.Delete();
                    FindDoor(map, TutorialIsleFarmLayout.OldDoorSpot)?.Delete();
                }''',
    '''            // cc-P741: a farm laid before the field and the farmhouse swapped sides: its gate, fence piece, Pip's props and
            // spawners go, and Wren, Tobin and Pip walk to their new spots (the farm addon itself is relaid just below)
            if (!dryRun) { MoveFromOldLayout(map); }

            // cc-P720: a farm laid with an older layout (P663's hillside farmhouse) is taken up, with its door, and laid again.
            if (FindAddon<TutorialIsleFarmAddon>(map, TutorialIsleFarmLayout.Anchor) is { } old && !IsCurrent(old))
            {
                if (!dryRun)
                {
                    old.Delete();
                    foreach (var spot in TutorialIsleFarmLayout.OldDoorSpots) { FindDoor(map, spot)?.Delete(); }
                }''')
rep('''        /// <summary>New Haven's farm props for the wing trials: the farm addon, its door and the pen (no Wren, no pests).</summary>''',
    '''        /// <summary>
        /// cc-P741: clears what a farm laid before the move left where the field and the farmhouse used to be, and walks the
        /// farm's people to their new spots. Idempotent: on a world laid since, it finds nothing. Returns how many things it
        /// removed or moved.
        /// </summary>
        public static int MoveFromOldLayout(Map map)
        {
            var gone = new List<Item>();
            if (FindDoor(map, TutorialWorld.Ground(map, OldFieldGateSpot)) is TutorialPestGate oldGate) { gone.Add(oldGate); }
            foreach (var item in map.GetItemsInRange<Static>(TutorialWorld.Ground(map, OldFieldFenceSpot), 0))
            {
                if (!item.Deleted && item.ItemID == FieldFenceId) { gone.Add(item); }
            }

            foreach (var (id, at, name) in OldPipProps)
            {
                foreach (var i in map.GetItemsInRange<Static>(at, 0))
                {
                    if (!i.Deleted && i.ItemID == id && i.Z == at.Z && i.Name == name) { gone.Add(i); }
                }
            }

            foreach (var (spot, now, types) in new[] { (OldPestSpot, PestSpot, PestTypes), (OldPenSpot, PenSpot, PenTypes) })
            {
                if (FindSpawner(map, spot, types[0]) is { } s && FindSpawner(map, now, types[0]) != s)
                {
                    gone.Add(s); // BaseSpawner.OnDelete removes what it spawned
                }
            }

            foreach (var i in gone) { i.Delete(); }

            var moved = 0;
            foreach (var (m, spot) in new (Mobile? M, Point2D Spot)[]
                     {
                         (FindNear<TutorialFarmhand>(map, FarmhandSpot), FarmhandSpot),
                         (FindNear<TutorialVeterinarian>(map, FarmVetSpot), FarmVetSpot)
                     })
            {
                if (m != null && (m.X != spot.X || m.Y != spot.Y))
                {
                    var at = TutorialWorld.Ground(map, spot);
                    if (m is BaseCreature bc) { bc.Home = at; }
                    m.MoveToWorld(at, map);
                    moved++;
                }
            }

            if (FindPip(map) is { } pip && pip.Location != PipBench)
            {
                pip.Home = PipBench;
                pip.Direction = Direction.West;
                pip.MoveToWorld(PipBench, map);
                moved++;
            }

            return gone.Count + moved;
        }

        /// <summary>The first <typeparamref name="T"/> within 30 tiles of <paramref name="spot"/> (the whole farm), or null.</summary>
        private static T? FindNear<T>(Map map, Point2D spot) where T : Mobile
        {
            foreach (var m in map.GetMobilesInRange(new Point3D(spot.X, spot.Y, 0), 30))
            {
                if (m is T t && !t.Deleted) { return t; }
            }

            return null;
        }

        /// <summary>New Haven's farm props for the wing trials: the farm addon, its door and the pen (no Wren, no pests).</summary>''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)

p = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/TutorialCorePlacement.cs'
s = open(p, encoding='utf-8').read()
rep('''        "core.healing" => Ground(new Point2D(6690, 3979)), // the farmhouse door's step''',
    '''        "core.healing" => Ground(new Point2D(6702, 3979)), // the farmhouse door's step (cc-P741: the farmhouse moved east)''')
rep('''        if (!dryRun) { MoveOldMarkers(map); } // cc-P720: a rune on its stop becomes the sign beside it''',
    '''        if (!dryRun) { MoveOldMarkers(map); } // cc-P720: a rune on its stop becomes the sign beside it
        if (!dryRun) { TutorialFarm.MoveFromOldLayout(map); } // cc-P741: Tobin moved before he is looked for''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
