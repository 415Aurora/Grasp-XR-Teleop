import argparse
import math
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from isaaclab.assets import RigidObject
    from isaaclab.managers import SceneEntityCfg


PROJECT_ROOT = Path("/home/ubuntu/workspaces/xr_teleoperate_local")


def build_wrench_scene_spec():
    return {
        "scenario_id": "e2_wrench",
        "asset_name": "wrench",
        "usd_path": str(
            PROJECT_ROOT
            / "unitree_sim_isaaclab"
            / "myusd"
            / "Objects"
            / "external_tools"
            / "wrench"
            / "wrench.usd"
        ),
        "object_pos": (-3.35, 0.40, 0.84),
        "object_rot": (1.0, 0.0, 0.0, 0.0),
        "object_scale": (0.0254, 0.0254, 0.0254),
        "target_zone_shape": "circle",
        "target_zone_radius_m": 0.12,
        "target_zone_center": (-2.95, 0.40, 0.701),
        "target_zone_height_m": 0.002,
    }


def is_inside_circular_target_zone(point_xy, center_xy, radius):
    return math.dist(point_xy, center_xy) <= radius


def reset_wrench_outside_target_zone(
    env,
    object_cfg=None,
    min_height: float = 0.70,
):
    if object_cfg is None:
        from isaaclab.managers import SceneEntityCfg

        object_cfg = SceneEntityCfg("object")

    spec = build_wrench_scene_spec()
    obj: "RigidObject" = env.scene[object_cfg.name]
    object_pos = obj.data.root_pos_w

    center_x, center_y, _ = spec["target_zone_center"]
    radius = spec["target_zone_radius_m"]

    dx = object_pos[:, 0] - center_x
    dy = object_pos[:, 1] - center_y
    radial_distance = (dx**2 + dy**2).sqrt()
    in_circle = radial_distance <= radius
    above_table = object_pos[:, 2] >= min_height
    done = in_circle & above_table
    return ~done


def build_wrench_sim_command():
    spec = build_wrench_scene_spec()
    return (
        f"python sim_main.py --device cpu --enable_cameras --task {spec['scenario_id']} "
        "--enable_dex3_dds --robot_type g129"
    )


def main():
    parser = argparse.ArgumentParser(description="Render the dedicated wrench extension simulation command.")
    parser.parse_args()
    print(build_wrench_sim_command())


if __name__ == "__main__":
    main()
