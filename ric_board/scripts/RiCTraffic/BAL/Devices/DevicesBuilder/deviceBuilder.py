from BAL.Devices.RiCDiffCloseLoop import RiCDiffCloseLoop
from BAL.Devices.RiCGPS import RiCGPS
from BAL.Devices.RiCIMU import RiCIMU
from BAL.Devices.RiCRelay import RiCRelay
from BAL.Devices.RiCSwitch import RiCSwitch
from BAL.Devices.RiCURF import RiCURF
from BAL.Header.Response.CloseLoopMotorTwoEncBuildResponse import CloseLoopMotorTwoEncBuildResponse
from BAL.Header.Response.IMUParamResponse import IMUParamResponse
from BAL.Header.Response.ParamBuildResponse import EngineCL, EngineCL2
from BAL.Header.Response.closeDiffParamResponse import CloseDiffParamResponse
from BAL.Header.Response.gpsParamResponse import GPSParamResponse
from BAL.Header.Response.relayParamResponse import RelayParamResponse
from BAL.Header.Response.switchParamResponse import SwitchParamResponse
from BAL.Header.Response.urfParamResponse import URFParamResponse

__author__ = 'tom1231'

import rospy
from BAL.Header.Requests.finishBuildingRequest import FinishBuildingRequest, ID_REQ
from BAL.Devices.RiCCloseLoopMotor import RiCCloseLoopMotor
from BAL.Devices.RiCServo import RiCServo
from BAL.Header.Response.BuildServoResponse import BuildServoResponse
from BAL.Header.Response.closeLoopMotorBuildResponse import CloseLoopMotorBuildResponse
from BAL.Header.Response.ackResponse import ACKResponse
from BAL.Handlers.incomingHandler import ACK_RES
from BAL.Handlers.serialWriteHandler import HEADER_START


class DeviceBuilder:
    def __init__(self, param, output, input, incomingDataHandle):
        self._param = param
        self._output = output
        self._input = input
        self._incomingDataHandler = incomingDataHandle
        self._allDevs = dict()
        self._allDevs['servos'] = []
        self._allDevs['motorsCl'] = []
        self._allDevs['urf'] = []
        self._allDevs['switch'] = []
        self._allDevs['diff'] = []
        self._allDevs['imu'] = []
        self._allDevs['relay'] = []
        self._allDevs['gps'] = []

    def createServos(self):
        servoAmount = self._param.getServoNum()
        for servoNum in xrange(servoAmount):
            rospy.loginfo("Building servo name: %s", self._param.getServoName(servoNum))
            self._allDevs['servos'].append(RiCServo(self._param, servoNum, self._output))
            servoTORic = BuildServoResponse(servoNum, self._param)
            self._output.writeAndWaitForAck(servoTORic.dataTosend(), servoNum)
            rospy.loginfo("Building servo name: %s was done successfully", self._param.getServoName(servoNum))

    def createCLMotors(self):
        closeMotorsAmount = self._param.getCloseLoopMotorSize()
        for motorNum in xrange(closeMotorsAmount):
            rospy.loginfo("building motor name: %s", self._param.getCloseLoopMotorName(motorNum))
            motor = RiCCloseLoopMotor(motorNum, self._param, self._output)
            self._allDevs['motorsCl'].append(motor)
            if self._param.getCloseLoopMotorEncoderType(motorNum) == 1:
                toSend = CloseLoopMotorBuildResponse(motorNum, self._param, EngineCL)
            else:
                toSend = CloseLoopMotorTwoEncBuildResponse(motorNum, self._param, EngineCL2)
            self._output.writeAndWaitForAck(toSend.dataTosend(), motorNum)
            rospy.loginfo("Building motor name: %s, was done successfully", self._param.getCloseLoopMotorName(motorNum))

    def createDiff(self):
        if self._param.isInitCloseDiff():
            rospy.loginfo("Building differential drive name: %s", self._param.getCloseDiffName())
            diff = RiCDiffCloseLoop(self._param, self._output)
            self._allDevs['diff'].append(diff)
            toSend = CloseDiffParamResponse(0, self._param)
            self._output.writeAndWaitForAck(toSend.dataTosend(), 0)
            rospy.loginfo("Building differential drive name: %s, was done successfully", self._param.getCloseDiffName())

    def createURF(self):
        URFAmount = self._param.getURFNum()
        for urfId in xrange(URFAmount):
            rospy.loginfo("Building URF name: %s", self._param.getURFName(urfId))
            urf = RiCURF(urfId, self._param)
            self._allDevs['urf'].append(urf)
            self._output.writeAndWaitForAck(URFParamResponse(urf.getType(), urfId, self._param).dataTosend(), urfId)
            rospy.loginfo("Building URF name: %s, was done successfully", self._param.getURFName(urfId))
    def createSwitchs(self):
        switchAmount = self._param.getSwitchSize()
        for switchNum in xrange(switchAmount):
            rospy.loginfo("Building switch name: %s", self._param.getSwitchName(switchNum))
            switch = RiCSwitch(switchNum, self._param)
            self._allDevs['switch'].append(switch)
            self._output.writeAndWaitForAck(SwitchParamResponse(switchNum, self._param).dataTosend(), switchNum)
            rospy.loginfo("Building switch name: %s, was done successfully", self._param.getSwitchName(switchNum))
    def createIMU(self):
        if self._param.isImuInit():
            rospy.loginfo("Building IMU name: %s", self._param.getIMUName())
            imu = RiCIMU(self._param, self._output)
            self._allDevs['imu'].append(imu)
            self._output.writeAndWaitForAck(IMUParamResponse(self._param).dataTosend(), 0)
            rospy.loginfo("Building IMU name: %s, was done successfully", self._param.getIMUName())

    def createRelays(self):
        relayAmount = self._param.getRelaysSize()
        for relayNum in xrange(relayAmount):
            rospy.loginfo("Building relay name: %s", self._param.getRelayName(relayNum))
            relay = RiCRelay(self._param, relayNum, self._output)
            self._output.writeAndWaitForAck(RelayParamResponse(relayNum, self._param).dataTosend(), relayNum)
            self._allDevs['relay'].append(relay)
            rospy.loginfo("Building relay name: %s, was done successfully", self._param.getRelayName(relayNum))

    def createGPS(self):
        if self._param.isGpsInit():
            rospy.loginfo("Building GPS name: %s", self._param.getGpsName())
            gps = RiCGPS(self._param, self._output)
            self._output.writeAndWaitForAck(GPSParamResponse(self._param).dataTosend(), 0)
            self._allDevs['gps'].append(gps)
            rospy.loginfo("Building GPS name: %s, was done successfully", self._param.getGpsName())

    def getDevs(self):
        return self._allDevs

    def sendFinishBuilding(self):
        self._output.writeAndWaitForAck(FinishBuildingRequest().dataTosend(), ID_REQ)


