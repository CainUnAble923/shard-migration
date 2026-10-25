"""cc-P146: where each open play-test item is done, so Chase can take everything he can do in one sitting.

Every open, later or blocked item gets exactly one Where (it["where"] = {key, label, chars}):

    questions  Questions            a decision (Who: You decide; every decision item from tools/decisions.py)
    outside    Outside the game     console tabs, web pages, desktop, files, the updater, a phone
    admin      In game: Admin       needs the Admin test account (Eve) or staff commands
    player     In game: Player      a normal character; chars names the test accounts the steps name (human, gargoyle,
                                    elf), or is empty for any character
    bot        Bot                  the overnight bot settles it (the page's Bot chip)
    cc         CC                   Claude Code settles it from files (the page's CC chip)

It comes from the item's Who (tools/playwho.py) and, for Chase's items, from the steps' Where line in
testing/playtest-steps.json. An item whose line is unclear sets "place" (and "chars") in its steps entry by hand, and
that wins. Nothing is written back.
"""
import re

KEYS = ("questions", "outside", "admin", "player", "bot", "cc")
LABELS = {"questions": "Questions", "outside": "Outside the game", "admin": "In game: Admin",
          "player": "In game: Player", "bot": "Bot", "cc": "CC"}
CHARS = ("human", "gargoyle", "elf")
CHAR_LABELS = {"human": "Human", "gargoyle": "Gargoyle", "elf": "Elf", "any": "Any character"}
OPEN = ("open", "later", "blocked")

ADMIN = re.compile(r"(?i)\badmin\b(?!\s+console)|\bEve\b|game ?master|\badministrator\b|\bstaff\b")
PLAYER = re.compile(r"(?i)^(the )?test shard\b|\bSL TEST\b|\bSL - TazUO\b|\bTazUO\b|\bcharacter\b|\bin game\b|"
                    r"\bRingo\b|\bGarg\b|\btutorial\b")
CHAR_RE = (("human", re.compile(r"(?i)\bhuman\b|\bRingo\b")), ("gargoyle", re.compile(r"(?i)\bgargoyle\b|\bGarg\b")),
           ("elf", re.compile(r"(?i)\belf\b")))


def chars_of(text):
    return [c for c, rx in CHAR_RE if rx.search(text or "")]


def classify(who_key, steps):
    """(key, chars) for one item: from its Who, its steps' hand-set place, or its steps' Where line."""
    s = steps or {}
    if s.get("place") in KEYS:
        return s["place"], [c for c in (s.get("chars") or []) if c in CHARS]
    if who_key == "decide":
        return "questions", []
    if who_key in ("bot", "cc"):
        return who_key, []
    where = s.get("where") or ""
    if not where:
        return "", []
    if ADMIN.search(where):
        return "admin", []
    if PLAYER.search(where):
        return "player", chars_of(where)
    return "outside", []


def where_of(key, chars):
    return {"key": key, "label": LABELS.get(key, ""), "chars": chars}


def annotate(doc):
    """After playwho (and decisions): it["where"] on every open item that has a Who, doc["where"] with the counts
    over open items and the items that have none."""
    missing = []
    for it in doc.get("items", []):
        if it.get("status") not in OPEN or "who" not in it:
            continue
        key, chars = classify(it["who"].get("key"), it.get("steps"))
        if not key:
            missing.append(it["id"])
            continue
        it["where"] = where_of(key, chars)
    doc["where"] = {"labels": dict(LABELS), "charLabels": dict(CHAR_LABELS), "missing": missing,
                    "counts": counts(shown_items(doc, "open"))}
    return doc


def char_match(item, char):
    """The Player sub-chip: a named account, or 'any' for an item that names none."""
    chars = (item.get("where") or {}).get("chars") or []
    return (not chars) if char == "any" else char in chars


def counts(items):
    """{key: n} for each Where, plus {"chars": {human, gargoyle, elf, any}} among the Player ones."""
    out = dict.fromkeys(KEYS, 0)
    ch = dict.fromkeys(CHARS + ("any",), 0)
    for it in items:
        w = it.get("where") or {}
        if w.get("key") in out:
            out[w["key"]] += 1
            if w["key"] == "player":
                for c in ch:
                    if char_match(it, c):
                        ch[c] += 1
    out["chars"] = ch
    return out


MINE = ("you", "botyou", "decide")


def primary(item, flt):
    """The page's filter buttons (index.html shown()), for an item or a decision. Kept the same as the page."""
    dec = item.get("kind") == "decision"
    st = item.get("state") if dec else item.get("status")
    if item.get("replacedBy") and flt != "all":
        return False
    who = (item.get("who") or {}).get("key", "")
    if dec:
        if flt == "open":
            return st in ("open", "later", "answered", "archived")
        if flt == "mine":
            return st in ("open", "later")
        if flt == "answered":
            return st == "answered" or st == "archived" and item.get("answerStatus") == "answered"
        return flt == "all"
    if flt == "answered":
        return False
    if flt == "mine":
        return st in OPEN and who in MINE
    if flt == "whobot":
        return st in OPEN and who == "bot"
    if flt == "cc":
        return st in OPEN and who == "cc"
    if flt == "open":
        return st in OPEN
    if flt == "fail":
        return st == "fail"
    return flt == "all"


def shown_items(doc, flt, where="", char=""):
    """Items and decisions the page shows for a filter button plus a Where chip (and a Player sub-chip)."""
    out = []
    for it in list(doc.get("items", [])) + list(doc.get("decisions", [])):
        if not primary(it, flt):
            continue
        if where and (it.get("where") or {}).get("key") != where:
            continue
        if where == "player" and char and not char_match(it, char):
            continue
        out.append(it)
    return out
