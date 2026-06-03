import json
import re
from pathlib import Path

from config.config_models import (
    ValidationConfig,
    NamingRules,
    MeshBudget,
    BudgetsConfig
)


class ConfigLoader:

    def __init__(self, config_folder):
        self.config_folder = config_folder

    def load_validation_config(self):

        path = self.config_folder / "configurations" / "validation_config.json"

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return ValidationConfig(
            strict_mode=data.get("StrictMode", False),
            fail_on_first_error=data.get("FailOnFirstError", False),
            auto_fix_enabled=data.get("AutoFixEnabled", False),
            include_info=data.get("IncludeInfo", True),
            include_warnings=data.get("IncludeWarnings", True),
            debug_mode=data.get("DebugMode", False)
        )

    def load_naming_rules(self):

        path = self.config_folder / "configurations" / "naming_rules.json"

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return NamingRules(
            valid_prefixes=data.get("ValidPrefixes", []),
            default_maya_names=data.get("DefaultMayaNames", []),
            name_pattern=re.compile(data.get("NamePattern", ""))
        )

    def load_budgets(self):

        path = self.config_folder / "configurations" / "budgets.json"

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        def budget(name):

            block = data.get(name, {})

            return MeshBudget(
                max_vertices=block.get("MaxVertices", 0),
                max_triangles=block.get("MaxTriangles", 0),
                max_material_slots=block.get("MaxMaterialSlots", 0)
            )

        return BudgetsConfig(
            static_mesh=budget("StaticMesh"),
            character=budget("Character"),
            weapon=budget("Weapon"),
            prop=budget("Prop"),
            environment=budget("Environment")
        )