"""cc-P436 step 1: three looks for the guild and League gumps, drawn from art on disk, beside today's stock look.

Each preview draws three real gumps at their real coordinates (the Add* calls of MinersCompactLiaisonGump's Member
Dashboard, LeagueRegistrarGump's main page and ForestersGuildmasterGump's main menu, 440 x 420 each), swapping only
the art a style helper would swap: the frame (9270), the inside (2624 panel or alpha region), the rule (9304) and the
row, back and close buttons (4011, 4014, 4023). Text keeps the gumps' own hues. Not the client's font: Tahoma 12 stands
in for the UO font, so line lengths are close but not exact.
    python -P previews.py        -> previews\\look-*.png and previews\\pieces-*.png
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -P leaves the script's folder off the path
import gumpkit as k  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "previews")

CC0_UI = r"D:\UO\third-party\uo-art-mods\ultima_online_mods-main\UI\GumpOverrides"
FMT = r"D:\UO\golems\Iron\ShatteredLegacy\player-package\vendor\fiddle-me-this\[Custom]\ExternalImages\gumps"
ERAD = os.path.join(r"D:\UO\third-party\erads-custom-content", "Erad's Custom UO Content", "Client",
                    "UO Gump Basalt Edition", "Character Status Basalt .bmp")

W, H = 440, 420

# Label hues as the client draws them (hues.mul entry hue + 1, ClusterFRequirements.cs's table).
HUE = {999: (172, 172, 172), 1153: (222, 246, 246), 1154: (74, 238, 49), 0x44: (74, 238, 49), 0x22: (246, 98, 131)}


def cc0(gid):
    return k.png(os.path.join(CC0_UI, "0x%04X.png" % gid), False)


def fmt(gid):
    return k.png(os.path.join(FMT, "%d.png" % gid), False)


# -- The looks -----------------------------------------------------------------------------------------------------


class Look:
    def __init__(self, name, frame, inside, rule, buttons, note):
        self.name = name
        self.frame = frame        # nine images
        self.inside = inside      # (image to tile, inset) or None: the frame's own centre shows
        self.rule = rule          # image tiled for AddImageTiled(..., 9304)
        self.buttons = buttons    # stock button id -> image
        self.note = note


def stock_look():
    return Look(
        "today (stock)", k.nine(k.stock, 9270), (k.stock(2624), 8), k.stock(9304),
        {g: k.stock(g) for g in (4011, 4014, 4023)},
        "frame 9270, panel 2624, rule 9304, buttons 4011 / 4014 / 4023 (all stock)",
    )


def celtic_look():
    # CorvaeOboro's dark redraw of the 2600 frame (Celtic knots in the corners), CC0; his dark arrow and close buttons
    # (4005, 4017) stand in for the row and close buttons; back keeps stock 4014. Rule: the bright top 2 rows of his
    # frame's top edge (measured: rows 0-2 are the edge's highlight, the rest is the dark field).
    frame = k.nine(cc0, 2600)
    rule = frame[1].crop((0, 0, frame[1].width, 2))
    return Look(
        "A. Dark Celtic", frame, None, rule,
        {4011: cc0(4005), 4014: k.stock(4014), 4023: cc0(4017)},
        "CorvaeOboro, uo-art-mods UI (CC0): frame = his 2600 redraw (9 pieces), buttons = his 4005 and 4017",
    )


def basalt_frame():
    """Erad's Basalt status gump cut into nine pieces: the braided bronze border and the dark basalt inside."""
    src = Image.open(ERAD).convert("RGBA")
    x0, y0, b = 20, 21, 12               # the outer border's corner and a 12-pixel slice (6 px braid + stone)
    tl = src.crop((x0, y0, x0 + b, y0 + b))
    top = src.crop((x0 + 40, y0, x0 + 40 + 96, y0 + b))
    left = src.crop((x0, y0 + 30, x0 + b, y0 + 30 + 96))
    # The inside: the title strip's plain basalt, columns 30-219 (measured: bronze at 20-25, then the "Character
    # Status" lettering from 223), stacked mirror-wise so it tiles.
    strip = src.crop((30, y0 + 7, 220, y0 + 7 + 11))
    centre = Image.new("RGBA", (190, 44))
    for i in range(4):
        centre.alpha_composite(strip if i % 2 == 0 else strip.transpose(Image.FLIP_TOP_BOTTOM), (0, i * 11))
    tr = tl.transpose(Image.FLIP_LEFT_RIGHT)
    bl = tl.transpose(Image.FLIP_TOP_BOTTOM)
    br = tr.transpose(Image.FLIP_TOP_BOTTOM)
    right = left.transpose(Image.FLIP_LEFT_RIGHT)
    bottom = top.transpose(Image.FLIP_TOP_BOTTOM)
    return [tl, top, tr, left, centre, right, bl, bottom, br], src.crop((x0 + 40, y0, x0 + 136, y0 + 6))


def basalt_look():
    frame, braid = basalt_frame()
    rule = braid.resize((braid.width, 3))
    return Look(
        "B. Stone and bronze", frame, None, rule,
        {g: k.stock(g) for g in (4011, 4014, 4023)},
        "Erachiro, Erad's Custom UO Content (free to use, credit): frame cut from his Basalt status gump (9 pieces), "
        "a bronze-braid rule; buttons stock (their bronze suits it)",
    )


def modern_look():
    # Fiddle-Me-This's custom panel frame 62180-62188 (CC0, already in our package for its XML gumps): flat dark with a
    # thin bronze edge. Rule: its own top edge. Buttons stay stock.
    frame = [fmt(62180 + i) for i in range(9)]
    rule = frame[1].crop((0, 0, frame[1].width, 2))
    return Look(
        "C. Clean modern", frame, None, rule,
        {g: k.stock(g) for g in (4011, 4014, 4023)},
        "NewYears1978, Fiddle-Me-This (CC0, already shipped in our package): frame 62180-62188; buttons stock",
    )


# -- The gumps (their real Add* calls, from the source) ----------------------------------------------------------


class G:
    def __init__(self, look):
        self.look = look
        self.c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        k.background(self.c, look.frame, 0, 0, W, H)
        if look.inside:
            img, inset = look.inside
            k.tile(self.c, img, inset, inset, W - 2 * inset, H - 2 * inset)

    def rule(self, x, y, w, h):
        k.tile(self.c, self.look.rule, x, y, w, h)

    def label(self, x, y, hue, text):
        k.label(self.c, x, y, HUE.get(hue, hue) if isinstance(hue, int) else hue, text)

    def button(self, x, y, gid):
        img = self.look.buttons.get(gid)
        if img is not None:
            self.c.alpha_composite(img, (x, y))

    def row(self, x, y, text, hue=999):
        self.button(x, y, 4011)
        self.label(x + 26, y + 2, hue, text)

    def footer(self, back=True):
        self.rule(10, H - 38, W - 20, 2)
        if back:
            self.button(18, H - 28, 4014)
            self.label(40, H - 26, 999, "Back")
        self.button(W - 50, H - 28, 4023)
        self.label(W - 28, H - 26, 1153, "X")


def miners_dashboard(look):
    g = G(look)
    g.label(W // 2 - 80, 12, 1153, "Miners' Compact")
    g.label(W // 2 - 60, 28, 999, "New Haven Liaison")
    g.rule(10, 48, W - 20, 2)
    g.label(18, 56, 1153, "Member Dashboard")
    g.rule(10, 72, W - 20, 1)
    for i, (colour, text) in enumerate([
        ((255, 215, 0), "Rank: Journeyman"), ((170, 170, 170), "Compact Standing: 6,200"),
        ((170, 170, 170), "Mining Vouchers: 42"), (None, ""),
        ((136, 136, 136), "Initiate (0) > Apprentice (1,000) > Journeyman (5,000)"),
        ((136, 136, 136), "Surveyor (15,000) > Master Delver (40,000)"),
        ((136, 136, 136), "Deepwarden (80,000) > Legendary Prospector (150,000)"),
    ]):
        if colour:
            g.label(16, 78 + i * 18, colour, text)
    g.rule(10, 216, W - 20, 1)
    g.row(18, 226, "Work Orders"); g.row(230, 226, "Learn Stone Mining")
    g.row(18, 250, "Restoration (Jacob's Pickaxe)")
    g.row(18, 274, "Upgrade to Tier 2 (Reinforced Pickaxe)")
    g.row(18, 298, "Upgrade Ore Satchel"); g.row(230, 298, "Climbing Boots")
    g.row(18, 322, "Replace Starting Kit")
    g.rule(10, 348, W - 20, 1)
    g.row(18, 356, "Civic Mule Exchange (mule upgrades)", 1153)
    g.footer()
    return g.c


def league_board(look):
    g = G(look)
    g.label(W // 2 - 120, 12, 1153, "League of Extraordinary Citizens")
    g.label(W // 2 - 75, 28, 999, "New Haven Field Office")
    g.rule(10, 48, W - 20, 2)
    g.label(18, 56, 999, "Welcome, Chase.")
    g.label(18, 72, (170, 170, 170), "Your League rank:")
    g.label(220, 72, (255, 215, 0), "Citizen of Note")
    g.rule(10, 96, W - 20, 1)
    y = 106
    for left, right in [("Citizen Status", "League Register"), ("About Renown", None), ("Achievements", "League Shop"),
                        ("Guilds Overview", "Titles"), ("Guild Referrals", None), ("League Dispatch", None),
                        ("Where to go first?", None), ("League Rank", "Requisitions board"),
                        ("The Compact's Mule (errand)", None)]:
        g.row(18, y, left)
        if right:
            g.row(230, y, right)
        y += 28
    g.footer(back=False)
    return g.c


def foresters_page(look):
    g = G(look)
    g.label(W // 2 - 70, 12, 1153, "Foresters' Union")
    g.label(W // 2 - 65, 28, 999, "Cedric Rowanwood")
    g.rule(10, 48, W - 20, 2)
    g.label(18, 56, 999, "What brings you to the wood yard, friend?")
    g.rule(10, 72, W - 20, 1)
    y = 82
    for text in ("About the Foresters' Union", "What We Harvest", "Joining Requirements", "Rewards and Timber Tokens"):
        g.row(18, y, text)
        y += 28
    y += 8
    g.rule(10, y, W - 20, 1)
    y += 8
    g.row(18, y, "Member Dashboard")
    g.footer(back=False)
    return g.c


def sheet(look, path):
    gumps = [miners_dashboard(look), league_board(look), foresters_page(look)]
    pad = 16
    out = Image.new("RGBA", (pad + len(gumps) * (W + pad), H + 2 * pad + 40), (46, 52, 40, 255))
    k.label(out, pad, 6, (255, 255, 255), f"{look.name}:  {look.note}")
    for i, gimg in enumerate(gumps):
        out.alpha_composite(gimg, (pad + i * (W + pad), pad + 24))
    out.convert("RGB").save(path)


def pieces(look, path):
    """The look's own pieces, one per new gump ID it would need, laid out with their sizes."""
    imgs = list(look.frame) + [look.rule] + [look.buttons[g] for g in (4011, 4014, 4023)]
    w = sum(max(i.width, 40) + 12 for i in imgs) + 12
    h = max(i.height for i in imgs) + 40
    out = Image.new("RGBA", (min(w, 3000), h), (70, 70, 70, 255))
    x = 12
    for i in imgs:
        out.alpha_composite(i.crop((0, 0, min(i.width, 400), i.height)), (x, 24))
        k.label(out, x, 4, (255, 255, 255), f"{i.width}x{i.height}")
        x += min(max(i.width, 40), 400) + 12
    out.convert("RGB").save(path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for tag, make in (("0-stock", stock_look), ("a-dark-celtic", celtic_look), ("b-stone-bronze", basalt_look),
                      ("c-clean-modern", modern_look)):
        look = make()
        sheet(look, os.path.join(OUT, f"look-{tag}.png"))
        if tag != "0-stock":
            pieces(look, os.path.join(OUT, f"pieces-{tag}.png"))
        print("wrote", tag)
