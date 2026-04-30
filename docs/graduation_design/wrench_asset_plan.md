# Wrench Asset Plan

This file tracks the first real-tool expansion path for the graduation design.

## Source Asset

- archive: `/home/ubuntu/下载/3d_models_of_tools/wrench.zip`
- expected type: `OBJ + MTL + JPG`
- role in thesis: first expanded real-tool asset after the main `e1/e2/e3/e4` task line is stable

## Recommended Workflow

1. Inspect the asset bundle:

```bash
python3 -m graduation_design.tool_asset wrench
```

2. Extract the OBJ bundle into the project-local source area:

```bash
mkdir -p /home/ubuntu/workspaces/xr_teleoperate_local/unitree_sim_isaaclab/assets/external_tools/wrench/source
unzip -o /home/ubuntu/下载/3d_models_of_tools/wrench.zip -d /home/ubuntu/workspaces/xr_teleoperate_local/unitree_sim_isaaclab/assets/external_tools/wrench/source
```

3. Import the extracted OBJ into USD using the Isaac-side asset workflow.

```bash
cd /home/ubuntu/workspaces/xr_teleoperate_local/unitree_sim_isaaclab/tools
python3 import_external_mesh.py --asset-name wrench --headless
```

4. Save the imported asset under:

`unitree_sim_isaaclab/myusd/Objects/external_tools/wrench/wrench.usd`

5. Build a dedicated wrench scene only after scale, collision and pose reset behavior are stable.

## Why Wrench First

- It is semantically closest to the existing `A2` and `B1` tasks.
- It is easier to interpret in the thesis than a generic synthetic object.
- It gives a cleaner path from current `e2` toward a real-tool benchmark extension.
