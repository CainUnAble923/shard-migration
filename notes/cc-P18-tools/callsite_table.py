"""A1 table: every line using the account guild API at bb51fad (before cc-P18), per file, split into
reads and writes, with the character that was in reach there (found by reading each site)."""
import re
import subprocess

M = r'\b(JoinedGuilds|GuildReputation|GuildCurrency|GetReputation|AddReputation|GetCurrency|SpendCurrency|AddCurrency)\b'
WRITE = re.compile(r'\.(AddReputation|AddCurrency|SpendCurrency)\(|\.(JoinedGuilds|GuildReputation|GuildCurrency)(\.(Add|Remove|Clear)\(|\[[^\]]*\]\s*=[^=])')

# What was in reach at the sites, from reading each one (cc-P18 A1).
REACH = {
    'ClusterFDevTools.cs': 'account, and a character if one is online or named; the reset clears every character, so none is needed',
    'ClusterFLeagueSystem.cs': 'pm at :151 (OnGuildJoined); GetStatus(data) at :63 had only the account record: its callers (LeagueRegistrarGump) have _pm, now passed in',
    'ClusterFCompactAdminTools.cs': 'the targeted PlayerMobile',
    'ClusterFGuildSystem.cs': 'pm or _pm everywhere; IsJoined(IAccount) at :296 had only the account, and all 20 callers had a PlayerMobile',
    'CompactOreSatchelRoutingHook.cs': 'pm (Mobile m cast to PlayerMobile)',
    'ClusterFSmithBODSystem.cs': 'pm / pmComm (the Mobile dropping the deed)',
    'SmithGuildSalvageBag.cs': 'pm (the Mobile using the bag)',
    'ClusterFCustodianSystem.cs': 'pm',
    'TrashBag.cs': 'pm',
}

base = 'server/customizations/'
names = subprocess.run(['git', 'ls-tree', '--name-only', 'bb51fad', base], capture_output=True, text=True).stdout.split()
rows = []
total = 0
for path in names:
    if not path.endswith('.cs') or path.endswith('ClusterFAccountData.cs'):
        continue
    text = subprocess.run(['git', 'show', f'bb51fad:{path}'], capture_output=True, text=True, encoding='utf-8').stdout
    reads, writes = [], []
    for i, line in enumerate(text.split('\n'), 1):
        if re.search(M, line) and not line.strip().startswith('//') and not line.strip().startswith('///') \
                and '[Description(' not in line:
            (writes if WRITE.search(line) else reads).append(i)
    if reads or writes:
        f = path[len(base):]
        total += len(reads) + len(writes)
        rows.append((f, reads, writes))

for tpath in ['server/tests/Misc/AccountDataSerializerVerification.cs', 'server/tests/Misc/GuildStarterPathVerification.cs']:
    text = subprocess.run(['git', 'show', f'bb51fad:{tpath}'], capture_output=True, text=True, encoding='utf-8').stdout
    lines = [i for i, l in enumerate(text.split('\n'), 1) if re.search(M, l) and not l.strip().startswith('//')]
    rows.append((tpath.replace('server/', ''), lines, []))
    total += len(lines)

print('| File | Reads (line) | Writes (line) | Character in reach |')
print('|---|---|---|---|')
for f, r, w in rows:
    reach = REACH.get(f, 'test code' if f.startswith('tests/') else 'pm or _pm (a PlayerMobile field or parameter)')
    print(f'| `{f}` | {", ".join(map(str, r)) or "-"} | {", ".join(map(str, w)) or "-"} | {reach} |')
print()
print(f'{len(rows)} files, {total} code lines (comments and [Description] strings excluded)')
