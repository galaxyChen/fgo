from baseOp import baseOperator,readAndConvert
from PIL import Image
import time

finish = readAndConvert('./img/抽完池子.png')#260,430,360,510
finish_2 = readAndConvert('./img/抽完池子2.png')#590,540,680,590
handler = baseOperator()

while True:
    img = handler.getScreenCap().convert('L')
    if handler.checkCondition(img,finish,260,430,finish.size):
        handler.tap(1140,245)
        time.sleep(1)
        handler.tap(840,560)
        time.sleep(1)
        while not handler.checkCondition(handler.getScreenCap().convert('L'),finish_2,590,540,finish_2.size):
            pass
        handler.tap(640,560)
        time.sleep(1)
    else:
        for i in range(10):
            handler.tap(430,450)
            time.sleep(0.1)