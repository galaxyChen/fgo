from baseOp import baseOperator,readAndConvert
from PIL import Image
import time

finish = readAndConvert('./img/抽完池子.png')#240,420,370,520
handler = baseOperator()

while True:
    img = handler.getScreenCap().convert('L')
    if handler.checkCondition(img,finish,240,420,finish.size):
        handler.tap(1140,245)
        time.sleep(0.3)
        handler.tap(840,560)
        time.sleep(0.3)
        handler.tap(640,560)
        time.sleep(0.3)
    else:
        for i in range(10):
            handler.tap(430,450)
            time.sleep(0.1)