#!/usr/bin/env python
import roslib; roslib.load_manifest('ric_robot')
import rospy
import math
from dynamixel_msgs.msg import JointState as dxl_JointState
from sensor_msgs.msg import JointState
from math import *
from ric_robot.srv import *
from ric_robot.msg import *
from std_msgs.msg import Float64

def br_callback(data):       
    global msg,ns
    msg.name[0]=ns+"_"+data.name
    msg.position[0]=data.current_pos
    msg.velocity[0]=data.velocity
    msg.effort[0]=data.load

def sh_callback(data):       
    global msg,ns
    msg.name[1]=ns+"_"+data.name
    msg.position[1]=data.current_pos
    msg.velocity[1]=data.velocity
    msg.effort[1]=data.load

def e1_callback(data):       
    global msg,ns
    msg.name[2]=ns+"_"+data.name
    msg.position[2]=data.current_pos
    msg.velocity[2]=data.velocity
    msg.effort[2]=data.load

def e2_callback(data):       
    global msg,ns
    msg.name[3]=ns+"_"+data.name
    msg.position[3]=data.current_pos
    msg.velocity[3]=data.velocity
    msg.effort[3]=data.load

def wr_callback(data):       
    global msg,ns
    msg.name[4]=ns+"_"+data.name
    msg.position[4]=data.current_pos
    msg.velocity[4]=data.velocity
    msg.effort[4]=data.load

def lf_callback(data):       
    global msg,ns
    msg.name[5]=ns+"_"+data.name
    msg.position[5]=data.current_pos
    msg.velocity[5]=data.velocity
    msg.effort[5]=data.load

def rf_callback(data):       
    global msg,ns
    msg.name[6]=ns+"_"+data.name
    msg.position[6]=data.current_pos
    msg.velocity[6]=data.velocity
    msg.effort[6]=data.load

def komodo_arm():
    global pub,msg,ns
    ns=rospy.get_namespace()
    ns=ns[1:-1]
    msg = JointState()
    for i in range(7):
        msg.name.append("")
        msg.position.append(0.0)
	msg.velocity.append(0.0)
	msg.effort.append(0.0)
    rospy.init_node('komodo_arm', anonymous=True)
    rospy.Subscriber("/"+ns+"/base_rotation_controller/state", dxl_JointState, br_callback)
    rospy.Subscriber("/"+ns+"/shoulder_controller/state", dxl_JointState, sh_callback)
    rospy.Subscriber("/"+ns+"/elbow1_controller/state", dxl_JointState, e1_callback)
    rospy.Subscriber("/"+ns+"/elbow2_controller/state", dxl_JointState, e2_callback)
    rospy.Subscriber("/"+ns+"/left_finger_controller/state", dxl_JointState, lf_callback)
    rospy.Subscriber("/"+ns+"/right_finger_controller/state", dxl_JointState, rf_callback)
    rospy.Subscriber("/"+ns+"/wrist_controller/state", dxl_JointState, wr_callback)
    pub = rospy.Publisher('/joint_states', JointState)
   
    while not rospy.is_shutdown():
    	msg.header.stamp = rospy.Time.now()
    	pub.publish(msg)
        #rospy.loginfo(ns)
	rospy.sleep(0.05)

if __name__ == '__main__':
    komodo_arm()



