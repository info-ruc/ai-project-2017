#include "AFMotor.h"

//设置两个motor的接口和频率
AF_DCMotor motor_right(1,MOTOR12_1KHZ);
AF_DCMotor motor_left(4,MOTOR34_1KHZ);

//设置两个舵机接口
const int TrigPin = 9; 
const int EchoPin = 10; 

void setup() {
  //设置左右motor速度
  motor_left.setSpeed(0);
  motor_right.setSpeed(0);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
      char ch = Serial.read();
      if(ch == 'F'){
         //前进
         Serial.println("up");
         motor_left.setSpeed(210);
         motor_right.setSpeed(180);
         motor_left.run(BACKWARD);
         motor_right.run(BACKWARD);
      }else if(ch == 'B'){
         //后退
         Serial.println("back");
         motor_left.setSpeed(210);
         motor_right.setSpeed(180);
         motor_left.run(FORWARD);
         motor_right.run(FORWARD);
      }else if(ch == 'L'){
         //左转
         Serial.println("left");
         motor_left.setSpeed(0);
         motor_right.setSpeed(180);
         motor_left.run(BACKWARD);
         motor_right.run(BACKWARD);
      }else if(ch == 'R'){
        //右转
         Serial.println("right");
         motor_left.setSpeed(210);
         motor_right.setSpeed(0);
         motor_left.run(BACKWARD);
         motor_right.run(BACKWARD);
      }else if(ch=='S'){
        //停车
         Serial.println("stop");
         motor_left.setSpeed(0);
         motor_right.setSpeed(0);
         motor_left.run(BACKWARD);
         motor_right.run(BACKWARD);
      }else{
        //其他编码
        Serial.println(ch);
      }
    }
}
