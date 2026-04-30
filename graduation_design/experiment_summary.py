import argparse
import csv
from pathlib import Path


NUMERIC_FIELDS = (
    "duration_s",
    "regrasp_count",
    "micro_adjust_count",
    "alignment_error_mm",
    "collision_count",
    "difficulty_score",
    "fatigue_score",
    "control_score",
)


def _parse_boolish(value):
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return True
    if normalized in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"Unsupported success value: {value!r}")


def _parse_optional_float(value):
    if value is None:
        return None
    normalized = str(value).strip()
    if normalized == "":
        return None
    return float(normalized)


def load_records(csv_path):
    records = []
    with Path(csv_path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            record = dict(row)
            record["success"] = _parse_boolish(row["success"])
            for field in NUMERIC_FIELDS:
                parsed = _parse_optional_float(row.get(field))
                if parsed is not None and field not in {"duration_s", "alignment_error_mm"}:
                    parsed = int(parsed)
                record[field] = parsed
            records.append(record)
    return records


def _mean(values):
    present = [value for value in values if value is not None]
    if not present:
        return None
    return sum(present) / len(present)


def _summarize_group(records):
    return {
        "trial_count": len(records),
        "success_rate": sum(1 for row in records if row["success"]) / len(records),
        "mean_duration_s": _mean(row["duration_s"] for row in records),
        "mean_regrasp_count": _mean(row["regrasp_count"] for row in records),
        "mean_micro_adjust_count": _mean(row["micro_adjust_count"] for row in records),
        "mean_alignment_error_mm": _mean(row["alignment_error_mm"] for row in records),
        "mean_collision_count": _mean(row["collision_count"] for row in records),
        "mean_difficulty_score": _mean(row["difficulty_score"] for row in records),
        "mean_fatigue_score": _mean(row["fatigue_score"] for row in records),
        "mean_control_score": _mean(row["control_score"] for row in records),
    }


def summarize_records(records):
    if not records:
        raise ValueError("At least one record is required.")

    task_groups = {}
    for row in records:
        task_groups.setdefault(row["task_id"], []).append(row)

    return {
        "overall": _summarize_group(records),
        "tasks": {
            task_id: _summarize_group(task_records)
            for task_id, task_records in sorted(task_groups.items())
        },
    }


def _format_metric(value, *, is_percent=False):
    if value is None:
        return "-"
    if is_percent:
        return f"{value * 100:.1f}%"
    if isinstance(value, int):
        return str(value)
    return f"{value:.2f}"


def render_markdown(summary):
    overall = summary["overall"]
    lines = [
        "# Graduation Design Experiment Summary",
        "",
        "## Overall Summary",
        "",
        f"- Trials: {overall['trial_count']}",
        f"- Success rate: {_format_metric(overall['success_rate'], is_percent=True)}",
        f"- Mean duration (s): {_format_metric(overall['mean_duration_s'])}",
        f"- Mean regrasp count: {_format_metric(overall['mean_regrasp_count'])}",
        f"- Mean micro-adjust count: {_format_metric(overall['mean_micro_adjust_count'])}",
        f"- Mean alignment error (mm): {_format_metric(overall['mean_alignment_error_mm'])}",
        f"- Mean collision count: {_format_metric(overall['mean_collision_count'])}",
        f"- Mean difficulty score: {_format_metric(overall['mean_difficulty_score'])}",
        f"- Mean fatigue score: {_format_metric(overall['mean_fatigue_score'])}",
        f"- Mean control score: {_format_metric(overall['mean_control_score'])}",
        "",
        "## Per-Task Summary",
        "",
        "| Task | Trials | Success Rate | Mean Duration (s) | Mean Regrasp | Mean Micro-Adjust | Mean Alignment Error (mm) | Mean Collisions |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for task_id, task_summary in summary["tasks"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    task_id,
                    str(task_summary["trial_count"]),
                    _format_metric(task_summary["success_rate"], is_percent=True),
                    _format_metric(task_summary["mean_duration_s"]),
                    _format_metric(task_summary["mean_regrasp_count"]),
                    _format_metric(task_summary["mean_micro_adjust_count"]),
                    _format_metric(task_summary["mean_alignment_error_mm"]),
                    _format_metric(task_summary["mean_collision_count"]),
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Summarize graduation design experiment CSV records.")
    parser.add_argument("csv_path", help="CSV file containing experiment records.")
    args = parser.parse_args()

    summary = summarize_records(load_records(args.csv_path))
    print(render_markdown(summary), end="")


if __name__ == "__main__":
    main()
