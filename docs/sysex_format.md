# Digitone Sound SysEx Structure
## Overall Structure
The following table shows the overall layout of the SysEx message for Digitone sounds.

| Bytes (Hex) | Description                      | Value (Hex)    |
| -----       | -----------                      | -----          |
| 000         | SysEx Start                      | F0             |
| 001 .. 003  | Manufacturer ID                  | 00 20 3C       |
| 004 .. 008  | Model ID                         | 0D 00 53 01 01 |
| 009         | Sound number in Bank<sup>*</sup> |                |
| 00A .. 163  | 7-bit Encoded Data               |                |
| 164 .. 165  | Checksum                         |                |
| 166 .. 167  | Length                           |                |
| 168         | SysEx End [F7]                   | F7             |

<sup>*</sup> For sounds 1 - 128 the value is 0 - 127. For sounds beyond 128 the value is 0.

## Checksum
- Sum of all the bytes in the data (00A..163)
- The lower 14 bits are represented in two bytes

## Message Length
- The length includes the EOM part, but not the prefix (00A..168)
- The lower 14 bits are represented in two bytes

## 7-bit Encoding of Data

Converts between this:

        Bit:   7  6  5  4  3  2  1  0
    Data[0]: [a7 a6 a5 a4 a3 a2 a1 a0]
    Data[1]: [b7 b6 b5 b4 b3 b2 b1 b0]
    Data[2]: [c7 c6 c5 c4 c3 c2 c1 c0]
    ...      ...
    Data[6]: [g7 g6 g5 g4 g3 g2 g1 g0]

And this:

        Bit:   7  6  5  4  3  2  1  0
    Data[0]: [ 0 a7 b7 c7 d7 e7 f7 g7]
    Data[1]: [ 0 a6 a5 a4 a3 a2 a1 a0]
    Data[2]: [ 0 b6 b5 b4 b3 b2 b1 b0]
    Data[3]: [ 0 c6 c5 c4 c3 c2 c1 c0]
    ...      ...
    Data[7]: [ 0 g6 g5 g4 g3 g2 g1 g0]
