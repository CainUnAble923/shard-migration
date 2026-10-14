"""The testing/ mirror, refreshed from Haven before each commit (cc-P107, Haven step H2).

    python tools/opsmirror.py [--root D:\\UO\\shard-migration] [--config <haven-ops.json>] [--state <state.json>]
                              [--token-file <token.txt>] [--api <http://host:port>]

Once the ops pages are on Haven (state.json mode "haven"), Haven's service is the only writer of play-test results,
ideas and bug reports. Commit-ShardWork.ps1 runs this first, so the commit carries Haven's data: it fetches
GET <opsApi>/api/export with the bearer token and puts the files back under <root>/testing with
opsdata.write_bundle (hash-checked, only the files the service writes, a removed screenshot removed too).

It never blocks a commit: every outcome is one line and exit 0. Mode "local" (or no state file): the game PC's own
service writes testing/ as before, and nothing is fetched. Haven unreachable: the previous mirror stays, and it says
so. Standard library only. ASCII only.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opsdata  # noqa: E402

DEFAULT_CONFIG = r"D:\ShatteredLegacy\scripts\haven-ops.json"


def _load(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _digest(root):
    out = {}
    base = os.path.join(root, "testing")
    for d, _, names in os.walk(base):
        for n in names:
            p = os.path.join(d, n)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            if opsdata._allowed(rel):
                with open(p, "rb") as f:
                    out[rel] = hashlib.sha256(f.read()).hexdigest()
    return out


def fetch_bundle(api, token, timeout=20):
    req = urllib.request.Request(api.rstrip("/") + "/api/export", headers={"Authorization": "Bearer " + token})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def refresh(root, mode, api, token, fetch=fetch_bundle):
    """{state, line, changed}. state: skipped | refreshed | unreachable | refused."""
    if mode != "haven":
        return {"state": "skipped", "changed": [],
                "line": "play-test mirror: not cut over to Haven (mode %s); the game PC's service writes testing/" % (mode or "local")}
    if not token:
        return {"state": "refused", "changed": [], "line": "play-test mirror NOT refreshed: no token file; the previous mirror stays"}
    try:
        bundle = fetch(api, token)
    except (urllib.error.URLError, OSError, ValueError) as e:
        return {"state": "unreachable", "changed": [],
                "line": "play-test mirror NOT refreshed (Haven unreachable: %s); the previous mirror stays" % e}
    before = _digest(root)
    try:
        written = opsdata.write_bundle(bundle, root)
    except ValueError as e:
        return {"state": "refused", "changed": [], "line": "play-test mirror NOT refreshed (%s); the previous mirror stays" % e}
    after = _digest(root)
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    return {"state": "refreshed", "changed": changed,
            "line": "play-test mirror refreshed from Haven: %d files, %d changed%s" % (
                len(written), len(changed), (": " + ", ".join(changed)) if changed else "")}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=r"D:\UO\shard-migration")
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--state", default="")
    ap.add_argument("--token-file", default="")
    ap.add_argument("--api", default="")
    a = ap.parse_args(argv)
    cfg = _load(a.config) or {}
    state = _load(a.state or cfg.get("stateFile", "")) or {}
    token = ""
    try:
        with open(a.token_file or cfg.get("tokenFile", ""), "r", encoding="ascii") as f:
            token = f.read().strip()
    except OSError:
        token = ""
    api = a.api or (cfg.get("haven") or {}).get("opsApi", "")
    r = refresh(a.root, state.get("mode", "local"), api, token)
    print("  " + r["line"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
