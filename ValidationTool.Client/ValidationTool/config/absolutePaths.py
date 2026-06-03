from pathlib import Path

ROOT_PATH = Path(r"C:\Users\StyopaDBM\source\repos\ValidationTool") #to be changed in case that the project is opened in another machine

CLIENT_PATH = ROOT_PATH / "ValidationTool.Client"

UI_PATH = ROOT_PATH / "ValidationTool.UI"


CONFIG_DIR = CLIENT_PATH / "config"
REPORTS_DIR = CLIENT_PATH / "reports"
SOURCE_MAYA = ROOT_PATH / "Sourcefiles" / "Source_Maya"
SOURCE_BLENDER = ROOT_PATH / "Sourcefiles" / "Source_Blender"
SOURCE_3DSMAX = ROOT_PATH / "Sourcefiles" / "Source_3DsMax"