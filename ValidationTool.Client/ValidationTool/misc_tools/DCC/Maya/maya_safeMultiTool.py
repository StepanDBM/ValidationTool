from dataclasses import asdict, is_dataclass
from pprint import pformat

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

def _safe_arnold_loaded():
    try:
        if not cmds.pluginInfo("mtoa", query=True, loaded=True):
            cmds.loadPlugin("mtoa")
    except Exception:
        pass  # fail silently if Arnold not available

def _pretty_print_context(title: str, obj):
    print(f"\n[{title}]")
    print("-" * (len(title) + 2))

    if is_dataclass(obj):
        print(pformat(asdict(obj), sort_dicts=False, width=120))
    else:
        print(pformat(obj, sort_dicts=False, width=120))



def _get_scene_path() -> str:
    try:
        return cmds.file(query=True, sceneName=True) or ""
    except Exception:
        return ""

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

def _safe_count_ngons(shape: str) -> int:
    try:
        faces = cmds.ls(f"{shape}.f[*]", flatten=True) or []
        count = 0

        for f in faces:
            vtx_count = cmds.polyEvaluate(f, vertex=True)
            if vtx_count and vtx_count > 4:
                count += 1

        return count

    except Exception:
        return 0
    
def _safe_has_non_manifold(shape: str) -> bool:
    try:
        result = cmds.polyInfo(shape, nonManifold=True)
        return bool(result)
    except Exception:
        return False


def _safe_has_lamina_faces(shape: str) -> bool:
    try:
        result = cmds.polyInfo(shape, laminaFaces=True)
        return bool(result)
    except Exception:
        return False


def _safe_count_zero_area_faces(shape: str, threshold=1e-6) -> int:
    try:
        faces = cmds.ls(f"{shape}.f[*]", flatten=True) or []
        count = 0

        for f in faces:
            area = cmds.polyEvaluate(f, area=True)
            if area is not None and area < threshold:
                count += 1

        return count

    except Exception:
        return 0
    
def _safe_has_history(shape: str) -> bool:
    try:
        history = cmds.listHistory(shape) or []
        return len(history) > 1
    except Exception:
        return False
    
def _safe_count_hard_edges(shape: str) -> int:
    try:
        edges = cmds.ls(f"{shape}.e[*]", flatten=True) or []
        count = 0

        for e in edges:
            angle = cmds.polySoftEdge(e, query=True, angle=True)
            if angle == 0:
                count += 1

        return count

    except Exception:
        return 0

def _safe_has_normals(shape: str) -> bool:
    try:
        normals = cmds.polyNormalPerVertex(shape, query=True, xyz=True)
        return bool(normals)
    except Exception:
        return False

def _safe_count_hidden_faces(shape: str) -> int:
    try:
        faces = cmds.ls(f"{shape}.f[*]", flatten=True) or []
        hidden_count = 0

        for f in faces:
            try:
                if not cmds.getAttr(f"{f}.visibility"):
                    hidden_count += 1
            except Exception:
                continue

        return hidden_count

    except Exception:
        return 0

def _safe_count_isolated_vertices(shape: str) -> int:
    try:
        vertices = cmds.ls(f"{shape}.vtx[*]", flatten=True) or []
        count = 0

        for v in vertices:
            try:
                connected_faces = cmds.polyListComponentConversion(
                    v,
                    fromVertex=True,
                    toFace=True
                )
                connected_faces = cmds.ls(connected_faces, flatten=True) or []

                if not connected_faces:
                    count += 1

            except Exception:
                continue

        return count

    except Exception:
        return 0

def _safe_count_degenerate_faces(shape: str) -> int:
    try:
        faces = cmds.ls(f"{shape}.f[*]", flatten=True) or []
        degenerate_count = 0

        for face in faces:
            try:
                verts = cmds.polyInfo(face, faceToVertex=True)

                if not verts:
                    continue

                vert_indices = verts[0].split(":")[-1].strip().split()
                unique_indices = set(vert_indices)

                if len(unique_indices) != len(vert_indices):
                    degenerate_count += 1

            except Exception:
                continue

        return degenerate_count

    except Exception:
        return 0

def _safe_has_broken_normals(shape: str) -> bool:
    try:
        normals = cmds.polyNormalPerVertex(shape, query=True, xyz=True)

        if not normals:
            return False

        # normals is a flat list [x,y,z,x,y,z,...]
        for i in range(0, len(normals), 3):
            x, y, z = normals[i:i+3]

            length = (x*x + y*y + z*z) ** 0.5

            if length < 1e-6:
                return True

        return False

    except Exception:
        return False

def _safe_has_overlapping_geo(shape: str, threshold=1e-5) -> bool:
    try:
        faces = cmds.ls(f"{shape}.f[*]", flatten=True) or []
        centers = set()

        for f in faces:
            try:
                center = cmds.xform(f, query=True, worldSpace=True, translation=True)

                key = (
                    round(center[0] / threshold),
                    round(center[1] / threshold),
                    round(center[2] / threshold)
                )

                if key in centers:
                    return True

                centers.add(key)

            except Exception:
                continue

        return False

    except Exception:
        return False








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

def _safe_get_int(attr_name: str, default: int = 0) -> int:
    try:
        value = cmds.getAttr(attr_name)

        if value is None:
            return default

        if isinstance(value, list):
            if value and isinstance(value[0], (list, tuple)) and value[0]:
                return int(value[0][0])
            if value:
                return int(value[0])

        return int(value)

    except Exception:
        return default
    
    
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