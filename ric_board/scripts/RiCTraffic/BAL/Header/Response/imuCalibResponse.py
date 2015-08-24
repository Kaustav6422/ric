from BAL.Header.RiCHeader import RiCHeader

__author__ = 'tom'
import struct

X_MAX = 10
Y_MAX = 14
Z_MAX = 18

X_MIN = 22
Y_MIN = 26
Z_MIN = 30


class ImuCalibResponse(RiCHeader):
    def __init__(self):
        RiCHeader.__init__(self)
        self._xMax = 0.0
        self._yMax = 0.0
        self._zMax = 0.0
        self._xMin = 0.0
        self._yMin = 0.0
        self._zMin = 0.0

    def getImuMsgId(self):
        return 1


    def buildRequest(self, data):
        RiCHeader.buildRequest(self, data)
        bytes = bytearray()

        while self.index < X_MAX:
            bytes.append(data[self.index])
            self.index += 1

        self._xMax = struct.unpack('<f', bytes)[0]

        bytes = bytearray()

        while self.index < Y_MAX:
            bytes.append(data[self.index])
            self.index += 1

        self._yMax = struct.unpack('<f', bytes)[0]

        bytes = bytearray()

        while self.index < Z_MAX:
            bytes.append(data[self.index])
            self.index += 1

        self._zMax = struct.unpack('<f', bytes)[0]

        bytes = bytearray()

        while self.index < X_MIN:
            bytes.append(data[self.index])
            self.index += 1

        self._xMin = struct.unpack('<f', bytes)[0]

        bytes = bytearray()

        while self.index < Y_MIN:
            bytes.append(data[self.index])
            self.index += 1

        self._yMin = struct.unpack('<f', bytes)[0]

        bytes = bytearray()

        while self.index < Z_MIN:
            bytes.append(data[self.index])
            self.index += 1

        self._zMin = struct.unpack('<f', bytes)[0]

    def getValues(self):

        return (
            self._xMax,
            self._yMax,
            self._zMax,
            self._xMin,
            self._yMin,
            self._zMin,
        )
