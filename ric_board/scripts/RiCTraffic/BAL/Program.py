import serial
import time
from BAL.Devices.DevicesBuilder.deviceBuilder import DeviceBuilder
from BAL.Handlers.incomingDataHandler import IncomingDataHandler
from BAL.Handlers.incomingHandler import IncomingHandler, MOTOR_RES, CLOSE_DIFF_RES, URF_RES, SWITCH_RES, IMU_RES,GPS_RES, \
    PPM_RES, BAT_RES
from BAL.Handlers.serialWriteHandler import SerialWriteHandler, HEADER_START
from BAL.Header.Response.IMUPublishResponse import IMUPublishResponse
from BAL.Header.Response.ServoPublishResponse import ServoPublishResponse
from BAL.Header.Response.URFPublishResponse import URFPublishResponse
from BAL.Header.Response.batteryPublishResponse import BatteryPublishResponse
from BAL.Header.Response.closeDiffPublishResponse import CloseDiffPublishRepose
from BAL.Header.Response.closeLoopPublishResponse import CloseLoopPublishResponse
from BAL.Header.Response.gpsPublishResponse import GPSPublishResponse
from BAL.Header.Response.ppmPublishResponse import PPMPublishResponse
from BAL.Header.Response.switchResponse import SwitchResponse

__author__ = 'tom1231'
import roslib; roslib.load_manifest('ric_board')
import rospy
from rospy import Subscriber, Publisher,Service
from BAL.Header.Response.ConnectionResponse import ConnectionResponse, RES_ID
from BAL.Header.RiCHeader import RiCHeader
from BAL.Header.Requests.ConnectionRequest import ConnectionRequest
from BAL.RiCParam.RiCParam import RiCParam
from serial import Serial, SerialException
import sys
from threading import Thread

CON_REQ = 1

SERVO_RES = 102
STATUS_RES = 100

class Program:

    def __init__(self):
        try:
            rospy.init_node('RiCTraffic')
            ser = Serial('/dev/RiCBoard')
            ser.flushInput()
            ser.flushOutput()
            # ser = Serial('/dev/ttyUSB0')
            incomingHandler = IncomingHandler()
            params = RiCParam()
            input = ser
            output = SerialWriteHandler(ser, incomingHandler, input)
            data = []
            input.baudrate = 9600
            incomingLength = 0
            headerId = 0
            devBuilder = DeviceBuilder(params, output, input, incomingHandler)
            gotHeaderStart = False

            try:
                self.waitForConnection(input, output)
                # rospy.loginfo("Connect to 0x%x.....", self.waitForConnection(input, output))
                rospy.loginfo("Configuring devices...")
                devBuilder.createServos()
                devBuilder.createCLMotors()
                devBuilder.createDiff()
                devBuilder.createURF()
                devBuilder.createSwitchs()
                devBuilder.createIMU()
                devBuilder.createRelays()
                devBuilder.createGPS()
                devBuilder.createPPM()
                devBuilder.createOpenLoopMotors()
                devBuilder.createBattery()
                devBuilder.createOpenDiff()
                devs = devBuilder.getDevs()
                devBuilder.sendFinishBuilding()
                input.timeout = None
                rospy.loginfo("Done, RiC Board is ready.")
                while not rospy.is_shutdown():
                    if gotHeaderStart:
                        if len(data) < 2:
                            data.append(input.read())
                            if len(data) == 2:
                                incomingLength ,headerId = incomingHandler.getIncomingHeaderSizeAndId(data)
                        elif incomingLength >= 2:
                            for i in range(2, incomingLength):
                                data.append(input.read())
                            # print data
                            msg = self.genData(data, headerId)
                            if msg is not None:
                                    Thread(target=IncomingDataHandler(msg, output, devs).run, args=()).start()
                            data = []
                            gotHeaderStart = False
                        else:
                            data = []
                            gotHeaderStart = False
                    elif ord(input.read()) == HEADER_START: gotHeaderStart = True

            except KeyboardInterrupt: pass
            finally:
                con = ConnectionResponse(False)
                output.writeAndWaitForAck(con.dataTosend(), RES_ID)
                ser.close()
        except SerialException:
            rospy.logerr("Can't find RiCBoard, please check if its connected to the computer.")

    def genData(self, data, headerId):
        result = None
        if headerId == CON_REQ: result = ConnectionRequest()
        if headerId == SERVO_RES: result = ServoPublishResponse()
        if headerId == MOTOR_RES: result = CloseLoopPublishResponse()
        if headerId == CLOSE_DIFF_RES: result = CloseDiffPublishRepose()
        if headerId == URF_RES: result = URFPublishResponse()
        if headerId == SWITCH_RES: result = SwitchResponse()
        if headerId == IMU_RES: result = IMUPublishResponse()
        if headerId == GPS_RES: result = GPSPublishResponse()
        if headerId == PPM_RES: result = PPMPublishResponse()
        if headerId == BAT_RES: result = BatteryPublishResponse()

        if result is not None: result.buildRequest(data)
        return result

    def waitForConnection(self, input, output):
        # isConnect = False
        # gotHeaderStart = False
        # data = []
        # while not rospy.is_shutdown() and not isConnect:
        #     if gotHeaderStart:
        #         for i in xrange(10):
        #             data.append(input.read())
        #         conReq = ConnectionRequest()
        #         conReq.buildRequest(data)
        #         if conReq.checkPackage() and conReq.toConnect():
        #             d = ConnectionResponse(True).dataTosend()
        #             for i in d:
        #                 print ord(i)

                    output.writeAndWaitForAck(ConnectionResponse(True).dataTosend(), RES_ID)

        #             isConnect = True
        #         gotHeaderStart = False
        #     elif ord(input.read()) == HEADER_START: gotHeaderStart = True
        #  return conReq.getDes()
