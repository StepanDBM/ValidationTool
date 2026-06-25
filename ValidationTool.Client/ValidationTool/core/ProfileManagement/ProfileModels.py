from dataclasses import dataclass, field
from typing import List, Any

from core.ProfileManagement.AttributeOverride import AttributeOverride

@dataclass
class ProfileConfig:
    id: str
    name: str
    description: str = ""
    dcc: List[str] = field(default_factory=list)
    enabled_categories: List[str] = field(default_factory=list)
    overrides: List[AttributeOverride] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProfileConfig":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            dcc=data.get("dcc", []),
            enabled_categories=data.get("enabled_categories", []),
            overrides=[
                AttributeOverride.from_dict(x)
                for x in data.get("overrides", [])
            ]
        )

    def allows_category(self, category: str) -> bool:
        if not self.enabled_categories:
            return True

        return category in self.enabled_categories
