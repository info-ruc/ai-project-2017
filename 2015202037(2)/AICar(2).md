# AICar（2）

@2015202004  @2015202008  @2015202031  @2015202037


- **人工智能小车** ：是一个可以根据传感器传感路障，依靠arduino板控制马达，自动调转方向运行的智能小车。还可通过蓝牙连接，人工操作小车的前后左右运转。

-------------------
### 前期准备
- 重新调试之前搭建的小车
- 二次购买面包板、面包线、电池等材料
- 下载链接蓝牙的APP
> 下载[Arduino](https://www.arduino.cc)，用于向arduino板导入控制程序
> 下载蓝牙串口控制APP，用于连接AICar上的BT06 Bluetooth


------------------
### 线路重连
1.改变上阶段电池连接在马达上的方式，本阶段通过驱动板连接马达和面包板。
2.利用与Arduino之间的连接以程序控制小车的运行。 
3.蓝牙板通过连线与驱动板和Arduino板相连
4.达到手机能连接蓝牙，控制小车的运行。


------------------
### 上阶段问题解决
- [x] 左右轮转速不均衡
- 导入程序，调整车轮转速对应的代码，是两轮的速度一致达到直线行走的目的。
- [x] 接入外接电源之后，小车无法稳定行驶
- 重新分析连接线路，更换新电池，驱动力充足。
- [x] 蓝牙发送指令无效并接收到来自小车的乱码
- 修改蓝牙连接的线路，尝试更换其他端口，使得蓝牙能正确连接。
- [x] arduino板接入电源后，发出警报声
- 后来发现是马达的运作声音，单接Arduino板是没有声音的。重连线路后，arduino板能够正常运行。

------------------
### 本阶段实现的功能
- 能够使用手机操纵小车的前进、后退、左右转功能
- 能够自动行驶并且躲避障碍物，返回与障碍物之间的距离
- 能够搭载手机，实时传输小车所到达位置的路况

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
### 未来展望
- 预设想：“循迹小车”——为小车搭建跑道，利用传感器控制小车自动沿轨道运行。
- 结合图像识别相关技术，处理小车传送回来的影像。
- 提高小车的质量，减少小车运行出错。

