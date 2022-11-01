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
from time import sleep
import vizdoom as vzd
import pandas as pd
import time
import numpy as np

DEFAULT_CONFIG = os.path.join("../../scenarios/", "deathmatch.cfg")

if __name__ == "__main__":
    parser = ArgumentParser("ViZDoom example showing how to use SPECTATOR mode.")
    parser.add_argument(dest="config",
                        default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../../scenarios/*cfg for more scenarios.")
    parser.add_argument("-n", "--name",
                        dest="name",
                        default=None,
                        type=str)

    args = parser.parse_args()

    assert args.name is not None, 'name please'

    game = vzd.DoomGame()
    
    # Choose scenario config file you wish to watch.
    # Don't load two configs cause the second will overrite the first one.
    # Multiple config files are ok but combining these ones doesn't make much sense.
    print('args config :',args.config)

    game.load_config(args.config)
    filepath='../../'
    heads = ['time', 'timestamp', 'ATTACK', 'SPEED', 'STRAFE', 'MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_BACKWARD', 'MOVE_FORWARD', 'TURN_RIGHT', 'TURN_LEFT', 'USE', 'SELECT_WEAPON1', 'SELECT_WEAPON2', 'SELECT_WEAPON3', 'SELECT_WEAPON4', 'SELECT_WEAPON5', 'SELECT_WEAPON6', 'SELECT_NEXT_WEAPON', 'SELECT_PREV_WEAPON', 'LOOK_UP_DOWN_DELTA', 'TURN_LEFT_RIGHT_DELTA', 'MOVE_LEFT_RIGHT_DELTA', 'KILLCOUNT', 'HEALTH', 'ARMOR', 'SELECTED_WEAPON', 'SELECTED_WEAPON_AMMO']
    # Enables freelook in engine
    game.add_game_args("+freelook 1")

    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)

    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    game.set_mode(vzd.Mode.SPECTATOR)

    game.init()

    episodes = 10
    elp_time = 0
    for i in range(episodes):
        print("Episode #" + str(i + 1))

        game.new_episode()
        data = pd.DataFrame(columns=heads)
        start_time = time.time()
        while not game.is_episode_finished():
            state = game.get_state()

            game.advance_action()
            now = time.time()

            last_action = game.get_last_action()
            reward = game.get_last_reward()
            variables = state.game_variables
            elp_time = now - start_time
            var = np.concatenate(([now], [elp_time], last_action, variables), axis=0)
            new_df = pd.DataFrame([var], columns=heads)
            
            data = pd.concat([data, new_df], ignore_index=True)

            print("State #" + str(state.number))
            print("Game variables: ", variables)
            print("Action:", last_action)
            print("Reward:", reward)
            print("=====================")

        print("Episode finished!")
        print("Total reward:", game.get_total_reward())
        print("************************")
        sleep(2.0)
        data.to_csv(filepath + str(start_time) + '_' + args.name + '_res.csv', index=False)

    game.close()
