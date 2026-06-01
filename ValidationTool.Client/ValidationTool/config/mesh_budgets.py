from dataclasses import dataclass

@dataclass(frozen=True)
class MeshBudget:
    max_vertices: int
    max_triangles: int
    max_material_slots: int

STATIC_MESH_BUDGET = MeshBudget(
    max_vertices=40000,
    max_triangles=60000,
    max_material_slots=3
)

CHARACTER_BUDGET = MeshBudget(
    max_vertices=80000,
    max_triangles=120000,
    max_material_slots=5
)

WEAPON_BUDGET = MeshBudget(
    max_vertices=15000,
    max_triangles=25000,
    max_material_slots=2
)

PROP_BUDGET = MeshBudget(
    max_vertices=10000,
    max_triangles=15000,
    max_material_slots=2
)

ENVIRONMENT_BUDGET = MeshBudget(
    max_vertices=10000,
    max_triangles=15000,
    max_material_slots=2
)