#!/bin/bash

echo -e "\e[34mStarting setup...\e[0m"
echo -e "\e[34mInstalling python-tk package...\e[0m"
apt-get -y install python-tk
echo -e "\e[34mFinish installing python-tk package...\e[0m"
echo -e "\e[34mInstalling idle package...\e[0m"
apt-get -y install idle
echo -e "\e[34mFinish installing idle package..\e[0m"
echo -e "\e[34mSetting usb rules..\e[0m"
cp ric_usb.rules /etc/udev/rules.d
echo -e "\e[34mRestarting rules..\e[0m"
/etc/init.d/udev reload
echo -e "\e[34mInstallation is complete..\e[0m"


