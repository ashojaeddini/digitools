from .sound import Sound

SYSEX_BEGIN = 0xF0
SYSEX_END = 0xF7
MESSAGE_SIZE = 361

class SysexProcessor:

    def split(self, filename):
        with open(filename, mode='rb') as file:
            contents = file.read()

        for i in range(len(contents) // MESSAGE_SIZE):
            with open(f'{i+1:03}.syx', mode='wb') as msg_file:
                msg_file.write(contents[i * MESSAGE_SIZE : (i + 1) * MESSAGE_SIZE])

    def load(self, filename):
        with open(filename, mode='rb') as file:
            contents = file.read()
        
        # TODO: Split into individual messages based on SysEx star/end (i.e. F0/F7) bytes instead

        mesaages = []

        for i in range(len(contents) // MESSAGE_SIZE):
            mesaages.append(contents[i * MESSAGE_SIZE : (i + 1) * MESSAGE_SIZE])

        return mesaages


if __name__ == '__main__':
    pass