"""cc-P735: the CHANGELOG's Staff line (a new 2026.10.31.5 section above main's newest) and VERSION.
Usage: python -P edit_changelog.py <code copy>"""
import sys

root = sys.argv[1]
p = root + "/CHANGELOG.md"
s = open(p, encoding="utf-8", newline="").read()
top = "## 2026.10.31.4\n"
assert s.count(top) == 1 and "## 2026.10.31.5" not in s
section = ("## 2026.10.31.5\n\n### Staff\n"
           "- The overnight play-test bot's New Haven checks (a new character pointed at the Guild Board, and the patch "
           "notes on an account's first login) make their character with the New Haven start again, on an account that "
           "has skipped the tutorial, now that new characters wake on the Wakening Isle. When an account still has New "
           "Haven locked, the bot first has a throwaway character wake on the isle and its Admin skips that tutorial.\n\n")
s = s.replace(top, section + top)
open(p, "w", encoding="utf-8", newline="").write(s)
open(root + "/VERSION", "w", encoding="utf-8", newline="\n").write("2026.10.31.5\n")
print("CHANGELOG and VERSION: 2026.10.31.5")
