import sys
import shutil
from pathlib import Path


PARENT_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PARENT_DIR))

from artistJsonCreator import(
    create_artist_json
)
from mArtists import ARTISTS
APP_DIR = Path.home() / "Documents" / "ValidationTool"
APP_DIR.mkdir(parents=True, exist_ok=True)
ARTISTS_DIR = APP_DIR / "Artists"
ARTISTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = APP_DIR / "Reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("Starting scene generation...\n")


    for item in ARTISTS_DIR.iterdir():
        if item.is_dir():
            shutil.rmtree(item)  # remove folder and its contents
        else:
            item.unlink()        # remove file
    ARTISTS_DIR.mkdir(parents=True, exist_ok=True)

    for artist in ARTISTS:
        artist_dir = ARTISTS_DIR / artist.replace(" ","")
        artist_dir.mkdir(parents=True, exist_ok=True)

        artistMaya_dir = artist_dir / "Source_Maya"
        artistMaya_dir.mkdir(parents=True, exist_ok=True)

        artistBlender_dir = artist_dir / "Source_Blender"
        artistBlender_dir.mkdir(parents=True, exist_ok=True)

        create_artist_json(artist, artist_dir)


if __name__ == "__main__":
    main()