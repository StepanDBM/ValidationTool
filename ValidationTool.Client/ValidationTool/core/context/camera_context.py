from dataclasses import dataclass
from core.context.baseContext import BaseContext
from core.validation_system import AssetType


@dataclass
class CameraContext(BaseContext):
    asset_type: AssetType

    camera_type: str

    focal_length: float
    near_clip: float
    far_clip: float

    position: tuple[float, float, float]
    rotation: tuple[float, float, float]
    scale: tuple[float, float, float]

    is_render_camera: bool