using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class LightingBudgetDto {
        [JsonPropertyName("light_count_max")]
        public int LightCountMax { get; set; } = 50;

        [JsonPropertyName("shadow_casters_max")]
        public int ShadowCastersMax { get; set; } = 20;

        [JsonPropertyName("area_lights_max")]
        public int AreaLightsMax { get; set; } = 20;

        [JsonPropertyName("environment_lights_max")]
        public int EnvironmentLightsMax { get; set; } = 2;

        [JsonPropertyName("light_groups_max")]
        public int LightGroupsMax { get; set; } = 10;

        [JsonPropertyName("volumetric_lights_max")]
        public int VolumetricLightsMax { get; set; } = 5;
    }
}
