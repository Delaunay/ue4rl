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

# python .\examples\run.py --exec E:\UnrealEngine\Engine\Binaries\Win64\UE4Editor.exe
#
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
#
#
#

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


    @staticmethod
    def default_agent_config():
        agent_config = AgentConfig()

        # Sensors
        # Sensors define the observation space

        # Params for all sensors:
        #   - tick_every_frame
        #   - tick_every_n_frames
        #   - tick_every_x_seconds

        agent_config.add_sensor(
            "Movement",
            {
                "location": "absolute",
                "velocity": "absolute"
            }
        )

        # Capture the scene as an image itslef
        # agent_config.add_sensor(
        #     "Camera",
        #     {
        #         "width":
        #         "height":
        #         "camera_index":
        #         "capture_source":
        #     }
        # )

        # this is needed if you want your input to work
        # Actuator mock the player's input
        # they define the action space
        #   see void ``U4MLActuator_InputKey::Act(const float DeltaTime)``
        agent_config.add_actuator("InputKey")
        agent_config.avatarClassName = "CartPole_Pawn_C"

        return agent_config


if 1:
    env = CartPole(
        args.project,
        UE4Params(
            sound=False,
            # Those are buggy
            # rendering=True,
            # single_thread=True
        ),
        launch=False,
        server_port=15151,
    )

    # INFO: ue4ml: connected to UE4RL at port 15151
    # DEBUG: ue4ml: setup agents
    # DEBUG: ue4ml: get action space
    # DEBUG: ue4ml: get observation space
    # Starting Environment
    # DEBUG: ue4ml: 15151: reset
    # DEBUG: ue4ml: reset!
    # DEBUG: ue4ml: Ready for next step
    # Traceback (most recent call last):
    #   File "examples/run.py", line 106, in <module>
    #     obs = env.reset()
    #   File "examples/run.py", line 56, in reset
    #     ret = super().reset(wait_action, skip_time)
    #   File "e:\unrealengine\engine\plugins\ai\ue4ml\source\python\ue4ml\core.py", line 183, in reset
    #     return self._get_observation()
    #   File "e:\unrealengine\engine\plugins\ai\ue4ml\source\python\ue4ml\core.py", line 158, in _get_observation
    #     return gym.spaces.unflatten(self.observation_space, raw_obs)
    #   File "F:\anaconda\envs\ue4\lib\functools.py", line 875, in wrapper
    #     return dispatch(args[0].__class__)(*args, **kw)
    #   File "F:\anaconda\envs\ue4\lib\site-packages\gym\spaces\utils.py", line 136, in unflatten_tuple
    #     return tuple(
    #   File "F:\anaconda\envs\ue4\lib\site-packages\gym\spaces\utils.py", line 137, in <genexpr>
    #     unflatten(s, flattened) for flattened, s in zip(list_flattened, space.spaces)
    #   File "F:\anaconda\envs\ue4\lib\functools.py", line 875, in wrapper
    #     return dispatch(args[0].__class__)(*args, **kw)
    #   File "F:\anaconda\envs\ue4\lib\site-packages\gym\spaces\utils.py", line 115, in unflatten_box_multibinary
    #     return np.asarray(x, dtype=space.dtype).reshape(space.shape)
    # ValueError: cannot reshape array of size 4 into shape (6,)
    # DEBUG: ue4ml: 15151: close(shutdown=True)
    # INFO: ue4ml: Closing connection on port 15151

else:
    env = ActionRPG(
        UE4Params(
            sound=False,
            rendering=True,
            single_thread=True
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
        print(obs, a, reward, done)
        obs, reward, done, _ = env.step(a)

    print("{}: Score: {}".format(i, reward))

env.close()
