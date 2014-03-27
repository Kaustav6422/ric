

//PINS
#define BATTERY_MONITOR_PIN A11


#define ENC1_A_PIN 30
#define ENC1_B_PIN 31
#define ENC2_A_PIN 32
#define ENC2_B_PIN 33
/*
LEFT MOTOR RED->M2B
LEFT MOTOR BLACK->M2A
LEFT ENCODER A -> ENC2_A_PIN = 32
LEFT ENCODER B -> ENC2_B_PIN = 33

RIGHT MOTOR RED->M1B
RIGHT MOTOR BLACK->M1A
RIGHT ENCODER A -> ENC1_A_PIN = 30
RIGHT ENCODER B -> ENC1_B_PIN = 31

*/
#include <CmdMessenger.h>  // CmdMessenger
// In order to receive, attach a callback function to these events
enum
{
  // Commands
  kCommand,
  kStatus,
  kEncoders,
  kReset, 
  kSetParameters,
  kGetParameters,
  kGetParametersAck,
};

#define  SERIAL_PORT_SPEED  115200
#define  SERIAL_PORT Serial2
#define PUB_ENC_INTERVAL 100 //10 hz
unsigned long enc_t = 0, status_t = 0, pub_t;


CmdMessenger cmdMessenger = CmdMessenger(SERIAL_PORT);



//BATTERY MONITOR
#define STATUS_INTERVAL 1000 //1 hz  
#define VOLTAGE_DIVIDER_RATIO 6.67


//DRIVER
#include <Encoder.h>
#include <PID_v1.h>


long left_enc = 0, right_enc = 0;
long pre_left_enc = 0, pre_right_enc = 0;
float left_spd = 0, right_spd = 0;

double Setpoint1, Input1, Output1;
double Setpoint2, Input2, Output2;
#define READ_ENCODERS_INTERVAL 50 //200 hz
int  CONTROL_INTERVAL = 1; //ms
double DT;
#define  WATCHDOG_INTERVAL 1500 //ms
#define  MAX_TICKS_PER_S 100000 //tics/sec
boolean wd_on = false;
float alpha = 0.5;
float kp = 0.001, ki = 0.01, kd = 0;
PID PID1(&Input1, &Output1, &Setpoint1, kp, ki, kd, DIRECT);
PID PID2(&Input2, &Output2, &Setpoint2, kp, ki, kd, DIRECT);

Encoder Enc1(ENC1_A_PIN, ENC1_B_PIN);
Encoder Enc2(ENC2_A_PIN, ENC2_B_PIN);
unsigned long wd_t = 0, control_t = 0;




void setup()
{

  pinMode(13, OUTPUT);
  SERIAL_PORT.begin(SERIAL_PORT_SPEED);
 //Serial.begin(115200); 
   // Adds newline to every command
  cmdMessenger.printLfCr(); 

  // Attach my application's user-defined callback methods
  attachCommandCallbacks();

  setup_driver();

}



void attachCommandCallbacks()
{
  // Attach callback methods
//  cmdMessenger.attach(OnUnknownCommand);
  cmdMessenger.attach(kCommand, OnCommand);
  cmdMessenger.attach(kSetParameters, OnSetParameters);
    cmdMessenger.attach(kGetParameters, OnGetParameters);
   cmdMessenger.attach(kReset, OnReset);
}


void loop()
{

  cmdMessenger.feedinSerialData();
  control_loop();


  if (millis() - wd_t >= WATCHDOG_INTERVAL)  {
    if (!wd_on) {
      stop_motors();
      wd_on = true;
    }
  }


  if (millis() - status_t >= STATUS_INTERVAL)  {
    pub_status();
    status_t = millis();
    digitalWrite(13, !digitalRead(13));
  }


  if (millis() - enc_t >= READ_ENCODERS_INTERVAL)  {
    read_encoders();
    enc_t = millis();
  }

  if (millis() - pub_t >= PUB_ENC_INTERVAL)  {
    pub_enc();
    pub_t = millis();
  }


}






