from isaaclab.app import AppLauncher
app_launcher = AppLauncher() 


import sys
from pathlib import Path
project_root=Path(__file__).parent.parent.parent.parent
print(project_root)
sys.path.insert(0, str(project_root))

print("the sim_main is finished!!")


from isaaclab.assets import ArticulationCfg
from tasks.common_scene.base_scene_pickplace_cylindercfg import TableCylinderSceneCfg

from tasks.common_config import  G1RobotPresets, CameraPresets

print("all import is success!!!!")

@configclass
class objectTableSceneCfg(TableCylinderSceneCfg):

    robot:ArticulationCfg=G1RobotPresets.g1_29dof_dex3_base_fix()

    front_camera=CameraPresets.g1_front_camera()
    left__wrist_camera=CameraPresets.left_dex3_wrist_camera()
    right_wrist_camera=CameraPresets.right_dex3_wrist_camera()

print("all procedure is ok")