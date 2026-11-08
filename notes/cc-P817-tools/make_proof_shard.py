"""cc-P817: proof-shard.ps1 from P769's, without the isle overlay (main's land is stock Trammel), as P813 ran it."""
src = r"D:\UO\golems\Iron\shard-migration\notes\cc-P769-tools\proof-shard.ps1"
dst = r"D:\UO\golems\Iron\shard-migration\notes\cc-P817-tools\proof-shard.ps1"
s = open(src, encoding="utf-8").read()
s = s.replace("$name = 'sl-p762-proof'", "$name = 'sl-p817-proof'")
s = s.replace("[string]$Image = 'sl-modernuo:cc-p762',", "[string]$Image = 'sl-modernuo:cc-p817',")
s = s.replace("$j.dataDirectories = @('/var/lib/uo/client-data/sl-map-overlay', '/var/lib/uo/client-data/classic-client')",
              "# cc-P817: the overlay only when -Overlay is given (the bank's new statics); otherwise the client data copy\n"
              "$j.dataDirectories = $(if ($Overlay) { @('/var/lib/uo/client-data/sl-map-overlay', '/var/lib/uo/client-data/classic-client') } else { @('/var/lib/uo/client-data/classic-client') })")
s = s.replace("'Shattered Legacy P762 new-character lockdown proof'", "'Shattered Legacy P817 creation and wake proof'")
a = s.index("$ovDir = if ($Overlay)")
b = s.index("docker run -d -t")
s = s[:a] + "$ovArgs = @()\nif ($Overlay) { $ovArgs = @('-v', (($Overlay -replace '\\\\', '/') + ':/var/lib/uo/client-data/sl-map-overlay:ro')) }\n" + s[b:]
old = "    -v 'D:/UO/tool-trials/client-data-copy:/var/lib/uo/client-data/classic-client:ro' `\n    -v \"${ov}:/var/lib/uo/client-data/sl-map-overlay:ro\" $Image"
assert old in s
s = s.replace(old, "    -v 'D:/UO/tool-trials/client-data-copy:/var/lib/uo/client-data/classic-client:ro' @ovArgs $Image")
s = s.replace("<#\n  proof-shard.ps1 (cc-P762", "<#\n  proof-shard.ps1 (cc-P817: the isle overlay only with -Overlay; cc-P762", 1)
open(dst, "w", encoding="utf-8").write(s)
print("ok")
