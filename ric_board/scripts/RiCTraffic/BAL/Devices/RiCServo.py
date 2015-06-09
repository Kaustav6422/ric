from threading import Thread
from BAL.Header.Requests.servoRequest import ServoRequest

__author__ = 'tom1231'
from rospy import Publisher, Subscriber
from std_msgs.msg import Float32
from BAL.Interfaces.Device import Device


class RiCServo(Device):

    def __init__(self, params, servoNum, output):
        Device.__init__(self, params.getServoName(servoNum), output)
        self._servoNum = servoNum
        self._pub = Publisher('%s/Position' % self._name, Float32, queue_size=params.getServoPublishHz(servoNum))
        Subscriber('%s/command' % self._name, Float32, self.servoCallBack)

    def publish(self, data):
        msg = Float32()
        msg.data = data
        self._pub.publish(msg)

    def servoCallBack(self, recv):
        Thread(target=self.sendMsg, args=(recv,)).start()
        # TOOD: ServoRequest


    def sendMsg(self, recv):
        position = recv.data
        msg = ServoRequest(self._servoNum, position)
        self._output.write(msg.dataTosend())