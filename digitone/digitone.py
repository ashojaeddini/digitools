"""A set of utilities for managing the Elektron Digitone.

The initail goal of the project is provide an easy way for editing
Digitone sound names and tags in a SysEx (i.e. *.syx) file.
"""

import enum
import csv
import sysex

class Tag(enum.Enum):
    KICK = 0
    SNAR = 1
    DEEP = 2
    BRAS = 3
    STRI = 4
    PERC = 5
    HHAT = 6
    CYMB = 7
    EVOL = 8
    EXPR = 9
    BASS = 10
    LEAD = 11
    PAD  = 12
    TXTR = 13
    CRD  = 14
    SFX  = 15
    ARP  = 16
    METL = 17
    ACOU = 18
    ATMO = 19
    NOIS = 20
    GLCH = 21
    HARD = 22
    SOFT = 23
    DARK = 24
    BRGT = 25
    VNTG = 26
    EPIC = 27
    FAIL = 28
    LOOP = 29
    MINE = 30
    FAV  = 31


class Sound:

    def __init__(self, message: bytes):
        # TODO: Validate the message
        # - Verify manufacturer/model ID
        # - Verify data length based on length in EOM
        # - Verify message integrity based on checkum in EOM

        data = Sound.decode(message[0x0A : len(message) - 5])

        self._message = message
        self._data = data
        self._tags = Sound.extract_tags(data)
        self._name = Sound.extract_name(data)

    @staticmethod
    def decode(data: bytes) -> bytes:
        length = len(data)

        if length % 8 == 1:
            raise TypeError('Provided data is not encoded as expected')

        result = bytearray()

        # Divide data into 8-byte groups

        si = 0

        while si < length:
            ei = min(si + 8, length)
            bg = data[si : ei]

            # Process the byte group

            msb_byte = bg[0]

            for i in range(1, len(bg)):
                msb = (msb_byte >> (7 - i)) & 1
                result.append(bg[i] | (msb << 7))

            si = ei
        
        return bytes(result)

    @staticmethod
    def extract_tags(data: bytes) -> list:
        tag_data = data[0x08 : 0x0C]

        tags = []

        for t in Tag:
            if (tag_data[3 - (t.value // 8)] >> (t.value % 8)) & 1:
                tags.append(t)

        return tags

    @staticmethod
    def extract_name(data: bytes) -> str:
        name_data = data[0x0C : min(data.index(0x00, 0x0C), 0x1B)]

        return str(name_data, 'latin-1')

    def message(self) -> bytes:
        return self._message

    def data(self) -> bytes:
        return self._data

    def name(self) -> str:
        return self._name

    def tags(self) -> list:
        return self._tags

    def __str__(self):
        return f'{self._name} {self._tags}'


class SoundManager:

    @staticmethod
    def load(syx_file: str) -> list:
        """Returns the sounds from the input file as a list of Sound objects.

        Args:
            syx_file: Path to the input SysEx file

        Returns:
            A list of Sound objects loaded from the input file
        """
        messages = sysex.SysEx.load(syx_file)

        sounds = []

        for message in messages:
            sounds.append(Sound(message))

        return sounds
    
    @staticmethod
    def print(syx_file: str):
        """Prints the list of sounds contained in the input file.

        This functions prints basic information (i.e. number, name, and tags)
        of the sounds contained in the SysEx file to the standard output.

        Args:
            syx_file: Path to the input SysEx file
        """
        sounds = SoundManager.load(syx_file)

        for i, sound in enumerate(sounds, start=1):
            print(f'{i:03}: {sound.name():15} {[t.name for t in sound.tags()]}')

    @staticmethod
    def export(syx_file: str, csv_file: str):
        """Exports the sounds in the input file to a CSV file.

        This functions exports basic information (i.e. number, name, and tags)
        of the sounds contained in the SysEx file to the specified output file
        in CSV format.

        Args:
            syx_file: Path to the input SysEx file
            csv_file: Path to the output CSV file
        """
        sounds = SoundManager.load(syx_file)

        with open(csv_file, 'w', newline='') as f:
            csvwriter = csv.writer(f, dialect='excel')
            
            # Write the header row
            csvwriter.writerow(['#', 'Sound Name'] + [t.name for t in Tag])

            # Write a row for each sound
            for i, sound in enumerate(sounds, start=1):
                sound_row = [f'{i:03}', sound.name()]

                for t in Tag:
                    sound_row.append('●' if t in sound.tags() else '')
                
                csvwriter.writerow(sound_row)