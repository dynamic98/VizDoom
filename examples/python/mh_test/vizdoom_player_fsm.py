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
    def __init__(self, game:vzd.DoomGame, playstyle):
        self.game = game
        self.screen_width = self.game.get_screen_width()
        self.screen_height = self.game.get_screen_height()
        self.able_shoot = False
        self.move_finished = True
        self.roam_finished = False
        self.now_sector = 'center'
        self.prev_sector = 'center'
        self.play_style = playstyle
        self.PlayerStyle()
        self.fov = 30
        self.idx = 0
        self.idx2 = 0
        # self.idx = choice(list(range(0,8)))
        self.SetSectorClass()

        self.updateState(self.game.get_state())
        self.ResetAction()

    def ResetFSM(self):
        self.now_sector = 'center'
        self.idx2 = 0
        self.updateState(self.game.get_state())
        self.ResetAction()


    def updateState(self, state):
        self.state = state
        self.MH_state = StateData2(self.state)
        self.checkMyState()
        self.ResetAction()
        self.OptimalWeapon() # plazma > shotgun > rocket > else
        self.OptimalAction()

    def OptimalAction(self):
        if self.play_style == 'aggressive':
            self.autoAim('super')
            if self.ICanShoot():
                self.Shot()
            # LeftAmmo = self.plazma
            if self.weapon!=6.0:
                # Low AMMO
                self.now_sector = 'weapon'
                self.ResetIdx2()

                if self.idx%2>0:
                    sector_list = [self.section_topright, self.section_topleft]
                else:
                    sector_list = [self.section_bottomleft, self.section_bottomright]

                idx = self.idx2%(len(sector_list))
                self.MoveSector(sector_list[idx])

            elif self.health < self.Threshold_health:
                # Low Health
                self.now_sector = 'health'
                self.ResetIdx2()
               
                if self.idx%2>0:
                    sector_list = [self.section_righttop, self.section_rightbottom]
                else:
                    sector_list = [self.section_leftbottom, self.section_lefttop]
                idx = self.idx2%(len(sector_list))
                self.MoveSector(sector_list[idx])

            else:
                self.ResetIdx2()
                # Fine
                self.idx+=1
                sector_list = [ self.section_centertop, self.section_centerleft, self.section_centerbottom, self.section_centerright]
                idx = self.idx2%(len(sector_list))
                self.MoveSector(sector_list[idx])
            
            self.prev_sector = self.now_sector
            

   #############################################################                     
        elif self.play_style == 'runner':
            self.autoAim('super')
            if self.ICanShoot():
                self.Shot()
            sector_list = [self.section_topright, self.section_topleft, self.section_centertop, self.section_centerleft, self.section_centerbottom, self.section_centerright,
            self.section_lefttop, self.section_leftbottom, self.section_centerbottom, self.section_bottomleft, self.section_bottomright,
            self.section_centerright, self.section_rightbottom, self.section_righttop, self.section_centertop]
            idx = self.idx2%(len(sector_list))
            self.MoveSector(sector_list[idx])


   #############################################################                     

        elif self.play_style == 'aimer':
            self.autoAim('super')
            if self.ICanShoot():
                self.Shot()
            sector_list = [self.section_topright, self.section_topleft, 
                        self.section_centertop, self.section_centerleft, self.section_centerbottom, self.section_centerright,
                        self.section_bottomleft, self.section_bottomright,
                        self.section_centerright, self.section_centertop, self.section_centerleft, self.section_centerbottom]
            idx = self.idx2%(len(sector_list))
            self.MoveSector(sector_list[idx])


        elif self.play_style == 'defender':
            self.autoAim('super')
            if self.ICanShoot():
                self.Shot()
            sector_list = [self.section_topright, self.section_topleft, 
                        self.section_lefttop, self.section_leftbottom, self.section_lefttop, self.section_leftbottom,
                        self.section_lefttop, self.section_leftbottom, self.section_lefttop, self.section_leftbottom,
                        self.section_lefttop, self.section_leftbottom, self.section_lefttop, self.section_leftbottom,
                        self.section_bottomleft, self.section_bottomright,
                        self.section_rightbottom, self.section_righttop, self.section_rightbottom, self.section_righttop,
                        self.section_rightbottom, self.section_righttop, self.section_rightbottom, self.section_righttop,
                        self.section_rightbottom, self.section_righttop, self.section_rightbottom, self.section_righttop]
            idx = self.idx2%(len(sector_list))
            self.MoveSector(sector_list[idx])


    def getAction(self):
        action = self.SelectAction(self.action)
        return action


    def PlayerStyle(self):
        if self.play_style == 'aggressive':
            self.Threshold_health = 70
            self.Threshold_AMMO = 30

        elif self.play_style == 'defensive':
            self.Threshold_health = 70
            self.Threshold_AMMO = 20
        elif self.play_style == 'runner':
            self.Threshold_health = 70
            self.Threshold_AMMO = 20


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
        # print(self.angle)
    

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
                    if self.MeORNot((o.object_position_x,o.object_position_y,o.object_position_z)): #This DoomPlayer is me
                        continue
                    else: # This DoomPlayer is not me
                        EnemyPosition.append([o.object_name, o.x, o.width])
            else:
                continue

        return EnemyPosition

    def MeORNot(self, object_position):
        Object_location = [int(object_position[0]), int(object_position[1]), int(object_position[2])]
        if Object_location==self.location:
            # print("0f0adf0a0fa")
            return True
        else:
            return False

    # def MovePosition(self, position):

    def Shot(self):
        self.action[PlayerAction.Atack] = True
        # self.action[PlayerAction.MoveFront] = True

    def MoveSector(self, self_sector_class):
        self.move_finished = False
        self.action = self_sector_class.make_action(self.MH_state, action_order_sheet= self.action)
        if self_sector_class.is_finished(self.MH_state):
            self.move_finished = True
            self.roam_finished = False
            self.idx2 += 1

    def roaming(self):
        random_action = choice([PlayerAction.MoveLeft, PlayerAction.Run])
        self.action[random_action] = 1
        self.action[PlayerAction.TurnRight] = 1

    def roamSector(self):
        print("ROAMING")
        if self.now_sector == 'center':
            print("self idx", self.idx)
            roam_list = [self.section_centertop, self.section_centerleft, self.section_centerbottom, self.section_centerright]
            this_sector = roam_list[self.idx]
            self.action = this_sector.make_action(self.MH_state, action_order_sheet= self.action)
            if this_sector.is_finished(self.MH_state):
                print(self.location)
                self.roam_finished = True
                candidate = [0,1,2,3]
                candidate.pop(self.idx)
                self.idx = choice(candidate)

        elif self.now_sector == 'left':
            roam_list = [self.section_lefttop, self.section_leftbottom]
            this_sector = roam_list[self.idx]
            self.action = this_sector.make_action(self.MH_state, action_order_sheet= self.action)
            if this_sector.is_finished(self.MH_state):
                self.roam_finished = True
                candidate = [0,1]
                candidate.pop(self.idx)
                self.idx = candidate[0]

        elif self.now_sector == 'right':
            roam_list = [self.section_righttop, self.section_rightbottom]
            this_sector = roam_list[self.idx]
            self.action = this_sector.make_action(self.MH_state, action_order_sheet= self.action)
            if this_sector.is_finished(self.MH_state):
                self.roam_finished = True
                candidate = [0,1]
                candidate.pop(self.idx)
                self.idx = candidate[0]

        elif self.now_sector == 'top':
            roam_list = [self.section_topleft, self.section_topright]
            this_sector = roam_list[self.idx]
            self.action = this_sector.make_action(self.MH_state, action_order_sheet= self.action)
            if this_sector.is_finished(self.MH_state):
                self.roam_finished = True
                candidate = [0,1]
                candidate.pop(self.idx)
                self.idx = candidate[0]

        elif self.now_sector == 'bottom':
            roam_list = [self.section_bottomleft, self.section_bottomright]
            this_sector = roam_list[self.idx]
            self.action = this_sector.make_action(self.MH_state, action_order_sheet= self.action)
            if this_sector.is_finished(self.MH_state):
                self.move_finished = False
                candidate = [0,1]
                candidate.pop(self.idx)
                self.idx = candidate[0]

    def setFov(self, fov):
        self.fov = fov

    def SetSectorClass(self):
        self.section_centertop = MoveToSectionActioner(self.game, Section.CenterTop)
        self.section_centerleft = MoveToSectionActioner(self.game, Section.Center)
        self.section_centerbottom = MoveToSectionActioner(self.game, Section.Center)
        self.section_centerright = MoveToSectionActioner(self.game, Section.Center)

        self.section_topleft = MoveToSectionActioner(self.game, Section.TopLeft) # Weapon Room
        self.section_topright = MoveToSectionActioner(self.game, Section.TopRight) # Weapon Room

        self.section_bottomleft = MoveToSectionActioner(self.game, Section.BottomLeft) # Weapon Room
        self.section_bottomright = MoveToSectionActioner(self.game, Section.BottomRight) # Weapon Room

        self.section_righttop =MoveToSectionActioner(self.game, Section.RightTop) # Health Room 
        self.section_rightbottom =MoveToSectionActioner(self.game, Section.RightBottom) # Health Room 

        self.section_lefttop = MoveToSectionActioner(self.game, Section.LeftTop) # Health Room
        self.section_leftbottom = MoveToSectionActioner(self.game, Section.LeftBottom) # Health Room

    def ResetAction(self): # action 누적을 위한 자료구조
        self.action = {
            PlayerAction.Atack : 0,
            PlayerAction.Run : True,
            PlayerAction.b : 0,

            PlayerAction.MoveRight : 0,
            PlayerAction.MoveLeft : 0,
            PlayerAction.MoveBack : 0,
            PlayerAction.MoveFront : 0,
            PlayerAction.TurnRight : 0,
            PlayerAction.TurnLeft : 0,
            PlayerAction.Use : 0,

            PlayerAction.weapone1 : 0,
            PlayerAction.weapone2 : 0,
            PlayerAction.weapone3 : 0,
            PlayerAction.weapone4 : 0,
            PlayerAction.weapone5 : 0,
            PlayerAction.weapone6 : 0,

            PlayerAction.SELECT_NEXT_WEAPON : 0,
            PlayerAction.SELECT_PREV_WEAPON : 0,

            PlayerAction.pitch : 0,
            PlayerAction.rotateY : 0,
            PlayerAction.rotateX : 0
            }

    def SelectAction(self, action_dict): # action_order를 doom 전용 action으로 표현
        action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # action = [0 for i in range(len(action_dict.keys()))]
        for key in action_dict.keys():
            action[key] = action_dict[key]
        return action

    def ResetIdx2(self):
        if self.now_sector!=self.prev_sector:
            self.idx2 = 0


    def OptimalWeapon(self):
        if self.plazma > 0:
            if self.weapon != 6.0:
                self.action[PlayerAction.SELECT_PREV_WEAPON] = True
        else:
            if self.weapon == 3.0:
                self.action[PlayerAction.SELECT_NEXT_WEAPON] = True

    def getLocation(self):
        return self.location

    def SeeCenter(self):
        x,y,_ = self.getLocation()
        if 500 != x:
            r_x, r_y = 500-x, 500-y
            theta = math.atan((r_y)/(r_x))
            if (r_x>0):
                theta = math.pi + theta
            theta = theta*180/math.pi
            rotate = theta - self.angle
            if rotate < 0:
                rotate += 360

            if rotate > 180:
                self.action[PlayerAction.TurnLeft]=True
                self.action[PlayerAction.Run]=False

            else:
                self.action[PlayerAction.TurnRight]=True
                self.action[PlayerAction.Run]=False

        else:
            self.action[PlayerAction.TurnLeft]=True
                
    def autoAim(self, version):
        if version == 'super':
            ExistObject = self.state.objects
            for o in ExistObject:
                if o.name == 'DoomPlayer':
                    o_x,o_y,o_z = o.position_x, o.position_y, o.position_z
                    if self.MeORNot((o_x,o_y,o_z)): #This DoomPlayer is me
                        continue
                    else: # This DoomPlayer is not me
                        x,y,_ = self.getLocation()
                        if o_x != x:
                            r_x, r_y = o_x-x, o_y-y
                            theta = math.atan((r_y)/(r_x))
                            if (r_x>0):
                                theta = math.pi + theta
                            theta = theta*180/math.pi
                            rotate = theta - self.angle
                            if rotate < 0:
                                rotate += 360

                            if rotate > 180:
                                self.action[PlayerAction.TurnLeft]=True
                                self.action[PlayerAction.Run]=False

                            else:
                                self.action[PlayerAction.TurnRight]=True
                                self.action[PlayerAction.Run]=False

                        else:
                            self.action[PlayerAction.TurnLeft]=True
                        return
                else:
                    continue
        else:
            # ExistObject = self.state.objects
            ExistObject = self.state.labels
            for o in ExistObject:
                if o.object_name == 'DoomPlayer':
                    o_x,o_y,o_z = o.object_position_x, o.object_position_y, o.object_position_z
                    if self.MeORNot((o_x,o_y,o_z)): #This DoomPlayer is me
                        continue
                    else: # This DoomPlayer is not me
                        x,y,_ = self.getLocation()
                        if o_x != x:
                            r_x, r_y = o_x-x, o_y-y
                            theta = math.atan((r_y)/(r_x))
                            if (r_x>0):
                                theta = math.pi + theta
                            theta = theta*180/math.pi
                            rotate = theta - self.angle
                            if rotate < 0:
                                rotate += 360

                            if rotate > 180:
                                self.action[PlayerAction.TurnLeft]=True
                                self.action[PlayerAction.Run]=False

                            else:
                                self.action[PlayerAction.TurnRight]=True
                                self.action[PlayerAction.Run]=False

                        else:
                            self.action[PlayerAction.TurnLeft]=True
                        return
                else:
                    continue
            self.SeeCenter()
            return
            

