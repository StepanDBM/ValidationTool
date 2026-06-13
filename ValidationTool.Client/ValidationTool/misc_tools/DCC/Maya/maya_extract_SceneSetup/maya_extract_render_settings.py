from core.context.SceneContext.render_settings_context import RenderSettingsContext

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _safe_get_float,
    _safe_get_bool,
    _safe_get_int,
    _safe_get_str,
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


_RENDER_DEVICE_MAP = {
    0: "CPU",
    1: "GPU",
    2: "HYBRID",
}

_BUCKET_SCANNING_MAP = {
    0: "TOP",
    1: "LEFT",
    2: "RANDOM",
    3: "WEAVE",
    4: "SPIRAL",
    5: "HILBERT",
}

_THREAD_MODE_MAP = {
    0: "AUTO",
    1: "FIXED",
    2: "CUSTOM",
}

_RENDER_MODE_MAP = {
    "arnold": "FINAL",
    "mayaSoftware": "FINAL",
    "mayaHardware2": "FINAL",
    "mayaVector": "FINAL",
    "redshift": "FINAL",
    "vray": "FINAL",
}


def _first_existing_attr(attr_names: list[str]) -> str:
    for attr in attr_names:
        try:
            if cmds.objExists(attr):
                return attr
        except Exception:
            continue
    return ""


def _safe_enum_text(attr_names: list[str], mapping: dict[int, str], default: str = "") -> str:
    attr = _first_existing_attr(attr_names)
    if not attr:
        return default

    value = _safe_get_int(attr, None)
    if value is None:
        return default

    return mapping.get(value, str(value))


def _get_current_renderer() -> str:
    return _safe_get_str("defaultRenderGlobals.currentRenderer", "")


def _get_renderer_version(renderer_name: str) -> str:
    renderer_name = renderer_name.lower()

    try:
        if renderer_name == "arnold":
            if cmds.pluginInfo("mtoa", query=True, loaded=True):
                return cmds.pluginInfo("mtoa", query=True, version=True) or ""
        elif renderer_name == "redshift":
            if cmds.pluginInfo("redshift4maya", query=True, loaded=True):
                return cmds.pluginInfo("redshift4maya", query=True, version=True) or ""
        elif renderer_name == "vray":
            if cmds.pluginInfo("vrayformaya", query=True, loaded=True):
                return cmds.pluginInfo("vrayformaya", query=True, version=True) or ""
    except Exception:
        pass

    return ""


def _get_render_device(renderer_name: str) -> str:
    renderer_name = renderer_name.lower()

    if renderer_name == "arnold":
        return _safe_enum_text(
            [
                "defaultArnoldRenderOptions.renderDevice",
                "defaultArnoldRenderOptions.renderingDevice",
            ],
            _RENDER_DEVICE_MAP,
            "CPU",
        )

    if renderer_name == "redshift":
        # Redshift is typically GPU-driven in Maya.
        return "GPU"

    return "CPU"


def _get_render_mode(renderer_name: str) -> str:
    renderer_name = renderer_name.lower()

    if renderer_name == "arnold":
        progressive = _safe_get_bool(
            _first_existing_attr([
                "defaultArnoldRenderOptions.enableProgressiveRender",
                "defaultArnoldRenderOptions.progressiveRender",
            ]),
            False,
        )
        if progressive:
            return "PROGRESSIVE"

        bucket = _first_existing_attr([
            "defaultArnoldDriver.mergeAOVs",
            "defaultArnoldRenderOptions.bucketSize",
        ])
        if bucket:
            return "BUCKET"

    return _RENDER_MODE_MAP.get(renderer_name, "")


def _extract_denoiser_settings(renderer_name: str) -> tuple[bool, str]:
    renderer_name = renderer_name.lower()

    if renderer_name == "arnold":
        enabled = _safe_get_bool(
            _first_existing_attr([
                "defaultArnoldRenderOptions.enableDenoising",
                "defaultArnoldRenderOptions.enableOptixDenoiser",
                "defaultArnoldRenderOptions.enableNoiceDenoiser",
            ]),
            False,
        )

        denoiser_type = _safe_get_str(
            _first_existing_attr([
                "defaultArnoldRenderOptions.denoiser",
                "defaultArnoldRenderOptions.aiDenoiser",
            ]),
            "",
        )

        return enabled, denoiser_type

    return False, ""


def _extract_bucket_scanning(renderer_name: str) -> str:
    renderer_name = renderer_name.lower()

    if renderer_name == "arnold":
        return _safe_enum_text(
            [
                "defaultArnoldRenderOptions.bucketScanning",
            ],
            _BUCKET_SCANNING_MAP,
            "",
        )

    return ""


def _extract_thread_mode() -> tuple[str, int]:
    thread_mode = _safe_enum_text(
        [
            "defaultRenderGlobals.numCpusToUseMode",
        ],
        _THREAD_MODE_MAP,
        "",
    )

    thread_count = _safe_get_int(
        _first_existing_attr([
            "defaultRenderGlobals.numCpusToUse",
        ]),
        0,
    )

    return thread_mode, thread_count


def _extract_tile_size(renderer_name: str) -> tuple[int, int]:
    renderer_name = renderer_name.lower()

    if renderer_name == "arnold":
        tile = _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.bucketSize",
            ]),
            0,
        )
        return tile, tile

    return 0, 0


def extract_render_settings() -> RenderSettingsContext:
    """
    Extract renderer/engine execution settings from the current Maya scene.

    This focuses on scene-global renderer configuration such as:
    - renderer identity
    - device selection
    - render mode (progressive/bucket)
    - denoiser
    - adaptive sampling toggles
    - motion blur / DOF
    - thread mode / tile size
    """

    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    renderer_name = _get_current_renderer()
    renderer_version = _get_renderer_version(renderer_name)

    render_device = _get_render_device(renderer_name)
    render_mode = _get_render_mode(renderer_name)
    bucket_scanning_mode = _extract_bucket_scanning(renderer_name)

    is_progressive = render_mode == "PROGRESSIVE"
    is_bucket = render_mode == "BUCKET"

    denoiser_enabled, denoiser_type = _extract_denoiser_settings(renderer_name)

    adaptive_sampling_enabled = _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldRenderOptions.enableAdaptiveSampling",
            "defaultArnoldRenderOptions.adaptiveSampling",
        ]),
        False,
    )

    adaptive_threshold = _safe_get_float(
        _first_existing_attr([
            "defaultArnoldRenderOptions.AAAdaptiveThreshold",
            "defaultArnoldRenderOptions.adaptiveThreshold",
        ]),
        0.0,
    )

    noise_threshold = _safe_get_float(
        _first_existing_attr([
            "defaultArnoldRenderOptions.AASampleClamp",
            "defaultArnoldRenderOptions.noiseThreshold",
        ]),
        0.0,
    )

    motion_blur_enabled = _safe_get_bool(
        _first_existing_attr([
            "defaultRenderGlobals.motionBlur",
            "defaultArnoldRenderOptions.motion_blur_enable",
            "defaultArnoldRenderOptions.ignoreMotionBlur",
        ]),
        False,
    )

    depth_of_field_enabled = False
    for cam_shape in cmds.ls(type="camera", long=True) or []:
        if _safe_get_bool(f"{cam_shape}.depthOfField", False):
            depth_of_field_enabled = True
            break

    thread_mode, thread_count = _extract_thread_mode()

    use_displacement = _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldRenderOptions.enableDisplacement",
        ]),
        False,
    )

    use_subsurface = False
    use_volumes = False
    use_caustics = _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldRenderOptions.enableCaustics",
        ]),
        False,
    )

    texture_auto_tx_enabled = _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldRenderOptions.autotx",
            "defaultArnoldRenderOptions.autoTx",
        ]),
        False,
    )

    force_linear_textures = _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldRenderOptions.forceTranslateShadingEngines",
        ]),
        False,
    )

    render_engine_mode = _safe_get_str(
        _first_existing_attr([
            "defaultArnoldRenderOptions.renderType",
        ]),
        "",
    )

    tile_size_x, tile_size_y = _extract_tile_size(renderer_name)

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
