"""cc-P105 (Haven step H1): the play-test service made host-agnostic, still the same on the game PC by default.

    python -m unittest tools/tests/test_haven_h1.py

Facts:
- the export bundle round-trips every file the service writes (play tests, SUMMARY.md, ideas, bug reports and their
  screenshots), refuses a bad hash or a name outside the list, and writes nothing then; a mirror drops a removed shot;
- the game PC snapshot ages into "offline since";
- the Cloudflare Access check: a good RS256 token passes; a bad signature, wrong audience, wrong issuer, expired
  token, alg none or unknown key is refused (a throwaway RSA key made here, a local key server for the service);
- "by" is recorded on results, manual items, ideas and bug reports;
- the service, run for real on a free local port: with the defaults it writes testing/ under the notes root as before,
  answers the same routes and opens no second listener; in Haven mode it writes to the data folder only, its token
  listener refuses a missing or wrong token, and export, ingest and the snapshot work; with Access on, a request
  without a token is refused (except /nav.js), and a result carries the email.

Every fact works in temporary folders. Standard library only. ASCII only.
"""
import base64
import hashlib
import json
import os
import random
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import accessjwt  # noqa: E402
import bugs  # noqa: E402
import ideas  # noqa: E402
import opsdata  # noqa: E402
import playtests as pt  # noqa: E402

SERVER = Path(os.environ.get("SL_SHARD", r"D:\ShatteredLegacy")) / "docker" / "test-queue" / "server.py"
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 40
JPG = b"\xff\xd8\xff\xe0" + b"\x01" * 40


# --- a throwaway RSA key and RS256 tokens, standard library only ---------------------------------------------

def _is_prime(n, rnd):
    if n < 4:
        return n in (2, 3)
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(24):
        x = pow(rnd.randrange(2, n - 2), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _prime(bits, rnd):
    while True:
        c = rnd.getrandbits(bits) | (1 << (bits - 1)) | 1
        if _is_prime(c, rnd):
            return c


def make_key(seed):
    rnd = random.Random(seed)
    e = 65537
    while True:
        p, q = _prime(512, rnd), _prime(512, rnd)
        phi = (p - 1) * (q - 1)
        if p != q and phi % e:
            return p * q, e, pow(e, -1, phi)


KEY = make_key(105)
OTHER_KEY = make_key(106)


def b64u(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def sign(key, message):
    n, _, d = key
    k = (n.bit_length() + 7) // 8
    t = accessjwt.SHA256_DIGESTINFO + hashlib.sha256(message).digest()
    em = b"\x00\x01" + b"\xff" * (k - len(t) - 3) + b"\x00" + t
    return pow(int.from_bytes(em, "big"), d, n).to_bytes(k, "big")


def token(claims, key=KEY, kid="k1", alg="RS256"):
    h = b64u(json.dumps({"alg": alg, "kid": kid, "typ": "JWT"}).encode())
    c = b64u(json.dumps(claims).encode())
    return h + "." + c + "." + b64u(sign(key, (h + "." + c).encode()))


def jwks(key=KEY, kid="k1"):
    n, e, _ = key
    return {"keys": [{"kty": "RSA", "kid": kid, "alg": "RS256",
                      "n": b64u(n.to_bytes((n.bit_length() + 7) // 8, "big")), "e": b64u(e.to_bytes(3, "big"))}]}


TEAM = "sl-test.cloudflareaccess.com"
AUD = "aud-tag-105"


def good_claims(**kw):
    c = {"aud": [AUD], "iss": "https://" + TEAM, "exp": time.time() + 600, "iat": time.time(), "email": "Chase@Example.com"}
    c.update(kw)
    return c


# --- data fixtures ------------------------------------------------------------------------------------------------

def seed_data(data):
    pt.save(data, dict(pt.new_doc(), items=[pt.new_item(id="M-001", source="manual", what="x", text="x")]))
    ideas.add(data, "Fishing nets", by="kid@example.com")
    b = bugs.add(data, "Smelt eats ore", by="chase@example.com")
    bugs.add_shot(data, b["id"], PNG)
    bugs.add_shot(data, b["id"], JPG)
    return b["id"]


def tree(root):
    out = {}
    base = os.path.join(root, "testing")
    for d, _, names in os.walk(base):
        for n in names:
            p = os.path.join(d, n)
            if not n.endswith((".lock", ".tmp")):
                with open(p, "rb") as f:
                    out[os.path.relpath(p, root).replace(os.sep, "/")] = f.read()
    return out


class ExportBundle(unittest.TestCase):
    def setUp(self):
        self.src = tempfile.mkdtemp(prefix="h1-src-")
        self.dest = tempfile.mkdtemp(prefix="h1-dest-")

    def tearDown(self):
        shutil.rmtree(self.src, ignore_errors=True)
        shutil.rmtree(self.dest, ignore_errors=True)

    def test_round_trip_of_every_file_the_service_writes(self):
        seed_data(self.src)
        bundle = json.loads(json.dumps(opsdata.export_bundle(self.src)))     # as it travels
        self.assertEqual({"testing/play-tests.json", "testing/SUMMARY.md", "testing/feature-ideas.json",
                          "testing/bug-reports.json", "testing/bug-reports/files/B-001-1.png",
                          "testing/bug-reports/files/B-001-2.jpg"}, set(bundle["files"]))
        opsdata.write_bundle(bundle, self.dest)
        self.assertEqual(tree(self.src), tree(self.dest))

    def test_a_mirror_drops_a_screenshot_the_source_no_longer_has(self):
        seed_data(self.src)
        opsdata.write_bundle(opsdata.export_bundle(self.src), self.dest)
        os.remove(os.path.join(self.src, "testing", "bug-reports", "files", "B-001-2.jpg"))
        opsdata.write_bundle(opsdata.export_bundle(self.src), self.dest)
        self.assertEqual(tree(self.src), tree(self.dest))

    def test_a_bad_hash_or_a_foreign_name_writes_nothing(self):
        seed_data(self.src)
        good = opsdata.export_bundle(self.src)
        bad = json.loads(json.dumps(good))
        bad["files"]["testing/SUMMARY.md"]["text"] += "tampered"
        with self.assertRaises(ValueError):
            opsdata.write_bundle(bad, self.dest)
        for name in ("../evil.txt", "testing/../../evil.txt", "notes/cc-P999.md", "testing/bug-reports/files/x.exe",
                     "testing/bug-reports/files/../../../evil.png"):
            evil = json.loads(json.dumps(good))
            evil["files"][name] = {"text": "x", "sha256": hashlib.sha256(b"x").hexdigest()}
            with self.assertRaises(ValueError, msg=name):
                opsdata.write_bundle(evil, self.dest)
        with self.assertRaises(ValueError):
            opsdata.write_bundle({"schema": 99, "files": {}}, self.dest)
        self.assertEqual({}, tree(self.dest), "nothing is written when a bundle is refused")


class GamePcSnapshot(unittest.TestCase):
    def test_never_received_then_fresh_then_offline_since(self):
        d = tempfile.mkdtemp(prefix="h1-gpc-")
        try:
            self.assertEqual("", opsdata.gamepc_status(d)["receivedAt"])
            self.assertIsNone(opsdata.gamepc_status(d)["offline"])
            rec = opsdata.save_gamepc(d, {"autopilot": "on"}, now=1_000_000)
            s = opsdata.gamepc_status(d, now=1_000_000 + 60)
            self.assertEqual((False, "", 60, {"autopilot": "on"}), (s["offline"], s["offlineSince"], s["ageSeconds"], s["snapshot"]))
            s = opsdata.gamepc_status(d, now=1_000_000 + opsdata.OFFLINE_SECONDS + 1)
            self.assertEqual((True, rec["receivedAt"]), (s["offline"], s["offlineSince"]))
            with self.assertRaises(ValueError):
                opsdata.save_gamepc(d, ["not", "an", "object"])
        finally:
            shutil.rmtree(d, ignore_errors=True)


class AccessCheck(unittest.TestCase):
    def verifier(self, keys=None):
        return accessjwt.AccessVerifier(TEAM, AUD, fetch=lambda url: keys or jwks())

    def test_a_good_token_passes(self):
        self.assertEqual("Chase@Example.com", self.verifier().verify(token(good_claims()))["email"])
        self.assertEqual("x@y.z", self.verifier().verify(token(good_claims(aud=AUD, email="x@y.z")))["email"])

    def test_everything_else_is_refused(self):
        v = self.verifier()
        good = token(good_claims())
        h, c, s = good.split(".")
        cases = {
            "bad signature": token(good_claims(), key=OTHER_KEY),
            "edited claims": h + "." + b64u(json.dumps(good_claims(email="evil@x.y")).encode()) + "." + s,
            "wrong audience": token(good_claims(aud=["someone-else"])),
            "wrong issuer": token(good_claims(iss="https://evil.cloudflareaccess.com")),
            "expired": token(good_claims(exp=time.time() - 3600)),
            "not yet": token(good_claims(nbf=time.time() + 3600)),
            "no email": token(good_claims(email="")),
            "alg none": b64u(b'{"alg":"none","kid":"k1"}') + "." + c + ".",
            "unknown kid": token(good_claims(), kid="k9"),
            "garbage": "not.a.jwt.at.all",
            "empty": "",
        }
        for why, t in cases.items():
            with self.assertRaises(accessjwt.AccessDenied, msg=why):
                v.verify(t)

    def test_the_token_comes_from_the_header_or_the_cookie(self):
        self.assertEqual("abc", accessjwt.token_from({"Cf-Access-Jwt-Assertion": " abc "}))
        self.assertEqual("xyz", accessjwt.token_from({"Cookie": "a=1; CF_Authorization=xyz; b=2"}))
        self.assertEqual("", accessjwt.token_from({}))


class WriterIdentity(unittest.TestCase):
    def test_by_is_recorded_on_results_manual_items_ideas_and_bugs(self):
        d = tempfile.mkdtemp(prefix="h1-by-")
        try:
            m = pt.add_manual(d, "Try the forge", by="kid@example.com")
            self.assertEqual("kid@example.com", m["by"])
            r = pt.set_result(d, m["id"], "pass", "fine", by="chase@example.com")
            self.assertEqual("chase@example.com", r["by"])
            self.assertEqual("", pt.set_result(d, m["id"], "open")["by"], "no identity: empty, as on the game PC")
            self.assertEqual("kid@example.com", ideas.add(d, "Nets", by="kid@example.com")["by"])
            self.assertEqual("chase@example.com", bugs.add(d, "Ore", by="chase@example.com")["by"])
        finally:
            shutil.rmtree(d, ignore_errors=True)


# --- the service, run for real ------------------------------------------------------------------------------------

def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class KeyServer:
    """A local stand-in for https://<team>/cdn-cgi/access/certs."""

    def __init__(self):
        body = json.dumps(jwks()).encode()

        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *a):
                pass

        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = "http://127.0.0.1:%d/cdn-cgi/access/certs" % self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def close(self):
        self.srv.shutdown()


@unittest.skipUnless(SERVER.exists(), "the play-test service is not on this machine")
class Service(unittest.TestCase):
    TOKEN = "h1-test-token-" + "x" * 20

    def start(self, extra=(), env=None):
        self.root = tempfile.mkdtemp(prefix="h1-svc-root-")
        for d in ("notes", "docs", "testing"):
            os.makedirs(os.path.join(self.root, d))
        shutil.copy(ROOT / "docs" / "feature-queue.md", os.path.join(self.root, "docs", "feature-queue.md"))
        self.port = free_port()
        e = dict(os.environ)
        for k in ("PLAYTESTS_DATA", "PLAYTESTS_LAN_PORT", "PLAYTESTS_TOKEN", "PLAYTESTS_TOKEN_FILE", "ACCESS_TEAM_DOMAIN",
                  "ACCESS_AUD", "ACCESS_CERTS_URL", "REPO_STAMP"):
            e.pop(k, None)
        e.update(env or {})
        self.proc = subprocess.Popen([sys.executable, "-B", str(SERVER), "--root", self.root, "--lib", str(TOOLS),
                                      "--bind", "127.0.0.1", "--port", str(self.port), "--status-page", os.devnull,
                                      "--deployed", os.devnull] + list(extra),
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e)
        for _ in range(100):
            if self.proc.poll() is not None:
                self.fail("the service exited: " + self.proc.stdout.read().decode("utf-8", "replace")[-600:])
            try:
                self.call("GET", "/nav.js")
                return
            except OSError:
                time.sleep(0.1)
        self.fail("the service did not start")

    def tearDown(self):
        if getattr(self, "proc", None):
            self.proc.terminate()
            self.proc.wait(10)
            self.proc.stdout.close()
        for d in (getattr(self, "root", None), getattr(self, "data", None)):
            if d:
                shutil.rmtree(d, ignore_errors=True)
        if getattr(self, "keys", None):
            self.keys.close()

    def call(self, method, path, body=None, port=None, headers=None):
        h = {"Content-Type": "application/json"}
        h.update(headers or {})
        req = urllib.request.Request("http://127.0.0.1:%d%s" % (port or self.port, path), method=method, headers=h,
                                     data=None if body is None else json.dumps(body).encode("utf-8"))
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def json_of(self, method, path, body=None, **kw):
        code, raw = self.call(method, path, body, **kw)
        return code, json.loads(raw.decode("utf-8"))

    def test_the_defaults_write_under_the_notes_root_as_before_and_open_no_second_listener(self):
        lan = free_port()
        self.start(extra=["--lan-port", "0"])
        for path in ("/", "/nav.js", "/api/items", "/api/summary", "/api/ideas", "/api/bugs", "/api/ideas/copy",
                     "/api/bugs/copy"):
            self.assertEqual(200, self.call("GET", path)[0], path)
        code, j = self.json_of("POST", "/api/manual", {"what": "Try the forge"})
        self.assertEqual((200, ""), (code, j["item"]["by"]))
        self.assertEqual(200, self.json_of("POST", "/api/ideas/add", {"title": "Nets"})[0])
        self.assertEqual(200, self.json_of("POST", "/api/bugs/add", {"title": "Ore"})[0])
        self.assertEqual({"testing/play-tests.json", "testing/SUMMARY.md", "testing/feature-ideas.json",
                          "testing/bug-reports.json"}, set(tree(self.root)))
        svc = self.json_of("GET", "/api/items")[1]["service"]
        self.assertEqual({"by": "", "access": False}, svc["identity"])
        self.assertIsNone(svc["gamepc"]["offline"])
        self.assertEqual("", svc["repo"]["at"], "a notes root that is not a git checkout: no 'repo as of'")
        for path in ("/api/export", "/api/gamepc"):
            self.assertEqual(404, self.call("GET", path)[0], "not on the page's listener: " + path)
        with self.assertRaises(OSError):
            self.call("GET", "/api/export", port=lan)

    def test_haven_mode_separates_the_data_and_guards_export_and_ingest_with_the_token(self):
        self.data = tempfile.mkdtemp(prefix="h1-svc-data-")
        lan = free_port()
        stamp = os.path.join(self.data, "stamp.txt")
        with open(stamp, "w", encoding="ascii") as f:
            f.write("0123456789abcdef0123 2026-10-14T12:00:00Z\n")
        self.start(extra=["--lan-port", str(lan), "--lan-bind", "127.0.0.1"],
                   env={"PLAYTESTS_DATA": self.data, "PLAYTESTS_TOKEN": self.TOKEN, "REPO_STAMP": stamp})
        bid = self.json_of("POST", "/api/bugs/add", {"title": "Ore"})[1]["bug"]["id"]
        shot = "data:image/png;base64," + base64.b64encode(PNG).decode("ascii")
        self.assertEqual(200, self.json_of("POST", "/api/bugs/shot", {"id": bid, "data": shot})[0])
        mid = self.json_of("POST", "/api/manual", {"what": "Forge"})[1]["item"]["id"]
        self.assertEqual(200, self.json_of("POST", "/api/result", {"id": mid, "status": "pass"})[0])
        self.assertEqual({}, tree(self.root), "nothing written under the notes root")
        self.assertIn("testing/bug-reports/files/%s-1.png" % bid, tree(self.data))
        self.assertEqual({"commit": "0123456789ab", "at": "2026-10-14T12:00:00Z", "source": "stamp"},
                         self.json_of("GET", "/api/items")[1]["service"]["repo"])
        # The token listener: nothing without the right token.
        for headers in ({}, {"Authorization": "Bearer wrong"}, {"Authorization": self.TOKEN},
                        {"Authorization": "Basic " + self.TOKEN}):
            self.assertEqual(401, self.call("GET", "/api/export", port=lan, headers=headers)[0], headers)
            self.assertEqual(401, self.call("POST", "/api/ingest/gamepc", {"a": 1}, port=lan, headers=headers)[0])
        auth = {"Authorization": "Bearer " + self.TOKEN}
        code, bundle = self.json_of("GET", "/api/export", port=lan, headers=auth)
        self.assertEqual(200, code)
        mirror = tempfile.mkdtemp(prefix="h1-svc-mirror-")
        try:
            opsdata.write_bundle(bundle, mirror)
            self.assertEqual(tree(self.data), tree(mirror), "the export over HTTP round-trips")
        finally:
            shutil.rmtree(mirror, ignore_errors=True)
        self.assertEqual(200, self.json_of("POST", "/api/ingest/gamepc", {"autopilot": "on", "queue": 3}, port=lan,
                                           headers=auth)[0])
        g = self.json_of("GET", "/api/gamepc", port=lan, headers=auth)[1]
        self.assertEqual(({"autopilot": "on", "queue": 3}, False), (g["snapshot"], g["offline"]))
        self.assertFalse(self.json_of("GET", "/api/items")[1]["service"]["gamepc"]["offline"])
        big = {"x": "y" * (opsdata.MAX_SNAPSHOT + 10)}
        self.assertEqual(413, self.call("POST", "/api/ingest/gamepc", big, port=lan, headers=auth)[0])
        self.assertEqual(404, self.call("GET", "/api/items", port=lan, headers=auth)[0], "the page is not on it")

    def test_a_token_listener_without_a_token_is_never_opened(self):
        lan = free_port()
        self.start(extra=["--lan-port", str(lan), "--lan-bind", "127.0.0.1"])
        with self.assertRaises(OSError):
            self.call("GET", "/api/export", port=lan, headers={"Authorization": "Bearer "})

    def test_with_access_on_a_request_needs_a_good_token_and_the_email_is_by(self):
        self.keys = KeyServer()
        self.start(env={"ACCESS_TEAM_DOMAIN": TEAM, "ACCESS_AUD": AUD, "ACCESS_CERTS_URL": self.keys.url})
        self.assertEqual(200, self.call("GET", "/nav.js")[0], "the menu holds no data: open")
        before = tree(self.root)     # the importer's own first write at start
        for path in ("/", "/api/items", "/api/summary", "/api/ideas", "/api/bugs"):
            self.assertEqual(403, self.call("GET", path)[0], path)
        self.assertEqual(403, self.call("POST", "/api/manual", {"what": "x"})[0])
        bad = {"Cf-Access-Jwt-Assertion": token(good_claims(), key=OTHER_KEY)}
        self.assertEqual(403, self.call("GET", "/api/items", headers=bad)[0])
        self.assertEqual(before, tree(self.root), "a refused write writes nothing")
        me = {"Cf-Access-Jwt-Assertion": token(good_claims())}
        code, j = self.json_of("POST", "/api/manual", {"what": "Forge"}, headers=me)
        self.assertEqual((200, "chase@example.com"), (code, j["item"]["by"]))
        kid = {"Cookie": "CF_Authorization=" + token(good_claims(email="Kid@Example.com"))}
        code, j = self.json_of("POST", "/api/result", {"id": j["item"]["id"], "status": "pass"}, headers=kid)
        self.assertEqual((200, "kid@example.com"), (code, j["item"]["by"]))
        self.assertEqual("kid@example.com", self.json_of("POST", "/api/ideas/add", {"title": "Nets"}, headers=kid)[1]["idea"]["by"])
        self.assertEqual("kid@example.com", self.json_of("POST", "/api/bugs/add", {"title": "Ore"}, headers=kid)[1]["bug"]["by"])
        self.assertEqual({"by": "chase@example.com", "access": True},
                         self.json_of("GET", "/api/items", headers=me)[1]["service"]["identity"])


class Menu(unittest.TestCase):
    def test_nav_js_has_url_mode_and_lan_only_and_keeps_todays_rows(self):
        text = (SERVER.parent / "html" / "nav.js").read_text(encoding="ascii")
        self.assertIn("if (p.url) return p.url;", text)
        self.assertIn("if (PAGES[i].lanOnly && !onLan()) continue;", text)
        self.assertIn("{ key: 'playtests', label: 'Play tests',   host: null, port: 8093, path: '/' }", text)
        self.assertIn("{ key: 'status',    label: 'Shard status', host: null, port: 8093, path: '/status' }", text)
        # cc-P107 pinned Homepage to the game PC until H5.
        # cc-P110 (H5) moved the Dashboard entry to Haven's Homepage; cc-P112 updated this pin (P110 missed it).
        self.assertIn("{ key: 'dashboard', label: 'Dashboard',    host: '192.168.1.61', port: 3000, path: '/', lanOnly: true }", text)


if __name__ == "__main__":
    unittest.main()
