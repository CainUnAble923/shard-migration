"""cc-P677 (S8 item 1): Blackthorn off on the Siege of Sosaria land, its code kept for P691 (the Fold's zone 5).
BlackthornRegions.OnThisLand (false) gates the start-up registration of both regions and the [GenBlackthorn command;
Register(map), Generate() and Delete() stay as they are for the facts and for P691."""
import os

BS = chr(92)
D = BS.join(['D:', 'UO', 'golems', 'Iron', 'ShatteredLegacy', 'server', 'customizations', 'Services', 'Revamped Dungeons',
             'BlackthornDungeon'])


def edit(name, old, new):
    p = os.path.join(D, name)
    s = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    old, new = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(old) == 1, (name, s.count(old))
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
    print('ok', name)


edit('Region.cs',
     '''    private static readonly Dictionary<Map, BlackthornDungeon> _dungeons = new();
    private static BlackthornCastle _castle;

    public static void Initialize()
    {
        Register(Map.Trammel);
''',
     '''    private static readonly Dictionary<Map, BlackthornDungeon> _dungeons = new();
    private static BlackthornCastle _castle;

    /// <summary>
    ///     cc-P677 (SoS swap S8): off. On the Siege of Sosaria land the dungeon's area (DungeonBounds) holds the author's
    ///     own dungeons and the castle's is his town, so neither region registers at start and [GenBlackthorn refuses.
    ///     The code stays whole for P691, which moves Blackthorn into the Fold's zone 5 and turns this on there.
    /// </summary>
    public static bool OnThisLand { get; set; }

    public static void Initialize()
    {
        if (!OnThisLand)
        {
            return;
        }

        Register(Map.Trammel);
''')

edit('Generate.cs',
     '''    public static void Generate_OnCommand(CommandEventArgs e)
    {
        var deleted = Delete();
''',
     '''    public static void Generate_OnCommand(CommandEventArgs e)
    {
        if (!BlackthornRegions.OnThisLand)
        {
            // cc-P677: its area is the author's dungeons on the Siege of Sosaria land; P691 moves it into the Fold.
            e.Mobile.SendMessage("Blackthorn Dungeon is off on this land until it moves into the Fold (P691). Nothing placed.");
            return;
        }

        var deleted = Delete();
''')
