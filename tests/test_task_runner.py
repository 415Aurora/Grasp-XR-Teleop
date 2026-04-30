import unittest

from graduation_design.task_runner import (
    build_recording_command,
    build_sim_command,
    get_task_definition,
    make_trial_name,
)


class TaskRunnerTests(unittest.TestCase):
    def test_get_task_definition_exposes_expected_mapping(self):
        task = get_task_definition("A1")

        self.assertEqual(task["scenario_id"], "e1")
        self.assertEqual(task["task_name"], "bolt-grasp-transfer")
        self.assertIn("bolt", task["task_goal"].lower())

    def test_make_trial_name_uses_participant_and_trial_index(self):
        name = make_trial_name("A1", "P03", 7)

        self.assertEqual(name, "A1_P03_T07")

    def test_build_sim_command_targets_expected_scene(self):
        command = build_sim_command("B1")

        self.assertIn("python sim_main.py", command)
        self.assertIn("--task e3", command)
        self.assertIn("--enable_dex3_dds", command)
        self.assertIn("--robot_type g129", command)

    def test_a2_uses_wrench_extension_scene(self):
        task = get_task_definition("A2")
        command = build_sim_command("A2")

        self.assertEqual(task["scenario_id"], "e2_wrench")
        self.assertIn("--task e2_wrench", command)
        self.assertIn("0.12 m radius circular target zone", task["task_desc"])

    def test_build_recording_command_contains_record_metadata(self):
        command = build_recording_command(
            "C1",
            participant_id="P01",
            trial_index=2,
            task_dir="./teleop/utils/data/graduation_design",
            img_server_ip="100.79.86.139",
        )

        self.assertIn("python teleop_hand_and_arm.py", command)
        self.assertIn("--record", command)
        self.assertIn("--task-name C1_P01_T02", command)
        self.assertIn("--task-dir ./teleop/utils/data/graduation_design", command)
        self.assertIn("--img-server-ip 100.79.86.139", command)
        self.assertIn("--task-goal", command)
        self.assertIn("--task-desc", command)
        self.assertIn("--task-steps", command)


if __name__ == "__main__":
    unittest.main()
