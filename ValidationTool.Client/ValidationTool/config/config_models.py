from dataclasses import dataclass
import re
from typing import List

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