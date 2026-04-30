import tempfile
import unittest
import zipfile
from pathlib import Path

from graduation_design.tool_asset import (
    build_import_plan,
    inspect_asset_archive,
    render_import_plan,
)


class ToolAssetTests(unittest.TestCase):
    def _make_sample_zip(self):
        tmp_dir = tempfile.TemporaryDirectory()
        zip_path = Path(tmp_dir.name) / "wrench.zip"
        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("sample_wrench/model.obj", "o wrench\n")
            archive.writestr("sample_wrench/model.mtl", "newmtl material0\n")
            archive.writestr("sample_wrench/albedo.jpg", "fake")
        return tmp_dir, zip_path

    def test_inspect_asset_archive_detects_obj_bundle(self):
        tmp_dir, zip_path = self._make_sample_zip()
        try:
            info = inspect_asset_archive(zip_path)
        finally:
            tmp_dir.cleanup()

        self.assertEqual(info["root_dir"], "sample_wrench")
        self.assertEqual(info["obj_files"], ["sample_wrench/model.obj"])
        self.assertEqual(info["mtl_files"], ["sample_wrench/model.mtl"])
        self.assertEqual(info["texture_files"], ["sample_wrench/albedo.jpg"])

    def test_build_import_plan_uses_expected_default_targets(self):
        tmp_dir, zip_path = self._make_sample_zip()
        try:
            plan = build_import_plan("wrench", zip_path=zip_path)
        finally:
            tmp_dir.cleanup()

        self.assertEqual(plan["asset_name"], "wrench")
        self.assertIn("assets/external_tools/wrench/source", plan["extract_dir"])
        self.assertIn("myusd/Objects/external_tools/wrench/wrench.usd", plan["usd_target"])
        self.assertTrue(plan["obj_entry"].endswith("model.obj"))

    def test_render_import_plan_contains_commands(self):
        tmp_dir, zip_path = self._make_sample_zip()
        try:
            text = render_import_plan("wrench", zip_path=zip_path)
        finally:
            tmp_dir.cleanup()

        self.assertIn("Asset Name: wrench", text)
        self.assertIn("unzip -o", text)
        self.assertIn("OBJ Entry:", text)
        self.assertIn("USD Target:", text)


if __name__ == "__main__":
    unittest.main()
