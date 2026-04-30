import unittest

from graduation_design.experiment_summary import (
    load_records,
    render_markdown,
    summarize_records,
)


class ExperimentSummaryTests(unittest.TestCase):
    def test_load_records_normalizes_types(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "records.csv"
            csv_path.write_text(
                "\n".join(
                    [
                        "participant_id,task_id,success,duration_s,regrasp_count,micro_adjust_count,alignment_error_mm,collision_count,difficulty_score,fatigue_score,control_score",
                        "p1,A1,1,10.5,1,2,5.0,0,2,1,4",
                        "p2,A1,false,20.0,3,4,,1,4,3,2",
                    ]
                ),
                encoding="utf-8",
            )

            records = load_records(csv_path)

        self.assertIs(records[0]["success"], True)
        self.assertEqual(records[0]["duration_s"], 10.5)
        self.assertEqual(records[0]["regrasp_count"], 1)
        self.assertIs(records[1]["success"], False)
        self.assertIsNone(records[1]["alignment_error_mm"])

    def test_summarize_records_groups_by_task(self):
        records = [
            {
                "participant_id": "p1",
                "task_id": "A1",
                "success": True,
                "duration_s": 10.0,
                "regrasp_count": 1,
                "micro_adjust_count": 2,
                "alignment_error_mm": 5.0,
                "collision_count": 0,
                "difficulty_score": 2,
                "fatigue_score": 1,
                "control_score": 4,
            },
            {
                "participant_id": "p2",
                "task_id": "A1",
                "success": False,
                "duration_s": 20.0,
                "regrasp_count": 3,
                "micro_adjust_count": 4,
                "alignment_error_mm": None,
                "collision_count": 1,
                "difficulty_score": 4,
                "fatigue_score": 3,
                "control_score": 2,
            },
            {
                "participant_id": "p3",
                "task_id": "B1",
                "success": True,
                "duration_s": 30.0,
                "regrasp_count": 0,
                "micro_adjust_count": 5,
                "alignment_error_mm": 3.0,
                "collision_count": 2,
                "difficulty_score": 5,
                "fatigue_score": 4,
                "control_score": 3,
            },
        ]

        summary = summarize_records(records)

        self.assertEqual(summary["overall"]["trial_count"], 3)
        self.assertAlmostEqual(summary["overall"]["success_rate"], 2 / 3)
        self.assertEqual(summary["tasks"]["A1"]["trial_count"], 2)
        self.assertEqual(summary["tasks"]["A1"]["success_rate"], 0.5)
        self.assertEqual(summary["tasks"]["A1"]["mean_duration_s"], 15.0)
        self.assertEqual(summary["tasks"]["A1"]["mean_alignment_error_mm"], 5.0)
        self.assertEqual(summary["tasks"]["B1"]["mean_micro_adjust_count"], 5.0)

    def test_render_markdown_contains_expected_sections(self):
        summary = {
            "overall": {
                "trial_count": 3,
                "success_rate": 2 / 3,
                "mean_duration_s": 20.0,
                "mean_regrasp_count": 1.33,
                "mean_micro_adjust_count": 3.67,
                "mean_alignment_error_mm": 4.0,
                "mean_collision_count": 1.0,
                "mean_difficulty_score": 3.67,
                "mean_fatigue_score": 2.67,
                "mean_control_score": 3.0,
            },
            "tasks": {
                "A1": {
                    "trial_count": 2,
                    "success_rate": 0.5,
                    "mean_duration_s": 15.0,
                    "mean_regrasp_count": 2.0,
                    "mean_micro_adjust_count": 3.0,
                    "mean_alignment_error_mm": 5.0,
                    "mean_collision_count": 0.5,
                    "mean_difficulty_score": 3.0,
                    "mean_fatigue_score": 2.0,
                    "mean_control_score": 3.0,
                }
            },
        }

        markdown = render_markdown(summary)

        self.assertIn("## Overall Summary", markdown)
        self.assertIn("| Task | Trials | Success Rate |", markdown)
        self.assertIn("| A1 | 2 | 50.0% |", markdown)


if __name__ == "__main__":
    unittest.main()
