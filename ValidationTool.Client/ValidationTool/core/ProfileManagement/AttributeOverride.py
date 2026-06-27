from dataclasses import dataclass
from typing import Any

@dataclass
class AttributeOverride:
    path: str
    value: Any
    enabled: bool = True
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AttributeOverride":
        return cls(
            path=data.get("path", ""),
            value=data.get("value"),
            enabled=data.get("enabled", True)
        )


def resolve_path_parent(root: object, path: str):
    parts = path.split(".")

    if len(parts) < 2:
        raise ValueError(f"Invalid override path: '{path}'")

    current = root

    for part in parts[:-1]:
        if isinstance(current, dict):
            if part not in current:
                raise KeyError(f"Dict key '{part}' not found while resolving '{path}'")
            current = current[part]
        else:
            if not hasattr(current, part):
                raise AttributeError(f"Attribute '{part}' not found while resolving '{path}'")
            current = getattr(current, part)

    return current, parts[-1]


def apply_override(root: object, override):
    if not override.enabled:
        return

    target_obj, final_name = resolve_path_parent(root, override.path)

    if isinstance(target_obj, dict):
        target_obj[final_name] = override.value
        return

    if not hasattr(target_obj, final_name):
        raise AttributeError(f"Final attribute '{final_name}' not found in path '{override.path}'")

    setattr(target_obj, final_name, override.value)


def apply_overrides(root: object, overrides: list):
    for ov in overrides:
        apply_override(root, ov)



def validate_override_paths(root: object, overrides: list[AttributeOverride]) -> list[str]:
    errors = []

    for ov in overrides:
        try:
            target_obj, final_name = resolve_path_parent(root, ov.path)

            if isinstance(target_obj, dict):
                continue

            if not hasattr(target_obj, final_name):
                errors.append(f"Invalid final attribute in path: {ov.path}")

        except Exception as ex:
            errors.append(f"{ov.path} -> {ex}")

    return errors