"""cc-P22 red run: one deliberate break per fact, every file restored byte-identical afterwards (SHA-256).

    python mutate.py apply     back up, record hashes, apply every mutation
    python mutate.py restore   put the originals back and check the hashes
"""
import hashlib, json, os, shutil, subprocess, sys

R = r'D:\ShatteredLegacy'
HERE = os.path.dirname(os.path.abspath(__file__))
BACK = os.path.join(HERE, 'red-backup')
MANIFEST = os.path.join(BACK, 'manifest.json')

# (file, old, new, what it breaks)
M = [
    # F-16: the old T1 voucher price.
    (r'server\customizations\MinersCompactLiaisonGump.cs',
     'internal const int RestoreVoucherCost = 1;', 'internal const int RestoreVoucherCost = 5; // P22 RED',
     'F16 a/b: T1 charges the old 5 vouchers'),
    (r'server\customizations\MinersCompactLiaisonGump.cs',
     'internal const int RestoreT2GoldCost       = 1000;', 'internal const int RestoreT2GoldCost       = 5000; // P22 RED',
     'F16 a (T2): the old T2 gold price'),
    (r'server\customizations\MinersCompactLiaisonGump.cs',
     'if (!Items.DevTestingCrystal.IsActive(_pm) && !TryPay(guild, GetRestoreCost(tier)))\n            return;',
     'if (!Items.DevTestingCrystal.IsActive(_pm)) TryPay(guild, GetRestoreCost(tier)); // P22 RED: refusal ignored',
     'F16 b: a refused payment still restores'),
    # F-19: the bank limit is pinned's 125, and Apply also writes the backpack.
    (r'server\customizations\ClusterFBankLimit.cs',
     'public static int GetMaxItems(Mobile owner) => BaseItems + LeagueRankBonus(owner);',
     'public static int GetMaxItems(Mobile owner) => Container.GlobalMaxItems; // P22 RED',
     'F19 1, 3: the bank stays at 125'),
    (r'server\customizations\ClusterFBankLimit.cs',
     '''        if (bank.MaxItems != limit)
        {
            bank.MaxItems = limit;
        }''',
     '''        if (bank.MaxItems != limit)
        {
            bank.MaxItems = limit;
        }

        if (m.Backpack != null) m.Backpack.MaxItems = 1000; // P22 RED''',
     'F19 2: the backpack is raised too'),
    # Thief: not seeded, no arrow, not invulnerable.
    (r'server\customizations\ClusterFGuildHallSeeder.cs',
     'foreach (var loc in GuildLocations.All.Concat(GuildLocations.Lookouts))',
     'foreach (var loc in GuildLocations.All.Concat(Array.Empty<GuildLocation>())) // P22 RED',
     'lookout 1: never placed'),
    (r'server\customizations\ThievesDenLookout.cs',
     'var told = ClusterFGuildStarter.ShowTheWay(pm, GuildKey);',
     'var told = "Follow the arrow (P22 RED, no arrow)";',
     'lookout 2: no arrow, and a missing guildmaster not reported'),
    (r'server\customizations\ThievesDenLookout.cs',
     'public override bool IsInvulnerable => true;', 'public override bool IsInvulnerable => false; // P22 RED',
     'lookout 3: can be attacked'),
    # F-11.
    (r'server\customizations\GuildResources.cs',
     'Walk(pm.FindBankNoCreate(), cost, list, bankLater);', '// P22 RED: the bank is not searched',
     'F11 1, 5, 6: pack only, as before F-11'),
    (r'server\customizations\GuildResources.cs',
     '(satchel ? inSatchel : loose).Add(item);', '(satchel ? loose : inSatchel).Add(item); // P22 RED',
     'F11 3, 6: satchels before loose'),
    (r'server\customizations\GuildResources.cs',
     'public static bool IsBlessed(Item item) => item.LootType == LootType.Blessed || item.BlessedFor != null;',
     'public static bool IsBlessed(Item item) => false; // P22 RED',
     'F11 4: blessed items taken'),
    (r'server\customizations\GuildResources.cs',
     '''            if (cost != null && cost.Amount > 0 && Count(pm, cost).Total < cost.Amount)
            {
                pm.SendMessage(0x22, ShortMessage(pm, cost));
                return false;
            }''',
     '''            if (cost != null && cost.Amount > 0 && Count(pm, cost).Total < cost.Amount)
            {
                pm.SendMessage(0x22, ShortMessage(pm, cost));
                return false;
            }

            TryConsume(pm, cost); // P22 RED: each material taken as it passes''',
     'F11 2: not all or nothing'),
    # F-17.
    (r'server\customizations\BODCombineContained.cs',
     '''        if (container != from.Backpack && !container.IsChildOf(from.Backpack))
        {''',
     '''        if (false) // P22 RED: any container
        {''',
     'F17 5: a bag in the bank feeds the deed'),
    (r'server\customizations\BODCombineContained.cs',
     '''            if (item.Deleted)
            {
                combined++;
            }''',
     '''            combined++; // P22 RED: counts every try''',
     'F17 3: the count is wrong'),
    (r'server\customizations\BODCombineContained.cs',
     'public const int ButtonID = 3;', 'public const int ButtonID = 4; // P22 RED',
     'F17 1, 2, 4: the gump button is not the one the response handles... (see patch mutation)'),
    # F-15.
    (r'server\customizations\ShardVersion.cs',
     'public static string Anchor(string version) => "version_" + version.Replace(".", "").Replace(":", "");',
     'public static string Anchor(string version) => "version_" + version; // P22 RED',
     'F15 1: the anchor keeps its dots'),
    (r'server\customizations\ShardVersion.cs',
     'return seen == CurrentNotes.Version ? null : CurrentNotes;', 'return CurrentNotes; // P22 RED',
     'F15 2: notes shown every login'),
    (r'server\customizations\ShardVersion.cs',
     '''        if (string.IsNullOrEmpty(markdown))
        {
            return versions;
        }''',
     '''        if (markdown.Length == 0) // P22 RED: null throws
        {
            return versions;
        }''',
     'F15 3: a missing changelog throws'),
    (r'server\customizations\ShardVersion.cs',
     'm.SendGump(new BulletinGump(m, new List<BulletinEntry>(), CurrentNotes));', '// P22 RED: no gump',
     'F15 4: [version shows no notes'),
    (r'server\customizations\ShardStatusPublisher.cs',
     'w.WriteString("version", version);', 'w.WriteNull("version"); // P22 RED',
     'F15 status.json: no version'),
    # The TCFill count is reported by failing on purpose (passing tests print nothing in build.sh's log).
    (r'server\tests\Misc\BankLimitVerification.cs',
     'Assert.True(bank.TotalItems > 0);',
     'Assert.Equal(-1, bank.TotalItems); // P22 RED: print the count',
     'F19 4: report the [TCFill count'),
]

# The patch: the one-item combine (button 2) is broken by the response branch the patch adds.
PATCH = r'server\patches\BOD-combine-contained.patch'
PATCH_OLD = '''+            else if (info.ButtonID == BODCombineContained.ButtonID) // Combine with contained items (F-17)
+            {
+                from.SendGump(new SmallBODGump(_deed));
+                BODCombineContained.Begin(from, _deed);
+            }'''


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def apply():
    os.makedirs(BACK, exist_ok=True)
    files = sorted({f for f, *_ in M} | {PATCH})
    manifest = {}
    for f in files:
        src = os.path.join(R, f)
        dst = os.path.join(BACK, f.replace('\\', '__'))
        shutil.copy2(src, dst)
        manifest[f] = sha(src)
    json.dump(manifest, open(MANIFEST, 'w'), indent=1)

    for f, old, new, what in M:
        p = os.path.join(R, f)
        s = open(p, newline='').read()
        assert s.count(old) == 1, (f, what)
        s = s.replace(old, new)
        open(p, 'w', newline='').write(s)
        print('applied:', what)

    # Patch mutation: the added branch swallows button 2 before pinned's own handler runs. Insert one + line at
    # the top of SmallBODGump.OnResponse's added block and fix the hunk's new-side count.
    p = os.path.join(R, PATCH)
    s = open(p, newline='').read()
    assert s.count(PATCH_OLD) == 1
    s = s.replace(PATCH_OLD, PATCH_OLD.replace(
        '+            else if (info.ButtonID == BODCombineContained.ButtonID)',
        '+            if (info.ButtonID == BODCombineContained.ButtonID || info.ButtonID == 2) // P22 RED'))
    open(p, 'w', newline='').write(s)
    print('applied: F17 6 (patch): button 2 also opens the contained-combine cursor, replacing the one-item one')


def restore():
    manifest = json.load(open(MANIFEST))
    ok = True
    for f, h in manifest.items():
        src = os.path.join(BACK, f.replace('\\', '__'))
        dst = os.path.join(R, f)
        shutil.copy2(src, dst)
        same = sha(dst) == h
        ok &= same
        print(('restored ' if same else 'MISMATCH ') + f + ' ' + h[:16])
    print('all byte-identical' if ok else 'NOT IDENTICAL')


if __name__ == '__main__':
    {'apply': apply, 'restore': restore}[sys.argv[1]]()
