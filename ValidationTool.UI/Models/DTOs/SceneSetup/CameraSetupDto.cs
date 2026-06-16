using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.SceneSetup {
    public class CameraSetupDto {
        [JsonPropertyName("active_render_camera")]
        public string ActiveRenderCamera { get; set; }

        [JsonPropertyName("renderable_cameras")]
        public List<string> RenderableCameras { get; set; }

        [JsonPropertyName("default_cameras_present")]
        public List<string> DefaultCamerasPresent { get; set; }

        [JsonPropertyName("camera_overrides_by_layer")]
        public Dictionary<string, string> CameraOverridesByLayer { get; set; }

        [JsonPropertyName("has_duplicate_render_cameras")]
        public bool HasDuplicateRenderCameras { get; set; }

        [JsonPropertyName("has_no_render_camera")]
        public bool HasNoRenderCamera { get; set; }

        [JsonPropertyName("expected_shot_camera")]
        public string ExpectedShotCamera { get; set; }

        [JsonPropertyName("uses_default_render_camera")]
        public bool UsesDefaultRenderCamera { get; set; }
    }
}