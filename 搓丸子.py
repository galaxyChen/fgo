# -*- coding: utf-8 -*-

from baseOp import baseOperator,readAndConvert
from PIL import Image
import time

confirm = readAndConvert('./img/强化确认.png')#760,0
goOn = readAndConvert('./img/继续强化.png')#1050,655

handler = baseOperator()
# x从135开始间隔135
y = [255,390,525]
while True:
    img = handler.getScreenCap().convert('L')
    if handler.checkCondition(img,goOn,1050,655,goOn.size):
        handler.tap(430,230)
        time.sleep(1)
    elif handler.checkCondition(img,confirm,760,0,confirm.size):
        for y_ in y:
            for i in range(7):
                handler.tap(135+i*135,y_)
                time.sleep(0.2)
        #决定
        handler.tap(1150,670)
        time.sleep(1)
        #强化
        handler.tap(1110,670)
        time.sleep(0.5)
        #决定
        handler.tap(840,590)
        while handler.checkCondition(handler.getScreenCap().convert('L'),confirm,760,0,confirm.size):
            handler.tap(1170,510)
    else:
        handler.tap(1170,510)
        handler.tap(1170,510)
        handler.tap(1170,510)
        #print("点点")
    time.sleep(0.5)
    
    