from pxr import Usd

# #USD-usda
# # 打开现有的 USD 文件
# stage = Usd.Stage.Open("/home/ubuntu/桌面/xr_teleoperate/unitree_sim_isaaclab/assets/objects/PackingTable/PackingTable.usd")

# # 导出为 USDA 文本格式
# stage.Export("PackingTable.usda")

from omni.isaac.urdf import _urdf
from omni.isaac.core.utils.extensions import get_extension_path_from_name

# 配置导入
urdf_interface = _urdf.acquire_urdf_interface()
import_config = _urdf.ImportConfig()
import_config.set_merge_fixed_joints(False)
import_config.set_convex_decomp(False)
import_config.set_import_inertia_tensor(True)
import_config.set_fix_base(False)

# 执行导入
status, import_path = urdf_interface.import_urdf(
    urdf_path="/home/ubuntu/桌面/螺栓与扳手建模/电动钻头.SLDASM/urdf/电动钻头.SLDASM.urdf",
    import_config=import_config
)

print(f"Imported to: {import_path}")

