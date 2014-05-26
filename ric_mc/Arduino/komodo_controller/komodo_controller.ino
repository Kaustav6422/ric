
//PINS

#define LED_PIN 13

#define BATTERY_MONITOR_PIN A0

#define ENC1_A_PIN 15 //right motor
#define ENC1_B_PIN 16 //right motor
#define ENC2_A_PIN 17 //left motor
#define ENC2_B_PIN 18 //left motor
/*
RIGHT MOTOR RED->M1A
RIGHT MOTOR BLACK->M1B
RIGHT ENCODER A -> ENC1_A_PIN = 15
RIGHT ENCODER B -> ENC1_B_PIN = 16

LEFT MOTOR RED->M2A
LEFT MOTOR BLACK->M2B
LEFT ENCODER A -> ENC2_A_PIN = 17
LEFT ENCODER B -> ENC2_B_PIN = 18
*/

//RX
#include <SabertoothSimplified.h>
SabertoothSimplified ST;
#define PUB_RX_INTERVAL 100
#include <Arduino.h>
#include <TeensyReceiver.h>

#define RX_DRIVE_MODE 1
#define RX_ARM_MODE 2
short DriveMode=1;
volatile uint16_t RX1=0,RX2=0,RX3=0,RX4=0,RX5=0,RX6=0;
unsigned long rx_t=0;

#define RX_DEAD_BAND 15

#define MIN_RX1 1195
#define MAX_RX1 1800
#define CENTER_RX1 1496
#define MIN_RX2 1241
#define MAX_RX2 1774
#define CENTER_RX2 1513

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
  kRx,
};

#define  SERIAL_PORT_SPEED  115200
#define  SERIAL_PORT Serial2

#define PUB_ENC_INTERVAL 50 //20 hz
unsigned long enc_t = 0, status_t = 0, pub_t;


CmdMessenger cmdMessenger = CmdMessenger(SERIAL_PORT);



//BATTERY MONITOR
#define STATUS_INTERVAL 1000 //1 hz  
#define VOLTAGE_DIVIDER_RATIO 11.48 //Vbat ----/\/\R1=47K/\/\----A0----/\/\R2=4.7K/\/\----AGND


//DRIVER
#include <Encoder.h>
#include <PID_v1.h>
//#include <EEPROM.h>

long left_enc = 0, right_enc = 0;
long pre_left_enc = 0, pre_right_enc = 0;
float left_spd = 0, right_spd = 0;
int drive_command=0,turn_command=0;
double Setpoint1, Input1, Output1;
double Setpoint2, Input2, Output2;
#define READ_ENCODERS_INTERVAL 50 //20 hz
int  CONTROL_INTERVAL = 1; //ms
double DT;
#define  WATCHDOG_INTERVAL 1500 //ms
#define  MAX_TICKS_PER_S 100000 //tics/sec
boolean wd_on = false;
float alpha = 0.5;
float kp = 0.03, ki = 0.15, kd = 0;
PID PID1(&Input1, &Output1, &Setpoint1, kp, ki, kd, DIRECT);
PID PID2(&Input2, &Output2, &Setpoint2, kp, ki, kd, DIRECT);

Encoder Enc1(ENC1_A_PIN, ENC1_B_PIN);
Encoder Enc2(ENC2_A_PIN, ENC2_B_PIN);
unsigned long wd_t = 0, control_t = 0,led_t=0;




void setup()
{

  pinMode(LED_PIN, OUTPUT);
  
Serial.begin(57600);

  SERIAL_PORT.begin(SERIAL_PORT_SPEED);
  
  initializeReceiver();

   // Adds newline to every command
  cmdMessenger.printLfCr(); 

  // Attach my application's user-defined callback methods
  attachCommandCallbacks();

  setup_driver();

 analogReadResolution(16);
// Setpoint1=2048;
}

void blink_led(int led_interval) {
 if (millis()-led_t>led_interval) {
  digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  led_t=millis();
 } 

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
    blink_led(1000);
  }
  
  
  if ((DriveMode==RX_ARM_MODE)&&(millis() - rx_t >= PUB_RX_INTERVAL))  {
    pub_rx();
    rx_t = millis();
    
  }

  if (millis() - status_t >= STATUS_INTERVAL)  {
    pub_status();
    status_t = millis();
    
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






