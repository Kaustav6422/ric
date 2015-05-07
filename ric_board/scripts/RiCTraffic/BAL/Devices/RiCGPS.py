import rospy

__author__ = 'tom1231'
from rospy import Publisher
from sensor_msgs.msg import NavSatFix
from BAL.Interfaces.Device import Device


class RiCGPS(Device):
    def __init__(self, param, output):
        Device.__init__(self, param.getGpsName(), output)
        self._frameId = param.getGpsFrameId()
        self._pub = Publisher('%s' % self._name, NavSatFix, queue_size=param.getGpsPubHz())

    def publish(self, data):
        msg = NavSatFix()
        msg.header.frame_id = self._frameId
        msg.header.stamp = rospy.get_rostime()
        msg.latitude = data.getLat()
        msg.longitude = data.getLng()
        msg.altitude = data.getMeters()
        msg.status.status = 0
        msg.status.service = 1
        self._pub.publish(msg)