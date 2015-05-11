__author__ = 'tom1231'
from rospy import Publisher
from std_msgs.msg import Float32
from BAL.Interfaces.Device import Device


class RiCBattery(Device):
    def __init__(self, param):
        Device.__init__(self, param.getBatteryName(), None)
        self._pub = Publisher('%s' % self._name, Float32, queue_size=param.getBatteryPubHz())

    def publish(self, data):
        msg = Float32()
        msg.data = data
        self._pub.publish(msg)