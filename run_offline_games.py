"""Run some games in some scenarios locally.

This is the correct entry to start the program.
To test your agent, the major modifications you need to make are:
1. import your own agent class (you definitely know where it is)
2. instantiate your agent and its opponent (replace the Agent below)

The code looks like:

from ai.agent import Agent

red = Agent()
blue = DemoAgent()
"""


import json
import pickle
import time
import zipfile
import os
import numpy

# from ai import Agent
from ai import Agent
from train_env import TrainEnv

RED, BLUE, GREEN = 0, 1, -1


def main():
    run_in_single_agent_mode()
    # run_in_multi_agents_mode()


def run_in_single_agent_mode():
    """
    run demo in single agent mode
    """
    print("running in single agent mode...")
    # instantiate agents and env
    red1 = Agent()
    blue1 = Agent()
    env1 = TrainEnv()
    begin = time.time()

    # get data ready, data can from files, web, or any other sources
    with open("Data/scenarios/2201010202.json") as f:
        scenario_data = json.load(f)
    with open("Data/maps/map_221/basic.json") as f:
        basic_data = json.load(f)
    with open('Data/maps/map_221/cost.pickle', 'rb') as file:
        cost_data = pickle.load(file)
    see_data = numpy.load("Data/maps/map_221/221see.npz")['data']

    # varialbe to build replay
    all_states = []

    # player setup info
    player_info = [{
        "seat": 1,
        "faction": 0,
        "role": 0,
        "user_name": "demo",
        "user_id": 0
    },
    {
        "seat": 11,
        "faction": 1,
        "role": 0,
        "user_name": "demo",
        "user_id": 0
    }]

    # env setup info
    env_step_info = {
        "scenario_data": scenario_data,
        "basic_data": basic_data,
        "cost_data": cost_data,
        "see_data": see_data,
        "player_info": player_info
    }

    # setup env
    state = env1.setup(env_step_info)
    all_states.append(state[GREEN])
    print("Environment is ready.")

    # setup AIs
    red1.setup(
        {
            "scenario": scenario_data,
            "basic_data": basic_data,
            "cost_data": cost_data,
            "see_data": see_data,
            "seat": 1,
            "faction": 0,
            "role": 0,
            "user_name": "demo",
            "user_id": 0,
            "state": state,
        }
    )
    blue1.setup(
        {
            "scenario": scenario_data,
            "basic_data": basic_data,
            "cost_data": cost_data,
            "see_data": see_data,
            "seat": 11,
            "faction": 1,
            "role": 0,
            "user_name": "demo",
            "user_id": 0,
            "state": state,
        }
    )
    print("agents are ready.")

    # loop until the end of game
    print("steping")
    done = False
    while not done:
        actions = []
        actions += red1.step(state[RED])
        red1.timess = red1.timess + 1
        actions += blue1.step(state[BLUE])
        if (state[RED]['time']['cur_step'] % 200 == 0) and (state[RED]["time"]["stage"] == 2):
            print("cur_step=", state[RED]['time']['cur_step'])

        state, done = env1.step(actions)
        all_states.append(state[GREEN])

    env1.reset()
    red1.reset()
    blue1.reset()
    
    print(f"Total time: {time.time() - begin:.3f}s")

    # save replay
    zip_name = f"logs/replays/replay_{begin}.zip"
    if not os.path.exists("logs/replays/"):
        os.makedirs("logs/replays/")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr(f"replay_{begin}.json", to_json_string(all_states).encode('gbk'))


def to_json_string(o, indent=None):
    return json.dumps(o, ensure_ascii=False, indent=indent, separators=(',', ':'))


def run_in_multi_agents_mode():
    """
    run demo in multi agent mode
    """
    print("running in multi agent mode...")
    # instantiate agents and env
    red1 = Agent()
    red2 = Agent()
    red3 = Agent()
    blue1 = Agent()
    blue2 = Agent()
    blue3 = Agent()
    env1 = TrainEnv()
    begin = time.time()

    # get data ready, data can from files, web, or any other sources
    with open("Data/scenarios/2201010202.json") as f:
        scenario_data = json.load(f)
    with open("Data/maps/map_94/basic.json") as f:
        basic_data = json.load(f)
    with open('Data/maps/map_94/cost.pickle', 'rb') as file:
        cost_data = pickle.load(file)
    see_data = numpy.load("Data/maps/map_94/94see.npz")['data']

    # varialbe to build replay
    all_states = []

    # player setup info
    player_info = [{
        "seat": 1,
        "faction": 0,
        "role": 1,
        "user_name": "red1",
        "user_id": 1
    },
    {
        "seat": 2,
        "faction": 0,
        "role": 0,
        "user_name": "red2",
        "user_id": 2
    },
    {
        "seat": 3,
        "faction": 0,
        "role": 0,
        "user_name": "red3",
        "user_id": 3
    },
    {
        "seat": 11,
        "faction": 1,
        "role": 1,
        "user_name": "blue1",
        "user_id": 11
    },
    {
        "seat": 12,
        "faction": 1,
        "role": 0,
        "user_name": "blue2",
        "user_id": 12
    },
    {
        "seat": 13,
        "faction": 1,
        "role": 0,
        "user_name": "blue3",
        "user_id": 13
    }]

    # env setup info
    env_step_info = {
        "scenario_data": scenario_data,
        "basic_data": basic_data,
        "cost_data": cost_data,
        "see_data": see_data,
        "player_info": player_info
    }

    # setup env
    state = env1.setup(env_step_info)
    all_states.append(state[GREEN])
    print("Environment is ready.")

    # setup AIs
    red1.setup(
        {
            "scenario": scenario_data,
            "basic_data": basic_data,
            "cost_data": cost_data,
            "see_data": see_data,
            "seat": 1,
            "faction": 0,
            "role": 1,
            "user_name": "red1",
            "user_id": 1,
            "state": state,
        }
    )
    red2.setup(
        {
            "scenario": scenario_data,
            "basic_data": basic_data,
            "cost_data": cost_data,
            "see_data": see_data,
            "seat": 2,
            "faction": 0,
            "role": 0,
            "user_name": "red2",
            "user_id": 2,
            "state": state,
        }
    )
    red3.setup(
        {
            "scenario": scenario_data,
            "basic_data": basic_data,
            "cost_data": cost_data,
            "see_data": see_data,
            "seat": 3,
            "faction": 0,
            "role": 0,
            "user_name": "red3",
            "user_id": 3,
            "state": state,
        }
    )
    blue1.setup(
        {
            "scenario": scenario_data,
            "basic_data": basic_data,
            "cost_data": cost_data,
            "see_data": see_data,
            "seat": 11,
            "faction": 1,
            "role": 1,
            "user_name": "blue1",
            "user_id": 11,
            "state": state,
        }
    )
    blue2.setup(
        {
            "scenario": scenario_data,
            "basic_data": basic_data,
            "cost_data": cost_data,
            "see_data": see_data,
            "seat": 12,
            "faction": 1,
            "role": 0,
            "user_name": "blue2",
            "user_id": 12,
            "state": state,
        }
    )
    blue3.setup(
        {
            "scenario": scenario_data,
            "basic_data": basic_data,
            "cost_data": cost_data,
            "see_data": see_data,
            "seat": 13,
            "faction": 1,
            "role": 0,
            "user_name": "blue3",
            "user_id": 13,
            "state": state,
        }
    )
    print("agents are ready.")


    

    state, done = env1.step([
        {
            "actor": 1,
            "type": 100,
            "info": {
                2: { 
                    "operators": [
                        1
                    ]
                }
            }
        }
    ])

    state, done = env1.step([
        {
            "actor": 1,
            "type": 200,
            "info": {
                "company_id": 3,
                "mission_type": 0,
                "target_pos": 1111111111,
                "route": [9990000,000000],
                "start_time": 43434343,
                "end_time": 43434343
            }
        }
    ])


    # loop until the end of game
    print("steping")
    done = False
    while not done:
        actions = []
        actions += red1.step(state[RED])
        actions += red2.step(state[RED])
        actions += red3.step(state[RED])
        actions += blue1.step(state[BLUE])
        actions += blue2.step(state[BLUE])
        actions += blue3.step(state[BLUE])
        state, done = env1.step(actions)
        all_states.append(state[GREEN])

    env1.reset()
    red1.reset()
    red2.reset()
    red3.reset()
    blue1.reset()
    blue2.reset()
    blue3.reset()
    
    print(f"Total time: {time.time() - begin:.3f}s")

    # save replay
    zip_name = f"logs/replays/replay_{begin}.zip"
    if not os.path.exists("logs/replays/"):
        os.makedirs("logs/replays/")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr(f"replay_{begin}.json", to_json_string(all_states).encode('gbk'))

if __name__ == "__main__":
    main()
