# 智能建造工具抓取毕设工作区

本目录用于固化毕业设计的任务定义、实验记录模板和扩展资产信息，避免实验过程中任务描述漂移。

## 主实验任务

- `A1`：螺栓抓取并放入指定容器，对应现有 `e1`
- `A2`：扳手抓取并转移到圆形目标放置区，对应现有 `e2_wrench`
- `B1`：工具/工件精细对位，对应现有 `e3`
- `C1`：带工具执行简化作业动作，对应现有 `e4`

当前建议作为论文主线的核心任务是 `A2`。

## 推荐实验流程

1. 启动 `sim_main.py` 对应任务场景
2. 用 `python -m graduation_design.task_runner <task_id>` 生成标准命令
3. 用 `teleop_hand_and_arm.py --record` 采集遥操作轨迹
3. 将单次实验结果登记到 `experiment_log_template.csv`
4. 用 `python -m graduation_design.experiment_summary <csv>` 输出汇总表
5. 将成功案例、失败案例截图和汇总表纳入论文结果章节

## 现有录制入口

`teleop/teleop_hand_and_arm.py` 已支持以下与论文实验直接相关的参数：

- `--record`
- `--task-dir`
- `--task-name`
- `--task-goal`
- `--task-desc`
- `--task-steps`

建议为每个正式任务统一填写：

- `A1`：bolt grasp and transfer
- `A2`：wrench grasp and transfer to circular target zone
- `B1`：tool alignment
- `C1`：tool-assisted operation

## 标准命令生成

使用下面的命令为正式实验生成统一的仿真和录制命令：

```bash
python3 -m graduation_design.task_runner A1 --participant-id P01 --trial-index 1
python3 -m graduation_design.task_runner B1 --participant-id P02 --trial-index 3
```

该工具会输出：

- 当前研究任务 ID
- 对应的仿真场景 ID
- 标准化试次名称，例如 `A1_P01_T01`
- `sim_main.py` 启动命令
- `teleop_hand_and_arm.py --record` 录制命令

这样可以避免每次实验手工改 `--task-name`、`--task-goal`、`--task-desc`、`--task-steps`。

如果要执行单次正式实验并同时拿到 CSV 记录骨架，使用：

```bash
python3 -m graduation_design.experiment_session A1 --participant-id P01 --trial-index 1
python3 -m graduation_design.experiment_session C1 --participant-id P02 --trial-index 4
```

如果要按正式试次流程一次性完成“试次目录初始化 + 命令生成 + episode 汇总 + CSV 回填”，使用：

```bash
python3 teleop/utils/formal_trial.py prepare A2 --participant-id P01 --trial-index 1
python3 teleop/utils/formal_trial.py summarize-episodes A2 --participant-id P01 --trial-index 1
python3 teleop/utils/formal_trial.py update-record A2 --participant-id P01 --trial-index 1 --success success
```

更完整的逐步实验说明见：

- `docs/graduation_design/experiment_runbook.md`

## 论文主线任务规范

建议将本科毕设的主实验正式定义为：

- 核心任务：扳手抓取并转移至圆形目标放置区
- 仿真场景：`e2_wrench`
- 目标区形状：圆形
- 目标区半径：`0.12 m`
- 成功判据：扳手被抓起、转移并释放后最终稳定停留在圆形目标区内

后续的姿态调整和简化操作任务建议作为扩展展示，不作为论文主体统计任务。

## 扩展资产池

位于 `/home/ubuntu/下载/3d_models_of_tools`，当前已确认包含：

- `hammer.zip`
- `wrench.zip`
- `phillips.zip`
- `cordless_drill.zip`
- `flat_head_screw.zip`

这些资产当前是 `OBJ + MTL + JPG` 组合，适合作为扩展任务池，不阻塞主实验线。

## 外部工具导入

为了把真实工具模型逐步接入仿真，当前工作区新增了统一的导入规格和 Isaac 侧导入脚本：

```bash
cd /home/ubuntu/workspaces/xr_teleoperate_local
python3 unitree_sim_isaaclab/tools/render_tool_asset_plan.py wrench
python3 unitree_sim_isaaclab/tools/render_mesh_import_command.py wrench
```

如果需要查看扳手资产的标准导入命令，可以执行：

```bash
python3 unitree_sim_isaaclab/tools/render_mesh_import_command.py wrench
```

实际生成 USD 时，在 `unitree_sim_isaaclab/tools/` 目录下运行：

```bash
python3 import_external_mesh.py --asset-name wrench --headless
```

默认输出位置为：

`unitree_sim_isaaclab/myusd/Objects/external_tools/wrench/wrench.usd`

## 扳手扩展场景

主实验线里的 `A2 -> e2` 继续保留，当前新增的是平行扩展场景 `e2_wrench`。

- 用途：把 `wrench.usd` 作为真实工具模型放入现有抓取场景
- 目标：先单独验证扳手的抓取、碰撞和放置稳定性
- 原则：扩展场景先验证通过，再决定是否回并到主实验任务线

直接启动扩展场景：

```bash
cd /home/ubuntu/workspaces/xr_teleoperate_local/unitree_sim_isaaclab
python3 sim_main.py --device cpu --enable_cameras --task e2_wrench --enable_dex3_dds --robot_type g129
```
