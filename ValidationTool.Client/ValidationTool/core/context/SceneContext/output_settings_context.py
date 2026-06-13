from dataclasses import dataclass


@dataclass
class OutputSettingsContext:
    output_path: str = ""
    output_prefix: str = ""
    file_naming_pattern: str = ""

    image_format: str = ""           # EXR / PNG / JPEG / TIFF / etc.
    bit_depth: int = 0               # 8 / 16 / 32

    compression: str = ""            # ZIP / PIZ / DWAA / NONE / etc.
    compression_quality: int = 0     # optional quality/compression level

    color_space: str = ""            # sRGB / ACEScg / Linear / Raw / etc.
    has_embedded_metadata: bool = False

    multilayer_enabled: bool = False
    alpha_enabled: bool = False
    premultiplied_alpha: bool = False

    tile_output_enabled: bool = False

    resolution_x: int = 0
    resolution_y: int = 0
    render_scale_percent: int = 100

    device_aspect_ratio: float = 1.0
    pixel_aspect_ratio: float = 1.0

    overscan_enabled: bool = False
    overscan_value: float = 0.0

    safe_frame_enabled: bool = False

    output_writable: bool = False