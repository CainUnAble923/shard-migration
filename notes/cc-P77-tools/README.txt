cc-P77 read-only map tools for the Order of the Alembic's hall. Nothing here writes to a save or a world.
fit.py, nhmap.py and rend.py are copies of cc-P15's (see cc-P15-tools/README.txt). Run from this folder.

layout.py    The hall props as data (the same rows as ClusterFAlembicGuild.Hall) and the guildmaster's post.
walk.py      CanFit port with the props added as decoration: checks the post fits at z35 and walks from both doors.
probe.py     Standable z's per tile in a box: python probe.py x0 y0 x1 y1
list.py      Statics (z 30 and up) and pinned New Haven decoration in a box: python list.py x0 y0 x1 y1
signs.py     Sign statics in a box (New Haven's shop signs are not statics; it found none).
rlayout.py   Renders the shop with the props: python rlayout.py <zcut>. PNGs here are git-ignored.
nh_mobiles.txt  Empty on purpose: rend.py reads it for NPC marks; no save copy was used in cc-P77.
