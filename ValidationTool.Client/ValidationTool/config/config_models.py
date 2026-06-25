from __future__ import annotations
from dataclasses import dataclass, field, asdict
import re
from typing import List, Any

@dataclass
class ValidationConfig:
    strict_mode: bool = False
    fail_on_first_error: bool = False
    auto_fix_enabled: bool = False
    include_info: bool = True
    include_warnings: bool = True
    debug_mode: bool = False
    

@dataclass
class NamingRules:
    valid_prefixes: List[str]
    default_maya_names: List[str]
    name_pattern: re.Pattern

@dataclass
class MeshBudget:
    max_vertices: int
    max_triangles: int
    max_material_slots: int

@dataclass
class BudgetsConfig:
    static_mesh: MeshBudget
    character: MeshBudget
    weapon: MeshBudget
    prop: MeshBudget
    environment: MeshBudget




# ============================================================
# SECTION DTOs
# ============================================================

@dataclass
class GeometryBudget:
    vertices_max: int = 50000
    triangles_max: int = 100000
    faces_max: int = 50000
    edges_max: int = 150000
    ngons_max: int = 0
    lamina_faces_max: int = 0
    isolated_vertices_max: int = 0
    hard_edges_max: int = 1000
    mesh_count_max: int = 50
    shells_max: int = 20
    bounding_box_diagonal_max: float = 10000.0
    scale_max: float = 1000.0
    non_uniform_scale_ratio_max: float = 10.0


@dataclass
class UvBudget:
    uv_sets_max: int = 2
    empty_uv_sets_max: int = 0
    duplicate_uv_set_names_max: int = 0
    uv_shells_max: int = 100
    overlap_percent_max: float = 0.0
    out_of_range_uvs_max: int = 0
    texel_density_min: float = 1.0
    texel_density_max: float = 20.0
    udim_tiles_max: int = 10


@dataclass
class MaterialBudget:
    material_slots_max: int = 6
    unique_materials_max: int = 10
    unused_materials_max: int = 0
    shader_node_count_max: int = 50
    texture_samplers_max: int = 10
    layered_shaders_max: int = 4
    default_material_allowed: bool = False


@dataclass
class TextureBudget:
    texture_count_max: int = 50
    texture_resolution_max: int = 4096
    texture_resolution_min: int = 256
    textures_4k_max: int = 10
    textures_8k_max: int = 0
    total_texture_memory_mb_max: int = 2048
    missing_textures_max: int = 0
    non_power_of_two_max: int = 0


@dataclass
class RiggingBudget:
    joint_count_max: int = 256
    deform_joints_max: int = 128
    controls_max: int = 300
    constraints_max: int = 200
    blendshapes_max: int = 100
    influences_per_vertex_max: int = 4


@dataclass
class AnimationBudget:
    key_count_max: int = 10000
    keyed_channels_max: int = 500
    frame_range_max: int = 2000
    animation_layers_max: int = 10
    clips_max: int = 50


@dataclass
class LightingBudget:
    light_count_max: int = 50
    shadow_casters_max: int = 20
    area_lights_max: int = 20
    environment_lights_max: int = 2
    light_groups_max: int = 10
    volumetric_lights_max: int = 5


@dataclass
class CameraBudget:
    camera_count_max: int = 10
    renderable_cameras_max: int = 1
    overscan_max: float = 1.1
    focal_length_min: float = 12.0
    focal_length_max: float = 200.0
    default_camera_render_allowed: bool = False


@dataclass
class RenderBudget:
    aa_samples_max: int = 8
    diffuse_samples_max: int = 4
    specular_samples_max: int = 4
    transmission_samples_max: int = 4
    sss_samples_max: int = 4
    volume_samples_max: int = 2
    adaptive_threshold_max: float = 0.05
    noise_threshold_max: float = 0.05
    tile_size_max: int = 512
    ray_depth_total_max: int = 8
    ray_depth_diffuse_max: int = 2
    ray_depth_specular_max: int = 2
    ray_depth_transmission_max: int = 4


@dataclass
class OutputBudget:
    resolution_x_max: int = 4096
    resolution_y_max: int = 4096
    resolution_x_min: int = 640
    resolution_y_min: int = 360
    aov_count_max: int = 20
    required_multilayer_exr: bool = False
    output_path_must_be_writable: bool = True


@dataclass
class ColorManagementBudget:
    aces_required: bool = False
    linear_workflow_required: bool = True
    gamma_min: float = 0.8
    gamma_max: float = 2.2
    exposure_min: float = -5.0
    exposure_max: float = 5.0


@dataclass
class SceneHygieneBudget:
    unknown_nodes_max: int = 0
    duplicate_names_max: int = 0
    namespaces_max: int = 5
    broken_references_max: int = 0
    missing_references_max: int = 0
    script_nodes_max: int = 0
    expressions_max: int = 0


@dataclass
class ExportBudget:
    export_file_size_mb_max: int = 500
    draw_calls_max: int = 1000
    submeshes_max: int = 20
    lod_count_max: int = 4
    collision_meshes_max: int = 10


@dataclass
class PerformanceBudget:
    validation_runtime_seconds_max: int = 120
    scene_open_time_seconds_max: int = 60
    memory_estimate_mb_max: int = 8192
    render_cost_score_max: int = 100
    json_report_size_kb_max: int = 2048


# ============================================================
# ROOT DTO
# ============================================================

@dataclass
class BudgetConfig:
    geometry: GeometryBudget = field(default_factory=GeometryBudget)
    uv: UvBudget = field(default_factory=UvBudget)
    materials: MaterialBudget = field(default_factory=MaterialBudget)
    textures: TextureBudget = field(default_factory=TextureBudget)
    rigging: RiggingBudget = field(default_factory=RiggingBudget)
    animation: AnimationBudget = field(default_factory=AnimationBudget)
    lighting: LightingBudget = field(default_factory=LightingBudget)
    camera: CameraBudget = field(default_factory=CameraBudget)
    render: RenderBudget = field(default_factory=RenderBudget)
    output: OutputBudget = field(default_factory=OutputBudget)
    color_management: ColorManagementBudget = field(default_factory=ColorManagementBudget)
    scene_hygiene: SceneHygieneBudget = field(default_factory=SceneHygieneBudget)
    export: ExportBudget = field(default_factory=ExportBudget)
    performance: PerformanceBudget = field(default_factory=PerformanceBudget)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "BudgetConfig":
        data = data or {}

        return cls(
            geometry=GeometryBudget(**data.get("geometry", {})),
            uv=UvBudget(**data.get("uv", {})),
            materials=MaterialBudget(**data.get("materials", {})),
            textures=TextureBudget(**data.get("textures", {})),
            rigging=RiggingBudget(**data.get("rigging", {})),
            animation=AnimationBudget(**data.get("animation", {})),
            lighting=LightingBudget(**data.get("lighting", {})),
            camera=CameraBudget(**data.get("camera", {})),
            render=RenderBudget(**data.get("render", {})),
            output=OutputBudget(**data.get("output", {})),
            color_management=ColorManagementBudget(**data.get("color_management", {})),
            scene_hygiene=SceneHygieneBudget(**data.get("scene_hygiene", {})),
            export=ExportBudget(**data.get("export", {})),
            performance=PerformanceBudget(**data.get("performance", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


    def debug_print_budget_config(budgets: "BudgetConfig") -> None:
        """
        Pretty-print the full BudgetConfig in a stable, ordered way for debugging.
        """
        if budgets is None:
            print("[BUDGET DEBUG] BudgetConfig is None")
            return

        data: dict[str, Any] = asdict(budgets)

        section_order = [
            "geometry",
            "uv",
            "materials",
            "textures",
            "rigging",
            "animation",
            "lighting",
            "camera",
            "render",
            "output",
            "color_management",
            "scene_hygiene",
            "export",
            "performance",
        ]

        pretty_names = {
            "geometry": "Geometry",
            "uv": "UV",
            "materials": "Materials",
            "textures": "Textures",
            "rigging": "Rigging",
            "animation": "Animation",
            "lighting": "Lighting",
            "camera": "Camera",
            "render": "Render",
            "output": "Output",
            "color_management": "Color Management",
            "scene_hygiene": "Scene Hygiene",
            "export": "Export",
            "performance": "Performance",
        }

        print("\n" + "=" * 80)
        print("BUDGET CONFIG DEBUG")
        print("=" * 80)

        for section_name in section_order:
            section_data = data.get(section_name, {})

            print(f"\n--- {pretty_names.get(section_name, section_name)} ---")

            if not section_data:
                print("  <empty>")
                continue

            for key, value in section_data.items():
                print(f"  {key:<35} : {value}")

        print("\n" + "=" * 80 + "\n")