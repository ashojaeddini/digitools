#!/usr/bin/env python3

import fire
import digitools.sound as sound

def main():
    try:
        fire.Fire(
            {
                'print':  sound.SoundManager.print,
                'export': sound.SoundManager.export,
                'update': sound.SoundManager.update,
                'decode': sound.SoundManager.decode
            }
        )
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()