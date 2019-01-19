# -*- coding: utf-8 -*-

from baseOp import baseOperator,readAndConvert
from PIL import Image
import time

confirm = readAndConvert('./img/灵基变还.png')#1040,0

handler = baseOperator()
# x从135开始间隔135
y = [255,390,525]
while True:
    img = handler.getScreenCap().convert('L')
    if handler.checkCondition(img,confirm,1040,0,confirm.size):
        for y in range(4):
            for x in range(7):
                handler.tap(135+x*135,255+y*135)
                time.sleep(0.1)
        # 决定
        handler.tap(1160,670)
        time.sleep(0.5)
        # 销毁
        handler.tap(840,590)
        time.sleep(1)
        handler.tap(640,585)
    else:
        handler.tap(640,585)
    time.sleep(0.5)
    
    