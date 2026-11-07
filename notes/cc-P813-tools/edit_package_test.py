r"""cc-P813: the package test edits (Build-UoOverrides.Tests.ps1): the new fact and the registry counts.

    python -P edit_package_test.py <Build-UoOverrides.Tests.ps1> <new fact .ps1>
"""

import sys

p, fact_path = sys.argv[1], sys.argv[2]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
fact = open(fact_path, encoding="utf-8").read().replace("\r\n", "\n").replace("\n", nl)

anchor = "Fact 'EveryRegistryRowsHexIsItsId' {"
assert s.count(anchor) == 1
s = s.replace(anchor, fact + anchor)

reps = [
    ("-and ([int]$_.id -lt 46690 -or [int]$_.id -gt 46709) })",
     "-and ([int]$_.id -lt 46690 -or [int]$_.id -gt 46709) -and [int]$_.id -ne 46710 })"),
    ("    # cc-P632: the scoring archery butte's hit pictures (46690-46709), checked by their own fact.\n    $k =",
     "    # cc-P632: the scoring archery butte's hit pictures (46690-46709), checked by their own fact.\n"
     "    # cc-P813: the Hall of Finishers banner (46710), checked by its own fact.\n    $k ="),
    ("    # cc-P665 the two vision panel gumps (23209-23210), fixed in cc-P674.\n    Assert-Equal 803 $reg.Count 'registry rows'   # cc-P665",
     "    # cc-P665 the two vision panel gumps (23209-23210), fixed in cc-P674; cc-P813 the twelve Claude Design gumps\n"
     "    # (23211-23222) and the Finishers banner art 46710.\n"
     "    Assert-Equal 816 $reg.Count 'registry rows'   # cc-P813: + 12 gumps + 1 art; cc-P665"),
    ("'gump rows: 64783, 54783, 22456-22458, 22459-22468, 22469, 23052-23080 (cc-P362), 23200-23208 (cc-P436) and 23209-23210 (cc-P665)'",
     "'gump rows: 64783, 54783, 22456-22458, 22459-22468, 22469, 23052-23080 (cc-P362), 23200-23208 (cc-P436), 23209-23210 (cc-P665) and 23211-23222 (cc-P813)'"),
    ("    Assert-Equal 56 @($reg | Where-Object { $_.kind -eq 'gump' }).Count",
     "    Assert-Equal 68 @($reg | Where-Object { $_.kind -eq 'gump' }).Count"),
    ("    Assert-Equal 672 @($reg | Where-Object { $_.kind -eq 'art' }).Count 'art rows (cc-P632: + 20 butte pictures)'",
     "    Assert-Equal 673 @($reg | Where-Object { $_.kind -eq 'art' }).Count 'art rows (cc-P632: + 20 butte pictures; cc-P813: + the Finishers banner)'"),
]
for a, b in reps:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)

open(p, "w", encoding="utf-8", newline="").write(s)
print("edited", p)
