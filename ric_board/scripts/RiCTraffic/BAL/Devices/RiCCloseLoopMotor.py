import re
from threading import Thread
import rospy
import rostopic
from BAL.Header.Requests.PublishRequest import PublishRequest
from BAL.Header.Requests.closeMotorRequest import CloseMotorRequest
from BAL.Header.Response.ParamBuildResponse import EngineCL

__author__ = 'tom1231'
from rospy import Publisher, Subscriber
from std_msgs.msg import Float32
from ric_board.msg import Motor
from BAL.Interfaces.Device import Device



class RiCCloseLoopMotor(Device):

    def __init__(self, motorNum ,param,output):
        Device.__init__(self, param.getCloseLoopMotorName(motorNum), output)
        self._motorId = motorNum
        self._pub = Publisher('%s/feedback' % self._name, Motor, queue_size=param.getCloseLoopMotorPubHz(motorNum))
        Subscriber('%s/command' % self._name, Float32, self.MotorCallback, queue_size=1)
        self._haveRightToPublish = False
        Thread(target=self.checkForSubscribers, args=()).start()

    def publish(self, data):
        msg = Motor()
        msg.position = data[0]
        msg.velocity = data[1]
        self._pub.publish(msg)

    def MotorCallback(self, msg):
        Thread(target=self.sendMsg, args=(msg,)).start()

    def sendMsg(self, msg):
        req = CloseMotorRequest(self._motorId, msg.data)
        self._output.write(req.dataTosend())

    def checkForSubscribers(self):
        try:
            while not rospy.is_shutdown():
                subCheck = re.search('Subscribers:.*', rostopic.get_info_text(self._pub.name)).group(0).split(': ')[1]

                if not self._haveRightToPublish and subCheck == '':
                    self._output.write(PublishRequest(EngineCL, self._motorId, True).dataTosend())
                    self._haveRightToPublish = True

                elif self._haveRightToPublish and subCheck == 'None':
                    self._output.write(PublishRequest(EngineCL, 0, False).dataTosend())
                    self._haveRightToPublish = False
        except: pass