"""cc-P708: GuildHallPlacementVerification fact 2: the League's headquarters is placed with its steward (LeagueSteward),
not Elara (LeagueRegistrar), who stays in New Haven. Each replaced text must occur exactly once.
    python -P edit_placement_fact.py
"""
P = 'D:/UO/golems/Iron/ShatteredLegacy/server/tests/Misc/GuildHallPlacementVerification.cs'
s = open(P, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s else '\n'


def rep(old, new):
    global s
    old, new = old.replace('\n', NL), new.replace('\n', NL)
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


rep("""//   2. Every hall is a guild (the League apart), placed with that guild's own guildmaster type; every guild but the""",
    """//   2. Every hall is a guild (the League apart, placed with its steward: cc-P708), placed with that guild's own
//      guildmaster type; every guild but the""")
rep("""            if (h.Key == "league")
            {
                Assert.Equal(typeof(LeagueRegistrar), h.NpcType);""", """            if (h.Key == "league")
            {
                // cc-P708: the headquarters at Valunstead has its own steward; Elara stays in New Haven
                Assert.Equal(typeof(LeagueSteward), h.NpcType);""")
open(P, 'w', encoding='utf-8', newline='').write(s)
print('ok')
