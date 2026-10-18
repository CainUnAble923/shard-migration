"""cc-P164: the play-test page's Up next: Chase's open items in short themed sessions.

    python -m unittest discover -s tools\\tests -p "test_playsessions.py"

tools/playsessions.py builds the sessions from testing/sessions.json (the overseer's file) and the annotated document;
the service (docker/test-queue/server.py) serves them on /api/items and marks a group Later in one write; the page
(html/index.html) opens on Up next. The Browser class drives the page in headless Chrome at a 390 px wide viewport
(Selenium, as P112 and P146 checked theirs by hand); the last class checks the real files.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
SHARD = Path(r"D:\ShatteredLegacy")
SERVER = SHARD / "docker" / "test-queue" / "server.py"
PAGE = SHARD / "docker" / "test-queue" / "html" / "index.html"
sys.path.insert(0, str(TOOLS))
import playtests as pt  # noqa: E402

try:
    import playsessions as ps  # noqa: E402
except ImportError:  # before cc-P164: every fact below fails on it, none errors out of the run
    ps = None


def need():
    if ps is None:
        raise AssertionError("tools/playsessions.py does not exist")


def item(iid, prompt, who="you", where="admin", status="open", chars=None, what="", expect="", steps=None,
         position=1, result_at=""):
    it = pt.new_item(id=iid, prompt=prompt, source="notes", what=what or ("do the thing for " + iid),
                     expect=expect or "it works", position=position)
    it["status"] = status
    it["resultAt"] = result_at
    if status in ("open", "later", "blocked"):
        it["who"] = {"key": who}
        it["where"] = {"key": where, "chars": chars or []}
    if steps is not None:
        it["steps"] = steps
    return it


def doc_of(items, prompts=None):
    return {"items": items, "prompts": prompts or {}, "where": {"labels": {
        "questions": "Questions", "outside": "Outside the game", "admin": "In game: Admin", "player": "In game: Player",
        "bot": "Bot", "cc": "CC"}}}


def by_id(doc):
    return {s["id"]: s for s in doc["sessions"]["list"]}


class Builder(unittest.TestCase):
    def setUp(self):
        need()

    def test_a_seeded_session_keeps_its_order_and_never_shows_bot_or_cc(self):
        items = [item("P10-1", "P10"), item("P10-2", "P10", who="bot", where="bot"), item("P10-3", "P10", who="cc", where="cc"),
                 item("P11-1", "P11", where="player"), item("P11-2", "P11", status="pass", result_at="2026-10-18T10:00:00Z")]
        spec = {"sessions": [{"id": "one", "title": "One", "why": "w", "before": ["log in"], "items": ["P11-1", "P10-2", "P10-1", "P10-3", "P11-2", "P99-9"]}]}
        d = ps.annotate(doc_of(items), spec)
        s = by_id(d)["one"]
        self.assertEqual(["P11-1", "P10-1", "P11-2"], [x["id"] for x in s["items"]])
        self.assertEqual((1, 3, False), (s["doneCount"], s["total"], s["finished"]))
        self.assertEqual(["log in"], s["before"])
        self.assertEqual("one", d["sessions"]["upNext"])
        self.assertEqual({"bot": 1, "cc": 1}, d["sessions"]["owed"])

    def test_a_finished_item_leaves_up_next_and_a_finished_session_collapses_with_its_date(self):
        items = [item("P10-1", "P10"), item("P10-2", "P10"), item("P11-1", "P11")]
        spec = {"sessions": [{"id": "a", "items": ["P10-1", "P10-2"]}, {"id": "b", "items": ["P11-1"]}]}
        self.assertEqual("a", ps.annotate(doc_of([dict(i) for i in items]), spec)["sessions"]["upNext"])
        items[0]["status"], items[0]["resultAt"] = "pass", "2026-10-17T09:00:00Z"
        d = ps.annotate(doc_of(items), spec)
        a = by_id(d)["a"]
        self.assertEqual([True, False], [x["done"] for x in a["items"]])
        self.assertEqual(("a", 1), (d["sessions"]["upNext"], a["doneCount"]))
        items[1]["status"], items[1]["resultAt"] = "later", "2026-10-18T11:30:00Z"
        d = ps.annotate(doc_of(items), spec)
        a = by_id(d)["a"]
        self.assertEqual((True, "2026-10-18"), (a["finished"], a["finishedAt"]))
        self.assertEqual("b", d["sessions"]["upNext"], "Up next moves on to the next unfinished session")

    def test_automatic_sessions_cap_at_twelve_keep_prompts_together_newest_first_and_lose_nothing(self):
        items = []
        for p, n in (("P20", 5), ("P21", 4), ("P22", 6), ("P23", 15)):
            items += [item("%s-%d" % (p, k), p, position=k) for k in range(1, n + 1)]
        items += [item("P24-1", "P24", where="player", chars=["elf"]), item("P24-2", "P24", where="outside"),
                  item("P25-1", "P25", who="bot", where="bot"), item("P25-2", "P25", who="decide", where="questions"),
                  item("P25-3", "P25", status="pass")]
        items[0]["replacedBy"] = ["P20-D1"]
        d = ps.annotate(doc_of(items), {})
        auto = [s for s in d["sessions"]["list"] if s["kind"] == "auto"]
        admin = [s for s in auto if s["id"].startswith("auto-admin")]
        self.assertEqual([12, 9, 8], [s["total"] for s in admin], "P23's 15 split 12 + 3; its 3 and P22's 6; P21 and P20 (4 left once P20-1 is replaced)")
        self.assertEqual(["P23"] * 12, [x["prompt"] for x in admin[0]["items"]])
        self.assertEqual(["P23"] * 3 + ["P22"] * 6, [x["prompt"] for x in admin[1]["items"]], "a prompt is never split across sessions unless it alone has more than 12")
        self.assertEqual(["P21"] * 4 + ["P20"] * 4, [x["prompt"] for x in admin[2]["items"]])
        self.assertTrue(all(s["total"] <= ps.MAX for s in auto))
        shown = [x["id"] for s in d["sessions"]["list"] for x in s["items"]]
        self.assertEqual(len(shown), len(set(shown)), "each item in one session")
        want = {i["id"] for i in items if i["status"] == "open" and i.get("who", {}).get("key") in ("you", "botyou") and not i.get("replacedBy")}
        self.assertEqual(want, set(shown), "every open item of Chase's, and only those (no Bot, CC, questions or replaced)")
        self.assertIn("auto-player-elf-1", by_id(d))
        self.assertIn("auto-outside-1", by_id(d))
        self.assertEqual("auto-admin-1", d["sessions"]["upNext"], "no seeded sessions: the first automatic one")

    def test_needs_rebuild_when_the_prompt_came_after_the_test_shard_was_deployed(self):
        items = [item("P30-1", "P30"), item("P31-1", "P31", where="player"), item("P31-2", "P31", where="outside"),
                 item("P32-1", "P32", what="install the newest player package and open the paperdoll")]
        prompts = {"P30": {"importedAt": "2026-10-18T09:00:00Z"}, "P31": {"importedAt": "2026-10-18T17:00:00Z"},
                   "P32": {"importedAt": "2026-10-18T08:00:00Z"}}
        dep = {"commit": "abc", "version": "2026.10.18.7", "at": "2026-10-18T16:20:51Z"}
        d = ps.annotate(doc_of(items, prompts), {}, dep)
        got = {x["id"]: x["needs"] for s in d["sessions"]["list"] for x in s["items"]}
        self.assertEqual({"P30-1": [], "P31-1": ["rebuild test shard"], "P31-2": [], "P32-1": ["newest player package"]}, got)
        d = ps.annotate(doc_of(items, prompts), {}, None)
        self.assertEqual([], {x["id"]: x["needs"] for s in d["sessions"]["list"] for x in s["items"]}["P31-1"], "no record: no guess")
        d = ps.annotate(doc_of(items, prompts), {}, dep, {"version": "x", "at": "2026-10-18T12:00:00Z"})
        self.assertEqual([], {x["id"]: x["needs"] for s in d["sessions"]["list"] for x in s["items"]}["P32-1"], "a package published after the prompt")
        self.assertIn("rebuild test shard", [s for s in d["sessions"]["list"] if any(x["id"] == "P31-1" for x in s["items"])][0]["needs"])

    def test_the_stale_rules_flag_superseded_unparsed_and_old_address_items_and_the_listed_ones(self):
        items = [item("P62-2", "P62", where="player"), item("P58-0", "P58", what="P58: checklist not parsed, read the notes"),
                 item("P88-1", "P88", where="outside", what="open http://192.168.1.58:8093/ on the phone"),
                 item("P73-7", "P73"), item("P90-1", "P90", what="see http://192.168.1.61:8093/"),
                 item("P91-1", "P91", what="P91: checklist not parsed"), item("P92-1", "P92", who="bot", where="bot", what="192.168.1.58:3000")]
        spec = {"sessions": [{"id": "s", "items": ["P91-1"]}], "superseded": {"P62": "P138 refit them"},
                "stale": {"items": [{"id": "P73-7", "reason": "done long ago"}]}}
        d = ps.annotate(doc_of(items), spec)
        st = by_id(d)["stale"]
        self.assertEqual(["P73-7", "P58-0", "P62-2", "P88-1"], [x["id"] for x in st["items"]], "the listed first, then by prompt")
        r = {x["id"]: x["reason"] for x in st["items"]}
        self.assertEqual("done long ago", r["P73-7"])
        self.assertIn("P138 refit them", r["P62-2"])
        self.assertIn("not parsed", r["P58-0"])
        self.assertIn("old page address", r["P88-1"])
        self.assertEqual(["P90-1"], [x["id"] for s in d["sessions"]["list"] if s["kind"] == "auto" for x in s["items"]],
                         "the Haven address is not stale; a seeded item and a Bot item are never in the stale group")
        self.assertEqual("s", d["sessions"]["upNext"], "the stale group is never Up next while a real session is open")

    def test_the_card_words_use_the_steps_only_when_they_fit_the_item(self):
        good = item("P50-1", "P50", what="`[add TheOverdraft` next to your character", expect="about one and a half humans tall",
                    steps={"where": "Test shard, SL TEST - Admin (Eve)", "do": ["`[add TheOverdraft` and stand next to it"], "pass": "It reads as a walking strongbox one and a half humans tall"})
        shifted = item("P50-2", "P50", what="a fresh tutorial character beside `[add SafeDepositBox`", expect="it springs and bites",
                       steps={"where": "x", "do": ["`[add CropCrow`, `[add Bird` side by side"], "pass": "The crow is black"})
        holder = item("P50-0", "P50", what="P50: checklist not parsed, read the notes", steps={"do": ["`[version`"], "pass": "plain lines"})
        self.assertEqual(("`[add TheOverdraft` and stand next to it", "It reads as a walking strongbox one and a half humans tall", "Test shard, SL TEST - Admin (Eve)"), ps.words(good))
        self.assertEqual(("a fresh tutorial character beside `[add SafeDepositBox`", "it springs and bites", ""), ps.words(shifted))
        self.assertEqual(("`[version`", "plain lines", ""), ps.words(holder))
        self.assertEqual("open the bag.", ps.words(item("P50-3", "P50", what="open the bag. Pass"))[0])

    def test_no_sessions_file_still_gives_automatic_sessions(self):
        d = ps.annotate(doc_of([item("P10-1", "P10")]), None)
        self.assertEqual((False, ["auto-admin-1"]), (d["sessions"]["available"], [s["id"] for s in d["sessions"]["list"]]))

    def test_several_items_go_later_in_one_write_or_none_do(self):
        root = tempfile.mkdtemp(prefix="p164-later-")
        try:
            os.makedirs(os.path.join(root, "testing"))
            doc = pt.new_doc()
            doc["items"] += [pt.new_item(id="P1-1", prompt="P1", source="notes", what="a"), pt.new_item(id="P1-2", prompt="P1", source="notes", what="b")]
            pt.save(root, doc)
            with self.assertRaises(KeyError):
                pt.set_later_many(root, [("P1-1", "x"), ("P1-9", "y")])
            self.assertEqual(["open", "open"], [i["status"] for i in pt.load(os.path.join(root, pt.DATA_REL))["items"]])
            out = pt.set_later_many(root, [("P1-1", "probably stale: one"), ("P1-2", "probably stale: two")], by="chase")
            self.assertEqual(["later", "later"], [i["status"] for i in out])
            got = {i["id"]: i for i in pt.load(os.path.join(root, pt.DATA_REL))["items"]}
            self.assertEqual(("probably stale: two", "chase"), (got["P1-2"]["note"], got["P1-2"]["by"]))
            self.assertTrue(got["P1-1"]["resultAt"])
        finally:
            shutil.rmtree(root, ignore_errors=True)


def free_port():
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


TRIAGE = """| P900-1 | EYES | look |
| P900-2 | EYES | look |
| P900-3 | BOT-PARTIAL | the bot, then you |
| P900-4 | BOT | the bot |
| P901-1 | EYES | look |
| P901-2 | DEPLOY | console |
| P62-2 | EYES | old frames |
"""
STEPS = {"schema": 1, "items": {
    "P900-1": {"where": "Test shard, SL TEST - Admin (Eve)", "do": ["`[add TheOverdraft` and stand beside it"], "pass": "The Overdraft stands one and a half humans tall"},
    "P900-2": {"where": "Test shard, SL TEST - Admin (Eve)"},
    "P900-3": {"where": "Test shard, SL TEST - Human (Ringo)"},
    "P901-1": {"where": "Test shard, SL TEST - Admin (Eve)"},
    "P901-2": {"where": "Shard Console on the game PC"},
    "P62-2": {"where": "Test shard, SL TEST - Elf"}}}
SPEC = {"schema": 1, "sessions": [{"id": "burrows", "title": "Rootdeep Burrows and the tutorial", "why": "Seed them, then walk them.",
                                    "before": ["Rebuild the test shard", "Log in as Admin (Eve)"],
                                    "items": ["P900-1", "P900-2", "P900-3", "P900-4"]}],
        "superseded": {"P62": "P138 refit the kitsune ears and tail"}}


def make_root(prefix):
    root = tempfile.mkdtemp(prefix=prefix)
    for d in ("notes", "docs", "testing"):
        os.makedirs(os.path.join(root, d))
    Path(root, "testing", "bot-triage.md").write_text(TRIAGE, encoding="utf-8")
    Path(root, "testing", "playtest-steps.json").write_text(json.dumps(STEPS), encoding="utf-8")
    Path(root, "testing", "sessions.json").write_text(json.dumps(SPEC), encoding="utf-8")
    doc = pt.new_doc()
    for iid, what, expect in (("P900-1", "`[add TheOverdraft` next to you", "one and a half humans tall"),
                              ("P900-2", "kill The Overdraft in the Strongroom", "the crawlway opens"),
                              ("P900-3", "step on the rocks at 5160,1159", "you go through"),
                              ("P900-4", "the bot walks the Burrows", "no errors"),
                              ("P901-1", "a fresh character beside a SafeDepositBox", "it bites"),
                              ("P901-2", "Shard Console > Test: Rebuild", "the shard starts"),
                              ("P62-2", "ears on her head above the hair", "tail behind the hip")):
        doc["items"].append(pt.new_item(id=iid, prompt=iid.split("-")[0], source="notes", what=what, expect=expect,
                                        position=int(iid.split("-")[1])))
    doc["prompts"] = {"P900": {"title": "cc-P900: the Burrows", "importedAt": "2026-10-18T06:00:00Z"},
                      "P901": {"title": "cc-P901: the tutorial chests", "importedAt": "2026-10-18T18:00:00Z"},
                      "P62": {"title": "cc-P62: kitsune frames", "importedAt": "2026-10-03T06:00:00Z"}}
    Path(root, pt.DATA_REL).write_text(json.dumps(pt.ordered_doc(doc)), encoding="utf-8")
    Path(root, "shard-commit.json").write_text(json.dumps({"commit": "835d8d5", "version": "2026.10.18.7", "at": "2026-10-18T16:20:51Z"}), encoding="utf-8")
    return root


def start(root, port, deployed):
    e = {k: v for k, v in os.environ.items() if not k.startswith(("PLAYTESTS_", "ACCESS_", "REPO_STAMP", "SHARD_"))}
    return subprocess.Popen([sys.executable, "-B", str(SERVER), "--root", root, "--lib", str(TOOLS), "--bind", "127.0.0.1",
                             "--port", str(port), "--status-page", os.devnull, "--deployed", deployed,
                             "--import-seconds", "3600", "--reload-seconds", "0"],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e)


def call(port, path, body=None):
    req = urllib.request.Request("http://127.0.0.1:%d%s" % (port, path),
                                 data=None if body is None else json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "null") if path.startswith("/api/") else None
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read().decode("utf-8"))


class ServiceBase(unittest.TestCase):
    deployed_in_snapshot = False

    def setUp(self):
        need()
        self.root = make_root("p164-root-")
        deployed = os.path.join(self.root, "shard-commit.json")
        if self.deployed_in_snapshot:   # Haven: no test world, the record rides in the game PC snapshot
            rec = json.loads(Path(deployed).read_text(encoding="utf-8"))
            os.makedirs(os.path.join(self.root, "ops"))
            Path(self.root, "ops", "gamepc.json").write_text(json.dumps({"receivedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "snapshot": {"testShard": rec}}), encoding="utf-8")
            deployed = os.devnull
        self.port = free_port()
        self.proc = start(self.root, self.port, deployed)
        for _ in range(100):
            if self.proc.poll() is not None:
                self.fail("the service exited: " + self.proc.stdout.read().decode("utf-8", "replace")[-800:])
            try:
                call(self.port, "/nav.js")
                return
            except OSError:
                time.sleep(0.1)
        self.fail("the service did not start")

    def tearDown(self):
        self.proc.terminate()
        self.proc.wait(10)
        self.proc.stdout.close()
        shutil.rmtree(self.root, ignore_errors=True)


class Service(ServiceBase):
    def test_items_carry_the_sessions_and_a_group_goes_later_in_one_call(self):
        code, d = call(self.port, "/api/items")
        self.assertEqual(200, code)
        S = d["sessions"]
        self.assertEqual("burrows", S["upNext"])
        ids = {s["id"]: [x["id"] for x in s["items"]] for s in S["list"]}
        self.assertEqual(["P900-1", "P900-2", "P900-3"], ids["burrows"], "seeded order; the Bot item left out")
        self.assertEqual(["P62-2"], ids["stale"])
        self.assertEqual(["P901-1"], ids["auto-admin-1"])
        self.assertEqual(["P901-2"], ids["auto-outside-1"])
        cards = {x["id"]: x for s in S["list"] for x in s["items"]}
        self.assertEqual(["rebuild test shard"], cards["P901-1"]["needs"], "P901 was imported after the deploy at 16:20")
        self.assertEqual([], cards["P901-2"]["needs"], "an outside item needs no rebuild")
        self.assertEqual("The Overdraft stands one and a half humans tall", cards["P900-1"]["pass"])
        self.assertEqual({"bot": 1, "cc": 0}, S["owed"])
        self.assertEqual("2026-10-18T16:20:51Z", S["deployed"]["at"])
        code, r = call(self.port, "/api/sessions/later", {"items": [{"id": "P62-2", "note": "probably stale: replaced"}]})
        self.assertEqual((200, "later"), (code, r["items"][0]["status"]))
        self.assertEqual(404, call(self.port, "/api/sessions/later", {"items": [{"id": "P62-99", "note": "x"}]})[0])
        self.assertEqual(400, call(self.port, "/api/sessions/later", {"items": []})[0])
        code, d = call(self.port, "/api/items")
        st = {s["id"]: s for s in d["sessions"]["list"]}["stale"]
        self.assertEqual((True, "probably stale: replaced"), (st["finished"], {i["id"]: i for i in d["items"]}["P62-2"]["note"]))
        self.assertEqual(200, call(self.port, "/api/result", {"id": "P900-1", "status": "pass"})[0])
        code, d = call(self.port, "/api/items")
        b = {s["id"]: s for s in d["sessions"]["list"]}["burrows"]
        self.assertEqual((1, 3, "burrows"), (b["doneCount"], b["total"], d["sessions"]["upNext"]))


class ServiceOnHaven(ServiceBase):
    deployed_in_snapshot = True

    def test_on_haven_the_deploy_record_comes_from_the_game_pc_snapshot(self):
        code, d = call(self.port, "/api/items")
        self.assertEqual("2026.10.18.7", d["sessions"]["deployed"]["version"])
        cards = {x["id"]: x for s in d["sessions"]["list"] for x in s["items"]}
        self.assertEqual(["rebuild test shard"], cards["P901-1"]["needs"])
        self.assertIn("2026.10.18.7 (test shard, 835d8d5)", call(self.port, "/api/bugs")[1]["version"], "and a bug report made on Haven carries the version")


def chrome():
    """A headless Chrome through Selenium, or a reason it is not here."""
    try:
        from selenium import webdriver
    except ImportError:
        return None, "selenium is not installed (pip install selenium)"
    o = webdriver.ChromeOptions()
    for a in ("--headless=new", "--disable-gpu", "--no-first-run", "--window-size=500,900"):
        o.add_argument(a)
    try:
        return webdriver.Chrome(options=o), ""
    except Exception as e:  # no Chrome, no driver
        return None, "no headless Chrome: %s" % e


class Browser(ServiceBase):
    """P112's check in a browser, kept as a test: the page on a phone-sized viewport, and Pass on a card."""

    def setUp(self):
        super().setUp()
        self.driver, why = chrome()
        if self.driver is None:
            self.skipTest(why)
        # A 390 px wide phone (an iPhone's CSS width); headless Chrome's own window cannot go below 500.
        self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 3, "mobile": True})

    def tearDown(self):
        if getattr(self, "driver", None):
            self.driver.quit()
        super().tearDown()

    def wait(self, fn, what, seconds=10):
        end = time.time() + seconds
        while time.time() < end:
            try:
                v = fn()
                if v:
                    return v
            except Exception:
                pass
            time.sleep(0.1)
        self.fail("timed out waiting for " + what + "; page text: " + self.driver.find_element("tag name", "body").text[:600])

    def test_up_next_renders_on_a_390px_phone_and_pass_on_a_card_records_a_result(self):
        d = self.driver
        d.get("http://127.0.0.1:%d/" % self.port)
        d.execute_script("localStorage.setItem('pt-filter', 'all');")
        d.get("http://127.0.0.1:%d/" % self.port)
        sess = self.wait(lambda: d.find_element("id", "session"), "the session")
        self.assertEqual(390, d.execute_script("return window.innerWidth"))
        self.assertIn("Rootdeep Burrows and the tutorial", sess.text)
        self.assertIn("Before you start", sess.text)
        self.assertEqual("0 of 3 done", d.find_element("id", "progress").text)
        self.assertLessEqual(d.execute_script("return document.documentElement.scrollWidth"), 390, "no sideways scrolling")
        self.assertEqual("true", d.find_element("css selector", '.filters button[data-f="next"]').get_attribute("aria-pressed"), "it opens on Up next, whatever filter was last used")
        self.assertFalse(d.find_element("id", "where-chips").is_displayed(), "the full list's chips are one tap away, not here")
        cards = d.find_elements("css selector", ".scard.todo")
        self.assertEqual(3, len(cards))
        first = cards[0]
        self.assertTrue(first.find_element("css selector", ".sline").text.startswith("[add TheOverdraft"))
        self.assertNotIn("P900-1", first.find_element("css selector", ".sline").text, "no id in the main line")
        self.assertEqual("P900-1", first.find_element("css selector", ".sid").text, "the id small, under the card")
        for b in first.find_elements("css selector", ".sact button"):
            self.assertGreaterEqual(b.size["height"], 44, "big tap targets: " + b.text)
        self.assertIn("Not yours: the overnight bot still owes 1", d.find_element("css selector", ".owed").text)
        first.find_element("css selector", 'button[data-ss="pass"]').click()
        self.wait(lambda: d.find_element("id", "progress").text == "1 of 3 done", "the progress line to move")
        got = {i["id"]: i for i in json.loads(Path(self.root, pt.DATA_REL).read_text(encoding="utf-8"))["items"]}
        self.assertEqual("pass", got["P900-1"]["status"], "Pass on a card is recorded")
        self.assertEqual(2, len(d.find_elements("css selector", ".scard.todo")))
        # Fail asks for its one line inline, and refuses an empty one.
        card = d.find_elements("css selector", ".scard.todo")[0]
        self.assertFalse(card.find_element("css selector", ".sfail").is_displayed(), "the note box waits for Fail")
        card.find_element("css selector", 'button[data-ss="fail"]').click()
        self.assertTrue(card.find_element("css selector", ".sfail").is_displayed())
        card.find_element("css selector", ".sfail input").send_keys("the crawlway stayed shut")
        card.find_element("css selector", 'button[data-ss="failsave"]').click()
        self.wait(lambda: d.find_element("id", "progress").text == "2 of 3 done", "the Fail to save")
        got = {i["id"]: i for i in json.loads(Path(self.root, pt.DATA_REL).read_text(encoding="utf-8"))["items"]}
        self.assertEqual(("fail", "the crawlway stayed shut"), (got["P900-2"]["status"], got["P900-2"]["note"]))
        # Next goes to the next session; All items is the full list, unchanged.
        d.find_element("css selector", 'button[data-sn="1"]').click()
        self.wait(lambda: "the tutorial chests" in d.find_element("id", "session").text, "the next session")
        self.assertIn("needs: rebuild test shard", d.find_element("id", "session").text)
        d.find_element("css selector", '.filters button[data-f="items"]').click()
        self.wait(lambda: d.find_element("id", "where-chips").is_displayed(), "the full list")
        self.assertTrue(d.find_elements("css selector", "#list .item"), "the full list's cards")


class Page(unittest.TestCase):
    def test_the_page_opens_on_up_next_and_stays_ascii(self):
        t = PAGE.read_text(encoding="utf-8")
        self.assertTrue(all(ord(c) < 128 for c in t), "ASCII only")
        self.assertIn("var filter = 'next';", t)
        self.assertIn('data-f="items"', t)
        self.assertIn("/api/sessions/later", t)


class RealFiles(unittest.TestCase):
    def setUp(self):
        need()
        self.spec = json.loads((ROOT / "testing" / "sessions.json").read_text(encoding="utf-8"))
        self.items = {i["id"]: i for i in json.loads((ROOT / "testing" / "play-tests.json").read_text(encoding="utf-8"))["items"]}

    def test_the_seeded_sessions_name_real_items_once_each_six_to_twelve_a_session(self):
        seen = []
        for s in self.spec["sessions"]:
            self.assertRegex(s["id"], r"^[a-z0-9-]+$")
            self.assertTrue(s["title"] and s["why"] and s["before"], s["id"])
            self.assertTrue(6 <= len(s["items"]) <= 12, "%s has %d" % (s["id"], len(s["items"])))
            for i in s["items"]:
                self.assertIn(i, self.items, "%s lists %s, which is not on the page" % (s["id"], i))
            seen += s["items"]
        for e in self.spec["stale"]["items"]:
            self.assertIn(e["id"], self.items)
            self.assertTrue(e["reason"])
            seen.append(e["id"])
        self.assertEqual(len(seen), len(set(seen)), "each id once")
        raw = (ROOT / "testing" / "sessions.json").read_text(encoding="utf-8")
        self.assertTrue(all(ord(c) < 128 for c in raw), "ASCII only")

    def test_the_seed_is_the_overseers_plan_of_2026_10_18(self):
        titles = [s["title"] for s in self.spec["sessions"]]
        self.assertEqual("Rootdeep Burrows and the tutorial", titles[0])
        self.assertEqual(["P141-7", "P140-6", "P140-5", "P141-3", "P141-4", "P140-3", "P140-4", "P142-6", "P142-7"], self.spec["sessions"][0]["items"])
        self.assertEqual(7, len(titles), "the plan's six sessions, its fourth split in two")
        self.assertIn("P62", self.spec["superseded"])


if __name__ == "__main__":
    unittest.main()
