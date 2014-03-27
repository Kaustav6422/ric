

//SUBSCRIBERS
#define COMMAND_TOPIC "command"
#define PAN_TILT_TOPIC "pan_tilt"
//PUBLISHER
#define RAW_TOPIC "ric_raw"
#define GPS_TOPIC "raw_gps"
#define STATUS_TOPIC "status"
//SERVICES
#define  RESET_ENCODERS_SRV "reset_encoders"
#define IMU_CALIB_SRV "imu_calib"




//PINS
#define BATTERY_MONITOR_PIN A11

#define PAN_SERVO_PIN 2
#define TILT_SERVO_PIN 3


#define LEFT_URF_PIN A8
#define REAR_URF_PIN A9
#define RIGHT_URF_PIN A10
#define URF_TX_PIN 5

/*

GPS PIN 1 -> GND
GPS PIN 2 -> VCC
GPS PIN 3 -> RX2 = 17
GPS PIN 4 -> TX2 = 16

*/
//CONTROLLER


#define  CONTROLLER_PORT_SPEED  115200
#define CONTROLLER_PORT Serial3
#include <CmdMessenger.h>  // CmdMessenger



CmdMessenger cmdMessenger = CmdMessenger(CONTROLLER_PORT);

int status_bits = 0;
float controller_bat_v = 0;
int left_enc = 0, right_enc = 0;
bool got_parameters=false;
enum
{
  kCommand,
  kStatus,
  kEncoders,
  kReset, 
  kSetParameters,
  kGetParameters,
  kGetParametersAck,
};


//ROS

#include <ros.h>
#include <ric_robot/ric_raw.h>
#include <ric_robot/ric_gps.h>
#include <ric_robot/ric_command.h>
#include <ric_robot/ric_pan_tilt.h>
#include <ric_robot/ric_status.h>

#include <ric_robot/imu_calib.h>
#include <std_srvs/Empty.h>

#define  ROS_PORT_SPEED  57600
#define  ROS_PORT Serial
#define PUB_RAW_INTERVAL 100 //10 hz
unsigned long urf_t = 0, enc_t = 0, status_t = 0, pub_t;

ros::NodeHandle nh;
using std_srvs::Empty;
using ric_robot::imu_calib;

//PROTOTYPES
void reset_encCb(const Empty::Request & req, Empty::Response & res);
void imu_calibCb(const imu_calib::Request & req, imu_calib::Response & res);
void commandCb( const ric_robot::ric_command& msg);
void pantiltCb( const ric_robot::ric_pan_tilt& msg);


ros::ServiceServer<imu_calib::Request, imu_calib::Response> imu_calib_server(IMU_CALIB_SRV, &imu_calibCb);
ros::ServiceServer<Empty::Request, Empty::Response> reset_enc_server(RESET_ENCODERS_SRV, &reset_encCb);

ros::Subscriber<ric_robot::ric_command> command_sub(COMMAND_TOPIC, &commandCb );

ros::Subscriber<ric_robot::ric_pan_tilt> pan_tilt_sub(PAN_TILT_TOPIC, &pantiltCb );


ric_robot::ric_gps gps_msg;
ric_robot::ric_raw raw_msg;
ric_robot::ric_status status_msg;


ros::Publisher p_raw(RAW_TOPIC, &raw_msg);
ros::Publisher p_gps(GPS_TOPIC, &gps_msg);
ros::Publisher p_status(STATUS_TOPIC, &status_msg);


//PAN TILT
#include <Servo.h>
#define MAX_PAN 35
#define MIN_PAN -35
#define MAX_TILT 30
#define MIN_TILT -30
#define PAN_CENTER 94
#define TILT_CENTER 94

Servo pan_servo;
Servo tilt_servo;
unsigned long pan_tilt_t = 0;
bool pan_tilt_moving = true;
#define PAN_TILT_MOVE_TIME 1000


//GPS
#include <TinyGPS++.h>
TinyGPSPlus gps;
#define  GPS_PORT_SPEED  9600
#define GPS_SERIAL_PORT Serial2

//IMU

#include <Wire.h>
#include "I2Cdev.h"
#include "MPU9150Lib.h"
#include "CalLib.h"
#include "DueFlash.h"
#include <dmpKey.h>
#include <dmpmap.h>
#include <inv_mpu.h>
#include <inv_mpu_dmp_motion_driver.h>
#include <Arduino.h>


float qx = 0, qy = 0, qz = 1, qw = 0;
unsigned long imu_t = 0;
unsigned long CHECK_IMU_INTERVAL;
boolean imu_fault = 0;
//  DEVICE_TO_USE selects whether the IMU at address 0x68 (default) or 0x69 is used
//    0 = use the device at 0x68
//    1 = use the device at ox69
#define  DEVICE_TO_USE    0
MPU9150Lib dueMPU; // the MPU object
//  MPU_UPDATE_RATE defines the rate (in Hz) at which the MPU updates the sensor data and DMP output
#define MPU_UPDATE_RATE  (10)
//  MAG_UPDATE_RATE defines the rate (in Hz) at which the MPU updates the magnetometer data
//  MAG_UPDATE_RATE should be less than or equal to the MPU_UPDATE_RATE
#define MAG_UPDATE_RATE  (10)
//  MPU_MAG_MIX defines the influence that the magnetometer has on the yaw output.
//  The magnetometer itself is quite noisy so some mixing with the gyro yaw can help
//  significantly. Some example values are defined below:
#define  MPU_MAG_MIX_GYRO_ONLY          0                   // just use gyro yaw
#define  MPU_MAG_MIX_MAG_ONLY           1                   // just use magnetometer and no gyro yaw
#define  MPU_MAG_MIX_GYRO_AND_MAG       10                  // a good mix value 
#define  MPU_MAG_MIX_GYRO_AND_SOME_MAG  50                  // mainly gyros with a bit of mag correction 
//  MPU_LPF_RATE is the low pas filter rate and can be between 5 and 188Hz
#define MPU_LPF_RATE   40

long lastPollTime; // last time the MPU-9150 was checked
long pollInterval; // gap between polls to avoid thrashing the I2C bus
char temp_msg[30];

int loopState; // what code to run in the loop

#define LOOPSTATE_NORMAL 0 // normal execution
#define LOOPSTATE_MAGCAL 1 // mag calibration
#define LOOPSTATE_ACCELCAL 2 // accel calibration

static CALLIB_DATA calData; // the calibration data

void magCalStart(void);
void magCalLoop(void);
void accelCalStart(void);
void accelCalLoop(void);




//BATTERY MONITOR
#define STATUS_INTERVAL 1000 //1 hz  
#define VOLTAGE_DIVIDER_RATIO 6.67



//URF
#define URF_INTERVAL 100 //10 hz
#define sample_size 5
#include "FastRunningMedian.h"
FastRunningMedian<unsigned int, sample_size, 0> Left_URF_Median;
FastRunningMedian<unsigned int, sample_size, 0> Right_URF_Median;
FastRunningMedian<unsigned int, sample_size, 0> Rear_URF_Median;



void setup()
{

  pinMode(13, OUTPUT);
  ROS_PORT.begin(ROS_PORT_SPEED);

  CONTROLLER_PORT.begin(CONTROLLER_PORT_SPEED);
  // Adds newline to every command
  cmdMessenger.printLfCr();
  // Attach my application's user-defined callback methods
  attachCommandCallbacks();



  nh.initNode();

  nh.advertise(p_raw);
  nh.advertise(p_gps);
  nh.advertise(p_status);

  nh.advertiseService(reset_enc_server);
  nh.advertiseService(imu_calib_server);

  nh.subscribe(command_sub);
  nh.subscribe(pan_tilt_sub);

  while (!nh.connected()) {
    nh.spinOnce();
  }

  nh.loginfo("Starting up...");

  setup_driver();
  nh.loginfo("Driver ready");

  pan_tilt_setup();
  nh.loginfo("Pan Tilt ready");

  setup_imu();

  setup_urf();
  nh.loginfo("URF sensors ready");

  GPS_SERIAL_PORT.begin(GPS_PORT_SPEED);
  nh.loginfo("GPS ready");


}
void attachCommandCallbacks()
{
  // Attach callback methods
  //  cmdMessenger.attach(OnUnknownCommand);
  cmdMessenger.attach(kGetParametersAck, OnGetParametersAck);
  cmdMessenger.attach(kStatus, OnStatus);
  cmdMessenger.attach(kEncoders, OnEncoders);
}

void pub_raw() {

  raw_msg.qw = qw;
  raw_msg.qx = qx;
  raw_msg.qy = qy;
  raw_msg.qz = qz;

  raw_msg.left_ticks = -(long)left_enc;
  raw_msg.right_ticks = (long)right_enc;

  raw_msg.left_urf = (float)Left_URF_Median.getMedian() / 799.8124 ; //* 3.3 / 4095 *1.5515;
  raw_msg.rear_urf = (float)Rear_URF_Median.getMedian() / 799.8124 ; //* 3.3 / 4095 *1.5515;
  raw_msg.right_urf = (float)Right_URF_Median.getMedian() / 799.8124 ; //* 3.3 / 4095 *1.5515;

  p_raw.publish(&raw_msg);

}

void loop()
{

cmdMessenger.feedinSerialData();


  if (millis() - status_t >= STATUS_INTERVAL)  {
    read_status();
    status_t = millis();
    digitalWrite(13, !digitalRead(13));
  }



  if (millis() - pub_t >= PUB_RAW_INTERVAL)  {
    pub_raw();
    pub_t = millis();
  }


  if (millis() - urf_t >= URF_INTERVAL)  {

    read_urf();
    //  nh.spinOnce();
    urf_t = millis();
  }

  read_gps();

  if (!imu_fault) {
    if (millis() - imu_t <= CHECK_IMU_INTERVAL)  {
      read_imu();
    }
    else {
      imu_fault = true;
    }
  }

  pan_tilt_wd();

  nh.spinOnce();
}






