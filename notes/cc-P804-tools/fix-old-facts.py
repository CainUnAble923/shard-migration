# cc-P804: the existing facts this change moves, on both copies. Each states a thing that is now different by design.
import re
for R in ['D:/UO/golems/Iron/ShatteredLegacy/', 'D:/UO/golems/Iron/p804-isle/']:
    T = R + 'server/tests/'

    def edit(path, fn):
        s = open(T + path, encoding='utf-8', newline='').read()
        n = fn(s)
        assert n != s, path
        open(T + path, 'w', encoding='utf-8', newline='').write(n)

    def trial(s):
        s = s.replace('[InlineData("gathering.camping", SkillName.Camping, typeof(Kindling), 0)]', '[InlineData("gathering.camping", SkillName.Camping, typeof(Kindling), 1)] // cc-P804: the wild garlic')
        nl = '\r\n' if '\r\n' in s else '\n'
        a = '        p.Pm.AddToBackpack(ore);' + nl + '        Roll(p, skill);' + nl + '        Assert.Contains(key, p.Record.StationsDone);'
        b = ('        p.Pm.AddToBackpack(ore);' + nl + '        Roll(p, skill);' + nl +
             '        if (key == "gathering.camping")' + nl + '        {' + nl +
             '            Assert.DoesNotContain(key, p.Record.StationsDone); // cc-P804: the garlic is still to pick' + nl +
             '            Assert.True(p.Pm.Skills[SkillName.Herbalism].Value >= 30.0);' + nl +
             '            Roll(p, SkillName.Herbalism);' + nl + '        }' + nl + nl +
             '        Assert.Contains(key, p.Record.StationsDone);')
        assert a in s
        return s.replace(a, b)

    edit('Tutorial/TutorialTradeTrialVerification.cs', trial)
    edit('Misc/TwoHundredCapVerification.cs', lambda s: s.replace('Assert.Equal(11600.0, ClusterFSkillCaps.TotalSkillCap);', 'Assert.Equal(SkillInfo.Table.Length * 200.0, ClusterFSkillCaps.TotalSkillCap);'))
    edit('Misc/AlembicGuildVerification.cs', lambda s: s.replace('Assert.Equal(new[] { SkillName.Alchemy, SkillName.TasteID }, GuildSkillTable.For(ClusterFAlembicGuild.Key));', 'Assert.Equal(new[] { SkillName.Alchemy, SkillName.TasteID, SkillName.Herbalism }, GuildSkillTable.For(ClusterFAlembicGuild.Key));'))

    def counts(s):
        s = re.sub(r'Assert\.Equal\((\d+), defs\.Count\);', lambda m: 'Assert.Equal(%d, defs.Count); // cc-P804: Green Thumb;' % (int(m.group(1)) + 1), s, 1)
        return re.sub(r'Assert\.Equal\((\d+) - RetiredKeys\.Length, total\);', lambda m: 'Assert.Equal(%d - RetiredKeys.Length, total);' % (int(m.group(1)) + 1), s, 1)

    edit('Misc/AchievementEarnedLineVerification.cs', counts)
print('ok')
