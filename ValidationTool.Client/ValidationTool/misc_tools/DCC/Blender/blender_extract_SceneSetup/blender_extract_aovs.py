import re

from core.context.SceneContext.aov_context import AovContext
from misc_tools.DCC.Blender.blender_safeMultiTool import (
    _get_scene
)
try:
    import bpy
except ImportError:
    bpy = None


_VALID_AOV_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")

_REQUIRED_AOVS = {
    # Keep empty or project-specific if your pipeline requires some by default.
    # Example: "Combined"
}


def _get_view_layer():
    try:
        return bpy.context.view_layer
    except Exception:
        return None


def _get_output_prefix(scene) -> str:
    try:
        filepath = bpy.path.abspath(scene.render.filepath or "")
        if not filepath:
            return ""

        normalized = filepath.replace("\\", "/")
        if normalized.endswith("/"):
            return ""

        base = normalized.split("/")[-1]
        if "." in base:
            return ".".join(base.split(".")[:-1])

        return base
    except Exception:
        return ""


def _get_output_path(scene) -> str:
    try:
        return bpy.path.abspath(scene.render.filepath or "")
    except Exception:
        return ""


def _has_valid_name(name: str) -> bool:
    return bool(_VALID_AOV_NAME_PATTERN.match(name))


def _is_required(name: str) -> bool:
    return name.lower() in {aov.lower() for aov in _REQUIRED_AOVS}


def _guess_data_type(name: str) -> str:
    lname = name.lower()

    if lname in {"normal", "vector", "uv", "position", "motionvector", "mist"}:
        return "VECTOR"

    if lname in {"z", "depth", "alpha", "ambient_occlusion"}:
        return "FLOAT"

    return "RGBA"


def _builtin_passes_for_view_layer(view_layer) -> list[tuple[str, bool]]:
    if view_layer is None:
        return []

    pass_specs = [
        ("Combined", True),
        ("Z", getattr(view_layer, "use_pass_z", False)),
        ("Mist", getattr(view_layer, "use_pass_mist", False)),
        ("Normal", getattr(view_layer, "use_pass_normal", False)),
        ("Vector", getattr(view_layer, "use_pass_vector", False)),
        ("UV", getattr(view_layer, "use_pass_uv", False)),
        ("Object Index", getattr(view_layer, "use_pass_object_index", False)),
        ("Material Index", getattr(view_layer, "use_pass_material_index", False)),
        ("Diffuse Direct", getattr(view_layer, "use_pass_diffuse_direct", False)),
        ("Diffuse Indirect", getattr(view_layer, "use_pass_diffuse_indirect", False)),
        ("Diffuse Color", getattr(view_layer, "use_pass_diffuse_color", False)),
        ("Glossy Direct", getattr(view_layer, "use_pass_glossy_direct", False)),
        ("Glossy Indirect", getattr(view_layer, "use_pass_glossy_indirect", False)),
        ("Glossy Color", getattr(view_layer, "use_pass_glossy_color", False)),
        ("Transmission Direct", getattr(view_layer, "use_pass_transmission_direct", False)),
        ("Transmission Indirect", getattr(view_layer, "use_pass_transmission_indirect", False)),
        ("Transmission Color", getattr(view_layer, "use_pass_transmission_color", False)),
        ("Emit", getattr(view_layer, "use_pass_emit", False)),
        ("Environment", getattr(view_layer, "use_pass_environment", False)),
        ("AO", getattr(view_layer, "use_pass_ambient_occlusion", False)),
        ("Shadow", getattr(view_layer, "use_pass_shadow", False)),
    ]

    result = []
    for name, enabled in pass_specs:
        result.append((name, bool(enabled)))

    return result


def _cryptomatte_passes_for_view_layer(view_layer) -> list[tuple[str, bool]]:
    if view_layer is None:
        return []

    return [
        ("CryptoObject", bool(getattr(view_layer, "use_pass_cryptomatte_object", False))),
        ("CryptoMaterial", bool(getattr(view_layer, "use_pass_cryptomatte_material", False))),
        ("CryptoAsset", bool(getattr(view_layer, "use_pass_cryptomatte_asset", False))),
    ]


def _custom_aovs_for_view_layer(view_layer) -> list[tuple[str, bool, str]]:
    result = []

    if view_layer is None:
        return result

    try:
        aovs = getattr(view_layer, "aovs", [])
    except Exception:
        aovs = []

    for aov in aovs:
        try:
            name = str(getattr(aov, "name", "") or "")
        except Exception:
            name = ""

        try:
            aov_type = str(getattr(aov, "type", "") or "")
        except Exception:
            aov_type = ""

        enabled = bool(name)
        result.append((name, enabled, aov_type))

    return result


def extract_aovs() -> list[AovContext]:
    """
    Extract Blender render passes / AOV-like outputs from the active View Layer.

    This includes:
    - builtin render passes
    - cryptomatte passes
    - custom AOVs (when available in Blender version / renderer)
    """

    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    scene = _get_scene()
    if scene is None:
        raise RuntimeError("No Blender scene available.")

    view_layer = _get_view_layer()
    output_prefix = _get_output_prefix(scene)
    output_path = _get_output_path(scene)

    contexts: list[AovContext] = []

    # Built-in passes
    for name, enabled in _builtin_passes_for_view_layer(view_layer):
        source_type = "BUILTIN"
        data_type = _guess_data_type(name)

        context = AovContext(
            name=name,
            enabled=enabled,
            data_type=data_type,
            source_type=source_type,
            driver=(scene.render.engine or ""),
            filter="",
            light_group="",
            is_builtin=True,
            output_path=output_path,
            output_prefix=output_prefix,
            has_valid_name=_has_valid_name(name.replace(" ", "_")),
            is_required=_is_required(name),
        )
        contexts.append(context)

    # Cryptomatte passes
    for name, enabled in _cryptomatte_passes_for_view_layer(view_layer):
        context = AovContext(
            name=name,
            enabled=enabled,
            data_type="RGBA",
            source_type="CRYPTOMATTE",
            driver=(scene.render.engine or ""),
            filter="",
            light_group="",
            is_builtin=True,
            output_path=output_path,
            output_prefix=output_prefix,
            has_valid_name=_has_valid_name(name),
            is_required=_is_required(name),
        )
        contexts.append(context)

    # Custom AOVs
    for name, enabled, aov_type in _custom_aovs_for_view_layer(view_layer):
        if not name:
            continue

        data_type = "FLOAT" if aov_type.upper() == "VALUE" else "RGBA"

        context = AovContext(
            name=name,
            enabled=enabled,
            data_type=data_type,
            source_type="CUSTOM",
            driver=(scene.render.engine or ""),
            filter="",
            light_group="",
            is_builtin=False,
            output_path=output_path,
            output_prefix=output_prefix,
            has_valid_name=_has_valid_name(name),
            is_required=_is_required(name),
        )
        contexts.append(context)

    return contexts