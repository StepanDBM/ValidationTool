from dataclasses import dataclass


@dataclass
class RayDepthSettingsContext:
    total_ray_depth: int = 0

    diffuse_ray_depth: int = 0
    specular_ray_depth: int = 0
    transmission_ray_depth: int = 0
    volume_ray_depth: int = 0

    transparency_depth: int = 0
    sss_depth: int = 0