from core.context.SceneContext.color_management_context import ColorManagementContext

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _safe_get_bool,
    _safe_get_float,
    _safe_get_int,
    _safe_get_str,
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


_VIEW_TRANSFORM_MAP = {
    0: "RAW",
    1: "SRGB",
    2: "ACES",
    3: "FILMIC",
}

_DISPLAY_DEVICE_MAP = {
    0: "SRGB",
    1: "REC709",
    2: "DISPLAY_P3",
}

_TEXTURE_COLOR_MANAGEMENT_MODE_MAP = {
    0: "AUTO",
    1: "LINEAR",
    2: "RAW",
    3: "SRGB",
}


def _first_existing_attr(attr_names: list[str]) -> str:
    for attr in attr_names:
        try:
            if attr and cmds.objExists(attr):
                return attr
        except Exception:
            continue
    return ""


def _safe_enum_text(attr_names: list[str], mapping: dict[int, str], default: str = "") -> str:
    attr = _first_existing_attr(attr_names)
    if not attr:
        return default

    value = _safe_get_int(attr, 0)
    return mapping.get(value, default or str(value))


def _get_view_transform() -> str:
    # Best-effort: different renderers / Maya versions expose different attrs.
    text_value = _safe_get_str(
        _first_existing_attr([
            "defaultViewColorManager.viewTransformName",
            "defaultColorMgtGlobals.viewTransformName",
            "defaultRenderGlobals.viewTransform",
        ]),
        "",
    )
    if text_value:
        return text_value

    return _safe_enum_text(
        [
            "defaultViewColorManager.viewTransform",
            "defaultColorMgtGlobals.viewTransform",
        ],
        _VIEW_TRANSFORM_MAP,
        "",
    )


def _get_display_device() -> str:
    text_value = _safe_get_str(
        _first_existing_attr([
            "defaultViewColorManager.displayName",
            "defaultColorMgtGlobals.displayName",
        ]),
        "",
    )
    if text_value:
        return text_value

    return _safe_enum_text(
        [
            "defaultViewColorManager.display",
            "defaultColorMgtGlobals.display",
        ],
        _DISPLAY_DEVICE_MAP,
        "",
    )


def _get_render_color_space() -> str:
    return _safe_get_str(
        _first_existing_attr([
            "defaultArnoldDriver.colorSpace",
            "defaultColorMgtGlobals.renderingSpaceName",
            "defaultColorMgtGlobals.renderSpaceName",
        ]),
        "",
    )


def _get_texture_color_management_mode() -> str:
    text_value = _safe_get_str(
        _first_existing_attr([
            "defaultColorMgtGlobals.cmConfigFileEnabled",
        ]),
        "",
    )
    if text_value:
        return text_value

    return _safe_enum_text(
        [
            "defaultColorMgtGlobals.imageColorProfileMode",
            "defaultColorMgtGlobals.textureColorSpaceMode",
        ],
        _TEXTURE_COLOR_MANAGEMENT_MODE_MAP,
        "",
    )


def _get_ocio_config() -> str:
    ocio_path = _safe_get_str(
        _first_existing_attr([
            "defaultColorMgtGlobals.configFilePath",
            "defaultColorMgtGlobals.ocioConfigPath",
        ]),
        "",
    )
    if ocio_path:
        return ocio_path

    return _safe_get_str(
        _first_existing_attr([
            "defaultColorMgtGlobals.configFileName",
        ]),
        "",
    )


def _get_linear_workflow_enabled() -> bool:
    return _safe_get_bool(
        _first_existing_attr([
            "defaultColorMgtGlobals.cmEnabled",
            "defaultRenderGlobals.enableDefaultColorMgtGlobals",
        ]),
        False,
    )


def _get_aces_enabled(view_transform: str, render_color_space: str, ocio_config: str) -> bool:
    merged = f"{view_transform} {render_color_space} {ocio_config}".upper()
    return "ACES" in merged


def _get_gamma() -> float:
    return _safe_get_float(
        _first_existing_attr([
            "defaultColorMgtGlobals.outputTransformGamma",
            "defaultColorMgtGlobals.displayGamma",
        ]),
        1.0,
    )


def _get_exposure() -> float:
    return _safe_get_float(
        _first_existing_attr([
            "defaultColorMgtGlobals.outputTransformExposure",
            "defaultColorMgtGlobals.exposure",
        ]),
        0.0,
    )


def _get_look() -> str:
    return _safe_get_str(
        _first_existing_attr([
            "defaultColorMgtGlobals.outputTransformLook",
            "defaultColorMgtGlobals.look",
        ]),
        "",
    )


def extract_color_management() -> ColorManagementContext:
    """
    Extract color-management configuration from the current Maya scene.

    This includes:
    - view transform
    - display device
    - render/output color space
    - texture color-management mode
    - OCIO config
    - linear workflow / ACES state
    - gamma / exposure / look
    """

    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    view_transform = _get_view_transform()
    display_device = _get_display_device()
    render_color_space = _get_render_color_space()

    texture_color_management_mode = _get_texture_color_management_mode()
    ocio_config = _get_ocio_config()

    linear_workflow_enabled = _get_linear_workflow_enabled()
    aces_enabled = _get_aces_enabled(view_transform, render_color_space, ocio_config)

    gamma = _get_gamma()
    exposure = _get_exposure()
    look = _get_look()

    return ColorManagementContext(
        view_transform=view_transform,
        display_device=display_device,
        render_color_space=render_color_space,
        texture_color_management_mode=texture_color_management_mode,
        ocio_config=ocio_config,
        linear_workflow_enabled=linear_workflow_enabled,
        aces_enabled=aces_enabled,
        gamma=gamma,
        exposure=exposure,
        look=look,
    )