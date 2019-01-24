# -*- coding: utf-8 -*-

from baseOp import baseOperator,crop,readAndConvert
from PIL import Image
from ocr import send

img = Image.open('./参考/战斗2.png').convert('L')
t=img.crop((1060,70,1200,100))
print(send(t))