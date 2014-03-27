

void setup_driver() {

  float pid_constatns[5];
  if (!nh.getParam("pid_constants", pid_constatns, 5)) {
    nh.loginfo("No PID parameters found, using defaults.");
  }
  else {
    nh.loginfo("PID parameters found, sending to controller...");
    cmdMessenger.sendCmdStart(kSetParameters);
    cmdMessenger.sendCmdArg(pid_constatns[0],5);
    cmdMessenger.sendCmdArg(pid_constatns[1],5);
    cmdMessenger.sendCmdArg(pid_constatns[2],5);
    cmdMessenger.sendCmdArg(pid_constatns[3],5);
    cmdMessenger.sendCmdArg((int)pid_constatns[4]);
    cmdMessenger.sendCmdEnd();

  }

  stop_motors();
unsigned long temp_t=millis();

while (millis()-temp_t<100) {
  cmdMessenger.feedinSerialData();
}
got_parameters=false;
cmdMessenger.sendCmd(kGetParameters, true);

while (!got_parameters) cmdMessenger.feedinSerialData();

}

void OnGetParametersAck() {
  got_parameters=true;
  nh.loginfo("Reading parameters from controller...");
  float kp = cmdMessenger.readFloatArg();
  float ki = cmdMessenger.readFloatArg();
  float kd = cmdMessenger.readFloatArg();
  float alpha = cmdMessenger.readFloatArg();
  int cdt = cmdMessenger.readIntArg();
  
  char log_msg[30];

  sprintf(log_msg, "    kp*10000 = %d", (int)(kp * 10000));
  nh.loginfo(log_msg);


  sprintf(log_msg, "    ki*10000 = %d", (int)(ki * 10000));
  nh.loginfo(log_msg);


  sprintf(log_msg, "    kd*10000 = %d", (int)(kd * 10000));
  nh.loginfo(log_msg);


  sprintf(log_msg, "    alpha*10000 = %d", (int)(alpha * 10000));
  nh.loginfo(log_msg);

  sprintf(log_msg, "    Control loop dt = %d", cdt);
  nh.loginfo(log_msg);
}


void OnEncoders() {
  left_enc = cmdMessenger.readIntArg();
  right_enc = cmdMessenger.readIntArg();
}

void OnStatus() {
  status_bits = cmdMessenger.readIntArg();
  controller_bat_v = cmdMessenger.readFloatArg();
}


void read_status() {


  int gps_fix_bit = !gps.location.isValid();
  int imu_bit = (int)imu_fault;
  status_msg.faults = 8 * imu_bit + 4 * gps_fix_bit + status_bits;
  status_msg.battery1_voltage = (float)analogRead(BATTERY_MONITOR_PIN) * 3.3 / 4096 * VOLTAGE_DIVIDER_RATIO;
  status_msg.battery2_voltage = controller_bat_v;
  p_status.publish(&status_msg);

}



void reset_encCb(const Empty::Request & req, Empty::Response & res) {
 cmdMessenger.sendCmd (kReset, true);
 
  nh.loginfo("Reset encoders");


}

void commandCb( const ric_robot::ric_command& msg) {

  cmdMessenger.sendCmdStart(kCommand);
  cmdMessenger.sendCmdArg(msg.left_wheel);
  cmdMessenger.sendCmdArg(msg.right_wheel);
  cmdMessenger.sendCmdEnd();

}

void stop_motors() {

  cmdMessenger.sendCmdStart(kCommand);
  cmdMessenger.sendCmdArg(0.0);
  cmdMessenger.sendCmdArg(0.0);
  cmdMessenger.sendCmdEnd();
}


