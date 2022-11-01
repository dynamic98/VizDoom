from pickletools import float8
from pydoc import visiblename
from tkinter.messagebox import NO
from turtle import st
import numpy as np
from vizdoom_object_data import *
from vizdoom_object_name import *
import math
enemy_name_list = [DoomObject.Demon, DoomObject.Zombieman, DoomObject.ChaingunGuy, DoomObject.ShotgunGuy, DoomObject.HellKnight, DoomObject.MarineChainsawVzd]

def is_any_enemy_ahead(stateData):
    enemy_object_list = []
    for object in stateData.get_object_date_list(visible = True):
        if is_enemy(object) == True:
            return True
    return False

def extract_enemy(objects):
    list = []
    for o  in objects:
        if is_enemy(o):
            list.append(o)
    return list
    
def is_enemy(object):
    return object.name in enemy_name_list


def get_closest_object(list):
    target = None
    dist = 10000000

    for o in list:
        if o.name == DoomObject.DoomPlayer:
            continue
        if o.dist_to_player < dist:
            dist = o.dist_to_player
            target = o

    return target

def is_in_shot_range(object, player): # 쏘면 맞는 위치인가?
    if object.visible:
        x = (object.x + object.w/2)
        print(x, player.x + player.w/2)
        return math.fabs(x-(player.x + player.w/2)) < object.w/2*0.8
    return False

def is_left(object, player):
    if object.visible == False:
        raise Exception('object가 visible일 때 만 수행 가능') 
    return (object.x + object.w/2) < (player.x+player.w/2)


def is_right(object, player):
    if object.visible == False:
        raise Exception('object가 visible일 때 만 수행 가능') 
    return (player.x+player.w/2) < (object.x + object.w/2)


def get_pos_x(object, player):
    if object.visible == False:
        raise Exception('object가 visible일 때 만 수행 가능') 
    return (object.x + object.w/2) - (player.x+player.w/2)