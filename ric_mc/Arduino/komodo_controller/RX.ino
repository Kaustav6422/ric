void ReadRxCommands() {
  // read data into variables
  cli(); // disable interrupts
  RX1=RX[0];
  RX2=RX[1];
  RX3=RX[2];
  RX4=RX[3];
  RX5=RX[4];
  RX6=RX[5];
  sei(); // enable interrupts

  if ((RX1<CENTER_RX1+RX_DEAD_BAND)&&(RX1>CENTER_RX1-RX_DEAD_BAND)) RX1=CENTER_RX1;
  else if (RX1>CENTER_RX1) RX1=RX1-RX_DEAD_BAND;
  else if (RX1<CENTER_RX1) RX1=RX1+RX_DEAD_BAND;

  if ((RX2<CENTER_RX2+RX_DEAD_BAND)&&(RX2>CENTER_RX2-RX_DEAD_BAND)) RX2=CENTER_RX2;
  else if (RX2>CENTER_RX2) RX2=RX2-RX_DEAD_BAND;
  else if (RX2<CENTER_RX2) RX2=RX2+RX_DEAD_BAND;
}

boolean isRxConnected() {
  return !failsafeEnabled;

}

void CommandsFromRX() {
  drive_command=0;
  turn_command=0;

  if (RX2>CENTER_RX2) drive_command=map(RX2,CENTER_RX2,MAX_RX2-RX_DEAD_BAND,0,127);
  else if (RX2<CENTER_RX2) drive_command=map(RX2,MIN_RX2+RX_DEAD_BAND,CENTER_RX2,-127,0);
  if (RX1>CENTER_RX1) turn_command=map(RX1,CENTER_RX1,MAX_RX1-RX_DEAD_BAND,0,127);
  else if (RX1<CENTER_RX1) turn_command=map(RX1,MIN_RX1+RX_DEAD_BAND,CENTER_RX1,-127,0);

  if (turn_command>127) turn_command=127;
  else if (turn_command<-127) turn_command=-127;

  if (drive_command>127) drive_command=127;
  else if (drive_command<-127) drive_command=-127;

}




