# Copyright (c) 2025, Unitree Robotics Co., Ltd. All Rights Reserved.
# License: Apache License, Version 2.0

import gymnasium as gym

from . import e2_wrench_cfg


gym.register(
    id="e2_wrench",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": e2_wrench_cfg.PickPlaceG129DEX3JointEnvCfgWrench,
    },
    disable_env_checker=True,
)
