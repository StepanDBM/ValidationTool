"""
SceneSetupContext
    scene_name
    scene_path
    project_path
    dcc_name
    dcc_version

    render_settings: RenderSettingsContext
    output_settings: OutputSettingsContext
    sampling_settings: SamplingSettingsContext
    ray_depth_settings: RayDepthSettingsContext
    color_management: ColorManagementContext
    camera_setup: CameraSetupContext

    render_layers: list[RenderLayerContext]
    aovs: list[AovContext]
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.context.baseContext import BaseContext

from core.context.SceneContext.render_settings_context import RenderSettingsContext
from core.context.SceneContext.output_settings_context import OutputSettingsContext
from core.context.SceneContext.sampling_settings_context import SamplingSettingsContext
from core.context.SceneContext.ray_depth_settings_context import RayDepthSettingsContext
from core.context.SceneContext.color_management_context import ColorManagementContext
from core.context.SceneContext.camera_setup_context import CameraSetupContext
from core.context.SceneContext.render_layer_context import RenderLayerContext
from core.context.SceneContext.aov_context import AovContext


@dataclass
class SceneSetupContext(BaseContext):
    scene_name: str
    project_path: str

    dcc_name: str
    dcc_version: str

    shot_name: str = ""
    sequence_name: str = ""

    render_settings: RenderSettingsContext | None = None
    output_settings: OutputSettingsContext | None = None
    sampling_settings: SamplingSettingsContext | None = None
    ray_depth_settings: RayDepthSettingsContext | None = None
    color_management: ColorManagementContext | None = None
    camera_setup: CameraSetupContext | None = None

    render_layers: list[RenderLayerContext] = field(default_factory=list)
    aovs: list[AovContext] = field(default_factory=list)