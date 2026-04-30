import csv
import io
import json
from pathlib import Path

from teleop.utils.experiment_commands import (
    build_recording_command,
    build_sim_command,
    make_trial_name,
)
from teleop.utils.experiment_tasks import get_target_zone_fields
from teleop.utils.experiment_tasks import get_task_definition


TRIAL_FIELDNAMES = (
    "participant_id",
    "trial_id",
    "task_id",
    "scenario_id",
    "target_zone_shape",
    "target_zone_radius_m",
    "trial_name",
    "episode_dir",
    "episode_count",
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
    target_zone = get_target_zone_fields(task_id)
    return {
        "participant_id": participant_id,
        "trial_id": str(trial_index),
        "task_id": task_id,
        "scenario_id": task["scenario_id"],
        "target_zone_shape": target_zone["target_zone_shape"],
        "target_zone_radius_m": target_zone["target_zone_radius_m"],
        "trial_name": make_trial_name(task_id, participant_id, trial_index),
        "episode_dir": "",
        "episode_count": "",
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


def load_trial_rows(csv_path):
    csv_path = Path(csv_path)
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def overwrite_trial_rows(csv_path, rows):
    csv_path = Path(csv_path)
    initialize_csv_if_missing(csv_path)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TRIAL_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def upsert_trial_row(csv_path, row):
    rows = load_trial_rows(csv_path)
    replaced = False
    for idx, existing in enumerate(rows):
        if existing.get("trial_name") == row["trial_name"]:
            rows[idx] = row
            replaced = True
            break
    if not replaced:
        rows.append(row)
    overwrite_trial_rows(csv_path, rows)


def summarize_trial_directory(trial_dir):
    trial_dir = Path(trial_dir)
    if not trial_dir.exists():
        return {
            "trial_dir": str(trial_dir),
            "episode_count": 0,
            "latest_episode_dir": "",
            "duration_s": 0.0,
            "episodes": [],
        }

    episode_dirs = sorted(
        path for path in trial_dir.iterdir() if path.is_dir() and path.name.startswith("episode_")
    )
    episodes = []
    total_duration_s = 0.0
    for episode_dir in episode_dirs:
        data_path = episode_dir / "data.json"
        if not data_path.exists():
            continue
        payload = json.loads(data_path.read_text(encoding="utf-8"))
        fps = float(payload.get("info", {}).get("image", {}).get("fps", 0) or 0)
        item_count = len(payload.get("data", []))
        duration_s = round((item_count / fps), 3) if fps > 0 else 0.0
        total_duration_s += duration_s
        episodes.append(
            {
                "episode_dir": str(episode_dir),
                "item_count": item_count,
                "fps": fps,
                "duration_s": duration_s,
                "goal": payload.get("text", {}).get("goal", ""),
            }
        )

    latest_episode_dir = episodes[-1]["episode_dir"] if episodes else ""
    return {
        "trial_dir": str(trial_dir),
        "episode_count": len(episodes),
        "latest_episode_dir": latest_episode_dir,
        "duration_s": round(total_duration_s, 3),
        "episodes": episodes,
    }


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
