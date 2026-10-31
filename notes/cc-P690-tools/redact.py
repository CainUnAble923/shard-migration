"""cc-P690: strip the private owner's password (echoed by the container's TTY at the owner prompt) from every log file
given, in place. python -P redact.py <secrets.json> <file>..."""
import json
import sys

pw = json.load(open(sys.argv[1], encoding="utf-8"))["ownerPassword"]
for p in sys.argv[2:]:
    s = open(p, encoding="utf-8", errors="replace").read()
    n = s.count(pw)
    open(p, "w", encoding="utf-8").write(s.replace(pw, "<redacted>"))
    print("%s: %d redacted" % (p, n))
