using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class OutputBudgetDto {
        [JsonPropertyName("resolution_x_max")]
        public int ResolutionXMax { get; set; } = 4096;

        [JsonPropertyName("resolution_y_max")]
        public int ResolutionYMax { get; set; } = 4096;

        [JsonPropertyName("resolution_x_min")]
        public int ResolutionXMin { get; set; } = 640;

        [JsonPropertyName("resolution_y_min")]
        public int ResolutionYMin { get; set; } = 360;

        [JsonPropertyName("aov_count_max")]
        public int AovCountMax { get; set; } = 20;

        [JsonPropertyName("required_multilayer_exr")]
        public bool RequiredMultilayerExr { get; set; } = false;

        [JsonPropertyName("output_path_must_be_writable")]
        public bool OutputPathMustBeWritable { get; set; } = true;
    }
}