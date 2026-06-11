"""
Core validation system for 3D assets, providing a structured way to define checks, report issues, and manage validation configurations.
Framework + Contracts + Execution system.
by Stepan David Batllori Martinez
"""
from enum import Enum
from dataclasses import dataclass

CHECK_VERTEX_COUNT = "CHECK_VERTEX_COUNT"
CHECK_TRIANGLE_COUNT = "CHECK_TRIANGLE_COUNT"
CHECK_MATERIAL_SLOTS = "CHECK_MATERIAL_SLOTS"
CHECK_UV_SETS = "CHECK_UV_SETS"
CHECK_TRANSFORMS = "CHECK_TRANSFORMS"
CHECK_NON_MANIFOLD = "CHECK_NON_MANIFOLD"
CHECK_DEGENERATE_FACES = "CHECK_DEGENERATE_FACES"
CHECK_BOUNDING_BOX = "CHECK_BOUNDING_BOX"
CHECK_NAMING = "CHECK_NAMING"
CHECK_SKELETON_COMPAT = "CHECK_SKELETON_COMPAT"
CHECK_HIDDEN_GEOMETRY = "CHECK_HIDDEN_GEOMETRY"
CHECK_COLLISION_READINESS = "CHECK_COLLISION_READINESS"

class ValidationSeverity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    HARD = "ERROR_HARD"  # Subsequent issues should be avoided. IE: no-faces means NO UVs, so no UV check needed.

class AssetType(Enum):
    STATIC_MESH = "STATIC_MESH"
    SKELETAL_MESH = "SKELETAL_MESH"
    PROP = "PROP"
    CHARACTER = "CHARACTER"
    WEAPON = "WEAPON"
    ENVIRONMENT_MODULAR = "ENVIRONMENT_MODULAR"
    UNKNOWN = "UNKNOWN"

@dataclass
class ValidationIssue:
    asset_name: str
    check_name: str
    severity: ValidationSeverity
    message: str
    suggestion: str = ""

@dataclass
class ObjectContext:
    name: str
    asset_type: AssetType

    vertex_count: int
    triangle_count: int

    scale: tuple[float, float, float]

    material_slot_count: int

    has_uv0: bool
    has_uv1: bool

    has_negative_scale: bool
    has_non_manifold_geo: bool
    has_degenerate_faces: bool

    bounding_box_min: tuple  # (x,y,z)
    bounding_box_max: tuple

    skeleton_name: str = ""

    uv_sets: list = None
    materials: list = None