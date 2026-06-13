from dataclasses import dataclass
"""
Render identity
Render backend/device
Execution mode
sampling behavior toggles
performance-heavy switches
renderer execution configuration
"""

@dataclass
class RenderSettingsContext:
    renderer_name: str = ""
    renderer_version: str = ""

    render_device: str = ""          # CPU / GPU / HYBRID
    render_mode: str = ""            # FINAL / INTERACTIVE / PREVIEW / PROGRESSIVE / BUCKET
    bucket_scanning_mode: str = ""   # TOP / BOTTOM / HILBERT / SPIRAL / etc.

    is_progressive: bool = False
    is_bucket: bool = False

    denoiser_enabled: bool = False
    denoiser_type: str = ""

    adaptive_sampling_enabled: bool = False
    adaptive_threshold: float = 0.0
    noise_threshold: float = 0.0

    motion_blur_enabled: bool = False
    depth_of_field_enabled: bool = False

    thread_mode: str = ""            # AUTO / FIXED / CUSTOM
    thread_count: int = 0

    use_displacement: bool = False
    use_subsurface: bool = False
    use_volumes: bool = False
    use_caustics: bool = False

    texture_auto_tx_enabled: bool = False
    force_linear_textures: bool = False

    render_engine_mode: str = ""     # Optional renderer-specific mode
    tile_size_x: int = 0
    tile_size_y: int = 0