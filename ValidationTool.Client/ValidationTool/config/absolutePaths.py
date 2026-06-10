from pathlib import Path


def find_root() -> Path:
    p = Path(__file__).resolve()

    for parent in p.parents:
        if (parent / ".validation_root").exists():
            return parent

    raise RuntimeError("Root not found")


ROOT_PATH = find_root()

CLIENT_PATH = ROOT_PATH / "ValidationTool.Client"

UI_PATH = ROOT_PATH / "ValidationTool.UI"


CONFIG_DIR = CLIENT_PATH / "config"
REPORTS_DIR = CLIENT_PATH / "reports"
SOURCE_MAYA = ROOT_PATH / "Sourcefiles" / "Source_Maya"
SOURCE_BLENDER = ROOT_PATH / "Sourcefiles" / "Source_Blender"
SOURCE_3DSMAX = ROOT_PATH / "Sourcefiles" / "Source_3DsMax"