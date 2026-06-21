using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class MaterialBudgetDto {
        [JsonPropertyName("material_slots_max")]
        public int MaterialSlotsMax { get; set; } = 6;

        [JsonPropertyName("unique_materials_max")]
        public int UniqueMaterialsMax { get; set; } = 10;

        [JsonPropertyName("unused_materials_max")]
        public int UnusedMaterialsMax { get; set; } = 0;

        [JsonPropertyName("shader_node_count_max")]
        public int ShaderNodeCountMax { get; set; } = 50;

        [JsonPropertyName("texture_samplers_max")]
        public int TextureSamplersMax { get; set; } = 10;

        [JsonPropertyName("layered_shaders_max")]
        public int LayeredShadersMax { get; set; } = 4;

        [JsonPropertyName("default_material_allowed")]
        public bool DefaultMaterialAllowed { get; set; } = false;
    }
}