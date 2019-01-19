# -*- coding: utf-8 -*-

from baseOp import baseOperator,readAndConvert
from PIL import Image
import time

friend = readAndConvert('./img/友情池.png')#710,650

handler = baseOperator()
handler.adbInit()
while True:
    img = handler.getScreenCap().convert('L')
    if handler.checkCondition(img,friend,710,650,friend.size):
        #print("召唤")
        handler.tap(770,670)
        time.sleep(1)
        handler.tap(830,550)
        time.sleep(0.5)
        handler.tap(830,550)
    else:
        handler.tap(1170,510)
        handler.tap(1170,510)
        handler.tap(1170,510)
        #print("点点")
    time.sleep(0.5)
    
    