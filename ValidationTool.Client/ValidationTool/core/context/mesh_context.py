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

    has_ngons: bool
    ngons_quant: int

    has_non_manifold_geo: bool
    has_zeroArea_faces: bool

    has_hidden_faces: bool
    hidden_faces_quant: int

    has_isolated_vertices: bool
    isolated_faces_quant: int

    has_lamina_faces:bool
    has_degenerate_faces: bool

    has_normals:bool
    has_broken_normals:bool

    has_overlapping_geo: bool

    bounding_box_min: tuple
    bounding_box_max: tuple
    collision_readiness: bool

    has_hard_edges: bool

    has_history: bool

    skeleton_name: str = ""

    uv_sets: list = field(default_factory=list)
    materials: list = field(default_factory=list)
