from multiprocessing import pool
from os import access
from tkinter.messagebox import NO
import numpy as np
import keyboard
from PIL import Image
import matplotlib.pyplot as plt


def draw_wall(map, origin, x1, y1, x2, y2, v):

    if x1 == x2:
        x = int(origin[0]+x1)
        from_y = int(origin[1] + min(y1, y2))
        to_y   = int(origin[1] + max(y1, y2))
        for y in range(from_y, to_y+1):
            map[y, x] = v
    else:
        y = int(origin[1]+y1)
        from_x = int(origin[0] + min(x1, x2))
        to_x =   int(origin[0] + max(x1, x2))
        for x in range(from_x, to_x+1):
            map[y, x] = v


def make_direction_map(access, target):
    map = np.ones(shape=access.shape)*10000

    work_list = []
    work_list.append((target[0], target[1], 1))

    while(len(work_list) != 0):
        x, y, l = work_list[0]
        work_list.pop(0)
        if not ((0 <= x and x < map.shape[0]) and (0 <= y and y <map.shape[1])):
            continue
        elif access[y, x] == 0:
            continue
        elif map[y, x] <= l:
            continue
        else:
            map[y, x] = l
            work_list.append((x+1, y, l+1))
            work_list.append((x-1, y, l+1))
            work_list.append((x, y+1, l+1))
            work_list.append((x, y-1, l+1))

    return map

        

def max_pooling(arr):
    x, y = arr.shape
    new_x, new_y = x//2, y//2
    arr = np.min(arr.reshape(new_x, 2, new_y, 2), axis = (1, 3))
    return arr

def get_map(state):
    for o in state.objects:
        if o.name == "DoomPlayer":
            plt.plot(o.position_x, o.position_y, color='green', marker='o')
        else:
            plt.plot(o.position_x, o.position_y, color='red', marker='o')

    for s in state.sectors:
        for l in s.lines:
            if l.is_blocking:
                plt.plot([l.x1, l.x2], [l.y1, l.y2], color='black', linewidth=2)

    return plt

def spread_height(value_map, x, y, height, term, n): # (x, y)에서 주변 n개 칸 까지 max값에서 term씩 줄어드는 값을 더해준다.
    for dy in range(max(0,-n), min(value_map.shape[0], n+1)):
        for dx in range(max(0,-n), min(value_map.shape[1], n+1)):
            dist = abs(dx) + abs(dy)
            if dist <= n:
                value_map[y+dy][x+dx] += height-dist*term

class AccessMap:

    def __init__(self, game, adjust_pos = (500, 500), pooling = (8, 8)): # adjust_pos: 원점 좌표 => 음수인 좌표를 모두 양수로 만들기 위함
        self.adjust_pos = adjust_pos
        self.pooling = pooling

        # 맵 생성
        state = game.get_state()
        map = np.ones(shape=(2000, 2000))            # game에서 맵의 크기를 확인하고 세팅하는 코드로 수정 필요
        # 0: accessable, 1: unaccessable


        # 벽 그리기
        for s in state.sectors:
            for l in s.lines:
                if l.is_blocking:
                    draw_wall(map, self.adjust_pos, l.x1, l.y1, l.x2, l.y2, 0)

        # 벽 주변 미세 높이 값 저장 맵 생성

        self.wall_around_height_map = np.zeros(shape=map.shape)
        for y in range(map.shape[0]):
            for x in range(map.shape[1]):
                if map[y][x] == 0:
                    pass
                    #spread_height(self.wall_around_height_map, x, y, 100, 1, 50)

        # pil_image=Image.fromarray(self.wall_around_height_map)
        # pil_image.show()
        

        # 축소 8x8 -> 1x1
        map = max_pooling(map)
        map = max_pooling(map)
        map = max_pooling(map)

        # 벽 키우기(두껍게)
        w = 1 # 두깨
        for y in range(map.shape[0]):
            for x in range(map.shape[1]): 
                if map[y, x] == 0:
                    for a in range(-w, w+1, 1):
                        for b in range(-w, w+1, 1):
                            if  (0 <= y+a) and (y+a < map.shape[0]) and (0 <= x+b) and (x+b < map.shape[1]):
                                if map[y+a, x+b] != 0: # 기존에 벽이 아닌 경우
                                    map[y+a, x+b] = -1
                                    

        for y in range(map.shape[0]):
            for x in range(map.shape[1]):
                if map[y, x] == -1:
                    map[y, x] = 0

        # static 변수에 저장
        self.map = map
        self.shape = self.map.shape


    def show(self):
        pil_image=Image.fromarray(self.map)
        pil_image.show()

    def get_map_pos(self, origin_pos): # 원래 좌표를 맵 위로 사상하여 반환 (평행 이동 -> 축소)
        # x축의 축소 비율이 a일 때 new_x=x//a, rest_ratio_x=나머지/a 이다.

        new_x = (origin_pos[0]+self.adjust_pos[0])//self.pooling[0]
        new_y = (origin_pos[1]+self.adjust_pos[1])//self.pooling[1]
        rest_x = ((origin_pos[0]+self.adjust_pos[0])%self.pooling[0])/self.pooling[0]
        rest_y = ((origin_pos[1]+self.adjust_pos[1])%self.pooling[1])/self.pooling[1]

        return (new_x, new_y, rest_x, rest_y)


class HeightMap: # map에서 높이 값을 표현(벽은 높이가 무한대라 가정)

    map = None
    adjust_pos = None
    pooling = None

    def __init__(self, access_map, target_pos):

        self.adjust_pos = access_map.adjust_pos
        self.pooling = access_map.pooling
        self.shape = access_map.shape
        self.access_map = access_map
        self.map = np.ones(shape=access_map.shape)*10000

        work_list = []
        map_pos = access_map.get_map_pos(target_pos)
        work_list.append((map_pos[0], map_pos[1], 1))
        
        while(len(work_list) != 0):
            x, y, l = work_list[0]
            
            work_list.pop(0)
            if not ((0 <= x and x < self.map.shape[1]) and (0 <= y and y <self.map.shape[0])):
                continue
            elif access_map.map[y, x] == 0:
                continue
            elif self.map[y, x] <= l:
                continue
            else:
                self.map[y, x] = l
                work_list.append((x+1, y, l+3))
                work_list.append((x-1, y, l+3))
                work_list.append((x, y+1, l+3))
                work_list.append((x, y-1, l+3))

        # 벽 키우기(두껍게)
        # w = 2 # 두깨
        # add_map = np.ones(shape=self.map.shape)
        # for y in range(add_map.shape[0]):
        #     for x in range(add_map.shape[1]): 
        #         if access_map.map[y, x] == 0: # 벽인 경우
        #             for a in range(-w, w+1, 1):
        #                 for b in range(-w, w+1, 1):
        #                     if  (0 <= y+a) and (y+a < add_map.shape[0]) and (0 <= x+b) and (x+b < add_map.shape[1]):
        #                         add_map[y+a, x+b] += (10-abs(max(a, b)))*30
        # self.map += add_map

    def __getitem__(self, pos):
        (x, y, dx, dy) = self.access_map.get_map_pos(pos)
        # print(x, y, dx, dy)

        dist_x = self.map[y, x+1] - self.map[y, x]
        dist_y = self.map[y+1, x] - self.map[y, x]

        dx = dist_x*dx
        dy = dist_y*dy

        return self.map[y, x] + dx + dy + self.access_map.wall_around_height_map[pos[1]][pos[0]]

    def show(self):
        pil_image=Image.fromarray(self.map)
        pil_image.show()