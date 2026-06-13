from dataclasses import dataclass, field


@dataclass
class CameraSetupContext:
    active_render_camera: str = ""
    renderable_cameras: list[str] = field(default_factory=list)

    default_cameras_present: list[str] = field(default_factory=list)
    camera_overrides_by_layer: dict[str, str] = field(default_factory=dict)

    has_duplicate_render_cameras: bool = False
    has_no_render_camera: bool = False

    expected_shot_camera: str = ""
    uses_default_render_camera: bool = False