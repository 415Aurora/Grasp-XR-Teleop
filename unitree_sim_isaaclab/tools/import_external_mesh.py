"""Import an external OBJ/STL/FBX tool mesh into a USD asset."""

import argparse
import os
import sys
from pathlib import Path


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from graduation_design.mesh_import import build_mesh_import_spec


def _parse_vec3(value):
    parts = tuple(float(item.strip()) for item in value.split(","))
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Expected three comma-separated values.")
    return parts


def _parse_quat(value):
    parts = tuple(float(item.strip()) for item in value.split(","))
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("Expected four comma-separated values.")
    return parts


def build_parser():
    parser = argparse.ArgumentParser(description="Import an external mesh asset into USD format.")
    parser.add_argument("--asset-name", required=True, help="Registered asset name, for example: wrench.")
    parser.add_argument("--asset-path", default=None, help="Override the source mesh path.")
    parser.add_argument("--output-usd", default=None, help="Override the generated USD output path.")
    parser.add_argument(
        "--collision-approximation",
        default=None,
        choices=["convexDecomposition", "convexHull", "boundingCube", "boundingSphere", "meshSimplification", "none"],
        help="Collision approximation strategy.",
    )
    parser.add_argument("--translation", type=_parse_vec3, default=None, help="Mesh translation as x,y,z.")
    parser.add_argument("--rotation", type=_parse_quat, default=None, help="Mesh rotation quaternion as w,x,y,z.")
    parser.add_argument("--scale", type=_parse_vec3, default=None, help="Mesh scale as x,y,z.")
    parser.add_argument("--mass", type=float, default=None, help="Rigid body mass in kilograms.")
    parser.add_argument(
        "--make-instanceable",
        action="store_true",
        default=None,
        help="Export the geometry as an instanceable USD asset.",
    )
    parser.add_argument("--headless", action="store_true", help="Launch Isaac Sim without GUI.")
    return parser


def resolve_import_spec(args):
    spec = build_mesh_import_spec(args.asset_name)
    overrides = {
        "asset_path": args.asset_path,
        "usd_path": args.output_usd,
        "collision_approximation": args.collision_approximation,
        "translation": args.translation,
        "rotation": args.rotation,
        "scale": args.scale,
        "mass": args.mass,
        "make_instanceable": args.make_instanceable,
    }
    for key, value in overrides.items():
        if value is not None:
            spec[key] = value
    return spec


def _build_app_launcher_argv(headless):
    argv = [sys.argv[0]]
    if headless:
        argv.append("--headless")
    return argv


def main():
    args = build_parser().parse_args()
    spec = resolve_import_spec(args)

    from isaaclab.app import AppLauncher

    original_argv = sys.argv[:]
    try:
        sys.argv = _build_app_launcher_argv(args.headless)
        app_launcher = AppLauncher()
    finally:
        sys.argv = original_argv
    simulation_app = app_launcher.app

    try:
        from isaaclab.sim.converters import MeshConverter, MeshConverterCfg
        from isaaclab.sim.schemas import schemas_cfg
        from isaaclab.utils.assets import check_file_path
        from isaaclab.utils.dict import print_dict

        mesh_path = os.path.abspath(spec["asset_path"])
        if not check_file_path(mesh_path):
            raise ValueError(f"Invalid mesh file path: {mesh_path}")

        dest_path = os.path.abspath(spec["usd_path"])
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        if spec["mass"] is not None:
            mass_props = schemas_cfg.MassPropertiesCfg(mass=spec["mass"])
            rigid_props = schemas_cfg.RigidBodyPropertiesCfg()
        else:
            mass_props = None
            rigid_props = None

        collision_enabled = spec["collision_approximation"] != "none"
        collision_props = schemas_cfg.CollisionPropertiesCfg(collision_enabled=collision_enabled)

        mesh_converter_cfg = MeshConverterCfg(
            mass_props=mass_props,
            rigid_props=rigid_props,
            collision_props=collision_props,
            asset_path=mesh_path,
            force_usd_conversion=True,
            usd_dir=os.path.dirname(dest_path),
            usd_file_name=os.path.basename(dest_path),
            make_instanceable=spec["make_instanceable"],
            collision_approximation=spec["collision_approximation"],
            translation=spec["translation"],
            rotation=spec["rotation"],
            scale=spec["scale"],
        )

        print("-" * 80)
        print(f"Asset Name: {spec['asset_name']}")
        print(f"Input Mesh file: {mesh_path}")
        print("Mesh importer config:")
        print_dict(mesh_converter_cfg.to_dict(), nesting=0)
        print("-" * 80)

        mesh_converter = MeshConverter(mesh_converter_cfg)

        print("Mesh importer output:")
        print(f"Generated USD file: {mesh_converter.usd_path}")
        print("-" * 80)
    finally:
        simulation_app.close()


if __name__ == "__main__":
    main()
