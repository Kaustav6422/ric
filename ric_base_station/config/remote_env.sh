#!/bin/sh
export ROS_HOSTNAME="10.0.0.6"
export ROS_MASTER_URI="http://localhost:11311"
. ~/catkin_ws/devel/setup.sh
exec "$@"
