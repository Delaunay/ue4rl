# Copyright Epic Games, Inc. All Rights Reserved.

import os
import gym
import ue4ml.logger as logger
from ue4ml.utils import random_action, ArgumentParser

from ue4ml.core import AgentConfig
from ue4ml.runner import UE4Params
from ue4rl.env import UnrealEnv
from ue4ml.envs import ActionRPG

logger.set_level(logger.DEBUG)

project = '/media/setepenre/Games/UE4RL/UE4RL.uproject'
project = 'E:/cartpole/UE4RL.uproject'
map = 'Game/CartPole/CartPole.umap'

# see ue4ml.utils.ArgumentParser.__init__ for list of default parameters
parser = ArgumentParser()
parser.add_argument("--iter", type=int, default=3, help="number of games to play")
parser.add_argument("--project", type=str, default=project, help="Path to the project containing the environment")
parser.add_argument("--level", type=str, default=map, help="Path to the level to load")
args = parser.parse_args()

if os.environ.get('UE-DevBinaries') is None and args.exec is None:
    raise RuntimeError('UE4 binaries not found')

# python run.py -h
# usage: {} [-h] [--env ENV] [--nothreads NOTHREADS] [--norendering NORENDERING] [--nosound NOSOUND] [--resx RESX]
#           [--resy RESY] [--exec EXEC] [--port PORT] [--iter ITER] [--project PROJECT] [--level LEVEL]

# optional arguments:
#   -h, --help            show this help message and exit
#   --env ENV             environment ID
#   --nothreads NOTHREADS
#   --norendering NORENDERING
#   --nosound NOSOUND
#   --resx RESX
#   --resy RESY
#   --exec EXEC
#   --port PORT
#   --iter ITER           number of games to play
#   --project PROJECT     Path to the project containing the environment
#   --level LEVEL         Path to the level to load

class CartPole(UnrealEnv):
    MAP = '/Game/CartPole/CartPole.umap'

    def __init__(self, path, ue4params=None, **kwargs):
        super().__init__(path, CartPole.MAP, ue4params=ue4params, **kwargs)

    def reset(self, wait_action=None, skip_time=1):
        # custom skip before resetting to give the game's BP control flow time to 'rest'
        self.skip(5)
        ret = super().reset(wait_action, skip_time)
        return ret

    def get_reward(self):
        return self._steps_performed

    # @staticmethod
    # def default_agent_config():
    #     agent_config = AgentConfig()
    #     # agent_config.add_sensor(
    #     #     "AIPerception",
    #     #     {
    #     #         "mode": "rotator",
    #     #         "count": 3,
    #     #         "sort": "distance",
    #     #         "peripheral_angle": 180,
    #     #     },
    #     # )
    #     # agent_config.add_sensor("Attribute", {"attributes": "health, mana"})
    #     # agent_config.add_actuator(
    #     #     "InputKey",
    #     #     {"ignore_keys": "esc, backspace", "ignore_actions": "pause, inventory"},
    #     # )

    #     # E:/cartpole/Content/CartPole/CartPole_Pawn.uasset
    #     # Blueprint'/Game/CartPole/CartPole_Pawn.CartPole_Pawn'
    #     agent_config.avatarClassName = "CartPole_Pawn_C"
    #     return agent_config


if False:
    env = CartPole(
        args.project,
        UE4Params(
            sound=False,
            # Those are buggy
            # rendering=True,
            # single_thread=True
        ),
    )
else:
    env = ActionRPG(
        UE4Params(
            sound=False,
            # rendering=True,
            # single_thread=True
        ),
    )

print('Starting Environment')

for i in range(args.iter):
    obs = env.reset()

    reward = 0
    done = False
    print('Environment initialized')

    while not env.game_over:
        a = random_action(env)
        print(a)
        _, reward, done, _ = env.step(a)

    print("{}: Score: {}".format(i, reward))

env.close()
