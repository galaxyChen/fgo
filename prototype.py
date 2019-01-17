# -*- coding: utf-8 -*-
import os
from socket import *
import io
from PIL import Image
import numpy as np
import time
from controller import Controller
import matplotlib.pyplot as plt

def excute(order,pre = ''):
    if pre == '':
        os.popen(order)
        return
    line = '%s "%s"'%(pre,order)
    #print(line)
    os.popen(line)
        
def adbInit():
    excute('adb connect 127.0.0.1:7555')
    excute('adb forward tcp:9090 tcp:7070')
    
    
def screenCap():
    #print("截图")
    #printTime()
    excute('screencap -p | busybox nc -p 7070 -l','adb shell')
        
def fetchImg():
    #print("开始拿图")
    #printTime()
    address='127.0.0.1'   #服务器的ip地址
    port = 9090         #服务器的端口号
    buffsize = 4096        #接收数据的缓存大小
    while True:
        s=socket(AF_INET, SOCK_STREAM)
        s.connect((address,port))
        recvdata=s.recv(buffsize)
        if len(recvdata)>0:
            f = []
            while len(recvdata)>0:
                f.append(recvdata)
                recvdata=s.recv(buffsize)
            
            byteFile = io.BytesIO(b''.join(f))
            img = Image.open(byteFile)
            return img

        s.close()
                
def getOpList():
    '''
    op格式：
    每个指令用空格隔开
    s代表选择助战，km是孔明，ml是梅林
    j代表技能，j112表示1号位的1技能给2号位（从左往右数），非指定技能格式为j11,没有第三个数字
    m代表master技能，m12表示1技能给2号位
    c代表改变目标,c1表示选择第一个目标
    b表示宝具，后面的数字表示第几个宝具
    
    返回一个dict，包括循环的苹果数目，需要的助战，战斗的流程
    '''
    #return 'skm'
    return {
        'support':'ml',
        'apple':-1,
        'fight':[
            'j11 j13 j22 j31 m21 b1',
            'b2',
            'b3'
        ],
        'xjbd':'red',
        'times':1,
        'apple_prior':3
    }
    
def printTime():
    print(time.strftime('%H:%M:%S',time.localtime(time.time())))  

adbInit()
op = getOpList()
endFlag = False
con = Controller(op)

while True:
    screenCap()
    img = fetchImg()
    con.analysis(img)
    if con.finished:
        break
    
    

