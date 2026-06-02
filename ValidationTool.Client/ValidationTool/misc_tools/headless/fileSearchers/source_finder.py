from pathlib import Path

SUPPORTED_EXTENSIONS = {
    "maya": [".ma", ".mb"],
    "blender": [".blend"],   # note: .bl is wrong, Blender uses .blend
    "max": [".max"],
    "houdini": [".hip", ".hipnc"]
}


def get_MAYA_files(root: str) -> list[str]:
    root = Path(root)
    return [str(p) for p in root.rglob("*") if p.suffix in SUPPORTED_EXTENSIONS["maya"]]

def get_Blender_files(root: str) -> list[str]:
    root = Path(root)
    return [str(p) for p in root.rglob("*") if p.suffix in SUPPORTED_EXTENSIONS["blender"]]

def get_3DsMax_files(root: str) -> list[str]:
    root = Path(root)
    return [str(p) for p in root.rglob("*") if p.suffix in SUPPORTED_EXTENSIONS["max"]]

def get_Houdini_files(root: str) -> list[str]:
    root = Path(root)
    return [str(p) for p in root.rglob("*") if p.suffix in SUPPORTED_EXTENSIONS["houdini"]]