from teleop.utils.experiment_commands import (
    build_recording_command,
    build_sim_command,
    make_trial_name,
)
from teleop.utils.experiment_session_utils import render_csv_row
from teleop.utils.experiment_tasks import get_target_zone_fields
from teleop.utils.experiment_tasks import get_task_definition


def build_plan_rows(participant_ids, task_ids, trials_per_task):
    rows = []
    for participant_id in participant_ids:
        for task_id in task_ids:
            task = get_task_definition(task_id)
            for trial_index in range(1, trials_per_task + 1):
                rows.append(
                    {
                        "participant_id": participant_id,
                        "task_id": task_id,
                        "scenario_id": task["scenario_id"],
                        "trial_index": trial_index,
                        "trial_name": make_trial_name(task_id, participant_id, trial_index),
                        "task_goal": task["task_goal"],
                    }
                )
    return rows


def build_csv_row_skeleton(row):
    target_zone = get_target_zone_fields(row["task_id"])
    return {
        "participant_id": row["participant_id"],
        "trial_id": str(row["trial_index"]),
        "task_id": row["task_id"],
        "scenario_id": row["scenario_id"],
        "target_zone_shape": target_zone["target_zone_shape"],
        "target_zone_radius_m": target_zone["target_zone_radius_m"],
        "success": "",
        "duration_s": "",
        "regrasp_count": "",
        "micro_adjust_count": "",
        "alignment_error_mm": "",
        "collision_count": "",
        "difficulty_score": "",
        "fatigue_score": "",
        "control_score": "",
        "notes": "",
    }


def render_markdown_plan(rows, task_dir, img_server_ip):
    lines = [
        "# First-Round Experiment Plan",
        "",
        "## Trial Table",
        "",
        "| Participant | Task | Scenario | Trial | Goal |",
        "| --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {row['participant_id']} | {row['task_id']} | {row['scenario_id']} | "
            f"{row['trial_name']} | {row['task_goal']} |"
        )

    lines.extend(["", "## Commands", ""])

    for row in rows:
        lines.extend(
            [
                f"### {row['trial_name']}",
                "",
                "Simulation Command:",
                "```bash",
                build_sim_command(row["task_id"]),
                "```",
                "",
                "Recording Command:",
                "```bash",
                build_recording_command(
                    row["task_id"],
                    participant_id=row["participant_id"],
                    trial_index=row["trial_index"],
                    task_dir=task_dir,
                    img_server_ip=img_server_ip,
                ),
                "```",
                "",
                "CSV Row Skeleton:",
                "```csv",
                render_csv_row(build_csv_row_skeleton(row)),
                "```",
                "",
            ]
        )

    return "\n".join(lines)
