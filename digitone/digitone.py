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
    def __init__(self, pnum: int, data: bytes):
        self._pnum = pnum
        self._data = bytearray(data)
        self._tags = self._read_tags()
        self._name = self._read_name()

    def _write_bytes(self, start: int, bs: bytes):
        for i, b in enumerate(bs):
            self._data[start + i] = b

    def _read_tags(self) -> list:
        tags = []

        for t in Tag:
            if self._data[11 - (t.value // 8)] >> (t.value % 8) & 1:
                tags.append(t)

        return tags

    def _write_tags(self, tags: list):
        tag_bytes = bytearray(4)

        for t in Tag:
            if t in tags:
                tag_bytes[3 - (t.value // 8)] |= 1 << (t.value % 8)

        self._write_bytes(8, tag_bytes)

    def _read_name(self) -> str:
        return str(self._data[12 : min(self._data.index(0x00, 12), 27)], 'latin-1')

    def _write_name(self, name: str):
        if len(name) > 15:
            TypeError('Maximum length for sound name is 15') # TODO: Confirm that max length is 15

        name_bytes = bytearray(name.encode('latin-1'))
        name_bytes.append(0x00)

        self._write_bytes(12, name_bytes)

    def pnum(self) -> int:
        return self._pnum

    def data(self) -> bytes:
        return self._data

    def name(self, value : str = None) -> str:
        if value:
            self._write_name(value)
            self._name = value
        
        return self._name

    def tags(self, value : list = None) -> list:
        if value:
            self._write_tags(value)
            self._tags = value
        
        return self._tags

    def __str__(self):
        return f'{self._name:15} {[t.name for t in self._tags]}'


class SoundSysExHandler:
    PREFIX = bytes((0x00, 0x20, 0x3C, 0x0D, 0x00, 0x53, 0x01, 0x01))

    @staticmethod
    def validate(message: bytes):
        # Validate the message
        # - Verify manufacturer/model ID
        # - Verify message integrity based on checkum in EOM
        # - Verify data length based on length in EOM

        eom = message[len(message) - 5 :]

        v1 = message[1 : 9] == SoundSysExHandler.PREFIX
        v2 = SoundSysExHandler.checksum(message[10 : len(message) - 5]) == eom[0 : 2]
        v3 = SoundSysExHandler.encode_number(len(message) - 10) == eom[2 : 4]

        # TODO: Raise individual errors for each validation 

        if not (v1 and v2 and v3):
            raise TypeError('Invalid sound data encountered')

    @staticmethod
    def message_to_sound(message: bytes) -> Sound:
        SoundSysExHandler.validate(message) # TODO: Handle error to show a message

        pnum = message[9]
        data = sysex.SysExDataEncoder.decode(message[10 : len(message) - 5])

        return Sound(pnum, data)

    @staticmethod
    def sound_to_message(sound: Sound) -> bytes:
        encoded_data = sysex.SysExDataEncoder.encode(sound.data())
        checksum = SoundSysExHandler.checksum(encoded_data)
        length = SoundSysExHandler.encode_number(len(encoded_data) + 5)

        message = bytearray()
        message.append(sysex.MSG_START)
        message.extend(SoundSysExHandler.PREFIX)
        message.append(sound.pnum())
        message.extend(encoded_data)
        message.extend(checksum)
        message.extend(length)
        message.append(sysex.MSG_END)

        return bytes(message)
    
    @staticmethod
    def checksum(data: bytes) -> bytes:
        return SoundSysExHandler.encode_number(sum(data))

    @staticmethod
    def encode_number(n: int) -> bytes:
        lsb = 0x7F & n
        msb = 0x7F & n >> 7

        return bytes((msb, lsb))


class SoundManager:

    @staticmethod
    def load(syx_file: str) -> list:
        """Loads the list of Sound objects from a SysEx file.

        Args:
            syx_file: Path to the input SysEx file

        Returns:
            A list of Sound objects loaded from the input file
        """
        messages = sysex.SysExHandler.load(syx_file)

        sounds = []

        for message in messages:
            sounds.append(SoundSysExHandler.message_to_sound(message))

        return sounds

    @staticmethod
    def save(sounds: list, syx_file: str):
        """Saves a list of Sound objects to a SysEx file.

        Args:
            sounds: the list of sounds to save
            syx_file: Path to the input SysEx file
        """
        messages = []

        for sound in sounds:
            messages.append(SoundSysExHandler.sound_to_message(sound))

        sysex.SysExHandler.save(messages, syx_file)
    
    @staticmethod
    def print(syx_file: str):
        """Prints the sounds in a SysEx file to the standard output.

        This functions prints basic information (i.e. number, name, and tags)
        of the sounds contained in the SysEx file to the standard output.

        Args:
            syx_file: Path to the input SysEx file
        """
        sounds = SoundManager.load(syx_file)

        for i, sound in enumerate(sounds, start=1):
            print(f'{i:03}: {sound.name():15} [{", ".join([t.name for t in sound.tags()])}]')

    @staticmethod
    def export(syx_file: str, csv_file: str):
        """Exports the sounds in a SysEx file to a CSV file.

        This functions exports basic information (i.e. number, name, and tags)
        of the sounds contained in the SysEx file to the specified output file
        in CSV format.

        Args:
            syx_file: Path to the input SysEx file
            csv_file: Path to the output CSV file
        """
        sounds = SoundManager.load(syx_file)

        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            
            writer.writerow(['#', 'Sound Name'] + [t.name for t in Tag])

            for i, sound in enumerate(sounds, start=1):
                sound_row = [f'{i:03}', sound.name()]

                for t in Tag:
                    sound_row.append('●' if t in sound.tags() else '')
                
                writer.writerow(sound_row)
    
    @staticmethod
    def update(syx_file: str, csv_file: str):
        """Updates name and tags of sounds in a SysEx file from a CSV file.

        Args:
            syx_file: Path to the SysEx file to update
            csv_file: Path to the CSV file with updates
        """
        sounds = SoundManager.load(syx_file)

        with open(csv_file, 'r', newline='') as f:
            reader = csv.DictReader(f, dialect='excel')

            for row in reader:
                tags = []
                for t in Tag:
                    if row[t.name]:
                        tags.append(t)
                
                s = sounds[int(row['#']) - 1]
                s.name(row['Sound Name'])
                s.tags(tags)
            
        SoundManager.save(sounds, syx_file)