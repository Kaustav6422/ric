#!/usr/bin/env python
import roslib
roslib.load_manifest('ric_robot')

import rospy
import actionlib
from std_msgs.msg import Float64
import trajectory_msgs.msg 
import control_msgs.msg  
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import JointTrajectoryAction, JointTrajectoryGoal, FollowJointTrajectoryAction, FollowJointTrajectoryGoal



class Joint:
        def __init__(self, motor_name):
            #arm_name should be b_arm or f_arm
            self.name = motor_name           
            self.jta = actionlib.SimpleActionClient('/komodo_1/komodo_arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
            rospy.loginfo('Waiting for joint trajectory action')
            self.jta.wait_for_server()
            rospy.loginfo('Found joint trajectory action!')

            
        def move_joint(self, angles):
            goal = FollowJointTrajectoryGoal()                  
            #char = self.name[0] #either 'f' or 'b'
            goal.trajectory.joint_names = ['base_rotation_joint','shoulder_joint','elbow1_joint','elbow2_joint','wrist_joint','right_finger_joint','left_finger_joint']
            point = JointTrajectoryPoint()
            point.positions = angles
            point.time_from_start = rospy.Duration(1)                   
            goal.trajectory.points.append(point)
            try:
	      self.jta.send_goal_and_wait(goal)
	    except TypeError as e:
	      print e
              

def main():
            arm = Joint('komodo_arm_controller')
            arm.move_joint([0.0,0.0,0.0,0.0,1.0,0.0,0.0])
            arm.move_joint([0.0,0.0,0.0,0.0,-1.0,0.0,0.0])

                        
if __name__ == '__main__':
      rospy.init_node('joint_position_tester')
      main()