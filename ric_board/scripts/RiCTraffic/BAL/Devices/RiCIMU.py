import rospy

__author__ = 'tom1231'
from rospy import Publisher
from sensor_msgs.msg import Imu, MagneticField
from BAL.Interfaces.Device import Device

class RiCIMU(Device):
    def __init__(self,param ,output):
        Device.__init__(self, param.getIMUName(), output)
        self._frameId = param.getIMUFrameId()
        self._pub = Publisher('%s_AGQ' % self._name, Imu, queue_size=param.getIMUPubHz())
        self._pubMag = Publisher('%s_M' % self._name, MagneticField, queue_size=param.getIMUPubHz())

    def publish(self, data):
        msg = Imu()
        msg.header.frame_id = self._frameId
        msg.header.stamp = rospy.get_rostime()
        msg.orientation = data.getOrientation()
        msg.linear_acceleration = data.getAcceleration()
        msg.angular_velocity = data.getVelocity()

        magMsg = MagneticField()
        magMsg.header.frame_id = self._frameId
        magMsg.header.stamp = rospy.get_rostime()
        magMsg.magnetic_field = data.getMagnetometer()

        self._pub.publish(msg)
        self._pubMag.publish(magMsg)