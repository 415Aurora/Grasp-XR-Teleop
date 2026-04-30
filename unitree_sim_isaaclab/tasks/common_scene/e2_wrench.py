# Copyright (c) 2025, Unitree Robotics Co., Ltd. All Rights Reserved.
# License: Apache License, Version 2.0

import os
import sys
from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.assets import AssetBaseCfg, RigidObjectCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import GroundPlaneCfg, UsdFileCfg
from isaaclab.utils import configclass
from tasks.common_config import CameraBaseCfg  # isort: skip


REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from graduation_design.wrench_extension import build_wrench_scene_spec


project_root = os.environ.get("PROJECT_ROOT")
WRENCH_SCENE_SPEC = build_wrench_scene_spec()


@configclass
class TableWrenchSceneCfg(InteractiveSceneCfg):
    room_walls = AssetBaseCfg(
        prim_path="/World/envs/env_.*/Room",
        init_state=AssetBaseCfg.InitialStateCfg(
            pos=[0.0, 0.0, -0.2],
            rot=[1.0, 0.0, 0.0, 0.0],
        ),
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/myusd/structures/iron-str1.usd",
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False),
        ),
    )

    packing_table = AssetBaseCfg(
        prim_path="/World/envs/env_.*/PackingTable",
        init_state=AssetBaseCfg.InitialStateCfg(pos=[-0.5, 0.75, -0.11], rot=[1.0, 0.0, 0.0, 0.0]),
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/myusd/table/table.usd",
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
        ),
    )

    packing_table_2 = AssetBaseCfg(
        prim_path="/World/envs/env_.*/PackingTable_2",
        init_state=AssetBaseCfg.InitialStateCfg(pos=[-3.5, 0.55, -0.15], rot=[1.0, 0.0, 0.0, 0.0]),
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/assets/objects/PackingTable/PackingTable.usda",
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
        ),
    )

    zuantou = AssetBaseCfg(
        prim_path="/World/envs/env_.*/zuantou",
        init_state=AssetBaseCfg.InitialStateCfg(
            pos=[-0.0333, 0.5907, 0.8925],
            rot=[0.653, 0.653, -0.271, -0.271],
        ),
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/myusd/Objects/zuantou/zuantou.usda",
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False),
        ),
    )

    object = RigidObjectCfg(
        prim_path="/World/envs/env_.*/Object",
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=list(WRENCH_SCENE_SPEC["object_pos"]),
            rot=list(WRENCH_SCENE_SPEC["object_rot"]),
        ),
        spawn=UsdFileCfg(
            usd_path=WRENCH_SCENE_SPEC["usd_path"],
            scale=WRENCH_SCENE_SPEC["object_scale"],
            rigid_props=sim_utils.RigidBodyPropertiesCfg(disable_gravity=False),
            mass_props=sim_utils.MassPropertiesCfg(mass=0.4),
            collision_props=sim_utils.CollisionPropertiesCfg(collision_enabled=True),
        ),
    )

    target_zone = AssetBaseCfg(
        prim_path="/World/envs/env_.*/TargetZone",
        init_state=AssetBaseCfg.InitialStateCfg(
            pos=list(WRENCH_SCENE_SPEC["target_zone_center"]),
            rot=[1.0, 0.0, 0.0, 0.0],
        ),
        spawn=sim_utils.CylinderCfg(
            radius=WRENCH_SCENE_SPEC["target_zone_radius_m"],
            height=WRENCH_SCENE_SPEC["target_zone_height_m"],
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
            collision_props=sim_utils.CollisionPropertiesCfg(collision_enabled=False),
            visual_material=sim_utils.PreviewSurfaceCfg(
                diffuse_color=(0.1, 0.7, 0.2),
                opacity=0.35,
                metallic=0.0,
            ),
        ),
    )

    ground = AssetBaseCfg(
        prim_path="/World/GroundPlane",
        spawn=GroundPlaneCfg(),
    )

    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DomeLightCfg(color=(0.75, 0.75, 0.75), intensity=3000.0),
    )

    world_camera = CameraBaseCfg.get_camera_config(
        prim_path="/World/PerspectiveCamera",
        pos_offset=(-0.1, 3.6, 1.6),
        rot_offset=(-0.00617, 0.00617, 0.70708, -0.70708),
        focal_length=16.5,
    )
