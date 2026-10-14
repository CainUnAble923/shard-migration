"""The play-test service's data, moved as one bundle, and the game PC's snapshot (cc-P105, Haven step H1).

Notes: notes/cc-P105-haven-h1-host-agnostic.md; the design is notes/cc-P89-haven-pages-plan.md Part B items 2 and 3.

- export_bundle(data) is what GET /api/export returns: every file the service writes under testing/ (play tests and
  their summary, feature ideas, bug reports and their screenshots), as one JSON object. Text files go as text, the
  screenshots as base64, each with its SHA-256.
- write_bundle(bundle, dest) puts a bundle back as files under dest, replacing the mirror wholesale: each file is
  checked against its hash and written by temp file and rename, and a screenshot the bundle no longer has is removed.
  Only the names listed here are ever written, so a bundle cannot write anywhere else. H2's Commit-ShardWork.ps1 uses
  it to refresh shard-migration/testing/ before each commit.
- The game PC snapshot (POST /api/ingest/gamepc, GET /api/gamepc) is kept in <data>/ops/gamepc.json with the time it
  arrived. It is "offline" once it is older than OFFLINE_SECONDS.
- repo_as_of(root, stamp) says how fresh the notes clone is: the pull container's stamp file if there is one, else
  git's last commit when git is installed, else nothing (the game PC's container has no git: the field stays empty).

Standard library only. ASCII only.
"""
import base64
import calendar
import hashlib
import json
import os
import re
import subprocess
import time

BUNDLE_SCHEMA = 1
TEXT_FILES = [
    os.path.join("testing", "play-tests.json"),
    os.path.join("testing", "SUMMARY.md"),
    os.path.join("testing", "feature-ideas.json"),
    os.path.join("testing", "bug-reports.json"),
]
SHOTS_REL = os.path.join("testing", "bug-reports", "files")
SHOT_RE = re.compile(r"^B-\d{3,}-\d+\.(png|jpg)$")
GAMEPC_REL = os.path.join("ops", "gamepc.json")
OFFLINE_SECONDS = 180
MAX_SNAPSHOT = 64 * 1024


def now_iso(t=None):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() if t is None else t))


def parse_iso(s):
    try:
        return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))
    except (TypeError, ValueError):
        return None


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _posix(rel):
    return rel.replace(os.sep, "/")


# --- the export bundle -------------------------------------------------------------------------------

def export_bundle(data):
    """Every file the service writes under data/testing, as one JSON-ready dict. A file not there yet is left out."""
    files = {}
    for rel in TEXT_FILES:
        path = os.path.join(data, rel)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                raw = f.read()
            files[_posix(rel)] = {"text": raw.decode("utf-8"), "sha256": _sha(raw)}
    shots = os.path.join(data, SHOTS_REL)
    if os.path.isdir(shots):
        for name in sorted(os.listdir(shots)):
            if SHOT_RE.match(name):
                with open(os.path.join(shots, name), "rb") as f:
                    raw = f.read()
                files[_posix(os.path.join(SHOTS_REL, name))] = {"base64": base64.b64encode(raw).decode("ascii"),
                                                                "sha256": _sha(raw)}
    return {"schema": BUNDLE_SCHEMA, "exportedAt": now_iso(), "files": files}


def _allowed(rel):
    if rel in [_posix(r) for r in TEXT_FILES]:
        return True
    head, _, name = rel.rpartition("/")
    return head == _posix(SHOTS_REL) and bool(SHOT_RE.match(name))


def write_bundle(bundle, dest):
    """Write a bundle's files under dest, wholesale. Returns the list of files written. Raises ValueError on anything
    that is not a bundle, a name outside the list, or a hash that does not match; nothing is written in that case."""
    if not isinstance(bundle, dict) or bundle.get("schema") != BUNDLE_SCHEMA or not isinstance(bundle.get("files"), dict):
        raise ValueError("not an export bundle (schema %r)" % (bundle.get("schema") if isinstance(bundle, dict) else None))
    staged = []
    for rel, entry in sorted(bundle["files"].items()):
        if not _allowed(rel) or not isinstance(entry, dict):
            raise ValueError("refused: %s is not a file the service writes" % rel)
        if "text" in entry:
            raw = str(entry["text"]).encode("utf-8")
        else:
            raw = base64.b64decode(str(entry.get("base64", "")), validate=True)
        if _sha(raw) != entry.get("sha256"):
            raise ValueError("refused: %s does not match its sha256" % rel)
        staged.append((rel, raw))
    written = []
    for rel, raw in staged:
        path = os.path.join(dest, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(raw)
        os.replace(tmp, path)
        written.append(rel)
    # A mirror, not a merge: a screenshot Haven no longer has goes from the mirror too.
    shots = os.path.join(dest, SHOTS_REL)
    keep = {rel.rpartition("/")[2] for rel, _ in staged if rel.startswith(_posix(SHOTS_REL) + "/")}
    if os.path.isdir(shots):
        for name in os.listdir(shots):
            if SHOT_RE.match(name) and name not in keep:
                os.remove(os.path.join(shots, name))
    return written


# --- the game PC snapshot --------------------------------------------------------------------------------

def save_gamepc(data, snapshot, now=None):
    if not isinstance(snapshot, dict):
        raise ValueError("send a JSON object")
    rec = {"receivedAt": now_iso(now), "snapshot": snapshot}
    path = os.path.join(data, GAMEPC_REL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, indent=1, sort_keys=True)
    os.replace(tmp, path)
    return rec


def gamepc_status(data, now=None):
    """{receivedAt, ageSeconds, offline, offlineSince, snapshot}. Never received: receivedAt empty, offline None."""
    try:
        with open(os.path.join(data, GAMEPC_REL), "r", encoding="utf-8") as f:
            rec = json.load(f)
    except (OSError, ValueError):
        return {"receivedAt": "", "ageSeconds": None, "offline": None, "offlineSince": "", "snapshot": None}
    got = parse_iso(rec.get("receivedAt", ""))
    age = None if got is None else max(0, int((time.time() if now is None else now) - got))
    offline = age is not None and age > OFFLINE_SECONDS
    return {"receivedAt": rec.get("receivedAt", ""), "ageSeconds": age, "offline": offline,
            "offlineSince": rec.get("receivedAt", "") if offline else "", "snapshot": rec.get("snapshot")}


# --- how fresh the notes are -------------------------------------------------------------------------------

def repo_as_of(root, stamp=""):
    """{commit, at, source}. The pull container's stamp file (one line: '<commit> <ISO time>') wins; else git."""
    if stamp:
        try:
            with open(stamp, "r", encoding="ascii") as f:
                parts = f.read().split()
            if len(parts) >= 2:
                return {"commit": parts[0][:12], "at": parts[1], "source": "stamp"}
        except OSError:
            pass
    try:
        out = subprocess.run(["git", "-C", root, "log", "-1", "--format=%H %cI"], capture_output=True, text=True,
                             timeout=5)
        if out.returncode == 0 and out.stdout.strip():
            sha, at = out.stdout.split()[:2]
            return {"commit": sha[:12], "at": at, "source": "git"}
    except (OSError, subprocess.SubprocessError, ValueError):
        pass
    return {"commit": "", "at": "", "source": ""}
