#Requires -Version 5.1
<#
  cc-P40 scratch prototype: apply our map patch (trammel.mapops) to copies of the player's own
  EA files, the way Build-UoOverrides.ps1 does for tiledata/animdata. Never writes to -UoDir.

      Apply-MapOps.ps1 -UoDir D:\UO\UltimaOnlineVanilla -Ops trammel.mapops -Out out

  Stamp: skips when the three EA files (size + LastWriteTimeUtc) and the ops file's hash match.
  Each touched block's EA content is fingerprinted in the ops file (B lines); a mismatch means EA
  changed our area under us, which is reported per block and the patch still applies.
#>
param([string]$UoDir, [string]$Ops, [string]$Out)
$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()

Add-Type -TypeDefinition @'
using System; using System.IO; using System.Collections.Generic; using System.Security.Cryptography;
public static class SlMap {
  static uint Rot(uint x, int k) { return (x << k) | (x >> (32 - k)); }
  public static ulong Hash(byte[] s) {
    int len = s.Length, k = 0; uint a, b, c; a = b = c = 0xDEADBEEF + (uint)len;
    while (len > 12) {
      a += BitConverter.ToUInt32(s, k); b += BitConverter.ToUInt32(s, k + 4); c += BitConverter.ToUInt32(s, k + 8);
      a -= c; a ^= Rot(c, 4); c += b; b -= a; b ^= Rot(a, 6); a += c; c -= b; c ^= Rot(b, 8); b += a;
      a -= c; a ^= Rot(c, 16); c += b; b -= a; b ^= Rot(a, 19); a += c; c -= b; c ^= Rot(b, 4); b += a;
      len -= 12; k += 12;
    }
    if (len == 0) return ((ulong)b << 32) | c;
    byte[] t = new byte[12]; Array.Copy(s, k, t, 0, len);
    c += (uint)(t[8] | t[9] << 8 | t[10] << 16 | t[11] << 24); b += BitConverter.ToUInt32(t, 4); a += BitConverter.ToUInt32(t, 0);
    c ^= b; c -= Rot(b, 14); a ^= c; a -= Rot(c, 11); b ^= a; b -= Rot(a, 25); c ^= b; c -= Rot(b, 16);
    a ^= c; a -= Rot(c, 4); b ^= a; b -= Rot(a, 14); c ^= b; c -= Rot(b, 24);
    return ((ulong)b << 32) | c;
  }
  // block index -> absolute offset of its 196-byte record in a LegacyMUL.uop map
  public static long[] EntryOffsets(string path, int facet, int entries) {
    var map = new Dictionary<ulong, long>();
    using (var f = new BinaryReader(File.OpenRead(path))) {
      if (f.ReadUInt32() != 0x0050594D) throw new Exception("not a UOP file");
      f.BaseStream.Seek(12, SeekOrigin.Begin); long next = f.ReadInt64();
      while (next != 0) {
        f.BaseStream.Seek(next, SeekOrigin.Begin); int cnt = f.ReadInt32(); next = f.ReadInt64();
        for (int i = 0; i < cnt; i++) {
          long off = f.ReadInt64(); int hl = f.ReadInt32(); int cl = f.ReadInt32(); int dl = f.ReadInt32();
          ulong h = f.ReadUInt64(); f.ReadUInt32(); short flag = f.ReadInt16();
          if (off == 0) continue;
          if (flag != 0 || cl != dl) throw new Exception("compressed map entry");
          map[h] = off + hl;
        }
      }
    }
    var r = new long[entries];
    for (int e = 0; e < entries; e++)
      r[e] = map[Hash(System.Text.Encoding.ASCII.GetBytes(string.Format("build/map{0}legacymul/{1:D8}.dat", facet, e)))];
    return r;
  }
  public static string Fingerprint(byte[] land192, byte[] sta, int lookup, int length) {
    using (var sha = SHA256.Create()) {
      var buf = new byte[192 + Math.Max(0, length)];
      Array.Copy(land192, buf, 192);
      if (lookup >= 0 && length > 0) Array.Copy(sta, lookup, buf, 192, length);
      return BitConverter.ToString(sha.ComputeHash(buf)).Replace("-", "").Substring(0, 16).ToLowerInvariant();
    }
  }
}
'@

$files = 'map1LegacyMUL.uop', 'statics1.mul', 'staidx1.mul'
New-Item -ItemType Directory -Force $Out | Out-Null
$stampPath = Join-Path $Out 'stamp.txt'
$stamp = (@('mapops 1') + ($files | ForEach-Object { $i = Get-Item -LiteralPath (Join-Path $UoDir $_); "$_ $($i.Length) $($i.LastWriteTimeUtc.Ticks)" }) +
          (Get-FileHash -LiteralPath $Ops -Algorithm SHA256).Hash) -join "`n"
if ((Test-Path $stampPath) -and ([IO.File]::ReadAllText($stampPath) -eq $stamp) -and
    @($files | Where-Object { -not (Test-Path (Join-Path $Out $_)) }).Count -eq 0) {
    Write-Host "skip (stamp matches) $($sw.ElapsedMilliseconds) ms"; return
}
Remove-Item -LiteralPath $stampPath -ErrorAction SilentlyContinue

$per = 4096; $blocksH = 512; $nblocks = 896 * 512
$mapOut = Join-Path $Out 'map1LegacyMUL.uop'
Copy-Item -LiteralPath (Join-Path $UoDir 'map1LegacyMUL.uop') -Destination $mapOut -Force
$entryOff = [SlMap]::EntryOffsets($mapOut, 1, [int][math]::Ceiling($nblocks / $per))
$idx = [IO.File]::ReadAllBytes((Join-Path $UoDir 'staidx1.mul'))
$sta = [IO.File]::ReadAllBytes((Join-Path $UoDir 'statics1.mul'))
$t1 = $sw.ElapsedMilliseconds

$land = New-Object 'System.Collections.Generic.List[int[]]'
$adds = @{}; $removes = @{}; $fps = @{}
foreach ($line in [IO.File]::ReadLines((Resolve-Path $Ops))) {
    if ($line.StartsWith('#') -or $line.Length -eq 0) { continue }
    $p = $line.Split(' ')
    switch ($p[0]) {
        'F' { if ($p[1] -ne '1') { throw "facet $($p[1]) not handled by this prototype" } }
        'B' { $fps[[int]$p[1]] = $p[2] }
        'L' { $land.Add([int[]]@([int]$p[1], [int]$p[2], [int]$p[3], [int]$p[4])) }
        default {
            $x = [int]$p[1]; $y = [int]$p[2]; $b = ($x -shr 3) * $blocksH + ($y -shr 3)
            $rec = New-Object byte[] 7
            [BitConverter]::GetBytes([uint16]$p[4]).CopyTo($rec, 0); $rec[2] = [byte]($x -band 7); $rec[3] = [byte]($y -band 7)
            $rec[4] = [byte]([sbyte]$p[3] -band 0xFF); [BitConverter]::GetBytes([uint16]$p[5]).CopyTo($rec, 5)
            $t = if ($p[0] -eq 'S+') { $adds } else { $removes }
            if (-not $t.ContainsKey($b)) { $t[$b] = New-Object 'System.Collections.Generic.List[byte[]]' }
            $t[$b].Add($rec)
        }
    }
}
$t2 = $sw.ElapsedMilliseconds

# EA changed one of our blocks? (hash of EA's block, compared with the one the patch was made on)
$drift = 0
$fs = [IO.File]::Open($mapOut, 'Open', 'ReadWrite')
try {
    $buf = New-Object byte[] 192
    foreach ($b in $fps.Keys) {
        $fs.Position = $entryOff[[int][math]::Floor($b / $per)] + ($b % $per) * 196 + 4
        [void]$fs.Read($buf, 0, 192)
        $lk = [BitConverter]::ToInt32($idx, $b * 12); $ln = [BitConverter]::ToInt32($idx, $b * 12 + 4)
        if ([SlMap]::Fingerprint($buf, $sta, $lk, $ln) -ne $fps[$b]) { $drift++; Write-Host "  EA changed block $b since the patch was made" -ForegroundColor Yellow }
    }
    $cell = New-Object byte[] 3
    foreach ($l in $land) {
        $b = ($l[0] -shr 3) * $blocksH + ($l[1] -shr 3)
        $fs.Position = $entryOff[[int][math]::Floor($b / $per)] + ($b % $per) * 196 + 4 + ((($l[1] -band 7) * 8) + ($l[0] -band 7)) * 3
        [BitConverter]::GetBytes([uint16]$l[2]).CopyTo($cell, 0); $cell[2] = [byte]([sbyte]$l[3] -band 0xFF)
        $fs.Write($cell, 0, 3)
    }
} finally { $fs.Close() }
$t3 = $sw.ElapsedMilliseconds

# statics: EA's file unchanged, our blocks appended at the end, their index entries repointed
$staOut = New-Object IO.MemoryStream
$staOut.Write($sta, 0, $sta.Length)
$missing = 0
foreach ($b in (@($adds.Keys) + @($removes.Keys) | Select-Object -Unique)) {
    $lk = [BitConverter]::ToInt32($idx, $b * 12); $ln = [BitConverter]::ToInt32($idx, $b * 12 + 4)
    $recs = New-Object 'System.Collections.Generic.List[byte[]]'
    if ($lk -ge 0 -and $ln -gt 0) { for ($i = 0; $i -lt $ln; $i += 7) { $r = New-Object byte[] 7; [Array]::Copy($sta, $lk + $i, $r, 0, 7); $recs.Add($r) } }
    if ($removes.ContainsKey($b)) {
        foreach ($rm in $removes[$b]) {
            $hit = -1
            for ($i = 0; $i -lt $recs.Count; $i++) { if ([Convert]::ToBase64String($recs[$i]) -eq [Convert]::ToBase64String($rm)) { $hit = $i; break } }
            if ($hit -ge 0) { $recs.RemoveAt($hit) } else { $missing++; Write-Host "  static to remove is not in EA's block $b any more; skipped" -ForegroundColor Yellow }
        }
    }
    if ($adds.ContainsKey($b)) { $recs.AddRange($adds[$b]) }
    if ($recs.Count -eq 0) { [BitConverter]::GetBytes([int]-1).CopyTo($idx, $b * 12); [BitConverter]::GetBytes([int]-1).CopyTo($idx, $b * 12 + 4); continue }
    [BitConverter]::GetBytes([int]$staOut.Length).CopyTo($idx, $b * 12)
    [BitConverter]::GetBytes([int]($recs.Count * 7)).CopyTo($idx, $b * 12 + 4)
    foreach ($r in $recs) { $staOut.Write($r, 0, 7) }
}
[IO.File]::WriteAllBytes((Join-Path $Out 'statics1.mul'), $staOut.ToArray())
[IO.File]::WriteAllBytes((Join-Path $Out 'staidx1.mul'), $idx)
$t4 = $sw.ElapsedMilliseconds
[IO.File]::WriteAllText($stampPath, $stamp, (New-Object Text.UTF8Encoding $false))
Write-Host ("rebuilt: load+copy {0} ms, parse {1} ms, land {2} ms, statics {3} ms, total {4} ms; drifted blocks {5}, missing removes {6}" -f $t1, ($t2 - $t1), ($t3 - $t2), ($t4 - $t3), $sw.ElapsedMilliseconds, $drift, $missing)
