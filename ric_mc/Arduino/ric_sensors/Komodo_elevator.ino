#ifdef HAVE_ELEVATOR
int pre_lh=LOW;
unsigned long lh_t=0;
boolean lh_stat=false;
//int lh_init=false;

int pre_uh=LOW;
unsigned long uh_t=0;
boolean uh_stat=false;



void check_lower_home() {
  int lh=digitalRead(HOME_DOWN_PIN);
  if ((lh==HIGH)&&(pre_lh==LOW)) {
    lh_t=millis();
    nh.loginfo("low to high");
  }
  else if((lh==HIGH)&&(pre_lh==HIGH)&&(!lh_stat)&&(millis()-lh_t>500)) {
    if (millis()-lh_t>500) {
      nh.loginfo("Lower home switch activated");
      set_elevator::Request req;
      set_elevator::Response res;
      req.pos = -0.01;
      elev_set_client.call(req, res);
      lh_stat=true;
    }
  }
  else if((lh==LOW)&&(pre_lh==HIGH)&&(lh_stat)) {
    lh_stat=false;
    //nh.loginfo("Lower home switch released");
  }

  pre_lh=lh;
}

void check_upper_home() {
  int uh=digitalRead(HOME_UP_PIN);
  if ((uh==HIGH)&&(pre_uh==LOW)) {
    uh_t=millis();

  }
  else if((uh==HIGH)&&(pre_uh==HIGH)&&(!uh_stat)&&(millis()-uh_t>500)) {
    if (millis()-uh_t>500) {
      nh.loginfo("Upper home switch activated");
      set_elevator::Request req;
      set_elevator::Response res;
      req.pos = 0.407;
      elev_set_client.call(req, res);
      uh_stat=true;
    }
  }
  else if((uh==LOW)&&(pre_uh==HIGH)&&(uh_stat)) {
    uh_stat=false;
    //nh.loginfo("Upper home switch released");
  }

  pre_uh=uh;
}


void setup_homing() {

  nh.loginfo("Seting up elevator home switches...");
  pinMode(HOME_UP_PIN, INPUT_PULLUP); 
  pinMode(HOME_DOWN_PIN, INPUT_PULLUP); 

  pre_lh=LOW;
  lh_t=millis();
  lh_stat=false;

  pre_uh=LOW;
  uh_t=millis();

}

#endif
/*
void setup_homing() {
 
 int have_elevator[1]={ 
 0        };
 
 if (!nh.getParam("have_elevator_int", have_elevator)) {
 nh.logwarn("No have_elevator parameter found, assuming no elevator");
 }
 else{
 if ( have_elevator[0]==1) {
 nh.loginfo("Seting up elevator home switches...");
 pinMode(HOME_UP_PIN, INPUT_PULLUP); 
 pinMode(HOME_DOWN_PIN, INPUT_PULLUP); 
 // attachInterrupt(HOME_UP_PIN,home_up, RISING); //FALLING
 // attachInterrupt(HOME_DOWN_PIN,home_down, RISING); //FALLING
 //nh.serviceClient(elev_set_client);
 pre_lh=LOW;
 lh_t=millis();
 lh_stat=false;
 
 pre_uh=LOW;
 uh_t=millis();
 uh_stat=false;
 }
 else {
 nh.loginfo("No arm elevator, ignoring elevator home switches");
 }
 }
 }
 
 
 
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
 nh.loginfo("Upper home switch");
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
 nh.loginfo("Lower home switch");
 }
 last_interrupt_time = interrupt_time;
 }
 */






