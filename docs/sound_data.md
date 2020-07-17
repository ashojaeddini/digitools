# Digitone Sound Data Layout
The following layout corresponds to non-encoded representation of sound data rather than the 7-bit encoded representation as contained in the SysEx message.

| Range     | Description            |
| -----     | -----------            |
| 00 .. 07  | TBD                    |
| 08 .. 11  | Tags (bit flas)        |
| 12 .. 27  | Name (15 chars + 0x00) |
| 28 .. End | TBD                    |
