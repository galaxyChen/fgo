# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt
from ocr import send

def readAndConvert(path):
    img = Image.open(path)
    return img.convert('L')

def printTime():
    print(time.strftime('%H:%M:%S',time.localtime(time.time())))

def excute(order,pre = ''):
    line = '%s "%s"'%(pre,order)
    #print(line)
    os.popen(line)
    
def tap(x,y):
    #print("点击%d %d"%(x,y))
    excute("input tap %d %d"%(x,y),"adb shell")

def similarity(s,t):
    return np.abs(s-t).sum()

def crop(img,x,y,size):
    # 从x，y位置切下来大小为size的一块
    width = size[0]
    height = size[1]
    return img.crop((x,y,x+width,y+height))

def picToArray(img):
    # 灰度图转变成矩阵
    return np.array(list(img.getdata())).reshape(img.size)

def shrink(img,times):
    # 等比缩小图片
    return img.resize((int(img.size[0]/times),int(img.size[1]/times)))

def findSmall(s,t,times = 1):
    # 缩小图片
    s = shrink(s,times)
    t = shrink(t,times)
    tlen = t.size[0] * t.size[1]
    t_ = picToArray(t)
    # 遍历每一个子图计算相似度
    min_x = 0
    min_y = 0
    min_dis = sys.maxsize
    for i in range(0,s.size[0] - t.size[0] + 1):
        for j in range(0,s.size[1] - t.size[1] + 1):
            s_ = picToArray(crop(s,i,j,t.size))
            dis = similarity(s_,t_)/tlen
            if dis < min_dis:
                min_x = i
                min_y = j
                min_dis = dis
    # 返回值是没有缩小的坐标
    return min_x*times,min_y*times,min_dis

def checkCondition(img,t,x,y,size):
    # 判断给定位置是不是有对应的图
    s = crop(img,x,y,size)
    x_,y_,dis = findSmall(s,t)
    # 小于阈值就判断为存在
    if dis<10:
        return True
    else:
        return False

def sumRGB(img):
    data = list(img.getdata())
    r = 0
    g = 0
    b = 0
    for p in data:
        r += p[0]
        g += p[1]
        b += p[2]
    
    l = len(data)
    return r/l,g/l,b/l