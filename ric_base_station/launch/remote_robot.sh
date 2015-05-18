#!/usr/bin/expect -f
set robot_ip [lindex $argv 0]
set pc_ip [lindex $argv 1]
spawn ssh lizi@$robot_ip -o ServerAliveInterval=30
expect "password:"
send "a\r"
expect "lizi@"
send "echo '#!/bin/sh' > ~/catkin_ws/src/ric/ric_base_station/config/remote_env.sh\r"
send "echo 'export ROS_HOSTNAME=\"$robot_ip\"' >> ~/catkin_ws/src/ric/ric_base_station/config/remote_env.sh\r"
send "echo 'export ROS_MASTER_URI=\"http://localhost:11311\"' >> ~/catkin_ws/src/ric/ric_base_station/config/remote_env.sh\r"
send "echo '. ~/catkin_ws/devel/setup.sh' >> ~/catkin_ws/src/ric/ric_base_station/config/remote_env.sh\r"
send "echo 'exec \"\$@\"' >> ~/catkin_ws/src/ric/ric_base_station/config/remote_env.sh\r"

send "roscore\r"
expect "started core service"
puts "Launching remote robot..."
system "~/catkin_ws/src/ric/ric_base_station/launch/base_station.sh $robot_ip $pc_ip"
#interact
while {true } {
#	puts ".\n";
	sleep 5
}

