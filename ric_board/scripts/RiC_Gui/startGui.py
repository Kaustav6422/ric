#!/usr/bin/env python
import sys
from GUI.Program import Program

__author__ = 'tom1231'
import rospy
import rospkg



def main():
    rospy.init_node('RiC_GUI')
    rospkg.RosPack().get_path('ric_board')
    Program(rospkg.RosPack().get_path('ric_board'))


if __name__ == '__main__':
    main()




