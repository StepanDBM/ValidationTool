try:
    import maya.cmds as cmds
except ImportError:
    cmds = None

MAYA_LIGHT_TYPES = {
    "ambientLight": "AMBIENT",
    "directionalLight": "DIRECTIONAL",
    "pointLight": "POINT",
    "spotLight": "SPOT",
    "areaLight": "AREA",
    "volumeLight": "VOLUME",

    "aiAreaLight": "ARNOLD_AREA",
    "aiSkyDomeLight": "ARNOLD_SKYDOME",
    "aiPhotometricLight": "ARNOLD_PHOTOMETRIC",
    "aiMeshLight": "ARNOLD_MESH",
}

def _get_parent_path(full_path: str) -> str:
    parts = full_path.split("|")
    if len(parts) <= 2:
        return ""
    return "|".join(parts[:-1])

def _safe_list_connections(node: str, type_name: str) -> list:
    return cmds.listConnections(node, type=type_name) or []


def _safe_poly_uv_sets(shape: str) -> list:
    return cmds.polyUVSet(shape, query=True, allUVSets=True) or []


def _safe_scale(transform: str) -> tuple[float, float, float]:
    value = cmds.getAttr(f"{transform}.scale")
    if value and isinstance(value, list):
        return tuple(value[0])
    return (1.0, 1.0, 1.0)


def _safe_bbox(node: str) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    bbox = cmds.exactWorldBoundingBox(node)
    return (bbox[0], bbox[1], bbox[2]), (bbox[3], bbox[4], bbox[5])


def _safe_poly_evaluate(shape: str, component: str) -> int:
    try:
        return cmds.polyEvaluate(shape, **{component: True}) or 0
    except Exception:
        return 0


#for most things, but in this case I made them for cameras.
def _get_parent_path(full_path: str) -> str:
    parts = full_path.split("|")
    if len(parts) <= 2:
        return ""
    return "|".join(parts[:-1])


def _safe_get_vec3(attr_name: str) -> tuple[float, float, float]:
    try:
        value = cmds.getAttr(attr_name)
        if value and isinstance(value, list):
            return tuple(value[0])
    except Exception:
        pass
    return (0.0, 0.0, 0.0)


def _safe_get_float(attr_name: str, default: float = 0.0) -> float:
    try:
        value = cmds.getAttr(attr_name)
        if value is not None:
            return float(value)
    except Exception:
        pass
    return default


def _safe_get_bool(attr_name: str, default: bool = False) -> bool:
    try:
        value = cmds.getAttr(attr_name)
        if value is not None:
            return bool(value)
    except Exception:
        pass
    return default


def _safe_get_str(attr_name: str, default: str = "") -> str:
    try:
        value = cmds.getAttr(attr_name)
        if value is not None:
            return str(value)
    except Exception:
        pass
    return default

#for lights, mainly

def _get_light_type(shape: str) -> str:
    node_type = cmds.nodeType(shape)
    return MAYA_LIGHT_TYPES.get(node_type, node_type.upper())


def _safe_get_color(attr_name: str) -> tuple[float, float, float]:
    try:
        value = cmds.getAttr(attr_name)
        if value and isinstance(value, list):
            return tuple(float(v) for v in value[0])
    except Exception:
        pass
    return (1.0, 1.0, 1.0)