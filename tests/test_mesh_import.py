import unittest

from graduation_design.mesh_import import (
    build_mesh_import_spec,
    render_mesh_import_command,
)


class MeshImportTests(unittest.TestCase):
    def test_build_mesh_import_spec_for_wrench(self):
        spec = build_mesh_import_spec("wrench")

        self.assertEqual(spec["asset_name"], "wrench")
        self.assertTrue(spec["asset_path"].endswith("13073_Combination_Wrench_v1_l3.obj"))
        self.assertTrue(spec["usd_path"].endswith("/myusd/Objects/external_tools/wrench/wrench.usd"))
        self.assertEqual(spec["translation"], (0.0, 0.0, 0.0))
        self.assertEqual(spec["scale"], (1.0, 1.0, 1.0))
        self.assertEqual(spec["collision_approximation"], "convexDecomposition")

    def test_render_mesh_import_command_contains_expected_args(self):
        command = render_mesh_import_command("wrench")

        self.assertIn("python import_external_mesh.py", command)
        self.assertIn("--asset-name wrench", command)
        self.assertIn("--collision-approximation convexDecomposition", command)
        self.assertIn("--mass 0.4", command)


if __name__ == "__main__":
    unittest.main()
