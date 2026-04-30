import argparse
import zipfile
from pathlib import Path


PROJECT_ROOT = Path("/home/ubuntu/workspaces/xr_teleoperate_local")
DEFAULT_TOOL_ARCHIVES = {
    "wrench": Path("/home/ubuntu/下载/3d_models_of_tools/wrench.zip"),
    "cordless_drill": Path("/home/ubuntu/下载/3d_models_of_tools/cordless_drill.zip"),
    "hammer": Path("/home/ubuntu/下载/3d_models_of_tools/hammer.zip"),
    "phillips": Path("/home/ubuntu/下载/3d_models_of_tools/phillips.zip"),
    "flat_head_screw": Path("/home/ubuntu/下载/3d_models_of_tools/flat_head_screw.zip"),
}


def inspect_asset_archive(zip_path):
    zip_path = Path(zip_path)
    obj_files = []
    mtl_files = []
    texture_files = []
    root_dirs = set()

    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.namelist():
            if member.endswith("/"):
                continue
            path = Path(member)
            if len(path.parts) > 1:
                root_dirs.add(path.parts[0])
            suffix = path.suffix.lower()
            if suffix == ".obj":
                obj_files.append(member)
            elif suffix == ".mtl":
                mtl_files.append(member)
            elif suffix in {".jpg", ".jpeg", ".png"}:
                texture_files.append(member)

    return {
        "zip_path": str(zip_path),
        "root_dir": sorted(root_dirs)[0] if root_dirs else "",
        "obj_files": sorted(obj_files),
        "mtl_files": sorted(mtl_files),
        "texture_files": sorted(texture_files),
    }


def build_import_plan(asset_name, zip_path=None):
    if zip_path is None:
        try:
            zip_path = DEFAULT_TOOL_ARCHIVES[asset_name]
        except KeyError as exc:
            raise ValueError(f"Unsupported asset_name: {asset_name}") from exc

    inspection = inspect_asset_archive(zip_path)
    if not inspection["obj_files"]:
        raise ValueError(f"No OBJ file found in archive: {zip_path}")

    extract_dir = PROJECT_ROOT / "unitree_sim_isaaclab" / "assets" / "external_tools" / asset_name / "source"
    usd_target = (
        PROJECT_ROOT
        / "unitree_sim_isaaclab"
        / "myusd"
        / "Objects"
        / "external_tools"
        / asset_name
        / f"{asset_name}.usd"
    )
    obj_entry = extract_dir / inspection["obj_files"][0]
    mtl_entry = extract_dir / inspection["mtl_files"][0] if inspection["mtl_files"] else None

    return {
        "asset_name": asset_name,
        "zip_path": str(Path(zip_path)),
        "extract_dir": str(extract_dir),
        "obj_entry": str(obj_entry),
        "mtl_entry": str(mtl_entry) if mtl_entry else None,
        "usd_target": str(usd_target),
        "inspection": inspection,
    }


def render_import_plan(asset_name, zip_path=None):
    plan = build_import_plan(asset_name, zip_path=zip_path)
    zip_arg = str(Path(plan["zip_path"]))
    extract_dir = plan["extract_dir"]
    lines = [
        f"Asset Name: {plan['asset_name']}",
        f"Archive: {plan['zip_path']}",
        f"Extract Dir: {extract_dir}",
        f"OBJ Entry: {plan['obj_entry']}",
        f"USD Target: {plan['usd_target']}",
        "",
        "Recommended Commands:",
        f"mkdir -p '{extract_dir}'",
        f"unzip -o '{zip_arg}' -d '{extract_dir}'",
        "",
        "Notes:",
        "- Verify scale and collision after import.",
        "- Keep the source OBJ/MTL/JPG bundle untouched for reproducibility.",
        "- Import to USD under unitree_sim_isaaclab/myusd/Objects/external_tools/<asset_name>/.",
    ]
    if plan["mtl_entry"]:
        lines.insert(4, f"MTL Entry: {plan['mtl_entry']}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Inspect external tool archives and render a standard import plan.")
    parser.add_argument("asset_name", choices=sorted(DEFAULT_TOOL_ARCHIVES.keys()))
    parser.add_argument("--zip-path", default=None, help="Override the default archive path.")
    args = parser.parse_args()

    print(render_import_plan(args.asset_name, zip_path=args.zip_path))


if __name__ == "__main__":
    main()
