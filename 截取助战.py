# -*- coding: utf-8 -*-

from baseOp import baseOperator,crop,readAndConvert
from PIL import Image

template = readAndConvert('./img/km1.png')
lz = readAndConvert('./img/wc.png')

img = Image.open('./参考/小莫.png')
x = 50
y = 200
member = crop(img,x,y,template.size)
newlz = crop(img,50,y+template.size[1],lz.size)