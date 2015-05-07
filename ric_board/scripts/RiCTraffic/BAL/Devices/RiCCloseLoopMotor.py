from BAL.Header.Requests.closeMotorRequest import CloseMotorRequest

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
        Subscriber('%s/command' % self._name, Float32, self.MotorCallback)

    def publish(self, data):
        msg = Motor()
        msg.position = data[0]
        msg.velocity = data[1]
        self._pub.publish(msg)

    def MotorCallback(self, msg):
        req = CloseMotorRequest(self._motorId, msg.data)
        self._output.write(req.dataTosend())
