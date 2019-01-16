# -*- coding: utf-8 -*-

import os
from socket import *
import io
from PIL import Image
import numpy as np
import time
from controller import Controller
import matplotlib.pyplot as plt

import sys
from ocr import send
from controlHelper import readAndConvert,findSmall,crop,tap,excute,checkCondition,getColor

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
        
def getScreenCap():
    screenCap()
    return fetchImg()
    
    
    
def getNp():
    img = getScreenCap()
    y = 650
    x = [105,420,740]
    width = 210
    height = 70
    np = ""
    for x_ in x:
        npImg = crop(img,x_,y,(width,height))
        data = send(npImg)
        data = data['data']['item_list']
        #print(data)
        #print()
        for item in data:
            npString = item['itemstring'].replace('.','').replace('-','')
            if npString.endswith('%'):
                np += npString + " "
                break
    print(np)
    

def getStar():
    img = getScreenCap().convert('L')
    y = 340
    x = [50,310,550,820,1080]
    width = 200
    height = 70
    
    star = ""
    for x_ in x:
        starImg = crop(img,x_,y,(width,height))
        data = send(starImg)
        data = data['data']['item_list']
        print(data)
        print()
        for item in data:
            starString = item['itemstring'].replace('.','').replace('-','')
            if starString.endswith('%'):
                star += starString + " "
                break
    print(star)

def getCards():
    y = 400
    x = [55,310,565,825,1085]
    width = 145
    height = 205
    
    
    
    
    
    