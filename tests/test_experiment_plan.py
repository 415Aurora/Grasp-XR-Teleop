import unittest

from graduation_design.experiment_plan import (
    build_plan_rows,
    render_markdown_plan,
)


class ExperimentPlanTests(unittest.TestCase):
    def test_build_plan_rows_expands_tasks_and_trials(self):
        rows = build_plan_rows(
            participant_ids=["P01"],
            task_ids=["A1", "B1"],
            trials_per_task=2,
        )

        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0]["task_id"], "A1")
        self.assertEqual(rows[0]["trial_name"], "A1_P01_T01")
        self.assertEqual(rows[1]["trial_name"], "A1_P01_T02")
        self.assertEqual(rows[2]["task_id"], "B1")
        self.assertEqual(rows[2]["scenario_id"], "e3")

    def test_render_markdown_plan_contains_table_and_commands(self):
        rows = build_plan_rows(
            participant_ids=["P02"],
            task_ids=["C1"],
            trials_per_task=1,
        )

        markdown = render_markdown_plan(
            rows,
            task_dir="./teleop/utils/data/graduation_design",
            img_server_ip="100.79.86.139",
        )

        self.assertIn("# First-Round Experiment Plan", markdown)
        self.assertIn("| Participant | Task | Scenario | Trial |", markdown)
        self.assertIn("| P02 | C1 | e4 | C1_P02_T01 |", markdown)
        self.assertIn("python sim_main.py --device cpu --enable_cameras --task e4", markdown)
        self.assertIn("python teleop_hand_and_arm.py", markdown)


if __name__ == "__main__":
    unittest.main()
