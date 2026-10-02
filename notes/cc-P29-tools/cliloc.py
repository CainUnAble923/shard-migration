# cc-P29 Part F: reads a client Cliloc file, compressed or not, by a port of pinned's own reader:
# Server/Localization/Localization.cs:88-143 (header test, entry layout) and Server/Client/BwtDecompress.cs
# (the move-to-front pass, then InternalDecompress). Read only.
#
#   python cliloc.py <Cliloc.enu> <number> [<number> ...]   print those entries
#   python cliloc.py <Cliloc.enu> --grep <regex>            print every entry whose text matches
import re
import struct
import sys


def _mtf(data):
    # BwtDecompress.Decompress: firstChar is the first byte after the 4-byte header; the 65536-entry table, built
    # and sorted, is 0..65535, so only its first 256 entries are ever read: a move-to-front decode of bytes.
    table = list(range(256))
    out = bytearray(len(data) - 1)  # every byte after the first is read once; the last read value is discarded
    first = data[0]
    i = 0
    for b in data[1:]:
        v = table[first]
        if first > 0:
            table[1:first + 1] = table[0:first]
        table[0] = v
        out[i] = v & 0xFF
        i += 1
        first = b
    # As in the C# loop, the last byte read is never decoded: the loop ends when the stream does.
    return out


def _frequency(counts):
    tmp = list(counts)
    out = [0] * 256
    for i in range(256):
        value, index = 0, 0
        for j in range(256):
            if tmp[j] > value:
                index, value = j, tmp[j]
        if value == 0:
            break
        out[i] = index
        tmp[index] = 0
    return out


def _internal(inp):
    st = list(range(256))
    partial = list(struct.unpack_from('<256i', inp, 0)) + [0] * 512
    total = sum(partial[:256])
    nonzero = 256 - partial[:256].count(0)
    freq = _frequency(partial[:256])
    m = 0
    for i in range(nonzero):
        f = freq[i]
        st[inp[m + 1024]] = f
        partial[f + 256] = m + 1
        m += partial[f]
        partial[f + 512] = m
    val = st[0]
    out = bytearray(total)
    count = 0
    while count < total:
        first = partial[val + 256]
        out[count] = val
        if first >= partial[val + 512]:
            if nonzero > 0:
                nonzero -= 1
                st[0:nonzero] = st[1:nonzero + 1]
                val = st[0]
            else:
                nonzero -= 1
        else:
            idx = inp[first + 1024]
            partial[val + 256] = first + 1
            if idx != 0:
                st[0:idx] = st[1:idx + 1]
                st[idx] = val
                val = st[0]
        count += 1
    return out


def load(path):
    raw = open(path, 'rb').read()
    if struct.unpack_from('<i', raw, 0)[0] == 2 and struct.unpack_from('<h', raw, 4)[0] == 1:
        data, o = raw, 6
    else:
        data = _internal(_mtf(raw[4:]))
        if struct.unpack_from('<i', data, 0)[0] != 2 or struct.unpack_from('<h', data, 4)[0] != 1:
            raise ValueError(f'invalid cliloc header in {path}')
        o = 6
    entries = {}
    while o < len(data):
        n, flag, ln = struct.unpack_from('<iBH', data, o)
        o += 7
        entries[n] = data[o:o + ln].decode('utf-8', 'replace')
        o += ln
    return entries


if __name__ == '__main__':
    c = load(sys.argv[1])
    print(f'{len(c)} entries')
    if len(sys.argv) > 3 and sys.argv[2] == '--grep':
        rx = re.compile(sys.argv[3], re.I)
        for n in sorted(c):
            if rx.search(c[n]):
                print(n, repr(c[n]))
    else:
        for a in sys.argv[2:]:
            print(a, repr(c.get(int(a))))
