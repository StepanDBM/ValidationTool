from dataclasses import dataclass
from core.context.baseContext import BaseContext

@dataclass
class SceneStatsContext(BaseContext):
    total_meshes: int
    total_cameras: int
    total_lights: int

    total_transforms: int
    total_references: int