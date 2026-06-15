
import bpy
import bmesh
import random
from pathlib import Path
import sys
import random

PARENT_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PARENT_DIR))

ARTISTS_DIR = Path.home() / "Documents" / "Artists"
ARTISTS_DIR.mkdir(parents=True, exist_ok=True)

def maybe(func, *args, probability=0.5):
    if random.random() < probability:
        func(*args)


def apply_naming_issues(meshes, probability=0.4):
    updated_meshes = []

    for obj in meshes:
        new_obj = obj

        if random.random() < probability:
            options = [
                "Cube",
                "badName",
                "CH__BadName",
                "CH Bad Name",
                "CH.BadName",
            ]
            try:
                new_name = random.choice(options)
                obj.name = new_name
                new_obj = bpy.data.objects[new_name]
            except:
                pass

        updated_meshes.append(new_obj)

    return updated_meshes


def apply_transform_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        choice = random.choice(["neg", "non_uniform", "zero", "extreme"])

        if choice == "neg":
            obj.scale = (-1, 1, 1)

        elif choice == "non_uniform":
            obj.scale = (1, 2, 3)

        elif choice == "zero":
            obj.scale = (0, 1, 1)

        elif choice == "extreme":
            obj.scale = (10000, 10000, 10000)


def apply_geometry_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        bpy.context.view_layer.objects.active = obj
        choice = random.choice(["ngon", "dense", "hidden", "overlap"])

        if choice == "dense":
            mod = obj.modifiers.new(name="Subsurf", type='SUBSURF')
            mod.levels = 2
            bpy.ops.object.modifier_apply(modifier=mod.name)

        elif choice == "ngon":
            mesh = obj.data
            bm = bmesh.new()
            bm.from_mesh(mesh)

            bm.faces.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.verts.ensure_lookup_table()

            if bm.faces:
                f = bm.faces[0]
                bmesh.ops.inset_individual(bm, faces=[f], thickness=0.1)

            bm.to_mesh(mesh)
            bm.free()
            mesh.update()

        elif choice == "hidden":
            obj.hide_set(True)

        elif choice == "overlap":
            dup = obj.copy()
            dup.data = obj.data.copy()
            bpy.context.collection.objects.link(dup)
            dup.location = obj.location


def apply_uv_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        mesh = obj.data

        if not mesh.uv_layers:
            mesh.uv_layers.new(name="UVMap")

        if random.random() < 0.5:
            for uv_layer in mesh.uv_layers:
                for loop in mesh.loops:
                    uv_layer.data[loop.index].uv = (0, 0)

        if random.random() < 0.5:
            for i in range(5):
                mesh.uv_layers.new(name=f"UV_extra{i}")


def apply_material_issues(meshes, probability=0.3):
    for obj in meshes:
        if random.random() > probability:
            continue

        for i in range(random.randint(2, 5)):
            mat = bpy.data.materials.new(name=f"mat_{obj.name}_{i}")
            obj.data.materials.append(mat)


def apply_scene_issues(probability=0.7):
    if random.random() < probability:
        bpy.ops.object.camera_add()
        bpy.context.object.name = "renderCam1"


def create_cubes(num_objects: int):
    meshes = []

    for i in range(num_objects):
        bpy.ops.mesh.primitive_cube_add(location=(i * 1.5, 0, 0))
        obj = bpy.context.object
        obj.name = f"PRP_Cube_{i}"
        meshes.append(obj)

    return meshes


def create_blenderScene_with_random_issues(file_path: Path):
    bpy.ops.wm.read_factory_settings(use_empty=True)

    num_objects = random.randint(10, 15)
    meshes = create_cubes(num_objects)

    apply_transform_issues(meshes, probability=0.4)
    apply_geometry_issues(meshes, probability=0.4)
    apply_uv_issues(meshes, probability=0.4)
    apply_material_issues(meshes, probability=0.3)
    meshes = apply_naming_issues(meshes, probability=0.5)

    apply_scene_issues(probability=0.5)

    bpy.ops.wm.save_as_mainfile(filepath=str(file_path))

    print(f"[CREATED] {file_path} with {num_objects} objects")



def main():
    print("Starting scene generation...\n")

    ARTISTS_DIR.mkdir(exist_ok=True)

    total_files = 0

    for artist_dir in ARTISTS_DIR.iterdir():

        if not artist_dir.is_dir():
            continue

        artist = artist_dir.name

        artistBlender_dir = artist_dir / "Source_Blender"
        artistBlender_dir.mkdir(parents=True, exist_ok=True)

        num_Blenderfiles = random.randint(2, 5)

        print(f"Creating {num_Blenderfiles} scenes for {artist}")

        for i in range(num_Blenderfiles):
            file_name = f"{artist}_brokenScene_{i}.blend"
            file_path = artistBlender_dir / file_name

            create_blenderScene_with_random_issues(file_path)
            total_files += 1

    print(f"\nDONE. Created {total_files} scenes.")



if __name__ == "__main__":
    main()