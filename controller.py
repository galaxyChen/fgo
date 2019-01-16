# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt
from ocr import send
from controlHelper import readAndConvert,findSmall,crop,tap,excute,checkCondition

# 初始化小图
km1 = readAndConvert('./img/km1.png') 
km2 = readAndConvert('./img/km2.png') 
ml1 = readAndConvert('./img/ml1.png') 
ml2 = readAndConvert('./img/ml2.png') 
wc = readAndConvert('./img/wc.png') 
mp = readAndConvert('./img/mpwc.png') 
template = readAndConvert('./img/template.png') 
box = (0,0,157,126)

state_selectBattle = readAndConvert('./img/关卡选择.png')#80,20
state_eatApple = readAndConvert('./img/吃苹果.png')#520,585
state_support = readAndConvert('./img/助战选择标记.png')#1040,0

refreshTooFast = readAndConvert('./img/刷新太快.png')#510,533
confirmFresh = readAndConvert('./img/刷新确认.png')#705,535
startMission = readAndConvert('./img/开始任务.png')#1105,640

skillReady = readAndConvert('./img/attack.png') #1070,650
nextStep = readAndConvert('./img/下一步.png') #1020,650
        
class Controller():
    def __init__(self,settings):
        self.settings = settings
        self.times = 0
        self.apple = 0
        self.retryCount = 0
        self.finished = False
        self.currentBattle = -1
        self.attackReady = False
        self.currentOp = []
    
    def finish(self):
        self.finished = True
        print(time.strftime('%H:%M:%S',time.localtime()))
        print("结束任务")
    
    def analysis(self,img):
        if self.attackReady:
            self.attack(img)
            return
        img = img.convert('L')
        state = self.checkState(img)
        if state == 'selectBattle':
            print("select battle")
            self.selectBattle(img)
            return
        if state == 'eatApple':
            print("eatApple")
            self.eatApple(img)
            return 
        if state == "selectSupport":
            print("选择助战")
            self.selectSupport(img)
            return
        if state == 'startMission':
            print("开始任务")
            self.startMission()
            return
        if state == "skill":
            #print("using skill")
            self.useSkill(img)
            return
        if state == "nextStep":
            print("下一步")
            self.nextStep(img)
            return
        if state == "wait":
            tap(970,90)
            tap(970,90)
            time.sleep(1)
            return
        
    def nextStep(self,img):
        tap(1100,680)
        time.sleep(5)
        
    def checkState(self,img):
        if checkCondition(img,startMission,1105,640,startMission.size):
            return "startMission"
        if checkCondition(img,state_selectBattle,80,20,state_selectBattle.size):
            return "selectBattle"
        if checkCondition(img,state_eatApple,520,585,state_eatApple.size):
            return "eatApple"
        if checkCondition(img,state_support,1040,0,state_support.size):
            return "selectSupport"
        if checkCondition(img,skillReady,1070,650,skillReady.size):
            return "skill"
        if checkCondition(img,nextStep,1020,650,nextStep.size):
            return "nextStep"
        return "wait"
        
    def xjbd(self,img):
        print("xjbd")
        cards = []
        
    
    def attack(self,img):
        self.attackReady = False
        op = self.currentOp[0]
        if op == "xjbd":
            self.xjbd(img)
            self.currentOp.pop(0)
        else:
            cardNum = 0
            while len(self.currentOp)>0:
                op = self.currentOp[0]
                if op[0] == 'b':
                    self.useBj(op)
                    time.sleep(0.5)
                    cardNum += 1
                    self.currentOp.pop(0)
            while cardNum<3:
                self.selectCard(cardNum)
                time.sleep(0.5)
                cardNum += 1
            
            
    def useSkill(self,img):
        battle = self.getBattle(img)
        if battle == -1:
            print("battle 识别出错，重试")
            return
        print("battle %d"%battle)
        if battle == self.currentBattle:
            # 继续执行当前的op
            if len(self.currentOp) == 0:
                # 预定义指令执行完了，开始xjbd
                # 点击attack
                self.currentOp.append('xjbd')
                tap(1130,600)
                self.attackReady = True
                time.sleep(2)
            else:
                op = self.currentOp[0]
                if op[0] == 'j' or op[0] == 'm':
                    self.skill(op)
                    self.currentOp.pop(0)
                elif op[0] == 'b':
                    # 点击attack
                    tap(1130,600)
                    self.attackReady = True
                    time.sleep(2)
                elif op[0] == 'c':
                    self.changeTarget(op)
                    self.currentOp.pop(0)
        else:
            # 更新op列表和当前的battle
            self.currentBattle = battle
            self.currentOp = self.settings['fight'][battle-1].split()
            self.useSkill(img)
                    
    
    def startMission(self):
        tap(1200,680)
        self.currentBattle = -1
        self.times += 1
        print(time.strftime('%H:%M:%S',time.localtime()))
        print("第%d次打本"%self.times)
        time.sleep(10)
        
    def selectBattle(self,img):
        select = False
        if self.settings['times']!=-1 :
            # 按照次数去打本
            if self.settings['times'] > self.times:
                #未达到额定次数
                select = True
            else:
                #达到了额定次数，完成任务
                self.finish()
                return 
        else:
            #按照苹果数量去打本
            select = True
        
        if select:
            tap(950,180)
            time.sleep(1)
            
    def eatApple(self,img):
        eat = False
        if self.settings['apple']!=-1:
            # 按照苹果数量来打本
            if self.apple < self.setting['apple']:
                # 数量未满足,吃苹果
                eat = True
            else:
                # 数量已经满足
                self.finish()
                return 
        else:
            # 根据次数打本，直接吃苹果
            eat = True
        
        if eat:
            self.apple += 1
            print("第%d次吃苹果"%self.apple)
            excute("input swipe 640 360 640 200 300","adb shell")
            time.sleep(0.5)
            if self.settings['apple_prior'] == 1:
                # 金苹果
                tap(380,200)
            if self.settings['apple_prior'] == 2:
                # 银苹果
                tap(380,350)   
            if self.settings['apple_prior'] == 3:
                # 铜苹果
                tap(380,500)
            # 确认吃苹果
            time.sleep(1)
            tap(840,560)
            
            
                                            
    def getBattle(self,img):
        t = img.crop((750,0,950,130))
        res = send(t)
        res = res['data']['item_list']
        for item in res:
            if item['itemstring'].upper().startswith('BAT'):
                battle = item['itemstring'].split()[1][0]
                return int(battle)
        #print(res)
        return -1;
            
    def selectCard(self,cardNum):
        y = 400;
        x_loc = {1:130,2:380,3:640,4:900,5:1160}
        x =x_loc[cardNum]
        tap(x,y)
    
    def useBjHelper(self,bjNum):
        y = 220
        x_loc = {1:410,2:640,3:880}
        x =x_loc[bjNum]
        tap(x,y)
    
    def useBj(self,op):
        num = int(op[1])
        self.useBjHelper(num)
        
    def changeTarget(self,op):
        target = int(op[1])
        y = 40
        x_loc = {1:45,2:285,3:525}
        x =x_loc[target]
        tap(x,y)
            
    def skill(self,op):
        print("使用技能：%s"%op)
        if op[0] == 'j':
            target = op[1:3]
            y = 580
            user = {'1':70,'2':380,'3':700}
            offset = {'1':0,'2':95,'3':190}
            x = user[target[0]] + offset[target[1]]
            tap(x,y)
            if len(op) == 4:
                y = 450
                target = {'1':330,'2':660,'3':950}
                x = target[op[3]]
                time.sleep(1)
                tap(x,y)
            time.sleep(1.5)
            return 
        
        if op[0] == 'm':
            tap(1190,310)
            time.sleep(0.5)
            y = 320
            target = {'1':910,'2':995,'3':1080}
            x = target[op[1]]
            tap(x,y)
            if len(op) == 3:
                y = 450
                target = {'1':330,'2':660,'3':950}
                x = target[op[2]]
                time.sleep(1)
                tap(x,y)
            time.sleep(1.5)
            return 
    
    def findSupport(self,supportList,target):
        # 判断当前助战列表有没有需要的目标
        x,y,dis = findSmall(supportList,target,10)
        if dis<40:
            print("发现目标!")
            tap(int(50+x+target.size[0]/2),int(170+y+target.size[1]/2))
            self.confirm = True # 等待开始任务标记
            self.retryCount = 0
            return True
        return False
    
    def refreshSupport(self):
        # 刷新助战列表
        print("刷新助战")
        tap(840,128)
        
    def selectSupport(self,img):
        # 组合出需要找的助战图
        if checkCondition(img,refreshTooFast,510,533,refreshTooFast.size):
            # 刷新助战太快
            print("刷新太快了")
            tap(640,560)
            time.sleep(3)
            self.refreshSupport()
            return 
            
            
        if checkCondition(img,confirmFresh,705,535,confirmFresh.size):
            # 刷新助战确认
            tap(840,560)
            print("刷新助战确认")
            time.sleep(1)
            return 
                
        print("搜索助战")
        target = self.settings['support']
        supportList = crop(img,50,170,(216,550))
        found = False
        if target == 'km':
            template.paste(km1,box)
            found = self.findSupport(supportList,template)
            if not found:
                template.paste(km2,box)
                found = self.findSupport(supportList,template)
        if target == 'ml':
            template.paste(ml1,box)
            found = self.findSupport(supportList,template)
            if not found:
                template.paste(ml2,box)
                found = self.findSupport(supportList,template)
        # 没找到就向下滑
        if not found:
            excute("input swipe 690 700 690 500 300","adb shell")
            print("划一下")
            time.sleep(3)
            self.retryCount += 1
            if self.retryCount == 6:
                # 尝试4次就刷新
                self.refreshSupport()
                self.retryCount = 0
        else:
            time.sleep(1.5)
        
        
if __name__ == '__main__':
    con = Controller('skm')
    #test = Image.open('./img/test2.png')
    #con.analysis(test)
        
        