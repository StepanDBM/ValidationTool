using System.Collections.Generic;
using System.Text.Json.Serialization;
using ValidationTool.UI.Models.DTOs.SceneSetup;
namespace ValidationTool.UI.Models.DTOs {
    public class SceneSetupDto {
        [JsonPropertyName("name")]
        public string Name { get; set; }

        [JsonPropertyName("object_type")]
        public string ObjectType { get; set; }

        [JsonPropertyName("path")]
        public string Path { get; set; }

        [JsonPropertyName("parent")]
        public string Parent { get; set; }

        [JsonPropertyName("scene_name")]
        public string SceneName { get; set; }

        [JsonPropertyName("scene_path")]
        public string ScenePath { get; set; }

        [JsonPropertyName("project_path")]
        public string ProjectPath { get; set; }

        [JsonPropertyName("dcc_name")]
        public string DccName { get; set; }

        [JsonPropertyName("dcc_version")]
        public string DccVersion { get; set; }

        [JsonPropertyName("shot_name")]
        public string ShotName { get; set; }

        [JsonPropertyName("sequence_name")]
        public string SequenceName { get; set; }

        [JsonPropertyName("render_settings")]
        public RenderSettingsDto RenderSettings { get; set; }

        [JsonPropertyName("output_settings")]
        public OutputSettingsDto OutputSettings { get; set; }

        [JsonPropertyName("sampling_settings")]
        public SamplingSettingsDto SamplingSettings { get; set; }

        [JsonPropertyName("ray_depth_settings")]
        public RayDepthSettingsDto RayDepthSettings { get; set; }

        [JsonPropertyName("color_management")]
        public ColorManagementDto ColorManagement { get; set; }

        [JsonPropertyName("camera_setup")]
        public CameraSetupDto CameraSetup { get; set; }

        [JsonPropertyName("render_layers")]
        public List<RenderLayerDto> RenderLayers { get; set; }

        [JsonPropertyName("aovs")]
        public List<AovDto> Aovs { get; set; }
    }
}