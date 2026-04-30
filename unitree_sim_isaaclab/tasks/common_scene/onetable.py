# Copyright (c) 2025, Unitree Robotics Co., Ltd. All Rights Reserved.
# License: Apache License, Version 2.0      
"""
public base scene configuration module
provides reusable scene element configurations, such as tables, objects, ground, lights, etc.
"""
print("=====onetable脚本开始=====")

import isaaclab.sim as sim_utils
from isaaclab.assets import  AssetBaseCfg, RigidObjectCfg, ArticulationCfg
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
            pos=[0.0, 0.0,0],  # 房间中心点
            rot=[1.0, 0.0, 0.0, 0.0]
        ),
        spawn=UsdFileCfg(
            #usd_path=f"{ISAAC_NUCLEUS_DIR}/Environments/Simple_Warehouse/warehouse.usd",  # use simple room model
            #usd_path=f"{project_root}/myusd/dlfisaacsim/Grid/default_environment.usd",
            #usd_path=f"{project_root}/myusd/dlfisaacsim/Simple_Warehouse/full_warehouse.usd",
            usd_path=f"{project_root}/myusd/structures/iron-str1.usd",
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False),
        ),
    )  
    packing_table = AssetBaseCfg(
        prim_path="/World/envs/env_.*/PackingTable",    # table in the scene
        init_state=AssetBaseCfg.InitialStateCfg(pos=[0.0, 0.55, -0.2],   # initial position [x, y, z]
                                                rot=[1.0, 0.0, 0.0, 0.0]), # initial rotation [x, y, z, w]
        spawn=UsdFileCfg(
            # usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/PackingTable/packing_table.usd",    # table model file
            usd_path=f"{project_root}/myusd/table/table.usda", #自定义桌子 
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),    
        ),
    )
    zuantou = AssetBaseCfg(
        prim_path="/World/envs/env_.*/zuantou",   
        init_state=AssetBaseCfg.InitialStateCfg(pos=[-2.2, 0.35, 0.70], # 在table2上  
                                                rot=[1.0, 0.0, 0.0, 0.0]), 
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/myusd/Objects/zuantou/zuantou.usda",    # table model file  
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
        ),
    )
    plateandbolt=RigidObjectCfg(
        prim_path="/World/envs/env_.*/plate",
        init_state=RigidObjectCfg.InitialStateCfg(pos=[-0.1, 0.45, 0.68], # 在table2上  
                                                rot=[1.0, 0.0, 0.0, 0.0]), 
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/myusd/Objects/plateandbolt/plate.usda",  
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
            # physics_material=sim_utils.RigidBodyMaterialCfg(
            #     friction_combine_mode="average",
            #     restitution_combine_mode="average",
            #     static_friction=0.8,
            #     dynamic_friction=0.6,
            #     restitution=0.0,
            # )
        ),
    )

    car=AssetBaseCfg(
        prim_path="/World/envs/env_.*/car",
        init_state=RigidObjectCfg.InitialStateCfg(pos=[0.5, 0.45, 1.8], # 在table2上  
                                                rot=[1.0, 0.0, 0.0, 0.0]), 
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/myusd/Objects/car/car.usda",  
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
        ),
    )
    # nut1 = AssetBaseCfg(
    #     prim_path="/World/envs/env_.*/nut1",   
    #     init_state=AssetBaseCfg.InitialStateCfg(pos=[2.9, 0.75, 0.9], # 在table2上  
    #                                             rot=[1.0, 0.0, 0.0, 0.0]), 
    #     spawn=UsdFileCfg(
    #         usd_path=f"{project_root}/myusd/Objects/plateandbolt/factory_nut_m20_tight/factory_nut_m20_tight.usd",    # table model file  
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
    #     ),
    # )
    # nut2 = AssetBaseCfg(
    #     prim_path="/World/envs/env_.*/nut2",   
    #     init_state=AssetBaseCfg.InitialStateCfg(pos=[3.1, 0.75, 0.9], # 在table2上  
    #                                             rot=[1.0, 0.0, 0.0, 0.0]), 
    #     spawn=UsdFileCfg(
    #         usd_path=f"{project_root}/myusd/Objects/plateandbolt/factory_nut_m20_tight/factory_nut_m20_tight.usd",    # table model file  
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
    #     ),
    # )
    # nut3 = AssetBaseCfg(
    #     prim_path="/World/envs/env_.*/nut3",   
    #     init_state=AssetBaseCfg.InitialStateCfg(pos=[2.9, 0.55, 0.9], # 在table2上  
    #                                             rot=[1.0, 0.0, 0.0, 0.0]), 
    #     spawn=UsdFileCfg(
    #         usd_path=f"{project_root}/myusd/Objects/plateandbolt/factory_nut_m20_tight/factory_nut_m20_tight.usd",    # table model file  
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
    #     ),
    # )

    # nut4 = AssetBaseCfg(
    #     prim_path="/World/envs/env_.*/nut4",   
    #     init_state=AssetBaseCfg.InitialStateCfg(pos=[3.1, 0.55, 0.9], # 在table2上  
    #                                             rot=[1.0, 0.0, 0.0, 0.0]), 
    #     spawn=UsdFileCfg(
    #         usd_path=f"{project_root}/myusd/Objects/plateandbolt/factory_nut_m20_tight/factory_nut_m20_tight.usd",    # table model file  
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
    #     ),
    # )

    nut0 = AssetBaseCfg(
        prim_path="/World/envs/env_.*/nut0",   
        init_state=AssetBaseCfg.InitialStateCfg(pos=[-0.3, 0.35, 0.70], # 在table2上  
                                                rot=[1.0, 0.0, 0.0, 0.0]), 
        spawn=UsdFileCfg(
            #usd_path=f"{project_root}/myusd/Objects/plateandbolt/factory_nut_m20_tight/factory_nut_m20_tight.usd",    # table model file  
            #usd_path=f"{project_root}/myusd/Objects/plateandbolt/nut2.0.usd",
            usd_path=f"{project_root}/myusd/Objects/plateandbolt/nut1.5.usd",
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
        ),
    )

    packing_table_2 = AssetBaseCfg(
        prim_path="/World/envs/env_.*/PackingTable_2",   
        init_state=AssetBaseCfg.InitialStateCfg(pos=[-3.5, 0.55, -0.2],  
                                                rot=[1.0, 0.0, 0.0, 0.0]), 
        spawn=UsdFileCfg(
            usd_path=f"{project_root}/assets/objects/PackingTable/PackingTable.usda",    # table model file
            #usd_path=f"{project_root}/IsaacLab/source/isaaclab_assets/data/Robots/ANYbotics/anymal_d.usd", # 机械狗，需要选kinematic_enabled=False
            #usd_path=f"{project_root}/PackingTable.usd", # 这会找不到材质啥的
            #rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False),   
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True), 
        ),
    )
    packing_table_3 = AssetBaseCfg(
        prim_path="/World/envs/env_.*/PackingTable_3",   
        init_state=AssetBaseCfg.InitialStateCfg(pos=[3.5, 0.55, -0.2],  
                                                rot=[1.0, 0.0, 0.0, 0.0]), 
        spawn=UsdFileCfg(
            #usd_path=f"{project_root}/myusd/table/table.usda",    # table model file
            #usd_path=f"{project_root}/assets/objects/PackingTable/PackingTable.usda",
            usd_path=f"{project_root}/myusd/table/table.usda", 
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),   
        ),
    )
    # packing_table_4 = AssetBaseCfg(
    #     prim_path="/World/envs/env_.*/PackingTable_4",   
    #     init_state=AssetBaseCfg.InitialStateCfg(pos=[3.5, -5, -0.2],  
    #                                             rot=[1.0, 0.0, 0.0, 0.0]), 
    #     spawn=UsdFileCfg(
    #         usd_path=f"{project_root}/assets/objects/PackingTable/PackingTable.usd",    # table model file
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),   
    #     ),
    # )
    # packing_table_5 = AssetBaseCfg(
    #     prim_path="/World/envs/env_.*/PackingTable_5",   
    #     init_state=AssetBaseCfg.InitialStateCfg(pos=[-3.5, -5, -0.2],  
    #                                             rot=[1.0, 0.0, 0.0, 0.0]), 
    #     spawn=UsdFileCfg(
    #         usd_path=f"{project_root}/assets/objects/PackingTable/PackingTable.usd",    # table model file
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),   
    #     ),
    # )
    # packing_table_6 = AssetBaseCfg(
    #     prim_path="/World/envs/env_.*/PackingTable_6",   
    #     init_state=AssetBaseCfg.InitialStateCfg(pos=[0.0, -5, -0.2],  
    #                                             rot=[1.0, 0.0, 0.0, 0.0]), 
    #     spawn=UsdFileCfg(
    #         usd_path=f"{project_root}/assets/objects/PackingTable/PackingTable.usd",    # table model file
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),   
    #     ),
    # )
    # Object
    # 2. object configuration (cylinder)     
    object = RigidObjectCfg(
        prim_path="/World/envs/env_.*/Object",    # object in the scene
        init_state=RigidObjectCfg.InitialStateCfg(pos=[-0.35, 0.40, 0.84], # initial position (pos) 
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

    # plate=RigidObjectCfg(
    #     prim_path="/World/envs/env_.0/plate",    # object in the scene
    #     init_state=RigidObjectCfg.InitialStateCfg(pos=[-0.35, 0.60, 0.84], # initial position (pos) 
    #                                               rot=[1, 0, 0, 0]), # initial rotation (rot)
    #     spawn = sim_utils.CuboidCfg(
    #         size=[0.30, 0.20, 0.01],
            
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(
    #         ),    # rigid body properties configuration (rigid_props)
    #         mass_props=sim_utils.MassPropertiesCfg(mass=0.4),    # mass properties configuration (mass)
    #         collision_props=sim_utils.CollisionPropertiesCfg(),    # collision properties configuration (collision_props)
    #         visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.15, 0.15, 0.15), metallic=1.0),    # visual material configuration (visual_material)
    #         physics_material=sim_utils.RigidBodyMaterialCfg(
    #             friction_combine_mode="max",    # friction combine mode
    #             restitution_combine_mode="min",    # restitution combine mode
    #             static_friction=1.5,    # static friction coefficient
    #             dynamic_friction=1.5,    # dynamic friction coefficient
    #             restitution=0.0,    # restitution coefficient (no restitution)
    #         ),
    #     ),
    # )

    # cubeonplate=RigidObjectCfg(
    #     prim_path="/World/envs/env_.0/plate/cube",
    #     init_state=RigidObjectCfg.InitialStateCfg(pos=[-0.35, 0.60, 0.84], # initial position (pos) 
    #                                               rot=[1, 0, 0, 0]), # initial rotation (rot)
    #     spawn = sim_utils.CuboidCfg(
    #         size=[0.10, 0.10, 0.1],
            
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(
    #         ),    # rigid body properties configuration (rigid_props)
    #         mass_props=sim_utils.MassPropertiesCfg(mass=0.4),    # mass properties configuration (mass)
    #         collision_props=sim_utils.CollisionPropertiesCfg(),    # collision properties configuration (collision_props)
    #         visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.15, 0.15, 0.15), metallic=1.0),    # visual material configuration (visual_material)
    #         physics_material=sim_utils.RigidBodyMaterialCfg(
    #             friction_combine_mode="max",    # friction combine mode
    #             restitution_combine_mode="min",    # restitution combine mode
    #             static_friction=1.5,    # static friction coefficient
    #             dynamic_friction=1.5,    # dynamic friction coefficient
    #             restitution=0.0,    # restitution coefficient (no restitution)
    #         ),
    #     ),

    # )
    
    


    # usd_netted = AssetBaseCfg( ## 这个还是不行(还看不懂原因)
    #     prim_path="/World/envs/env_.*/netted",   
    #     init_state=AssetBaseCfg.InitialStateCfg(pos=[3.5, 0.55, 0.84],  
    #                                             rot=[1.0, 0.0, 0.0, 0.0]), 
    #     spawn=UsdFileCfg(
    #         #usd_path=f"{project_root}/myusd/chair/chair.usd",    # table model file  
    #         #usd_path=f"{project_root}/myusd/Objects/zuantou/zuantou.usd", 
    #         #usd_path=f"{project_root}/myusd/Industrial/Assets/ArchVis/Industrial/Shelves/RackLargeEmpty_A1.usd", 
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=False), 
    #     ),
    # )
    # zuantou=RigidObjectCfg( # 据说我这玩意不是单关节的刚体
    #     prim_path="/World/envs/env_.*/zuantou",
    #     init_state=RigidObjectCfg.InitialStateCfg(pos=[-0.35, 0.60, 0.84], # initial position (pos) 
    #                                               rot=[1, 0, 0, 0]),
    #     spawn=UsdFileCfg(
    #         usd_path=f"{project_root}/myusd/Objects/zuantou/zuantou.usd",
    #         rigid_props=sim_utils.RigidBodyPropertiesCfg(
    #         ),
    #         mass_props=sim_utils.MassPropertiesCfg(mass=0.4),

    #     ), 

    # )



#     dog= ArticulationCfg(
#         prim_path="/World/envs/env_.*/dog",   
#         spawn=UsdFileCfg(        
#             usd_path=f"{project_root}/IsaacLab/source/isaaclab_assets/data/Robots/ANYbotics/anymal_d.usd",
#             articulation_props=sim_utils.ArticulationRootPropertiesCfg(
#                 enabled_self_collisions=True,
#                 solver_position_iteration_count=4,
#                 solver_velocity_iteration_count=0,),        
#             rigid_props=sim_utils.RigidBodyPropertiesCfg(
#                 disable_gravity=False,),),
#         actuators={
#             "dog_joints": ImplicitActuatorCfg(
#                 joint_names_expr=[".*"],  
#                 stiffness=80.0,           
#                 damping=2.0,),},
#         init_state=ArticulationCfg.InitialStateCfg(pos=[-3.5, 0.55, 0.5]), # 稍微调高点，防止掉出地面
# )



    # Ground plane
    # 3. ground configuration
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


print("=====onetable脚本结束=====")