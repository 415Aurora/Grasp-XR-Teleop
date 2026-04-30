import csv
import io
import unittest

from graduation_design.experiment_session import (
    TRIAL_FIELDNAMES,
    append_trial_row,
    build_trial_row,
    initialize_csv_if_missing,
    render_csv_row,
    render_session_checklist,
)


class ExperimentSessionTests(unittest.TestCase):
    def test_build_trial_row_prefills_task_metadata(self):
        row = build_trial_row("B1", participant_id="P02", trial_index=4)

        self.assertEqual(row["participant_id"], "P02")
        self.assertEqual(row["trial_id"], "4")
        self.assertEqual(row["task_id"], "B1")
        self.assertEqual(row["scenario_id"], "e3")
        self.assertEqual(row["success"], "")
        self.assertEqual(row["notes"], "")

    def test_render_csv_row_matches_template_columns(self):
        row = build_trial_row("A2", participant_id="P01", trial_index=2)

        rendered = render_csv_row(row)
        parsed = next(csv.DictReader(io.StringIO(",".join(TRIAL_FIELDNAMES) + "\n" + rendered)))

        self.assertEqual(list(parsed.keys()), list(TRIAL_FIELDNAMES))
        self.assertEqual(parsed["task_id"], "A2")
        self.assertEqual(parsed["scenario_id"], "e2_wrench")
        self.assertEqual(parsed["target_zone_shape"], "circle")
        self.assertEqual(parsed["target_zone_radius_m"], "0.12")

    def test_render_session_checklist_contains_commands_and_log_row(self):
        checklist = render_session_checklist(
            "C1",
            participant_id="P03",
            trial_index=1,
            task_dir="./teleop/utils/data/graduation_design",
            img_server_ip="100.79.86.139",
        )

        self.assertIn("Task ID: C1", checklist)
        self.assertIn("Simulation Command:", checklist)
        self.assertIn("--task e4", checklist)
        self.assertIn("Recording Command:", checklist)
        self.assertIn("--task-name C1_P03_T01", checklist)
        self.assertIn("CSV Row:", checklist)

    def test_initialize_csv_if_missing_writes_header(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "results.csv"
            initialize_csv_if_missing(csv_path)
            content = csv_path.read_text(encoding="utf-8").strip()

        self.assertEqual(content, ",".join(TRIAL_FIELDNAMES))

    def test_append_trial_row_creates_file_and_appends_row(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "results.csv"
            row = build_trial_row("A1", participant_id="P01", trial_index=1)
            append_trial_row(csv_path, row)
            content = csv_path.read_text(encoding="utf-8").strip().splitlines()

        self.assertEqual(content[0], ",".join(TRIAL_FIELDNAMES))
        self.assertEqual(content[1], render_csv_row(row))


if __name__ == "__main__":
    unittest.main()
