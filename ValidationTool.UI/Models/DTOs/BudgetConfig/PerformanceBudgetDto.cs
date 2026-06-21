using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class PerformanceBudgetDto {
        [JsonPropertyName("validation_runtime_seconds_max")]
        public int ValidationRuntimeSecondsMax { get; set; } = 120;

        [JsonPropertyName("scene_open_time_seconds_max")]
        public int SceneOpenTimeSecondsMax { get; set; } = 60;

        [JsonPropertyName("memory_estimate_mb_max")]
        public int MemoryEstimateMbMax { get; set; } = 8192;

        [JsonPropertyName("render_cost_score_max")]
        public int RenderCostScoreMax { get; set; } = 100;

        [JsonPropertyName("json_report_size_kb_max")]
        public int JsonReportSizeKbMax { get; set; } = 2048;
    }
}