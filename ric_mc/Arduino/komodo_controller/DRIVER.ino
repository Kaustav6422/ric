
void setup_driver() {

  /* TODO: READ FROM FLASH
   float pid_constatns[5];
   if (!nh.getParam("pid_constants", pid_constatns, 5)) {
   nh.loginfo("No PID parameters found, using defaults.");
   }
   else {
   PID1.SetTunings(pid_constatns[0], pid_constatns[1], pid_constatns[2]);
   PID2.SetTunings(pid_constatns[0], pid_constatns[1], pid_constatns[2]);
   alpha = pid_constatns[3];
   CONTROL_INTERVAL = (int)pid_constatns[4];
   }
   */

  Setpoint1 = 0;
  Setpoint2 = 0;
  PID1.SetSampleTime(CONTROL_INTERVAL);
  PID2.SetSampleTime(CONTROL_INTERVAL);
  DT = (double)READ_ENCODERS_INTERVAL / 1000.0;
  PID1.SetMode(AUTOMATIC);
  PID2.SetMode(AUTOMATIC);
  PID1.SetOutputLimits(-127, 127);
  PID2.SetOutputLimits(-127, 127);

  SabertoothTXPinSerial.begin(38400);


  stop_motors();


}

void pub_enc() {
  cmdMessenger.sendCmdStart(kEncoders);
  cmdMessenger.sendCmdArg(left_enc);
  cmdMessenger.sendCmdArg(right_enc);
  cmdMessenger.sendCmdEnd();
}

void pub_status() {

  float battery_voltage = (float)analogRead(BATTERY_MONITOR_PIN) * 3.3 / 65535 * VOLTAGE_DIVIDER_RATIO;
 // Serial.println(battery_voltage);
  cmdMessenger.sendCmdStart(kStatus);
  cmdMessenger.sendCmdArg(isRxConnected());
  cmdMessenger.sendCmdArg(battery_voltage);
  cmdMessenger.sendCmdEnd();
}


void  read_encoders() {
  pre_left_enc = left_enc;
  pre_right_enc = right_enc;

  left_enc =-Enc2.read(); //left
  right_enc = Enc1.read(); //right

  left_spd = alpha * (double)(left_enc - pre_left_enc) / DT  + (1 - alpha) * (double)left_spd;
  right_spd = alpha * (double)(right_enc - pre_right_enc) / DT + (1 - alpha) * (double)right_spd;

  Input2 = left_spd;
  Input1 = right_spd;
 /* 
  Serial.print(right_enc);
     Serial.print("   ");
     Serial.println(left_enc);
*/
  RX_failSafe();
}

void control_loop() {

  if (isRxConnected()) {
    ReadRxCommands();

    CommandsFromRX();

    ST.turn(-turn_command);
    ST.drive(drive_command);
    /*
      Serial.print(RX1);
     Serial.print("   ");
     Serial.print(RX2);
     Serial.print("   ");
     Serial.print(RX3);
     Serial.print("   ");
     Serial.print(RX4);
     Serial.print("   ");
     Serial.print(RX5);
     Serial.print("   ");
     Serial.print(RX6);
     Serial.print("        ");
     Serial.print(drive_command);
     Serial.print("   ");
     Serial.println(turn_command);
*/
     
     blink_led(300);
  }
  
 /* else if (wd_on) {
    stop_motors();
    blink_led(1000);
    // Serial.println("wd on");
  }
  */
  else if ( (PID1.Compute()) && (PID2.Compute()) ) {
    ST.motor(1,-(int)Output1);
    ST.motor(2,-(int)Output2);
    /*
        Serial.print("Inputs: ");
         Serial.print((int)Input1);
     Serial.print("   ");
     Serial.print((int)Input2);
     
    Serial.print("    Outputs: ");
         Serial.print(-(int)Output1);
     Serial.print("   ");
     Serial.println(-(int)Output2);
     */
    blink_led(100);
  }

}



void OnReset() {
  bool temp = cmdMessenger.readBoolArg();
  Enc1.write(0);
  Enc2.write(0);

  left_enc = 0;
  right_enc = 0;
  left_spd = 0;
  right_spd = 0;


}

void OnGetParameters() {
  bool temp = cmdMessenger.readBoolArg();
  cmdMessenger.sendCmdStart(kGetParametersAck);
  cmdMessenger.sendCmdArg(kp,5);
  cmdMessenger.sendCmdArg(ki,5);
  cmdMessenger.sendCmdArg(kd,5);
  cmdMessenger.sendCmdArg(alpha,5);
  cmdMessenger.sendCmdArg(CONTROL_INTERVAL);
  cmdMessenger.sendCmdEnd();
/*
  Serial.println("Sent parameters");
   Serial.println(kp,5);
   Serial.println(ki,5);
   Serial.println(kd,5);
   Serial.println(alpha,5);
   Serial.println(CONTROL_INTERVAL);
 */  
}

void OnSetParameters() {
  kp = cmdMessenger.readFloatArg();
  ki = cmdMessenger.readFloatArg();
  kd = cmdMessenger.readFloatArg();
  alpha = cmdMessenger.readFloatArg();
  CONTROL_INTERVAL = cmdMessenger.readIntArg();

  PID1.SetTunings(kp, ki, kd);
  PID2.SetTunings(kp, ki, kd);

  PID1.SetSampleTime(CONTROL_INTERVAL);
  PID2.SetSampleTime(CONTROL_INTERVAL);
  
  
  /* Serial.println("Got parameters");
   Serial.println(kp,5);
   Serial.println(ki,5);
   Serial.println(kd,5);
   Serial.println(alpha,5);
   Serial.println(CONTROL_INTERVAL);
   */
}

void OnCommand() {
  if (wd_on) {
    wd_on = false;
    //  md.setTorque(true);
  }
  wd_t = millis();

  // Setpoint2 = -msg.left_wheel;
  // Setpoint1 = msg.right_wheel;
  Setpoint2 = cmdMessenger.readFloatArg(); //left
  Setpoint1 = cmdMessenger.readFloatArg(); //right

  if (Setpoint1 > MAX_TICKS_PER_S) Setpoint1 = MAX_TICKS_PER_S;
  else if (Setpoint1 < -MAX_TICKS_PER_S) Setpoint1 = -MAX_TICKS_PER_S;
  if (Setpoint2 > MAX_TICKS_PER_S) Setpoint2 = MAX_TICKS_PER_S;
  else if (Setpoint2 < -MAX_TICKS_PER_S) Setpoint2 = -MAX_TICKS_PER_S;

/*
   Serial.println("Got command");
   Serial.println(Setpoint2);
    Serial.println(Setpoint1);
*/
}

void stop_motors( ) {


  Setpoint1 = 0;
  Setpoint2 = 0;
  ST.stop();

}



