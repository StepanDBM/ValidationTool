import os

from core.context.SceneContext.output_settings_context import OutputSettingsContext
from misc_tools.DCC.Blender.blender_safeMultiTool import (
    _safe_bool,
    _safe_float,
    _safe_int,
    _safe_str
)
try:
    import bpy
except ImportError:
    bpy = None


def _get_scene():
    try:
        return bpy.context.scene
    except Exception:
        return None


def _get_render(scene):
    try:
        return scene.render
    except Exception:
        return None


def _get_image_settings(scene):
    try:
        return scene.render.image_settings
    except Exception:
        return None

def _get_output_path(render) -> str:
    try:
        return bpy.path.abspath(render.filepath or "")
    except Exception:
        return ""


def _get_output_prefix(output_path: str) -> str:
    if not output_path:
        return ""

    normalized = output_path.replace("\\", "/")

    # If it's clearly directory-like, no prefix
    if normalized.endswith("/"):
        return ""

    base = os.path.basename(normalized)

    # If it has an extension, prefix is filename without extension
    if "." in base:
        return os.path.splitext(base)[0]

    # Blender often stores a file prefix without extension
    return base


def _get_file_naming_pattern(output_path: str) -> str:
    return output_path or ""


def _get_image_format(image_settings) -> str:
    try:
        return _safe_str(image_settings.file_format, "")
    except Exception:
        return ""


def _get_bit_depth(image_settings) -> int:
    try:
        return _safe_int(image_settings.color_depth, 0)
    except Exception:
        return 0


def _get_compression(image_settings, image_format: str) -> str:
    image_format = (image_format or "").upper()

    if image_format in {"OPEN_EXR", "OPEN_EXR_MULTILAYER"}:
        try:
            return _safe_str(image_settings.exr_codec, "")
        except Exception:
            return ""

    if image_format in {"PNG", "TIFF", "JPEG2000", "WEBP"}:
        try:
            return _safe_str(image_settings.compression, "")
        except Exception:
            return ""

    if image_format in {"JPEG", "WEBP"}:
        return image_format

    return ""


def _get_compression_quality(image_settings, image_format: str) -> int:
    image_format = (image_format or "").upper()

    if image_format in {"JPEG", "JPEG2000", "WEBP"}:
        try:
            return _safe_int(image_settings.quality, 0)
        except Exception:
            return 0

    return 0


def _get_color_space(image_settings) -> str:
    try:
        return _safe_str(image_settings.color_mode, "")
    except Exception:
        return ""


def _get_has_embedded_metadata(scene) -> bool:
    # Best-effort: Blender stamp settings are metadata/burn-in adjacent, but not a perfect equivalent.
    try:
        render = scene.render
        return _safe_bool(getattr(render, "use_stamp", False), False)
    except Exception:
        return False


def _get_multilayer_enabled(image_format: str) -> bool:
    return (image_format or "").upper() == "OPEN_EXR_MULTILAYER"


def _get_alpha_enabled(image_settings) -> bool:
    try:
        color_mode = _safe_str(image_settings.color_mode, "").upper()
        return "A" in color_mode
    except Exception:
        return False


def _get_premultiplied_alpha(scene) -> bool:
    # Blender versions vary here; use best-effort if alpha_mode exists.
    try:
        alpha_mode = _safe_str(getattr(scene.render, "alpha_mode", ""), "").upper()
        return alpha_mode == "PREMUL"
    except Exception:
        return False


def _get_tile_output_enabled() -> bool:
    # Blender does not expose Maya-style tiled final output in the same way.
    return False


def _get_resolution(render) -> tuple[int, int]:
    try:
        return _safe_int(render.resolution_x, 0), _safe_int(render.resolution_y, 0)
    except Exception:
        return 0, 0


def _get_render_scale_percent(render) -> int:
    try:
        return _safe_int(render.resolution_percentage, 100)
    except Exception:
        return 100


def _get_device_aspect_ratio(resolution_x: int, resolution_y: int) -> float:
    if resolution_y == 0:
        return 0.0
    return float(resolution_x) / float(resolution_y)


def _get_pixel_aspect_ratio(render) -> float:
    try:
        x = _safe_float(render.pixel_aspect_x, 1.0)
        y = _safe_float(render.pixel_aspect_y, 1.0)
        if y == 0.0:
            return x
        return x / y
    except Exception:
        return 1.0


def _get_overscan() -> tuple[bool, float]:
    # No direct global Blender equivalent in standard render output settings.
    return False, 0.0


def _get_safe_frame_enabled() -> bool:
    # Safe areas are viewport/display-side in Blender, not really render-output global settings.
    return False


def _resolve_output_directory(output_path: str) -> str:
    if not output_path:
        return ""

    normalized = output_path.replace("\\", "/")

    # Explicit directory path
    if normalized.endswith("/"):
        return os.path.normpath(output_path)

    # If last segment looks like a file name (has extension), use dirname
    base = os.path.basename(normalized)
    if "." in base:
        return os.path.normpath(os.path.dirname(output_path))

    # Otherwise treat as directory/prefix folder
    return os.path.normpath(output_path)


def _get_output_writable(output_path: str) -> bool:
    output_dir = _resolve_output_directory(output_path)
    if not output_dir:
        return False

    try:
        if os.path.isdir(output_dir):
            return os.access(output_dir, os.W_OK)

        parent = os.path.dirname(output_dir)
        if parent and os.path.isdir(parent):
            return os.access(parent, os.W_OK)
    except Exception:
        pass

    return False


def extract_output_settings() -> OutputSettingsContext:

    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    scene = _get_scene()
    if scene is None:
        raise RuntimeError("No Blender scene available.")

    render = _get_render(scene)
    if render is None:
        raise RuntimeError("No Blender render settings available.")

    image_settings = _get_image_settings(scene)
    if image_settings is None:
        raise RuntimeError("No Blender image settings available.")

    output_path = _get_output_path(render)
    output_prefix = _get_output_prefix(output_path)
    file_naming_pattern = _get_file_naming_pattern(output_path)

    image_format = _get_image_format(image_settings)
    bit_depth = _get_bit_depth(image_settings)

    compression = _get_compression(image_settings, image_format)
    compression_quality = _get_compression_quality(image_settings, image_format)

    color_space = _get_color_space(image_settings)
    has_embedded_metadata = _get_has_embedded_metadata(scene)

    multilayer_enabled = _get_multilayer_enabled(image_format)
    alpha_enabled = _get_alpha_enabled(image_settings)
    premultiplied_alpha = _get_premultiplied_alpha(scene)

    tile_output_enabled = _get_tile_output_enabled()

    resolution_x, resolution_y = _get_resolution(render)
    render_scale_percent = _get_render_scale_percent(render)

    device_aspect_ratio = _get_device_aspect_ratio(resolution_x, resolution_y)
    pixel_aspect_ratio = _get_pixel_aspect_ratio(render)

    overscan_enabled, overscan_value = _get_overscan()
    safe_frame_enabled = _get_safe_frame_enabled()

    output_writable = _get_output_writable(output_path)

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