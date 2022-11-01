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

    game.set_screen_resolution(vzd.ScreenResolution.RES_1920X1080)
    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    game.set_mode(vzd.Mode.SPECTATOR)
    
    game.init()

    game.new_episode()

    while not game.is_episode_finished():
        state = game.get_state()
        
        game.advance_action() # 이거 있어야 조작 가능

        if keyboard.is_pressed("Enter"):
            print("State #" + str(state.number))

            screen_buffer = state.screen_buffer
            print("screen buffer type: " + str(type(screen_buffer)))
            print("screen buffer shape: " + str(state.screen_buffer.shape)) # 현재 화면 
            print("screen buffer (below)")
            print(state.screen_buffer)      # 현재 화면

            im = Image.fromarray(screen_buffer[0]) # 왠지 모르겠지만 일단 RGB 전체는 안돼서 하나만 저장
            im.save("test(#%d).png" % state.number)
            
        
        while keyboard.is_pressed("Enter"):
            continue
    game.close()

"""
game.get_state().screen_buffer가 현 시점의 
"""
