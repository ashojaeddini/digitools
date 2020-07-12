from .tag import Tag

class Sound:

    def __init__(self, message):
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
    def decode(data):
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
    def extract_tags(data):
        tag_data = data[0x08 : 0x0C]

        tags = []

        for t in Tag:
            if (tag_data[3 - (t.value // 8)] >> (t.value % 8)) & 1:
                tags.append(t.name)

        return tags

    @staticmethod
    def extract_name(data):
        name_data = data[0x0C : min(data.index(0x00, 0x0C), 0x1B)]

        return str(name_data, 'latin-1')

    def message(self):
        return self._message

    def data(self):
        return self._data

    def name(self):
        return self._name

    def tags(self):
        return self._tags

    def __str__(self):
        #return self._name
        return f'{self._name} {self._tags}'