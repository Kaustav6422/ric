#ifndef _ROS_ric_robot_ric_status_h
#define _ROS_ric_robot_ric_status_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace ric_robot
{

  class ric_status : public ros::Msg
  {
    public:
      uint8_t faults;
      float battery1_voltage;
      float battery2_voltage;
      float battery3_voltage;

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      *(outbuffer + offset + 0) = (this->faults >> (8 * 0)) & 0xFF;
      offset += sizeof(this->faults);
      union {
        float real;
        uint32_t base;
      } u_battery1_voltage;
      u_battery1_voltage.real = this->battery1_voltage;
      *(outbuffer + offset + 0) = (u_battery1_voltage.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_battery1_voltage.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_battery1_voltage.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_battery1_voltage.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->battery1_voltage);
      union {
        float real;
        uint32_t base;
      } u_battery2_voltage;
      u_battery2_voltage.real = this->battery2_voltage;
      *(outbuffer + offset + 0) = (u_battery2_voltage.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_battery2_voltage.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_battery2_voltage.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_battery2_voltage.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->battery2_voltage);
      union {
        float real;
        uint32_t base;
      } u_battery3_voltage;
      u_battery3_voltage.real = this->battery3_voltage;
      *(outbuffer + offset + 0) = (u_battery3_voltage.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_battery3_voltage.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_battery3_voltage.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_battery3_voltage.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->battery3_voltage);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      this->faults =  ((uint8_t) (*(inbuffer + offset)));
      offset += sizeof(this->faults);
      union {
        float real;
        uint32_t base;
      } u_battery1_voltage;
      u_battery1_voltage.base = 0;
      u_battery1_voltage.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_battery1_voltage.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_battery1_voltage.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_battery1_voltage.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->battery1_voltage = u_battery1_voltage.real;
      offset += sizeof(this->battery1_voltage);
      union {
        float real;
        uint32_t base;
      } u_battery2_voltage;
      u_battery2_voltage.base = 0;
      u_battery2_voltage.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_battery2_voltage.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_battery2_voltage.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_battery2_voltage.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->battery2_voltage = u_battery2_voltage.real;
      offset += sizeof(this->battery2_voltage);
      union {
        float real;
        uint32_t base;
      } u_battery3_voltage;
      u_battery3_voltage.base = 0;
      u_battery3_voltage.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_battery3_voltage.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_battery3_voltage.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_battery3_voltage.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->battery3_voltage = u_battery3_voltage.real;
      offset += sizeof(this->battery3_voltage);
     return offset;
    }

    const char * getType(){ return "ric_robot/ric_status"; };
    const char * getMD5(){ return "94718088ad2766e13cb29c6d268fcfbd"; };

  };

}
#endif