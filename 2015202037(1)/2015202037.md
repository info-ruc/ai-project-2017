# AICar（1）

@2015202004  @2015202008  @2015202031  @2015202037


- **人工智能小车** ：是一个可以根据传感器传感路障，依靠arduino板控制马达，自动调转方向运行的智能小车。还可通过蓝牙连接，人工操作小车的前后左右运转。

-------------------
### 前期准备
- Arduino UNO
- BT06 Bluetooth
- HC-SR04 Ultrasonic Distance Measuring
- L293D Motor Drive Shield
- 2WD Smart Robot Car Chassis Kit
- 及其他相关器材
> 下载[Arduino](https://www.arduino.cc)，用于向arduino板导入控制程序
> 下载蓝牙串口控制APP，用于连接AICar上的BT06 Bluetooth

------------------
### 实验思路
```flow
st=>start: 接受部分
e=>end: 等待
op=>operation: 自动避障
op1=>operation: 启动超声波模块
op2=>operation: 等待接收数据
op3=>operation: 转向
op4=>operation: 继续行驶
cond=>condition: 近吗？
op5=>operation: 判断是否接到命令
op6=>operation: 等待
st->op->op1->op2->cond
cond(yes)->op3->op5->op6
cond(no)->op4->op5->op6


```
------------------
### 线路搭建
1.底板搭建：将三个轮子固定在底盘上，两个后轮分别与马达相连，注意：马达的突起方向朝外，便于马达连接电池。
2.驱动板与arduino板上下重叠连接，置于底盘上方中部。
3.驱动板两端M1、M4四个端口与马达相连，两个马达与航模电池串联。
4.超声波测距传感器置于面包板上，面包板固定于底板前端。
5.其中蓝牙板的四个接口分别连接驱动板上的5v、Gnd、1、0四个端口。
6.超声波测距传感器的四个接口分别与驱动板左上角的SER1、SERV0_2连接。
7.Arduino板的接口可连接电脑或充电宝。


------------------
### 初步启动
在未导入程序之前，AI小车可以凭借自身电路启动并行走。小车在搭建完成之后，我们尝试了第一次启动。

[初次启动的视频](http://www.example.com)

小车车轮由两块航模电车驱动，在电路通路时，小车向前行驶。由于物理器件的原因，小车左轮转速高于右轮，这就使得小车不断顺时针旋转。我们推测是由于马达驱动不均衡所造成的。解决的办法有两个：一是使用代码来人工调整小车左右轮的转速，使之平衡；二是换马达，使两个马达动力尽量均衡。


------------------
### 程序导入

```java
@luckh2
void setup() {
  // 启动程序
  Serial.begin(9600);    
  Rback_motor.setSpeed(0);
  Rback_motor.run(RELEASE);
  Lback_motor.setSpeed(0);
  Lback_motor.run(RELEASE);
  delay(2000);

  //超声波测距
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
}

```

```java
@luckh2
//以下为本实验中不同输入所对应的功能：其中输入'>'与'<'可以人为调整两个轮胎的转速，使得小车能够直线运行
void driver() {
  if ((getstr == '<')&&(RLRatio>0.1)) {
    RLRatio -= 0.1;
    Serial.println(RLRatio);
  }  
  if (getstr == '>') {
    RLRatio += 0.1;
    Serial.println(RLRatio);
  }  
  if (getstr == '5') {
    Serial.println("stopcar");
    stopcar();
    control=0;
  }
  if (getstr == '1') {
    Serial.println("forward");
    forward();
    control=0;
  }
if (getstr == '2') {
    Serial.println("backward");
    backward();
    control=0;
  }
  if (getstr == '3') {
    Serial.println("right");
    right();
    control=0;
  }
  if (getstr == '4') {
    Serial.println("left");
    left();
    control=0;
  }
  if (getstr=='6'){
    control=1;
    Serial.println("Auto Control On");
  }
  if(getstr=='7'){
    control=0;
    Serial.println("Auto Control Off");
  }
 
```
以上为本次实验的部分代码，针对我们组装小车时候遇见的问题给出了修正。


------------------
### 现阶段问题分析

- [x] 电脑无法识别arduino板
- [ ] 左右轮转速不均衡
- [ ] 接入外接电源之后，小车无法稳定行驶
- [ ] 蓝牙发送指令无效并接收到来自小车的乱码
- [ ] arduino板接入电源后，发出警报声
- [ ] arduino板一旦接入，便无法运行
> 可能原因:接线电路存在问题，电池驱动力不足，两侧马达驱动能力不一致等。


------------------
### 未来展望




1.解决现阶段存在的问题，蓝牙连接成功并实现避障功能。
2.美化小车外形，丰富小车功能。



