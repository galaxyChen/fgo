# -*- coding: utf-8 -*-

import os
from socket import *
import io
from PIL import Image
import numpy as np
import time
from controller import Controller
import matplotlib.pyplot as plt
from PIL import ImageEnhance
import re

import sys
from ocr import send
from controlHelper import readAndConvert,findSmall,crop,tap,excute,checkCondition,getColor

cards = []
for i in range(5):
    cards.append(Image.open('./img/card%dTitle.png'%(i+1)))

numPattern = re.compile(r'[^\d]')
member = ['梅林','c狐','阿比']
memberCards = {}
for m in member:
    memberCards[m] = {}
    for c in ['红卡','蓝卡','绿卡']:
        memberCards[m][c] = Image.open('./img/cards/%s_%s.png'%(m,c)).convert('L')

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
    
    
    
def getNp(img = None):
    if not img:
        img = getScreenCap().convert('L')
    start_time = time.time()
    data = send(img.crop((105,650,950,720)))['data']
    np = []
    for item in data['item_list']:
        if '%' in item['itemstring']:
            num = re.sub(numPattern,'',item['itemstring'])
            if len(num)==0:
                np.append(0)
            else:
                np.append(int(num))
                
    #print(time.time()-start_time)
    return np
    


def getCardsColor(img = None):
    if not img:
        img = getScreenCap()
    y = 500
    x = [55,310,565,825,1085]
    width = 145
    height = 105
    colors =[]
    for x_ in x:
        c=getColor(crop(img,x_,y,(width,height)))
        colors.append(c)
    return colors

def recognizeCard(img = None):
    if not img:
        img = getScreenCap().convert('L')
    y = 350
    x = [40,300,550,810,1070]
    width = 180
    height = 300
    cardList = []
    for x_ in x:
        #print()
        oneCard = crop(img,x_,y,(width,height))
        cardName = ""
        minDis = 100
        for m in memberCards:
            for c in ['红卡','蓝卡','绿卡']:
                #print("check "+m+c)
                _,_,dis = findSmall(oneCard,memberCards[m][c],5)
                #print(dis)
                if dis<minDis:
                    cardName = m+c
                    minDis = dis
        cardList.append(cardName)
    
    return cardList
    
    
    
def getStars(img = None):
    if not img:
        img = getScreenCap()
    enh = ImageEnhance.Contrast(img)
    img = enh.enhance(2)
    y = 340
    x = [50,310,550,820,1080]
    width = 200
    height = 70
    newImg = Image.new("RGBA",(width,height*10))
    
    for i in range(5):
        h = 2*i*height
        newImg.paste(cards[i],(0,h,width,h+height))
        h += height
        newImg.paste(crop(img,x[i],y,(width,height)),(0,h,width,h+height))
    
    data = send(newImg.convert('L'))
    star = []
    currentStar = 0
    while (data['ret']!=0):
        print("星星识别出错，重新识别")
        data = send(newImg.convert('L'))
    data = data['data']['item_list']
    for item in data:
        if item['itemstring'].startswith('色卡'):
            if item['itemstring'] != '色卡1:':
                star.append(currentStar)
                currentStar = 0
            
        if '%' in item['itemstring']:
            num = re.sub(numPattern,'',item['itemstring'])
            if len(num)==0 or num == '0':
                currentStar = 0
            else:
                currentStar = int(num)
    star.append(currentStar)
    return star
    
def getCardsInfo(img = None ,show = False):
    if not img:
        img = getScreenCap()
    color = getCardsColor(img)
    np = getNp(img)
    star = getStars(img)
    cardList = recognizeCard()
    if show:
        print("color:")
        print(color)
        print("np:")
        print(np)
        print("star")
        print(star)
        print("card")
        print(cardList)
