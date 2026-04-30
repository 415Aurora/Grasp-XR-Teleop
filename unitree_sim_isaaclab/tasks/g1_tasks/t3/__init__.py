
# Copyright (c) 2025, Unitree Robotics Co., Ltd. All Rights Reserved.
# License: Apache License, Version 2.0  

import gymnasium as gym
import os

from . import t3cfg


gym.register(
    id="t3",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": t3cfg.PickPlaceG129DEX3JointEnvCfg2,
    },
    disable_env_checker=True,
)

