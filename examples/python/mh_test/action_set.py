from abc import abstractmethod
from typing import overload
from vizdoom_player_action import * 
from draw_map import *
from vizdoom_object_data import *

class DeathmatchAction:
    def set_angle(stateData, angle):
        action = make_into_doom_action({
            PlayerAction.rotateX: stateData.player.object.angle-angle
        })
        return (action, True)

    def MoveTo(stateData, pos):
        make_into_doom_action({
            # PlayerAction.Atack:True,
            PlayerAction.MoveLeft: (map[y+1,x] < map[y,x]),
            PlayerAction.MoveRight: (map[y-1,x] < map[y,x]),
            PlayerAction.MoveBack: (map[y,x-1] < map[y,x]),
            PlayerAction.MoveFront: (map[y,x+1] < map[y,x]),
        })
        pass



    # def get_map(section)
    #     if section == "Top":
    #         make_direction_map(access, ((500+1200)//8, (500+500)//8))
    #     else

class AbstractActioner:
    @ abstractmethod
    def do(self): # 한 스텝 수행 후 종료 여부 반환
        pass

    def do_all(self): # 액션의 전체 과정을 수행
        while True:
            if self.do():
                break

class RotateTo(AbstractActioner):
    def __init__(self, game, angle):
        self.game = game
        self.angle = angle

    def do(self):
        self.game.make_action(make_into_doom_action({
                PlayerAction.rotateX: StateData(self.game.get_state()).player.object.angle-self.angle
        }))
        return True


class MoveToActioner(AbstractActioner):
    
    def __init__(self, game, target_pos): 
        access_map = AccessMap(game.get_state())
        self.map = HeightMap(access_map, target_pos)



    def do(self):
        if map[(y,x)] < 3:
            return True
        else:
            RotateTo(self.game, 0).do_all() # 각도를 0으로
            stateData = StateData(self.game.get_state())
            x = int(stateData.player.pos[0])
            y = int(stateData.player.pos[1])

            right = map[(y-1,x)] < map[(y,x)]
            left = map[(y+1,x)] < map[(y,x)] and not right
            front = (map[(y,x+1)] < map[(y,x)])
            back = (map[(y,x-1)] < map[(y,x)]) and not front

            self.game.make_action(make_into_doom_action({
                PlayerAction.MoveFront: front,
                PlayerAction.MoveBack: back,
                PlayerAction.MoveRight: right,
                PlayerAction.MoveLeft: left
            }))
            return False

