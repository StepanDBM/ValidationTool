import maya.standalone
maya.standalone.initialize(name="python")

import maya.cmds as cmds
from pathlib import Path
import random
import sys

PARENT_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PARENT_DIR))

from genDCCrootPath import (
    ARTISTS_DIR
)

def maybe(func, *args, probability=0.5): #this is honestly so cool, I feel quite proud of it.
    if random.random() < probability:
        func(*args)


def apply_naming_issues(meshes, probability=0.4):
    updated_meshes = []

    for obj in meshes:
        new_name = obj

        if random.random() < probability:
            options = [
                lambda o: "pCube1",
                lambda o: "badName",
                lambda o: "CH__BadName"
            ]

            try:
                new_name = cmds.rename(obj, random.choice(options)(obj))
            except:
                pass

        updated_meshes.append(new_name)

    return updated_meshes


def apply_transform_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        choice = random.choice(["neg", "non_uniform", "zero", "extreme"])

        if choice == "neg":
            cmds.scale(-1, 1, 1, obj)

        elif choice == "non_uniform":
            cmds.scale(1, 2, 3, obj)

        elif choice == "zero":
            cmds.scale(0, 1, 1, obj)

        elif choice == "extreme":
            cmds.scale(10000, 10000, 10000, obj)

def apply_geometry_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        choice = random.choice(["ngon", "dense", "hidden", "overlap"])

        if choice == "dense":
            cmds.polySmooth(obj, dv=2)

        elif choice == "ngon":
            cmds.polySubdivideFacet(obj, dv=2)

        elif choice == "hidden":
            cmds.setAttr(f"{obj}.visibility", 0)

        elif choice == "overlap":
            dup = cmds.duplicate(obj)[0]
            cmds.move(0, 0, 0, dup)

def apply_uv_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        if random.random() < 0.5:
            cmds.polyEditUV(f"{obj}.map[*]", u=0, v=0)

        if random.random() < 0.5:
            for i in range(5):
                cmds.polyUVSet(obj, create=True, uvSet=f"UV_extra{i}")

def apply_material_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        # assign multiple materials
        for i in range(random.randint(2, 5)):
            mat = cmds.shadingNode("lambert", asShader=True, name=f"mat_{obj}_{i}")
            sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
            cmds.connectAttr(mat + ".outColor", sg + ".surfaceShader")
            cmds.sets(obj, edit=True, forceElement=sg)


def apply_scene_issues(probability: 0.7):
    if random.random() < probability: # duplicate camera problem
        cam = cmds.camera(name="renderCam1")[0]


def create_cubes(num_objects: int):
    meshes = []

    for i in range(num_objects):
        name = f"PRP_Cube_{i}"
        cube = cmds.polyCube(name=name)[0]
        cmds.move(i * 1.5, 0, 0, cube)
        meshes.append(cube)

    return meshes

def create_mayaScene_with_random_issues(file_path: Path):
    cmds.file(new=True, force=True)


    num_objects = random.randint(10, 15)
    meshes = create_cubes(num_objects)


    apply_transform_issues(meshes, probability=0.4)
    apply_geometry_issues(meshes, probability=0.4)
    apply_uv_issues(meshes, probability=0.4)
    apply_material_issues(meshes, probability=0.3)
    apply_naming_issues(meshes, probability=0.5)


    apply_scene_issues(probability=0.5)

    cmds.file(rename=str(file_path))
    cmds.file(save=True, type="mayaAscii")

    print(f"[CREATED] {file_path} with {num_objects} objects")


def main():
    print("Starting scene generation...\n")

    ARTISTS_DIR.mkdir(exist_ok=True)

    total_files = 0
    artists_data = []

    for artist_dir in ARTISTS_DIR.iterdir():
        if not artist_dir.is_dir():
            continue

        artist = artist_dir.name
        num_files = random.randint(2, 5)

        artists_data.append((artist_dir, artist, num_files))
        total_files += num_files

    current_index = 0

    print(f"TOTAL_FILES: {total_files}")

    for artist_dir, artist, num_Mayafiles in artists_data:

        artistMaya_dir = artist_dir / "Source_Maya"
        artistMaya_dir.mkdir(parents=True, exist_ok=True)

        print(f"[INFO] Creating {num_Mayafiles} Maya scenes for {artist}")

        for i in range(num_Mayafiles):
            file_name = f"{artist}_brokenScene_{i}.ma"
            file_path = artistMaya_dir / file_name

            print(f"CURRENT_FILE: {file_path}")

            create_mayaScene_with_random_issues(file_path)

            current_index += 1

            percent = int((current_index / total_files) * 100)

            print(f"PROGRESS: [{percent}%]")

    print(f"\nDONE. Created {current_index} scenes.")

if __name__ == "__main__":
    main()