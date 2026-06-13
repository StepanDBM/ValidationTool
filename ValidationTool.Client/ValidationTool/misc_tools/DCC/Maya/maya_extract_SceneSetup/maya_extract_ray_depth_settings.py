from core.context.SceneContext.ray_depth_settings_context import RayDepthSettingsContext

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _safe_get_int,
    _safe_get_str,
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


def _first_existing_attr(attr_names: list[str]) -> str:
    for attr in attr_names:
        try:
            if attr and cmds.objExists(attr):
                return attr
        except Exception:
            continue
    return ""


def _get_current_renderer() -> str:
    return _safe_get_str("defaultRenderGlobals.currentRenderer", "").lower()


def _get_total_ray_depth(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GITotalDepth",
            ]),
            0,
        )

    return _safe_get_int(
        _first_existing_attr([
            "defaultRenderQuality.rayTraceDepth",
        ]),
        0,
    )


def _get_diffuse_ray_depth(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GIDiffuseDepth",
            ]),
            0,
        )

    return 0


def _get_specular_ray_depth(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GISpecularDepth",
            ]),
            0,
        )

    return _safe_get_int(
        _first_existing_attr([
            "defaultRenderQuality.reflections",
        ]),
        0,
    )


def _get_transmission_ray_depth(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GITransmissionDepth",
            ]),
            0,
        )

    return _safe_get_int(
        _first_existing_attr([
            "defaultRenderQuality.refractions",
        ]),
        0,
    )


def _get_volume_ray_depth(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GIVolumeDepth",
            ]),
            0,
        )

    return 0


def _get_transparency_depth(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.autoTransparencyDepth",
            ]),
            0,
        )

    return _safe_get_int(
        _first_existing_attr([
            "defaultRenderQuality.transpLimit",
        ]),
        0,
    )


def _get_sss_depth(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GISssDepth",
                "defaultArnoldRenderOptions.GISSSDepth",
            ]),
            0,
        )

    return 0


def extract_ray_depth_settings() -> RayDepthSettingsContext:
    """
    Extract renderer ray-depth / bounce-limit settings from the current Maya scene.

    This includes:
    - total ray depth
    - diffuse/specular/transmission/volume ray depth
    - transparency depth
    - SSS depth
    """

    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    renderer_name = _get_current_renderer()

    total_ray_depth = _get_total_ray_depth(renderer_name)
    diffuse_ray_depth = _get_diffuse_ray_depth(renderer_name)
