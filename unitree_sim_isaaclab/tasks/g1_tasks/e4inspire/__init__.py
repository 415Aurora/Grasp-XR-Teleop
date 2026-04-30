
# Copyright (c) 2025, Unitree Robotics Co., Ltd. All Rights Reserved.
# License: Apache License, Version 2.0  

import gymnasium as gym

from . import e4inspirecfg


gym.register(
    id="e4inspire",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": e4inspirecfg.PickPlaceG129InspireBaseFixEnvCfg,
    },
    disable_env_checker=True,
)

