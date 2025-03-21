from cx_Freeze import setup, Executable
import os

path = "./assets"
asset_list = os.listdir(path)
asset_list_completa = [os.path.join(path, assets).replace("\\", "/") for assets in asset_list]
print(asset_list_completa)

executables = [Executable("main.py")]
files = {"include_files": asset_list_completa, "packages": ["pygame"]}

setup(
    name="MountainShooter",
    version="1.0",
    description="Mountain Shooter app",
    options={"build_exe": files},
    executables=executables
)
