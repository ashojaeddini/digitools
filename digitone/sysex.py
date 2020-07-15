"""A set of utility functions for loading and parsing standard SysEx files.
"""

MSG_START = 0xF0
MSG_END = 0xF7

class SysExHandler:

    @staticmethod
    def load(syx_file: str) -> list:
        """Returns the individual SysEx messages in the input file as a list of bytes objects
        """
        with open(syx_file, mode='rb') as f:
            contents = f.read()
        
        messages = []

        si = 0
        while si < len(contents):
            if contents[si] != MSG_START:
                raise TypeError('Invalid SysEx message encountered')
            
            ei = contents.find(MSG_END, si + 1) + 1
            messages.append(contents[si : ei])
            si = ei

        return messages

    @staticmethod
    def save(messages: list, syx_file: str):
        """Stores the provided SysEx messages to the specified file
        """
        with open(syx_file, mode='wb') as f:
            for message in messages:
                f.write(message)

    @staticmethod
    def split(syx_file: str):
        """Saves the individual SysEx messages in the input file as individual files
        """
        messages = SysExHandler.load(syx_file)

        for i, message in enumerate(messages):
            with open(f'{i+1:03}.syx', mode='wb') as f:
                f.write(message)


class SysExDataEncoder:

    @staticmethod
    def encode(data: bytes) -> bytes:
        """Performs 7-bit encoding on the data for use in SysEx messages
        """
        result = bytearray()

        for g in SysExDataEncoder.group(data, 7):
            e = bytearray(len(g) + 1)
            
            for i in range(0, len(g)):
                e[0] = (g[i] >> 7) << (6 - i) | e[0]
                e[i + 1] = g[i] & 0x7F
            
            result.extend(e)
        
        return bytes(result)

    @staticmethod
    def decode(data: bytes) -> bytes:
        """Performs 7-bit decoding on the data to yield original raw data
        """
        if len(data) % 8 == 1:
            raise TypeError('Provided data is not encoded as expected')

        result = bytearray()

        for g in SysExDataEncoder.group(data, 8):
            for i in range(1, len(g)):
                msb = g[0] >> (7 - i) & 1
                result.append(g[i] | msb << 7)
        
        return bytes(result)

    @staticmethod
    def group(data: bytes, size: int) -> list:
        """Splits the data into groups of specified size
        """
        result = []

        l = len(data)
        d = l // size
        r = l % size

        for i in range(d):
            result.append(data[i * size : (i + 1) * size])

        if r > 0:
            result.append(data[l - r :])

        return result