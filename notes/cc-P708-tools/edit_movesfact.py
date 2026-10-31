"""cc-P708: GuildHallSosMovesVerification fact 4 uses a real account (AlembicGuildVerification's pattern)."""
P = 'D:/UO/golems/Iron/ShatteredLegacy/server/tests/Misc/GuildHallSosMovesVerification.cs'
s = open(P, encoding='utf-8').read()
old = """        var pm = new PlayerMobile();
        try
        {
            pm.Account = new TestAccount();
            foreach"""
new = """        var account = new Account($"p708{Guid.NewGuid():N}"[..16], "p708-test-only");
        var pm = new PlayerMobile { Player = true, Race = Race.Human };
        pm.AddItem(new Backpack());
        account[0] = pm;
        pm.MoveToWorld(new Point3D(3660, 2552, 0), Map.Trammel);
        try
        {
            foreach"""
assert s.count(old) == 1
s = s.replace(old, new)
old = """        finally
        {
            pm.Delete();
        }
    }
}"""
new = """        finally
        {
            pm.Delete();
            Accounts.Remove(account);
        }
    }
}"""
assert s.count(old) == 1
s = s.replace(old, new)
s = s.replace("using Server;\nusing Server.Items;", "using Server;\nusing Server.Accounting;\nusing Server.Items;")
assert 'using Server.Accounting;' in s
open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
