__author__ = 'tom1231'
import struct
from BAL.Header.RiCHeader import RiCHeader
from geometry_msgs.msg import Vector3, Quaternion
V_X_LEN = 12
V_Y_LEN = 16
V_Z_LEN = 20

A_X_LEN = 24
A_Y_LEN = 28
A_Z_LEN = 32

M_X_LEN = 36
M_Y_LEN = 40
M_Z_LEN = 44

O_X_LEN = 48
O_Y_LEN = 52
O_Z_LEN = 56
O_W_LEN = 60

# ROLL_LEN = 64
# PITCH_LEN = 68
# YAW_LEN = 72
# TEMP_LEN = 76

class IMUPublishResponse(RiCHeader):
    def __init__(self):
        RiCHeader.__init__(self)
        self._velocityX = 0.0
        self._velocityY = 0.0
        self._velocityZ = 0.0

        self._accelerationX = 0.0
        self._accelerationY = 0.0
        self._accelerationZ = 0.0

        self._magnetometerX = 0.0
        self._magnetometerY = 0.0
        self._magnetometerZ = 0.0

        self._orientationX = 0.0
        self._orientationY = 0.0
        self._orientationZ = 0.0
        self._orientationW = 0.0

        self._roll = 0.0
        self._pitch = 0.0
        self._yaw = 0.0
        self._temperature = 0.0

    def getVelocity(self):
        vec = Vector3()
        vec.x = self._velocityX
        vec.y = self._velocityY
        vec.z = self._velocityZ
        return vec

    def getAcceleration(self):
        acc = Vector3()
        acc.x = self._accelerationX
        acc.y = self._accelerationY
        acc.z = self._accelerationZ
        return acc

    def getMagnetometer(self):
        mag = Vector3()
        mag.x = self._magnetometerX
        mag.y = self._magnetometerY
        mag.z = self._magnetometerZ
        return mag

    def getOrientation(self):
        ort = Quaternion()
        ort.x = self._orientationX
        ort.y = self._orientationY
        ort.z = self._orientationZ
        ort.w = self._orientationW
        return ort

    def getRoll(self):
        return self._roll

    def getPitch(self):
        return self._pitch

    def getYaw(self):
        return self._yaw

    def getTemperature(self):
        return self._temperature

    def buildRequest(self, data):
        RiCHeader.buildRequest(self, data)
        bytes = bytearray()
        while self.index < V_X_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._velocityX = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < V_Y_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._velocityY = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < V_Z_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._velocityZ = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < A_X_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._accelerationX = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < A_Y_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._accelerationY = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < A_Z_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._accelerationZ = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < M_X_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._magnetometerX = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < M_Y_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._magnetometerY = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < M_Z_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._magnetometerZ = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < O_X_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._orientationX = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < O_Y_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._orientationY = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < O_Z_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._orientationZ = struct.unpack('<f', bytes)[0]
        bytes = bytearray()
        while self.index < O_W_LEN:
            bytes.append(data[self.index])
            self.index += 1
        self._orientationW = struct.unpack('<f', bytes)[0]
        # bytes = bytearray()
        # while self.index < ROLL_LEN:
        #     bytes.append(data[self.index])
        #     self.index += 1
        # self._roll = struct.unpack('<f', bytes)[0]
        # bytes = bytearray()
        # while self.index < PITCH_LEN:
        #     bytes.append(data[self.index])
        #     self.index += 1
        # self._pitch = struct.unpack('<f', bytes)[0]
        # bytes = bytearray()
        # while self.index < YAW_LEN:
        #     bytes.append(data[self.index])
        #     self.index += 1
        # self._yaw = struct.unpack('<f', bytes)[0]
        # bytes = bytearray()
        # while self.index < TEMP_LEN:
        #     bytes.append(data[self.index])
        #     self.index += 1
        # self._temperature = struct.unpack('<f', bytes)[0]
