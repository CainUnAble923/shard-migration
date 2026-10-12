# cc-P34 WRITES player-package/vendor/shattered-legacy-art/art/<id>.png for the 47 winter IDs, through
# scripts/anchor-art-frames.py --keep-geometry --black-transparent (format and black only; see that tool).
# The table here is the one place the choice of file per ID is written; registry.csv repeats it per row.
import subprocess, sys, os
W = r'D:/UO/third-party/winter-holiday'
MR = W + '/For ServUO 2'
VK = W + '/Christmas sprites/BMP'
OUT = r'D:/ShatteredLegacy/player-package/vendor/shattered-legacy-art/art'
TOOL = r'D:/ShatteredLegacy/scripts/anchor-art-frames.py'
GROUPS = [
    (15424, [MR + '/Statues/Father Christmas/%d.bmp' % i for i in range(1, 6)]),
    (15429, [MR + '/Raised Firepit/%d.bmp' % i for i in range(1, 6)]),
    (15434, [MR + '/Stoves/1/%d.bmp' % i for i in range(1, 5)]),
    (15438, [MR + '/Stoves/2/%d.bmp' % i for i in range(1, 5)]),
    (15442, [VK + '/Christmas tree_1.bmp']),
    (15443, [VK + "/SS Santa's Bag_1.bmp"]),
    (15444, [VK + '/Gift Box 01_1.bmp']),
    (15445, [VK + '/Gift Box 02_1.bmp']),
    (15446, [VK + '/Present.003_Kharzug_1.bmp']),
    (15447, [MR + '/Candy Cane stuff/SmallCaner.bmp']),
    (15448, [MR + '/Candy Cane stuff/SmallCaner2.bmp']),
    (15449, [MR + '/Food Items/EggNogTray.bmp']),
    (15450, [MR + '/Food Items/Eggnogtray1.bmp']),
    (15451, [MR + '/Food Items/ChristmasCookiesPan1.bmp']),
    (15452, [MR + '/Food Items/CandyCaneOnTray.bmp']),
    (15453, [MR + '/Food Items/ChristmasPlatter.bmp']),
    (15454, [MR + '/Food Items/turkey.bmp']),
    (15455, [MR + '/Food Items/1.bmp']),
    (15456, [VK + '/M3DCF Christmas Fireplace_1.bmp']),
    (15457, [VK + '/Garland.003_1.bmp']),
    (15458, [VK + '/Garland.003_4.bmp']),
    (15459, [VK + '/Painting 12_1.bmp']),
    (15460, [VK + '/Painting 12_4.bmp']),
    (15461, [VK + '/Painting 15_1.bmp']),
    (15462, [VK + '/Painting 15_4.bmp']),
    (15463, [MR + '/Snow Covered Shields and Paintings/1.bmp']),
    (15464, [MR + '/Snow Covered Shields and Paintings/2.bmp']),
    (15465, [MR + '/Snow Covered Shields and Paintings/S1.bmp']),
    (15466, [MR + '/Snow Covered Shields and Paintings/s2.bmp']),
    (15467, [MR + '/Snow Patches/Snowpatches/1/2.bmp']),
    (15468, [MR + '/Snow Patches/Snowpatches/1/3.bmp']),
    (15469, [MR + '/Snow Patches/Snowpatches/1/4.bmp']),
    (15470, [VK + '/Christmas Sleigh_1.bmp']),
]
if __name__ == '__main__':
    for first, files in GROUPS:
        r = subprocess.run([sys.executable, TOOL, '--files'] + files + ['--first-id', str(first), '--out', OUT,
                            '--keep-geometry', '--black-transparent'] + sys.argv[1:], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
        if r.returncode: sys.exit(r.returncode)
