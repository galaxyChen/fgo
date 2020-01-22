from baseOp import baseOperator,readAndConvert
from PIL import Image
import time

finish = readAndConvert('./img/抽完池子.png')#1100,230
reset = readAndConvert('./img/重置.png')#800,540
close = readAndConvert('./img/重置关闭.png') # 600,540
handler = baseOperator()


def waitUntil(condition,x,y,handler,sleep=1):
    while True:
        img = handler.getScreenCap().convert('L')
        if handler.checkCondition(img,condition,x,y,condition.size):
            return
        handler.tap(1100,300)
        time.sleep(sleep)
        
count = 0
while True:
    print("抽")
    for _ in range(10):
        handler.tap(430,450)
        time.sleep(0.1)
    img = handler.getScreenCap().convert('L')
    if handler.checkCondition(img,finish,1100,230,finish.size):
        count += 1
        print("抽完第%d池"%count)
        print("重置")
        handler.tap(1140,245)
        waitUntil(reset, 800,540, handler, 0.5)
        print("重置确认")
        handler.tap(840,570)
        waitUntil(close, 600,540, handler, 0.5)
        print("关闭窗口")
        handler.tap(650,560)
