import argparse

from teleop.utils.experiment_plan_utils import build_plan_rows, render_markdown_plan


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
