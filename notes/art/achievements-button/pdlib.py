"""Loads cc-P81's gump reader (design/paperdoll-sos/tools/render.py, up to its tiledata part) for the P147 mockups."""
src = open(r"D:/ShatteredLegacy/design/paperdoll-sos/tools/render.py", encoding="utf-8").read()
src = src.split("# tiledata static entries")[0]
src = src.replace("os.makedirs(OUT, exist_ok=True)", "")
NS = {"__name__": "pdlib_render"}
exec(compile(src, "render.py", "exec"), NS)
gump = NS["gump"]
