from email.charset import add_alias
from enum import IntEnum
from abc import abstractmethod
from examples.python.mh_test.cig_multiplayer import GameVariable

from vizdoom_player_action import * 
from draw_map import *
from vizdoom_object_data import *
import math
from time import time
import vizdoom as vzd



class Doom_FSM():
    def __init__(self, game:vzd.DoomGame):
        self.game = game
        self.screen_width = self.game.get_screen_width()
        self.screen_height = self.game.get_screen_height()
        self.updateState(self.game.get_state())

    def updateState(self, state):
        self.state = state
        self.whereAmI()


    def whereAmI(self):
        GameVariable = self.state.game_variables
        self.location = list(map(int, GameVariable))
    

    def ICanShoot(self, fov):
        radar = [int((self.screen_width-fov)/2), int((self.screen_width+fov)/2)]


    def GetEnemyPos(self):
        enemy_name_list = ["Demon", "Zombieman", "ChaingunGuy", "ShotgunGuy", "HellKnight", "MarineChainsawVzd", "DoomPlayer"]
        AppearObject = self.state.labels
        EnemyPosition = []
        for o in AppearObject:
            if o != 'DoomPlayer':
                EnemyPosition.append([(o.x-o.width)/2, (o.x+o.width)/2])
            else:
                self.MeORNot()

    def MeORNot(self, object):
        x, y, z = object.object_position_x, object.object_position_y, object.object_position_z
        GameVariable = self.state.game_variables
        if (int(x)==int(GameVariable[0]))&(int(y)==int(GameVariable[1]))&(int(z)==int(GameVariable[2])):
            return False
        else:
            return True






