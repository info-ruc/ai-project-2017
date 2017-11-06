# coding=utf-8
import turtle
import time
import math

def shield():
    # 设置背景
    turtle.bgcolor('#010101')
    # 设置速度
    turtle.speed(5)
    turtle.done()

if __name__ == '__main__':
    #shield()
    turtle.bgcolor('#000000')
    # 设置速度
    turtle.speed(1)
    turtle.pensize(3)
    turtle.color('#FF0000', '#FF0000')
    turtle.fillcolor()
    
    count=0
    i=0
    for t in range(1):
        f = open('data.txt',encoding='UTF-8')
        #i=0
        time=0
        times=0
        record=0
        for lines in f:
            if count==i:
                list1=lines.split(' ')
                if time!=0:
                    a=int(list1[1])
                    times=a-time
                    time=a
                    if list1[0]=='random':
                        record=int(list1[2])
                        time=a+int(list1[2])
                    print(times)
                else:
                    time=float(list1[1])
                    status=0
                if status=='backward':
                    turtle.backward(float(times)/100)
                elif status=='forward':
                    turtle.forward(float(times)/100)
                elif status=='left':
                    turtle.left(float(times)/100*3)
                elif status=='right':
                    turtle.right(float(times)/100*3)
                elif status=='random':
                    a=list1[2]
                    turtle.right(float(record)/100*3)
                    turtle.forward(float(times)/100)
                else:
                    pass
                count=count+1

                status=list1[0]
            i=i+1
        f.close()
    turtle.done()

