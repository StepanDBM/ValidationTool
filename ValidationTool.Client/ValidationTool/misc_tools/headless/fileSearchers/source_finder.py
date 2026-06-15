from pathlib import Path

SUPPORTED_EXTENSIONS = {
    "maya": [".ma", ".mb"],
    "blender": [".blend"],
    "max": [".max"],
    "houdini": [".hip", ".hipnc"]
}

DCC_FOLDER_MAP = {
    "maya": "Source_Maya",
    "blender": "Source_Blender",
    "max": "Source_3DsMax",
    "houdini": "Source_Houdini"
}

def get_documents_scenes_root() -> Path:
    return Path.home() / "Documents" / "Artists"

def get_dcc_files(root: Path, dcc: str) -> list[dict]:
    if dcc not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported DCC: {dcc}")

    dcc_folder_name = DCC_FOLDER_MAP[dcc]
    extensions = SUPPORTED_EXTENSIONS[dcc]

    result = []
    root = get_documents_scenes_root()

    for artist_dir in root.iterdir():
        if not artist_dir.is_dir():
            continue

        artist_log = artist_dir / "artistLog.json"

        dcc_dir = artist_dir / dcc_folder_name

        if not dcc_dir.exists():
            continue

        for p in dcc_dir.rglob("*"):
            if p.is_file() and p.suffix in extensions:
                result.append({
                    "file_path": str(p),
                    "artist_log": str(artist_log)
                })

    return result   