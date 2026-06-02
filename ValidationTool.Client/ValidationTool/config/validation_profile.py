from dataclasses import dataclass, field
from typing import Set, Optional


@dataclass
class ValidationProfile:
    """
    Defines WHAT should run, not HOW it runs.
    Replaces ad-hoc filtering in runner/UI.
    """

    # Active categories (geometry, uv, transform, naming...)
    enabled_categories: Set[str] = field(default_factory=set)

    # Optional: allow explicit check control
    enabled_checks: Optional[Set[str]] = None
    disabled_checks: Optional[Set[str]] = None

    # Future expansion hooks (no logic yet, the same used in "validation_config.py" that will be rendered useless in the future)
    strict_mode: bool = True

    def allows_category(self, category: str) -> bool:
        if not self.enabled_categories:
            return True  # no restriction = run all

        return category in self.enabled_categories

    def is_check_enabled(self, check_id: str) -> bool:
        if self.enabled_checks is not None:
            return check_id in self.enabled_checks

        if self.disabled_checks is not None:
            return check_id not in self.disabled_checks

        return True