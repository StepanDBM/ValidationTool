import sys
import importlib as iL
import gc


MODULES_TO_CLEAR = [
    "core.context.baseContext",
    "core.context.mesh_context",
    "core.context.camera_context",
    "core.context.light_context",

    "core.context.SceneContext.SceneSetupContext",
    "core.context.SceneContext.aov_context",
    "core.context.SceneContext.camera_setup_context",
    "core.context.SceneContext.color_management_context",
    "core.context.SceneContext.output_settings_context",
    "core.context.SceneContext.ray_depth_settings_context",
    "core.context.SceneContext.render_layer_context",
    "core.context.SceneContext.rneder_settings_context",
    "core.context.SceneContext.sampling_settings_context",


    "core.runner",
    "core.registry",
    "core.validation_context",
    "core.validation_models",
    "core.validation_system",

    "config.mesh_budgets",
    "config.validation_config",
    "config.check_categories",
    "config.validation_profile",
    """
        "misc_tools.DCC.Maya.maya_adapter",
        "misc_tools.DCC.Maya.maya_extract_cameras",
        "misc_tools.DCC.Maya.maya_extract_lights",
        "misc_tools.DCC.Maya.maya_extract_meshes",
        "misc_tools.DCC.Maya.maya_safeMultiTool",
        "misc_tools.DCC.Maya.maya_extract_SceneSetup",

        "misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_aovs",
        "misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_camera_setup",
        "misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_color_management",
        "misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_output_settings",
        "misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_ray_depth_settings",
        "misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_render_layers",
        "misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_render_settings",
        "misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_sampling_settings",
        "misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_SSContext",

        
        "misc_tools.DCC.Blender.blender_adapter",
        "misc_tools.DCC.Blender.blender_extract_cameras",
        "misc_tools.DCC.Blender.blender_extract_lights",
        "misc_tools.DCC.Blender.blender_extract_meshes",
        "misc_tools.DCC.Blender.blender_safeMultiTool",
        "misc_tools.DCC.Blender.blender_extract_SceneSetup",

        "misc_tools.DCC.Blender.blender_extract_SceneSetup.maya_extract_aovs",
        "misc_tools.DCC.Blender.blender_extract_SceneSetup.maya_extract_camera_setup",
        "misc_tools.DCC.Blender.blender_extract_SceneSetup.maya_extract_color_management",
        "misc_tools.DCC.Blender.blender_extract_SceneSetup.maya_extract_output_settings",
        "misc_tools.DCC.Blender.blender_extract_SceneSetup.maya_extract_ray_depth_settings",
        "misc_tools.DCC.Blender.blender_extract_SceneSetup.maya_extract_render_layers",
        "misc_tools.DCC.Blender.blender_extract_SceneSetup.maya_extract_render_settings",
        "misc_tools.DCC.Blender.blender_extract_SceneSetup.maya_extract_sampling_settings",
        "misc_tools.DCC.Blender.blender_extract_SceneSetup.maya_extract_SSContext",

        "misc_tools.headless.maya_sceneBuilder",
        "misc_tools.headless.run_blender_validation",
        "misc_tools.headless.run_maya_validation",
        "misc_tools.headless.fileSearchers",
        "misc_tools.headless.fileSearchers.source_finder",



        "core.checks.Geometry.check_bounding_box",
        "core.checks.Geometry.check_collision_readiness",
        "core.checks.Geometry.check_degenerate_faces",
        "core.checks.Geometry.check_hard_edges",
        "core.checks.Geometry.check_hidden_geometry",
        "core.checks.Geometry.check_isolated_vertices",
        "core.checks.Geometry.check_lamina_faces",
        "core.checks.Geometry.check_ngons",
        "core.checks.Geometry.check_non_manifold",
        "core.checks.Geometry.check_normals_exist",
        "core.checks.Geometry.check_normals",
        "core.checks.Geometry.check_overlapping_geometry",
        "core.checks.Geometry.check_triangle_count",
        "core.checks.Geometry.check_vertex_count",
        "core.checks.Geometry.check_zero_area_faces",

        "core.checks.History.check_history",

        "core.checks.Material.check_material_slots",

        "core.checks.Naming.check_default_dcc_name",
        "core.checks.Naming.check_double_underscore",
        "core.checks.Naming.config_models",
        "core.checks.Naming.dcc_list",
        "core.checks.Naming.exec_stages",
        "core.checks.Naming.validation_config",
        "core.checks.Naming.validation_profile",

        
        "core.checks.Transform.check_extreme_scale",
        "core.checks.Transform.check_negative_scale",
        "core.checks.Transform.check_non_uniform_scale",
        "core.checks.Transform.check_zero_scale",

        "core.checks.Geometry.check_duplicate_uv_set_names",
        "core.checks.Geometry.check_empty_uv_set_names",
        "core.checks.Geometry.check_missing_uv",

        "core.checks.Geometry.validation_check_ids",
    """

    "reporting.json_reporter",
    "reporting.staged_json_reporter",
    "my_ui_module.validator_UI",
    "my_ui_module.launch_UI",
    "run_validator"
]



def destroy_ui():
    try:
        launch_ui_mod = sys.modules.get("my_ui_module.launch_UI")
        if launch_ui_mod and hasattr(launch_ui_mod, "close_existing"):
            launch_ui_mod.close_existing()
    except Exception as e:
        print("[BOOTSTRAP] UI close skipped:", e)


def hard_reload():
    # kill modules
    for m in MODULES_TO_CLEAR:
        if m in sys.modules:
            del sys.modules[m]

    gc.collect()

    print("[BOOTSTRAP] reload complete")


def launch_ui():
    launch_ui_mod = iL.import_module("my_ui_module.launch_UI")
    return launch_ui_mod.show()


def letsDoThis():
    destroy_ui()
    hard_reload()
    launch_ui()
