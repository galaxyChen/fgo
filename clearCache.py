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
                
fetchImg()