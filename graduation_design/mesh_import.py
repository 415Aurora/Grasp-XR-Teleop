import argparse
from pathlib import Path


PROJECT_ROOT = Path("/home/ubuntu/workspaces/xr_teleoperate_local")

_ASSET_LIBRARY = {
    "wrench": {
        "asset_path": (
            PROJECT_ROOT
            / "unitree_sim_isaaclab"
            / "assets"
            / "external_tools"
            / "wrench"
            / "source"
            / "Combination_Wrench_v1_L3.123c05d4289b-e966-4438-b0fc-691503f4eb40"
            / "13073_Combination_Wrench_v1_l3.obj"
        ),
        "usd_path": (
            PROJECT_ROOT
            / "unitree_sim_isaaclab"
            / "myusd"
            / "Objects"
            / "external_tools"
            / "wrench"
            / "wrench.usd"
        ),
        "translation": (0.0, 0.0, 0.0),
        "rotation": (1.0, 0.0, 0.0, 0.0),
        "scale": (1.0, 1.0, 1.0),
        "collision_approximation": "convexDecomposition",
        "mass": 0.4,
        "make_instanceable": True,
    },
}


def build_mesh_import_spec(asset_name):
    try:
        defaults = _ASSET_LIBRARY[asset_name]
    except KeyError as exc:
        raise ValueError(f"Unsupported asset_name: {asset_name}") from exc

    spec = {"asset_name": asset_name}
    spec.update(defaults)
    spec["asset_path"] = str(spec["asset_path"])
    spec["usd_path"] = str(spec["usd_path"])
    return spec


def render_mesh_import_command(asset_name):
    spec = build_mesh_import_spec(asset_name)
    return " ".join(
        [
            "python",
            "import_external_mesh.py",
            f"--asset-name {spec['asset_name']}",
            f"--asset-path '{spec['asset_path']}'",
            f"--output-usd '{spec['usd_path']}'",
            f"--collision-approximation {spec['collision_approximation']}",
            f"--mass {spec['mass']}",
            "--make-instanceable",
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="Render the standard mesh import command for a registered asset.")
    parser.add_argument("asset_name", choices=sorted(_ASSET_LIBRARY.keys()))
    args = parser.parse_args()
    print(render_mesh_import_command(args.asset_name))


if __name__ == "__main__":
    main()
