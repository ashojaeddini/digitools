"""A set of utility functions for loading and parsing standard SysEx files.
"""

SYSEX_BEGIN = 0xF0
SYSEX_END = 0xF7
MESSAGE_SIZE = 361

class SysEx:

    @staticmethod
    def load(syx_file: str) -> bytes:
        """Returns the individual SysEx messages in the input file as a list of bytes objects
        """
        with open(syx_file, mode='rb') as f:
            contents = f.read()
        
        # TODO: Split into individual messages based on SysEx star/end (i.e. F0/F7) bytes instead

        messages = []

        for i in range(len(contents) // MESSAGE_SIZE):
            messages.append(contents[i * MESSAGE_SIZE : (i + 1) * MESSAGE_SIZE])

        return messages

    @staticmethod
    def split(syx_file: str):
        """Saves the individual SysEx messages in the input file as individual files
        """
        messages = SysEx.load(syx_file)

        for i, message in enumerate(messages):
            with open(f'{i+1:03}.syx', mode='wb') as f:
                f.write(message)