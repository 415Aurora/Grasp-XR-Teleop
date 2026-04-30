# Copyright (c) 2025, Unitree Robotics Co., Ltd. All Rights Reserved.
# License: Apache License, Version 2.0      
"""
public base scene configuration module
provides reusable scene element configurations, such as tables, objects, ground, lights, etc.
"""
import isaaclab.sim as sim_utils
from isaaclab.assets import  AssetBaseCfg, RigidObjectCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import GroundPlaneCfg, UsdFileCfg
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
from tasks.common_config import   CameraBaseCfg  # isort: skip
import os
project_root = os.environ.get("PROJECT_ROOT")
@configclass
class TableCylinderSceneCfg(InteractiveSceneCfg): # inherit from the interactive scene configuration class
    """object table scene configuration class
    defines a complete scene containing robot, object, table, etc.
    """
      # 1. room wall configuration - simplified configuration to avoid rigid body property conflicts
    room_walls = AssetBaseCfg(
        prim_path="/World/envs/env_.*/Room",
        init_state=AssetBaseCfg.InitialStateCfg(
            pos=[0.0, 0.0, -0.2],  # 房间中心点
            rot=[1.0, 0.0, 0.0, 0.0]
        ),
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/myusd/structures/iron-str1.usd",
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False),
        ),
    )
    
    packing_table = AssetBaseCfg(
        prim_path="/World/envs/env_.*/PackingTable",    # table in the scene
        init_state=AssetBaseCfg.InitialStateCfg(pos=[-0.5,0.75, -0.11],   # initial position [x, y, z]
                                                rot=[1.0, 0.0, 0.0, 0.0]), # initial rotation [x, y, z, w]
        spawn=UsdFileCfg(
            # usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/PackingTable/packing_table.usd",    # table model file
            usd_path=f"{project_root}/myusd/table/table.usd", #自定义桌子 
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),    
        ),
    )

    nutworld = AssetBaseCfg(
        prim_path="/World/envs/env_.*/nut0",   
        init_state=AssetBaseCfg.InitialStateCfg(pos=[0.03838, 0.3712, 0.70], # 在table2上  
                                                rot=[0.707, 0.0, 0.0, 0.707]), 
        spawn=UsdFileCfg(
            #usd_path=f"{project_root}/myusd/Objects/plateandbolt/factory_nut_m20_tight/factory_nut_m20_tight.usd",    # table model file  
            #usd_path=f"{project_root}/myusd/Objects/plateandbolt/nut2.0.usd",
            #usd_path=f"{project_root}/myusd/Objects/plateandbolt/nut1.5.usd",
            usd_path=f"{project_root}/myusd/Objects/plateandbolt/nutworld.usd",
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
        ),
    )

    packing_table_2 = AssetBaseCfg(
        prim_path="/World/envs/env_.*/PackingTable_2",   
        init_state=AssetBaseCfg.InitialStateCfg(pos=[-3.5, 0.55, -0.15],  
                                                rot=[1.0, 0.0, 0.0, 0.0]), 
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/assets/objects/PackingTable/PackingTable.usda",    # table model file
            #usd_path=f"{project_root}/IsaacLab/source/isaaclab_assets/data/Robots/ANYbotics/anymal_d.usd", # 机械狗，需要选kinematic_enabled=False
            #usd_path=f"{project_root}/PackingTable.usd", # 这会找不到材质啥的
            #rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False),   
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True), 
        ),
    )

    basket = AssetBaseCfg(
        prim_path="/World/envs/env_.*/basket",   
        init_state=AssetBaseCfg.InitialStateCfg(pos=[-1.2484, 0.6446, -0.255],  
                                                rot=[1.0, 0.0, 0.0, 0.0]), 
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/assets/objects/PackingTable/basket.usd",    # table model file  
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True), 
        ),
    )


   
    object = RigidObjectCfg(
        prim_path="/World/envs/env_.*/Object",    # object in the scene
        init_state=RigidObjectCfg.InitialStateCfg(pos=[-3.35, 0.40, 0.84], # initial position (pos) 
                                                  rot=[1, 0, 0, 0]), # initial rotation (rot)
        spawn=sim_utils.CylinderCfg(
            radius=0.018,    # cylinder radius (radius)
            height=0.35,     # cylinder height (height)
 
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
            ),    # rigid body properties configuration (rigid_props)
            mass_props=sim_utils.MassPropertiesCfg(mass=0.4),    # mass properties configuration (mass)
            collision_props=sim_utils.CollisionPropertiesCfg(),    # collision properties configuration (collision_props)
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.15, 0.15, 0.15), metallic=1.0),    # visual material configuration (visual_material)
            physics_material=sim_utils.RigidBodyMaterialCfg(
                friction_combine_mode="max",    # friction combine mode
                restitution_combine_mode="min",    # restitution combine mode
                static_friction=1.5,    # static friction coefficient
                dynamic_friction=1.5,    # dynamic friction coefficient
                restitution=0.0,    # restitution coefficient (no restitution)
            ),
        ),
    )


    ground = AssetBaseCfg(
        prim_path="/World/GroundPlane",    # ground in the scene
        spawn=GroundPlaneCfg( ),    # ground configuration
    )   

    # Lights
    # 4. light configuration
    light = AssetBaseCfg(
        prim_path="/World/light",   # light in the scene
        spawn=sim_utils.DomeLightCfg(color=(0.75, 0.75, 0.75), # light color (white)
                                     intensity=3000.0),    # light intensity
    )

    world_camera = CameraBaseCfg.get_camera_config(prim_path="/World/PerspectiveCamera",
                                                    pos_offset=(-0.1, 3.6, 1.6),
                                                    rot_offset=( -0.00617,0.00617, 0.70708, -0.70708),
                                                    focal_length = 16.5)