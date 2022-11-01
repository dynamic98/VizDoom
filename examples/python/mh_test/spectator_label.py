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
from turtle import st
import vizdoom as vzd
from PIL import Image
import keyboard
import matplotlib.pyplot as plt
import cv2
import numpy as np

def draw_bounding_box(buffer, x, y, width, height, color):
        """
        Draw a rectangle (bounding box) on a given buffer in the given color.
        """
        for i in range(width):
            buffer[y, x + i, :] = color
            buffer[y + height, x + i, :] = color

        for i in range(height):
            buffer[y + i, x, :] = color
            buffer[y + i, x + width, :] = color


def color_labels(labels):
    """
    Walls are blue, floor/ceiling are red (OpenCV uses BGR).
    """
    tmp = np.stack([labels] * 3, -1)
    tmp[labels == 0] = [255, 0, 0]
    tmp[labels == 1] = [0, 0, 255]

    return tmp

doom_red_color = [0, 0, 203]
doom_blue_color = [203, 0, 0]
sleep_time = 28

DEFAULT_CONFIG = os.path.join(vzd.scenarios_path, "deathmatch.cfg")

def OrganizeObjectInfor(objects):
    dict = {}
    for o in state.objects: # 동작 가능 - 존재하는 모든 오브젝트의 정보 반환
        if o.name not in dict:
            dict[o.name] = 0
        dict[o.name] += 1
    return dict

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

    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)
    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    game.set_mode(vzd.Mode.SPECTATOR)
    
    game.set_labels_buffer_enabled(True)

    game.clear_available_game_variables()
    game.add_available_game_variable(vzd.GameVariable.POSITION_X)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Y)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Z)

    game.init()

    game.new_episode()

    while not game.is_episode_finished():
        game.advance_action() # 이거 있어야 조작 가능

        if keyboard.is_pressed("Enter"):
            state = game.get_state()

            # print object infor
            print("State: %s" % str(state.number))
            labels = state.labels
            print("Type %s" % type(labels))
            print("Visable Object Num: %d" % len(labels))
            # if labels is not None:
            #     cv2.imshow('ViZDoom Labels Buffer', color_labels(labels))
            dictInfor = OrganizeObjectInfor(state.objects)
            print(dictInfor)
            print("=====================")    

            if labels is not None:
                cv2.imshow('ViZDoom Labels Buffer', color_labels(labels))

            screen = state.screen_buffer
            for l in state.labels:
                if l.object_name in ["Medkit", "GreenArmor"]:
                    draw_bounding_box(screen, l.x, l.y, l.width, l.height, doom_blue_color)
                else:
                    draw_bounding_box(screen, l.x, l.y, l.width, l.height, doom_red_color)
            cv2.imshow('ViZDoom Screen Buffer', screen)

            cv2.waitKey(sleep_time)




            while keyboard.is_pressed("Enter"):
                continue
        

    game.close()

