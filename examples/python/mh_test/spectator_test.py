#!/usr/bin/env python3

#####################################################################
# This script presents SPECTATOR mode. In SPECTATOR mode you play and
# your agent can learn from it.
# Configuration is loaded from "../../scenarios/<SCENARIO_NAME>.cfg" file.
# 
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from argparse import ArgumentParser
import os
from pydoc import ispackage
from time import sleep
import vizdoom as vzd
from PIL import Image
import keyboard
from vizdoom_object_data import *
from vizdoom_player_action import * 

DEFAULT_CONFIG = os.path.join(vzd.scenarios_path, "deathmatch.cfg")

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

    game.set_objects_info_enabled(True)
    game.set_sectors_info_enabled(True)
    game.set_labels_buffer_enabled(True)
    game.set_automap_buffer_enabled(True)

    game.add_available_game_variable(vzd.GameVariable.POSITION_X)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Y)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Z)



    game.set_screen_resolution(vzd.ScreenResolution.RES_1920X1080)
    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    game.set_mode(vzd.Mode.SPECTATOR)
    
    game.init()

    game.new_episode()
       
    aimActioner = AimActioner(game)
    attackActioner = AttackActioner(game)
    while not game.is_episode_finished():
        stateData = StateData2(game.get_state())
        action_order_sheet = aimActioner.make_action(stateData)
        action_order_sheet = attackActioner.make_action(stateData, action_order_sheet= action_order_sheet)
        game.make_action(make_into_doom_action(action_order_sheet))
        

    #     a = 1
    #     for i in range(1000000):
    #         a += 2
    #     # print(get_angle_from_player_to_direction(game, 500, 500))

    #     # relative_angle = (-get_player(game).angle)+360)%360
    #     # rx = 500-get_player(game).position_x
    #     # ry = 500-get_player(game).position_y
    #     # ra = ((get_angle_from_player_to_direction(game, 500, 500)-get_player(game).angle)+360)%360
    #     # print("Game Player Angle: %d, Relative: %d, rx: %d, ry: %d"% (get_player(game).angle, ra, rx, ry))

    #     a = get_player(game).angle
    #     x = get_player(game).position_x
    #     y = get_player(game).position_y

    #     print("a: %d, x: %d, y: %d"%(a, x, y))
    #     game.advance_action() # 이거 있어야 조작 가능
        
        

    game.close()

"""
game.get_state().screen_buffer가 현 시점의 
"""
