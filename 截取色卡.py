# -*- coding: utf-8 -*-

from PIL import Image
from baseOp import crop,baseOperator

op = baseOperator()
#img = Image.open('./参考/闪闪.png')
img = op.getScreenCap()
y = 441
x = [55,310,565,825,1085]
width = 120
height = 50

cardNum = 1
cardImg = crop(img,x[cardNum-1],y,(width,height))