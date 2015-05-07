__author__ = 'tom1231'
import struct
from BAL.Header.RiCHeader import RiCHeader

ID_LEN = 12
STATUS_LEN = 16

class SwitchResponse(RiCHeader):
    def __init__(self):
        RiCHeader.__init__(self)
        self._switchNum = 0
        self._status = 0

    def buildRequest(self, data):
        RiCHeader.buildRequest(self, data)
        bytes = bytearray()
        while self.index < ID_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._switchNum = struct.unpack('<i', bytes)[0]

        bytes = bytearray()
        while self.index < STATUS_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._status = struct.unpack('<i', bytes)[0]

    def getSwitchNum(self):
        return self._switchNum

    def getStatus(self):
        return self._status == 1


