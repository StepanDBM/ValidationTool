from dataclasses import dataclass
from core.context.baseContext import BaseContext
from core.validation_system import AssetType


@dataclass
class LightContext(BaseContext):
    asset_type: AssetType

    light_type: str

    intensity: float
    color: tuple[float, float, float]

    position: tuple[float, float, float]
    rotation: tuple[float, float, float]
    scale: tuple[float, float, float]

    casts_shadows: bool
    emits_diffuse: bool
    emits_specular: bool
    enabled: bool