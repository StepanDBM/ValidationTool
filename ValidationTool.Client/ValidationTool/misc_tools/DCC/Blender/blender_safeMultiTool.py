try:
    import bpy
    import bmesh
except ImportError:
    bpy = None

def _safe_str(value, default: str = "") -> str:
    try:
        if value is None:
            return default
        return str(value)
    except Exception:
        return default


def _safe_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _safe_bool(value, default: bool = False) -> bool:
    try:
        return bool(value)
    except Exception:
        return default



def _get_scene():
    try:
        return bpy.context.scene
    except Exception:
        return None


def _get_render_engine(scene) -> str:
    try:
        return str(scene.render.engine).upper()
    except Exception:
        return ""


def _get_cycles(scene):
    try:
        return scene.cycles
    except Exception:
        return None


def _get_bmesh(obj):
    if obj.type != 'MESH':
        return None

    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.normal_update()
    return bm

def _safe_count_ngons(obj):
    bm = _get_bmesh(obj)
    if not bm:
        return 0

    count = sum(1 for f in bm.faces if len(f.verts) > 4)
    bm.free()
    return count

def _safe_count_zero_area_faces(obj):
    bm = _get_bmesh(obj)
    if not bm:
        return 0

    count = sum(1 for f in bm.faces if f.calc_area() < 1e-10)
    bm.free()
    return count

def _safe_count_hard_edges(obj):
    bm = _get_bmesh(obj)
    if not bm:
        return 0

    count = sum(1 for e in bm.edges if not e.smooth)
    bm.free()
    return count

def _safe_has_non_manifold(obj):
    bm = _get_bmesh(obj)
    if not bm:
        return False

    for e in bm.edges:
        if not e.is_manifold:
            bm.free()
            return True

    bm.free()
    return False

def _safe_has_lamina_faces(obj):
    bm = _get_bmesh(obj)
    if not bm:
        return False

    seen_faces = set()

    for f in bm.faces:
        key = tuple(sorted(v.index for v in f.verts))
        if key in seen_faces:
            bm.free()
            return True
        seen_faces.add(key)

    bm.free()
    return False

def _safe_has_history(obj):
    return len(obj.modifiers) > 0

def _safe_has_normals(obj):
    return obj.data.has_custom_normals

def _safe_count_hidden_faces(obj):
    bm = _get_bmesh(obj)
    if not bm:
        return 0

    count = sum(1 for f in bm.faces if f.hide)
    bm.free()
    return count

def _safe_count_isolated_vertices(obj):
    bm = _get_bmesh(obj)
    if not bm:
        return 0

    count = sum(1 for v in bm.verts if not v.link_edges)
    bm.free()
    return count

def _safe_count_degenerate_faces(obj):
    bm = _get_bmesh(obj)
    if not bm:
        return 0

    count = 0
    for f in bm.faces:
        if len(set(v.co[:] for v in f.verts)) < 3:
            count += 1

    bm.free()
    return count

def _safe_has_broken_normals(obj):
    mesh = obj.data

    for poly in mesh.polygons:
        if poly.normal.length < 1e-6:
            return True

    return False

def _safe_has_overlapping_geo(obj):
    bm = _get_bmesh(obj)
    if not bm:
        return False

    verts = [tuple(v.co[:]) for v in bm.verts]

    has_overlap = len(verts) != len(set(verts))

    bm.free()
    return has_overlap