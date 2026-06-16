import re

from core.context.SceneContext.aov_context import AovContext

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _safe_get_bool,
    _safe_get_str,
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


_VALID_AOV_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")

_BUILTIN_AOVS = {
    "beauty",
    "rgba",
    "rgb",
    "alpha",
    "depth",
    "z",
    "normal",
    "n",
    "position",
    "p",
    "diffuse",
    "diffuse_direct",
    "diffuse_indirect",
    "specular",
    "specular_direct",
    "specular_indirect",
    "transmission",
    "sss",
    "emission",
    "coat",
    "sheen",
    "volume",
    "motionvector",
    "crypto_asset",
    "crypto_material",
    "crypto_object",
}

_REQUIRED_AOVS = {
    # Keep empty or project-specific if your pipeline requires some by default.
    # Example: "beauty"
}


def _first_existing_attr(attr_names: list[str]) -> str:
    for attr in attr_names:
        try:
            if attr and cmds.objExists(attr):
                return attr
        except Exception:
            continue
    return ""


def _get_output_prefix() -> str:
    return _safe_get_str("defaultRenderGlobals.imageFilePrefix", "")


def _get_default_output_path() -> str:
    try:
        images_rule = cmds.workspace(fileRuleEntry="images") or "images"
        expanded = cmds.workspace(expandName=images_rule) or ""
        return expanded
    except Exception:
        return ""

def _get_aov_name(aov_node: str) -> str:
    return _safe_get_str(f"{aov_node}.name", aov_node)


def _is_aov_enabled(aov_node: str) -> bool:
    return _safe_get_bool(f"{aov_node}.enabled", False)


def _has_valid_name(name: str) -> bool:
    return bool(_VALID_AOV_NAME_PATTERN.match(name))


def _is_builtin(name: str) -> bool:
    return name.lower() in _BUILTIN_AOVS


def _is_required(name: str) -> bool:
    return name.lower() in _REQUIRED_AOVS


def _guess_source_type(name: str, aov_node: str) -> str:
    lname = name.lower()

    if lname.startswith("crypto_") or "cryptomatte" in lname:
        return "CRYPTOMATTE"

    if _safe_get_str(f"{aov_node}.lightGroups", ""):
        return "LIGHT_GROUP"

    if _is_builtin(name):
        return "BUILTIN"

    return "CUSTOM"


def _get_light_group(aov_node: str) -> str:
    return _safe_get_str(
        _first_existing_attr([
            f"{aov_node}.lightGroups",
            f"{aov_node}.lightGroup",
        ]),
        "",
    )


def _get_connected_node_of_type(node: str, node_type: str) -> str:
    try:
        conns = cmds.listConnections(node, type=node_type) or []
        if conns:
            return conns[0]
    except Exception:
        pass
    return ""


def _get_driver_name(aov_node: str) -> str:
    driver_node = _get_connected_node_of_type(aov_node, "aiAOVDriver")
    if not driver_node:
        driver_node = "defaultArnoldDriver" if cmds.objExists("defaultArnoldDriver") else ""

    if not driver_node:
        return ""

    translator = _safe_get_str(f"{driver_node}.aiTranslator", "")
    return translator or driver_node


def _get_filter_name(aov_node: str) -> str:
    filter_node = _get_connected_node_of_type(aov_node, "aiAOVFilter")
    if not filter_node:
        filter_node = _get_connected_node_of_type(aov_node, "aiFilter")

    if not filter_node:
        return ""

    return _safe_get_str(f"{filter_node}.aiTranslator", "") or filter_node


def _guess_data_type(name: str, source_type: str) -> str:
    lname = name.lower()

    if source_type == "CRYPTOMATTE":
        return "RGBA"

    if lname in {"normal", "n", "position", "p", "motionvector"}:
        return "VECTOR"

    if lname in {"z", "depth", "alpha"}:
        return "FLOAT"

    return "RGBA"


def _get_output_path_for_aov(aov_node: str) -> str:
    driver_node = _get_connected_node_of_type(aov_node, "aiAOVDriver")
    if driver_node:
        prefix = _safe_get_str(
            _first_existing_attr([
                f"{driver_node}.prefix",
                f"{driver_node}.filePrefix",
            ]),
            "",
        )
        if prefix:
            return prefix

    return _get_default_output_path()


""" might as well follow blender's suit and create a nice list of disabled aovs in the result window
def _get_ai_aov_nodes() -> list[str]:
    return cmds.ls(type="aiAOV") or []
"""

def _get_ai_aov_nodes() -> dict[str, str]:
    """
    Returns a mapping:
        { aov_name_lower : aiAOV_node_name }

    Only real scene-configured aiAOV nodes are returned here.
    """
    nodes = cmds.ls(type="aiAOV") or []
    result: dict[str, str] = {}

    for node in nodes:
        name = _get_aov_name(node)
        if not name:
            continue

        result[name.lower()] = node

    return result


def _get_available_aov_entries() -> list[tuple[str, str | None]]:
    """
    Returns a merged list of:
    - all built-in available AOV names (implicit Maya/Arnold options)
    - real scene aiAOV nodes where they exist
    - custom aiAOV nodes not present in the built-in list

    Output shape:
        [(aov_name, aiAOV_node_or_None), ...]
    """
    node_map = _get_ai_aov_nodes()
    entries: list[tuple[str, str | None]] = []
    seen = set()

    # 1) Built-in / implicit AOVs, even if they do not exist as nodes yet
    for builtin_name in sorted(_BUILTIN_AOVS):
        node = node_map.get(builtin_name.lower())
        entries.append((builtin_name, node))
        seen.add(builtin_name.lower())

    # 2) Any custom scene nodes not already represented above
    for node_name_lower, node in node_map.items():
        if node_name_lower in seen:
            continue

        real_name = _get_aov_name(node) or node_name_lower
        entries.append((real_name, node))
        seen.add(node_name_lower)

    return entries


def _make_implicit_aov_context(name: str, output_prefix: str) -> AovContext:
    source_type = "CRYPTOMATTE" if name.lower().startswith("crypto_") else "BUILTIN"
    data_type = _guess_data_type(name, source_type)

    # Treat beauty / rgba / rgb as implicitly enabled outputs
    implicitly_enabled = name.lower() in {"beauty", "rgba", "rgb"}

    return AovContext(
        name=name,
        enabled=implicitly_enabled,
        data_type=data_type,
        source_type=source_type,
        driver="defaultArnoldDriver" if cmds.objExists("defaultArnoldDriver") else "",
        filter="",
        light_group="",
        is_builtin=_is_builtin(name),
        output_path=_get_default_output_path(),
        output_prefix=output_prefix,
        has_valid_name=_has_valid_name(name),
        is_required=_is_required(name),
    )


def extract_aovs() -> list[AovContext]:
    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    output_prefix = _get_output_prefix()
    contexts: list[AovContext] = []

    for name, aov_node in _get_available_aov_entries():
        # Built-in implicit entry with no real aiAOV node in scene yet
        if not aov_node:
            contexts.append(_make_implicit_aov_context(name, output_prefix))
            continue

        enabled = _is_aov_enabled(aov_node)
        source_type = _guess_source_type(name, aov_node)
        light_group = _get_light_group(aov_node)
        is_builtin = _is_builtin(name)

        driver = _get_driver_name(aov_node)
        filter_name = _get_filter_name(aov_node)
        data_type = _guess_data_type(name, source_type)
        output_path = _get_output_path_for_aov(aov_node)

        context = AovContext(
            name=name,
            enabled=enabled,
            data_type=data_type,
            source_type=source_type,
            driver=driver,
            filter=filter_name,
            light_group=light_group,
            is_builtin=is_builtin,
            output_path=output_path,
            output_prefix=output_prefix,
            has_valid_name=_has_valid_name(name),
            is_required=_is_required(name),
        )

        contexts.append(context)

    return contexts