"""
Might as well plan ahead.
if :
EXECUTION_STAGES = [
    NAMING,
    SCENE,
    HIERARCHY,
    TRANSFORM,
    GEOMETRY,
    UV,
    MATERIAL,
    RIG,
    ANIMATION,
    CAMERA,
    LIGHT,
    REFERENCE,
    RENDER,
    HISTORY,
    PRE_EXPORT,
]
then :
    For SSContext:
        core/
        ├── checks/
        │   │
        │   ├── naming/
        │   │   ├── check_object_naming.py
        │   │   ├── check_render_layer_name.py
        │   │   └── check_aov_name.py
        │   │
        │   ├── scene/
        │   │   ├── check_output_path.py
        │   │   ├── check_project_path.py
        │   │   └── check_scene_metadata.py
        │   │
        │   ├── hierarchy/
        │   │   └── ...
        │   │
        │   ├── transform/
        │   │   ├── check_negative_scale.py
        │   │   ├── check_non_uniform_scale.py
        │   │   ├── check_zero_scale.py
        │   │   └── check_extreme_scale.py
        │   │
        │   ├── geometry/
        │   │   ├── check_vertex_count.py
        │   │   ├── check_triangle_count.py
        │   │   ├── check_non_manifold.py
        │   │   ├── check_degenerate_faces.py
        │   │   └── check_bounding_box.py
        │   │
        │   ├── uv/
        │   │   ├── check_uv_sets.py
        │   │   ├── check_missing_uv0.py
        │   │   ├── check_missing_uv1.py
        │   │   └── check_duplicate_uv_set_names.py
        │   │
        │   ├── material/
        │   │   ├── check_material_slots.py
        │   │   └── ...
        │   │
        │   ├── rig/
        │   │   └── ...
        │   │
        │   ├── animation/
        │   │   └── ...
        │   │
        │   ├── camera/
        │   │   ├── check_has_render_camera.py
        │   │   ├── check_duplicate_render_cameras.py
        │   │   ├── check_default_render_camera.py
        │   │   └── ...
        │   │
        │   ├── light/
        │   │   └── check_environment_light_presence.py
        │   │
        │   ├── reference/
        │   │   └── ...
        │   │
        │   ├── render/
        │   │   ├── renderer/
        │   │   │   ├── check_renderer_supported.py
        │   │   │   ├── check_render_device.py
        │   │   │   └── check_render_mode.py
        │   │   │
        │   │   ├── output/
        │   │   │   ├── check_output_prefix.py
        │   │   │   ├── check_output_format.py
        │   │   │   ├── check_resolution.py
        │   │   │   └── check_compression.py
        │   │   │
        │   │   ├── sampling/
        │   │   │   ├── check_aa_samples.py
        │   │   │   ├── check_sampling_balance.py
        │   │   │   └── check_noise_threshold.py
        │   │   │
        │   │   ├── color/
        │   │   │   ├── check_color_management.py
        │   │   │   ├── check_aces_usage.py
        │   │   │   └── check_ocio_config.py
        │   │   │
        │   │   ├── layers/
        │   │   │   └── check_render_layers.py
        │   │   │
        │   │   ├── aovs/
        │   │   │   ├── check_required_aovs.py
        │   │   │   ├── check_duplicate_aovs.py
        │   │   │   └── check_aov_driver_filter.py
        │   │   │
        │   │   └── performance/
        │   │       ├── check_cpu_render.py
        │   │       ├── check_high_subdivision.py
        │   │       └── check_low_resolution.py
        │   │
        │   ├── history/
        │   │   └── ...
        │   │
        │   └── pre_export/
        │       ├── check_scene_ready_for_export.py
        │       └── check_missing_required_aovs.py
        │
        └── registry/
            ├── validation_registry.py
            └── build_registry.py

.... WHY? Right? Makes sense to ask that. But here I am to explain, my lil' future me.

If I have, for instance and just like I did before:
check_name=CHECK_TRANSFORMS
for
negative scale
non-uniform scale
zero scale
extreme scale

Then when I get all the issues, I will NOT know what kind of check it was unless I parse the message/suggestion.
I lose granularity:
Best practice seems to be to have List[ValidationIssue] BUT outside the checks, which will return 0 or 1 issue with WARNING/ERROR in it, no  "INFO" non-sense.
So instead of 
    check_transforms()

we have
    check_negative_scale()
    check_non_uniform_scale()
    check_zero_scale()
    check_extreme_scale()
HENCE: UI becomes
    CHECK_NEGATIVE_SCALE
    CHECK_NON_UNIFORM_SCALE
    CHECK_ZERO_SCALE
    CHECK_EXTREME_SCALE
Then the check name is WAAAAY clearer from the start after we parse the json.
We can even make messages arbitrary as well as suggestions and just take the exec stage and check "type" as the source of truth.
"""