__author__ = 'tom1231'

import struct
import binascii

ID_PLACE = 2
LENGTH_PLACE = 4
DES_PLACE = 6
CHECK_SUM_PLACE = 8

# lst = ['\x01', '\x00', '\n', '\x00', '\x01', '\x10', '\x00', '\x00', '\x01', '\x00']


class RiCHeader:
    def __init__(self):
        self.index = 0
        self._id = 0
        self._length = 0
        self._des = 0
        self._checkSum = 0

    def buildRequest(self, data):
        bytes = bytearray()
        while self.index < ID_PLACE:
            bytes.append(data[self.index])
            self.index += 1
        self._id = struct.unpack('<h', bytes)[0]
        bytes = bytearray()
        while self.index < LENGTH_PLACE:
            bytes.append(data[self.index])
            self.index += 1
        self._length = struct.unpack('<h', bytes)[0]
        bytes = bytearray()
        while self.index < DES_PLACE:
            bytes.append(data[self.index])
            self.index += 1
        self._des = struct.unpack('<h', bytes)[0]
        bytes = bytearray()
        while self.index < CHECK_SUM_PLACE:
            bytes.append(data[self.index])
            data[self.index] = '\x00'
            self.index += 1
        self._checkSum = struct.unpack('<h', bytes)[0]
        self.checkSumRes = self.calCheckSum(data)

    def getId(self):
        return self._id

    def getDes(self):
        return self._des

    def getLength(self):
        return self._length

    def getCheckSum(self):
        return self._checkSum

    def checkPackage(self):
        return self.checkSumRes == self._checkSum

    def calCheckSum(self, data):
        res = 0
        for val in data:
            res += ord(val)
        return res

    def dataTosend(self):
        return struct.pack('<h', self._id) \
               + struct.pack('<h', self._length) \
               + struct.pack('<h', self._des) \
               + struct.pack('<h', self._checkSum)
