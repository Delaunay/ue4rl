    # @staticmethod
    # def default_agent_config():
    #     agent_config = AgentConfig()

    #     # Sensors
    #     # Sensors define the observation space

    #     # Params for all sensors:
    #     #   - tick_every_frame
    #     #   - tick_every_n_frames
    #     #   - tick_every_x_seconds

    #     agent_config.add_sensor(
    #         "Movement",
    #         {
    #             "location": "absolute",
    #             "velocity": "absolute"
    #         }
    #     )

    #     # Capture the scene as an image itslef
    #     # agent_config.add_sensor(
    #     #     "Camera",
    #     #     {
    #     #         "width":
    #     #         "height":
    #     #         "camera_index":
    #     #         "capture_source":
    #     #     }
    #     # )

    #     # this is needed if you want your input to work
    #     # Actuator mock the player's input
    #     # they define the action space
    #     #   see void ``U4MLActuator_InputKey::Act(const float DeltaTime)``