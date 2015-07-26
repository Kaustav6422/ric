
from threading import Thread
import time
import rospy
import rostopic
from BAL.Header.Requests.PublishRequest import PublishRequest
from BAL.Header.Response.ParamBuildResponse import Battery

__author__ = 'tom1231'
from rospy import Publisher
from std_msgs.msg import Float32
from BAL.Interfaces.Device import Device
import re

class RiCBattery(Device):
    def __init__(self, param, output):
        Device.__init__(self, param.getBatteryName(), output)
        self._pub = Publisher('%s' % self._name, Float32, queue_size=param.getBatteryPubHz())
        self._haveRightToPublish = False
        Thread(target=self.checkForSubscribers, args=()).start()

    def publish(self, data):
        msg = Float32()
        msg.data = data
        self._pub.publish(msg)

    def checkForSubscribers(self):
        try:
            while not rospy.is_shutdown():
                subCheck = re.search('Subscribers:.*', rostopic.get_info_text(self._pub.name)).group(0).split(': ')[1]

                if not self._haveRightToPublish and subCheck == '':
                    self._output.write(PublishRequest(Battery, 0, True).dataTosend())
                    self._haveRightToPublish = True

                elif self._haveRightToPublish and subCheck == 'None':
                    self._output.write(PublishRequest(Battery, 0, False).dataTosend())
                    self._haveRightToPublish = False
        except: pass
