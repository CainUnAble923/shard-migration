"""cc-P722: P719's CHANGELOG line as its own section 2026.10.28.5 on top of the release branch's CHANGELOG (ours)."""
import subprocess
import sys

W = sys.argv[1]
ours = subprocess.run(["git", "-C", W, "show", ":2:CHANGELOG.md"], capture_output=True, check=True).stdout.decode("utf-8")
theirs = subprocess.run(["git", "-C", W, "show", "18d524e:CHANGELOG.md"], capture_output=True, check=True).stdout.decode("utf-8")
line = [l for l in theirs.splitlines() if l.startswith("- A new character walks until you turn on Always run")]
assert len(line) == 1
anchor = "## 2026.10.28.4\n"
assert ours.count(anchor) == 1 and "## 2026.10.28.5" not in ours
s = ours.replace(anchor, "## 2026.10.28.5\n\n### Changed\n" + line[0] + "\n\n" + anchor)
open(W + "/CHANGELOG.md", "w", encoding="utf-8", newline="").write(s)
open(W + "/VERSION", "w", encoding="utf-8", newline="").write("2026.10.28.5\n")
print("ok")
