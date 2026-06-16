using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.SceneSetup {
    public class ColorManagementDto {
        [JsonPropertyName("view_transform")]
        public string ViewTransform { get; set; }

        [JsonPropertyName("display_device")]
        public string DisplayDevice { get; set; }

        [JsonPropertyName("render_color_space")]
        public string RenderColorSpace { get; set; }

        [JsonPropertyName("texture_color_management_mode")]
        public string TextureColorManagementMode { get; set; }

        [JsonPropertyName("ocio_config")]
        public string OcioConfig { get; set; }

        [JsonPropertyName("linear_workflow_enabled")]
        public bool LinearWorkflowEnabled { get; set; }

        [JsonPropertyName("aces_enabled")]
        public bool AcesEnabled { get; set; }

        [JsonPropertyName("gamma")]
        public double Gamma { get; set; }

        [JsonPropertyName("exposure")]
        public double Exposure { get; set; }

        [JsonPropertyName("look")]
        public string Look { get; set; }
    }
}