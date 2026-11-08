r"""cc-P817, the isle release only (release/isle-20261028 has no P714 start rules, ClusterFStartChoices): the trade choice,
the stock Blacksmith (profession 3), refused by NewCharacterRules and CharacterCreation; the package's Prof.txt copy
leaves out only that entry (the release still offers Necromancer, Paladin, Samurai and Ninja); the facts read the
release's own list.

    python -P isle_profession.py <isle code copy>
"""
import sys

root = sys.argv[1]


def edit(rel, reps, enc='utf-8'):
    p = root + '/' + rel
    s = open(p, encoding=enc, newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    for a, b in reps:
        a, b = a.replace('\n', nl), b.replace('\n', nl)
        assert s.count(a) == 1, (rel, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding=enc, newline='').write(s)


edit('server/customizations/Tutorial/NewCharacterRules.cs', [
    ("""    /// <summary>GameMaster and up: neither lock applies.</summary>""",
     """    /// <summary>
    /// cc-P817 (the isle release; Chase 2026-11-07: "I also want to remove the trade choice"): the stock Blacksmith
    /// (profession 3: Blacksmithy, Tailoring, Tinkering and Mining at 30) is not offered. The player package's Prof.txt
    /// copy leaves it off the creation screen (Build-UoOverrides.ps1, $ProfRemoved), and a client that asks for it anyway
    /// (an old package, a third-party client) makes no character (CharacterCreation.OnCharacterCreated). Main refuses
    /// the same number as P714's Maker (ClusterFStartChoices.RemovedProfessions). Staff are exempt.
    /// </summary>
    public static readonly int[] RefusedProfessions = [3];

    public static bool ProfessionRefused(IAccount? account, int profession) =>
        !IsExempt(account) && Array.IndexOf(RefusedProfessions, profession) >= 0;

    /// <summary>GameMaster and up: neither lock applies.</summary>"""),
])

edit('server/customizations/CharacterCreation.cs', [
    ("""        // cc-P762: only the races newCharacters.races allows (Human, for now); any other is made Human, with a line once""",
     """        // cc-P817 (isle release): the trade choice, the stock Blacksmith, makes no character; the client is told
        // "Character creation blocked." (pinned's handler for a null Mobile) and the log says why.
        if (Server.Tutorial.NewCharacterRules.ProfessionRefused(args.Account, args.Profession))
        {
            logger.Information("Login: {NetState}: Character creation refused (account={Account}): profession {Profession} (the Blacksmith) is no longer offered",
                state, args.Account?.Username, args.Profession);
            args.Mobile = null;
            return;
        }

        // cc-P762: only the races newCharacters.races allows (Human, for now); any other is made Human, with a line once"""),
])

edit('player-package/payload/app/Build-UoOverrides.ps1', [
    ("""# cc-P817: the professions the server refuses at creation (ClusterFStartChoices.RemovedProfessions), by Desc number:
# 3 Blacksmith (the shard's Maker: Chase's "trade choice"), 4 Necromancer, 5 Paladin, 6 Samurai, 7 Ninja.
$ProfRemoved = @(3, 4, 5, 6, 7)""",
     """# cc-P817: the professions the server refuses at creation, by Desc number. On the isle release that is the stock
# Blacksmith alone (Chase's "trade choice"; server\\customizations\\Tutorial\\NewCharacterRules.cs, RefusedProfessions).
$ProfRemoved = @(3)"""),
    ("""       (server\\customizations\\ClusterFStartChoices.cs, RemovedProfessions), so the screen offers only what is made.""",
     """       (isle release: server\\customizations\\Tutorial\\NewCharacterRules.cs, RefusedProfessions), so the screen offers only what is made."""),
], enc='ascii')

edit('player-package/tests/Prof-Overrides.Tests.ps1', [
    ("""$startCs = Join-Path $repo 'server\\customizations\\ClusterFStartChoices.cs'""",
     """$startCs = Join-Path $repo 'server\\customizations\\Tutorial\\NewCharacterRules.cs'   # the isle release's list"""),
    ("""    $want = $header + (Block 'Warrior' 1) + (Block 'Mage' 2)
    Assert-Equal $want ([IO.File]::ReadAllText($copy)) 'Warrior and Mage, as they were; the trade (Blacksmith) and the four schools gone'""",
     """    $want = $header + (Block 'Samurai' 6) + (Block 'Ninja' 7) + (Block 'Paladin' 5) + (Block 'Necromancer' 4) + (Block 'Warrior' 1) + (Block 'Mage' 2)
    Assert-Equal $want ([IO.File]::ReadAllText($copy)) 'every profession as it was but the trade (Blacksmith), gone (the isle release offers the rest)'"""),
    ("""    $cs = [IO.File]::ReadAllText($startCs)
    $ids = @{}
    foreach ($m in [regex]::Matches($cs, 'public const int (\\w+)Id = (\\d+);')) { $ids[$m.Groups[1].Value] = [int]$m.Groups[2].Value }
    $names = [regex]::Match($cs, 'RemovedProfessions = \\[([^\\]]*)\\]').Groups[1].Value.Split(',') | ForEach-Object { $_.Trim() -replace 'Id$', '' }
    $server = @($names | ForEach-Object { $ids[$_] } | Sort-Object)
    Assert-Equal ($server -join ',') ($client -join ',') 'Build-UoOverrides.ps1 and ClusterFStartChoices.cs'""",
     """    $cs = [IO.File]::ReadAllText($startCs)
    $server = @([regex]::Match($cs, 'RefusedProfessions = \\[([^\\]]*)\\]').Groups[1].Value.Split(',') | ForEach-Object { [int]$_.Trim() } | Sort-Object)
    Assert-Equal ($server -join ',') ($client -join ',') 'Build-UoOverrides.ps1 and NewCharacterRules.cs'"""),
], enc='utf-8')

edit('server/tests/Tutorial/TutorialIsleVerification.cs', [
    ("""    // Item 2: the trade choice (the client's Blacksmith, the shard's Maker template, profession 3) makes no character.
    [Fact]
    public void P817_TheTradeProfessionIsRefused()
    {
        Assert.Null(ClusterFStartChoices.Resolve(3, [], [60, 15, 15], Race.Human, true, out var why));
        Assert.Contains("no longer offered", why);
        Assert.NotNull(ClusterFStartChoices.Resolve(1, [], [45, 35, 10], Race.Human, true, out _)); // the Fighter still is
        Assert.NotNull(ClusterFStartChoices.Resolve(2, [], [25, 20, 45], Race.Human, true, out _)); // and the Mage
    }""",
     """    // Item 2 (isle release): the trade choice, the stock Blacksmith (profession 3), makes no character; staff are exempt.
    [Fact]
    public void P817_TheTradeProfessionIsRefused()
    {
        using var t = new Trainees();
        Assert.True(NewCharacterRules.ProfessionRefused(t.Account, 3));
        Assert.False(NewCharacterRules.ProfessionRefused(t.Account, 1)); // the Warrior still is
        Assert.False(NewCharacterRules.ProfessionRefused(t.Account, 2)); // and the Mage
        var staff = new Account($"p817s{Guid.NewGuid():N}"[..16], "p817-test-only") { AccessLevel = AccessLevel.GameMaster };
        try
        {
            Assert.False(NewCharacterRules.ProfessionRefused(staff, 3));
        }
        finally
        {
            staff.Delete();
        }
    }"""),
])
print('ok')
