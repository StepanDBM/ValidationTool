from dataclasses import dataclass


@dataclass
class ColorManagementContext:
    view_transform: str = ""              # ACES / Filmic / Standard / etc.
    display_device: str = ""             # sRGB / Rec.709 / Display P3 / etc.
    render_color_space: str = ""         # ACEScg / Linear / Raw / sRGB / etc.

    texture_color_management_mode: str = ""
    ocio_config: str = ""

    linear_workflow_enabled: bool = False
    aces_enabled: bool = False

    gamma: float = 1.0
    exposure: float = 0.0
    look: str = ""                       # Medium High Contrast / None / etc.