import urdf_usd_converter
from pxr import Sdf, Usd

converter = urdf_usd_converter.Converter()

asset: Sdf.AssetPath = converter.convert("C:/user/urdf/diandong/urdf/diandong.urdf", "C:/user/urdf/usd")
print("until now sucess")