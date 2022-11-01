from pickletools import float8
from time import get_clock_info
from tkinter.messagebox import NO
from turtle import st
from winsound import PlaySound
import numpy as np
from vizdoom_object_name import *
import math

def dist(p1, p2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    return np.sqrt(np.sum(np.square(p1-p2)))




class ObjectData:
    def __init__(self, object):
        self.id = object.id
        self.object = object
        self.name = DoomObject(DoomObject.ToEnum(object.name))
        self.pos = (object.position_x, object.position_y)
        self.visible = False

class StateData:
    # Dict<ObjectName, List<object>>
    type_objects_dict = {}
    def __init__(self, state):
        self.id_object_dict = self.make_id_object_dict(state) # id-object 쌍 생성
        self.type_objects_dict = self.make_type_objects_dict(self.id_object_dict.values()) # type-object 쌍 생성
        
        self.set_visible_value(state) # 모든 객체에 visible 값 세팅
        self.set_dist_to_player() # 모든 객체에 player와의 거리 계산
        self.set_label_infor(state)


        self.player = self.get_object_date_list(name = DoomObject.DoomPlayer)[0]
        
    def set_label_infor(self, state): # visible의 경우 label 정보를 세팅해줌
        for label in state.labels:
            object = self.id_object_dict[label.object_id]
            object.x = label.x
            object.y = label.y
            object.w = label.width
            object.h = label.height

    def set_visible_value(self, state): # visible 변수 세팅
        for label in state.labels:
            self.id_object_dict[label.object_id].visible = True
    

    def set_dist_to_player(self): # state에 모든 object에 대해 player와의 거리를 구하고 세팅해준다.
        # Player 찾기
        player = None
        for object in self.id_object_dict.values():
            if object.name == DoomObject.DoomPlayer:
                player = object
                break
        
        for object in self.id_object_dict.values(): 
            object.dist_to_player = dist(object.pos, player.pos)

    def get_object_date_list(self, name = None, visible=None):
        objects = self.id_object_dict.values()

        # name에 맞는 object만 남기기
        if name is not None:
            target = []
            for o in objects:
                if o.name == name:
                    target.append(o)
            objects = target

        # visible조건에 맞는 object만 남기기
        if visible is not None:
            target = []
            for o in objects:
                if o.visible == visible:
                    target.append(o)
            objects = target
        
        return objects

    @staticmethod
    def make_id_object_dict(state):
        id_object_dict = {}
        for o in state.objects:
            id_object_dict[o.id] = ObjectData(o)
        return id_object_dict

    @staticmethod
    def make_type_objects_dict(objects):
        type_objects_dict = {}
        for object in objects:
            if object.name not in type_objects_dict:
                type_objects_dict[object.name] = []
            type_objects_dict[object.name].append(object)
        return type_objects_dict


class StateData2:

    def __init__(self, state):
        self.state = state
        self.player_id = None
        self.enemy_id_list = None
        self.closest_enomy_object_id = None
        self.id_object_dict = None # id 와 object 쌍 저장
        self.id_label_dict = None # id 와 label 쌍 저장
        self.enemy_label_id_list = None
        self.closest_enemy_label_id = None

    def get_player_id(self):
        if self.player_id == None:
            for object in self.state.objects:
                if object.name == "DoomPlayer":
                    self.player_id = object.id
                    break
        return self.player_id
    
    def is_enemy(self, id): # object가 적인지 판단.
        return self.get_object(id).name in enemy_name_list

    def get_enemy_id_list(self): # 존재하는 모든 적 object의 id 리스트 반환
        if self.enemy_id_list == None:
            enemy_id_list= []
            for object in self.state.objects:
                if self.is_enemy(object.id):
                    enemy_id_list.append(object.id)

            self.enemy_id_list = enemy_id_list

        return self.enemy_id_list

    def get_closest_enemy_object_id(self):
        if self.closest_enomy_object_id == None:
            min_dist = 10000000
            min_enemy_id = None
            for id in self.get_enemy_id_list():
                dist = self.get_dist_from_player(id)
                if dist < min_dist:
                    min_enemy_id = id
                    min_dist = dist
            self.closest_enomy_object_id = min_enemy_id
        
        return self.closest_enomy_object_id
                
    def get_dist_from_player(self, id):
        player = self.get_object(self.get_player_id())
        object = self.get_object(id)
        player_pos = (player.position_x, player.position_y)
        object_pos = (object.position_x, object.position_y)
        return dist(player_pos, object_pos)

    def dist(p1, p2):
        p1 = np.array(p1)
        p2 = np.array(p2)
        return np.sqrt(np.sum(np.square(p1-p2)))

    def get_id_object_dict(self):
        if self.id_object_dict == None:
            id_object_dict = {}
            for object in self.state.objects:
                id_object_dict[object.id] = object
            self.id_object_dict = id_object_dict

        return self.id_object_dict

    def get_id_label_dict(self):
        if self.id_label_dict == None:
            id_label_dict = {}
            for object in self.state.labels:
                id_label_dict[object.object_id] = object
            self.id_label_dict = id_label_dict

        return self.id_label_dict

    def get_object(self, id):
        id_object_dict = self.get_id_object_dict()
        return id_object_dict[id] if id in id_object_dict else None

    def get_label(self, id):
        id_label_dict = self.get_id_label_dict()
        return id_label_dict[id] if id in id_label_dict else None

    def get_enemy_label_id_list(self):
        if self.enemy_label_id_list == None:
            enemy_label_id_list = []
            for label in self.state.labels:
                if self.is_enemy(label.object_id):
                    enemy_label_id_list.append(label.object_id)
            self.enemy_label_id_list = enemy_label_id_list

        return self.enemy_label_id_list

    def get_closest_enemy_label_id(self):
        if self.closest_enemy_label_id is None:
            min_dist = 1000000000
            min_enemy_label_id = None
            for enemy_label_id in self.get_enemy_label_id_list():
                dist = self.get_dist_from_player(enemy_label_id)
                if dist < min_dist:
                    min_dist = dist
                    min_enemy_label_id = enemy_label_id
            self.closest_enemy_label_id = min_enemy_label_id
        return self.closest_enemy_label_id

    def get_x_pixel_dist(self, id): # 화면 상에서 object와 플레이어의 중심좌표 간의 거리
        object_label = self.get_label(id)
        player_label = self.get_label(self.get_player_id())
        if object_label is None:
            return None

        if player_label is None:
            return None

        # print("player_id: %s, player: %s, target: %s"%(str(self.get_player_id()), str(player_label), str(object_label)))
        return (object_label.x + object_label.width/2) - 1920/2
        # return (object_label.x + object_label.width/2) - (player_label.x+player_label.width/2)

    def is_in_shotting_effective_zone(self, id):

        x_pixel_dist = self.get_x_pixel_dist(id)
        if x_pixel_dist is None:
            return False
        # print(math.fabs(x_pixel_dist))
        print(math.fabs(x_pixel_dist), max(50, self.get_label(id).width))
        return math.fabs(x_pixel_dist) <= max(50, self.get_label(id).width) # 플레이어와 표적의 중심 좌표가 표적의 withd 보다 짧은가


def get_angle_from_player_to_direction(px, py, dx, dy): # player를 기준으로 (x, y)의 방향을 angle(0~359)로 반환

    # 상대 거리 좌표
    x_dist = dx - px
    y_dist = dy - py

    d = dist((dx, dy), (px, py))

    if x_dist == 0:
        if y_dist > 0:
            return 90
        else:
            return 270

    a = math.acos(x_dist/d)/math.pi*180
    if y_dist < 0:
        a =  360-a # x 축 대칭

    return a
    

