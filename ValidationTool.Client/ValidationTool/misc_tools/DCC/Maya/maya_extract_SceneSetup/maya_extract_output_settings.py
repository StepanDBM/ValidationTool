import os

from core.context.SceneContext.output_settings_context import OutputSettingsContext

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

#source Autodesk.Help. Fuck was this weird to research.
_IMAGE_FORMAT_MAP = {
    0: "GIF",
    1: "SOFTIMAGE",
    2: "RLA",
    3: "TIFF",
    4: "TIFF16",
    5: "SGI",
    6: "ALIAS",
    7: "JPEG",
    8: "OPENEXR",
    9: "IFF",
    10: "MAYA16IFF",
    11: "CIN",
    12: "YUV",
    13: "SGIMV",
    19: "TGA",
    20: "BMP",
    31: "PNG",
    32: "DDS",
    35: "PSD",
    36: "PSD_LAYERED",
    51: "EXR",
}

#source Autodesk.Help
_EXR_COMPRESSION_MAP = {
    0: "NONE",
    1: "RLE",
    2: "ZIPS",
    3: "ZIP",
    4: "PIZ",
    5: "PXR24",
    6: "B44",
    7: "B44A",
    8: "DWAA",
    9: "DWAB",
}

#source Autodesk.Help
_PNG_COMPRESSION_MAP = {
    0: "NONE",
    1: "FAST",
    2: "MEDIUM",
    3: "HIGH",
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


def _get_output_prefix() -> str:
    return _safe_get_str("defaultRenderGlobals.imageFilePrefix", "")


def _get_file_naming_pattern() -> str:
    # Keep this generic: use the file prefix as the pipeline-facing naming pattern.
    # Maya stores additional naming controls in several attrs, but prefix is the most
    # relevant output token string for validation.
    return _get_output_prefix()


def _get_image_format(renderer_name: str) -> str:
    renderer_name = renderer_name.lower()

    # Arnold usually writes through the Arnold driver.
    if renderer_name == "arnold":
        ai_translator = _safe_get_str("defaultArnoldDriver.aiTranslator", "")
        if ai_translator:
            return ai_translator.upper()

    return _safe_enum_text(
        ["defaultRenderGlobals.imageFormat"],
        _IMAGE_FORMAT_MAP,
        ""
    )


def _get_bit_depth(image_format: str) -> int:
    image_format = (image_format or "").upper()

    # Try renderer-specific attrs first.
    exr_half = _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldDriver.halfPrecision",
            "defaultArnoldDriver.halfPrecisionFloat",
        ]),
        False,
    )

    if image_format in {"EXR", "OPENEXR"}:
        return 16 if exr_half else 32

    if image_format in {"PNG", "TIFF", "TGA", "BMP", "JPEG"}:
        return 8

    if image_format in {"TIFF16", "MAYA16IFF"}:
        return 16

    return 0


def _get_compression(image_format: str) -> str:
    image_format = (image_format or "").upper()

    if image_format in {"EXR", "OPENEXR"}:
        return _safe_enum_text(
            ["defaultArnoldDriver.exrCompression"],
            _EXR_COMPRESSION_MAP,
            ""
        )

    if image_format == "PNG":
        return _safe_enum_text(
            ["defaultRenderGlobals.pngCompression"],
            _PNG_COMPRESSION_MAP,
            ""
        )

    if image_format == "JPEG":
        return "JPEG"

    return ""


def _get_compression_quality(image_format: str) -> int:
    image_format = (image_format or "").upper()

    if image_format == "JPEG":
        return _safe_get_int(
            _first_existing_attr([
                "defaultRenderGlobals.jpegQuality",
            ]),
            0,
        )

    return 0


def _get_color_space() -> str:
    # Output color space is renderer / OCIO dependent. Keep this best-effort.
    return _safe_get_str(
        _first_existing_attr([
            "defaultArnoldDriver.colorSpace",
            "defaultRenderGlobals.colorSpace",
        ]),
        ""
    )


def _get_has_embedded_metadata() -> bool:
    # Best-effort generic switch; renderer-specific metadata is not consistently exposed.
    return _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldDriver.append",
            "defaultRenderGlobals.enableDefaultColorMgtGlobals",
        ]),
        False,
    )


def _get_multilayer_enabled(renderer_name: str, image_format: str) -> bool:
    renderer_name = renderer_name.lower()
    image_format = (image_format or "").upper()

    if renderer_name == "arnold":
        merge_aovs = _safe_get_bool("defaultArnoldDriver.mergeAOVs", False)
        if merge_aovs and image_format in {"EXR", "OPENEXR"}:
            return True

    return False


def _get_alpha_enabled() -> bool:
    return _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldDriver.autocrop",   # not alpha, but a useful fallback attr probe
            "defaultRenderGlobals.outFormatControl",
        ]),
        False,
    )


def _get_premultiplied_alpha() -> bool:
    return _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldDriver.preserveLayerName",
            "defaultRenderGlobals.preMel",
        ]),
        False,
    )


def _get_tile_output_enabled() -> bool:
    return _safe_get_bool(
        _first_existing_attr([
            "defaultArnoldDriver.tiled",
        ]),
        False,
    )


def _get_resolution() -> tuple[int, int]:
    resolution_x = _safe_get_int("defaultResolution.width", 0)
    resolution_y = _safe_get_int("defaultResolution.height", 0)
    return resolution_x, resolution_y


def _get_render_scale_percent() -> int:
    # Maya itself does not use Blender-style resolution %. Keep at 100 unless overridden elsewhere.
    return 100


def _get_device_aspect_ratio() -> float:
    return _safe_get_float("defaultResolution.deviceAspectRatio", 1.0)


def _get_pixel_aspect_ratio() -> float:
    return _safe_get_float("defaultResolution.pixelAspect", 1.0)


def _get_overscan() -> tuple[bool, float]:
    # Overscan is generally camera-level, not global, but studios often treat it as delivery setup.
    # We expose a best-effort aggregate: if any camera has overscan enabled, mark it.
    cameras = cmds.ls(type="camera", long=True) or []

    for cam in cameras:
        if cmds.objExists(f"{cam}.overscan"):
            overscan_value = _safe_get_float(f"{cam}.overscan", 1.0)
            if abs(overscan_value - 1.0) > 1e-5:
                return True, overscan_value

    return False, 0.0


def _get_safe_frame_enabled() -> bool:
    # Safe frame display is a viewport/camera concern more than a render-global one;
    # use best-effort probing from render globals if available.
    return _safe_get_bool(
        _first_existing_attr([
            "defaultResolution.lockDeviceAspectRatio",
        ]),
        False,
    )


def _get_output_path_and_writable(output_prefix: str) -> tuple[str, bool]:
    try:
        images_rule = cmds.workspace(fileRuleEntry="images") or "images"
        project_root = cmds.workspace(query=True, rootDirectory=True) or ""
        base_images_path = cmds.workspace(expandName=images_rule) or os.path.join(project_root, images_rule)
    except Exception:
        project_root = ""
        base_images_path = ""

    # If prefix includes subfolders, preserve them in the displayed output path.
    prefix_dir = ""
    if output_prefix:
        prefix_dir = os.path.dirname(output_prefix)

    if base_images_path and prefix_dir:
        output_path = os.path.normpath(os.path.join(base_images_path, prefix_dir))
    else:
        output_path = os.path.normpath(base_images_path) if base_images_path else ""

    writable_target = output_path or project_root or ""
    output_writable = os.path.isdir(writable_target) and os.access(writable_target, os.W_OK)

    return output_path, output_writable


def extract_output_settings() -> OutputSettingsContext:
    """
    Extract final-render output settings from the current Maya scene.

    This includes:
    - output path / prefix
    - file naming pattern
    - image format / bit depth / compression
    - alpha / multilayer / tile output flags
    - resolution / aspect / overscan
    - basic writability validation for the output directory
    """

    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    renderer_name = _get_current_renderer()
    output_prefix = _get_output_prefix()
    file_naming_pattern = _get_file_naming_pattern()

    image_format = _get_image_format(renderer_name)
    bit_depth = _get_bit_depth(image_format)

    compression = _get_compression(image_format)
    compression_quality = _get_compression_quality(image_format)

    color_space = _get_color_space()
    has_embedded_metadata = _get_has_embedded_metadata()

    multilayer_enabled = _get_multilayer_enabled(renderer_name, image_format)
    alpha_enabled = _get_alpha_enabled()
    premultiplied_alpha = _get_premultiplied_alpha()

    tile_output_enabled = _get_tile_output_enabled()

    resolution_x, resolution_y = _get_resolution()
    render_scale_percent = _get_render_scale_percent()

    device_aspect_ratio = _get_device_aspect_ratio()
    pixel_aspect_ratio = _get_pixel_aspect_ratio()

    overscan_enabled, overscan_value = _get_overscan()
    safe_frame_enabled = _get_safe_frame_enabled()

    output_path, output_writable = _get_output_path_and_writable(output_prefix)

    return OutputSettingsContext(
        output_path=output_path,
        output_prefix=output_prefix,
        file_naming_pattern=file_naming_pattern,

        image_format=image_format,
        bit_depth=bit_depth,

        compression=compression,
        compression_quality=compression_quality,

        color_space=color_space,
        has_embedded_metadata=has_embedded_metadata,

        multilayer_enabled=multilayer_enabled,
        alpha_enabled=alpha_enabled,
        premultiplied_alpha=premultiplied_alpha,

        tile_output_enabled=tile_output_enabled,

        resolution_x=resolution_x,
        resolution_y=resolution_y,
        render_scale_percent=render_scale_percent,

        device_aspect_ratio=device_aspect_ratio,
        pixel_aspect_ratio=pixel_aspect_ratio,

        overscan_enabled=overscan_enabled,
        overscan_value=overscan_value,

        safe_frame_enabled=safe_frame_enabled,
        output_writable=output_writable,
    )