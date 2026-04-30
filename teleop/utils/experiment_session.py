import argparse

from teleop.utils.experiment_session_utils import (
    TRIAL_FIELDNAMES,
    append_trial_row,
    build_trial_row,
    initialize_csv_if_missing,
    render_csv_row,
    render_session_checklist,
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
