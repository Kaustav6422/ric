import rospy

__author__ = 'tom1231'
from rospy import Publisher
from sensor_msgs.msg import Imu, MagneticField
from BAL.Interfaces.Device import Device
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Quaternion
from math import pi

class RiCIMU(Device):
    def __init__(self, param ,output):
        Device.__init__(self, param.getIMUName(), output)
        self._frameId = param.getIMUFrameId()
        self._angle = param.getIMUOrientation()
        self._pub = Publisher('%s_AGQ' % self._name, Imu, queue_size=param.getIMUPubHz())
        self._pubMag = Publisher('%s_M' % self._name, MagneticField, queue_size=param.getIMUPubHz())

    def publish(self, data):
        q = data.getOrientation()
        roll, pitch, yaw = euler_from_quaternion([q.w, q.x, q.y, q.z])

        # print "Before ", "Yaw: " + str(yaw * 180 / pi), "Roll: " + str(roll * 180 / pi), "pitch: " + str(pitch * 180 / pi), "\n\n"

        array = quaternion_from_euler(roll, pitch, yaw + (self._angle * pi / 180))


        res = Quaternion()
        res.w = array[0]
        res.x = array[1]
        res.y = array[2]
        res.z = array[3]

        roll, pitch, yaw = euler_from_quaternion([q.w, q.x, q.y, q.z])

        # print "after ", "Yaw: " + str(yaw * 180 / pi), "Roll: " + str(roll * 180 / pi), "pitch: " + str(pitch * 180 / pi), "\n\n"

        msg = Imu()
        msg.header.frame_id = self._frameId
        msg.header.stamp = rospy.get_rostime()
        msg.orientation = res
        msg.linear_acceleration = data.getAcceleration()
        msg.angular_velocity = data.getVelocity()

        magMsg = MagneticField()
        magMsg.header.frame_id = self._frameId
        magMsg.header.stamp = rospy.get_rostime()
        magMsg.magnetic_field = data.getMagnetometer()

        self._pub.publish(msg)
        self._pubMag.publish(magMsg)