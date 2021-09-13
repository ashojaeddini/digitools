# Sound Tags
Sounds can be tagged with one or more predefined tags. Each device supports 32 tags, but the tag names vary between devices. The following sections list the set of tags for each device and describe how tags are encoded in a sound.
## Tag Sets

### Analog Four
The following is the list of tags available on Analog Four.

| #  | Name      |
| -- | --------- |
| 00 | BASS      |
| 01 | LEAD      |
| 02 | PAD       |
| 03 | TEXTURE   |
| 04 | CHORD     |
| 05 | KEYS      |
| 06 | BRASS     |
| 07 | STRINGS   |
| 08 | TRANSIENT |
| 09 | SOUND FX  |
| 10 | KICK      |
| 11 | SNARE     |
| 12 | HIHAT     |
| 13 | PERCUSSIO |
| 14 | ATMOSPHER |
| 15 | EVOLVING  |
| 16 | NOISY     |
| 17 | GLITCH    |
| 18 | HARD      |
| 19 | SOFT      |
| 20 | EXPRESSIV |
| 21 | DEEP      |
| 22 | DARK      |
| 23 | BRIGHT    |
| 24 | VINTAGE   |
| 25 | ACID      |
| 26 | EPIC      |
| 27 | FAIL      |
| 28 | TEMPO SYN |
| 29 | INPUT     |
| 30 | MINE      |
| 31 | FAVOURITE |

### Digitone
The following is the list of tags available on Digitone.

| #  | Name |
| -- | ---- |
| 00 | KICK |
| 01 | SNAR |
| 02 | DEEP |
| 03 | BRAS |
| 04 | STRI |
| 05 | PERC |
| 06 | HHAT |
| 07 | CYMB |
| 08 | EVOL |
| 09 | EXPR |
| 10 | BASS |
| 11 | LEAD |
| 12 | PAD  |
| 13 | TXTR |
| 14 | CRD  |
| 15 | SFX  |
| 16 | ARP  |
| 17 | METL |
| 18 | ACOU |
| 19 | ATMO |
| 20 | NOIS |
| 21 | GLCH |
| 22 | HARD |
| 23 | SOFT |
| 24 | DARK |
| 25 | BRGT |
| 26 | VNTG |
| 27 | EPIC |
| 28 | FAIL |
| 29 | LOOP |
| 30 | MINE |
| 31 | FAV  |

## Bitmap Encoding of Tags
Tags are represented with the following pattern in four bytes. The corresponding bits for all tags the sound is associated with will be set.

    00: -------- -------- -------- -------●
    01: -------- -------- -------- ------●-
    02: -------- -------- -------- -----●--
    03: -------- -------- -------- ----●---
    04: -------- -------- -------- ---●----
    05: -------- -------- -------- --●-----
    06: -------- -------- -------- -●------
    07: -------- -------- -------- ●-------

    08: -------- -------- -------● --------
    09: -------- -------- ------●- --------
    10: -------- -------- -----●-- --------
    11: -------- -------- ----●--- --------
    12: -------- -------- ---●---- --------
    13: -------- -------- --●----- --------
    14: -------- -------- -●------ --------
    15: -------- -------- ●------- --------

    16: -------- -------● -------- --------
    17: -------- ------●- -------- --------
    18: -------- -----●-- -------- --------
    19: -------- ----●--- -------- --------
    20: -------- ---●---- -------- --------
    21: -------- --●----- -------- --------
    22: -------- -●------ -------- --------
    23: -------- ●------- -------- --------

    24: -------● -------- -------- --------
    25: ------●- -------- -------- --------
    26: -----●-- -------- -------- --------
    27: ----●--- -------- -------- --------
    28: ---●---- -------- -------- --------
    29: --●----- -------- -------- --------
    30: -●------ -------- -------- --------
    31: ●------- -------- -------- --------

These bytes correspond to byte indexes 8..11 of the decoded sound data.