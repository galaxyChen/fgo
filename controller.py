# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt
from ocr import send
from controlHelper import readAndConvert,findSmall,crop,tap,excute,checkCondition
from baseOp import baseOperator
import re

# 初始化助战路径
img_path = './img/'
support_dict = {
        'cba':['cba.png'],
        'km':['km1.png','km2.png','km3.png'],
        'ml':['ml1.png','ml2.png','ml3.png']
        }

wc = readAndConvert('./img/wc.png') 
mp = readAndConvert('./img/mpwc.png') 
template = readAndConvert('./img/template.png') 
box = (0,0,157,126)

# 场景标记
state_selectBattle = readAndConvert('./img/关卡选择.png')#80,20
state_eatApple = readAndConvert('./img/吃苹果.png')#520,585
state_support = readAndConvert('./img/助战选择标记.png')#1040,0

refreshTooFast = readAndConvert('./img/刷新太快.png')#510,533
confirmFresh = readAndConvert('./img/刷新确认.png')#705,535
startMission = readAndConvert('./img/开始任务.png')#1105,640

skillReady = readAndConvert('./img/attack.png') #1070,650
nextStep = readAndConvert('./img/下一步.png') #1020,650
goBack = readAndConvert('./img/返回按钮.png') # 1235, 670

changeX = readAndConvert('./img/换人x.png')#1200,115

addFriend = readAndConvert("./img/申请好友.png") # 900,600
        
class Controller():
    def __init__(self,settings):
        self.targetTimes = -1
        self.targetApples = -1
        self.times = 0
        self.apple = 0
        self.apple_prior = 1
        
        self.support = []
        self.supportImg = {}
        self.cloth = []
        self.currentSupport = None
        
        self.retryCount = 0
        self.finished = False
        self.attackReady = False
        self.currentOp = []
        self.offline = False
        self.currentBattle = 1
        
        self.setConfig(settings)
        self.op = baseOperator()
        
        
        
    def setConfig(self, setting):
        if 'times' in setting:
            self.targetTimes = setting['times']
        if 'apple' in setting:
            self.targetApples = setting['apple']
        if 'support' in setting:
            self.support = setting['support']
            for people in setting['support']:
                peopleImg = []
                for imgName in support_dict[people]:
                    peopleImg.append(readAndConvert(img_path+imgName))
                self.supportImg[people] = peopleImg
        if 'cloth' in setting and setting['cloth'] is not None:
            self.cloth = setting['cloth']
        if 'apple_prior' in setting:
            self.apple_prior = setting['apple_prior']
        if 'offline' in setting:
            self.offline = setting['offline']
    
    def finish(self):
        print("finish")
        self.finished = True
        print(time.strftime('%H:%M:%S',time.localtime()))
        print("结束任务")
    
        
    def nextStep(self):
        print("next step")
        tap(1100,680)
        time.sleep(5)
        
    def checkState(self,img=None):
        if img is None:
            img = self.op.getScreenCap().convert("L")
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
        if checkCondition(img,addFriend,900,600,addFriend.size):
            return "addFriend"
        return "wait"
                
    
    def attack(self):
        print("attack")
        tap(1130, 600)
        time.sleep(2)
        
    def goBack(self):
        print("go back")
        tap(1200,680)
        time.sleep(1)
        
    def refuse(self):
        print("refuse")
        tap(330,620)
        time.sleep(1)
            
            
    def startMission(self):
        print("start mission")
        tap(1200,680)
        self.currentBattle = 1
        self.times += 1
        print(time.strftime('%H:%M:%S',time.localtime()))
        print("第%d次打本"%self.times)
        time.sleep(10)
        
    def selectBattle(self,img=None):
        print("select battle")
        select = False
        if self.targetTimes!=-1 :
            # 按照次数去打本
            if self.targetTimes > self.times:
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
            
    def eatApple(self):
        print("eat apple")
        eat = False
        if self.targetApples!=-1:
            # 按照苹果数量来打本
            if self.apple < self.targetApples:
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
            if self.apple_prior == 1:
                # 金苹果
                tap(380,200)
            if self.apple_prior == 2:
                # 银苹果
                tap(380,350)   
            if self.apple_prior == 3:
                # 铜苹果
                tap(380,500)
            # 确认吃苹果
            time.sleep(1)
            tap(840,560)
            
    def _getBattleOffline(self):
        battle = self.currentBattle
        self.currentBattle += 1
        if self.currentBattle == 4:
            self.currentBattle = 1
        print("battle:", battle)
        return battle
                                            
    def getBattle(self,img=None):
        print("get battle")
        if self.offline:
            return self._getBattleOffline()
        if img is None:
            img = self.op.getScreenCap().convert("L")
        t = img.crop((750,0,950,130))
        res = send(t)
        res = res['data']['item_list']
        print("=============")
        for item in res:
            print(item['itemstring'])
            match =  re.search('([123])[/1]3', item['itemstring'].replace(" ",""))
            if match:
                battle = match.group(1)
                print("=============")
                print("battle", battle)
                return int(battle)
        print("============")
        #print(res)
        return self.getBattle()
            
    def selectCard(self,cards):
        print("select cards", cards)
        for cardNum in cards:
            y = 400;
            x_loc = {1:130,2:380,3:640,4:900,5:1160}
            x =x_loc[cardNum]
            tap(x,y)
            time.sleep(0.5)
    
    
    def useBj(self,bjs):
        print("use big", bjs)
        for bjNum in bjs:
            y = 220
            x_loc = {1:410,2:640,3:880}
            x =x_loc[bjNum]
            tap(x,y)
            time.sleep(0.5)
        
    def changeTarget(self,target):
        print("change target:", target)
        # 从左到右123
        y = 40
        x_loc = {1:45,2:285,3:525}
        x =x_loc[target]
        tap(x,y)
        
    def changeMember(self,m1,m2):
        print("change member")
        self.useSkill(['m3'], wait_after=False)
        print("检查换人窗口")
        while not self.op.checkCondition(self.op.getScreenCap().convert('L'),changeX,1200,115,changeX.size):
            self.useSkill(['m3'])
            time.sleep(1)
        print("换人")
        y = 350
        x = [140,340,540,740,940,1140]
        self.op.tap(x[m1-1],y)
        time.sleep(0.3)
        self.op.tap(x[m2-1],y)
        time.sleep(0.3)
        self.op.tap(640,620)
        self.op.tap(640,620)
        self.op.tap(640,620)
        time.sleep(3)
        # 检查换人错误
        print("检查换人错误")
        while self.checkState()!='skill':
            if self.op.checkCondition(self.op.getScreenCap().convert('L'),changeX,1200,115,changeX.size):
                self.op.tap(1220,140)
                time.sleep(0.5)
                self.op.tap(1190,310)
                self.changeMember(m1,m2)
            print("等待状态")
            
    def useSkill(self,skillList, wait_after=True):
        """
        执行技能序列
        s: 技能
        m: 御主技能
        123是从左到右的编号
        第一个数字是英灵，第二个数字是技能，第三个数字是目标
        """
        print("use skill")
        for op in skillList:
            self.waitUtilSkillReady()
            print("使用技能：%s"%op)
            if op[0] == 's':
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
        if wait_after:
            self.waitUtilSkillReady()
        
    
    def findSupport(self,supportList,target):
        # 判断当前助战列表有没有需要的目标
        print("find support")
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
        time.sleep(1)
        img = self.op.getScreenCap().convert("L")
        if checkCondition(img,confirmFresh,705,535,confirmFresh.size):
            # 刷新助战确认
            tap(840,560)
            print("刷新助战确认")
            time.sleep(1)
            return 
        
        
    def selectSupport(self,img = None):
        print("select support")
        if img is None:
            img = self.op.getScreenCap().convert("L")
        # 组合出需要找的助战图
        if checkCondition(img,refreshTooFast,510,533,refreshTooFast.size):
            # 刷新助战太快
            print("刷新太快了")
            tap(640,560)
            time.sleep(3)
            self.refreshSupport()
            return 
            
                
        print("搜索助战")
        supportList = crop(img,50,170,(216,550))
        found = False
        for people in self.supportImg:
            if found:
                break
            for peopleImg in self.supportImg[people]:
                found = self.findSupport(supportList,peopleImg)
                if found:
                    self.currentSupport = people
                    break
                
        # 没找到就向下滑
        if not found:
            excute("input swipe 690 700 690 500 300","adb shell")
            print("划一下")
            time.sleep(3)
            self.retryCount += 1
            if self.retryCount == 3:
                # 尝试3次就刷新
                self.refreshSupport()
                self.selectSupport()
                self.retryCount = 0
        else:
            time.sleep(1.5)
            
    def _waitUntil(self, condition, x, y, tapLoc = None, sleep=1):
        """
        wait util a target image shown in (x,y)
        will tap screen at tapLoc whiling waiting
        """
        print("waiting skill ready")
        while True:
            img = self.op.getScreenCap().convert('L')
            if self.op.checkCondition(img,condition, x, y, condition.size):
                return
            if tapLoc is not None:
                self.op.tap(*tapLoc)
            time.sleep(sleep)
    
    def waitUtilSkillReady(self):
        self._waitUntil(goBack, 1160, 670, (1130,600), 0.5)
        tap(1200,680)
        time.sleep(0.5)
    
                

class gameRunner:
    def __init__(self, con, battles):
        self.battles = battles
        self.con = con
        self.log_name = time.strftime("%m-%d_%H-%M-%S",time.localtime())
        if not os.path.exists("./log/%s"%self.log_name):
            os.mkdir("./log/%s"%self.log_name)
        
    def run(self):
        """
        完整的生命周期
        """
        while not self.con.finished:
            state = self.con.checkState()
            if state == 'selectBattle':
                print("select battle")
                self.con.selectBattle()
            if state == 'eatApple':
                print("eatApple")
                self.con.eatApple()
            if state == "selectSupport":
                print("选择助战")
                self.con.selectSupport()
            if state == 'startMission':
                print("开始任务")
                self.con.startMission()
            if state == "skill":
                #print("using skill")
                battle = self.con.getBattle()
                self.battles[battle-1](self.con)
                
            if state == "nextStep":
                img = self.con.op.getScreenCap()
                img.save("./log/%s/%s.png"%(self.log_name, time.strftime("%m-%d_%H-%M-%S",time.localtime())))
                self.con.nextStep()
            
            if state == "addFriend":
                self.con.refuse()
                
            if state == "wait":
                tap(970,90)
                tap(970,90)
                time.sleep(1)
        
if __name__ == '__main__':
    con = Controller({
            'apple':10,
            'support':['cba'],
            'cloth':None,
            'battle1':None,
            'battle2':None,
            'battle3':None,
            'offline':True
            })
    #test = Image.open('./img/test2.png')
    #con.analysis(test)
        
        