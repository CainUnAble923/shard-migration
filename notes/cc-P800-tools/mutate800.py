# cc-P800: one deliberate break per behaviour, each written as changed sources under notes/cc-P800-tools/mutants/<name>/.
# run-mutants.sh builds each in one container and runs the sash facts. Each must turn a fact red; see mutants.txt.
import os, shutil
S = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/'
OUT = 'D:/UO/golems/Iron/shard-migration/notes/cc-P800-tools/mutants/'
SASH = ('LeagueShop/LeagueSash.cs', 'LeagueShop')
LOOP = ('Tutorial/ClusterFLoops.cs', 'Tutorial')
ACH = ('ClusterFAchievements.cs', 'Misc')
ROLL = ('LootBoxes/LootBoxRoller.cs', 'LootBoxes')
ITEMS = ('LootBoxes/LootBoxItems.cs', 'LootBoxes')
GUMP = ('LeagueRegistrarGump.cs', 'Misc')
M = {
 'rank-not-checked': (SASH, 'if (ClusterFLeagueRanks.GetRank(pm) < table.RankNeeded(next))', 'if (false)'),
 'fee-not-charged': (SASH, 'if (Data(pm)?.SpendRenown(fee) != true)', 'if (Data(pm) == null)'),
 'stale-page-pays': (SASH, 'if (step != fromStep)', 'if (false)'),
 'second-sash-issued': (SASH, 'if (Find(pm) != null)\r\n            {\r\n                message = "You already', 'if (false)\r\n            {\r\n                message = "You already'),
 'unregistered-issued': (SASH, 'if (ClusterFLeagueRanks.GetRank(pm) <= 0)', 'if (false)'),
 'lost-back-at-zero': (SASH, 'var sash = Create(pm, StepOf(pm));', 'var sash = Create(pm, 0);'),
 'first-hue-wrong': (SASH, 'Hue = LeagueSashTable.Current.HueOf(Step);', 'Hue = LeagueSashTable.Current.HueOf(Math.Max(1, Step));'),
 'convert-no-keepsake': (SASH, 'if (Has(pm))\r\n            {\r\n                item.Label = KeepsakeLabel;', 'if (false)\r\n            {\r\n                item.Label = KeepsakeLabel;'),
 'convert-moves-to-pack': (SASH, 'pack.AddItem(sash);\r\n                sash.Location = at;', 'pm.Backpack.DropItem(sash);'),
 'load-ignores-account': (SASH, 'return pm != null && AccountBinding.SameAccount(pm, item.BoundAccount);', 'return pm != null;'),
 'login-no-pass': (SASH, 'if (IsOld(item) && HeldByItsAccount(item, out _) && Convert(item, pm))', 'if (false)'),
 'login-converts-any': (SASH, 'if (IsOld(item) && HeldByItsAccount(item, out _) && Convert(item, pm))', 'if (HeldByItsAccount(item, out _) && Convert(item, pm))'),
 'lift-by-anyone': (SASH, 'if (from.AccessLevel < AccessLevel.GameMaster && !IsOwner(from))', 'if (false)'),
 'not-blessed': (SASH, 'LootType = LootType.Blessed;', 'LootType = LootType.Regular;'),
 'loop-resets-step': (LOOP, 'LeagueSashSystem.Refresh(pm);', 'LeagueSashSystem.Find(pm)?.SetStep(0);'),
 'bonus-when-carried': (SASH, 'pm?.FindItemOnLayer(Layer.MiddleTorso) is LeagueSash sash && sash.IsOwner(pm) ? LeagueSashTable.Current.BonusOf(sash.Step) : 0;', 'Find(pm) is { } sash ? LeagueSashTable.Current.BonusOf(sash.Step) : 0;'),
 'bonus-on-commission': (SASH, 'source is RenownSource.Achievement or RenownSource.LeagueJob ? WornBonus(pm) : 0', 'WornBonus(pm)'),
 'carry-dropped': (SASH, '(hundredths % 100).ToString(', '(0).ToString('),
 'file-bonus-unchecked': (SASH, 'ReadInt(el, "bonusPercent", 0, 100, where, errors)', 'ReadInt(el, "bonusPercent", 0, 1000, where, errors)'),
 'file-order-unchecked': (SASH, 'else if (rank.Index <= lastRank)', 'else if (false)'),
 'box-always-gives': (SASH, 'public static bool BoxMayGive(PlayerMobile pm) => !Has(pm);', 'public static bool BoxMayGive(PlayerMobile pm) => true;'),
 'box-open-no-convert': (ITEMS, 'item = LeagueSashSystem.FromBox(pm, item);', ''),
 'step-not-saved': (SASH, '[SerializableField(1, setter: "private")]\r\n        private int _step;', 'public int Step { get; private set; }'),
 'achievement-no-bonus': (ACH, 'LeagueSashSystem.Earn(data, OnlineCharacter(acct), def.Renown, RenownSource.Achievement);', 'data.GrantRenown(def.Renown, RenownSource.Achievement);'),
 'menu-row-missing': (GUMP, 'AddButton(230, y, 4011, 4012, BtnSash);', ''),
}
ONLY = ('convert-no-keepsake', 'convert-moves-to-pack', 'load-ignores-account', 'login-no-pass', 'login-converts-any')
M = {k: v for k, v in M.items() if k in ONLY}
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
for name, ((rel, dest), a, b) in M.items():
    s = open(S + rel, encoding='utf-8', newline='').read()
    if '\r\n' not in s:
        a = a.replace('\r\n', '\n'); b = b.replace('\r\n', '\n')
    assert s.count(a) == 1, (name, s.count(a))
    d = OUT + name + '/' + dest
    os.makedirs(d)
    open(d + '/' + os.path.basename(rel), 'w', encoding='utf-8', newline='').write(s.replace(a, b))
    open(OUT + name + '/target', 'w').write(dest + '/' + os.path.basename(rel))
print(len(M), 'mutants')
