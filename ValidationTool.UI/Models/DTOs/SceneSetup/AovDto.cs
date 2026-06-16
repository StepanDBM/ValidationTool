using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.SceneSetup {
    public class AovDto {
        [JsonPropertyName("name")]
        public string Name { get; set; }

        [JsonPropertyName("enabled")]
        public bool Enabled { get; set; }

        [JsonPropertyName("data_type")]
        public string DataType { get; set; }

        [JsonPropertyName("source_type")]
        public string SourceType { get; set; }

        [JsonPropertyName("driver")]
        public string Driver { get; set; }

        [JsonPropertyName("filter")]
        public string Filter { get; set; }

        [JsonPropertyName("light_group")]
        public string LightGroup { get; set; }

        [JsonPropertyName("is_builtin")]
        public bool IsBuiltin { get; set; }

        [JsonPropertyName("output_path")]
        public string OutputPath { get; set; }

        [JsonPropertyName("output_prefix")]
        public string OutputPrefix { get; set; }

        [JsonPropertyName("has_valid_name")]
        public bool HasValidName { get; set; }

        [JsonPropertyName("is_required")]
        public bool IsRequired { get; set; }
    }
}