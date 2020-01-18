# -*- coding: utf-8 -*-

from PIL import Image
import os
import time
from baseOp import baseOperator,crop,readAndConvert,excute
from collections import defaultdict
from ocr import send
import codecs

# 初始化小图
km1 = readAndConvert('./img/km1.png')
km2 = readAndConvert('./img/km2.png')
km3 = readAndConvert('./img/km3.png')
ml1 = readAndConvert('./img/ml1.png')
ml2 = readAndConvert('./img/ml2.png')
wc = readAndConvert('./img/wc.png') # 满破礼装
template = readAndConvert('./img/template.png') 
box = (0,0,157,126)

state_selectBattle = readAndConvert('./img/关卡选择.png')#80,20
state_eatApple = readAndConvert('./img/吃苹果.png')#520,585
state_support = readAndConvert('./img/助战选择标记.png')#1040,0

refreshTooFast = readAndConvert('./img/刷新太快.png')#510,533
confirmFresh = readAndConvert('./img/刷新确认.png')#705,535
startMission = readAndConvert('./img/开始任务.png')#1105,640

detailX = readAndConvert('./img/详情x.png')#1040,70
skillX = readAndConvert('./img/技能x.png')#380,400
changeX = readAndConvert('./img/换人x.png')#1200,115

#skillReady = readAndConvert('./img/attack.png') #1070,650
fightReady = readAndConvert('./img/fight.png')
nextStep = readAndConvert('./img/下一步.png') #1020,650

cards = []
for i in range(5):
    cards.append(Image.open('./img/card%dTitle.png'%(i+1)))

member = []
memberCards = {}
for m in member:
    memberCards[m] = Image.open('./img/cards/%s.png'%(m)).convert('L')


        
class Controller():
    def __init__(self,settings):
        self.settings = settings
        self.times = 0
        self.apple = 0
        self.retryCount = 0
        self.finished = False
        self.currentBattle = -1
        self.attackReady = False
        self.op = baseOperator()
        self.logFile = codecs.open('./log/log_%s.txt'%time.strftime('%m_%d_%H_%M_%S',time.localtime()),'a',encoding='utf-8')
        self.logPath = './log/%s/'%time.strftime('%m_%d_%H_%M_%S',time.localtime())
        os.mkdir(self.logPath)
        self.inBattle = False
        self.lastImg = None
        
        self.memberCheck = 3
        self.skillCheck = 3
        self.skillReady = readAndConvert('./img/skill/nt3.png')
        
        self.condition = {
            '1':False,
            '2':False,
            '3':False,
            'ab':False
        }
    
    def resetCondition(self):
        for con in self.condition:
            self.condition[con] = False
        self.memberCheck = 3
        self.skillCheck = 3
        self.skillReady = readAndConvert('./img/skill/nt3.png')
        
    def log(self,sentence):
        t = time.strftime('%H:%M:%S',time.localtime())
        self.logFile.write(t+" "+sentence+'\n')
    
    def finish(self):
        self.finished = True
        #os.popen('adb shell am force-stop com.bilibili.fatego')
        self.log("结束任务")
        self.logFile.close()
        print(time.strftime('%H:%M:%S',time.localtime()))
        print("结束任务")
    
    def run(self):
        while not self.finished:
            img = self.op.getScreenCap()
            self.analysis(img)
            time.sleep(0.2)

    def analysis(self,img = None):
        if img is None:
            img = self.op.getScreenCap()
        self.img = img
        img = img.convert('L')
        state = self.checkState(img)
        print("check state:",state)
        if state == "attack":
            self.attack(self.img)
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
        if state == "detail error" or state == "skill error":
            self.op.tap(60,300)
            time.sleep(0.2)
            self.op.tap(60,300)
            return 
        if state == 'changeError':
            self.op.tap(1220,135)
            time.sleep(0.3)
            self.changeMember(3,4)
            return
        if state == "nextStep":
            print("下一步")
            self.nextStep()
            return
        if state == "wait":
            self.op.tap(970,90)
            self.op.tap(970,90)
            return
        
    def nextStep(self):
        print("点击下一步")
        self.inBattle = False
        img = self.op.getScreenCap()
        img.save(self.logPath+time.strftime('%m_%d_%H_%M_%S',time.localtime())+".png")
        self.op.tap(1100,680)
        excute("adb forward tcp:9090 tcp:7070")
        time.sleep(5)
        
    def checkState(self,img = None):
        if img is None:
            img = self.op.getScreenCap().convert('L')
        if self.inBattle:
            # 检查skill
            if self.op.checkCondition(img,skillX,380,400,skillX.size):
                return "skill error"
            t = self.op.cutSkill(img,self.memberCheck,self.skillCheck)
            self.lastImg = t
            if self.op.checkCondition(t,self.skillReady,0,0,t.size):
                return "skill"
            # 检查选卡
            t = crop(img,1060,70,(140,30)).convert('L')
            t = t.point(lambda x:0 if x<200 else x)
            if self.op.checkCondition(t,fightReady,0,0,t.size):
                return "attack"
            if self.op.checkCondition(img,detailX,1040,70,detailX.size):
                return "detail error"
            if self.op.checkCondition(img,nextStep,1020,650,nextStep.size):
                return "nextStep"
            return "wait"
        if self.op.checkCondition(img,state_selectBattle,80,20,state_selectBattle.size):
            return "selectBattle"
        if self.op.checkCondition(img,state_eatApple,520,585,state_eatApple.size):
            return "eatApple"
        if self.op.checkCondition(img,state_support,1040,0,state_support.size):
            return "selectSupport"
        if self.op.checkCondition(img,startMission,1105,640,startMission.size):
            return "startMission"
        return "wait"
                
    def getCardList(self,battle,img):
        if battle == 1:
            memberCards_ = {}
            for m in memberCards:
                if m in ['北斋','阿比','大英雄']:
                    memberCards_[m] = memberCards[m]
        elif battle == 2:
            memberCards_ = {}
            for m in memberCards:
                if m in ['北斋','阿比','孔明']:
                    memberCards_[m] = memberCards[m]
        else:
            memberCards_ = {}
            for m in memberCards:
                if m in ['北斋','阿比','孔明']:
                    memberCards_[m] = memberCards[m]
                    
        print("识别英灵色卡")
        cardList = self.op.recognizeCard(memberCards = memberCards_,img = img)
        print(cardList)
        #self.log('星星：'+' '.join([str(s) for s in star]))
        self.log(' '.join(cardList))
        card = []
        cardCount = defaultdict(lambda : 0)
        colorCount = defaultdict(lambda : 0)
        for i,c in enumerate(cardList):
            temp = {}
            c = c.split('_')
            temp['member'] = c[0]
            temp['color'] = c[1]
            temp['loc'] = i+1
            cardCount[c[0]] += 1
            colorCount[c[1]] += 1
            card.append(temp)
        return card
    
    def attack(self,img):
        self.attackReady = False
        self.log("开始攻击")
        print("开始攻击")
        battle = self.currentBattle
        print("battle: %d"%battle)
        #star = self.op.getStars(img)
    
        if battle == 1:
            print("尼托宝具")
            self.useBj(3)
            
        if battle == 2:
            print("尼托宝具")
            self.useBj(3)
                    
        if battle == 3:
            self.changeTarget(1)
            print("三藏宝具")
            self.useBj(1)
            print("海伦娜宝具")
            self.useBj(2)


        # 以防万一全选一次卡
        time.sleep(0.3)
        for i in range(5):
            self.selectCard(i+1)
            time.sleep(0.3)
        
        time.sleep(2)
            
                
            
    def excuteSillList(self,skillList):
        print("执行技能序列")
        time.sleep(1)
        for s in skillList:
            self.skill(s)
            time.sleep(2)
            state = self.checkState()
            while state!='skill':
                if state == "detail error" or state =="skill error":
                    self.op.tap(60,300)
                    self.op.tap(60,300)
                state = self.checkState()
                print("等待状态")
    
    def useSkill(self,img):
        self.log("使用技能")
        battle = self.op.getBattleByImg(img)
        print("battle %d"%battle)
        self.log("进入battle%d"%battle)
        if battle != self.currentBattle:
            if battle == 1:
                skillList = ['j13','j21','j23','j31']
                self.excuteSillList(skillList)
                        
            if battle == 2:
                skillList = ['j32']
                self.excuteSillList(skillList)
            
            if battle == 3:
                skillList = ['j11','j22','m12']
                self.excuteSillList(skillList)
                
            self.currentBattle = battle
        else:
            if self.checkState()!='attack':
                self.attackReady = True
                self.op.tap(1130,600)
                time.sleep(1)
            
    
    def startMission(self):
        self.op.tap(1200,680)
        self.currentBattle = -1
        self.times += 1
        self.log("第%d次打本"%self.times)
        print(time.strftime('%H:%M:%S',time.localtime()))
        print("第%d次打本"%self.times)
        self.inBattle = True
        self.resetCondition()
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
            self.op.tap(950,180)
            time.sleep(1.5)
            
    def eatApple(self,img):
        eat = False
        if self.settings['apple']!=-1:
            # 按照苹果数量来打本
            if self.apple < self.settings['apple']:
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
            self.log("第%d次吃苹果"%self.apple)
            print("第%d次吃苹果"%self.apple)
            excute("input swipe 640 360 640 200 300","adb shell")
            time.sleep(0.8)
            excute("input swipe 640 360 640 200 300","adb shell")
            time.sleep(0.8)
            if self.settings['apple_prior'] == 1:
                # 金苹果
                self.op.tap(380,200)
            if self.settings['apple_prior'] == 2:
                # 银苹果
                self.op.tap(380,350)   
            if self.settings['apple_prior'] == 3:
                # 铜苹果
                self.op.tap(380,500)
            # 确认吃苹果
            time.sleep(1)
            self.op.tap(840,560)
            
            
    def selectCard(self,cardNum):
        y = 400
        x_loc = {1:130,2:380,3:640,4:900,5:1160}
        x = x_loc[cardNum]
        self.op.tap(x,y)
    
    def useBj(self,bjNum):
        time.sleep(1.5)
        y = 220
        x_loc = {1:410,2:640,3:880}
        x =x_loc[bjNum]
        self.op.tap(x,y)
            
    def changeTarget(self,target):
        print("change target")
        y = 40
        x_loc = {1:45,2:285,3:525}
        x =x_loc[target]
        self.op.tap(x,y)
        time.sleep(0.2)
        self.op.tap(x,y)
        
    def changeMember(self,m1,m2):
        self.skill('m3')
        print("检查换人窗口")
        while not self.op.checkCondition(self.op.getScreenCap().convert('L'),changeX,1200,115,changeX.size):
            self.skill('m3')
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
            
    def skill(self,op):
        print("使用技能：%s"%op)
        if op[0] == 'j':
            target = op[1:3]
            y = 580
            user = {'1':70,'2':380,'3':700}
            offset = {'1':0,'2':95,'3':190}
            x = user[target[0]] + offset[target[1]]
            self.op.tap(x,y)
            if len(op) == 4:
                y = 450
                target = {'1':330,'2':660,'3':950}
                x = target[op[3]]
                time.sleep(0.5)
                self.op.tap(x,y)
            #time.sleep(1.5)
            return 
        
        if op[0] == 'm':
            self.op.tap(1190,310)
            time.sleep(0.8)
            y = 320
            target = {'1':910,'2':995,'3':1080}
            x = target[op[1]]
            self.op.tap(x,y)
            if len(op) == 3:
                y = 450
                target = {'1':330,'2':660,'3':950}
                x = target[op[2]]
                time.sleep(0.5)
                self.op.tap(x,y)
            #time.sleep(1.5)
            return 
    
    def findSupport(self,supportList,target):
        # 判断当前助战列表有没有需要的目标
        x,y,dis = self.op.findSmall(supportList,target,10)
        if dis<40:
            print("发现目标!")
            self.op.tap(int(50+x+target.size[0]/2),int(170+y+target.size[1]/2))
            self.retryCount = 0
            return True
        return False
    
    def refreshSupport(self):
        # 刷新助战列表
        print("刷新助战")
        self.op.tap(840,128)
        
    def selectSupport(self,img):
        # 组合出需要找的助战图
        if self.op.checkCondition(img,refreshTooFast,510,533,refreshTooFast.size):
            # 刷新助战太快
            print("刷新太快了")
            self.op.tap(640,560)
            time.sleep(3)
            self.refreshSupport()
            return 
            
            
        if self.op.checkCondition(img,confirmFresh,705,535,confirmFresh.size):
            # 刷新助战确认
            self.op.tap(840,560)
            self.log("刷新助战")
            print("刷新助战确认")
            time.sleep(2)
            return 
                
        print("搜索助战")
        img = self.op.getScreenCap().convert('L')
        supportList = crop(img,50,170,(216,550))
        found = False
        supportTarget = [km1,km2,km3,ml1,ml2]
        #supportTarget = [xh]
        lzTarget = [wc]
        for sup in supportTarget:
            if found:
                break
            for lz in lzTarget:
                template.paste(sup,box)
                template.paste(lz,(0,126,157,126+lz.size[1]))
                found = self.findSupport(supportList,template)
                if found:
                    break

        # 没找到就向下滑
        if not found:
            excute("input swipe 690 700 690 500 300","adb shell")
            print("划一下")
            time.sleep(1)
            self.retryCount += 1
            if self.retryCount >= 5:
                # 尝试x次就刷新
                self.refreshSupport()
                self.retryCount = 0
        else:
            time.sleep(1.5)
        
        
if __name__ == '__main__':
    #con = Controller('skm')
    #test = Image.open('./img/test2.png')
    #con.analysis(test)
    settings = {
        'apple':-1,
        'times':7,
        'apple_prior':3
    }
    con = Controller(settings)
    con.inBattle = False
    con.run()
        