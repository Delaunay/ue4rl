from ue4ml.core import AgentConfig
from ue4rl.env import UnrealEnv


class CartPole(UnrealEnv):
    def __init__(self, ue4params=None, **kwargs):
        if ue4params is not None:
            ue4params.set_default_map_name("Game/CartPole/CartPole.umap")

        super().__init__(ue4params=ue4params, **kwargs)

    @staticmethod
    def default_agent_config():
        agent_config = AgentConfig()
        agent_config.add_sensor(
            "AIPerception",
            {
                "mode": "rotator",
                "count": 3,
                "sort": "distance",
                "peripheral_angle": 180,
            },
        )
        agent_config.add_sensor("Attribute", {"attributes": "health, mana"})
        agent_config.add_actuator(
            "InputKey",
            {"ignore_keys": "esc, backspace", "ignore_actions": "pause, inventory"},
        )
        agent_config.avatarClassName = "CartPole_Pawn"
        return agent_config
