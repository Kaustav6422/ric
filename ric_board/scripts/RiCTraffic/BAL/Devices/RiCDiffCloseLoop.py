from threading import Thread
from nav_msgs.msg import Odometry
import rospy
from BAL.Header.Requests.closeDiffRequest import CloseDiffRequest
from BAL.Header.Requests.closeDiffSetOdomRequest import CloseDiffSetOdomRequest

__author__ = 'tom1231'
from BAL.Interfaces.Device import Device
from rospy import Subscriber, Service, Publisher
# from ric_board.msg import Odometry
from ric_board.srv._set_odom import set_odom, set_odomResponse
from tf import TransformBroadcaster
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Twist, TransformStamped, Quaternion


class RiCDiffCloseLoop(Device):

    def __init__(self, param, output):
        Device.__init__(self, param.getCloseDiffName(), output)
        self._baseLink = param.getCloseDiffBaseLink()
        self._odom = param.getCloseDiffOdom()
        self._maxAng = param.getCloseDiffMaxAng()
        self._maxLin = param.getCloseDiffMaxLin()
        self._pub = Publisher("%s/odometry" % self._name, Odometry, queue_size=param.getCloseDiffPubHz())
        self._broadCase = TransformBroadcaster()
        Subscriber('%s/command' % self._name, Twist, self.diffServiceCallback, queue_size=1)
        Service('%s/setOdometry' % self._name, set_odom, self.setOdom)

    def diffServiceCallback(self, msg):
        Thread(target=self.sendMsg, args=(msg,)).start()

    def sendMsg(self, msg):
        if msg.angular.z > self._maxAng:
            msg.angular.z = self._maxAng
        elif msg.angular.z < -self._maxAng:
            msg.angular.z = -self._maxAng

        if msg.linear.x > self._maxLin:
            msg.linear.x = self._maxLin
        elif msg.linear.x < -self._maxLin:
            msg.linear.x = -self._maxLin
        # print msg.angular.z, msg.linear.x
        self._output.write(CloseDiffRequest(msg.angular.z, msg.linear.x).dataTosend())


    def setOdom(self, req):
        self._output.write(CloseDiffSetOdomRequest(req.x, req.y, req.theta).dataTosend())
        return set_odomResponse(True)

    def publish(self, data):
        q = Quaternion()
        q.x = 0
        q.y = 0
        q.z = data[6]
        q.w = data[7]
        odomMsg = Odometry()
        odomMsg.header.frame_id = self._odom
        odomMsg.header.stamp = rospy.get_rostime()
        odomMsg.child_frame_id = self._baseLink
        odomMsg.pose.pose.position.x = data[0]
        odomMsg.pose.pose.position.y = data[1]
        odomMsg.pose.pose.position.z = 0
        odomMsg.pose.pose.orientation = q
        self._pub.publish(odomMsg)
        traMsg = TransformStamped()
        traMsg.header.frame_id = self._odom
        traMsg.header.stamp = rospy.get_rostime()
        traMsg.child_frame_id = self._baseLink
        traMsg.transform.translation.x = data[0]
        traMsg.transform.translation.y = data[1]
        traMsg.transform.translation.z = 0
        traMsg.transform.rotation = q
        self._broadCase.sendTransformMessage(traMsg)

