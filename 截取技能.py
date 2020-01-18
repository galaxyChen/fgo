from PIL import Image
from baseOp import crop,baseOperator





if __name__ == '__main__':
    op = baseOperator()
    #img = Image.open('./参考/attack1.png')
    img = op.getScreenCap()
    y = 550
    width = 55
    height = 55
    x_gap = 95
    x = [40,360,680]
    
    member = 3
    skill = 3
    skillImg = crop(img,x[member-1]+(skill-1)*x_gap,y,(width,height))