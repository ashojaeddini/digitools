#!/usr/bin/env python3

import fire
import digitone

def main():
    fire.Fire(
        {
            'print': digitone.SoundManager.print,
            'export': digitone.SoundManager.export,
            'update': digitone.SoundManager.update
        }
    )

if __name__ == '__main__':
    main()