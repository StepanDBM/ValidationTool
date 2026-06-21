using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class TextureBudgetDto {
        [JsonPropertyName("texture_count_max")]
        public int TextureCountMax { get; set; } = 50;

        [JsonPropertyName("texture_resolution_max")]
        public int TextureResolutionMax { get; set; } = 4096;

        [JsonPropertyName("texture_resolution_min")]
        public int TextureResolutionMin { get; set; } = 256;

        [JsonPropertyName("textures_4k_max")]
        public int Textures4kMax { get; set; } = 10;

        [JsonPropertyName("textures_8k_max")]
        public int Textures8kMax { get; set; } = 0;

        [JsonPropertyName("total_texture_memory_mb_max")]
        public int TotalTextureMemoryMbMax { get; set; } = 2048;

        [JsonPropertyName("missing_textures_max")]
        public int MissingTexturesMax { get; set; } = 0;

        [JsonPropertyName("non_power_of_two_max")]
        public int NonPowerOfTwoMax { get; set; } = 0;
    }
}