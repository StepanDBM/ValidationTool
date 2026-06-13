from core.context.SceneContext.sampling_settings_context import SamplingSettingsContext

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _safe_get_bool,
    _safe_get_float,
    _safe_get_int,
    _safe_get_str,
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


_TEXTURE_SAMPLING_MODE_MAP = {
    0: "AUTO",
    1: "MIPMAP",
    2: "LINEAR",
    3: "CLOSEST",
}


def _first_existing_attr(attr_names: list[str]) -> str:
    for attr in attr_names:
        try:
            if attr and cmds.objExists(attr):
                return attr
        except Exception:
            continue
    return ""


def _safe_enum_text(attr_names: list[str], mapping: dict[int, str], default: str = "") -> str:
    attr = _first_existing_attr(attr_names)
    if not attr:
        return default

    value = _safe_get_int(attr, 0)
    return mapping.get(value, default or str(value))


def _get_current_renderer() -> str:
    return _safe_get_str("defaultRenderGlobals.currentRenderer", "").lower()


def _get_camera_aa_samples(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.AASamples",
            ]),
            0,
        )
    return 0


def _get_diffuse_samples(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GIDiffuseSamples",
            ]),
            0,
        )
    return 0


def _get_specular_samples(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GISpecularSamples",
            ]),
            0,
        )
    return 0


def _get_transmission_samples(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GITransmissionSamples",
            ]),
            0,
        )
    return 0


def _get_sss_samples(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GISssSamples",
                "defaultArnoldRenderOptions.GISSSSamples",
            ]),
            0,
        )
    return 0


def _get_volume_samples(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GIVolumeSamples",
            ]),
            0,
        )
    return 0


def _get_light_samples(renderer_name: str) -> int:
    if renderer_name == "arnold":
        # Arnold does not expose a truly global "light samples" in the same way as the other GI sample blocks.
        # Keep this best-effort for scene-level inspection.
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.GILightSamples",
            ]),
            0,
        )
    return 0


def _get_adaptive_sampling_enabled(renderer_name: str) -> bool:
    if renderer_name == "arnold":
        return _safe_get_bool(
            _first_existing_attr([
                "defaultArnoldRenderOptions.enableAdaptiveSampling",
                "defaultArnoldRenderOptions.adaptiveSampling",
            ]),
            False,
        )
    return False


def _get_adaptive_threshold(renderer_name: str) -> float:
    if renderer_name == "arnold":
        return _safe_get_float(
            _first_existing_attr([
                "defaultArnoldRenderOptions.AAAdaptiveThreshold",
                "defaultArnoldRenderOptions.adaptiveThreshold",
            ]),
            0.0,
        )
    return 0.0


def _get_noise_threshold(renderer_name: str) -> float:
    if renderer_name == "arnold":
        return _safe_get_float(
            _first_existing_attr([
                "defaultArnoldRenderOptions.AAAdaptiveThreshold",
                "defaultArnoldRenderOptions.noiseThreshold",
            ]),
            0.0,
        )
    return 0.0


def _get_max_subdiv_iterations(renderer_name: str) -> int:
    if renderer_name == "arnold":
        return _safe_get_int(
            _first_existing_attr([
                "defaultArnoldRenderOptions.maxSubdivisions",
                "defaultArnoldRenderOptions.maxSubdivIterations",
            ]),
            0,
        )
    return 0


def _get_texture_blur(renderer_name: str) -> float:
    if renderer_name == "arnold":
        return _safe_get_float(
            _first_existing_attr([
                "defaultArnoldRenderOptions.textureBlur",
                "defaultArnoldRenderOptions.textureBlurriness",
            ]),
            0.0,
        )
    return 0.0


def _get_texture_sampling_mode(renderer_name: str) -> str:
    if renderer_name == "arnold":
        return _safe_enum_text(
            [
                "defaultArnoldRenderOptions.textureFiltering",
                "defaultArnoldRenderOptions.textureFilterType",
            ],
            _TEXTURE_SAMPLING_MODE_MAP,
            "",
        )
    return ""


def _get_clamp_sample_values(renderer_name: str) -> bool:
    if renderer_name == "arnold":
        attr = _first_existing_attr([
            "defaultArnoldRenderOptions.AASampleClamp",
            "defaultArnoldRenderOptions.clampSampleValues",
        ])
        if not attr:
            return False

        # Treat non-zero clamp values as enabled if the renderer exposes the clamp scalar itself.
        value = _safe_get_float(attr, 0.0)
        return abs(value) > 1e-5

    return False


def _get_sample_clamp_direct(renderer_name: str) -> float:
    if renderer_name == "arnold":
        return _safe_get_float(
            _first_existing_attr([
                "defaultArnoldRenderOptions.AASampleClamp",
                "defaultArnoldRenderOptions.sampleClampDirect",
            ]),
            0.0,
        )
    return 0.0


def _get_sample_clamp_indirect(renderer_name: str) -> float:
    if renderer_name == "arnold":
        return _safe_get_float(
            _first_existing_attr([
                "defaultArnoldRenderOptions.indirectSampleClamp",
                "defaultArnoldRenderOptions.sampleClampIndirect",
            ]),
            0.0,
        )
    return 0.0


def extract_sampling_settings() -> SamplingSettingsContext:
    """
    Extract renderer sampling configuration from the current Maya scene.

    Focuses on:
    - camera / AA samples
    - diffuse/specular/transmission/SSS/volume samples
    - adaptive sampling state and thresholds
    - subdivision limits
    - texture sampling behavior
    - sample clamping
    """

    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    renderer_name = _get_current_renderer()

    camera_aa_samples = _get_camera_aa_samples(renderer_name)

    diffuse_samples = _get_diffuse_samples(renderer_name)
    specular_samples = _get_specular_samples(renderer_name)
    transmission_samples = _get_transmission_samples(renderer_name)
    sss_samples = _get_sss_samples(renderer_name)
    volume_samples = _get_volume_samples(renderer_name)
    light_samples = _get_light_samples(renderer_name)

    adaptive_sampling_enabled = _get_adaptive_sampling_enabled(renderer_name)
    adaptive_threshold = _get_adaptive_threshold(renderer_name)
    noise_threshold = _get_noise_threshold(renderer_name)

    max_subdiv_iterations = _get_max_subdiv_iterations(renderer_name)

    texture_blur = _get_texture_blur(renderer_name)
    texture_sampling_mode = _get_texture_sampling_mode(renderer_name)

    clamp_sample_values = _get_clamp_sample_values(renderer_name)
    sample_clamp_direct = _get_sample_clamp_direct(renderer_name)
    sample_clamp_indirect = _get_sample_clamp_indirect(renderer_name)

    return SamplingSettingsContext(
        camera_aa_samples=camera_aa_samples,
        diffuse_samples=diffuse_samples,
        specular_samples=specular_samples,
        transmission_samples=transmission_samples,
        sss_samples=sss_samples,
        volume_samples=volume_samples,
        light_samples=light_samples,
        adaptive_sampling_enabled=adaptive_sampling_enabled,
        adaptive_threshold=adaptive_threshold,
        noise_threshold=noise_threshold,
        max_subdiv_iterations=max_subdiv_iterations,
        texture_blur=texture_blur,
        texture_sampling_mode=texture_sampling_mode,
        clamp_sample_values=clamp_sample_values,
        sample_clamp_direct=sample_clamp_direct,
        sample_clamp_indirect=sample_clamp_indirect,
    )