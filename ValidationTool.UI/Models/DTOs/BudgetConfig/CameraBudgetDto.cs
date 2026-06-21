using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class CameraBudgetDto {
        [JsonPropertyName("camera_count_max")]
        public int CameraCountMax { get; set; } = 10;

        [JsonPropertyName("renderable_cameras_max")]
        public int RenderableCamerasMax { get; set; } = 1;

        [JsonPropertyName("overscan_max")]
        public double OverscanMax { get; set; } = 1.1;

        [JsonPropertyName("focal_length_min")]
        public double FocalLengthMin { get; set; } = 12.0;

        [JsonPropertyName("focal_length_max")]
        public double FocalLengthMax { get; set; } = 200.0;

        [JsonPropertyName("default_camera_render_allowed")]
        public bool DefaultCameraRenderAllowed { get; set; } = false;
    }
}
