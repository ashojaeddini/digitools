#!/usr/bin/env python3

from .sysex import SysexProcessor
from .sound import Sound

def main():
    print('///// Digitone Utilities /////')
    print()

    processor = SysexProcessor()

    messages = processor.load('data/sounds.syx')

    sounds = []

    for message in messages:
        sounds.append(Sound(message))

    for s in sounds:
        print(s)

if __name__ == '__main__':
    main()