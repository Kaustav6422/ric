

void home_up() {

  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 200ms, assume it's a bounce and ignore
  if (interrupt_time - last_interrupt_time > 1000)
  {
    set_elevator::Request req;
    set_elevator::Response res;
    req.pos = 0.31;
    elev_set_client.call(req, res);
  }
  last_interrupt_time = interrupt_time;


}
void home_down() {
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 200ms, assume it's a bounce and ignore
  if (interrupt_time - last_interrupt_time > 1000)
  {
    set_elevator::Request req;
    set_elevator::Response res;
    req.pos = -0.01;
    elev_set_client.call(req, res);
  }
  last_interrupt_time = interrupt_time;
}

void setup_homing() {

  int have_elevator[1]={ 0  };

  if (!nh.getParam("have_elevator_int", have_elevator)) {
    nh.logwarn("No have_elevator parameter found, assuming no elevator");
  }
  else{
    if ( have_elevator[0]==1) {
      nh.loginfo("Seting up elevator home switches...");
      pinMode(HOME_UP_PIN, INPUT_PULLUP); 
      pinMode(HOME_DOWN_PIN, INPUT_PULLUP); 
      attachInterrupt(HOME_UP_PIN,home_up, FALLING);
      attachInterrupt(HOME_DOWN_PIN,home_down, FALLING);
      nh.serviceClient(elev_set_client);
    }
    else {
      nh.loginfo("No arm elevator, ignoring elevator home switches");
      
    }
  }
}



