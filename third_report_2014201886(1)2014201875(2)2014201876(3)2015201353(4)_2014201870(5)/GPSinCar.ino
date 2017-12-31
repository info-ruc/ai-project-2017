#include <AFMotor.h>
#include <SoftwareSerial.h>
#define GPRMC_TERM "$GPRMC,"    //定义要解析的指令，因为这条指令包含定位和时间信息

SoftwareSerial gps(2,3);
SoftwareSerial BT(0,1);

char nmeaSentence[68];
String latitude;    //纬度
String longitude;   //经度
String lndSpeed;    //速度
String gpsTime;     //UTC时间，本初子午线经度0度的时间，和北京时间差8小时
String beiJingTime;   //北京时间

AF_DCMotor Rback_motor(4);    //右后轮  
AF_DCMotor Lback_motor(2);    //左后轮
float RLRatio = 1.32 ; 

int maxSpeed = 80;//最大速度
char getstr ;//串口数据
int IntervalTime;//测距时间
int trig = 9;//sero1保留端口  输出端口
int echo = 10;//sero2保留端口  输入端口
int control=1;//0:人工控制;1:自动控制

void setup() {
 // put your setup code here, to run once:
 BT.begin(9600);
 gps.begin(9600);
//  Serial.begin(9600);    
 Rback_motor.setSpeed(0);
 Rback_motor.run(RELEASE);
 Lback_motor.setSpeed(0);
 Lback_motor.run(RELEASE);
 delay(2000);

 //超声波测距
 pinMode(echo, INPUT);
 pinMode(trig, OUTPUT);

 stopcar();
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

 //gps module  adjust direction
 if(getstr == '9'){

   long n = random(1000,2000);
   if(n > 1500)
     randomright();
   else
     randomleft();
   forward();
   
   n = random(1000,2000);//向前试探 1 - 2秒
   delay(n); 
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
 Rback_motor.setSpeed(0);
 Lback_motor.setSpeed(50);
 Rback_motor.run(RELEASE);
}

void randomright(){
 Rback_motor.run(BACKWARD);
 Lback_motor.run(FORWARD);
 Rback_motor.setSpeed(50);
 Lback_motor.setSpeed(80);
 long n = random(500,1000);//随机转向 0.05 - 1秒
 delay(n);
 Rback_motor.setSpeed(0);
 Lback_motor.setSpeed(0);
}

void randomleft(){
 Rback_motor.run(BACKWARD);
 Lback_motor.run(FORWARD);
 Rback_motor.setSpeed(80*RLRatio);
 Lback_motor.setSpeed(50);
 long n = random(500,1000);//随机转向 0.05 - 1秒
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
String getBeiJingTime(String s)
{
 int hour = s.substring(0,2).toInt();
 int minute = s.substring(2,4).toInt();
 int second = s.substring(4,6).toInt();

 hour += 8;

 if(hour > 24)
   hour -= 24;
 s = String(hour) + String(minute) + String(second);
 return s;
}

//Parse GPRMC NMEA sentence data from String
//String must be GPRMC or no data will be parsed
//Return Latitude
String parseGprmcLat(String s)
{
 int pLoc = 0; //paramater location pointer
 int lEndLoc = 0; //lat parameter end location
 int dEndLoc = 0; //direction parameter end location
 String lat;
 /*make sure that we are parsing the GPRMC string. 
  Found that setting s.substring(0,5) == "GPRMC" caused a FALSE.
  There seemed to be a 0x0D and 0x00 character at the end. */
 if(s.substring(0,4) == "GPRM")
 {
   //Serial.println(s);
   for(int i = 0; i < 5; i++)
   {
     if(i < 3) 
     {
       pLoc = s.indexOf(',', pLoc+1);
       /*Serial.print("i < 3, pLoc: ");
        Serial.print(pLoc);
        Serial.print(", ");
        Serial.println(i);*/
     }
     if(i == 3)
     {
       lEndLoc = s.indexOf(',', pLoc+1);
       lat = s.substring(pLoc+1, lEndLoc);
       /*Serial.print("i = 3, pLoc: ");
        Serial.println(pLoc);
        Serial.print("lEndLoc: ");
        Serial.println(lEndLoc);*/
     }
     else
     {
       dEndLoc = s.indexOf(',', lEndLoc+1);
       lat = lat + " " + s.substring(lEndLoc+1, dEndLoc);
       /*Serial.print("i = 4, lEndLoc: ");
        Serial.println(lEndLoc);
        Serial.print("dEndLoc: ");
        Serial.println(dEndLoc);*/
     }
   }
   return lat; 
 }
 //}
 //}
}

//Parse GPRMC NMEA sentence data from String
//String must be GPRMC or no data will be parsed
//Return Longitude
String parseGprmcLon(String s)
{
 int pLoc = 0; //paramater location pointer
 int lEndLoc = 0; //lat parameter end location
 int dEndLoc = 0; //direction parameter end location
 String lon;

 /*make sure that we are parsing the GPRMC string. 
  Found that setting s.substring(0,5) == "GPRMC" caused a FALSE.
  There seemed to be a 0x0D and 0x00 character at the end. */
 if(s.substring(0,4) == "GPRM")
 {
   //Serial.println(s);
   for(int i = 0; i < 7; i++)
   {
     if(i < 5) 
     {
       pLoc = s.indexOf(',', pLoc+1);
       /*Serial.print("i < 3, pLoc: ");
        Serial.print(pLoc);
        Serial.print(", ");
        Serial.println(i);*/
     }
     if(i == 5)
     {
       lEndLoc = s.indexOf(',', pLoc+1);
       lon = s.substring(pLoc+1, lEndLoc);
       /*Serial.print("i = 3, pLoc: ");
        Serial.println(pLoc);
        Serial.print("lEndLoc: ");
        Serial.println(lEndLoc);*/
     }
     else
     {
       dEndLoc = s.indexOf(',', lEndLoc+1);
       lon = lon + " " + s.substring(lEndLoc+1, dEndLoc);
       /*Serial.print("i = 4, lEndLoc: ");
        Serial.println(lEndLoc);
        Serial.print("dEndLoc: ");
        Serial.println(dEndLoc);*/
     }
   }
   return lon; 
 }
}

//Parse GPRMC NMEA sentence data from String
//String must be GPRMC or no data will be parsed
//Return Longitude
String parseGprmcSpeed(String s)
{
 int pLoc = 0; //paramater location pointer
 int lEndLoc = 0; //lat parameter end location
 int dEndLoc = 0; //direction parameter end location
 String lndSpeed;

 /*make sure that we are parsing the GPRMC string. 
  Found that setting s.substring(0,5) == "GPRMC" caused a FALSE.
  There seemed to be a 0x0D and 0x00 character at the end. */
 if(s.substring(0,4) == "GPRM")
 {
   //Serial.println(s);
   for(int i = 0; i < 8; i++)
   {
     if(i < 7) 
     {
       pLoc = s.indexOf(',', pLoc+1);
       /*Serial.print("i < 8, pLoc: ");
        Serial.print(pLoc);
        Serial.print(", ");
        Serial.println(i);*/
     }
     else
     {
       lEndLoc = s.indexOf(',', pLoc+1);
       lndSpeed = s.substring(pLoc+1, lEndLoc);
       /*Serial.print("i = 8, pLoc: ");
        Serial.println(pLoc);
        Serial.print("lEndLoc: ");
        Serial.println(lEndLoc);*/
     }
   }
   return lndSpeed; 
 }
}


//Parse GPRMC NMEA sentence data from String
//String must be GPRMC or no data will be parsed
//Return Longitude
String parseGprmcTime(String s)
{
 int pLoc = 0; //paramater location pointer
 int lEndLoc = 0; //lat parameter end location
 int dEndLoc = 0; //direction parameter end location
 String gpsTime;

 /*make sure that we are parsing the GPRMC string. 
  Found that setting s.substring(0,5) == "GPRMC" caused a FALSE.
  There seemed to be a 0x0D and 0x00 character at the end. */
 if(s.substring(0,4) == "GPRM")
 {
   //Serial.println(s);
   for(int i = 0; i < 2; i++)
   {
     if(i < 1) 
     {
       pLoc = s.indexOf(',', pLoc+1);
       /*Serial.print("i < 8, pLoc: ");
        Serial.print(pLoc);
        Serial.print(", ");
        Serial.println(i);*/
     }
     else
     {
       lEndLoc = s.indexOf(',', pLoc+1);
       gpsTime = s.substring(pLoc+1, lEndLoc);
       /*Serial.print("i = 8, pLoc: ");
        Serial.println(pLoc);
        Serial.print("lEndLoc: ");
        Serial.println(lEndLoc);*/
     }
   }
   return gpsTime; 
 }
}

// Turn char[] array into String object
String charToString(char *c)
{

 String val = "";

 for(int i = 0; i <= sizeof(c); i++) 
 {
   val = val + c[i];
 }

 return val;
}

void loop() {
//  Serial.println("ok");
//  if(Serial.available()){
//    getstr = Serial.read();
//    driver();
//  }
//   BT.println("ok");

 if(BT.available()){
   getstr = BT.read();
   driver();
 }
 gps.listen();
 
//  driver();
//  if(control==1)
//  {
//    ultrasonicCar();
//  }
 delay(1000);
 
 // For one second we parse GPS data and report some key values
 for (unsigned long start = millis(); millis() - start < 1000;)  //一秒钟内不停扫描GPS信息
 {
  if(gps.available()) //串口获取到数据开始解析
   {
     char c = gps.read();  //读取一个字节获取的数据

     switch(c)         //判断该字节的值
     {
     case '$':         //若是$，则说明是一帧数据的开始
       gps.readBytesUntil('*', nmeaSentence, 67);    //读取接下来的数据，存放在nmeaSentence字符数组中，最大存放67个字节
       //Serial.println(nmeaSentence);
       latitude = parseGprmcLat(nmeaSentence); //获取纬度值
       longitude = parseGprmcLon(nmeaSentence);//获取经度值
       lndSpeed = parseGprmcSpeed(nmeaSentence);//获取速度值
       gpsTime = parseGprmcTime(nmeaSentence);//获取GPS时间


       if((latitude > "" || longitude > "") && (latitude != " " && longitude != " "))   //当不是空时候打印输出
       {
         BT.listen();
         BT.println(latitude  + "##" + longitude + "\n");
         break;
       }
     }
   }
}
 delay(2000);
}




