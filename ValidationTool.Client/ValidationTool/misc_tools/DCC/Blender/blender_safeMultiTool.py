try:
    import bpy
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
