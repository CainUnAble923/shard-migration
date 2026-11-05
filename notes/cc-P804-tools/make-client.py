# cc-P804: client\patches\0011 (a skill no group lists goes to Miscellaneous) and the skill-add in Build-UoOverrides.ps1 with its fact.
import difflib, re
SRC = 'D:/UO/cc-p40-work/tazuo-3212623f/src/ClassicUO.Client/Game/Managers/SkillsGroupManager.cs'
REL = 'src/ClassicUO.Client/Game/Managers/SkillsGroupManager.cs'
R = 'D:/UO/golems/Iron/ShatteredLegacy/'
raw = open(SRC, 'rb').read().decode('utf-8')
nl = '\r\n' if '\r\n' in raw else '\n'
s = raw


def sub(s, a, b):
    a, b = a.replace('\n', nl), b.replace('\n', nl)
    assert s.count(a) == 1, a
    return s.replace(a, b)


n = sub(s, '''                    g.Sort();
                    Add(g);
                }
            }
        }
''', '''                    g.Sort();
                    Add(g);
                }
            }

            AddUnplacedSkills();
        }

        // Shattered Legacy (cc-P804): a skill no group lists (Herbalism, for a profile saved before it existed, or skillgrp.mul,
        // which stops at the stock skills) goes to the first group, so both skill windows show it.
        private void AddUnplacedSkills()
        {
            if (Groups.Count == 0)
            {
                return;
            }

            SkillsGroup misc = Groups.Find(g => g.Name == TazLang.Get("miscellaneous")) ?? Groups[0];
            bool added = false;

            for (int i = 0; i < Client.Game.UO.FileManager.Skills.SkillsCount; i++)
            {
                if (!Groups.Exists(g => g.Contains((byte) i)))
                {
                    misc.Add((byte) i);
                    added = true;
                }
            }

            if (added)
            {
                misc.Sort();
            }
        }
''')
n = sub(n, '''                MakeDefaultBard();
            }

            foreach (SkillsGroup g in Groups)
''', '''                MakeDefaultBard();
            }

            AddUnplacedSkills();

            foreach (SkillsGroup g in Groups)
''')
d = list(difflib.unified_diff(s.split(nl), n.split(nl), 'a/' + REL, 'b/' + REL, n=3, lineterm=''))
body = ''
for i, line in enumerate(d):
    body += line + ('\n' if i < 2 else nl if nl == '\r\n' and not line.startswith('@@') else '\n')
head = '''From 0000000000000000000000000000000000000000 Mon Sep 17 00:00:00 2001
From: Chase Fleming <ckfleming@gmail.com>
Date: Thu, 5 Nov 2026 12:00:00 -0600
Subject: [PATCH] Skills: a skill no group lists goes to Miscellaneous (Shattered Legacy cc-P804)

Both skill windows list only grouped skills, and groups come from the profile's saved
skillsgroups.xml or from skillgrp.mul, neither of which knows a new skill. Herbalism is the first.
---
'''
open(R + 'client/patches/0011-unplaced-skills.patch', 'w', encoding='utf-8', newline='').write(head + 'diff --git a/' + REL + ' b/' + REL + '\n' + body)

p = R + 'player-package/payload/app/Build-UoOverrides.ps1'
b = open(p, encoding='utf-8-sig', newline='').read()
bom = open(p, 'rb').read(3) == b'\xef\xbb\xbf'
nl2 = '\r\n' if '\r\n' in b else '\n'


def sub2(s, a, b_):
    a, b_ = a.replace('\n', nl2), b_.replace('\n', nl2)
    assert s.count(a) == 1, a
    return s.replace(a, b_)


b = sub2(b, "$SkillsStampFormat = 'uo-skills 1'\n", "$SkillsStampFormat = 'uo-skills 2'\n")
b = sub2(b, "# cc-P239 (F-14): the skills we rename for everyone.", "# cc-P804 (F-51): skills we add. TazUO numbers the filled slots in order, so a new one must follow the last filled slot with no gap.\n$SkillAdds = @([pscustomobject]@{ Index = 58; Action = 0; Name = 'Herbalism' })\n\n# cc-P239 (F-14): the skills we rename for everyone.")
b = sub2(b, '''    $renames = ($SkillRenames | ForEach-Object { "$($_.Index) $($_.From) > $($_.To)" }) -join '; '
''', '''    $renames = (@($SkillRenames | ForEach-Object { "$($_.Index) $($_.From) > $($_.To)" }) + @($SkillAdds | ForEach-Object { "$($_.Index) + $($_.Name)" })) -join '; '
''')
b = sub2(b, '''    if ($changed -eq 0) { Stop-Step; return }

    if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
    if (Test-Path -LiteralPath $stampOut) { Remove-Item -LiteralPath $stampOut -Force }
    [IO.File]::WriteAllBytes($outMul, $packed.ToArray())
''', '''    foreach ($add in $SkillAdds) {
        if (($add.Index + 1) * 12 -gt $idx.Length) { continue }    # a small test file with no such slot
        $at = $add.Index * 12
        if ([BitConverter]::ToInt32($idx, $at) -ge 0 -and [BitConverter]::ToInt32($idx, $at + 4) -gt 0) {
            Say-Skip "Shattered Legacy skill names: skill $($add.Index) is left alone: your Ultima Online files already use that slot."
            continue
        }
        if ($add.Index -gt 0 -and ([BitConverter]::ToInt32($idx, $at - 12) -lt 0 -or [BitConverter]::ToInt32($idx, $at - 8) -le 0)) {
            Say-Skip "Shattered Legacy skill names: $($add.Name) is left out: the slot before it is empty in your Ultima Online files."
            continue
        }
        $name  = $ascii.GetBytes($add.Name)
        $entry = New-Object byte[] ($name.Length + 2)
        $entry[0] = [byte]$add.Action
        [Array]::Copy($name, 0, $entry, 1, $name.Length)
        [Array]::Copy([BitConverter]::GetBytes([int]$packed.Position), 0, $newIdx, $at, 4)
        [Array]::Copy([BitConverter]::GetBytes([int]$entry.Length), 0, $newIdx, $at + 4, 4)
        $packed.Write($entry, 0, $entry.Length)
        $changed++
    }
    if ($changed -eq 0) { Stop-Step; return }

    if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
    if (Test-Path -LiteralPath $stampOut) { Remove-Item -LiteralPath $stampOut -Force }
    [IO.File]::WriteAllBytes($outMul, $packed.ToArray())
''')
open(p, 'w', encoding='utf-8-sig' if bom else 'utf-8', newline='').write(b)

t = R + 'player-package/tests/Build-UoOverrides.Tests.ps1'
x = open(t, encoding='utf-8-sig', newline='').read()
bom2 = open(t, 'rb').read(3) == b'\xef\xbb\xbf'
nl3 = '\r\n' if '\r\n' in x else '\n'
fact = '''# cc-P804: slot 58 of a full-size file. Every slot is filled up to 57, then empty to 255, as EA ships it.
function Write-FullSkills([string]$dir) {
    $ascii = New-Object Text.ASCIIEncoding
    $mul = New-Object IO.MemoryStream
    $idx = New-Object IO.MemoryStream
    for ($i = 0; $i -lt 256; $i++) {
        if ($i -lt 58) {
            $name = $ascii.GetBytes("Skill$i")
            $at = [int]$mul.Position
            $mul.WriteByte(0)
            $mul.Write($name, 0, $name.Length)
            $mul.WriteByte(0)
            $idx.Write([BitConverter]::GetBytes($at), 0, 4)
            $idx.Write([BitConverter]::GetBytes($name.Length + 2), 0, 4)
        } else {
            $idx.Write([BitConverter]::GetBytes(-1), 0, 4)
            $idx.Write([BitConverter]::GetBytes(0), 0, 4)
        }
        $idx.Write([BitConverter]::GetBytes(0), 0, 4)
    }
    [IO.File]::WriteAllBytes((Join-Path $dir 'skills.mul'), $mul.ToArray())
    [IO.File]::WriteAllBytes((Join-Path $dir 'Skills.idx'), $idx.ToArray())
}

Fact 'HerbalismIsAddedAtSlot58AndEveryStockSlotIsKept' {
    $uo = New-UoDir 'skills-add' (New-Tiledata) (New-Animdata)
    Write-FullSkills $uo
    $out = Join-Path $work 'skills-add-out'
    $r = Invoke-BuilderSaying $uo $out
    Assert-True ($r.Result) "an override list was written ($($r.Said))"
    $got = @(Read-Skills (Join-Path $out 'skills.mul') (Join-Path $out 'Skills.idx'))
    Assert-Equal 256 $got.Count 'every slot is still there'
    Assert-Equal '0:Skill0:0' $got[0] 'the first skill'
    Assert-Equal '0:Skill57:0' $got[57] 'the last stock skill'
    Assert-Equal '0:Herbalism:0' $got[58] 'the new skill'
    Assert-Equal '-' $got[59] 'the next slot stays empty'
    Assert-True ($r.Said -notmatch 'skill') "nothing said about skills: $($r.Said)"
}

Fact 'ASlot58TheFilesAlreadyUseIsLeftAloneWithOneLine' {
    $uo = New-UoDir 'skills-taken' (New-Tiledata) (New-Animdata)
    Write-FullSkills $uo
    $idxPath = Join-Path $uo 'Skills.idx'
    $idx = [IO.File]::ReadAllBytes($idxPath)
    [Array]::Copy([BitConverter]::GetBytes(0), 0, $idx, 58 * 12, 4)
    [Array]::Copy([BitConverter]::GetBytes(8), 0, $idx, 58 * 12 + 4, 4)
    [IO.File]::WriteAllBytes($idxPath, $idx)
    $r = Invoke-BuilderSaying $uo (Join-Path $work 'skills-taken-out')
    Assert-True ($r.Said -match 'skill 58 is left alone') "one line says so: $($r.Said)"
}

'''.replace('\n', nl3)
key = "Fact 'ASkillThreeTheFilesNoLongerCallItemIdentificationIsLeftAloneWithOneLine' {"
assert x.count(key) == 1
if 'HerbalismIsAddedAtSlot58' not in x:
    x = x.replace(key, fact + key)
open(t, 'w', encoding='utf-8-sig' if bom2 else 'utf-8', newline='').write(x)
print('ok')
