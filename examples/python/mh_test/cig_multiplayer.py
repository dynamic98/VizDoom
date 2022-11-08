#!/usr/bin/env python3

#####################################################################
# This script presents how to join and play a deathmatch game,
# that can be hosted using cig_multiplayer_host.py script.
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
from vizdoom_object_state_analysis import *
from vizdoom_player_fsm import Doom_FSM

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


game = vzd.DoomGame()

# Use CIG example config or your own.
scenarios_path = '../../../scenarios'
game.load_config(os.path.join(scenarios_path, "deathmatch_multi.cfg"))


# game.set_doom_map("map01")  # Limited deathmatch.
#game.set_doom_map("map02")  # Full deathmatch.

# Join existing game.
game.add_game_args("-join 127.0.0.1 -port 5029") # Connect to a host for a multiplayer game.

# Name your agent and select color
# colors: 0 - green, 1 - gray, 2 - brown, 3 - red, 4 - light gray, 5 - light brown, 6 - light red, 7 - light blue
game.add_game_args("+name AI +colorset 0")

# During the competition, async mode will be forced for all agents.
# game.set_mode(Mode.PLAYER)

game.set_mode(vzd.Mode.ASYNC_PLAYER)
# game.set_mode(vzd.Mode.ASYNC_SPECTATOR)

# game.set_window_visible(False)

game.set_objects_info_enabled(True)
game.set_sectors_info_enabled(True)
game.set_labels_buffer_enabled(True)

game.clear_available_game_variables()
game.add_available_game_variable(vzd.GameVariable.POSITION_X)
game.add_available_game_variable(vzd.GameVariable.POSITION_Y)
game.add_available_game_variable(vzd.GameVariable.POSITION_Z)
game.add_available_game_variable(vzd.GameVariable.ANGLE)

game.add_available_game_variable(vzd.GameVariable.HEALTH)
game.add_available_game_variable(vzd.GameVariable.ARMOR)
game.add_available_game_variable(vzd.GameVariable.SELECTED_WEAPON)

game.add_available_game_variable(vzd.GameVariable.AMMO3)
game.add_available_game_variable(vzd.GameVariable.AMMO5)
game.add_available_game_variable(vzd.GameVariable.AMMO6)

actions = [[True, False, False], [False, True, False], [False, False, True]]

game.init()
myDoomFSM = Doom_FSM(game, playstyle='aggressive')
# Three example sample actions
# actions = [[1,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0]]

# Get player's number
player_number = int(game.get_game_variable(vzd.GameVariable.PLAYER_NUMBER))
last_frags = 0
die_count = 0
# aimActioner = AimActioner(game)
# attackActioner = AttackActioner(game)
# moveActionerList = []


# # Play until the game (episode) is over.
# stateData = StateData2(game.get_state())
# # print(-stateData.get_object(stateData.get_player_id()).angle)
# game.make_action(make_into_doom_action({PlayerAction.rotateX: stateData.get_object(stateData.get_player_id()).angle}))
#
# aimActioner = AimActioner(game)
# attackActioner = AttackActioner(game)
idx = 0
while not game.is_episode_finished():
    
    state = game.get_state()
    myDoomFSM.updateState(state)

    game.make_action(myDoomFSM.getAction())
    # print(myDoomFSM.getAction())

    if keyboard.is_pressed("Enter"):    
        print(myDoomFSM.getLocation())


    frags = game.get_game_variable(vzd.GameVariable.FRAGCOUNT)
    if frags != last_frags:
        last_frags = frags
        print("Player " + str(player_number) + " has " + str(frags) + " frags.")
        # print(last_frags + ' kills and' + die_count + ' deaths')
        print(str(frags) + ' kills and  ' + str(die_count) + ' deaths')



    # Check if player is dead
    if game.is_player_dead():
        die_count+=1
        print("Player " + str(player_number) + " died.")
        print(str(frags) + ' kills and  ' + str(die_count) + ' deaths')
        # Use this to respawn immediately after death, new state will be available.
        game.respawn_player()
        myDoomFSM.ResetFSM()


game.close()
