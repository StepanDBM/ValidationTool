from dataclasses import dataclass


@dataclass
class SamplingSettingsContext:
    camera_aa_samples: int = 0

    diffuse_samples: int = 0
    specular_samples: int = 0
    transmission_samples: int = 0
    sss_samples: int = 0
    volume_samples: int = 0
    light_samples: int = 0

    adaptive_sampling_enabled: bool = False
    adaptive_threshold: float = 0.0
    noise_threshold: float = 0.0

    max_subdiv_iterations: int = 0

    texture_blur: float = 0.0
    texture_sampling_mode: str = ""

    clamp_sample_values: bool = False
    sample_clamp_direct: float = 0.0
    sample_clamp_indirect: float = 0.0
