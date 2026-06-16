using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.SceneSetup {
    public class RayDepthSettingsDto {
        [JsonPropertyName("total_ray_depth")]
        public int TotalRayDepth { get; set; }

        [JsonPropertyName("diffuse_ray_depth")]
        public int DiffuseRayDepth { get; set; }

        [JsonPropertyName("specular_ray_depth")]
        public int SpecularRayDepth { get; set; }

        [JsonPropertyName("transmission_ray_depth")]
        public int TransmissionRayDepth { get; set; }

        [JsonPropertyName("volume_ray_depth")]
        public int VolumeRayDepth { get; set; }

        [JsonPropertyName("transparency_depth")]
        public int TransparencyDepth { get; set; }

        [JsonPropertyName("sss_depth")]
        public int SssDepth { get; set; }
    }
}