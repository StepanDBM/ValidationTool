from pathlib import Path
import config.absolutePaths as absPath

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


def get_dcc_files(dcc: str) -> list[dict]:
    if dcc not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported DCC: {dcc}")

    dcc_folder_name = DCC_FOLDER_MAP[dcc]
    extensions = SUPPORTED_EXTENSIONS[dcc]

    result = []

    path = absPath.ARTISTS_DIR

    for artist_dir in path.iterdir():
        if not artist_dir.is_dir():
            continue

        artist_log = artist_dir / "artistLog.json"
        
        dcc_dir = artist_dir / dcc_folder_name

        if not dcc_dir.exists():
            continue

        for p in dcc_dir.rglob("*"):
            if p.is_file() and p.suffix in extensions:
                result.append({
                    "file_path": p.relative_to(absPath.ARTISTS_DIR),
                    "artist_log": artist_log.relative_to(absPath.ARTISTS_DIR)
                })

    return result   