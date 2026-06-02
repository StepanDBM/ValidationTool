import bpy
import bmesh
import random
from mathutils import Vector


# -------------------------------------------------
# UTILS
# -------------------------------------------------

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def add_uv_chaos(obj):
    """Blender UV stress equivalent to Maya polyUVSet chaos"""

    mesh = obj.data

    # Ensure UV layer exists
    if not mesh.uv_layers:
        mesh.uv_layers.new(name="UVMap")

    # Create multiple UV sets
    for i in range(1, 5):
        uv_name = f"uvSet_{i}"
        if uv_name not in mesh.uv_layers:
            mesh.uv_layers.new(name=uv_name)

    # Duplicate-like behaviour (Blender doesn't support direct UV duplication like Maya)
    if mesh.uv_layers:
        try:
            mesh.uv_layers.new(name="uvSet1_dup")
        except:
            pass


def apply_random_scale(obj):
    obj.scale.x = random.choice([-1, 1]) * random.uniform(0.01, 2000)
    obj.scale.y = random.choice([-1, 1]) * random.uniform(0.01, 2000)
    obj.scale.z = random.choice([-1, 1]) * random.uniform(0.01, 2000)


def apply_extreme_scale(obj, x, y, z):
    obj.scale = (x, y, z)


def apply_modifiers(obj, levels=3):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.modifier_add(type='SUBSURF')
    obj.modifiers["Subdivision"].levels = levels

    bpy.ops.object.modifier_apply(modifier="Subdivision")


# -------------------------------------------------
# SCENE BUILD
# -------------------------------------------------

def build_test_scene():
    clear_scene()

    # ----------------------------------------
    # CLEAN BASE (geometry stress cubes)
    # ----------------------------------------
    for i in range(4):
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.name = f"ENV_{i}"

        apply_modifiers(obj, levels=i + 2)
        apply_extreme_scale(obj,
            1500 * (i + 1),
            1200 * (i + 1),
            800 * (i + 1)
        )

        add_uv_chaos(obj)

    # ----------------------------------------
    # NEGATIVE SCALE / HERO / CHARACTER STRESS
    # ----------------------------------------
    bpy.ops.mesh.primitive_uv_sphere_add()
    ch = bpy.context.active_object
    ch.name = "CH_shieh"
    apply_modifiers(ch, levels=2)
    ch.scale.x = -1
    add_uv_chaos(ch)

    bpy.ops.mesh.primitive_uv_sphere_add()
    hero = bpy.context.active_object
    hero.name = "HERO__shieh"
    apply_modifiers(hero, levels=2)
    hero.scale = (2, 5, 0.5)
    add_uv_chaos(hero)

    # ----------------------------------------
    # EMPTY GEOMETRY OBJECT (hard fail equivalent)
    # ----------------------------------------
    bpy.ops.mesh.primitive_cube_add()
    empty = bpy.context.active_object
    empty.name = "EMPTY_ZERO"

    # delete geometry but keep object
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # ----------------------------------------
    # TORUS STRESS OBJECTS
    # ----------------------------------------
    bpy.ops.mesh.primitive_torus_add()
    env1 = bpy.context.active_object
    env1.name = "ENV_shiehhhh"
    apply_modifiers(env1, levels=1)
    env1.scale.x = 2000
    env1.scale.y = 1
    env1.scale.z = 1
    add_uv_chaos(env1)

    bpy.ops.mesh.primitive_torus_add()
    prp = bpy.context.active_object
    prp.name = "PRP_mine"
    apply_modifiers(prp, levels=2)
    prp.scale = (1, 3, 10)
    add_uv_chaos(prp)

    bpy.ops.mesh.primitive_torus_add()
    mod = bpy.context.active_object
    mod.name = "some_MOD"
    apply_modifiers(mod, levels=3)
    mod.scale = (-3, 2000, 0)  # includes zero scale
    add_uv_chaos(mod)

    bpy.ops.mesh.primitive_torus_add()
    broken = bpy.context.active_object
    broken.name = "brokennaming"
    apply_modifiers(broken, levels=3)
    broken.scale = (1, 1, 1)
    add_uv_chaos(broken)

    print("Scene build complete (Blender stress test)")


# -------------------------------------------------
# RUN
# -------------------------------------------------

if __name__ == "__main__":
    build_test_scene()