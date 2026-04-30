import argparse

from teleop.utils.experiment_commands import (
    build_recording_command,
    build_sim_command,
    make_trial_name,
    render_task_sheet,
)
from teleop.utils.experiment_tasks import TASK_DEFINITIONS, get_task_definition


def main():
    parser = argparse.ArgumentParser(description="Generate standardized commands for graduation design experiments.")
    parser.add_argument("task_id", choices=sorted(TASK_DEFINITIONS.keys()))
    parser.add_argument("--participant-id", default="P01")
    parser.add_argument("--trial-index", type=int, default=1)
    parser.add_argument("--task-dir", default="./teleop/utils/data/graduation_design")
    parser.add_argument("--img-server-ip", default="100.79.86.139")
    args = parser.parse_args()

    print(
        render_task_sheet(
            args.task_id,
            participant_id=args.participant_id,
            trial_index=args.trial_index,
            task_dir=args.task_dir,
            img_server_ip=args.img_server_ip,
        )
    )


if __name__ == "__main__":
    main()
