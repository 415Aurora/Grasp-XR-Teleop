import unittest

from graduation_design.wrench_extension import (
    build_wrench_scene_spec,
    build_wrench_sim_command,
    is_inside_circular_target_zone,
)


class WrenchExtensionTests(unittest.TestCase):
    def test_build_wrench_scene_spec_points_to_registered_extension_scene(self):
        spec = build_wrench_scene_spec()

        self.assertEqual(spec["scenario_id"], "e2_wrench")
        self.assertEqual(spec["asset_name"], "wrench")
        self.assertTrue(spec["usd_path"].endswith("/myusd/Objects/external_tools/wrench/wrench.usd"))
        self.assertEqual(spec["object_pos"], (-3.35, 0.40, 0.84))
        self.assertEqual(spec["object_rot"], (1.0, 0.0, 0.0, 0.0))
        self.assertEqual(spec["object_scale"], (0.0254, 0.0254, 0.0254))
        self.assertEqual(spec["target_zone_shape"], "circle")
        self.assertEqual(spec["target_zone_radius_m"], 0.12)
        self.assertEqual(spec["target_zone_center"], (-2.95, 0.40, 0.701))
        self.assertEqual(spec["target_zone_height_m"], 0.002)

    def test_build_wrench_sim_command_targets_extension_scene(self):
        command = build_wrench_sim_command()

        self.assertIn("python sim_main.py", command)
        self.assertIn("--task e2_wrench", command)
        self.assertIn("--enable_dex3_dds", command)
        self.assertIn("--robot_type g129", command)

    def test_is_inside_circular_target_zone_accepts_center_and_rejects_outside_point(self):
        spec = build_wrench_scene_spec()

        self.assertTrue(
            is_inside_circular_target_zone(
                point_xy=spec["target_zone_center"][:2],
                center_xy=spec["target_zone_center"][:2],
                radius=spec["target_zone_radius_m"],
            )
        )
        self.assertFalse(
            is_inside_circular_target_zone(
                point_xy=(-2.60, 0.40),
                center_xy=spec["target_zone_center"][:2],
                radius=spec["target_zone_radius_m"],
            )
        )


if __name__ == "__main__":
    unittest.main()
