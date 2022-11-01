#!/usr/bin/env python3

#####################################################################
# This script presents SPECTATOR mode. In SPECTATOR mode you play and
# your agent can learn from it.
# Configuration is loaded from "../../scenarios/<SCENARIO_NAME>.cfg" file.
# 
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from argparse import ArgumentParser
from multiprocessing.util import close_all_fds_except
import os
from pydoc import ispackage
from time import sleep
from turtle import st
from matplotlib.axis import Tick
import vizdoom as vzd
from PIL import Image
from random import choice
import keyboard
import matplotlib.pyplot as plt
import numpy as np
from vizdoom_object_data import *
from vizdoom_player_action import * 
DEFAULT_CONFIG = os.path.join(vzd.scenarios_path, "deathmatch.cfg")

from vizdoom_object_state_analysis import *



def IsThereTargetInMySight(state, name):
    for label in state.labels:
        if label.object_name == name:
            return True
    return False

def GetAllObjectIdListInView(state, name):
    id_list = []
    for label in state.labels:
        if label.object_name == name:
            id_list.append(label.object_id)
    return id_list

def GetClosestObjectId(state, id_list):
    min_dist = 1000000
    min_id = None
    # for id in id_list:
    #     if label.object_name == name:
    #         return label.x + label.width/2
    print(state.objects)
    return None


def OrganizeObjectInfor(objects):
    dict = {}
    for o in state.objects: # 동작 가능 - 존재하는 모든 오브젝트의 정보 반환
        if o.name not in dict:
            dict[o.name] = 0
        dict[o.name] += 1
    return dict

###############################################

action1 = make_into_doom_action({
    PlayerAction.Atack:False,
    PlayerAction.rotateX: 5
})

action2 = make_into_doom_action({
    PlayerAction.Atack:True,
    PlayerAction.rotateX: 5
})

action3 = make_into_doom_action({
    PlayerAction.Atack:True,
    PlayerAction.MoveFront:True,
    PlayerAction.rotateX: 3
})

action4 = make_into_doom_action({
    PlayerAction.Atack:True,
    PlayerAction.MoveFront:True,
    PlayerAction.rotateX: -3
})

if __name__ == "__main__":
    parser = ArgumentParser("ViZDoom example showing how to use SPECTATOR mode.")
    parser.add_argument(dest="config",
                        default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../../scenarios/*cfg for more scenarios.")
    args = parser.parse_args()
    game = vzd.DoomGame()

    # Choose scenario config file you wish to watch.
    # Don't load two configs cause the second will overrite the first one.
    # Multiple config files are ok but combining these ones doesn't make much sense.

    game.load_config(args.config)

    # Enables freelook in engine
    game.add_game_args("+freelook 1")

    game.set_screen_resolution(vzd.ScreenResolution.RES_1920X1080)
    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    


    game.set_objects_info_enabled(True)
    game.set_sectors_info_enabled(True)
    game.set_labels_buffer_enabled(True)

    game.clear_available_game_variables()
    game.add_available_game_variable(vzd.GameVariable.POSITION_X)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Y)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Z)

    game.set_mode(vzd.Mode.SPECTATOR) # 동작을 직접 넣을 거면 실행 x

    actions = [[True, False, False], [False, True, False], [False, False, True]]

    game.init()

    game.new_episode()

    while not game.is_episode_finished():
        state = game.get_state()
        game.advance_action() # 이거 있어야 조작 가능
        
        stateData = StateData2(state)
        closest_enemy_label = stateData.get_closest_enemy_label_id()
        if closest_enemy_label is not None:
            print(closest_enemy_label.x + closest_enemy_label.width/2, closest_enemy_label.y + closest_enemy_label.height/2)



        if keyboard.is_pressed("Enter"):    
            print("State: %s" % str(state.number))
            while keyboard.is_pressed("Enter"):
                continue
        

    game.close()

