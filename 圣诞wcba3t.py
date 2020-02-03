# -*- coding: utf-8 -*-

from controller import Controller, gameRunner


def battle1(con):
    con.useSkill(['s23'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])

def battle2(con):
    con.useSkill(['s132','s12','s113'])
    con.changeMember(1,4)
    con.useSkill(['s21','s132'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])

def battle3(con):
    con.useSkill(['s332','s12','s32','s21'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])
    
def battle1km(con):
    con.useSkill(['s33','s32','s311'])
    con.attack()
    con.useBj([1])
    con.selectCard([1,2])
    
def battle2km(con):
    con.useSkill(['s13','m1'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])

def battle3km(con):
    con.changeMember(3,4)
    con.useSkill(['s33','s32','s312','s23','s21'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])
    

if __name__ == "__main__":
    setting = {
            'times':1,
            'support':['cba'],
            'offline':True
            }
    con = Controller(setting)
    runner = gameRunner(con, [battle1, battle2, battle3])
    runner.run()