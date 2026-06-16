using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.SceneSetup {
    public class RenderSettingsDto {
        [JsonPropertyName("renderer_name")]
        public string RendererName { get; set; }

        [JsonPropertyName("renderer_version")]
        public string RendererVersion { get; set; }

        [JsonPropertyName("render_device")]
        public string RenderDevice { get; set; }

        [JsonPropertyName("render_mode")]
        public string RenderMode { get; set; }

        [JsonPropertyName("bucket_scanning_mode")]
        public string BucketScanningMode { get; set; }

        [JsonPropertyName("is_progressive")]
        public bool IsProgressive { get; set; }

        [JsonPropertyName("is_bucket")]
        public bool IsBucket { get; set; }

        [JsonPropertyName("denoiser_enabled")]
        public bool DenoiserEnabled { get; set; }

        [JsonPropertyName("denoiser_type")]
        public string DenoiserType { get; set; }

        [JsonPropertyName("adaptive_sampling_enabled")]
        public bool AdaptiveSamplingEnabled { get; set; }

        [JsonPropertyName("adaptive_threshold")]
        public double AdaptiveThreshold { get; set; }

        [JsonPropertyName("noise_threshold")]
        public double NoiseThreshold { get; set; }

        [JsonPropertyName("motion_blur_enabled")]
        public bool MotionBlurEnabled { get; set; }

        [JsonPropertyName("depth_of_field_enabled")]
        public bool DepthOfFieldEnabled { get; set; }

        [JsonPropertyName("thread_mode")]
        public string ThreadMode { get; set; }

        [JsonPropertyName("thread_count")]
        public int ThreadCount { get; set; }

        [JsonPropertyName("use_displacement")]
        public bool UseDisplacement { get; set; }

        [JsonPropertyName("use_subsurface")]
        public bool UseSubsurface { get; set; }

        [JsonPropertyName("use_volumes")]
        public bool UseVolumes { get; set; }

        [JsonPropertyName("use_caustics")]
        public bool UseCaustics { get; set; }

        [JsonPropertyName("texture_auto_tx_enabled")]
        public bool TextureAutoTxEnabled { get; set; }

        [JsonPropertyName("force_linear_textures")]
        public bool ForceLinearTextures { get; set; }

        [JsonPropertyName("render_engine_mode")]
        public string RenderEngineMode { get; set; }

        [JsonPropertyName("tile_size_x")]
        public int TileSizeX { get; set; }

        [JsonPropertyName("tile_size_y")]
        public int TileSizeY { get; set; }
    }
}