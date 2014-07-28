#!/bin/bash
source ../../../../devel/setup.bash
echo -e "\e[34mSetting usb rules...\e[0m"
cp ric_usb.rules /etc/udev/rules.d
cp 49-teensy.rules /etc/udev/rules.d/49-teensy.rules
cp uvcvideo.conf /etc/modprobe.d

echo -e "\e[34mAdding user: [$SUDO_USER] to dialout group (serial premmisions)\e[0m"
usermod -a -G dialout $SUDO_USER


echo -e "\e[34mInstalling rosserial...\e[0m"
roscd ric_robot
cd ..
cd ..
git clone https://github.com/ros-drivers/rosserial.git
cp -f ric/ric_mc/ArduinoHardware.h rosserial/rosserial_arduino/src/ros_lib

echo -e "\e[32mWould you like to install usb_cam package (front webcam support) (y/n)?\e[0m"
read
if [[ $REPLY =~ ^[Yy]$ ]]
then
    apt-get install ros-hydro-usb-cam
fi

echo -e "\e[32mWould you like to install openni2 packages (Asus Xtion PRO LIVE support) (y/n)?\e[0m"
read
if [[ $REPLY =~ ^[Yy]$ ]]
then
    apt-get install ros-hydro-openni2-*
fi

echo -e "\e[32mWould you like to install openssh packages (remote machine control support) (y/n)?\e[0m"
read
if [[ $REPLY =~ ^[Yy]$ ]]
then
    apt-get install openssh-client openssh-server
fi

echo -e "\e[32mWould you like to install hokuyo_node packages (Hokuyo laser scanner support) (y/n)?\e[0m"
read
if [[ $REPLY =~ ^[Yy]$ ]]
then
    apt-get install ros-hydro-hokuyo-node
fi

echo -e "\e[32mWould you like to install ros-hydro-dynamixel-motor packages (Komodo arm support) (y/n)?\e[0m"
read
if [[ $REPLY =~ ^[Yy]$ ]]
then
    apt-get install ros-hydro-dynamixel-motor
fi

echo -e "\e[32mWould you like to install ros-hydro-joystick-drivers package (joystick support) (y/n)?\e[0m"
read
if [[ $REPLY =~ ^[Yy]$ ]]
then
    apt-get install ros-hydro-joystick-drivers
fi
