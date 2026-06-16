from core.context.SceneContext.render_settings_context import RenderSettingsContext
from misc_tools.DCC.Blender.blender_safeMultiTool import (
    _get_scene,
    _get_render_engine
)

try:
    import bpy
except ImportError:
    bpy = None


def _get_renderer_name(engine: str) -> str:
    engine = (engine or "").upper()

    if engine == "CYCLES":
        return "cycles"
    if engine == "BLENDER_EEVEE":
        return "eevee"
    if engine == "BLENDER_WORKBENCH":
        return "workbench"

    return engine.lower()


def _get_renderer_version() -> str:
    try:
        return bpy.app.version_string
    except Exception:
        return ""


def _get_cycles_settings(scene):
    try:
        return scene.cycles
    except Exception:
        return None


def _get_render_device(scene, renderer_name: str) -> str:
    if renderer_name != "cycles":
        return "GPU" if renderer_name == "eevee" else "CPU"

    cycles = _get_cycles_settings(scene)
    if cycles is None:
        return "CPU"

    try:
        device = getattr(cycles, "device", "CPU")
        if str(device).upper() == "GPU":
            return "GPU"
    except Exception:
        pass

    return "CPU"


def _get_render_mode(renderer_name: str) -> str:
    if renderer_name == "cycles":
        return "PROGRESSIVE"
    if renderer_name == "eevee":
        return "REALTIME"
    if renderer_name == "workbench":
        return "VIEWPORT"

    return "FINAL"


def _extract_denoiser_settings(scene, renderer_name: str) -> tuple[bool, str]:
    if renderer_name != "cycles":
        return False, ""

    cycles = _get_cycles_settings(scene)
    if cycles is None:
        return False, ""

    enabled = False
    denoiser_type = ""

    try:
        enabled = bool(getattr(cycles, "use_denoising", False))
    except Exception:
        enabled = False

    try:
        denoiser_type = str(getattr(cycles, "denoiser", ""))
    except Exception:
        denoiser_type = ""

    try:
        view_layer = bpy.context.view_layer
        if view_layer is not None and getattr(view_layer, "cycles", None):
            enabled = enabled or bool(getattr(view_layer.cycles, "use_denoising", False))
    except Exception:
        pass

    return enabled, denoiser_type


def _extract_adaptive_sampling(scene, renderer_name: str) -> tuple[bool, float, float]:
    if renderer_name != "cycles":
        return False, 0.0, 0.0

    cycles = _get_cycles_settings(scene)
    if cycles is None:
        return False, 0.0, 0.0

    adaptive_enabled = False
    adaptive_threshold = 0.0
    noise_threshold = 0.0

    try:
        adaptive_enabled = bool(getattr(cycles, "use_adaptive_sampling", False))
    except Exception:
        adaptive_enabled = False

    try:
        adaptive_threshold = float(getattr(cycles, "adaptive_threshold", 0.0))
    except Exception:
        adaptive_threshold = 0.0

    noise_threshold = adaptive_threshold

    return adaptive_enabled, adaptive_threshold, noise_threshold


def _extract_motion_blur(scene) -> bool:
    try:
        return bool(scene.render.use_motion_blur)
    except Exception:
        return False


def _extract_depth_of_field(scene) -> bool:
    try:
        for obj in scene.objects:
            if obj.type != "CAMERA":
                continue

            cam_data = obj.data
            if cam_data and getattr(cam_data.dof, "use_dof", False):
                return True
    except Exception:
        pass

    return False


def _extract_thread_mode(scene) -> tuple[str, int]:
    try:
        mode = str(scene.render.threads_mode)
    except Exception:
        mode = ""

    try:
        count = int(scene.render.threads)
    except Exception:
        count = 0

    return mode, count


def _extract_tile_size(scene, renderer_name: str) -> tuple[int, int]:
    if renderer_name != "cycles":
        return 0, 0

    tile_x = 0
    tile_y = 0

    try:
        tile_x = int(getattr(scene.render, "tile_x", 0))
    except Exception:
        tile_x = 0

    try:
        tile_y = int(getattr(scene.render, "tile_y", 0))
    except Exception:
        tile_y = 0

    return tile_x, tile_y


def _extract_use_caustics(scene, renderer_name: str) -> bool:
    if renderer_name != "cycles":
        return False

    cycles = _get_cycles_settings(scene)
    if cycles is None:
        return False

    try:
        reflective = bool(getattr(cycles, "caustics_reflective", False))
    except Exception:
        reflective = False

    try:
        refractive = bool(getattr(cycles, "caustics_refractive", False))
    except Exception:
        refractive = False

    return reflective or refractive


def extract_render_settings() -> RenderSettingsContext:
    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    scene = _get_scene()
    if scene is None:
        raise RuntimeError("No Blender scene available.")

    engine = _get_render_engine(scene)
    renderer_name = _get_renderer_name(engine)
    renderer_version = _get_renderer_version()

    render_device = _get_render_device(scene, renderer_name)
    render_mode = _get_render_mode(renderer_name)
    bucket_scanning_mode = ""

    is_progressive = renderer_name == "cycles"
    is_bucket = False

    denoiser_enabled, denoiser_type = _extract_denoiser_settings(scene, renderer_name)
    adaptive_sampling_enabled, adaptive_threshold, noise_threshold = _extract_adaptive_sampling(scene, renderer_name)

    motion_blur_enabled = _extract_motion_blur(scene)
    depth_of_field_enabled = _extract_depth_of_field(scene)

    thread_mode, thread_count = _extract_thread_mode(scene)

    use_displacement = False
    use_subsurface = False
    use_volumes = False
    use_caustics = _extract_use_caustics(scene, renderer_name)

    texture_auto_tx_enabled = False
    force_linear_textures = False

    render_engine_mode = engine
    tile_size_x, tile_size_y = _extract_tile_size(scene, renderer_name)

    return RenderSettingsContext(
        renderer_name=renderer_name,
        renderer_version=renderer_version,
        render_device=render_device,
        render_mode=render_mode,
        bucket_scanning_mode=bucket_scanning_mode,
        is_progressive=is_progressive,
        is_bucket=is_bucket,
        denoiser_enabled=denoiser_enabled,
        denoiser_type=denoiser_type,
        adaptive_sampling_enabled=adaptive_sampling_enabled,
        adaptive_threshold=adaptive_threshold,
        noise_threshold=noise_threshold,
        motion_blur_enabled=motion_blur_enabled,
        depth_of_field_enabled=depth_of_field_enabled,
        thread_mode=thread_mode,
        thread_count=thread_count,
        use_displacement=use_displacement,
        use_subsurface=use_subsurface,
        use_volumes=use_volumes,
        use_caustics=use_caustics,
        texture_auto_tx_enabled=texture_auto_tx_enabled,
        force_linear_textures=force_linear_textures,
        render_engine_mode=render_engine_mode,
        tile_size_x=tile_size_x,
        tile_size_y=tile_size_y,
    )