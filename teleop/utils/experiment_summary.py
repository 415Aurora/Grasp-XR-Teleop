import argparse

from teleop.utils.experiment_summary_utils import load_records, render_markdown, summarize_records


def main():
    parser = argparse.ArgumentParser(description="Summarize graduation design experiment CSV records.")
    parser.add_argument("csv_path", help="CSV file containing experiment records.")
    args = parser.parse_args()

    summary = summarize_records(load_records(args.csv_path))
    print(render_markdown(summary), end="")


if __name__ == "__main__":
    main()
