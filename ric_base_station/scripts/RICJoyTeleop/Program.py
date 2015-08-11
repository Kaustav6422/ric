#!/usr/bin/env python
__author__ = 'tom1231'
import pygame
from pygame.locals import *
import rospy
import sys
from threading import Thread, RLock
from geometry_msgs.msg import Twist

LEFT_RIGHT_NUM = 0
UP_DOWN_NUM = 1

BOOST_SPEED_BUTTON = 4
ENABLE_BUTTON = 5

class Program:
    def __init__(self):
        self._axes = [0.0, 0.0]
        self._enable = False
        self._maxSpeed = float(sys.argv[1])
        self._maxSpeedWithBoot = float(sys.argv[2])
        self._factor = self._maxSpeed
        self._lock = RLock()

        rospy.init_node('ric_joyTeleop')
        self._pub = rospy.Publisher('%s/command' % sys.argv[3], Twist, queue_size=1)

        rospy.loginfo("listen to %s" % self._pub.name)

        Thread(target=self.listenToJoystick, args=()).start()

        rate = rospy.Rate(20)
        try:
            while not rospy.is_shutdown():
                if self.isEnable():
                    msg = Twist()

                    msg.linear.x = -self.getUpAndDownAxes()
                    msg.angular.z = self.getLeftAndRightAxes()

                    self._pub.publish(msg)
                rate.sleep()

        except KeyboardInterrupt: pass
        finally:
            pygame.event.post(pygame.event.Event(QUIT))

    def setLeftAndRightAxes(self, newAxis):
        with self._lock:
            self._axes[0] = newAxis

    def setUpAndDownAxes(self, newAxis):
        with self._lock:
            self._axes[1] = newAxis

    def getLeftAndRightAxes(self):
        with self._lock:
            return self._axes[LEFT_RIGHT_NUM] * self.getFactor()

    def getUpAndDownAxes(self):
        with self._lock:
            return self._axes[UP_DOWN_NUM] * self.getFactor()

    def setEnable(self, newVal):
        with self._lock:
            self._enable = newVal

    def isEnable(self):
        with self._lock:
            return self._enable

    def setFactor(self, val):
        with self._lock:
            self._factor = val

    def getFactor(self):
        with self._lock:
            return self._factor

    def listenToJoystick(self):
        pygame.init()
        pygame.joystick.init()

        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        quitLoop = False

        while not quitLoop:
            event = pygame.event.wait()
            if event.type == QUIT:
                quitLoop = True

            elif event.type == JOYAXISMOTION:
                if self.isEnable():
                    data = event.dict
                    if data['axis'] == LEFT_RIGHT_NUM:
                        self.setLeftAndRightAxes(data['value'])
                    elif data['axis'] == UP_DOWN_NUM:
                        self.setUpAndDownAxes(data['value'])

            elif event.type == JOYBUTTONDOWN:
                if event.dict['button'] == BOOST_SPEED_BUTTON:
                    self.setFactor(self._maxSpeedWithBoot)
                elif event.dict['button'] == ENABLE_BUTTON:
                    self.setEnable(True)

            elif event.type == JOYBUTTONUP:
                if event.dict['button'] == BOOST_SPEED_BUTTON:
                    self.setFactor(self._maxSpeed)
                elif event.dict['button'] == ENABLE_BUTTON:
                    self.setEnable(False)
                    self.setLeftAndRightAxes(0.0)
                    self.setUpAndDownAxes(0.0)


if __name__ == '__main__':
    Program()
