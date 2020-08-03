#!/usr/bin/env python3

import fire
import digitools.digitone as digitone

def main():
    try:
        fire.Fire(
            {
                'print': digitone.SoundManager.print,
                'export': digitone.SoundManager.export,
                'update': digitone.SoundManager.update
            }
        )
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()