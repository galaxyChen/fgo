# -*- coding: utf-8 -*-

from baseOp import baseOperator,readAndConvert
from PIL import Image
import time

confirm = readAndConvert('./img/从者强化.png')#1090,650
goOn = readAndConvert('./img/继续强化.png')#1050,655

handler = baseOperator()
# x从135开始间隔135
y = [255,390,525]
while True:
    if handler.checkCondition(handler.getScreenCap().convert('L'),confirm,1090,650,confirm.size):
        print("选择狗粮")
        for y_ in y:
            for i in range(7):
                handler.tap(135+i*135,y_)
                time.sleep(0.2)
        #决定
        handler.tap(1150,670)
        time.sleep(1.5)
        #强化
        handler.tap(1110,670)
        time.sleep(1.5)
        #决定
        handler.tap(840,590)
        time.sleep(3)
        print("等待强化界面")
        while not handler.checkCondition(handler.getScreenCap().convert('L'),goOn,1050,655,goOn.size):
            print("等待强化界面")
            time.sleep(0.2)
            handler.tap(1170,510)
    elif handler.checkCondition(handler.getScreenCap().convert('L'),goOn,1050,655,goOn.size):
        print("强化界面，准备选狗粮")
        handler.tap(430,230)
        print("进入选狗粮界面")
        while not handler.checkCondition(handler.getScreenCap().convert('L'),confirm,1090,650,confirm.size):
            pass
    else:
        print("什么也没有")
        handler.tap(1170,510)
        handler.tap(1170,510)
        handler.tap(1170,510)
        #print("点点")
    time.sleep(0.5)
    
    