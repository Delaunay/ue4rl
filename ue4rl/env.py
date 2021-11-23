from ue4ml import UnrealEnv as UnrealEnvBase, LOCALHOST, DEFAULT_PORT


class UnrealEnv(UnrealEnvBase):
    """Allows you to load any UnrealEngine project from an arbitrary path"""

    def __init__(
        self,
        path: str,
        map: str,
        server_address=LOCALHOST,
        server_port=DEFAULT_PORT,
        agent_config=None,
        reacquire=True,
        realtime=False,
        auto_connect=True,
        timeout=20,
        ue4params=None,
    ):
        super(UnrealEnv, self).__init__(
            server_address,
            server_port,
            agent_config,
            reacquire,
            realtime,
            auto_connect,
            timeout,
            ue4params,
        )
        self.PROJECT_NAME = path
        self.map = map

        if ue4params is not None:
            ue4params.set_default_map_name(self.map)
