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

def apply_geometry_issues(meshes, probability=0.4):
    for obj in meshes:
        if random.random() > probability:
            continue

        choice = random.choice([
            "ngon",
            "dense",
            "hidden_transform",
            "overlap",
            "zero_area",
            "isolated_vertex",
            "history",
            "hard_edges",
            "broken_normals"
        ])

        try:
            # NGONS
            if choice == "ngon":
                cmds.polySubdivideFacet(obj, dv=2)

            # HEAVY / DENSE GEO
            elif choice == "dense":
                cmds.polySmooth(obj, dv=2)

            # HIDDEN (TRANSFORM LEVEL)
            elif choice == "hidden_transform":
                cmds.setAttr(f"{obj}.visibility", 0)

            # OVERLAPPING GEO
            elif choice == "overlap":
                dup = cmds.duplicate(obj)[0]
                cmds.move(0, 0, 0, dup)

            # ZERO AREA FACES
            elif choice == "zero_area":
                faces = cmds.ls(f"{obj}.f[*]", flatten=True) or []
                if faces:
                    f = random.choice(faces)
                    try:
                        cmds.scale(0.0, 0.0, 0.0, f, relative=True)
                    except Exception:
                        pass

            # ISOLATED VERTICES
            elif choice == "isolated_vertex":
                verts = cmds.ls(f"{obj}.vtx[*]", flatten=True) or []
                if verts:
                    v = random.choice(verts)
                    try:
                        cmds.polySplitVertex(v)
                    except Exception:
                        pass

            # HISTORY
            elif choice == "history":
                cmds.polyBevel(obj)

            # HARD EDGES
            elif choice == "hard_edges":
                edges = cmds.ls(f"{obj}.e[*]", flatten=True) or []
                if edges:
                    cmds.polySoftEdge(edges, angle=0)

            # BROKEN NORMALS
            elif choice == "broken_normals":
                cmds.polyNormal(obj, normalMode=3)

        except Exception:
            # Generator must NEVER crash
            pass


def apply_topology_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        choice = random.choice([
            "lamina",
            "non_manifold",
            "degenerate"
        ])

        try:
            # LAMINA FACES (fixed + correct)
            if choice == "lamina":
                faces = cmds.ls(f"{obj}.f[*]", flatten=True) or []
                if not faces:
                    continue

                # Duplicate entire mesh
                dup = cmds.duplicate(obj)[0]

                # Merge back → overlapping geometry
                merged = cmds.polyUnite(obj, dup, constructionHistory=False)[0]

                cmds.delete(merged, constructionHistory=True)

                # Merge vertices very close → lamina faces
                cmds.polyMergeVertex(merged, d=0.0001)

            # NON-MANIFOLD (safe edge selection)
            elif choice == "non_manifold":
                edges = cmds.ls(f"{obj}.e[*]", flatten=True) or []
                if edges:
                    e = random.choice(edges)
                    cmds.polyExtrudeEdge(e, ltz=0)
                    cmds.polyMergeVertex(obj, d=0.0001)

            # DEGENERATE FACES
            elif choice == "degenerate":
                faces = cmds.ls(f"{obj}.f[*]", flatten=True) or []
                if faces:
                    face = random.choice(faces)

                    verts = cmds.polyListComponentConversion(
                        face,
                        toVertex=True
                    )
                    verts = cmds.ls(verts, flatten=True) or []

                    if len(verts) >= 2:
                        v1, v2 = random.sample(verts, 2)

                        cmds.move(0, 0, 0, v1, absolute=True)
                        cmds.move(0, 0, 0, v2, absolute=True)

        except Exception:
            # Never break generator
            pass


def apply_normals_issues(meshes, probability=0.2):
    for obj in meshes:
        if random.random() > probability:
            continue

        try:
            # Object must exist
            if not cmds.objExists(obj):
                continue

            # Must have a shape
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
            if not shapes:
                continue

            choice = random.choice(["delete_normals", "break_normals"])

            # DELETE / UNLOCK NORMALS (missing/invalid normals)
            if choice == "delete_normals":
                try:
                    cmds.polyNormalPerVertex(obj, unFreezeNormal=True)
                    cmds.polySetToFaceNormal(obj)
                except Exception:
                    pass

            # BREAK NORMALS (bad shading)
            elif choice == "break_normals":
                try:
                    cmds.polyNormal(obj, normalMode=3)
                except Exception:
                    pass

        except Exception:
            # never crash generator
            pass


def apply_uv_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        try:
            # Object must exist
            if not cmds.objExists(obj):
                continue

            # Must have shape
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
            if not shapes:
                continue

            # Ensure UV set exists
            uv_sets = cmds.polyUVSet(obj, query=True, allUVSets=True) or []

            # 🔧 If no UVs → optionally create some (so we can break them later)
            if not uv_sets:
                try:
                    cmds.polyAutoProjection(obj)
                    uv_sets = cmds.polyUVSet(obj, query=True, allUVSets=True) or []
                except Exception:
                    continue

            if not uv_sets:
                continue

            # Ensure UV components actually exist
            uv_components = cmds.ls(f"{obj}.map[*]", flatten=True) or []
            if not uv_components:
                continue

            # Collapse UVs (overlap)
            if random.random() < 0.5:
                try:
                    cmds.polyEditUV(uv_components, u=0, v=0)
                except Exception:
                    pass

            # Create extra UV sets
            if random.random() < 0.5:
                for i in range(3):
                    try:
                        cmds.polyUVSet(obj, create=True, uvSet=f"UV_extra{i}")
                    except Exception:
                        continue

            # Delete UV set → creates missing UV scenario
            if random.random() < 0.3 and len(uv_sets) > 1:
                try:
                    cmds.polyUVSet(obj, delete=True, uvSet=uv_sets[0])
                except Exception:
                    pass

        except Exception:
            # Never break generator
            pass

def apply_material_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        try:
            # Ensure object still exists
            if not cmds.objExists(obj):
                continue

            # Ensure it still has a shape
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
            if not shapes:
                continue

            # assign multiple materials
            for i in range(random.randint(2, 5)):
                try:
                    mat = cmds.shadingNode(
                        "lambert",
                        asShader=True,
                        name=f"mat_{obj}_{i}"
                    )

                    sg = cmds.sets(
                        renderable=True,
                        noSurfaceShader=True,
                        empty=True
                    )

                    cmds.connectAttr(
                        mat + ".outColor",
                        sg + ".surfaceShader",
                        force=True
                    )

                    cmds.sets(obj, edit=True, forceElement=sg)

                except Exception:
                    continue

        except Exception:
            pass


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
    apply_topology_issues(meshes, probability=0.3)

    meshes = [
        m for m in (cmds.ls(type="transform", long=True) or [])
        if cmds.listRelatives(m, shapes=True, type="mesh")
    ]

    apply_normals_issues(meshes, probability=0.2)
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