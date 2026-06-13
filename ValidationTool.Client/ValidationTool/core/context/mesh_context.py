from dataclasses import dataclass, field
from core.context.baseContext import BaseContext
from core.validation_system import AssetType


@dataclass
class MeshContext(BaseContext):
    asset_type : AssetType
    
    vertex_count: int
    triangle_count: int

    scale: tuple[float, float, float]

    material_slot_count: int

    has_uv0: bool
    has_uv1: bool

    has_negative_scale: bool
    has_non_manifold_geo: bool
    has_degenerate_faces: bool

    bounding_box_min: tuple
    bounding_box_max: tuple

    skeleton_name: str = ""

    uv_sets: list = field(default_factory=list)
    materials: list = field(default_factory=list)
