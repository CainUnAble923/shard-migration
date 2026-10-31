"""cc-P690: answer ModernUO's first-boot owner prompt (AccountPrompt.cs: "Do you want to create the owner account
now? (y/n)", then the username and the password) on a PRIVATE proof container started with -i -t, through Docker
Desktop's API pipe (the P289 way: POST /containers/<name>/attach?stream=1&stdin=1 with Upgrade: tcp). Private worlds
only; the password is read from a file outside the repos and never printed.

    python -P answer_owner.py <container> <secrets.json with "owner" and "ownerPassword">
"""
import json
import sys
import time

name, secrets = sys.argv[1], sys.argv[2]
assert name.startswith("sl-p690"), "private proof containers only"
s = json.load(open(secrets, encoding="utf-8"))
user, pw = s["owner"], s["ownerPassword"]

f = open(r"\\.\pipe\docker_engine", "r+b", buffering=0)
req = ("POST /containers/%s/attach?stream=1&stdin=1&stdout=0&stderr=0 HTTP/1.1\r\nHost: docker\r\n"
       "Connection: Upgrade\r\nUpgrade: tcp\r\nContent-Length: 0\r\n\r\n" % name)
f.write(req.encode("ascii"))
head = b""
while b"\r\n\r\n" not in head:
    c = f.read(1)
    if not c:
        break
    head += c
print(head.split(b"\r\n")[0].decode("ascii", "replace"))
for line in ("y", user, pw):
    time.sleep(1.5)
    f.write((line + "\n").encode("ascii"))
time.sleep(2)
f.close()
print("answered the owner prompt for", user)
