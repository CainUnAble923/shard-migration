"""cc-P708: fact 4 sets the password algorithm before making its account (as AlembicGuildVerification does); it passed
in the full run only because an earlier fact had set it."""
P = 'D:/UO/golems/Iron/ShatteredLegacy/server/tests/Misc/GuildHallSosMovesVerification.cs'
s = open(P, encoding='utf-8').read()
old = """        var account = new Account($"p708{Guid.NewGuid():N}"[..16], "p708-test-only");"""
new = """        if (AccountSecurity.CurrentAlgorithm == PasswordProtectionAlgorithm.None)
        {
            AccountSecurity.CurrentAlgorithm = PasswordProtectionAlgorithm.PBKDF2;
        }

        var account = new Account($"p708{Guid.NewGuid():N}"[..16], "p708-test-only");"""
assert s.count(old) == 1
s = s.replace(old, new)
old = "using Server.Accounting;\n"
assert s.count(old) == 1
s = s.replace(old, "using Server.Accounting;\nusing Server.Accounting.Security;\n")
open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
