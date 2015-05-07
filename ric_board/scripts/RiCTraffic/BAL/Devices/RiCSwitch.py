__author__ = 'tom1231'
from rospy import Publisher
from BAL.Interfaces.Device import Device
from std_msgs.msg import Bool


class RiCSwitch(Device):


    def __init__(self, devId,param):
        Device.__init__(self, param.getSwitchName(devId), None)
        self._pub = Publisher('%s' % self._name, Bool, queue_size=param.getSwitchPubHz(devId))

    def publish(self, data):
        msg = Bool()
        msg.data = data
        self._pub.publish(msg)
