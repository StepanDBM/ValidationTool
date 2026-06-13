from dataclasses import dataclass, field


@dataclass
class RenderLayerContext:
    name: str = ""

    enabled: bool = False
    renderable: bool = False
    is_active: bool = False

    camera_override: str = ""
    material_override: str = ""

    light_overrides: list[str] = field(default_factory=list)
    object_overrides: list[str] = field(default_factory=list)
    collection_overrides: list[str] = field(default_factory=list)

    has_members: bool = False
    member_count: int = 0

    has_valid_name: bool = True
    is_required: bool = False