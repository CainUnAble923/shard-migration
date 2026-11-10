# cc-P871: placed list for the variable carpet (P857, fixed up after the build review P866)

Item IDs are the stock carpet art. "Map" directions: x grows east, y grows south; the code names the corners
by the screen (ArtAt's NorthCorner is the map's north-west tile, the top of the screen). Facing: carpet
pieces have one facing each; the piece is chosen by its place in the carpet, nothing is turned.

## The six styles, as `VariableCarpetStyle.ArtAt` lays them

| # | Style | NW corner (`NorthCorner`) | NE corner (`EastCorner`) | SE corner (`SouthCorner`) | SW corner (`WestCorner`) | W edge (`NorthWestEdge`) | N edge (`NorthEastEdge`) | E edge (`SouthEastEdge`) | S edge (`SouthWestEdge`) | middle (`Middle`) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Blue, patterned | 0x0AC3 | 0x0AC5 | 0x0AC2 | 0x0AC4 | 0x0AF6 | 0x0AF7 | 0x0AF8 | 0x0AF9 | 0x0ABD |
| 1 | Blue, plain | 0x0AC3 | 0x0AC5 | 0x0AC2 | 0x0AC4 | 0x0AF6 | 0x0AF7 | 0x0AF8 | 0x0AF9 | 0x0ABE |
| 2 | Blue with gold | 0x0AD3 | 0x0AD5 | 0x0AD2 | 0x0AD4 | 0x0AD6 | 0x0AD7 | 0x0AD8 | 0x0AD9 | 0x0AD1 |
| 3 | Red, patterned | 0x0ACA | 0x0ACC | 0x0AC9 | 0x0ACB | 0x0ACD | 0x0ACE | 0x0ACF | 0x0AD0 | 0x0AC7 |
| 4 | Red, plain | 0x0ACA | 0x0ACC | 0x0AC9 | 0x0ACB | 0x0ACD | 0x0ACE | 0x0ACF | 0x0AD0 | 0x0AC8 |
| 5 | Gold, patterned | 0x0ADC | 0x0ADE | 0x0ADB | 0x0ADD | 0x0ADF | 0x0AE0 | 0x0AE1 | 0x0AE2 | 0x0ADA |

The red set agrees with the building guide's carpet rule (section 2.5: edges north 0x0ACE, south 0x0AD0,
west 0x0ACD, east 0x0ACF; corners NW 0x0ACA, SE 0x0AC9, NE 0x0ACC, SW 0x0ACB). Renders of every style laid
5 by 3 and 3 by 5: `carpet-<n>-<style>.jpg` and `carpets-all-six.jpg` in this folder.

## Carpets laid in the TazUO proofs

All in the trainee's own stone-and-plaster house (Trammel, centre 1986,2242, floor z 7), one at a time,
each rolled up before the next.

### Red, patterned, hue 1157, 4 by 4 (x by y), from 1984,2240,7 to 1987,2243,7 (P857 shots/p857/p857-carpet-laid.jpg)
- 0x0ACA, 1984,2240,7, NW corner
- 0x0ACE, 1985,2240,7, N edge
- 0x0ACE, 1986,2240,7, N edge
- 0x0ACC, 1987,2240,7, NE corner
- 0x0ACD, 1984,2241,7, W edge
- 0x0AC7, 1985,2241,7, middle
- 0x0AC7, 1986,2241,7, middle
- 0x0ACF, 1987,2241,7, E edge
- 0x0ACD, 1984,2242,7, W edge
- 0x0AC7, 1985,2242,7, middle
- 0x0AC7, 1986,2242,7, middle
- 0x0ACF, 1987,2242,7, E edge
- 0x0ACB, 1984,2243,7, SW corner
- 0x0AD0, 1985,2243,7, S edge
- 0x0AD0, 1986,2243,7, S edge
- 0x0AC9, 1987,2243,7, SE corner

### Blue with gold, hue 0, 4 by 4 (x by y), from 1984,2240,7 to 1987,2243,7 (P857 shots/p857/p857-carpet-blue-gold.jpg)
- 0x0AD3, 1984,2240,7, NW corner
- 0x0AD7, 1985,2240,7, N edge
- 0x0AD7, 1986,2240,7, N edge
- 0x0AD5, 1987,2240,7, NE corner
- 0x0AD6, 1984,2241,7, W edge
- 0x0AD1, 1985,2241,7, middle
- 0x0AD1, 1986,2241,7, middle
- 0x0AD8, 1987,2241,7, E edge
- 0x0AD6, 1984,2242,7, W edge
- 0x0AD1, 1985,2242,7, middle
- 0x0AD1, 1986,2242,7, middle
- 0x0AD8, 1987,2242,7, E edge
- 0x0AD4, 1984,2243,7, SW corner
- 0x0AD9, 1985,2243,7, S edge
- 0x0AD9, 1986,2243,7, S edge
- 0x0AD2, 1987,2243,7, SE corner

### Blue, patterned, hue 0, 5 by 3 (x by y), from 1984,2240,7 to 1988,2242,7 (P871 shots/p871-0-blue-patterned-5x3.jpg)
- 0x0AC3, 1984,2240,7, NW corner
- 0x0AF7, 1985,2240,7, N edge
- 0x0AF7, 1986,2240,7, N edge
- 0x0AF7, 1987,2240,7, N edge
- 0x0AC5, 1988,2240,7, NE corner
- 0x0AF6, 1984,2241,7, W edge
- 0x0ABD, 1985,2241,7, middle
- 0x0ABD, 1986,2241,7, middle
- 0x0ABD, 1987,2241,7, middle
- 0x0AF8, 1988,2241,7, E edge
- 0x0AC4, 1984,2242,7, SW corner
- 0x0AF9, 1985,2242,7, S edge
- 0x0AF9, 1986,2242,7, S edge
- 0x0AF9, 1987,2242,7, S edge
- 0x0AC2, 1988,2242,7, SE corner

### Blue, plain, hue 0, 3 by 4 (x by y), from 1984,2240,7 to 1986,2243,7 (P871 shots/p871-1-blue-plain-3x4.jpg)
- 0x0AC3, 1984,2240,7, NW corner
- 0x0AF7, 1985,2240,7, N edge
- 0x0AC5, 1986,2240,7, NE corner
- 0x0AF6, 1984,2241,7, W edge
- 0x0ABE, 1985,2241,7, middle
- 0x0AF8, 1986,2241,7, E edge
- 0x0AF6, 1984,2242,7, W edge
- 0x0ABE, 1985,2242,7, middle
- 0x0AF8, 1986,2242,7, E edge
- 0x0AC4, 1984,2243,7, SW corner
- 0x0AF9, 1985,2243,7, S edge
- 0x0AC2, 1986,2243,7, SE corner

### Blue with gold, hue 0, 5 by 3 (x by y), from 1984,2240,7 to 1988,2242,7 (P871 shots/p871-2-blue-with-gold-5x3.jpg)
- 0x0AD3, 1984,2240,7, NW corner
- 0x0AD7, 1985,2240,7, N edge
- 0x0AD7, 1986,2240,7, N edge
- 0x0AD7, 1987,2240,7, N edge
- 0x0AD5, 1988,2240,7, NE corner
- 0x0AD6, 1984,2241,7, W edge
- 0x0AD1, 1985,2241,7, middle
- 0x0AD1, 1986,2241,7, middle
- 0x0AD1, 1987,2241,7, middle
- 0x0AD8, 1988,2241,7, E edge
- 0x0AD4, 1984,2242,7, SW corner
- 0x0AD9, 1985,2242,7, S edge
- 0x0AD9, 1986,2242,7, S edge
- 0x0AD9, 1987,2242,7, S edge
- 0x0AD2, 1988,2242,7, SE corner

### Red, patterned, hue 0, 3 by 4 (x by y), from 1984,2240,7 to 1986,2243,7 (P871 shots/p871-3-red-patterned-3x4.jpg)
- 0x0ACA, 1984,2240,7, NW corner
- 0x0ACE, 1985,2240,7, N edge
- 0x0ACC, 1986,2240,7, NE corner
- 0x0ACD, 1984,2241,7, W edge
- 0x0AC7, 1985,2241,7, middle
- 0x0ACF, 1986,2241,7, E edge
- 0x0ACD, 1984,2242,7, W edge
- 0x0AC7, 1985,2242,7, middle
- 0x0ACF, 1986,2242,7, E edge
- 0x0ACB, 1984,2243,7, SW corner
- 0x0AD0, 1985,2243,7, S edge
- 0x0AC9, 1986,2243,7, SE corner

### Red, plain, hue 0, 5 by 3 (x by y), from 1984,2240,7 to 1988,2242,7 (P871 shots/p871-4-red-plain-5x3.jpg)
- 0x0ACA, 1984,2240,7, NW corner
- 0x0ACE, 1985,2240,7, N edge
- 0x0ACE, 1986,2240,7, N edge
- 0x0ACE, 1987,2240,7, N edge
- 0x0ACC, 1988,2240,7, NE corner
- 0x0ACD, 1984,2241,7, W edge
- 0x0AC8, 1985,2241,7, middle
- 0x0AC8, 1986,2241,7, middle
- 0x0AC8, 1987,2241,7, middle
- 0x0ACF, 1988,2241,7, E edge
- 0x0ACB, 1984,2242,7, SW corner
- 0x0AD0, 1985,2242,7, S edge
- 0x0AD0, 1986,2242,7, S edge
- 0x0AD0, 1987,2242,7, S edge
- 0x0AC9, 1988,2242,7, SE corner

### Gold, patterned, hue 0, 3 by 4 (x by y), from 1984,2240,7 to 1986,2243,7 (P871 shots/p871-5-gold-patterned-3x4.jpg)
- 0x0ADC, 1984,2240,7, NW corner
- 0x0AE0, 1985,2240,7, N edge
- 0x0ADE, 1986,2240,7, NE corner
- 0x0ADF, 1984,2241,7, W edge
- 0x0ADA, 1985,2241,7, middle
- 0x0AE1, 1986,2241,7, E edge
- 0x0ADF, 1984,2242,7, W edge
- 0x0ADA, 1985,2242,7, middle
- 0x0AE1, 1986,2242,7, E edge
- 0x0ADD, 1984,2243,7, SW corner
- 0x0AE2, 1985,2243,7, S edge
- 0x0ADB, 1986,2243,7, SE corner
