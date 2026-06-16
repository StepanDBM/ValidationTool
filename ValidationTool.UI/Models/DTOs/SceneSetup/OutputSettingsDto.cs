using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.SceneSetup {
    public class OutputSettingsDto {
        [JsonPropertyName("output_path")]
        public string OutputPath { get; set; }

        [JsonPropertyName("output_prefix")]
        public string OutputPrefix { get; set; }

        [JsonPropertyName("file_naming_pattern")]
        public string FileNamingPattern { get; set; }

        [JsonPropertyName("image_format")]
        public string ImageFormat { get; set; }

        [JsonPropertyName("bit_depth")]
        public int BitDepth { get; set; }

        [JsonPropertyName("compression")]
        public string Compression { get; set; }

        [JsonPropertyName("compression_quality")]
        public int CompressionQuality { get; set; }

        [JsonPropertyName("color_space")]
        public string ColorSpace { get; set; }

        [JsonPropertyName("has_embedded_metadata")]
        public bool HasEmbeddedMetadata { get; set; }

        [JsonPropertyName("multilayer_enabled")]
        public bool MultilayerEnabled { get; set; }

        [JsonPropertyName("alpha_enabled")]
        public bool AlphaEnabled { get; set; }

        [JsonPropertyName("premultiplied_alpha")]
        public bool PremultipliedAlpha { get; set; }

        [JsonPropertyName("tile_output_enabled")]
        public bool TileOutputEnabled { get; set; }

        [JsonPropertyName("resolution_x")]
        public int ResolutionX { get; set; }

        [JsonPropertyName("resolution_y")]
        public int ResolutionY { get; set; }

        [JsonPropertyName("render_scale_percent")]
        public int RenderScalePercent { get; set; }

        [JsonPropertyName("device_aspect_ratio")]
        public double DeviceAspectRatio { get; set; }

        [JsonPropertyName("pixel_aspect_ratio")]
        public double PixelAspectRatio { get; set; }

        [JsonPropertyName("overscan_enabled")]
        public bool OverscanEnabled { get; set; }

        [JsonPropertyName("overscan_value")]
        public double OverscanValue { get; set; }

        [JsonPropertyName("safe_frame_enabled")]
        public bool SafeFrameEnabled { get; set; }

        [JsonPropertyName("output_writable")]
        public bool OutputWritable { get; set; }
    }
}
