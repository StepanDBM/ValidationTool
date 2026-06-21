using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class ColorManagementBudgetDto {
        [JsonPropertyName("aces_required")]
        public bool AcesRequired { get; set; } = false;

        [JsonPropertyName("linear_workflow_required")]
        public bool LinearWorkflowRequired { get; set; } = true;

        [JsonPropertyName("gamma_min")]
        public double GammaMin { get; set; } = 0.8;

        [JsonPropertyName("gamma_max")]
        public double GammaMax { get; set; } = 2.2;

        [JsonPropertyName("exposure_min")]
        public double ExposureMin { get; set; } = -5.0;

        [JsonPropertyName("exposure_max")]
        public double ExposureMax { get; set; } = 5.0;
    }
}