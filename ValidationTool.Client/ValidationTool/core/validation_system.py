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


class ObjectType(Enum):
    MESH = "MESH"
    CAMERA = "CAMERA"
    LIGHT = "LIGHT"
    CURVE = "CURVE"
    NURBS = "NURBS"
    TRANSFORM = "TRANSFORM"
    RIG = "RIG"
    SCENE = "SCENE"
    REFERENCE = "REFERENCE"
    UNKNOWN = "UNKNOWN"

class AssetType(Enum):
    PROP = "PROP"
    STATIC_MESH = "STATIC_MESH"
    CHARACTER = "CHARACTER"
    WEAPON = "WEAPON"
    VEHICLE = "VEHICLE"
    ENVIRONMENT = "ENVIRONMENT"
    ENVIRONMENT_MODULAR = "ENVIRONMENT_MODULAR"
    VFX = "VFX"
    UI = "UI"
    UNKNOWN = "UNKNOWN"
    
class GeometryType(Enum):
    STATIC = "STATIC"
    SKELETAL = "SKELETAL"
    DEFORMABLE = "DEFORMABLE"

@dataclass
class ValidationIssue:
    asset_name: str
    check_name: str
    severity: ValidationSeverity
    message: str
    suggestion: str = ""

#NEW CLASS, 13/06/2026 BaseContext is abstracted from and into every context afterwards.



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