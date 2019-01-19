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
import re
from PIL import ImageEnhance

def readAndConvert(path):
    img = Image.open(path)
    return img.convert('L')

def excute(order,pre = ''):
    if pre == '':
        os.popen(order)
        return
    line = '%s "%s"'%(pre,order)
    #print(line)
    os.popen(line)
    
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

def getColor(img):
    r,g,b = sumRGB(img)
    color = {'red':r,'green':g,'blue':b}
    return max(color,key = lambda x:color[x])

numPattern = re.compile(r'[^\d]')
cards = []
for i in range(5):
    cards.append(Image.open('./img/card%dTitle.png'%(i+1)))
    

class baseOperator:
    def __init__(self):
        self.memberCards = None
        pass
    
    def loadMember(self,member):
        memberCards = {}
        for m in member:
            memberCards[m] = {}
            for c in ['红卡','蓝卡','绿卡']:
                memberCards[m][c] = Image.open('./img/cards/%s_%s.png'%(m,c)).convert('L')
        self.memberCards = memberCards
    
    def checkMemberData(self):
        if self.memberCards is None:
            return False
        return True
    
    def adbInit(self):
        excute('adb connect 127.0.0.1:7555')
        excute('adb forward tcp:9090 tcp:7070')
        
    def getScreenCap(self):
        screenCap()
        return fetchImg()
        
    def tap(self,x,y):
        #print("点击%d %d"%(x,y))
        excute("input tap %d %d"%(x,y),"adb shell")
    
    def findSmall(self,s,t,times = 1):
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
    
    def checkCondition(self,img,t,x,y,size):
        # 判断给定位置是不是有对应的图
        s = crop(img,x,y,size)
        x_,y_,dis = self.findSmall(s,t)
        # 小于阈值就判断为存在
        if dis<10:
            return True
        else:
            return False
    
    def getBattle(self,img):
        t = img.crop((750,0,950,130))
        res = send(t)
        res = res['data']['item_list']
        for item in res:
            if item['itemstring'].upper().startswith('BAT'):
                battle = item['itemstring'].split()[1][0]
                return int(battle)
        #print(res)
        return -1;
    
    def getNp(self,img = None):
        if not img:
            img = self.getScreenCap().convert('L')
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
        
    
    
    def getCardsColor(self,img = None):
        if not img:
            img = self.getScreenCap()
        y = 500
        x = [55,310,565,825,1085]
        width = 145
        height = 105
        colors =[]
        for x_ in x:
            c = getColor(crop(img,x_,y,(width,height)))
            colors.append(c)
        return colors
    
    def recognizeCard(self,img = None):
        if not self.checkMemberData():
            print("member data not found!")
            return
        if not img:
            img = self.getScreenCap().convert('L')
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
            for m in self.memberCards:
                for c in ['红卡','蓝卡','绿卡']:
                    #print("check "+m+c)
                    _,_,dis = self.findSmall(oneCard,self.memberCards[m][c],5)
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
    
    