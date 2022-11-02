from email.charset import add_alias
from enum import IntEnum
from abc import abstractmethod

from vizdoom_player_action import * 
from draw_map import AccessMap
from vizdoom_object_data import *
import math
from time import time
import vizdoom as vzd
from random import choice


class Doom_FSM():
    def __init__(self, game:vzd.DoomGame):
        self.game = game
        self.map = AccessMap(self.game)
        self.screen_width = self.game.get_screen_width()
        self.screen_height = self.game.get_screen_height()
        self.able_shoot = False
        self.fov = 30
        self.priorweapon = [3,5,6]

        self.updateState(self.game.get_state())
        self.ResetAction()

    def updateState(self, state):
        self.state = state
        self.checkMyState()
        self.ResetAction()

        if self.ICanShoot():
            self.action[0] = True
            self.action[6] = True

        else:
            self.action[7] = True

            # self.action[choice([3,4,5,6,7,8])] = True

    def getAction(self):
        return self.action


    def checkMyState(self):
        GameVariable = self.state.game_variables
        self.location = list(map(int, GameVariable[0:3]))
        self.angle = GameVariable[3]
        self.health = GameVariable[4]
        self.armor = GameVariable[5]
        self.weapon = GameVariable[6]
        self.shotgun = GameVariable[7]
        self.rocket = GameVariable[8]
        self.plazma = GameVariable[9]
        print(self.angle)
    

    def ICanShoot(self):
        radar = [int((self.screen_width-self.fov)/2), int((self.screen_width+self.fov)/2)]
        EnemyPosition = self.GetEnemyPos()
        if len(EnemyPosition)>0:
            for enemy in EnemyPosition:
                enemy_name, enemy_x, enemy_width = enemy
                if (radar[0]<enemy_x<radar[1])or(radar[0]<enemy_x+enemy_width<radar[1]):
                    self.able_shoot = True
                    break
                else:
                    self.able_shoot = False
                    continue
        else:
            self.able_shoot = False
        
        return self.able_shoot

    def GetEnemyPos(self):
        enemy_name_list = ["Demon", "Zombieman", "ChaingunGuy", "ShotgunGuy", "HellKnight", "MarineChainsawVzd", "DoomPlayer"]
        AppearObject = self.state.labels
        EnemyPosition = []
        for o in AppearObject:
            if o.object_name in enemy_name_list:
                if o.object_name != 'DoomPlayer':
                    EnemyPosition.append([o.object_name, o.x, o.width])
                else:
                    if self.MeORNot(o): #This DoomPlayer is me
                        continue
                    else: # This DoomPlayer is not me
                        EnemyPosition.append([o.object_name, o.x, o.width])
            else:
                continue

        return EnemyPosition


    def getMap(self):
        map = self.game.map


    def MeORNot(self, object):
        Object_location = [int(object.object_position_x), int(object.object_position_y), int(object.object_position_z)]
        if Object_location==self.location:
            # print("0f0adf0a0fa")
            return True
        else:
            return False

    def setFov(self, fov):
        self.fov = fov

    def ResetAction(self):
        self.action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def getLocation(self):
        return self.location

