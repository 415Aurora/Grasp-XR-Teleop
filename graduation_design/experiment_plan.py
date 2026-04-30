

































import argparse

from graduation_design.experiment_session import render_csv_row
from graduation_design.task_runner import (
    build_recording_command,
    build_sim_command,
    get_task_definition,
    make_trial_name,
)


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
    target_zone_shape = "circle" if row["task_id"] == "A2" else ""
    target_zone_radius_m = "0.12" if row["task_id"] == "A2" else ""
    return {
        "participant_id": row["participant_id"],
        "trial_id": str(row["trial_index"]),
        "task_id": row["task_id"],
        "scenario_id": row["scenario_id"],
        "target_zone_shape": target_zone_shape,
        "target_zone_radius_m": target_zone_radius_m,
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


def main():
    parser = argparse.ArgumentParser(description="Generate a first-round experiment plan for graduation design tasks.")
    parser.add_argument("--participant-ids", nargs="+", default=["P01"])
    parser.add_argument("--task-ids", nargs="+", default=["A1", "A2", "B1", "C1"])
    parser.add_argument("--trials-per-task", type=int, default=1)
    parser.add_argument("--task-dir", default="./teleop/utils/data/graduation_design")
    parser.add_argument("--img-server-ip", default="100.79.86.139")
    args = parser.parse_args()

    rows = build_plan_rows(args.participant_ids, args.task_ids, args.trials_per_task)
    print(
        render_markdown_plan(
            rows,
            task_dir=args.task_dir,
            img_server_ip=args.img_server_ip,
        )
    )


if __name__ == "__main__":
    main()
