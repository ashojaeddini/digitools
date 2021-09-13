"""A set of utilities for managing the Elektron device sounds.
"""

import enum
import csv
import digitools.sysex as sysex

class Device(enum.Enum):
    A4 = 0x06 # Analog Four MKI/MKII
    DN = 0x0D # Digitone

TAG_NAMES = {
    Device.A4: ['BASS', 'LEAD', 'PAD', 'TEXTURE', 'CHORD', 'KEYS', 'BRASS', 'STRINGS', 'TRANSIENT', 'SOUND FX', 'KICK', 'SNARE', 'HIHAT', 'PERCUSSIO', 'ATMOSPHER', 'EVOLVING', 'NOISY', 'GLITCH', 'HARD', 'SOFT', 'EXPRESSIV', 'DEEP', 'DARK', 'BRIGHT', 'VINTAGE', 'ACID', 'EPIC', 'FAIL', 'TEMPO SYN', 'INPUT', 'MINE', 'FAVOURITE'],
    Device.DN: ['KICK', 'SNAR', 'DEEP', 'BRAS', 'STRI', 'PERC', 'HHAT', 'CYMB', 'EVOL', 'EXPR', 'BASS', 'LEAD', 'PAD', 'TXTR', 'CRD', 'SFX', 'ARP', 'METL', 'ACOU', 'ATMO', 'NOIS', 'GLCH', 'HARD', 'SOFT', 'DARK', 'BRGT', 'VNTG', 'EPIC', 'FAIL', 'LOOP', 'MINE', 'FAV']
}


class Sound:
    """Represents an Elektron device sound

    This class represents the information contained in the data portion of the
    Elektron device sound SysEx message. The complete data is stored as bytes, and only
    name and tag are currently represented by additional variables and functions.

    The tag and name information is stored in following ranges:
        data[08 : 12] = Tags (bit flag)
        data[12 : 28] = Name (15 chars + 0x00)
    """

    NAME_MAX_LEN = 15
    NAME_ENCODING = 'latin-1'

    def __init__(self, pnum: int, device: Device, data: bytes):
        self._pnum = pnum
        self._device = device
        self._data = bytearray(data)
        self._tags = self._read_tags()
        self._name = self._read_name()

    def _write(self, start: int, bs: bytes):
        for i, b in enumerate(bs):
            self._data[start + i] = b

    def _read_tags(self) -> list:
        tags = []

        for t in range(0, 32):
            if self._data[11 - (t // 8)] >> (t % 8) & 1:
                tags.append(t)

        return tags

    def _write_tags(self, tags: list):
        tag_bytes = bytearray(4)

        for t in range(0, 32):
            if t in tags:
                tag_bytes[3 - (t // 8)] |= 1 << (t % 8)

        self._write(8, tag_bytes)

    def _read_name(self) -> str:
        return str(self._data[12 : min(self._data.index(0x00, 12), 27)], self.NAME_ENCODING)

    def _write_name(self, name: str):
        if len(name) > self.NAME_MAX_LEN:
            TypeError(f'The sound name "{name}"" exceeds the maximum length of {self.NAME_MAX_LEN}')

        name_bytes = bytearray(name.encode(self.NAME_ENCODING))
        name_bytes.append(0x00)

        self._write(12, name_bytes)

    def pnum(self) -> int:
        return self._pnum

    def device(self) -> Device:
        return self._device

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

    def tags_names(self) -> list:
        device_tags = TAG_NAMES[self._device]
        names = []

        for t in self._tags:
            names.append(device_tags[t])
        
        return names

    def __str__(self):
        return f'{self._name.ljust(self.NAME_MAX_LEN)} [{", ".join([t for t in self.tags_names()])}]'


class SoundSysExHandler:
    MANUFACTURER_ID = bytes((0x00, 0x20, 0x3C))
    PREFIX = bytes((0x00, 0x53, 0x01, 0x01))

    @staticmethod
    def validate(message: bytes):
        eom = message[len(message) - 5 :]

        if message[1 : 4] != SoundSysExHandler.MANUFACTURER_ID:
            raise TypeError('The SysEx message manufacturer ID is not recognized')

        if message[4] not in [device.value for device in Device]:
            raise TypeError('The SysEx message model ID is not recognized')

        if SoundSysExHandler.checksum(message[10 : len(message) - 5]) != eom[0 : 2]:
            raise TypeError('Data in the SysEx message is corrupted. Checksum validation failed.')

        if SoundSysExHandler.encode_number(len(message) - 10) != eom[2 : 4]:
            raise TypeError('Data in the SysEx message is corrupted. Length validation failed.')

    @staticmethod
    def message_to_sound(message: bytes) -> Sound:
        SoundSysExHandler.validate(message)

        pnum = message[9]
        device = Device(message[4])
        data = sysex.SysExDataEncoder.decode(message[10 : len(message) - 5])

        return Sound(pnum, device, data)

    @staticmethod
    def sound_to_message(sound: Sound) -> bytes:
        encoded_data = sysex.SysExDataEncoder.encode(sound.data())
        checksum = SoundSysExHandler.checksum(encoded_data)
        length = SoundSysExHandler.encode_number(len(encoded_data) + 5)

        message = bytearray()
        message.append(sysex.MSG_START)
        message.extend(SoundSysExHandler.MANUFACTURER_ID)
        message.append(sound.device().value)
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
    """Provides functions for working with sound files (SysEx).
    """

    @staticmethod
    def load(syx_file: str) -> list:
        """Loads the list of Sound objects from a sound file (SysEx).

        Args:
            syx_file: Path to the input SysEx file

        Returns:
            A list of Sound objects loaded from the input file
        """
        messages = sysex.SysExHandler.load(syx_file)

        sounds = []

        for i, message in enumerate(messages, start=1):
            try:
                sounds.append(SoundSysExHandler.message_to_sound(message))
            except TypeError:
                print(f'Loading the sound at position {i:03} failed. The SysEx message is not a valid sound.')

        return sounds

    @staticmethod
    def save(sounds: list, syx_file: str):
        """Saves a list of Sound objects to a sound file (SysEx).

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
        """Prints the sounds in a sound file (SysEx) to the standard output.

        This functions prints basic information (i.e. number, name, and tags)
        of the sounds contained in the SysEx file to the standard output.

        Args:
            syx_file: Path to the input SysEx file
        """
        sounds = SoundManager.load(syx_file)

        for i, sound in enumerate(sounds, start=1):
            print(f'{i:03}: {sound}')

    @staticmethod
    def export(syx_file: str, csv_file: str = None):
        """Exports the sounds in a sound file (SysEx) to a CSV file.

        This functions exports basic information (i.e. number, name, and tags)
        of the sounds contained in the SysEx file to the specified output file
        in CSV format.

        Args:
            syx_file: Path to the input SysEx file
            csv_file: Path to the output CSV file. If not specified, it will be derived from <syx_file>.
        """
        if not csv_file:
            csv_file = syx_file + '.csv'

        sounds = SoundManager.load(syx_file)

        if len(sounds) == 0:
            return
        
        tag_names = TAG_NAMES[sounds[0].device()]

        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            
            writer.writerow(['#', 'Sound Name'] + tag_names)

            for i, sound in enumerate(sounds, start=1):
                sound_row = [f'{i:03}', sound.name()]

                for t in range(0, 32):
                    sound_row.append('●' if t in sound.tags() else '')
                
                writer.writerow(sound_row)
    
    @staticmethod
    def update(syx_file: str, csv_file: str = None):
        """Updates name and tags of sounds in a sound file (SysEx) from a CSV file.

        Args:
            syx_file: Path to the SysEx file to update
            csv_file: Path to the CSV file with updates. If not specified, it will be derived from <syx_file>.
        """
        if not csv_file:
            csv_file = syx_file + '.csv'
        
        sounds_in = SoundManager.load(syx_file)
        sounds_out = []

        if len(sounds_in) == 0:
            return

        tag_names = TAG_NAMES[sounds_in[0].device()]

        with open(csv_file, 'r', newline='') as f:
            reader = csv.DictReader(f, dialect='excel')

            for row in reader:
                tags = []
                for i, t in enumerate(tag_names):
                    if row[t]:
                        tags.append(i)
                
                s = sounds_in[int(row['#']) - 1]
                s.name(row['Sound Name'])
                s.tags(tags)

                sounds_out.append(s)
            
        SoundManager.save(sounds_out, syx_file)

    @staticmethod
    def decode(syx_file: str, data_file: str):
        sounds = SoundManager.load(syx_file)

        with open(data_file, mode='wb') as f:
            for sound in sounds:
                f.write(sound.data())