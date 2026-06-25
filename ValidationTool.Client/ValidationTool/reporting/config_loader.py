import json
import re
from pathlib import Path

from config.config_models import ValidationConfig, NamingRules, BudgetConfig
from core.ProfileManagement.ProfileModels import ProfileConfig


class ConfigLoader:
    def __init__(self, config_folder):
        self.config_folder = Path(config_folder)

    def _load_json(self, path: Path) -> dict:
        if not path.exists():
            return {}

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, path: Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def _get_config_path(self, file_name: str) -> Path:
        return self.config_folder / file_name

    # ============================================================
    # GENERAL VALIDATION CONFIG
    # ============================================================

    def load_validation_config(self) -> ValidationConfig:
        path = self._get_config_path("validation_config.json")
        data = self._load_json(path)

        if not data:
            defaults = ValidationConfig(
                strict_mode=False,
                fail_on_first_error=False,
                auto_fix_enabled=False,
                include_info=True,
                include_warnings=True,
                debug_mode=False
            )
            self.save_validation_config(defaults)
            return defaults

        return ValidationConfig(
            strict_mode=data.get("StrictMode", False),
            fail_on_first_error=data.get("FailOnFirstError", False),
            auto_fix_enabled=data.get("AutoFixEnabled", False),
            include_info=data.get("IncludeInfo", True),
            include_warnings=data.get("IncludeWarnings", True),
            debug_mode=data.get("DebugMode", False)
        )

    def save_validation_config(self, config: ValidationConfig) -> None:
        path = self._get_config_path("validation_config.json")

        data = {
            "StrictMode": config.strict_mode,
            "FailOnFirstError": config.fail_on_first_error,
            "AutoFixEnabled": config.auto_fix_enabled,
            "IncludeInfo": config.include_info,
            "IncludeWarnings": config.include_warnings,
            "DebugMode": config.debug_mode
        }

        self._save_json(path, data)

    # ============================================================
    # NAMING RULES
    # ============================================================

    def load_naming_rules(self) -> NamingRules:
        path = self._get_config_path("naming_rules.json")
        data = self._load_json(path)

        if not data:
            defaults = NamingRules(
                valid_prefixes=[],
                default_maya_names=[],
                name_pattern=re.compile("")
            )
            self.save_naming_rules(defaults)
            return defaults

        return NamingRules(
            valid_prefixes=data.get("ValidPrefixes", []),
            default_maya_names=data.get("DefaultMayaNames", []),
            name_pattern=re.compile(data.get("NamePattern", ""))
        )

    def save_naming_rules(self, naming_rules: NamingRules) -> None:
        path = self._get_config_path("naming_rules.json")

        pattern_text = naming_rules.name_pattern.pattern if naming_rules.name_pattern else ""

        data = {
            "ValidPrefixes": naming_rules.valid_prefixes,
            "DefaultMayaNames": naming_rules.default_maya_names,
            "NamePattern": pattern_text
        }

        self._save_json(path, data)

    # ============================================================
    # NEW FULL BUDGET CONFIG
    # ============================================================

    def load_budgets(self) -> BudgetConfig:
        
        path = self._get_config_path("budgets.json")
        data = self._load_json(path)

        if not data:
            defaults = BudgetConfig()
            self.save_budgets(defaults)
            return defaults

        return BudgetConfig.from_dict(data)

    def save_budgets(self, budgets: BudgetConfig) -> None:
        
        path = self._get_config_path("budgets.json")
        self._save_json(path, budgets.to_dict())


# ============================================================
# PROFILES
# ============================================================

    def load_profiles(self) -> list[ProfileConfig]:
        path = self._get_config_path("profiles.json")
        data = self._load_json(path)

        raw_profiles = data.get("profiles", [])
        return [ProfileConfig.from_dict(p) for p in raw_profiles]

    def load_profile(self, profile_id: str) -> ProfileConfig | None:
        profiles = self.load_profiles()

        for profile in profiles:
            if profile.id == profile_id:
                return profile

        return None