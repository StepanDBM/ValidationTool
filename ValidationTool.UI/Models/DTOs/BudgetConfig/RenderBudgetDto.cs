using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class RenderBudgetDto {
        [JsonPropertyName("aa_samples_max")]
        public int AaSamplesMax { get; set; } = 8;

        [JsonPropertyName("diffuse_samples_max")]
        public int DiffuseSamplesMax { get; set; } = 4;

        [JsonPropertyName("specular_samples_max")]
        public int SpecularSamplesMax { get; set; } = 4;

        [JsonPropertyName("transmission_samples_max")]
        public int TransmissionSamplesMax { get; set; } = 4;

        [JsonPropertyName("sss_samples_max")]
        public int SssSamplesMax { get; set; } = 4;

        [JsonPropertyName("volume_samples_max")]
        public int VolumeSamplesMax { get; set; } = 2;

        [JsonPropertyName("adaptive_threshold_max")]
        public double AdaptiveThresholdMax { get; set; } = 0.05;

        [JsonPropertyName("noise_threshold_max")]
        public double NoiseThresholdMax { get; set; } = 0.05;

        [JsonPropertyName("tile_size_max")]
        public int TileSizeMax { get; set; } = 512;

        [JsonPropertyName("ray_depth_total_max")]
        public int RayDepthTotalMax { get; set; } = 8;

        [JsonPropertyName("ray_depth_diffuse_max")]
        public int RayDepthDiffuseMax { get; set; } = 2;

        [JsonPropertyName("ray_depth_specular_max")]
        public int RayDepthSpecularMax { get; set; } = 2;

        [JsonPropertyName("ray_depth_transmission_max")]
        public int RayDepthTransmissionMax { get; set; } = 4;
    }
}