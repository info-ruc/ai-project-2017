#include "AFMotor.h"

//设置两个motor的接口和频率
AF_DCMotor motor_left(1,MOTOR12_1KHZ);
AF_DCMotor motor_right(4,MOTOR34_1KHZ);

//设置两个舵机接口
const int TrigPin = 9; 
const int EchoPin = 10; 

//距离变量
float cm; 

void setup() 
{ 
  Serial.begin(9600); 
  pinMode(TrigPin, OUTPUT); 
  pinMode(EchoPin, INPUT); 
  //设置左右motor速度
  motor_left.setSpeed(180);
  motor_right.setSpeed(210);
} 

void loop() 
{
  digitalWrite(TrigPin, LOW); //低高低电平发一个短时间脉冲去TrigPin 
  delayMicroseconds(2); 
  digitalWrite(TrigPin, HIGH); 
  delayMicroseconds(10); 
  digitalWrite(TrigPin, LOW); 

  cm = pulseIn(EchoPin, HIGH) / 58.0; //将回波时间换算成cm 
  cm = (int(cm * 100.0)) / 100.0; //保留两位小数 

  if(cm < 15){
    motor_left.setSpeed(180);
    motor_left.run(FORWARD);
    motor_right.run(FORWARD);
    delay(300);
  }
  else if(cm < 40){
    motor_left.setSpeed(0);
    motor_left.run(BACKWARD);
    motor_right.run(BACKWARD);
    delay(300);
  }
  else{
    motor_left.setSpeed(180);
    motor_left.run(BACKWARD);
    motor_right.run(BACKWARD);
  }
  delay(100); 
}
