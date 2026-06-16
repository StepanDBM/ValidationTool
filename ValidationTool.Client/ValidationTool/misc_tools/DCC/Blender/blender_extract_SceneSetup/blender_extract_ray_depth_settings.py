from core.context.SceneContext.ray_depth_settings_context import RayDepthSettingsContext
from misc_tools.DCC.Blender.blender_safeMultiTool import (
    _get_scene,
    _get_cycles,
    _get_render_engine
)

try:
    import bpy
except ImportError:
    bpy = None


def _get_total_ray_depth(scene, renderer_name: str) -> int:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return int(getattr(cycles, "max_bounces", 0))
            except Exception:
                pass
    return 0


def _get_diffuse_ray_depth(scene, renderer_name: str) -> int:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return int(getattr(cycles, "diffuse_bounces", 0))
            except Exception:
                pass
    return 0


def _get_specular_ray_depth(scene, renderer_name: str) -> int:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return int(getattr(cycles, "glossy_bounces", 0))
            except Exception:
                pass
    return 0


def _get_transmission_ray_depth(scene, renderer_name: str) -> int:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return int(getattr(cycles, "transmission_bounces", 0))
            except Exception:
                pass
    return 0


def _get_volume_ray_depth(scene, renderer_name: str) -> int:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return int(getattr(cycles, "volume_bounces", 0))
            except Exception:
                pass
    return 0


def _get_transparency_depth(scene, renderer_name: str) -> int:
    if renderer_name == "CYCLES":
        cycles = _get_cycles(scene)
        if cycles is not None:
            try:
                return int(getattr(cycles, "transparent_max_bounces", 0))
            except Exception:
                pass
    return 0


def _get_sss_depth(scene, renderer_name: str) -> int:
    return 0


def extract_ray_depth_settings() -> RayDepthSettingsContext:
    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    scene = _get_scene()
    if scene is None:
        raise RuntimeError("No Blender scene available.")

    renderer_name = _get_render_engine(scene)

    total_ray_depth = _get_total_ray_depth(scene, renderer_name)
    diffuse_ray_depth = _get_diffuse_ray_depth(scene, renderer_name)
    specular_ray_depth = _get_specular_ray_depth(scene, renderer_name)
    transmission_ray_depth = _get_transmission_ray_depth(scene, renderer_name)
    volume_ray_depth = _get_volume_ray_depth(scene, renderer_name)
    transparency_depth = _get_transparency_depth(scene, renderer_name)
    sss_depth = _get_sss_depth(scene, renderer_name)

    return RayDepthSettingsContext(
        total_ray_depth=total_ray_depth,
        diffuse_ray_depth=diffuse_ray_depth,
        specular_ray_depth=specular_ray_depth,
        transmission_ray_depth=transmission_ray_depth,
        volume_ray_depth=volume_ray_depth,
        transparency_depth=transparency_depth,
        sss_depth=sss_depth,
    )