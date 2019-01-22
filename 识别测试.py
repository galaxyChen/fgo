# -*- coding: utf-8 -*-

from baseOp import baseOperator,crop,readAndConvert
from PIL import Image

op = baseOperator()
member = ['孔明','船长','阿比','梅林']
memberCards = {}
for m in member:
    memberCards[m] = Image.open('./img/cards/%s.png'%(m)).convert('L')
    
img = Image.open('./参考/卡3.png')
img_ = img.convert('L')
y = 350
x = [40,300,550,810,1070]
width = 180
height = 300
color = []
cards = []
print("begin")
for i,x_ in enumerate(x):
    t = crop(img_,x_,y,(width,height))
    minDis = 100
    mark = ''
    for m in member:
        _,_,dis = op.findSmall(t,memberCards[m],5)
        if dis<minDis:
            minDis = dis
            mark = m
    cards.append(mark)
    
color = op.getCardsColor(img)
cards = zip(cards,color)
for i,c in enumerate(cards):
    print("card %d: %s%s"%(i+1,c[0],c[1]))