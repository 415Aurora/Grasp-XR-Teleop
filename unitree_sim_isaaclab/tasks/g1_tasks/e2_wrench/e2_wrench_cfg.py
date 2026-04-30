# Copyright (c) 2025, Unitree Robotics Co., Ltd. All Rights Reserved.
# License: Apache License, Version 2.0

from isaaclab.assets import ArticulationCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.utils import configclass

from graduation_design.wrench_extension import reset_wrench_outside_target_zone
from tasks.common_config import CameraPresets, G1RobotPresets  # isort: skip
from tasks.common_scene.e2_wrench import TableWrenchSceneCfg
from tasks.g1_tasks.e2.e2cfg import PickPlaceG129DEX3JointEnvCfg2


@configclass
class ObjectTableWrenchSceneCfg(TableWrenchSceneCfg):
    robot: ArticulationCfg = G1RobotPresets.g1_29dof_dex3_base_fix()
    front_camera = CameraPresets.g1_front_camera()
    left_wrist_camera = CameraPresets.left_dex3_wrist_camera()
    right_wrist_camera = CameraPresets.right_dex3_wrist_camera()
    my_camera1 = CameraPresets.my_camera1()


@configclass
class WrenchTerminationsCfg:
    success = DoneTerm(func=reset_wrench_outside_target_zone)


@configclass
class PickPlaceG129DEX3JointEnvCfgWrench(PickPlaceG129DEX3JointEnvCfg2):
    scene: ObjectTableWrenchSceneCfg = ObjectTableWrenchSceneCfg(
        num_envs=1,
        env_spacing=2.5,
        replicate_physics=True,
    )
    terminations: WrenchTerminationsCfg = WrenchTerminationsCfg()
