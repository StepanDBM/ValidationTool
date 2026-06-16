from core.context.SceneContext.sampling_settings_context import SamplingSettingsContext
from misc_tools.DCC.Blender.blender_safeMultiTool import (
    _get_cycles,
    _get_render_engine,
    _get_scene
)

try:
    import bpy
except ImportError:
    bpy = None


def _get_camera_aa_samples(scene, renderer_name: str) -> int:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return int(getattr(cycles, "samples", 0))
            except Exception:
                pass
    return 0


def _get_diffuse_samples(scene, renderer_name: str) -> int:
    return 0


def _get_specular_samples(scene, renderer_name: str) -> int:
    return 0


def _get_transmission_samples(scene, renderer_name: str) -> int:
    return 0


def _get_sss_samples(scene, renderer_name: str) -> int:
    return 0


def _get_volume_samples(scene, renderer_name: str) -> int:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return int(getattr(cycles, "volume_samples", 0))
            except Exception:
                pass
    return 0


def _get_light_samples(scene, renderer_name: str) -> int:
    return 0


def _get_adaptive_sampling_enabled(scene, renderer_name: str) -> bool:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return bool(getattr(cycles, "use_adaptive_sampling", False))
            except Exception:
                pass
    return False


def _get_adaptive_threshold(scene, renderer_name: str) -> float:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return float(getattr(cycles, "adaptive_threshold", 0.0))
            except Exception:
                pass
    return 0.0


def _get_noise_threshold(scene, renderer_name: str) -> float:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return float(getattr(cycles, "adaptive_threshold", 0.0))
            except Exception:
                pass
    return 0.0


def _get_max_subdiv_iterations(scene, renderer_name: str) -> int:
    return 0


def _get_texture_blur(scene, renderer_name: str) -> float:
    return 0.0


def _get_texture_sampling_mode(scene, renderer_name: str) -> str:
    return ""


def _get_clamp_sample_values(scene, renderer_name: str) -> bool:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                direct = float(getattr(cycles, "sample_clamp_direct", 0.0))
            except Exception:
                direct = 0.0

            try:
                indirect = float(getattr(cycles, "sample_clamp_indirect", 0.0))
            except Exception:
                indirect = 0.0

            return abs(direct) > 1e-5 or abs(indirect) > 1e-5

    return False


def _get_sample_clamp_direct(scene, renderer_name: str) -> float:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return float(getattr(cycles, "sample_clamp_direct", 0.0))
            except Exception:
                pass
    return 0.0


def _get_sample_clamp_indirect(scene, renderer_name: str) -> float:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return float(getattr(cycles, "sample_clamp_indirect", 0.0))
            except Exception:
                pass
    return 0.0


def extract_sampling_settings() -> SamplingSettingsContext:
    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    scene = _get_scene()
    if scene is None:
        raise RuntimeError("No Blender scene available.")

    renderer_name = _get_render_engine(scene)

    camera_aa_samples = _get_camera_aa_samples(scene, renderer_name)

    diffuse_samples = _get_diffuse_samples(scene, renderer_name)
    specular_samples = _get_specular_samples(scene, renderer_name)
    transmission_samples = _get_transmission_samples(scene, renderer_name)
    sss_samples = _get_sss_samples(scene, renderer_name)
    volume_samples = _get_volume_samples(scene, renderer_name)
    light_samples = _get_light_samples(scene, renderer_name)

    adaptive_sampling_enabled = _get_adaptive_sampling_enabled(scene, renderer_name)
    adaptive_threshold = _get_adaptive_threshold(scene, renderer_name)
    noise_threshold = _get_noise_threshold(scene, renderer_name)

    max_subdiv_iterations = _get_max_subdiv_iterations(scene, renderer_name)

    texture_blur = _get_texture_blur(scene, renderer_name)
    texture_sampling_mode = _get_texture_sampling_mode(scene, renderer_name)

    clamp_sample_values = _get_clamp_sample_values(scene, renderer_name)
    sample_clamp_direct = _get_sample_clamp_direct(scene, renderer_name)
    sample_clamp_indirect = _get_sample_clamp_indirect(scene, renderer_name)

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