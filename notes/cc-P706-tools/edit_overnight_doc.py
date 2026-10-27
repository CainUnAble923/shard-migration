"""cc-P706: Run-OvernightPlaytests.ps1's header says the transcripts are git-ignored now."""
import sys

p = sys.argv[1]
s = open(p, 'rb').read().decode('ascii')
nl = '\r\n' if '\r\n' in s else '\n'
old = r"""     D:\UO\shard-migration\testing\bot-runs\<yyyy-MM-dd-HHmm>\.""" + nl
new = old + (r"""     cc-P706: its transcripts\ (10 to 21 MB a night) are git-ignored by the docs repo (.gitignore), as run.log is; only""" + nl +
             r"""     report.md, results.json, email.txt and the other small files are committed. Commit-ShardWork.ps1 leaves anything""" + nl +
             r"""     else over its 5 MB cap under testing\bot-runs\ out of a commit instead of refusing the merge.""" + nl)
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'wb').write(s.encode('ascii'))
print('ok')
