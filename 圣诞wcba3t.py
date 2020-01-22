# -*- coding: utf-8 -*-

from controller import Controller, gameRunner


def battle1(con):
    con.useSkill(['s23'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])

def battle2(con):
    con.useSkill(['s112','s312','s23'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])

def battle3(con):
    con.useSkill(['s12','s32','s132','s332'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])
    
# 孔明
def battle2km(con):
    con.useSkill(['s13','s33','s312'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])

def battle3km(con):
    con.useSkill(['s32'])
    con.changeMember(3,5)
    con.useSkill(['s12','s112','s23','s332','s32'])
    con.attack()
    con.useBj([2])
    con.selectCard([1,2])

if __name__ == "__main__":
    setting = {
            'apple':60,
            'support':['km']
            }
    con = Controller(setting)
    runner = gameRunner(con, [battle1, battle2km, battle3km])
    runner.run()