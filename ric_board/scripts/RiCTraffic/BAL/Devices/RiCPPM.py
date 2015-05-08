__author__ = 'tom1231'
import rospy
from rospy import Publisher
from ric_board.msg import PPM
from BAL.Interfaces.Device import Device


class RiCPPM(Device):

    def __init__(self, param):
        Device.__init__(self, param.getPPMName(), None)
        self._pub = Publisher('%s' % self._name, PPM, queue_size=param.getPPMPubHz())

    def publish(self, data):
        msg = PPM()
        msg.channels = data.getChannels()
        self._pub.publish(msg)