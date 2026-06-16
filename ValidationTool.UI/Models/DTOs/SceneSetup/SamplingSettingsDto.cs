using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.SceneSetup {
    public class SamplingSettingsDto {
        [JsonPropertyName("camera_aa_samples")]
        public int CameraAaSamples { get; set; }

        [JsonPropertyName("diffuse_samples")]
        public int DiffuseSamples { get; set; }

        [JsonPropertyName("specular_samples")]
        public int SpecularSamples { get; set; }

        [JsonPropertyName("transmission_samples")]
        public int TransmissionSamples { get; set; }

        [JsonPropertyName("sss_samples")]
        public int SssSamples { get; set; }

        [JsonPropertyName("volume_samples")]
        public int VolumeSamples { get; set; }

        [JsonPropertyName("light_samples")]
        public int LightSamples { get; set; }

        [JsonPropertyName("adaptive_sampling_enabled")]
        public bool AdaptiveSamplingEnabled { get; set; }

        [JsonPropertyName("adaptive_threshold")]
        public double AdaptiveThreshold { get; set; }

        [JsonPropertyName("noise_threshold")]
        public double NoiseThreshold { get; set; }

        [JsonPropertyName("max_subdiv_iterations")]
        public int MaxSubdivIterations { get; set; }

        [JsonPropertyName("texture_blur")]
        public double TextureBlur { get; set; }

        [JsonPropertyName("texture_sampling_mode")]
        public string TextureSamplingMode { get; set; }

        [JsonPropertyName("clamp_sample_values")]
        public bool ClampSampleValues { get; set; }

        [JsonPropertyName("sample_clamp_direct")]
        public double SampleClampDirect { get; set; }

        [JsonPropertyName("sample_clamp_indirect")]
        public double SampleClampIndirect { get; set; }
    }
}