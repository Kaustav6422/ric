__author__ = 'caja'
import rospy
import time
import shlex
import subprocess
from threading import Thread
from BAL.Interfaces.Runnable import Runnable

TIME_OUT = 3000


class KeepAliveHandler(Runnable):

    is_init = False

    def __init__(self, topic_name, msg_type):
        if self.is_init: pass
        self.is_init = True
        self._watch_dog_time = int(round(time.time() * 1000))
        rospy.Subscriber(topic_name, msg_type, self.callback_to_watch)
        Thread(target=self.run, args=()).start()

    def run(self):
        rate = rospy.Rate(20)
        while not rospy.is_shutdown():
            if int(round(time.time() * 1000)) - self._watch_dog_time > TIME_OUT:
                subprocess.Popen(shlex.split("pkill -f ros"))
            rate.sleep()

    def callback_to_watch(self, msg):
        self._watch_dog_time = int(round(time.time() * 1000))