#include <AFMotor.h>
#include <SoftwareSerial.h>

SoftwareSerial BT(0,1);

AF_DCMotor Rback_motor(4);    //右后轮  
AF_DCMotor Lback_motor(2);    //左后轮
float RLRatio = 1.32 ; 

int maxSpeed = 80;//最大速度
char getstr = '1'  ;//串口数据
int IntervalTime;//测距时间
int trig = 9;//sero1保留端口  输出端口
int echo = 10;//sero2保留端口  输入端口
int control=1;//0:人工控制;1:自动控制

void setup() {
  // put your setup code here, to run once:
  BT.begin(9600);    
  Rback_motor.setSpeed(0);
  Rback_motor.run(RELEASE);
  Lback_motor.setSpeed(0);
  Lback_motor.run(RELEASE);
  delay(2000);

  //超声波测距
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
}

void driver() {
  if ((getstr == '<')&&(RLRatio>0.1)) 
  {
    RLRatio -= 0.01;
    //BT.println(RLRatio);
  }  
  if (getstr == '>') 
  {
    RLRatio += 0.01;
    //BT.println(RLRatio);
  }  
  if (getstr == '5') 
  {
    //BT.println("stopcar");
    stopcar();
    control=0;
  }
  if (getstr == '1') 
  {
    //BT.println("forward");
    forward();
    control=0;
  }
  if (getstr == '2') {
    //BT.println("backward");
    backward();
    control=0;
  }
  if (getstr == '3') {
    //BT.println("right");
    right();
    control=0;
  }
  if (getstr == '4') {
    //BT.println("left");
    left();
    control=0;
  }
  if (getstr=='6')
  {
    control=1;
    //BT.println("Auto Control On");
  }
  if(getstr=='7')
  {
    control=0;
    //BT.println("Auto Control Off");
  }
  
}

void forward() {
  Rback_motor.run(FORWARD);
  Lback_motor.run(FORWARD);
  Rback_motor.setSpeed(maxSpeed*RLRatio);
  Lback_motor.setSpeed(maxSpeed);
}

void backward() {
  Rback_motor.run(BACKWARD);
  Lback_motor.run(BACKWARD);
  Rback_motor.setSpeed(maxSpeed*RLRatio);
  Lback_motor.setSpeed(maxSpeed);
}

void stopcar() {
  Rback_motor.setSpeed(0);
  Lback_motor.setSpeed(0);
  Rback_motor.run(RELEASE);
  Lback_motor.run(RELEASE);
}
void left(){
  Rback_motor.run(FORWARD);
  
  Rback_motor.setSpeed(80*RLRatio);
  Lback_motor.setSpeed(0);
  Lback_motor.run(RELEASE);
}
void right(){
  
  Lback_motor.run(FORWARD);
  Rback_motor.setSpeed(20);
  Lback_motor.setSpeed(80);
  Rback_motor.run(BACKWARD);
}

void randomright(){
  Rback_motor.run(BACKWARD);
  Lback_motor.run(FORWARD);
  Rback_motor.setSpeed(maxSpeed*RLRatio);
  Lback_motor.setSpeed(maxSpeed);
  long n = random(50,1000);//随机转向 0.05 - 1秒
  delay(n);
  Rback_motor.setSpeed(0);
  Lback_motor.setSpeed(0);
}

float getdistance() {
  digitalWrite(trig, 1);
  delayMicroseconds(15);
  digitalWrite(trig, 0);
  IntervalTime = pulseIn(echo, HIGH);
  return IntervalTime / 58.00;
}

void ultrasonicCar(float s) {
  if ((s < 40)&&(s>0)){//40cm以内
    randomright();
  }
  else{
    forward();
  }
}

void ultrasonicCar() {
  float s = 0;
  s = getdistance();
  ultrasonicCar(s);
}

void loop() {
  
  if(BT.available()){
    getstr = BT.read();
    BT.println(getstr);
  }
  
  driver();
  if(control==1)
  {
    ultrasonicCar();
  }
}