from baseOp import baseOperator,readAndConvert
from PIL import Image
import time

finish = readAndConvert('./img/daili.png')# 1050,570, (195,45)
finish_2 = readAndConvert('./img/daili_start.png')#1050,400,(100,200)
handler = baseOperator()

def waitUntil(condition,x,y,handler,sleep=1):
    while True:
        img = handler.getScreenCap().convert('L')
        if handler.checkCondition(img,condition,x,y,condition.size):
            return
        handler.tap(1100,300)
        time.sleep(sleep)
        

number = 4
count = 0
while True:
    waitUntil(finish,1050,570,handler,10)
    handler.tap(1150,655)
    waitUntil(finish_2,1050,400,handler)
    handler.tap(1100,500)
    count += 1
    print("begin the %d battle"%count)
    if number>0 and count==number:
        break
    time.sleep(60)