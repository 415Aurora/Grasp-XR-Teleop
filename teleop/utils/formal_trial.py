import argparse
import json
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from teleop.utils.experiment_commands import build_recording_command, build_sim_command
from teleop.utils.experiment_session_utils import (
    TRIAL_FIELDNAMES,
    build_trial_row,
    initialize_csv_if_missing,
    summarize_trial_directory,
    upsert_trial_row,
)


DEFAULT_TASK_DIR = "./teleop/utils/data/graduation_design"
DEFAULT_CSV_PATH = "./docs/graduation_design/experiment_log_template.csv"


def build_parser():
    parser = argparse.ArgumentParser(
        description="Formal-trial helper for graduation-design teleoperation experiments."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("prepare", "commands", "summarize-episodes", "update-record"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("task_id", choices=["A1", "A2", "B1", "C1"], nargs="?", default="A2")
        subparser.add_argument("--participant-id", default="P01")
        subparser.add_argument("--trial-index", type=int, default=1)
        subparser.add_argument("--task-dir", default=DEFAULT_TASK_DIR)
        subparser.add_argument("--img-server-ip", default="100.79.86.139")

    subparsers.choices["prepare"].add_argument("--csv-path", default=DEFAULT_CSV_PATH)

    subparsers.choices["summarize-episodes"].add_argument(
        "--trial-dir",
        default=None,
        help="Directory containing episode_XXXX subdirectories. Defaults to <task-dir>/<trial_name>.",
    )

    update_parser = subparsers.choices["update-record"]
    update_parser.add_argument("--csv-path", default=DEFAULT_CSV_PATH)
    update_parser.add_argument("--trial-dir", default=None)
    update_parser.add_argument("--success", choices=["success", "failure", "1", "0"], required=True)
    update_parser.add_argument("--duration-s", type=float, default=None)
    update_parser.add_argument("--regrasp-count", type=int, default=0)
    update_parser.add_argument("--micro-adjust-count", type=int, default=0)
    update_parser.add_argument("--alignment-error-mm", default="")
    update_parser.add_argument("--collision-count", type=int, default=0)
    update_parser.add_argument("--difficulty-score", type=int, default=0)
    update_parser.add_argument("--fatigue-score", type=int, default=0)
    update_parser.add_argument("--control-score", type=int, default=0)
    update_parser.add_argument("--notes", default="")
    return parser


def build_command_payload(args, row):
    return {
        "trial_name": row["trial_name"],
        "trial_dir": str(Path(args.task_dir) / row["trial_name"]),
        "csv_path": getattr(args, "csv_path", DEFAULT_CSV_PATH),
        "sim_command": build_sim_command(args.task_id),
        "teleop_command": build_recording_command(
            args.task_id,
            participant_id=args.participant_id,
            trial_index=args.trial_index,
            task_dir=args.task_dir,
            img_server_ip=args.img_server_ip,
        ),
        "csv_fieldnames": list(TRIAL_FIELDNAMES),
    }


def resolve_trial_dir(args, row):
    if args.trial_dir:
        return Path(args.trial_dir)
    return Path(args.task_dir) / row["trial_name"]


def cmd_prepare(args):
    row = build_trial_row(args.task_id, args.participant_id, args.trial_index)
    trial_dir = Path(args.task_dir) / row["trial_name"]
    trial_dir.mkdir(parents=True, exist_ok=True)
    initialize_csv_if_missing(args.csv_path)
    upsert_trial_row(args.csv_path, row)
    print(json.dumps(build_command_payload(args, row), ensure_ascii=False, indent=2))


def cmd_commands(args):
    row = build_trial_row(args.task_id, args.participant_id, args.trial_index)
    print(json.dumps(build_command_payload(args, row), ensure_ascii=False, indent=2))


def cmd_summarize_episodes(args):
    row = build_trial_row(args.task_id, args.participant_id, args.trial_index)
    print(json.dumps(summarize_trial_directory(resolve_trial_dir(args, row)), ensure_ascii=False, indent=2))


def cmd_update_record(args):
    row = build_trial_row(args.task_id, args.participant_id, args.trial_index)
    summary = summarize_trial_directory(resolve_trial_dir(args, row))
    row["episode_dir"] = summary["latest_episode_dir"]
    row["episode_count"] = str(summary["episode_count"])
    row["success"] = "1" if args.success in {"success", "1"} else "0"
    row["duration_s"] = str(args.duration_s if args.duration_s is not None else summary["duration_s"])
    row["regrasp_count"] = str(args.regrasp_count)
    row["micro_adjust_count"] = str(args.micro_adjust_count)
    row["alignment_error_mm"] = str(args.alignment_error_mm)
    row["collision_count"] = str(args.collision_count)
    row["difficulty_score"] = str(args.difficulty_score)
    row["fatigue_score"] = str(args.fatigue_score)
    row["control_score"] = str(args.control_score)
    row["notes"] = args.notes
    initialize_csv_if_missing(args.csv_path)
    upsert_trial_row(args.csv_path, row)
    print(json.dumps(row, ensure_ascii=False, indent=2))


def main():
    args = build_parser().parse_args()
    {
        "prepare": cmd_prepare,
        "commands": cmd_commands,
        "summarize-episodes": cmd_summarize_episodes,
        "update-record": cmd_update_record,
    }[args.command](args)


if __name__ == "__main__":
    main()
