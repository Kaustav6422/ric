import struct

__author__ = 'tom1231'

CON_REQ = 1
RELAY_REQ = 12
OPEN_LOOP_REQ = 15

SERVO_RES = 102
ACK_RES = 105
MOTOR_RES = 106
CLOSE_DIFF_RES = 108
URF_RES = 109
SWITCH_RES = 110
IMU_RES = 111
GPS_RES = 113
PPM_RES = 114
BAT_RES = 116

class IncomingHandler:

    def getIncomingHeaderId(self, data):
        return struct.unpack('<h', bytearray(data))[0]

    def getIncomingHeaderSizeAndId(self, data):
        id = self.getIncomingHeaderId(data)
        if id == CON_REQ: return 10, id
        if id == SERVO_RES: return 16, id
        if id == ACK_RES: return 16, id
        if id == MOTOR_RES: return 20, id
        if id == CLOSE_DIFF_RES: return 28, id
        if id == URF_RES: return 16, id
        if id == SWITCH_RES: return 16, id
        if id == IMU_RES: return 60, id
        if id == GPS_RES: return 48, id
        if id == PPM_RES: return 40, id
        if id == BAT_RES: return 12, id
        return 0, 0

