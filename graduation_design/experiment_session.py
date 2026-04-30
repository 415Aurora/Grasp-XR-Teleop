import argparse
import csv
import io
from pathlib import Path

from graduation_design.task_runner import (
    build_recording_command,
    build_sim_command,
    get_task_definition,
    make_trial_name,
)


TRIAL_FIELDNAMES = (
    "participant_id",
    "trial_id",
    "task_id",
    "scenario_id",
    "target_zone_shape",
    "target_zone_radius_m",
    "success",
    "duration_s",
    "regrasp_count",
    "micro_adjust_count",
    "alignment_error_mm",
    "collision_count",
    "difficulty_score",
    "fatigue_score",
    "control_score",
    "notes",
)


def build_trial_row(task_id, participant_id, trial_index):
    task = get_task_definition(task_id)
    target_zone_shape = "circle" if task_id == "A2" else ""
    target_zone_radius_m = "0.12" if task_id == "A2" else ""
    return {
        "participant_id": participant_id,
        "trial_id": str(trial_index),
        "task_id": task_id,
        "scenario_id": task["scenario_id"],
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


def render_csv_row(row):
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=TRIAL_FIELDNAMES, lineterminator="")
    writer.writerow(row)
    return buffer.getvalue()


def initialize_csv_if_missing(csv_path):
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if not csv_path.exists():
        csv_path.write_text(",".join(TRIAL_FIELDNAMES) + "\n", encoding="utf-8")


def append_trial_row(csv_path, row):
    csv_path = Path(csv_path)
    initialize_csv_if_missing(csv_path)
    with csv_path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(render_csv_row(row) + "\n")


def render_session_checklist(task_id, participant_id, trial_index, task_dir, img_server_ip):
    task = get_task_definition(task_id)
    trial_name = make_trial_name(task_id, participant_id, trial_index)
    row = build_trial_row(task_id, participant_id, trial_index)
    return "\n".join(
        [
            f"Task ID: {task_id}",
            f"Scenario ID: {task['scenario_id']}",
            f"Participant ID: {participant_id}",
            f"Trial Name: {trial_name}",
            "",
            "Checklist:",
            "1. Start the simulation scene.",
            "2. Start the XR teleoperation recording command.",
            "3. Complete the task and save the episode.",
            "4. Fill the CSV row with outcome metrics.",
            "5. Capture at least one success screenshot and one failure screenshot if available.",
            "6. For A2, verify that the wrench finally rests inside the 0.12 m radius circular target zone.",
            "",
            "Simulation Command:",
            build_sim_command(task_id),
            "",
            "Recording Command:",
            build_recording_command(task_id, participant_id, trial_index, task_dir, img_server_ip),
            "",
            "CSV Row:",
            render_csv_row(row),
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="Generate a per-trial checklist and CSV row for graduation design experiments.")
    parser.add_argument("task_id", choices=["A1", "A2", "B1", "C1"])
    parser.add_argument("--participant-id", default="P01")
    parser.add_argument("--trial-index", type=int, default=1)
    parser.add_argument("--task-dir", default="./teleop/utils/data/graduation_design")
    parser.add_argument("--img-server-ip", default="100.79.86.139")
    parser.add_argument("--append-csv", default=None, help="Append the generated row to the given CSV file.")
    args = parser.parse_args()

    row = build_trial_row(args.task_id, args.participant_id, args.trial_index)
    if args.append_csv:
        append_trial_row(args.append_csv, row)

    print(
        render_session_checklist(
            args.task_id,
            participant_id=args.participant_id,
            trial_index=args.trial_index,
            task_dir=args.task_dir,
            img_server_ip=args.img_server_ip,
        )
    )


if __name__ == "__main__":
    main()
